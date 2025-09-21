#!/usr/bin/env python3
"""
vcf-to-obsidian-vcf-contacts

A Python script that batch-converts a folder containing VCF files into Markdown files
that are compatible with obsidian-vcf-contacts plugin for ObsidianMD.

Usage:
    python vcf_to_obsidian.py <source_vcf_directory> <destination_obsidian_folder>

Author: Ian Dennis Miller
License: MIT
"""

import argparse
import os
import sys
from pathlib import Path
import re
from jinja2 import Environment, FileSystemLoader, Template
import vobject


def parse_vcf_file_vobject(vcf_path):
    """
    Parse a VCF file using vobject library for better vCard 4.0 support.
    
    Args:
        vcf_path (Path): Path to the VCF file
        
    Returns:
        dict: Parsed contact data
    """
    contact_data = {
        'uid': '',
        'full_name': '',
        'given_name': '',
        'family_name': '',
        'organization': '',
        'phone_numbers': [],
        'email_addresses': [],
        'addresses': [],
        'notes': '',
        'url': '',
        'birthday': '',
        'photo': '',
        'categories': '',
        'version': '',
        # Store raw field data with type information
        'raw_emails': {},  # Will store email addresses with their types
        'raw_phones': {},  # Will store phone numbers with their types  
        'raw_urls': {},    # Will store URLs with their types
        'raw_addresses': {}  # Will store addresses with their types and components
    }
    
    try:
        with open(vcf_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        vcard = vobject.readOne(content)
        
        # Extract UID
        if hasattr(vcard, 'uid'):
            contact_data['uid'] = vcard.uid.value
        
        # Extract Full Name
        if hasattr(vcard, 'fn'):
            contact_data['full_name'] = vcard.fn.value
        
        # Extract structured name
        if hasattr(vcard, 'n'):
            n = vcard.n.value
            contact_data['family_name'] = n.family if n.family else ''
            contact_data['given_name'] = n.given if n.given else ''
        
        # Extract organization
        if hasattr(vcard, 'org'):
            org_value = vcard.org.value
            if isinstance(org_value, list) and org_value:
                contact_data['organization'] = org_value[0]
            elif isinstance(org_value, str):
                contact_data['organization'] = org_value
        
        # Extract phone numbers
        if hasattr(vcard, 'tel_list'):
            for tel in vcard.tel_list:
                contact_data['phone_numbers'].append(tel.value)
                
                # Extract type information for raw_phones
                type_label = 'DEFAULT'
                if hasattr(tel, 'params') and 'TYPE' in tel.params:
                    type_values = tel.params['TYPE']
                    if isinstance(type_values, list) and type_values:
                        type_label = type_values[0].upper()
                    elif isinstance(type_values, str):
                        type_label = type_values.upper()
                
                field_key = f"TEL[{type_label}]"
                contact_data['raw_phones'][field_key] = tel.value
        
        # Extract email addresses
        if hasattr(vcard, 'email_list'):
            for email in vcard.email_list:
                contact_data['email_addresses'].append(email.value)
                
                # Extract type information for raw_emails
                type_label = 'DEFAULT'
                if hasattr(email, 'params') and 'TYPE' in email.params:
                    type_values = email.params['TYPE']
                    if isinstance(type_values, list) and type_values:
                        type_label = type_values[0].upper()
                    elif isinstance(type_values, str):
                        type_label = type_values.upper()
                
                field_key = f"EMAIL[{type_label}]"
                contact_data['raw_emails'][field_key] = email.value
        
        # Extract addresses
        if hasattr(vcard, 'adr_list'):
            for adr in vcard.adr_list:
                adr_value = adr.value
                # Combine non-empty address parts
                address_parts = []
                if adr_value.street:
                    address_parts.append(adr_value.street)
                if adr_value.city:
                    address_parts.append(adr_value.city)
                if adr_value.region:
                    address_parts.append(adr_value.region)
                if adr_value.code:
                    address_parts.append(adr_value.code)
                if adr_value.country:
                    address_parts.append(adr_value.country)
                
                if address_parts:
                    contact_data['addresses'].append(', '.join(address_parts))
                
                # Extract type information for raw_addresses
                type_label = 'DEFAULT'
                if hasattr(adr, 'params') and 'TYPE' in adr.params:
                    type_values = adr.params['TYPE']
                    if isinstance(type_values, list) and type_values:
                        type_label = type_values[0].upper()
                    elif isinstance(type_values, str):
                        type_label = type_values.upper()
                
                # Store address components
                base_key = f"ADR[{type_label}]"
                if adr_value.box:
                    contact_data['raw_addresses'][f"{base_key}.POBOX"] = adr_value.box
                if adr_value.extended:
                    contact_data['raw_addresses'][f"{base_key}.EXTENDED"] = adr_value.extended
                if adr_value.street:
                    contact_data['raw_addresses'][f"{base_key}.STREET"] = adr_value.street
                if adr_value.city:
                    contact_data['raw_addresses'][f"{base_key}.LOCALITY"] = adr_value.city
                if adr_value.region:
                    contact_data['raw_addresses'][f"{base_key}.REGION"] = adr_value.region
                if adr_value.code:
                    contact_data['raw_addresses'][f"{base_key}.POSTAL"] = adr_value.code
                if adr_value.country:
                    contact_data['raw_addresses'][f"{base_key}.COUNTRY"] = adr_value.country
        
        # Extract notes
        if hasattr(vcard, 'note'):
            contact_data['notes'] = vcard.note.value
        
        # Extract URL
        if hasattr(vcard, 'url'):
            contact_data['url'] = vcard.url.value
            
            # Extract type information for raw_urls
            type_label = 'DEFAULT'
            if hasattr(vcard.url, 'params') and 'TYPE' in vcard.url.params:
                type_values = vcard.url.params['TYPE']
                if isinstance(type_values, list) and type_values:
                    type_label = type_values[0].upper()
                elif isinstance(type_values, str):
                    type_label = type_values.upper()
            
            field_key = f"URL[{type_label}]"
            contact_data['raw_urls'][field_key] = vcard.url.value
        
        # Extract birthday
        if hasattr(vcard, 'bday'):
            contact_data['birthday'] = str(vcard.bday.value)
        
        # Extract photo
        if hasattr(vcard, 'photo'):
            contact_data['photo'] = vcard.photo.value
        
        # Extract categories
        if hasattr(vcard, 'categories'):
            contact_data['categories'] = vcard.categories.value
        
        # Extract version
        if hasattr(vcard, 'version'):
            contact_data['version'] = vcard.version.value
            
    except Exception as e:
        print(f"Error parsing VCF file {vcf_path} with vobject: {e}")
        
    return contact_data


def parse_vcf_file(vcf_path):
    """
    Parse a VCF file and extract contact information.
    Uses vobject library for vCard parsing.
    
    Args:
        vcf_path (Path): Path to the VCF file
        
    Returns:
        dict: Parsed contact data
    """
    return parse_vcf_file_vobject(vcf_path)


def generate_obsidian_markdown(contact_data, template_path=None):
    """
    Generate Markdown content compatible with obsidian-vcf-contacts plugin.
    
    Args:
        contact_data (dict): Parsed contact data
        template_path (str, optional): Path to custom Jinja2 template file.
                                     If None, uses default template.
        
    Returns:
        str: Markdown content with frontmatter
    """
    # Use full name as title, fallback to given + family name
    title = contact_data['full_name']
    if not title and (contact_data['given_name'] or contact_data['family_name']):
        title = f"{contact_data['given_name']} {contact_data['family_name']}".strip()
    
    # Prepare template variables
    template_vars = {
        'title': title,
        'uid': contact_data['uid'],
        'full_name': contact_data['full_name'],
        'given_name': contact_data['given_name'],
        'family_name': contact_data['family_name'],
        'organization': contact_data['organization'],
        'phone_numbers': contact_data['phone_numbers'],
        'email_addresses': contact_data['email_addresses'],
        'addresses': contact_data['addresses'],
        'notes': contact_data['notes'],
        'url': contact_data['url'],
        'birthday': contact_data['birthday'],
        'photo': contact_data['photo'],
        'categories': contact_data['categories'],
        'version': contact_data['version'],
        'raw_emails': contact_data['raw_emails'],
        'raw_phones': contact_data['raw_phones'],
        'raw_urls': contact_data['raw_urls'],
        'raw_addresses': contact_data['raw_addresses']
    }
    
    if template_path and Path(template_path).exists():
        # Use custom template
        template_dir = Path(template_path).parent
        template_name = Path(template_path).name
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
    else:
        # Use default template
        script_dir = Path(__file__).parent
        template_dir = script_dir / 'templates'
        if template_dir.exists():
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('default.md.j2')
        else:
            # Fallback to inline template if templates directory doesn't exist
            template_str = """---
{%- if family_name %}
N.FN: {{ family_name }}
{%- endif %}
{%- if given_name %}
N.GN: {{ given_name }}
{%- endif %}
{%- if full_name %}
FN: {{ full_name }}
{%- endif %}
{%- if photo %}
PHOTO: {{ photo }}
{%- endif %}
{%- for email_key, email_value in raw_emails.items() %}
"{{ email_key }}": {{ email_value }}
{%- endfor %}
{%- for phone_key, phone_value in raw_phones.items() %}
"{{ phone_key }}": "{{ phone_value }}"
{%- endfor %}
{%- if birthday %}
BDAY: {{ birthday }}
{%- endif %}
{%- for url_key, url_value in raw_urls.items() %}
"{{ url_key }}": {{ url_value }}
{%- endfor %}
{%- if organization %}
ORG: {{ organization }}
{%- endif %}
{%- for addr_key, addr_value in raw_addresses.items() %}
"{{ addr_key }}": {% if addr_key.endswith('.POSTAL') %}"{{ addr_value }}"{% else %}{{ addr_value }}{% endif %}
{%- endfor %}
{%- if categories %}
CATEGORIES: {{ categories }}
{%- endif %}
{%- if uid %}
UID: {{ uid }}
{%- endif %}
{%- if version %}
VERSION: "{{ version }}"
{%- endif %}

---
{%- if notes or categories %}
#### Notes

{%- if categories %}
{%- set category_list = categories.split(',') %}
#Contact{% for category in category_list %} #{{ category.strip() }}{% endfor %}
{%- else %}
#Contact
{%- endif %}
{%- endif %}"""
            template = Template(template_str)
    
    # Render the template with contact data
    content = template.render(**template_vars)
    
    # Clean up any extra whitespace/newlines at the end
    return content.strip() + '\n'


def find_existing_files_with_uid(output_dir, uid):
    """
    Find existing Markdown files in output directory that have the same UID.
    
    Args:
        output_dir (Path): Output directory to search
        uid (str): UID to search for
        
    Returns:
        list: List of Path objects for files with matching UID
    """
    if not uid:
        return []
    
    matching_files = []
    md_files = output_dir.glob("*.md")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for UID line in the content
                if f"UID: {uid}" in content:
                    matching_files.append(md_file)
        except Exception:
            # Skip files that can't be read
            continue
    
    return matching_files


def convert_vcf_to_markdown(vcf_path, output_dir, template_path=None):
    """
    Convert a single VCF file to Markdown format.
    
    Args:
        vcf_path (Path): Path to the VCF file
        output_dir (Path): Output directory for Markdown files
        template_path (str, optional): Path to custom Jinja2 template file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Parse VCF file
        contact_data = parse_vcf_file(vcf_path)
        
        # Generate Markdown content
        markdown_content = generate_obsidian_markdown(contact_data, template_path)
        
        # Create output filename based on FN (preferred) or UID (fallback)
        contact_name = contact_data['full_name']
        if not contact_name and (contact_data['given_name'] or contact_data['family_name']):
            contact_name = f"{contact_data['given_name']} {contact_data['family_name']}".strip()
        
        if contact_name:
            # Use contact name as filename (preferred)
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', contact_name)
            output_file = output_dir / f"{safe_filename}.md"
        elif contact_data['uid']:
            # Fallback to UID if no contact name is available
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', contact_data['uid'])
            output_file = output_dir / f"{safe_filename}.md"
        else:
            # Final fallback to VCF filename if neither name nor UID is available
            safe_filename = vcf_path.stem
            output_file = output_dir / f"{safe_filename}.md"
        
        # Remove existing files with the same UID if the filename would be different
        if contact_data['uid']:
            existing_files = find_existing_files_with_uid(output_dir, contact_data['uid'])
            for existing_file in existing_files:
                if existing_file != output_file:
                    try:
                        existing_file.unlink()
                        print(f"Removed old file: {existing_file.name}")
                    except Exception as e:
                        print(f"Warning: Could not remove old file {existing_file.name}: {e}")
        
        # Write Markdown file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Converted: {vcf_path.name} -> {output_file.name}")
        return True
        
    except Exception as e:
        print(f"Error converting {vcf_path}: {e}")
        return False


def main():
    """Main function to handle command-line interface and batch conversion."""
    parser = argparse.ArgumentParser(
        description="Convert VCF files to Markdown format for obsidian-vcf-contacts plugin"
    )
    parser.add_argument(
        "source_dir",
        help="Source directory containing VCF files"
    )
    parser.add_argument(
        "dest_dir", 
        help="Destination directory for Markdown files"
    )
    parser.add_argument(
        "--template", "-t",
        help="Path to custom Jinja2 template file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate source directory
    source_path = Path(args.source_dir)
    if not source_path.exists():
        print(f"Error: Source directory '{source_path}' does not exist.")
        sys.exit(1)
    if not source_path.is_dir():
        print(f"Error: Source path '{source_path}' is not a directory.")
        sys.exit(1)
    
    # Create destination directory if it doesn't exist
    dest_path = Path(args.dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Find all VCF files
    vcf_files = list(source_path.glob("*.vcf")) + list(source_path.glob("*.VCF"))
    
    if not vcf_files:
        print(f"No VCF files found in '{source_path}'")
        sys.exit(1)
    
    print(f"Found {len(vcf_files)} VCF file(s) in '{source_path}'")
    print(f"Converting to Markdown in '{dest_path}'")
    
    # Convert each VCF file
    success_count = 0
    for vcf_file in vcf_files:
        if args.verbose:
            print(f"Processing: {vcf_file}")
        
        if convert_vcf_to_markdown(vcf_file, dest_path, args.template):
            success_count += 1
    
    print(f"Successfully converted {success_count}/{len(vcf_files)} files.")


if __name__ == "__main__":
    main()
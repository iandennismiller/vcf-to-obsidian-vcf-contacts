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


def parse_vcf_file(vcf_path):
    """
    Parse a VCF file and extract contact information.
    
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
        'birthday': ''
    }
    
    try:
        with open(vcf_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Parse VCF properties
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('FN:'):
                # Full Name
                contact_data['full_name'] = line[3:].strip()
            elif line.startswith('UID:'):
                # Unique Identifier
                contact_data['uid'] = line[4:].strip()
            elif line.startswith('N:'):
                # Structured Name (Family;Given;Additional;Prefix;Suffix)
                name_parts = line[2:].split(';')
                if len(name_parts) >= 2:
                    contact_data['family_name'] = name_parts[0].strip()
                    contact_data['given_name'] = name_parts[1].strip()
            elif line.startswith('ORG:'):
                # Organization
                contact_data['organization'] = line[4:].strip()
            elif line.startswith('TEL'):
                # Phone numbers
                phone_match = re.search(r'TEL[^:]*:(.+)', line)
                if phone_match:
                    contact_data['phone_numbers'].append(phone_match.group(1).strip())
            elif line.startswith('EMAIL'):
                # Email addresses
                email_match = re.search(r'EMAIL[^:]*:(.+)', line)
                if email_match:
                    contact_data['email_addresses'].append(email_match.group(1).strip())
            elif line.startswith('ADR'):
                # Addresses
                addr_match = re.search(r'ADR[^:]*:(.+)', line)
                if addr_match:
                    # ADR format: PO Box;Extended;Street;City;State;Postal Code;Country
                    addr_parts = addr_match.group(1).split(';')
                    # Combine non-empty parts into a readable address
                    address = ', '.join([part.strip() for part in addr_parts if part.strip()])
                    if address:
                        contact_data['addresses'].append(address)
            elif line.startswith('NOTE:'):
                # Notes
                contact_data['notes'] = line[5:].strip()
            elif line.startswith('URL:'):
                # URL
                contact_data['url'] = line[4:].strip()
            elif line.startswith('BDAY:'):
                # Birthday
                contact_data['birthday'] = line[5:].strip()
                
    except Exception as e:
        print(f"Error parsing VCF file {vcf_path}: {e}")
        
    return contact_data


def generate_obsidian_markdown(contact_data):
    """
    Generate Markdown content compatible with obsidian-vcf-contacts plugin.
    
    Args:
        contact_data (dict): Parsed contact data
        
    Returns:
        str: Markdown content with frontmatter
    """
    # Use full name as title, fallback to given + family name
    title = contact_data['full_name']
    if not title and (contact_data['given_name'] or contact_data['family_name']):
        title = f"{contact_data['given_name']} {contact_data['family_name']}".strip()
    
    # Create frontmatter for obsidian-vcf-contacts
    frontmatter = "---\n"
    frontmatter += "vcf-contact: true\n"
    
    if title:
        frontmatter += f"name: \"{title}\"\n"
    if contact_data['given_name']:
        frontmatter += f"given-name: \"{contact_data['given_name']}\"\n"
    if contact_data['family_name']:
        frontmatter += f"family-name: \"{contact_data['family_name']}\"\n"
    if contact_data['organization']:
        frontmatter += f"organization: \"{contact_data['organization']}\"\n"
    if contact_data['phone_numbers']:
        frontmatter += "phone-numbers:\n"
        for phone in contact_data['phone_numbers']:
            frontmatter += f"  - \"{phone}\"\n"
    if contact_data['email_addresses']:
        frontmatter += "email-addresses:\n"
        for email in contact_data['email_addresses']:
            frontmatter += f"  - \"{email}\"\n"
    if contact_data['addresses']:
        frontmatter += "addresses:\n"
        for address in contact_data['addresses']:
            frontmatter += f"  - \"{address}\"\n"
    if contact_data['url']:
        frontmatter += f"url: \"{contact_data['url']}\"\n"
    if contact_data['birthday']:
        frontmatter += f"birthday: \"{contact_data['birthday']}\"\n"
    
    frontmatter += "---\n\n"
    
    # Generate markdown content
    content = f"# {title}\n\n"
    
    if contact_data['organization']:
        content += f"**Organization:** {contact_data['organization']}\n\n"
    
    if contact_data['phone_numbers']:
        content += "**Phone Numbers:**\n"
        for phone in contact_data['phone_numbers']:
            content += f"- {phone}\n"
        content += "\n"
    
    if contact_data['email_addresses']:
        content += "**Email Addresses:**\n"
        for email in contact_data['email_addresses']:
            content += f"- {email}\n"
        content += "\n"
    
    if contact_data['addresses']:
        content += "**Addresses:**\n"
        for address in contact_data['addresses']:
            content += f"- {address}\n"
        content += "\n"
    
    if contact_data['url']:
        content += f"**Website:** {contact_data['url']}\n\n"
    
    if contact_data['birthday']:
        content += f"**Birthday:** {contact_data['birthday']}\n\n"
    
    if contact_data['notes']:
        content += f"**Notes:**\n{contact_data['notes']}\n\n"
    
    return frontmatter + content


def convert_vcf_to_markdown(vcf_path, output_dir):
    """
    Convert a single VCF file to Markdown format.
    
    Args:
        vcf_path (Path): Path to the VCF file
        output_dir (Path): Output directory for Markdown files
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Parse VCF file
        contact_data = parse_vcf_file(vcf_path)
        
        # Generate Markdown content
        markdown_content = generate_obsidian_markdown(contact_data)
        
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
        
        if convert_vcf_to_markdown(vcf_file, dest_path):
            success_count += 1
    
    print(f"Successfully converted {success_count}/{len(vcf_files)} files.")


if __name__ == "__main__":
    main()
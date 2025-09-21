#!/usr/bin/env python3
"""
vcf-to-obsidian-vcf-contacts

A Python script that batch-converts a folder containing VCF files into Markdown files
that are compatible with obsidian-vcf-contacts plugin for ObsidianMD.

Usage:
    python vcf_to_obsidian.py --folder <source_directory> --obsidian <destination_folder>
    python vcf_to_obsidian.py --file <vcf_file> --obsidian <destination_folder>
    python vcf_to_obsidian.py --folder <dir1> --folder <dir2> --file <file1.vcf> --obsidian <destination>

Author: Ian Dennis Miller
License: MIT
"""

import click
import os
import sys
from pathlib import Path
import re
import vobject



def generate_obsidian_markdown(vcard):
    """
    Generate Markdown content compatible with obsidian-vcf-contacts plugin.
    Works directly with vobject instead of intermediate representation.
    
    Args:
        vcard: vobject vCard object
        
    Returns:
        str: Markdown content with frontmatter
    """
    # Build the markdown content directly from vobject
    lines = ["---"]
    
    # Extract structured name
    if hasattr(vcard, 'n') and vcard.n.value:
        n = vcard.n.value
        if hasattr(n, 'family') and n.family:
            lines.append(f"N.FN: {n.family}")
        if hasattr(n, 'given') and n.given:
            lines.append(f"N.GN: {n.given}")
    
    # Extract Full Name
    if hasattr(vcard, 'fn') and vcard.fn.value:
        lines.append(f"FN: {vcard.fn.value}")
    
    # Extract photo
    if hasattr(vcard, 'photo') and vcard.photo.value:
        lines.append(f"PHOTO: {vcard.photo.value}")
    
    # Extract email addresses with type information
    if hasattr(vcard, 'email_list'):
        for email in vcard.email_list:
            type_label = 'DEFAULT'
            if hasattr(email, 'params') and 'TYPE' in email.params:
                type_values = email.params['TYPE']
                if isinstance(type_values, list) and type_values:
                    type_label = type_values[0].upper()
                elif isinstance(type_values, str):
                    type_label = type_values.upper()
            
            field_key = f"EMAIL[{type_label}]"
            lines.append(f'"{field_key}": {email.value}')
    
    # Extract phone numbers with type information
    if hasattr(vcard, 'tel_list'):
        for tel in vcard.tel_list:
            type_label = 'DEFAULT'
            if hasattr(tel, 'params') and 'TYPE' in tel.params:
                type_values = tel.params['TYPE']
                if isinstance(type_values, list) and type_values:
                    type_label = type_values[0].upper()
                elif isinstance(type_values, str):
                    type_label = type_values.upper()
            
            field_key = f"TEL[{type_label}]"
            lines.append(f'"{field_key}": "{tel.value}"')
    
    # Extract birthday
    if hasattr(vcard, 'bday') and vcard.bday.value:
        lines.append(f"BDAY: {vcard.bday.value}")
    
    # Extract URLs with type information
    if hasattr(vcard, 'url') and vcard.url.value:
        type_label = 'DEFAULT'
        if hasattr(vcard.url, 'params') and 'TYPE' in vcard.url.params:
            type_values = vcard.url.params['TYPE']
            if isinstance(type_values, list) and type_values:
                type_label = type_values[0].upper()
            elif isinstance(type_values, str):
                type_label = type_values.upper()
        
        field_key = f"URL[{type_label}]"
        lines.append(f'"{field_key}": {vcard.url.value}')
    
    # Extract organization
    if hasattr(vcard, 'org') and vcard.org.value:
        org_value = vcard.org.value
        if isinstance(org_value, list) and org_value:
            lines.append(f"ORG: {org_value[0]}")
        elif isinstance(org_value, str):
            lines.append(f"ORG: {org_value}")
    
    # Extract addresses with type information
    if hasattr(vcard, 'adr_list'):
        for adr in vcard.adr_list:
            adr_value = adr.value
            type_label = 'DEFAULT'
            if hasattr(adr, 'params') and 'TYPE' in adr.params:
                type_values = adr.params['TYPE']
                if isinstance(type_values, list) and type_values:
                    type_label = type_values[0].upper()
                elif isinstance(type_values, str):
                    type_label = type_values.upper()
            
            base_key = f"ADR[{type_label}]"
            
            if hasattr(adr_value, 'box') and adr_value.box:
                lines.append(f'"{base_key}.POBOX": {adr_value.box}')
            if hasattr(adr_value, 'extended') and adr_value.extended:
                lines.append(f'"{base_key}.EXTENDED": {adr_value.extended}')
            if hasattr(adr_value, 'street') and adr_value.street:
                lines.append(f'"{base_key}.STREET": {adr_value.street}')
            if hasattr(adr_value, 'city') and adr_value.city:
                lines.append(f'"{base_key}.LOCALITY": {adr_value.city}')
            if hasattr(adr_value, 'region') and adr_value.region:
                lines.append(f'"{base_key}.REGION": {adr_value.region}')
            if hasattr(adr_value, 'code') and adr_value.code:
                lines.append(f'"{base_key}.POSTAL": "{adr_value.code}"')
            if hasattr(adr_value, 'country') and adr_value.country:
                lines.append(f'"{base_key}.COUNTRY": {adr_value.country}')
    
    # Extract categories
    if hasattr(vcard, 'categories') and vcard.categories.value:
        lines.append(f"CATEGORIES: {vcard.categories.value}")
    
    # Extract UID
    if hasattr(vcard, 'uid') and vcard.uid.value:
        lines.append(f"UID: {vcard.uid.value}")
    
    # Extract version
    if hasattr(vcard, 'version') and vcard.version.value:
        lines.append(f'VERSION: "{vcard.version.value}"')
    
    lines.append("")
    lines.append("---")
    
    # Add notes section if available
    notes_added = False
    if hasattr(vcard, 'note') and vcard.note.value:
        notes_added = True
    if hasattr(vcard, 'categories') and vcard.categories.value:
        notes_added = True
    
    if notes_added:
        lines.append("#### Notes")
        lines.append("")
        
        if hasattr(vcard, 'categories') and vcard.categories.value:
            category_list = vcard.categories.value.split(',')
            contact_line = "#Contact"
            for category in category_list:
                contact_line += f" #{category.strip()}"
            lines.append(contact_line)
        else:
            lines.append("#Contact")
    
    return '\n'.join(lines) + '\n'


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
        # Parse VCF file directly with vobject
        with open(vcf_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        vcard = vobject.readOne(content)
        
        # Generate Markdown content directly from vobject
        markdown_content = generate_obsidian_markdown(vcard)
        
        # Create output filename based on FN (preferred) or UID (fallback)
        contact_name = ''
        if hasattr(vcard, 'fn') and vcard.fn.value:
            contact_name = vcard.fn.value
        elif hasattr(vcard, 'n') and vcard.n.value:
            n = vcard.n.value
            given_name = getattr(n, 'given', '') or ''
            family_name = getattr(n, 'family', '') or ''
            if given_name or family_name:
                contact_name = f"{given_name} {family_name}".strip()
        
        if contact_name:
            # Use contact name as filename (preferred)
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', contact_name)
            output_file = output_dir / f"{safe_filename}.md"
        elif hasattr(vcard, 'uid') and vcard.uid.value:
            # Fallback to UID if no contact name is available
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', vcard.uid.value)
            output_file = output_dir / f"{safe_filename}.md"
        else:
            # Final fallback to VCF filename if neither name nor UID is available
            safe_filename = vcf_path.stem
            output_file = output_dir / f"{safe_filename}.md"
        
        # Remove existing files with the same UID if the filename would be different
        if hasattr(vcard, 'uid') and vcard.uid.value:
            existing_files = find_existing_files_with_uid(output_dir, vcard.uid.value)
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


@click.command()
@click.option('--folder',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
              multiple=True,
              help="Source folder containing VCF files to convert")
@click.option('--obsidian',
              type=click.Path(path_type=Path),
              required=True,
              help="Destination directory for Markdown files")
@click.option('--file',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
              multiple=True,
              help="Specific VCF file to convert (can be specified multiple times)")
@click.option('--verbose', '-v',
              is_flag=True,
              help="Enable verbose output")
def main(folder, obsidian, file, verbose):
    """Convert VCF files to Markdown format for obsidian-vcf-contacts plugin
    
    Use --folder to process all VCF files in a directory, or --file to process
    specific files. You can mix --folder and --file options.
    """
    # Validate that at least one source is provided
    if not folder and not file:
        click.echo("Error: Must specify at least one --folder or --file option.", err=True)
        sys.exit(1)
    
    # Create destination directory if it doesn't exist
    dest_path = obsidian
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Build task list of VCF files to process
    task_list = []
    
    # Add files from folders
    for folder_path in folder:
        if not folder_path.is_dir():
            click.echo(f"Error: Folder path '{folder_path}' is not a directory.", err=True)
            sys.exit(1)
        
        # Find all VCF files in this folder
        folder_vcf_files = list(folder_path.glob("*.vcf")) + list(folder_path.glob("*.VCF"))
        task_list.extend(folder_vcf_files)
        
        if verbose:
            click.echo(f"Found {len(folder_vcf_files)} VCF file(s) in '{folder_path}'")
    
    # Add individual files
    for file_path in file:
        if not file_path.suffix.lower() == '.vcf':
            click.echo(f"Warning: File '{file_path}' does not have a .vcf extension", err=True)
        task_list.append(file_path)
        
        if verbose:
            click.echo(f"Added individual file: {file_path}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_task_list = []
    for vcf_file in task_list:
        if vcf_file not in seen:
            seen.add(vcf_file)
            unique_task_list.append(vcf_file)
    
    task_list = unique_task_list
    
    if not task_list:
        click.echo("No VCF files found to process.", err=True)
        sys.exit(1)
    
    click.echo(f"Processing {len(task_list)} VCF file(s)")
    click.echo(f"Converting to Markdown in '{dest_path}'")
    
    # Convert each VCF file in the task list
    success_count = 0
    for vcf_file in task_list:
        if verbose:
            click.echo(f"Processing: {vcf_file}")
        
        if convert_vcf_to_markdown(vcf_file, dest_path):
            success_count += 1
    
    click.echo(f"Successfully converted {success_count}/{len(task_list)} files.")


if __name__ == "__main__":
    main()
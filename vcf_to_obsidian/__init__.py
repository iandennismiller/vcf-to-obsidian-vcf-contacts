"""
vcf-to-obsidian-vcf-contacts

A Python module that batch-converts VCF files into Markdown files
that are compatible with obsidian-vcf-contacts plugin for ObsidianMD.

Author: Ian Dennis Miller
License: MIT
"""

from .vcf_reader import VCFReader
from .markdown_writer import MarkdownWriter
from .filename_generator import FilenameGenerator
from .cli import CLI

# For backward compatibility with existing tests
from .vcf_reader import VCFReader as parse_vcf_file_class
from .markdown_writer import MarkdownWriter as generate_obsidian_markdown_class

# For backward compatibility with test that expects HAS_VOBJECT
HAS_VOBJECT = True

# Main conversion function
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
        # Read VCF file
        reader = VCFReader()
        vcard = reader.read_vcf_file(vcf_path)
        
        # Generate markdown content
        writer = MarkdownWriter()
        markdown_content = writer.generate_obsidian_markdown(vcard)
        
        # Generate filename
        filename_gen = FilenameGenerator()
        output_filename = filename_gen.generate_filename(vcard, vcf_path)
        
        from pathlib import Path
        output_file = Path(output_dir) / f"{output_filename}.md"
        
        # Remove existing files with the same UID if the filename would be different
        if hasattr(vcard, 'uid') and vcard.uid and vcard.uid.value:
            existing_files = filename_gen.find_existing_files_with_uid(output_dir, vcard.uid.value)
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

# For backward compatibility
def generate_obsidian_markdown(vcard):
    """Generate Markdown content compatible with obsidian-vcf-contacts plugin."""
    writer = MarkdownWriter()
    return writer.generate_obsidian_markdown(vcard)

def parse_vcf_file(vcf_path):
    """Parse a VCF file and return contact data."""
    reader = VCFReader()
    return reader.parse_vcf_file(vcf_path)

def find_existing_files_with_uid(output_dir, uid):
    """Find existing Markdown files with the same UID."""
    filename_gen = FilenameGenerator()
    return filename_gen.find_existing_files_with_uid(output_dir, uid)

# CLI entry point
def main():
    """Main CLI entry point."""
    from .cli import main_cli
    main_cli()

__all__ = [
    'VCFReader', 'MarkdownWriter', 'FilenameGenerator', 'CLI',
    'convert_vcf_to_markdown', 'generate_obsidian_markdown', 
    'parse_vcf_file', 'find_existing_files_with_uid', 'main'
]
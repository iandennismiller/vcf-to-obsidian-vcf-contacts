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
from .vcf_converter import VCFConverter
from .cli import CLI

# For backward compatibility with existing tests
from .vcf_reader import VCFReader as parse_vcf_file_class
from .markdown_writer import MarkdownWriter as generate_obsidian_markdown_class

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
    converter = VCFConverter()
    return converter.convert_vcf_to_markdown(vcf_path, output_dir)

# For backward compatibility
def generate_obsidian_markdown(vcard):
    """Generate Markdown content compatible with obsidian-vcf-contacts plugin."""
    writer = MarkdownWriter()
    return writer.generate_obsidian_markdown(vcard)



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
    'VCFReader', 'MarkdownWriter', 'FilenameGenerator', 'VCFConverter', 'CLI',
    'convert_vcf_to_markdown', 'generate_obsidian_markdown', 
    'find_existing_files_with_uid', 'main'
]
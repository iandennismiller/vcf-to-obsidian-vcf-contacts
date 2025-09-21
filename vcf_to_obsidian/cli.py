"""
CLI module for command-line interface handling.
"""

import click
import sys
from pathlib import Path
from .vcf_converter import VCFConverter


class CLI:
    """Class responsible for handling command-line interface operations."""
    
    def __init__(self):
        """Initialize the CLI handler."""
        self.converter = VCFConverter()
    
    def convert_vcf_to_markdown(self, vcf_path, output_dir):
        """
        Convert a single VCF file to Markdown format.
        
        Args:
            vcf_path (Path): Path to the VCF file
            output_dir (Path): Output directory for Markdown files
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.converter.convert_vcf_to_markdown_with_validation(vcf_path, output_dir)


# Create the click command outside the class
@click.command()
@click.option('--folder', 
              type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
              multiple=True,
              help="Source directory containing VCF files (can be specified multiple times)")
@click.option('--obsidian',
              type=click.Path(path_type=Path),
              required=True,
              help="Destination directory for Markdown files")
@click.option('--file',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
              multiple=True,
              help="Specific VCF file to process (can be specified multiple times)")
@click.option('--verbose', '-v',
              is_flag=True,
              help="Enable verbose output")
@click.option('--ignore',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
              multiple=True,
              help="Specific VCF file to ignore (can be specified multiple times)")
def main_cli(folder, obsidian, file, verbose, ignore):
    """Convert VCF files to Markdown format for obsidian-vcf-contacts plugin
    
    Use --folder to specify source directories containing VCF files
    Use --obsidian to specify the destination directory for Markdown files  
    Use --file to specify individual VCF files to process
    Use --ignore to specify individual VCF files to skip
    
    --folder, --file, and --ignore options can be specified multiple times.
    """
    converter = VCFConverter()
    converter.process_tasks(folder, obsidian, file, verbose, ignore)
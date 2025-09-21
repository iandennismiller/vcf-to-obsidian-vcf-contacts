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
    
    def run_cli(self, folder, obsidian, file, verbose, ignore):
        """Convert VCF files to Markdown format for obsidian-vcf-contacts plugin
        
        Use --folder to specify source directories containing VCF files
        Use --obsidian to specify the destination directory for Markdown files  
        Use --file to specify individual VCF files to process
        Use --ignore to specify individual VCF files to skip
        
        --folder, --file, and --ignore options can be specified multiple times.
        """
        # Validate that at least one source is specified
        if not folder and not file:
            click.echo("Error: Must specify at least one --folder or --file option.", err=True)
            sys.exit(1)
        
        # Validate file and folder sources exist before processing
        for folder_path in folder:
            if not folder_path.is_dir():
                click.echo(f"Error: Source path '{folder_path}' is not a directory.", err=True)
                sys.exit(1)
        
        for file_path in file:
            if not file_path.exists():
                click.echo(f"Error: File '{file_path}' does not exist.", err=True)
                sys.exit(1)
            if not file_path.is_file():
                click.echo(f"Error: Path '{file_path}' is not a file.", err=True)
                sys.exit(1)
        
        # Convert tuples to lists for easier handling
        folder_sources = list(folder) if folder else []
        file_sources = list(file) if file else []
        ignore_files = list(ignore) if ignore else []
        
        # Use VCFConverter to handle the conversion
        successful_conversions, total_conversions, all_vcf_files = self.converter.convert_vcf_files_from_sources(
            folder_sources=folder_sources,
            file_sources=file_sources,
            output_dir=obsidian,
            ignore_files=ignore_files,
            verbose=verbose
        )
        
        # Handle edge cases for messaging
        if not all_vcf_files:
            if not folder_sources and not file_sources:
                click.echo("No VCF files found to process.", err=True)
            else:
                click.echo("No VCF files remaining to process after applying ignore list.", err=True)
            sys.exit(1)
        
        # Report final results
        click.echo(f"Found {len(all_vcf_files)} VCF file(s) to process")
        click.echo(f"Successfully completed {successful_conversions}/{len(all_vcf_files)} conversions.")


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
    cli = CLI()
    cli.run_cli(folder, obsidian, file, verbose, ignore)
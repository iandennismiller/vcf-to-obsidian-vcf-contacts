"""
CLI module for command-line interface handling.
"""

import click
import sys
from pathlib import Path
from .vcf_reader import VCFReader
from .markdown_writer import MarkdownWriter
from .filename_generator import FilenameGenerator


class CLI:
    """Class responsible for handling command-line interface operations."""
    
    def __init__(self):
        """Initialize the CLI handler."""
        self.reader = VCFReader()
        self.writer = MarkdownWriter()
        self.filename_gen = FilenameGenerator()
    
    def convert_vcf_to_markdown(self, vcf_path, output_dir):
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
            vcard = self.reader.read_vcf_file(vcf_path)
            
            # Generate markdown content
            markdown_content = self.writer.generate_obsidian_markdown(vcard)
            
            # Generate filename
            output_filename = self.filename_gen.generate_filename(vcard, vcf_path)
            output_file = output_dir / f"{output_filename}.md"
            
            # Remove existing files with the same UID if the filename would be different
            if hasattr(vcard, 'uid') and vcard.uid and vcard.uid.value:
                existing_files = self.filename_gen.find_existing_files_with_uid(output_dir, vcard.uid.value)
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
    
    def run_cli(self, folder, obsidian, file, verbose):
        """Convert VCF files to Markdown format for obsidian-vcf-contacts plugin
        
        Use --folder to specify source directories containing VCF files
        Use --obsidian to specify the destination directory for Markdown files  
        Use --file to specify individual VCF files to process
        
        --folder and --file options can be specified multiple times to process multiple sources.
        """
        # Validate that at least one source is specified
        if not folder and not file:
            click.echo("Error: Must specify at least one --folder or --file option.", err=True)
            sys.exit(1)
        
        # Note: --obsidian is required by click, so no need to validate it here
        
        # Collect all VCF files to process
        all_vcf_files = []
        processed_paths = set()  # Track processed file paths to avoid duplicates
        
        # Process folder sources
        for source_path in folder:
            if not source_path.is_dir():
                click.echo(f"Error: Source path '{source_path}' is not a directory.", err=True)
                sys.exit(1)
            
            # Find all VCF files in this directory
            vcf_files = list(source_path.glob("*.vcf")) + list(source_path.glob("*.VCF"))
            new_files_count = 0
            for vcf_file in vcf_files:
                absolute_path = vcf_file.resolve()
                if absolute_path not in processed_paths:
                    all_vcf_files.append(vcf_file)
                    processed_paths.add(absolute_path)
                    new_files_count += 1
            
            if verbose:
                if new_files_count < len(vcf_files):
                    click.echo(f"Found {len(vcf_files)} VCF file(s) in '{source_path}' ({new_files_count} new, {len(vcf_files) - new_files_count} duplicates)")
                else:
                    click.echo(f"Found {len(vcf_files)} VCF file(s) in '{source_path}'")
        
        # Process individual file sources
        for file_path in file:
            if not file_path.exists():
                click.echo(f"Error: File '{file_path}' does not exist.", err=True)
                sys.exit(1)
            
            if not file_path.is_file():
                click.echo(f"Error: Path '{file_path}' is not a file.", err=True)
                sys.exit(1)
            
            # Check if it's a VCF file by extension
            if file_path.suffix.lower() not in ['.vcf']:
                click.echo(f"Warning: File '{file_path}' does not have a .vcf extension.", err=True)
            
            absolute_path = file_path.resolve()
            if absolute_path not in processed_paths:
                all_vcf_files.append(file_path)
                processed_paths.add(absolute_path)
                
                if verbose:
                    click.echo(f"Added individual file: '{file_path}'")
            else:
                if verbose:
                    click.echo(f"Skipping duplicate file: '{file_path}'")
        
        if not all_vcf_files:
            click.echo("No VCF files found to process.", err=True)
            sys.exit(1)
        
        click.echo(f"Found {len(all_vcf_files)} VCF file(s) to process")
        
        # Create destination directory
        dest_path = obsidian
        dest_path.mkdir(parents=True, exist_ok=True)
        if verbose:
            click.echo(f"Destination directory: '{dest_path}'")
        
        click.echo(f"Converting to Markdown in '{dest_path}'")
        
        # Convert each VCF file to the destination
        successful_conversions = 0
        
        for vcf_file in all_vcf_files:
            if verbose:
                click.echo(f"Processing: {vcf_file} -> {dest_path}")
            
            if self.convert_vcf_to_markdown(vcf_file, dest_path):
                successful_conversions += 1
        
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
def main_cli(folder, obsidian, file, verbose):
    """Convert VCF files to Markdown format for obsidian-vcf-contacts plugin
    
    Use --folder to specify source directories containing VCF files
    Use --obsidian to specify the destination directory for Markdown files  
    Use --file to specify individual VCF files to process
    
    --folder and --file options can be specified multiple times to process multiple sources.
    """
    cli = CLI()
    cli.run_cli(folder, obsidian, file, verbose)
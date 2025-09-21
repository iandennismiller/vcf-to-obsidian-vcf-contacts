"""
CLI module for command-line interface handling.
"""

import click
from pathlib import Path
from .vcf_converter import VCFConverter


# Create the click command
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

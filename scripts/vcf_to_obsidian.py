#!/usr/bin/env python3
"""
vcf-to-obsidian-vcf-contacts

A Python script that batch-converts a folder containing VCF files into Markdown files
that are compatible with obsidian-vcf-contacts plugin for ObsidianMD.

Usage:
    python vcf_to_obsidian.py --folder <source_vcf_directory> --obsidian <destination_obsidian_folder>
    python vcf_to_obsidian.py --file <vcf_file> --obsidian <destination_obsidian_folder>

Multiple sources can be specified but only one destination:
    python vcf_to_obsidian.py --folder <dir1> --folder <dir2> --file <file> --obsidian <output_dir>

Author: Ian Dennis Miller
License: MIT
"""

# Import the modular components from parent directory
import sys
from pathlib import Path

# Add parent directory to sys.path to import the vcf_to_obsidian module
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcf_to_obsidian.cli import main_cli

if __name__ == "__main__":
    main_cli()
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

# Import the modular components
from vcf_to_obsidian import main

# For backward compatibility, import individual functions
from vcf_to_obsidian import (
    convert_vcf_to_markdown,
    generate_obsidian_markdown,
    parse_vcf_file,
    find_existing_files_with_uid
)

if __name__ == "__main__":
    main()
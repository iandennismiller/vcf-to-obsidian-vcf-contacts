Usage
=====

This document provides comprehensive usage examples for both implementations.

Bash Script
-----------

The bash script (``scripts/vcf-to-obsidian.sh``) provides functionality with zero dependencies:

::

   # Convert a single VCF file
   ./scripts/vcf-to-obsidian.sh --file contact.vcf --obsidian ./obsidian-vault/contacts

   # Convert all VCF files in a directory  
   ./scripts/vcf-to-obsidian.sh --folder ./contacts --obsidian ./obsidian-vault/contacts

   # Process multiple sources
   ./scripts/vcf-to-obsidian.sh --folder ./contacts1 --folder ./contacts2 --file ./special.vcf --obsidian ./vault

   # Enable verbose output
   ./scripts/vcf-to-obsidian.sh --folder ./contacts --obsidian ./vault --verbose


Python Script
-------------

After installing with pip or pipx:
::

   vcf-to-obsidian --folder <source_vcf_directory> --obsidian <destination_obsidian_folder>


Or using the Python script directly:
::

   python scripts/vcf_to_obsidian.py --folder <source_vcf_directory> --obsidian <destination_obsidian_folder>


Examples
--------

Convert all VCF files from a directory:
::

   vcf-to-obsidian --folder ./contacts --obsidian ./obsidian-vault/contacts


Convert a specific VCF file:
::

   vcf-to-obsidian --file ./contact.vcf --obsidian ./obsidian-vault/contacts


Process multiple sources to single destination:
::

   vcf-to-obsidian --folder ./contacts1 --folder ./contacts2 --file ./special.vcf --obsidian ./vault


With verbose output:
::

::

   vcf-to-obsidian --folder ./contacts --obsidian ./obsidian-vault/contacts --verbose


Command Line Options
--------------------

- ``--folder``: Source directory containing VCF files (can be specified multiple times)
- ``--obsidian``: Destination directory for generated Markdown files (required, single directory only)
- ``--file``: Specific VCF file to process (can be specified multiple times)
- ``--verbose`` or ``-v``: Enable verbose output
- ``--help`` or ``-h``: Show help message

**Note**: You must specify at least one source (either ``--folder`` or ``--file``) and exactly one destination (``--obsidian``).

Template Output
---------------

The script generates markdown output with a fixed template that is compatible with the obsidian-vcf-contacts plugin format. The template includes:

- YAML frontmatter with all contact metadata extracted directly from the VCF file
- Structured markdown content optimized for Obsidian

The template works directly with the VCF data structure to ensure maximum compatibility and reduce complexity. No custom templates are supported - the built-in template ensures consistent, reliable output.
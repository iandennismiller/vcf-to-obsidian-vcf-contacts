# Documentation

This directory contains the Sphinx documentation for vcf-to-obsidian-vcf-contacts.

## Building the Documentation

To build the documentation locally:

1. Install the required dependencies:
   ```bash
   pip install sphinx sphinx-autoapi sphinx-rtd-theme vobject click
   ```

2. Build the HTML documentation:
   ```bash
   make html
   ```

3. View the documentation:
   ```bash
   # Open build/html/index.html in your browser
   open build/html/index.html  # macOS
   xdg-open build/html/index.html  # Linux
   ```

## Available Commands

- `make html` - Build HTML documentation
- `make clean` - Clean build artifacts
- `make help` - Show all available make targets

## Online Documentation

The documentation is automatically built and deployed to GitHub Pages at:
https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/

## Documentation Structure

- `source/` - reStructuredText source files
- `source/conf.py` - Sphinx configuration
- `source/index.rst` - Main documentation index
- `build/` - Generated documentation (created when building)
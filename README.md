# vcf-to-obsidian-vcf-contacts

A collection of tools that batch-convert VCF files into Markdown files compatible with the obsidian-vcf-contacts plugin for ObsidianMD.

This repository provides two implementations:
- **Python script** (`vcf_to_obsidian.py`) - Full-featured implementation with vobject library
- **Bash script** (`vcf-to-obsidian.sh`) - Pure bash implementation for environments without Python dependencies

## Features

- Batch conversion of VCF files to Markdown format
- Compatible with obsidian-vcf-contacts plugin metadata structure  
- Preserves contact information including names, phone numbers, emails, addresses, and notes
- Command-line interface for easy automation
- Error handling and validation
- Support for both vCard 3.0 and 4.0 formats
- Intelligent filename generation with priority logic (FN > constructed name > UID > filename)

## Quick Start

### Bash Implementation (No Dependencies)

The bash script requires only standard Unix tools and works on any system with bash:

```bash
# Make executable
chmod +x vcf-to-obsidian.sh

# Convert a single file
./vcf-to-obsidian.sh --file contact.vcf --obsidian ./output

# Convert a folder
./vcf-to-obsidian.sh --folder ./contacts --obsidian ./output

# Multiple sources
./vcf-to-obsidian.sh --folder ./contacts1 --file ./special.vcf --obsidian ./output
```

### Python Implementation

### Python Implementation

For the Python implementation, you need:

- Python 3.12+ (tested with Python 3.12.3)
- vobject 0.9.0+ (for enhanced vCard 3.0/4.0 parsing)
- click 8.0.0+ (for command line interface)

### Option 1: Install with pip (Recommended)

```bash
pip install vcf-to-obsidian-vcf-contacts
```

### Option 2: Install with pipx (For CLI tools)

```bash
pipx install vcf-to-obsidian-vcf-contacts
```

### Option 3: Development Installation

1. Clone this repository:
```bash
git clone https://github.com/iandennismiller/vcf-to-obsidian-vcf-contacts.git
cd vcf-to-obsidian-vcf-contacts
```

2. Install in development mode with testing dependencies:
```bash
pip install -e .[dev]
```

This installs the package in editable mode along with pytest for running tests.

## Usage

### Bash Script

The bash script (`vcf-to-obsidian.sh`) provides the same functionality as the Python version but with zero dependencies:

```bash
# Convert a single VCF file
./vcf-to-obsidian.sh --file contact.vcf --obsidian ./obsidian-vault/contacts

# Convert all VCF files in a directory  
./vcf-to-obsidian.sh --folder ./contacts --obsidian ./obsidian-vault/contacts

# Process multiple sources
./vcf-to-obsidian.sh --folder ./contacts1 --folder ./contacts2 --file ./special.vcf --obsidian ./vault

# Enable verbose output
./vcf-to-obsidian.sh --folder ./contacts --obsidian ./vault --verbose
```

### Python Script

After installing with pip or pipx:
```bash
vcf-to-obsidian --folder <source_vcf_directory> --obsidian <destination_obsidian_folder>
```

Or using the Python script directly:
```bash
python vcf_to_obsidian.py --folder <source_vcf_directory> --obsidian <destination_obsidian_folder>
```

### Examples

Convert all VCF files from a directory:
```bash
vcf-to-obsidian --folder ./contacts --obsidian ./obsidian-vault/contacts
```

Convert a specific VCF file:
```bash
vcf-to-obsidian --file ./contact.vcf --obsidian ./obsidian-vault/contacts
```

Process multiple sources to single destination:
```bash
vcf-to-obsidian --folder ./contacts1 --folder ./contacts2 --file ./special.vcf --obsidian ./vault
```

With verbose output:
```bash
vcf-to-obsidian --folder ./contacts --obsidian ./obsidian-vault/contacts --verbose
```

### Command Line Options

- `--folder`: Source directory containing VCF files (can be specified multiple times)
- `--obsidian`: Destination directory for generated Markdown files (required, single directory only)
- `--file`: Specific VCF file to process (can be specified multiple times)
- `--verbose` or `-v`: Enable verbose output
- `--help` or `-h`: Show help message

**Note**: You must specify at least one source (either `--folder` or `--file`) and exactly one destination (`--obsidian`).

## Implementation Comparison

| Feature | Bash Script | Python Script |
|---------|-------------|---------------|
| **Dependencies** | None (standard Unix tools) | Python 3.12+, vobject, click |
| **Performance** | Fast (line-by-line processing) | Fast (vobject parsing) |
| **VCard Support** | 3.0 and 4.0 | 3.0 and 4.0 (via vobject) |
| **Field Parsing** | Manual regex-based | Library-based |
| **Error Handling** | Basic | Comprehensive |
| **Portability** | Unix/Linux/macOS | Cross-platform |
| **Maintenance** | Self-contained | Library dependencies |

**When to use the bash script:**
- No Python environment available
- Minimal dependencies preferred  
- Unix/Linux/macOS environments
- Simple deployment scenarios

**When to use the Python script:**
- Python environment already available
- Cross-platform compatibility needed
- More robust error handling required
- Integration with Python workflows

Both implementations produce identical output format and support the same command line interface.

## Template Output

The script generates markdown output with a fixed template that is compatible with the obsidian-vcf-contacts plugin format. The template includes:

- YAML frontmatter with all contact metadata extracted directly from the VCF file
- Structured markdown content optimized for Obsidian

The template works directly with the VCF data structure to ensure maximum compatibility and reduce complexity. No custom templates are supported - the built-in template ensures consistent, reliable output.

## VCF Support

The script supports both vCard 3.0 and vCard 4.0 formats and extracts the following fields:

- **UID**: Unique Identifier (used for stable filename generation)
- **FN**: Full Name
- **N**: Structured Name (Family;Given;Additional;Prefix;Suffix)
- **ORG**: Organization
- **TEL**: Phone Numbers (with type detection)
- **EMAIL**: Email Addresses (with type detection)
- **ADR**: Addresses (with type detection)
- **URL**: Website URL
- **BDAY**: Birthday
- **NOTE**: Notes/Comments

### vCard 4.0 Support

The script uses the `vobject` library for enhanced vCard parsing, which provides:

- **Better vCard 4.0 compatibility**: Improved parsing of modern vCard format
- **Robust field handling**: More accurate extraction of complex fields like addresses
- **Type parameter support**: Proper handling of type parameters (HOME, WORK, etc.)

### Parsing Engine

The script uses the `vobject` library for comprehensive vCard 3.0/4.0 support. This ensures reliable parsing of VCF files while taking advantage of modern parsing capabilities.

### Filename Generation

The script uses a priority-based approach for generating Markdown filenames:

1. **Full Name (FN)** (highest priority): Uses the full name from the VCF FN field (e.g., `John Doe.md`)
2. **Constructed Name** (fallback): If no FN field, combines given and family names (e.g., `John Smith.md`)  
3. **UID** (fallback): If no name is available, uses the UID field (e.g., `12345-abcde-67890.md`)
4. **VCF Filename** (final fallback): Uses the original VCF filename if no other options are available

This approach prioritizes human-readable filenames while providing UID-based fallback for stability when contact information is incomplete.

## Testing

The project includes a comprehensive test suite to ensure reliability and correctness, organized using pytest.

### Running Tests

Run the test suite using pytest:

```bash
pytest
```

Or run with verbose output:

```bash
pytest -v
```

Run tests for a specific functionality:

```bash
pytest tests/test_vcf_reading.py      # VCF parsing tests
pytest tests/test_markdown_writing.py # Markdown generation tests
pytest tests/test_command_line.py     # CLI functionality tests
pytest tests/test_filename_generation.py # Filename logic tests
pytest tests/test_integration.py      # End-to-end integration tests
```

### Test Organization

Tests are organized into separate files by functionality:

- **`tests/test_vcf_reading.py`** - VCF file parsing and data extraction
- **`tests/test_markdown_writing.py`** - Markdown content generation
- **`tests/test_command_line.py`** - Command line interface functionality
- **`tests/test_filename_generation.py`** - Filename generation logic and special character handling
- **`tests/test_integration.py`** - End-to-end integration tests

### Test Coverage

The test suite covers:

- VCF parsing with various field combinations
- Filename generation priority logic (FN > constructed name > UID > filename)
- Special character handling in filenames and UIDs
- Markdown content generation and frontmatter
- Template system functionality
- Command line interface behavior
- Edge cases (empty fields, missing data)
- Error handling scenarios

## Development and Maintenance

This project includes a comprehensive Makefile for installation, testing, linting, and other maintenance tasks.

### Quick Setup

```bash
# Set up development environment
make setup-dev

# Run all tests
make test-all

# Run linting
make lint

# Show all available targets
make help
```

### Available Make Targets

**Installation:**
- `make install` - Install package dependencies
- `make install-dev` - Install development dependencies (includes pytest)
- `make install-lint` - Install linting tools (flake8, black, isort, mypy)
- `make setup-dev` - Set up complete development environment

**Testing:**
- `make test` - Run all available tests
- `make test-bash` - Run bash implementation tests
- `make test-python` - Run Python tests with pytest
- `make test-all` - Run all tests (bash and python if available)

**Linting and Code Quality:**
- `make lint` - Run all linting tools
- `make lint-python` - Run Python linting (flake8, black, isort, mypy)
- `make lint-bash` - Run bash script linting (shellcheck)
- `make format` - Format code using black and isort

**Build and Package:**
- `make build` - Build package (syntax check, make executable)
- `make package` - Create distributable package
- `make check-deps` - Check if required dependencies are available

**Maintenance:**
- `make clean` - Clean temporary files and build artifacts
- `make docs` - Show usage documentation
- `make demo` - Run a quick demo with test data

**Development Workflows:**
- `make ci` - Run full CI pipeline (install, test, lint)
- `make dev-check` - Quick development check (test + lint)
- `make quick-start` - Show quick start guide

### Dependencies

The Makefile handles dependency installation automatically. For manual installation:

**Required for Python implementation:**
- Python 3.12+
- vobject 0.9.0+
- click 8.0.0+

**Development dependencies:**
- pytest 7.0.0+

**Linting tools (optional):**
- flake8, black, isort, mypy for Python
- shellcheck for bash scripts

## Error Handling

The script includes robust error handling for:

- Non-existent source directories
- Empty directories with no VCF files
- Malformed VCF files
- File system permissions issues
- Invalid characters in filenames

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Author

Ian Dennis Miller

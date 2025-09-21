# vcf-to-obsidian-vcf-contacts

A Python script that batch-converts a folder containing VCF files into Markdown files that are compatible with the obsidian-vcf-contacts plugin for ObsidianMD.

## Features

- Batch conversion of VCF files to Markdown format
- Compatible with obsidian-vcf-contacts plugin metadata structure
- Preserves contact information including names, phone numbers, emails, addresses, and notes
- Command-line interface for easy automation
- Error handling and validation

## Requirements

- Python 3.12+ (tested with Python 3.12.3)
- No external dependencies required

## Installation

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

2. Install in development mode:
```bash
pip install -e .
```

### Option 4: Direct Script Usage

1. Clone this repository:
```bash
git clone https://github.com/iandennismiller/vcf-to-obsidian-vcf-contacts.git
cd vcf-to-obsidian-vcf-contacts
```

2. Make the script executable (optional):
```bash
chmod +x vcf_to_obsidian.py
```

## Usage

### Basic Usage

After installing with pip or pipx:
```bash
vcf-to-obsidian <source_vcf_directory> <destination_obsidian_folder>
```

Or using the Python script directly:
```bash
python vcf_to_obsidian.py <source_vcf_directory> <destination_obsidian_folder>
```

### Examples

Convert all VCF files from a directory (using installed CLI):
```bash
vcf-to-obsidian ./contacts ./obsidian-vault/contacts
```

Convert all VCF files from a directory (using Python script):
```bash
python vcf_to_obsidian.py ./contacts ./obsidian-vault/contacts
```

With verbose output (using installed CLI):
```bash
vcf-to-obsidian ./contacts ./obsidian-vault/contacts --verbose
```

With verbose output (using Python script):
```bash
python vcf_to_obsidian.py ./contacts ./obsidian-vault/contacts --verbose
```

### Command Line Options

- `source_dir`: Directory containing VCF files to convert
- `dest_dir`: Destination directory for generated Markdown files
- `--verbose` or `-v`: Enable verbose output
- `--help` or `-h`: Show help message

## VCF Support

The script supports standard VCF (vCard) format and extracts the following fields:

- **FN**: Full Name
- **N**: Structured Name (Family;Given;Additional;Prefix;Suffix)
- **ORG**: Organization
- **TEL**: Phone Numbers (with type detection)
- **EMAIL**: Email Addresses (with type detection)
- **ADR**: Addresses (with type detection)
- **URL**: Website URL
- **BDAY**: Birthday
- **NOTE**: Notes/Comments

## Output Format

Generated Markdown files include:

1. **YAML frontmatter** with metadata compatible with obsidian-vcf-contacts plugin
2. **Structured content** with contact information formatted for readability

### Example Output

```markdown
---
vcf-contact: true
name: "John Doe"
given-name: "John"
family-name: "Doe"
organization: "Acme Corporation"
phone-numbers:
  - "+1-555-123-4567"
email-addresses:
  - "john.doe@acme.com"
---

# John Doe

**Organization:** Acme Corporation

**Phone Numbers:**
- +1-555-123-4567

**Email Addresses:**
- john.doe@acme.com
```

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

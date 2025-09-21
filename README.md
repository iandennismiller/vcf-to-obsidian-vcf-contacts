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
- Jinja2 3.0.0+ (for templating)
- vobject 0.9.0+ (for enhanced vCard 3.0/4.0 parsing)

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

2. Install dependencies:
```bash
pip install jinja2 vobject
```

3. Make the script executable (optional):
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

Using a custom template:
```bash
python vcf_to_obsidian.py ./contacts ./obsidian-vault/contacts --template ./my_template.md.j2
```

### Command Line Options

- `source_dir`: Directory containing VCF files to convert
- `dest_dir`: Destination directory for generated Markdown files
- `--template` or `-t`: Path to custom Jinja2 template file (optional)
- `--verbose` or `-v`: Enable verbose output
- `--help` or `-h`: Show help message

## Templates

The script uses Jinja2 templates to generate the markdown output, providing flexibility for customization while maintaining compatibility with obsidian-vcf-contacts.

### Default Template

By default, the script uses a built-in template that generates markdown compatible with the obsidian-vcf-contacts plugin format. This template includes:

- YAML frontmatter with `vcf-contact: true` and all contact metadata
- Structured markdown content with contact information

### Custom Templates

You can provide your own Jinja2 template using the `--template` option. The template has access to the following variables:

- `title`: Contact's display name (full name or constructed from given/family names)
- `uid`: Unique identifier from VCF
- `full_name`: Full name from FN field
- `given_name`: Given (first) name
- `family_name`: Family (last) name
- `organization`: Organization name
- `phone_numbers`: List of phone numbers
- `email_addresses`: List of email addresses
- `addresses`: List of formatted addresses
- `notes`: Notes text
- `url`: Website URL
- `birthday`: Birthday date

### Example Custom Template

```jinja2
---
vcf-contact: true
custom-template: true
{%- if title %}
name: "{{ title }}"
{%- endif %}
---

# 📇 {{ title or "Contact" }}

{%- if organization %}
🏢 **Company:** {{ organization }}
{%- endif %}

{%- if phone_numbers %}
📞 **Phone:** {{ phone_numbers[0] }}
{%- endif %}

{%- if email_addresses %}
✉️ **Email:** {{ email_addresses[0] }}
{%- endif %}
```

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
- **Fallback mechanism**: Automatically falls back to legacy parsing if vobject is unavailable

### Parsing Engine

The script automatically uses the best available parsing method:

1. **vobject library** (preferred): Uses the `vobject` library for comprehensive vCard 3.0/4.0 support
2. **Legacy parser** (fallback): Uses a simple line-by-line parser if `vobject` is not available

This dual approach ensures maximum compatibility while taking advantage of modern parsing capabilities when available.

### Filename Generation

The script uses a priority-based approach for generating Markdown filenames:

1. **Full Name (FN)** (highest priority): Uses the full name from the VCF FN field (e.g., `John Doe.md`)
2. **Constructed Name** (fallback): If no FN field, combines given and family names (e.g., `John Smith.md`)  
3. **UID** (fallback): If no name is available, uses the UID field (e.g., `12345-abcde-67890.md`)
4. **VCF Filename** (final fallback): Uses the original VCF filename if no other options are available

This approach prioritizes human-readable filenames while providing UID-based fallback for stability when contact information is incomplete.

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

## Testing

The project includes a comprehensive test suite to ensure reliability and correctness.

### Running Tests

Run the test suite using Python's built-in unittest module:

```bash
python test_vcf_to_obsidian.py
```

Or run with verbose output:

```bash
python test_vcf_to_obsidian.py -v
```

### Test Coverage

The test suite covers:

- VCF parsing with various field combinations
- Filename generation priority logic (FN > constructed name > UID > filename)
- Special character handling in filenames and UIDs
- Markdown content generation and frontmatter
- Edge cases (empty fields, missing data)
- Error handling scenarios

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

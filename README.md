# vcf-to-obsidian-vcf-contacts

A collection of tools that batch-convert VCF files into Markdown files compatible with the obsidian-vcf-contacts plugin for ObsidianMD.

This repository provides two implementations:
- **Python script** - Full-featured implementation with robust vCard parsing
- **Bash script** - Zero-dependency implementation for Unix environments

## Features

- Batch conversion of VCF files to Markdown format
- Compatible with obsidian-vcf-contacts plugin metadata structure  
- Preserves contact information including names, phone numbers, emails, addresses, and notes
- Support for both vCard 3.0 and 4.0 formats
- Intelligent filename generation with priority logic
- Command-line interface for easy automation

## Quick Start

### Python Implementation

#### Installation

```bash
pip install vcf-to-obsidian-vcf-contacts
```

#### Usage

Convert all VCF files from a directory:
```bash
vcf-to-obsidian --folder ./contacts --obsidian ./obsidian-vault/contacts
```

### Bash Implementation (Zero Dependencies)

**Note:** The bash script requires bash to run and uses bash-specific features. On macOS where zsh is the default shell, make sure to run the script with its shebang (`./script.sh`) or explicitly with bash (`bash script.sh`).

#### Installation

Clone the repository and make the script executable:
```bash
git clone https://github.com/iandennismiller/vcf-to-obsidian-vcf-contacts.git
cd vcf-to-obsidian-vcf-contacts
chmod +x scripts/vcf-to-obsidian.sh
```

#### Usage

Convert all VCF files from a directory:
```bash
./scripts/vcf-to-obsidian.sh --folder ./contacts --obsidian ./obsidian-vault/contacts
```

Convert a specific VCF file:
```bash
./scripts/vcf-to-obsidian.sh --file ./contact.vcf --obsidian ./obsidian-vault/contacts
```

## Documentation

For detailed information, see the documentation in the [`/docs`](docs/) folder:

- **[Installation Guide](docs/installation.md)** - All installation options (pip, pipx, development setup)
- **[Usage Guide](docs/usage.md)** - Comprehensive usage examples and command-line options
- **[Implementation Comparison](docs/implementation-comparison.md)** - Comparing bash vs Python implementations
- **[VCF Support](docs/vcf-support.md)** - Supported vCard fields and filename generation
- **[Testing](docs/testing.md)** - Running and organizing tests
- **[Development](docs/development.md)** - Development setup and maintenance tasks

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Author

Ian Dennis Miller

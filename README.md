# vcf-to-obsidian-vcf-contacts

A collection of tools that batch-convert VCF files into Markdown files compatible with the [obsidian-vcf-contacts](https://github.com/broekema41/obsidian-vcf-contacts) plugin for ObsidianMD.

This repository provides three implementations:
- **Python script** - Full-featured implementation with robust vCard parsing
- **Node.js module** - Modern JavaScript implementation with comprehensive testing
- **Bash script** - Zero-dependency implementation for Unix environments

## Features

- Batch conversion of VCF files to Markdown format
- Compatible with [obsidian-vcf-contacts](https://github.com/broekema41/obsidian-vcf-contacts) plugin metadata structure  
- Preserves contact information including names, phone numbers, emails, addresses, and notes
- Support for both vCard 3.0 and 4.0 formats
- Intelligent filename generation with priority logic
- Command-line interface for easy automation

## Quick Start

### Python Implementation

#### Installation

```bash
pip install git+https://github.com/iandennismiller/vcf-to-obsidian-vcf-contacts.git
```

#### Usage

Convert all VCF files from a directory:
```bash
vcf-to-obsidian --folder ./contacts --obsidian ./obsidian-vault/contacts
```

### Node.js Implementation

#### Installation

```bash
cd nodejs-vcf-to-obsidian
npm install
```

#### Usage

Convert all VCF files from a directory:
```bash
node cli.js --folder ./contacts --obsidian ./obsidian-vault/contacts
```

Convert a specific VCF file:
```bash
node cli.js --file ./contact.vcf --obsidian ./obsidian-vault/contacts
```

### Bash Implementation (Zero Dependencies)

**Note:** The bash script requires bash 4.0+ for associative array support. macOS ships with bash 3.2 due to licensing restrictions, so macOS users should install bash 4.0+ via Homebrew (`brew install bash`) or use the Python implementation.

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

For detailed information, see the comprehensive documentation:

- **[Online Documentation](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/)** - Complete documentation hosted on GitHub Pages
- **[Build Documentation Locally](docx/)** - Build the documentation locally using Sphinx

### Quick Links:
- [Installation Guide](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/installation.html) - All installation options (pip, pipx, development setup)
- [Usage Guide](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/usage.html) - Comprehensive usage examples and command-line options
- [Integration Guide](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/integration.html) - Integration with vdirsyncer and other tools
- [Implementation Comparison](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/implementation-comparison.html) - Comparing bash vs Python implementations
- [VCF Support](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/vcf-support.html) - Supported vCard fields and filename generation
- [Testing](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/testing.html) - Running and organizing tests
- [Development](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/development.html) - Development setup and maintenance tasks
- [API Reference](https://iandennismiller.github.io/vcf-to-obsidian-vcf-contacts/autoapi/vcf_to_obsidian/index.html) - Complete API documentation

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Author

Ian Dennis Miller

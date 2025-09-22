# vcf-to-obsidian (Node.js Implementation)

A Node.js module that batch-converts VCF files into Markdown files that are compatible with obsidian-vcf-contacts plugin for ObsidianMD.

## Installation

```bash
npm install
```

## Usage

### Command Line Interface

```bash
# Convert a single VCF file
node cli.js --file path/to/contact.vcf --obsidian /path/to/obsidian/vault

# Convert all VCF files in a directory
node cli.js --folder /path/to/vcf/directory --obsidian /path/to/obsidian/vault

# Convert multiple sources
node cli.js --folder /dir1 --folder /dir2 --file /single/file.vcf --obsidian /path/to/obsidian/vault

# With verbose output
node cli.js --file contact.vcf --obsidian /path/to/vault --verbose

# Ignore specific files
node cli.js --folder /vcf/dir --ignore /vcf/dir/unwanted.vcf --obsidian /path/to/vault
```

### Programmatic Usage

```javascript
const { VCFConverter } = require('./lib');

const converter = new VCFConverter();

// Convert a single file
converter.convertVcfToMarkdown('/path/to/contact.vcf', '/path/to/output/directory');

// Convert multiple sources
converter.convertVcfFilesFromSources(
    ['/folder1', '/folder2'],    // folder sources
    ['/file1.vcf', '/file2.vcf'], // individual files
    '/output/directory',          // output directory
    ['/ignore.vcf'],             // files to ignore (optional)
    true                         // verbose output (optional)
);
```

## Features

- **Priority-based filename generation**:
  1. Full Name (FN) field
  2. Constructed name from given + family names
  3. UID field
  4. Original VCF filename

- **Complete vCard field support**:
  - Names (FN, N fields)
  - Contact info (EMAIL, TEL with types)
  - Addresses (ADR with types)
  - Organization (ORG)
  - Birthday (BDAY)
  - URLs (URL)
  - Notes (NOTE)
  - Categories (CATEGORIES)
  - Photos (PHOTO)
  - UID tracking for duplicate handling

- **Smart duplicate handling**: Removes old files with same UID when contact name changes
- **File modification checking**: Skips conversion if VCF is not newer than existing markdown
- **Filesystem-safe filenames**: Automatically cleans invalid characters

## Testing

```bash
npm test
```

## Dependencies

- `commander`: Command line interface
- `vcard-parser`: VCF file parsing
- `jest`: Testing framework (dev dependency)

## License

MIT - See LICENSE file for details

## Author

Ian Dennis Miller
#!/usr/bin/env node

/**
 * CLI interface for vcf-to-obsidian
 * 
 * A Node.js script that batch-converts a folder containing VCF files into Markdown files
 * that are compatible with obsidian-vcf-contacts plugin for ObsidianMD.
 */

const { Command } = require('commander');
const path = require('path');
const { VCFConverter } = require('./lib');

const program = new Command();

program
    .name('vcf-to-obsidian')
    .description('Convert VCF files to Markdown format for obsidian-vcf-contacts plugin')
    .version('1.0.0');

program
    .option('--folder <path>', 'Source directory containing VCF files (can be specified multiple times)', (value, previous) => {
        return previous ? previous.concat([value]) : [value];
    }, [])
    .option('--obsidian <path>', 'Destination directory for Markdown files (required)')
    .option('--file <path>', 'Specific VCF file to process (can be specified multiple times)', (value, previous) => {
        return previous ? previous.concat([value]) : [value];
    }, [])
    .option('-v, --verbose', 'Enable verbose output')
    .option('--ignore <path>', 'Specific VCF file to ignore (can be specified multiple times)', (value, previous) => {
        return previous ? previous.concat([value]) : [value];
    }, []);

program.parse();

const options = program.opts();

// Validate required options
if (!options.obsidian) {
    console.error('Error: --obsidian option is required');
    program.help();
}

// Validate that at least one source is provided
if (options.folder.length === 0 && options.file.length === 0) {
    console.error('Error: At least one --folder or --file option must be provided');
    program.help();
}

// Convert relative paths to absolute paths
const folders = options.folder.map(f => path.resolve(f));
const files = options.file.map(f => path.resolve(f));
const ignore = options.ignore.map(f => path.resolve(f));
const obsidianDir = path.resolve(options.obsidian);

// Create converter and process tasks
const converter = new VCFConverter();
converter.processTasks(folders, obsidianDir, files, options.verbose, ignore);
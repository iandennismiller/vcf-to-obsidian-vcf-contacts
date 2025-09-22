/**
 * Integration tests for VCF Converter
 */

const fs = require('fs');
const path = require('path');
const VCFConverter = require('../../nodejs-vcf-to-obsidian/lib/vcf-converter');

describe('VCFConverter Integration', () => {
    let converter;
    let tempOutputDir;

    beforeEach(() => {
        converter = new VCFConverter();
        tempOutputDir = '/tmp/jest-test-output-' + Date.now();
        
        // Create temp directory
        if (!fs.existsSync(tempOutputDir)) {
            fs.mkdirSync(tempOutputDir, { recursive: true });
        }
    });

    afterEach(() => {
        // Cleanup temp directory
        if (fs.existsSync(tempOutputDir)) {
            const files = fs.readdirSync(tempOutputDir);
            for (const file of files) {
                fs.unlinkSync(path.join(tempOutputDir, file));
            }
            fs.rmdirSync(tempOutputDir);
        }
    });

    describe('convertVcfToMarkdown', () => {
        test('should convert basic VCF file to markdown', () => {
            const vcfPath = path.join(__dirname, '../../tests/data/content_generation_test.vcf');
            
            const result = converter.convertVcfToMarkdown(vcfPath, tempOutputDir);
            expect(result).toBe(true);
            
            const outputFile = path.join(tempOutputDir, 'Test User.md');
            expect(fs.existsSync(outputFile)).toBe(true);
            
            const content = fs.readFileSync(outputFile, 'utf-8');
            expect(content).toContain('FN: Test User');
            expect(content).toContain('UID: content-test-123');
            expect(content).toContain('ORG: Test Organization');
        });

        test('should handle filename with special characters', () => {
            const vcfPath = path.join(__dirname, '../../tests/data/special_characters_filename.vcf');
            
            const result = converter.convertVcfToMarkdown(vcfPath, tempOutputDir);
            expect(result).toBe(true);
            
            // Check that the output file was created with cleaned filename
            const files = fs.readdirSync(tempOutputDir);
            expect(files.length).toBe(1);
            expect(files[0]).toMatch(/\.md$/);
        });

        test('should handle VCF file with minimal data', () => {
            const vcfPath = path.join(__dirname, '../../tests/data/minimal_contact.vcf');
            
            const result = converter.convertVcfToMarkdown(vcfPath, tempOutputDir);
            expect(result).toBe(true);
            
            const files = fs.readdirSync(tempOutputDir);
            expect(files.length).toBe(1);
        });
    });

    describe('convertVcfFilesFromSources', () => {
        test('should convert multiple files from folder source', () => {
            const testDataDir = path.join(__dirname, '../../tests/data');
            
            const result = converter.convertVcfFilesFromSources([testDataDir], [], tempOutputDir);
            
            expect(result.successful).toBeGreaterThan(0);
            expect(result.total).toBeGreaterThan(0);
            expect(result.successful).toBeLessThanOrEqual(result.total);
            
            // Check that some markdown files were created
            const files = fs.readdirSync(tempOutputDir);
            const mdFiles = files.filter(f => f.endsWith('.md'));
            expect(mdFiles.length).toBeGreaterThan(0);
        });

        test('should convert individual file sources', () => {
            const vcfPath = path.join(__dirname, '../../tests/data/content_generation_test.vcf');
            
            const result = converter.convertVcfFilesFromSources([], [vcfPath], tempOutputDir);
            
            expect(result.successful).toBe(1);
            expect(result.total).toBe(1);
            
            const outputFile = path.join(tempOutputDir, 'Test User.md');
            expect(fs.existsSync(outputFile)).toBe(true);
        });
    });
});
/**
 * Tests for Filename Generator module
 */

const path = require('path');
const FilenameGenerator = require('../../nodejs-vcf-to-obsidian/lib/filename-generator');

describe('FilenameGenerator', () => {
    let generator;

    beforeEach(() => {
        generator = new FilenameGenerator();
    });

    describe('generateFilename', () => {
        test('should prioritize FN field', () => {
            const vcard = {
                fn: [{ value: 'John Doe' }],
                n: [{ value: ['Smith', 'John', '', '', ''] }],
                uid: [{ value: 'test-uid' }]
            };
            const vcfPath = '/test/path.vcf';
            
            const result = generator.generateFilename(vcard, vcfPath);
            expect(result).toBe('John Doe');
        });

        test('should use constructed name when FN is not available', () => {
            const vcard = {
                n: [{ value: ['Smith', 'John', '', '', ''] }],
                uid: [{ value: 'test-uid' }]
            };
            const vcfPath = '/test/path.vcf';
            
            const result = generator.generateFilename(vcard, vcfPath);
            expect(result).toBe('John Smith');
        });

        test('should use UID when names are not available', () => {
            const vcard = {
                uid: [{ value: 'test-uid-12345' }]
            };
            const vcfPath = '/test/path.vcf';
            
            const result = generator.generateFilename(vcard, vcfPath);
            expect(result).toBe('test-uid-12345');
        });

        test('should use VCF filename as last resort', () => {
            const vcard = {};
            const vcfPath = '/test/fallback-name.vcf';
            
            const result = generator.generateFilename(vcard, vcfPath);
            expect(result).toBe('fallback-name');
        });

        test('should clean invalid characters', () => {
            const vcard = {
                fn: [{ value: 'John<>:"/\\|?*Doe' }]
            };
            const vcfPath = '/test/path.vcf';
            
            const result = generator.generateFilename(vcard, vcfPath);
            expect(result).toBe('John_________Doe');
        });
    });
});
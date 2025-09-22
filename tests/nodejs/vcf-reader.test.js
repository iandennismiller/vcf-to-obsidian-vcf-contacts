/**
 * Tests for VCF Reader module
 */

const path = require('path');
const VCFReader = require('../../nodejs-vcf-to-obsidian/lib/vcf-reader');

describe('VCFReader', () => {
    let reader;

    beforeEach(() => {
        reader = new VCFReader();
    });

    describe('isValidUuid', () => {
        test('should return true for valid UUID', () => {
            const validUuid = '123e4567-e89b-12d3-a456-426614174000';
            expect(reader.isValidUuid(validUuid)).toBe(true);
        });

        test('should return false for invalid UUID', () => {
            expect(reader.isValidUuid('not-a-uuid')).toBe(false);
            expect(reader.isValidUuid('')).toBe(false);
            expect(reader.isValidUuid(null)).toBe(false);
            expect(reader.isValidUuid(undefined)).toBe(false);
        });
    });

    describe('readVcfFile', () => {
        test('should read and parse basic VCF file', () => {
            const vcfPath = path.join(__dirname, '../../tests/data/content_generation_test.vcf');
            const result = reader.readVcfFile(vcfPath);
            
            expect(result).toBeDefined();
            expect(result.fn).toBeDefined();
            expect(result.fn[0].value).toBe('Test User');
            expect(result.uid[0].value).toBe('content-test-123');
        });

        test('should throw error for non-existent file', () => {
            expect(() => {
                reader.readVcfFile('/path/that/does/not/exist.vcf');
            }).toThrow();
        });
    });
});
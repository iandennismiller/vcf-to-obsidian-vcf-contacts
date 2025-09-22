/**
 * Tests for Markdown Writer module
 */

const MarkdownWriter = require('../../nodejs-vcf-to-obsidian/lib/markdown-writer');

describe('MarkdownWriter', () => {
    let writer;

    beforeEach(() => {
        writer = new MarkdownWriter();
    });

    describe('generateObsidianMarkdown', () => {
        test('should generate basic markdown for simple vcard', () => {
            const vcard = {
                fn: [{ value: 'John Doe' }],
                n: [{ value: ['Doe', 'John', '', '', ''] }],
                uid: [{ value: 'test-uid' }],
                version: [{ value: '3.0' }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            
            expect(result).toContain('---');
            expect(result).toContain('N.FN: Doe');
            expect(result).toContain('N.GN: John');
            expect(result).toContain('FN: John Doe');
            expect(result).toContain('UID: test-uid');
            expect(result).toContain('VERSION: "3.0"');
            expect(result).toContain('REV:');
            expect(result).toContain('#### Notes');
            expect(result).toContain('#Contact');
        });

        test('should handle email with type', () => {
            const vcard = {
                fn: [{ value: 'Test User' }],
                email: [{ 
                    value: 'test@example.com',
                    meta: { type: ['WORK'] }
                }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            expect(result).toContain('"EMAIL[WORK]": test@example.com');
        });

        test('should handle telephone with type', () => {
            const vcard = {
                fn: [{ value: 'Test User' }],
                tel: [{ 
                    value: '+1-555-123-4567',
                    meta: { type: ['HOME'] }
                }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            expect(result).toContain('"TEL[HOME]": "+1-555-123-4567"');
        });

        test('should handle birthday', () => {
            const vcard = {
                fn: [{ value: 'Test User' }],
                bday: [{ value: '1990-01-01' }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            expect(result).toContain('BDAY: 1990-01-01');
        });

        test('should handle organization', () => {
            const vcard = {
                fn: [{ value: 'Test User' }],
                org: [{ value: 'Test Company' }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            expect(result).toContain('ORG: Test Company');
        });

        test('should handle URL with default type', () => {
            const vcard = {
                fn: [{ value: 'Test User' }],
                url: [{ value: 'https://example.com' }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            expect(result).toContain('"URL[DEFAULT]": https://example.com');
        });

        test('should handle note field', () => {
            const vcard = {
                fn: [{ value: 'Test User' }],
                note: [{ value: 'This is a test note' }]
            };
            
            const result = writer.generateObsidianMarkdown(vcard);
            expect(result).toContain('NOTE: This is a test note');
        });
    });
});
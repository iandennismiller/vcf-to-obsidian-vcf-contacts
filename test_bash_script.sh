#!/bin/bash

# Simple test script for vcf-to-obsidian.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/test_data/vcf"
OUTPUT_DIR="/tmp/vcf_to_obsidian_test"

echo "Testing vcf-to-obsidian.sh..."

# Clean up previous test runs
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Test 1: Single file processing
echo "Test 1: Processing single VCF file..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

if [[ ! -f "$OUTPUT_DIR/Test User.md" ]]; then
    echo "FAIL: Expected output file 'Test User.md' not found"
    exit 1
fi

echo "✓ Test 1 passed"

# Test 2: Folder processing
echo "Test 2: Processing folder..."
rm -rf "$OUTPUT_DIR"/*
"$VCF_TO_OBSIDIAN" --folder "$TEST_DATA_DIR" --obsidian "$OUTPUT_DIR"

# Count generated files (some may be overwritten due to duplicate names)
file_count=$(ls -1 "$OUTPUT_DIR"/*.md 2>/dev/null | wc -l)
expected_min=10  # At least 10 unique files should be generated

if [[ $file_count -lt $expected_min ]]; then
    echo "FAIL: Expected at least $expected_min files, got $file_count"
    exit 1
fi

echo "✓ Test 2 passed"

# Test 3: Filename priority tests
echo "Test 3: Testing filename priorities..."
rm -rf "$OUTPUT_DIR"/*

# FN priority
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/priority_test_fn_over_uid.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/Priority Test 1.md" ]]; then
    echo "FAIL: FN priority test failed"
    exit 1
fi

# Constructed name priority
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/priority_test_constructed_over_uid.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/Priority ConstructedTest.md" ]]; then
    echo "FAIL: Constructed name priority test failed"
    exit 1
fi

# UID fallback
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/uid_only_no_names.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/only-uid-available-12345.md" ]]; then
    echo "FAIL: UID fallback test failed"
    exit 1
fi

echo "✓ Test 3 passed"

# Test 4: Special character handling
echo "Test 4: Testing special character handling..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/special_characters_filename.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/John _Doe_ _test@email.com_.md" ]]; then
    echo "FAIL: Special character handling test failed"
    exit 1
fi

echo "✓ Test 4 passed"

# Test 5: Content validation
echo "Test 5: Validating output content..."
rm -rf "$OUTPUT_DIR"/*
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

# Check if the markdown file contains expected frontmatter
output_file="$OUTPUT_DIR/Test User.md"
if ! grep -q "FN: Test User" "$output_file"; then
    echo "FAIL: Output file missing FN field"
    exit 1
fi

if ! grep -q "UID: content-test-123" "$output_file"; then
    echo "FAIL: Output file missing UID field"
    exit 1
fi

if ! grep -q "ORG: Test Organization" "$output_file"; then
    echo "FAIL: Output file missing ORG field"
    exit 1
fi

echo "✓ Test 5 passed"

# Test 6: VCard 4.0 support
echo "Test 6: Testing VCard 4.0 support..."
rm -rf "$OUTPUT_DIR"/*
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Jane Doe.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: VCard 4.0 file not processed"
    exit 1
fi

if ! grep -q "VERSION: \"4.0\"" "$output_file"; then
    echo "FAIL: VCard 4.0 version not detected"
    exit 1
fi

echo "✓ Test 6 passed"

echo ""
echo "All tests passed! ✅"
echo "Generated files are in: $OUTPUT_DIR"
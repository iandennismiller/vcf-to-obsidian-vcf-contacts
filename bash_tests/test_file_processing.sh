#!/bin/bash

# Test file processing functionality (single file and folder processing)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../scripts/vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../test_data/vcf"
OUTPUT_DIR="/tmp/vcf_to_obsidian_test_file_processing"

echo "Running file processing tests..."

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

echo "✓ Test 1 passed: Single file processing"

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

echo "✓ Test 2 passed: Folder processing"

# Test 3: Multiple files with --file option
echo "Test 3: Processing multiple files with --file option..."
rm -rf "$OUTPUT_DIR"/*
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR"

if [[ ! -f "$OUTPUT_DIR/Test User.md" ]] || [[ ! -f "$OUTPUT_DIR/Jane Doe.md" ]]; then
    echo "FAIL: Expected output files not found for multiple --file processing"
    exit 1
fi

echo "✓ Test 3 passed: Multiple file processing"

# Test 4: Mixed sources (folder and file)
echo "Test 4: Processing mixed sources..."
rm -rf "$OUTPUT_DIR"/*
mkdir -p "/tmp/test_vcf_subset"
cp "$TEST_DATA_DIR/content_generation_test.vcf" "/tmp/test_vcf_subset/"

"$VCF_TO_OBSIDIAN" --folder "/tmp/test_vcf_subset" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR"

if [[ ! -f "$OUTPUT_DIR/Test User.md" ]] || [[ ! -f "$OUTPUT_DIR/Jane Doe.md" ]]; then
    echo "FAIL: Expected output files not found for mixed source processing"
    exit 1
fi

echo "✓ Test 4 passed: Mixed source processing"

# Clean up
rm -rf "/tmp/test_vcf_subset"
rm -rf "$OUTPUT_DIR"

echo "All file processing tests passed! ✅"
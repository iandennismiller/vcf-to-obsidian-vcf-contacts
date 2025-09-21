#!/bin/bash

# Test file processing functionality (single file and folder processing)

set -e

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh"

OUTPUT_DIR=$(create_unique_test_dir "file_processing")

echo "Running file processing tests..."

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
OUTPUT_DIR_2=$(create_unique_test_dir "file_processing_folder")
"$VCF_TO_OBSIDIAN" --folder "$TEST_DATA_DIR" --obsidian "$OUTPUT_DIR_2"

# Count generated files (some may be overwritten due to duplicate names)
file_count=$(ls -1 "$OUTPUT_DIR_2"/*.md 2>/dev/null | wc -l)
expected_min=10  # At least 10 unique files should be generated

if [[ $file_count -lt $expected_min ]]; then
    echo "FAIL: Expected at least $expected_min files, got $file_count"
    exit 1
fi

echo "✓ Test 2 passed: Folder processing"

# Test 3: Multiple files with --file option
echo "Test 3: Processing multiple files with --file option..."
OUTPUT_DIR_3=$(create_unique_test_dir "file_processing_multiple")
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR_3"

if [[ ! -f "$OUTPUT_DIR_3/Test User.md" ]] || [[ ! -f "$OUTPUT_DIR_3/Jane Doe.md" ]]; then
    echo "FAIL: Expected output files not found for multiple --file processing"
    exit 1
fi

echo "✓ Test 3 passed: Multiple file processing"

# Test 4: Mixed sources (folder and file)
echo "Test 4: Processing mixed sources..."
OUTPUT_DIR_4=$(create_unique_test_dir "file_processing_mixed")
TEMP_VCF_DIR=$(create_unique_test_dir "temp_vcf_subset")
cp "$TEST_DATA_DIR/content_generation_test.vcf" "$TEMP_VCF_DIR/"

"$VCF_TO_OBSIDIAN" --folder "$TEMP_VCF_DIR" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR_4"

if [[ ! -f "$OUTPUT_DIR_4/Test User.md" ]] || [[ ! -f "$OUTPUT_DIR_4/Jane Doe.md" ]]; then
    echo "FAIL: Expected output files not found for mixed source processing"
    exit 1
fi

echo "✓ Test 4 passed: Mixed source processing"

echo "All file processing tests passed! ✅"
#!/bin/bash

# Test special character handling in filenames and UIDs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../../scripts/vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../data/vcf"
OUTPUT_DIR="/tmp/vcf_to_obsidian_test_special_chars"

echo "Running special character handling tests..."

# Clean up previous test runs
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Test 1: Special characters in FN field
echo "Test 1: Testing special character handling in filename..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/special_characters_filename.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/John _Doe_ _test@email.com_.md" ]]; then
    echo "FAIL: Special character handling test failed"
    echo "Expected: 'John _Doe_ _test@email.com_.md'"
    echo "Available files:"
    ls -la "$OUTPUT_DIR"
    exit 1
fi
echo "✓ Test 1 passed: Special characters in FN"

# Test 2: Special characters in UID field (fallback scenario)
echo "Test 2: Testing special character handling in UID..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/uid_special_chars_fallback.vcf" --obsidian "$OUTPUT_DIR"
# This should create a file with cleaned UID as filename
if [[ ! -f "$OUTPUT_DIR/special_chars_in_uid_file_name_.md" ]]; then
    echo "FAIL: Special character UID handling test failed"
    echo "Expected: 'special_chars_in_uid_file_name_.md'"
    echo "Available files:"
    ls -la "$OUTPUT_DIR"
    exit 1
fi
echo "✓ Test 2 passed: Special characters in UID"

# Test 3: Another special character scenario
echo "Test 3: Testing another special character scenario..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/special_characters_uid.vcf" --obsidian "$OUTPUT_DIR"
# This should use the name from N field instead of special char UID
if [[ ! -f "$OUTPUT_DIR/User Test.md" ]]; then
    echo "FAIL: Special character UID with name test failed"
    echo "Expected: 'User Test.md'"
    echo "Available files:"
    ls -la "$OUTPUT_DIR"
    exit 1
fi
echo "✓ Test 3 passed: Special characters with name fallback"

# Test 4: Verify that invalid filename characters are properly replaced
echo "Test 4: Verifying filename character replacement..."
# Check that all generated files have valid filenames (no invalid chars)
for file in "$OUTPUT_DIR"/*.md; do
    filename=$(basename "$file")
    # Check for invalid characters that should have been replaced
    if echo "$filename" | grep -q '[<>:"/\\|?*]'; then
        echo "FAIL: Found invalid characters in filename: $filename"
        exit 1
    fi
done
echo "✓ Test 4 passed: Filename character replacement"

# Clean up
rm -rf "$OUTPUT_DIR"

echo "All special character handling tests passed! ✅"
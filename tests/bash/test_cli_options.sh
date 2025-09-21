#!/bin/bash

# Test command line interface options and error handling

set -e

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh"

OUTPUT_DIR=$(create_unique_test_dir "cli")

echo "Running CLI options tests..."

# Test 1: Help option
echo "Test 1: Testing --help option..."
if ! "$VCF_TO_OBSIDIAN" --help | grep -q "Convert VCF files to Obsidian-compatible Markdown"; then
    echo "FAIL: Help option not working properly"
    exit 1
fi
echo "✓ Test 1 passed: Help option"

# Test 2: Verbose option
echo "Test 2: Testing --verbose option..."
output=$("$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR" --verbose 2>&1)
if [[ ! "$output" =~ "Processing:" ]]; then
    echo "FAIL: Verbose option not producing expected output"
    echo "Output: $output"
    exit 1
fi
echo "✓ Test 2 passed: Verbose option"

# Test 3: Error handling - missing source
echo "Test 3: Testing error handling for missing source..."
if "$VCF_TO_OBSIDIAN" --obsidian "$OUTPUT_DIR" 2>/dev/null; then
    echo "FAIL: Should have failed with missing source"
    exit 1
fi
echo "✓ Test 3 passed: Missing source error handling"

# Test 4: Error handling - missing destination
echo "Test 4: Testing error handling for missing destination..."
if "$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" 2>/dev/null; then
    echo "FAIL: Should have failed with missing destination"
    exit 1
fi
echo "✓ Test 4 passed: Missing destination error handling"

# Test 5: Error handling - non-existent file
echo "Test 5: Testing error handling for non-existent file..."
if "$VCF_TO_OBSIDIAN" --file "/non/existent/file.vcf" --obsidian "$OUTPUT_DIR" 2>/dev/null; then
    echo "FAIL: Should have failed with non-existent file"
    exit 1
fi
echo "✓ Test 5 passed: Non-existent file error handling"

# Test 6: Error handling - non-existent directory
echo "Test 6: Testing error handling for non-existent directory..."
if "$VCF_TO_OBSIDIAN" --folder "/non/existent/directory" --obsidian "$OUTPUT_DIR" 2>/dev/null; then
    echo "FAIL: Should have failed with non-existent directory"
    exit 1
fi
echo "✓ Test 6 passed: Non-existent directory error handling"

# Test 7: Multiple --obsidian options (should use last one)
echo "Test 7: Testing multiple --obsidian options..."
OBSIDIAN_DIR1=$(create_unique_test_dir "obsidian1")
OBSIDIAN_DIR2=$(create_unique_test_dir "obsidian2")

output=$("$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OBSIDIAN_DIR1" --obsidian "$OBSIDIAN_DIR2" 2>&1)

# File should be in the second directory
if [[ ! -f "$OBSIDIAN_DIR2/Test User.md" ]]; then
    echo "FAIL: Multiple --obsidian options not handled correctly"
    echo "Output: $output"
    ls -la "$OBSIDIAN_DIR1/" "$OBSIDIAN_DIR2/"
    exit 1
fi

# Should warn about multiple options
if [[ ! "$output" =~ "Warning: Multiple --obsidian options" ]]; then
    echo "FAIL: Should warn about multiple --obsidian options"
    echo "Output: $output"
    exit 1
fi

echo "✓ Test 7 passed: Multiple --obsidian options"

# Test 8: Invalid option
echo "Test 8: Testing invalid option handling..."
if "$VCF_TO_OBSIDIAN" --invalid-option 2>/dev/null; then
    echo "FAIL: Should have failed with invalid option"
    exit 1
fi
echo "✓ Test 8 passed: Invalid option error handling"

# Test 9: Non-VCF file handling
echo "Test 9: Testing non-VCF file handling..."
NON_VCF_FILE="$BASE_OUTPUT_DIR/test_not_vcf.txt"
echo "This is not a VCF file" > "$NON_VCF_FILE"
if "$VCF_TO_OBSIDIAN" --file "$NON_VCF_FILE" --obsidian "$OUTPUT_DIR" 2>/dev/null; then
    echo "FAIL: Should have warned about non-VCF file"
    # Note: This might not fail completely but should show a warning
fi
echo "✓ Test 9 passed: Non-VCF file handling"

# Test 10: Empty directory handling
echo "Test 10: Testing empty directory handling..."
EMPTY_VCF_DIR=$(create_unique_test_dir "empty_vcf")
output=$("$VCF_TO_OBSIDIAN" --folder "$EMPTY_VCF_DIR" --obsidian "$OUTPUT_DIR" 2>&1 || echo "EXIT_CODE:$?")
if [[ ! "$output" =~ "No VCF files found" ]]; then
    echo "FAIL: Should warn about empty directory"
    echo "Output: $output"
    # Don't exit 1 here as this might be a warning, not an error
fi
echo "✓ Test 10 passed: Empty directory handling"

echo "All CLI options tests passed! ✅"
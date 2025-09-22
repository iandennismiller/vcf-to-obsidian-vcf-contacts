#!/bin/bash

# Test REV timestamp functionality

set -e

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh"

OUTPUT_DIR=$(create_unique_test_dir "rev")

echo "Running REV timestamp tests..."

# Test 1: REV timestamp presence and format
echo "Test 1: Validating REV timestamp presence and format..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Test User.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check if REV attribute is present
if ! grep -q "REV: " "$output_file"; then
    echo "FAIL: REV attribute not found in output"
    cat "$output_file"
    exit 1
fi

# Extract REV timestamp and validate format
rev_line=$(grep "REV: " "$output_file")
rev_timestamp=$(echo "$rev_line" | sed 's/REV: //')

# Validate format: YYYYMMDDTHHMMSSZ (16 characters)
if [[ ${#rev_timestamp} -ne 16 ]]; then
    echo "FAIL: REV timestamp should be 16 characters, got ${#rev_timestamp}: $rev_timestamp"
    exit 1
fi

if [[ ! "$rev_timestamp" =~ ^[0-9]{8}T[0-9]{6}Z$ ]]; then
    echo "FAIL: REV timestamp format invalid. Expected YYYYMMDDTHHMMSSZ, got: $rev_timestamp"
    exit 1
fi

echo "✓ Test 1 passed: REV timestamp format validation"

# Test 2: REV timestamp updates only when VCF is newer
echo "Test 2: Validating REV timestamp updates when VCF is newer..."

# Get first timestamp
first_timestamp="$rev_timestamp"

# Second conversion immediately - should skip since VCF is not newer
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

# Get second timestamp
second_rev_line=$(grep "REV: " "$output_file")
second_timestamp=$(echo "$second_rev_line" | sed 's/REV: //')

if [[ "$first_timestamp" != "$second_timestamp" ]]; then
    echo "FAIL: REV timestamp should NOT update when VCF is not newer"
    echo "First: $first_timestamp"
    echo "Second: $second_timestamp"
    exit 1
fi

# Now make VCF file newer and test again
sleep 1
touch "$TEST_DATA_DIR/content_generation_test.vcf"
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

# Get third timestamp
third_rev_line=$(grep "REV: " "$output_file")
third_timestamp=$(echo "$third_rev_line" | sed 's/REV: //')

if [[ "$second_timestamp" == "$third_timestamp" ]]; then
    echo "FAIL: REV timestamp should update when VCF is newer"
    echo "Second: $second_timestamp"
    echo "Third: $third_timestamp"
    exit 1
fi

echo "✓ Test 2 passed: REV timestamp updates correctly only when VCF is newer"

# Test 3: REV timestamp in different VCF files
echo "Test 3: Validating REV in different VCF files..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR"

vcard4_output="$OUTPUT_DIR/Jane Doe.md"
if [[ ! -f "$vcard4_output" ]]; then
    echo "FAIL: VCard 4.0 output file not created"
    exit 1
fi

if ! grep -q "REV: " "$vcard4_output"; then
    echo "FAIL: REV attribute not found in VCard 4.0 output"
    cat "$vcard4_output"
    exit 1
fi

# Extract and validate VCard 4.0 REV timestamp
vcard4_rev_line=$(grep "REV: " "$vcard4_output")
vcard4_timestamp=$(echo "$vcard4_rev_line" | sed 's/REV: //')

if [[ ! "$vcard4_timestamp" =~ ^[0-9]{8}T[0-9]{6}Z$ ]]; then
    echo "FAIL: VCard 4.0 REV timestamp format invalid: $vcard4_timestamp"
    exit 1
fi

echo "✓ Test 3 passed: REV in different VCF files"

# Test 4: REV timestamp consistency across multiple files in batch
echo "Test 4: Validating REV in batch processing..."
OUTPUT_DIR_4=$(create_unique_test_dir "rev_batch")
"$VCF_TO_OBSIDIAN" --folder "$TEST_DATA_DIR" --obsidian "$OUTPUT_DIR_4"

# Check that all generated files have REV timestamps
rev_count=0
total_files=0

for md_file in "$OUTPUT_DIR_4"/*.md; do
    if [[ -f "$md_file" ]]; then
        total_files=$((total_files + 1))
        if grep -q "REV: " "$md_file"; then
            rev_count=$((rev_count + 1))
        else
            echo "FAIL: File missing REV timestamp: $(basename "$md_file")"
            exit 1
        fi
    fi
done

if [[ $rev_count -ne $total_files ]]; then
    echo "FAIL: Not all files have REV timestamps. Found $rev_count REV in $total_files files"
    exit 1
fi

echo "✓ Test 4 passed: REV in batch processing ($rev_count/$total_files files)"

echo "All REV timestamp tests passed! ✅"
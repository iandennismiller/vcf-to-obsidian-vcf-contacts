#!/bin/bash

# Test REV timestamp functionality

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../test_data/vcf"
OUTPUT_DIR="/tmp/vcf_to_obsidian_test_rev"

echo "Running REV timestamp tests..."

# Clean up previous test runs
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

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

# Test 2: REV timestamp updates on each conversion
echo "Test 2: Validating REV timestamp updates..."

# Get first timestamp
first_timestamp="$rev_timestamp"

# Wait a moment and convert again
sleep 1
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

# Get second timestamp
second_rev_line=$(grep "REV: " "$output_file")
second_timestamp=$(echo "$second_rev_line" | sed 's/REV: //')

if [[ "$first_timestamp" == "$second_timestamp" ]]; then
    echo "FAIL: REV timestamp should update on each conversion"
    echo "First: $first_timestamp"
    echo "Second: $second_timestamp"
    exit 1
fi

echo "✓ Test 2 passed: REV timestamp updates correctly"

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
rm -rf "$OUTPUT_DIR"/*
"$VCF_TO_OBSIDIAN" --folder "$TEST_DATA_DIR" --obsidian "$OUTPUT_DIR"

# Check that all generated files have REV timestamps
rev_count=0
total_files=0

for md_file in "$OUTPUT_DIR"/*.md; do
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

# Clean up
rm -rf "$OUTPUT_DIR"

echo "All REV timestamp tests passed! ✅"
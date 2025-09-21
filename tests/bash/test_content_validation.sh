#!/bin/bash

# Test output content validation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
<<<<<<< HEAD:bash_tests/test_content_validation.sh
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../scripts/vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../test_data/vcf"
=======
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../../vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../data/vcf"
>>>>>>> main:tests/bash/test_content_validation.sh
OUTPUT_DIR="/tmp/vcf_to_obsidian_test_content"

echo "Running content validation tests..."

# Clean up previous test runs
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Test 1: Basic content validation
echo "Test 1: Validating basic output content..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Test User.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check if the markdown file contains expected frontmatter
if ! grep -q "FN: Test User" "$output_file"; then
    echo "FAIL: Output file missing FN field"
    cat "$output_file"
    exit 1
fi

if ! grep -q "UID: content-test-123" "$output_file"; then
    echo "FAIL: Output file missing UID field"
    cat "$output_file"
    exit 1
fi

if ! grep -q "ORG: Test Organization" "$output_file"; then
    echo "FAIL: Output file missing ORG field"
    cat "$output_file"
    exit 1
fi

echo "✓ Test 1 passed: Basic content validation"

# Test 2: Frontmatter structure validation
echo "Test 2: Validating frontmatter structure..."
if ! grep -q "^---$" "$output_file"; then
    echo "FAIL: Missing frontmatter delimiters"
    exit 1
fi

# Count frontmatter delimiters (should be exactly 2)
delimiter_count=$(grep -c "^---$" "$output_file")
if [[ $delimiter_count -ne 2 ]]; then
    echo "FAIL: Expected 2 frontmatter delimiters, found $delimiter_count"
    exit 1
fi

echo "✓ Test 2 passed: Frontmatter structure"

# Test 3: Contact fields validation
echo "Test 3: Validating contact fields..."
if ! grep -q "N.FN: User" "$output_file"; then
    echo "FAIL: Missing structured family name"
    exit 1
fi

if ! grep -q "N.GN: Test" "$output_file"; then
    echo "FAIL: Missing structured given name"
    exit 1
fi

if ! grep -q '"EMAIL\[WORK\]": test@example.com' "$output_file"; then
    echo "FAIL: Missing email field with type"
    exit 1
fi

if ! grep -q '"TEL\[WORK\]": "+1-555-123-4567"' "$output_file"; then
    echo "FAIL: Missing phone field with type"
    exit 1
fi

echo "✓ Test 3 passed: Contact fields validation"

# Test 4: Contact tags validation
echo "Test 4: Validating contact tags..."
if ! grep -q "#Contact" "$output_file"; then
    echo "FAIL: Missing contact tag"
    exit 1
fi

if ! grep -q "#### Notes" "$output_file"; then
    echo "FAIL: Missing notes section"
    exit 1
fi

echo "✓ Test 4 passed: Contact tags validation"

# Test 5: REV timestamp validation
echo "Test 5: Validating REV timestamp..."
if ! grep -q "REV: " "$output_file"; then
    echo "FAIL: Missing REV timestamp"
    exit 1
fi

# Validate REV format: YYYYMMDDTHHMMSSZ
rev_line=$(grep "REV: " "$output_file")
rev_timestamp=$(echo "$rev_line" | sed 's/REV: //')

if [[ ! "$rev_timestamp" =~ ^[0-9]{8}T[0-9]{6}Z$ ]]; then
    echo "FAIL: REV timestamp format invalid. Expected YYYYMMDDTHHMMSSZ, got: $rev_timestamp"
    exit 1
fi

echo "✓ Test 5 passed: REV timestamp validation"

# Test 6: Complex contact validation (VCard 4.0)
echo "Test 6: Validating complex contact content..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR"

complex_file="$OUTPUT_DIR/Jane Doe.md"
if [[ ! -f "$complex_file" ]]; then
    echo "FAIL: Complex contact file not created"
    exit 1
fi

# Check for address fields
if ! grep -q 'ADR\[HOME\]\.STREET' "$complex_file"; then
    echo "FAIL: Missing home address street"
    exit 1
fi

if ! grep -q 'ADR\[WORK\]\.LOCALITY' "$complex_file"; then
    echo "FAIL: Missing work address locality"
    exit 1
fi

# Check for multiple emails
if ! grep -q 'EMAIL\[HOME\]' "$complex_file" || ! grep -q 'EMAIL\[WORK\]' "$complex_file"; then
    echo "FAIL: Missing multiple email types"
    exit 1
fi

# Check for REV timestamp in complex file too
if ! grep -q "REV: " "$complex_file"; then
    echo "FAIL: Missing REV timestamp in complex contact"
    exit 1
fi

echo "✓ Test 6 passed: Complex contact validation"

# Test 7: Empty fields handling
echo "Test 7: Validating empty fields handling..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/minimal_contact.vcf" --obsidian "$OUTPUT_DIR"

minimal_file="$OUTPUT_DIR/minimal_contact.md"
if [[ ! -f "$minimal_file" ]]; then
    echo "FAIL: Minimal contact file not created"
    exit 1
fi

# Should still have valid frontmatter structure even with minimal data
if ! grep -q "^---$" "$minimal_file"; then
    echo "FAIL: Minimal contact missing frontmatter"
    exit 1
fi

# Verify REV timestamp in minimal file too
if ! grep -q "REV: " "$minimal_file"; then
    echo "FAIL: Missing REV timestamp in minimal contact"
    exit 1
fi

echo "✓ Test 7 passed: Empty fields handling"

# Clean up
rm -rf "$OUTPUT_DIR"

echo "All content validation tests passed! ✅"
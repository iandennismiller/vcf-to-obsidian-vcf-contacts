#!/bin/bash

# Test VCard format support (3.0 and 4.0)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../test_data/vcf"
OUTPUT_DIR="/tmp/vcf_to_obsidian_test_vcard"

echo "Running VCard format support tests..."

# Clean up previous test runs
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Test 1: VCard 3.0 support
echo "Test 1: Testing VCard 3.0 support..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Test User.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: VCard 3.0 file not processed"
    exit 1
fi

if ! grep -q 'VERSION: "3.0"' "$output_file"; then
    echo "FAIL: VCard 3.0 version not detected"
    cat "$output_file"
    exit 1
fi

echo "✓ Test 1 passed: VCard 3.0 support"

# Test 2: VCard 4.0 support
echo "Test 2: Testing VCard 4.0 support..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/vcard4_test.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Jane Doe.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: VCard 4.0 file not processed"
    exit 1
fi

if ! grep -q 'VERSION: "4.0"' "$output_file"; then
    echo "FAIL: VCard 4.0 version not detected"
    cat "$output_file"
    exit 1
fi

echo "✓ Test 2 passed: VCard 4.0 support"

# Test 3: VCard 4.0 advanced features
echo "Test 3: Testing VCard 4.0 advanced features..."
# Check for proper handling of multiple address types
if ! grep -q 'ADR\[HOME\]' "$output_file"; then
    echo "FAIL: VCard 4.0 home address not parsed"
    exit 1
fi

if ! grep -q 'ADR\[WORK\]' "$output_file"; then
    echo "FAIL: VCard 4.0 work address not parsed"
    exit 1
fi

# Check for multiple phone types
if ! grep -q 'TEL\[HOME\]' "$output_file"; then
    echo "FAIL: VCard 4.0 home phone not parsed"
    exit 1
fi

# Check for complex phone type (WORK,VOICE)
if ! grep -q 'TEL\[WORK,VOICE\]' "$output_file"; then
    echo "FAIL: VCard 4.0 complex phone type not parsed"
    exit 1
fi

echo "✓ Test 3 passed: VCard 4.0 advanced features"

# Test 4: Mixed VCard versions in batch
echo "Test 4: Testing mixed VCard versions..."
rm -rf "$OUTPUT_DIR"/*
mkdir -p "/tmp/test_mixed_vcards"
cp "$TEST_DATA_DIR/content_generation_test.vcf" "/tmp/test_mixed_vcards/"  # v3.0
cp "$TEST_DATA_DIR/vcard4_test.vcf" "/tmp/test_mixed_vcards/"              # v4.0

"$VCF_TO_OBSIDIAN" --folder "/tmp/test_mixed_vcards" --obsidian "$OUTPUT_DIR"

# Both files should be processed
if [[ ! -f "$OUTPUT_DIR/Test User.md" ]] || [[ ! -f "$OUTPUT_DIR/Jane Doe.md" ]]; then
    echo "FAIL: Mixed VCard versions not all processed"
    ls -la "$OUTPUT_DIR"
    exit 1
fi

# Check versions in output
v3_file="$OUTPUT_DIR/Test User.md"
v4_file="$OUTPUT_DIR/Jane Doe.md"

if ! grep -q 'VERSION: "3.0"' "$v3_file"; then
    echo "FAIL: VCard 3.0 version lost in mixed processing"
    exit 1
fi

if ! grep -q 'VERSION: "4.0"' "$v4_file"; then
    echo "FAIL: VCard 4.0 version lost in mixed processing"
    exit 1
fi

echo "✓ Test 4 passed: Mixed VCard versions"

# Test 5: VCard with extended features
echo "Test 5: Testing VCard extended features..."
# Use the full_name_and_uid.vcf which has multiple field types
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/full_name_and_uid.vcf" --obsidian "$OUTPUT_DIR"

extended_file="$OUTPUT_DIR/John Doe.md"
if [[ ! -f "$extended_file" ]]; then
    echo "FAIL: Extended VCard not processed"
    exit 1
fi

# Check for various field types
fields_to_check=("FN:" "N.FN:" "N.GN:" "ORG:" "UID:")
for field in "${fields_to_check[@]}"; do
    if ! grep -q "$field" "$extended_file"; then
        echo "FAIL: Missing field $field in extended VCard"
        cat "$extended_file"
        exit 1
    fi
done

echo "✓ Test 5 passed: VCard extended features"

# Clean up
rm -rf "/tmp/test_mixed_vcards"
rm -rf "$OUTPUT_DIR"

echo "All VCard format support tests passed! ✅"
#!/bin/bash

# Test filename generation priority logic

set -e

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/test_common.sh"

OUTPUT_DIR=$(create_unique_test_dir "filename_priority")

echo "Running filename priority tests..."

# Test 1: FN (Full Name) priority - highest priority
echo "Test 1: Testing FN priority over UID..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/priority_test_fn_over_uid.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/Priority Test 1.md" ]]; then
    echo "FAIL: FN priority test failed - expected 'Priority Test 1.md'"
    exit 1
fi
echo "✓ Test 1 passed: FN priority"

# Test 2: Constructed name priority (Given + Family) over UID
echo "Test 2: Testing constructed name priority over UID..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/priority_test_constructed_over_uid.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/Priority ConstructedTest.md" ]]; then
    echo "FAIL: Constructed name priority test failed - expected 'Priority ConstructedTest.md'"
    exit 1
fi
echo "✓ Test 2 passed: Constructed name priority"

# Test 3: UID fallback when no names available
echo "Test 3: Testing UID fallback..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/uid_only_no_names.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/only-uid-available-12345.md" ]]; then
    echo "FAIL: UID fallback test failed - expected 'only-uid-available-12345.md'"
    exit 1
fi
echo "✓ Test 3 passed: UID fallback"

# Test 4: VCF filename fallback when no names or UID
echo "Test 4: Testing VCF filename fallback..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/minimal_contact.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/minimal_contact.md" ]]; then
    echo "FAIL: VCF filename fallback test failed - expected 'minimal_contact.md'"
    exit 1
fi
echo "✓ Test 4 passed: VCF filename fallback"

# Test 5: Empty UID handling (should use FN)
echo "Test 5: Testing empty UID handling..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/empty_uid.vcf" --obsidian "$OUTPUT_DIR"
if [[ ! -f "$OUTPUT_DIR/Empty UID Test.md" ]]; then
    echo "FAIL: Empty UID test failed - expected 'Empty UID Test.md'"
    exit 1
fi
echo "✓ Test 5 passed: Empty UID handling"

# Test 6: Constructed name from N field only (no FN)
echo "Test 6: Testing constructed name from N field..."
"$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/constructed_name_fallback.vcf" --obsidian "$OUTPUT_DIR"
# This should create "Alice Brown.md" based on N field
expected_files=("Alice Brown.md" "Alice Brown.md")  # Some variations possible
file_found=false
for expected_file in "${expected_files[@]}"; do
    if [[ -f "$OUTPUT_DIR/$expected_file" ]]; then
        file_found=true
        break
    fi
done

if [[ "$file_found" != "true" ]]; then
    echo "FAIL: Constructed name test failed - expected one of: ${expected_files[*]}"
    ls -la "$OUTPUT_DIR"
    exit 1
fi
echo "✓ Test 6 passed: Constructed name from N field"

echo "All filename priority tests passed! ✅"
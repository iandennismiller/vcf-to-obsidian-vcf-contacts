#!/bin/bash

# Test modification time checking functionality

set -e

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh"

OUTPUT_DIR=$(create_unique_test_dir "modification_time")

echo "Running modification time checking tests..."

# Test 1: Test skipping when markdown is newer
echo "Test 1: Validating conversion skip when markdown is newer..."

# Create a test VCF file
VCF_FILE="$OUTPUT_DIR/test.vcf"
cat > "$VCF_FILE" << 'EOF'
BEGIN:VCARD
VERSION:3.0
FN:Modification Test User
N:User;Modification;;;
EMAIL:modtest@example.com
UID:mod-test-123
END:VCARD
EOF

# Convert first time
"$VCF_TO_OBSIDIAN" --file "$VCF_FILE" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Modification Test User.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Second conversion should skip
result=$("$VCF_TO_OBSIDIAN" --file "$VCF_FILE" --obsidian "$OUTPUT_DIR" 2>&1)
if [[ ! "$result" == *"Skipped:"* ]]; then
    echo "FAIL: Second conversion should have been skipped"
    echo "Result: $result"
    exit 1
fi

echo "✓ Test 1 passed: Conversion skipped when VCF not newer"

# Test 2: Test conversion when VCF is newer
echo "Test 2: Validating conversion when VCF is newer..."

# Make VCF file newer
sleep 1
touch "$VCF_FILE"

result=$("$VCF_TO_OBSIDIAN" --file "$VCF_FILE" --obsidian "$OUTPUT_DIR" 2>&1)
if [[ ! "$result" == *"Converted:"* ]]; then
    echo "FAIL: Conversion should have been performed when VCF is newer"
    echo "Result: $result"
    exit 1
fi

echo "✓ Test 2 passed: Conversion performed when VCF is newer"

# Test 3: Test conversion when markdown has no REV timestamp
echo "Test 3: Validating conversion when markdown has no REV timestamp..."

# Create markdown without REV timestamp
cat > "$output_file" << 'EOF'
---
FN: Modification Test User
---
EOF

result=$("$VCF_TO_OBSIDIAN" --file "$VCF_FILE" --obsidian "$OUTPUT_DIR" 2>&1)
if [[ ! "$result" == *"Converted:"* ]]; then
    echo "FAIL: Conversion should have been performed when no REV timestamp"
    echo "Result: $result"
    exit 1
fi

echo "✓ Test 3 passed: Conversion performed when no REV timestamp"

# Test 4: Test conversion when markdown doesn't exist
echo "Test 4: Validating conversion when markdown doesn't exist..."

rm -f "$output_file"

result=$("$VCF_TO_OBSIDIAN" --file "$VCF_FILE" --obsidian "$OUTPUT_DIR" 2>&1)
if [[ ! "$result" == *"Converted:"* ]]; then
    echo "FAIL: Conversion should have been performed when markdown doesn't exist"
    echo "Result: $result"
    exit 1
fi

echo "✓ Test 4 passed: Conversion performed when markdown doesn't exist"

echo "All modification time checking tests passed! ✅"

echo "🧹 Cleaning up temporary test files..."
cleanup() {
    rm -rf "$OUTPUT_DIR" 2>/dev/null || true
}
cleanup
echo "Cleanup complete."
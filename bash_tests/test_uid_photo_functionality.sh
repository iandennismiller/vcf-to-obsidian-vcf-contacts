#!/bin/bash

# Test UID namespace prefix and PHOTO field filtering functionality

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../vcf-to-obsidian.sh"
OUTPUT_DIR="/tmp/vcf_to_obsidian_test_uid_photo"

echo "Running UID namespace and PHOTO field tests..."

# Clean up previous test runs
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Test 1: UID namespace prefix normalization
echo "Test 1: Testing UID namespace prefix normalization..."

# Create test VCF with simple UID
cat > "/tmp/test_uid_prefix.vcf" << 'EOF'
BEGIN:VCARD
VERSION:3.0
UID:simple-test-uid
FN:UID Test
N:Test;UID;;;
EMAIL:test@example.com
END:VCARD
EOF

"$VCF_TO_OBSIDIAN" --file "/tmp/test_uid_prefix.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/UID Test.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check that UID has urn:uuid: prefix
if ! grep -q "UID: urn:uuid:simple-test-uid" "$output_file"; then
    echo "FAIL: UID should have urn:uuid: prefix"
    echo "Found:"
    grep "UID:" "$output_file" || echo "No UID field found"
    exit 1
fi
echo "✓ Test 1 passed: UID namespace prefix normalization"

# Test 2: UID already has namespace prefix (should not double-prefix)
echo "Test 2: Testing UID with existing namespace prefix..."

# Create test VCF with prefixed UID
cat > "/tmp/test_uid_existing_prefix.vcf" << 'EOF'
BEGIN:VCARD
VERSION:3.0
UID:urn:uuid:already-prefixed-uid
FN:UID Existing Prefix Test
N:Test;Prefix;;;
EMAIL:test@example.com
END:VCARD
EOF

rm -f "$OUTPUT_DIR"/*.md
"$VCF_TO_OBSIDIAN" --file "/tmp/test_uid_existing_prefix.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/UID Existing Prefix Test.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check that UID doesn't have double prefix
if ! grep -q "UID: urn:uuid:already-prefixed-uid" "$output_file"; then
    echo "FAIL: UID should not be double-prefixed"
    echo "Found:"
    grep "UID:" "$output_file" || echo "No UID field found"
    exit 1
fi

if grep -q "UID: urn:uuid:urn:uuid:" "$output_file"; then
    echo "FAIL: UID should not be double-prefixed"
    echo "Found:"
    grep "UID:" "$output_file"
    exit 1
fi
echo "✓ Test 2 passed: UID with existing prefix not double-prefixed"

# Test 3: PHOTO field with URL should be included
echo "Test 3: Testing PHOTO field with URL..."

# Create test VCF with photo URL
cat > "/tmp/test_photo_url.vcf" << 'EOF'
BEGIN:VCARD
VERSION:3.0
UID:photo-url-test
FN:Photo URL Test
N:Test;Photo;;;
PHOTO:https://example.com/avatar.jpg
EMAIL:test@example.com
END:VCARD
EOF

rm -f "$OUTPUT_DIR"/*.md
"$VCF_TO_OBSIDIAN" --file "/tmp/test_photo_url.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Photo URL Test.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check that PHOTO URL is included
if ! grep -q "PHOTO: https://example.com/avatar.jpg" "$output_file"; then
    echo "FAIL: PHOTO URL should be included"
    echo "Found:"
    cat "$output_file"
    exit 1
fi
echo "✓ Test 3 passed: PHOTO URL included"

# Test 4: PHOTO field with binary data should be excluded
echo "Test 4: Testing PHOTO field with binary data..."

# Create test VCF with photo binary data
cat > "/tmp/test_photo_binary.vcf" << 'EOF'
BEGIN:VCARD
VERSION:3.0
UID:photo-binary-test
FN:Photo Binary Test
N:Test;Binary;;;
PHOTO;ENCODING=b;TYPE=JPEG:/9j/4AAQSkZJRgABAQEAAQABAAD//2Q=
EMAIL:test@example.com
END:VCARD
EOF

rm -f "$OUTPUT_DIR"/*.md
"$VCF_TO_OBSIDIAN" --file "/tmp/test_photo_binary.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Photo Binary Test.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check that PHOTO binary is NOT included
if grep -q "PHOTO:" "$output_file"; then
    echo "FAIL: PHOTO binary data should be excluded"
    echo "Found:"
    grep "PHOTO:" "$output_file"
    exit 1
fi
echo "✓ Test 4 passed: PHOTO binary data excluded"

# Test 5: PHOTO field with http URL should be included
echo "Test 5: Testing PHOTO field with http URL..."

# Create test VCF with http photo URL
cat > "/tmp/test_photo_http.vcf" << 'EOF'
BEGIN:VCARD
VERSION:3.0
UID:photo-http-test
FN:Photo HTTP Test
N:Test;HTTP;;;
PHOTO:http://example.com/avatar.jpg
EMAIL:test@example.com
END:VCARD
EOF

rm -f "$OUTPUT_DIR"/*.md
"$VCF_TO_OBSIDIAN" --file "/tmp/test_photo_http.vcf" --obsidian "$OUTPUT_DIR"

output_file="$OUTPUT_DIR/Photo HTTP Test.md"
if [[ ! -f "$output_file" ]]; then
    echo "FAIL: Output file not created"
    exit 1
fi

# Check that PHOTO http URL is included
if ! grep -q "PHOTO: http://example.com/avatar.jpg" "$output_file"; then
    echo "FAIL: PHOTO http URL should be included"
    echo "Found:"
    cat "$output_file"
    exit 1
fi
echo "✓ Test 5 passed: PHOTO http URL included"

# Clean up
rm -rf "$OUTPUT_DIR"
rm -f "/tmp/test_uid_prefix.vcf"
rm -f "/tmp/test_uid_existing_prefix.vcf"
rm -f "/tmp/test_photo_url.vcf"
rm -f "/tmp/test_photo_binary.vcf"
rm -f "/tmp/test_photo_http.vcf"

echo "All UID namespace and PHOTO field tests passed! ✅"
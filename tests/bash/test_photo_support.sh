#!/bin/bash

# test_photo_support.sh
# Tests for PHOTO field support in bash implementation

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh"

echo "Running PHOTO field support tests..."

# Test 1: Test PHOTO field with base64 data URI
echo "Test 1: Testing PHOTO field with base64 data URI..."
OUTPUT_DIR=$(create_unique_test_dir "test_photo_base64")
if bash "$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/photo_test.vcf" --obsidian "$OUTPUT_DIR" > /dev/null 2>&1; then
    if [[ -f "$OUTPUT_DIR/Photo Test User.md" ]]; then
        if grep -q "PHOTO: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD" "$OUTPUT_DIR/Photo Test User.md"; then
            echo "✓ Test 1 passed: PHOTO field with base64 data URI"
        else
            echo "✗ Test 1 failed: PHOTO field content not found or incorrect"
            cat "$OUTPUT_DIR/Photo Test User.md" | grep PHOTO || echo "No PHOTO field found"
            exit 1
        fi
    else
        echo "✗ Test 1 failed: Output file not created"
        exit 1
    fi
else
    echo "✗ Test 1 failed: Conversion failed"
    exit 1
fi

# Test 2: Test PHOTO field with URL
echo "Test 2: Testing PHOTO field with URL..."
OUTPUT_DIR=$(create_unique_test_dir "test_photo_url")
if bash "$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/photo_url_test.vcf" --obsidian "$OUTPUT_DIR" > /dev/null 2>&1; then
    if [[ -f "$OUTPUT_DIR/Photo URL Test User.md" ]]; then
        if grep -q "PHOTO: https://example.com/photo.jpg" "$OUTPUT_DIR/Photo URL Test User.md"; then
            echo "✓ Test 2 passed: PHOTO field with URL"
        else
            echo "✗ Test 2 failed: PHOTO URL content not found or incorrect"
            cat "$OUTPUT_DIR/Photo URL Test User.md" | grep PHOTO || echo "No PHOTO field found"
            exit 1
        fi
    else
        echo "✗ Test 2 failed: Output file not created"
        exit 1
    fi
else
    echo "✗ Test 2 failed: Conversion failed"
    exit 1
fi

# Test 3: Test Python test compatibility (complete data URI)
echo "Test 3: Testing Python test compatibility..."
OUTPUT_DIR=$(create_unique_test_dir "test_photo_python_compat")
if bash "$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/photo_python_test.vcf" --obsidian "$OUTPUT_DIR" > /dev/null 2>&1; then
    if [[ -f "$OUTPUT_DIR/All Fields Test.md" ]]; then
        if grep -q "PHOTO: data:image/jpeg;base64,dGVzdA==" "$OUTPUT_DIR/All Fields Test.md"; then
            echo "✓ Test 3 passed: Python test compatibility"
        else
            echo "✗ Test 3 failed: Python compatibility test failed"
            cat "$OUTPUT_DIR/All Fields Test.md" | grep PHOTO || echo "No PHOTO field found"
            exit 1
        fi
    else
        echo "✗ Test 3 failed: Output file not created"
        exit 1
    fi
else
    echo "✗ Test 3 failed: Conversion failed"
    exit 1
fi

# Test 4: Test VCF without PHOTO field (should not affect other fields)
echo "Test 4: Testing VCF without PHOTO field..."
OUTPUT_DIR=$(create_unique_test_dir "test_no_photo")
if bash "$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/content_generation_test.vcf" --obsidian "$OUTPUT_DIR" > /dev/null 2>&1; then
    if [[ -f "$OUTPUT_DIR/Test User.md" ]]; then
        # Should have other fields but no PHOTO field
        if grep -q "FN: Test User" "$OUTPUT_DIR/Test User.md" && ! grep -q "PHOTO:" "$OUTPUT_DIR/Test User.md"; then
            echo "✓ Test 4 passed: VCF without PHOTO field works correctly"
        else
            echo "✗ Test 4 failed: VCF without PHOTO field test failed"
            cat "$OUTPUT_DIR/Test User.md"
            exit 1
        fi
    else
        echo "✗ Test 4 failed: Output file not created"
        exit 1
    fi
else
    echo "✗ Test 4 failed: Conversion failed"
    exit 1
fi

# Test 5: Test position of PHOTO field in output (should be after FN)
echo "Test 5: Testing PHOTO field position in output..."
OUTPUT_DIR=$(create_unique_test_dir "test_photo_position")
if bash "$VCF_TO_OBSIDIAN" --file "$TEST_DATA_DIR/photo_test.vcf" --obsidian "$OUTPUT_DIR" > /dev/null 2>&1; then
    if [[ -f "$OUTPUT_DIR/Photo Test User.md" ]]; then
        # Check that PHOTO comes after FN in the output
        fn_line=$(grep -n "FN:" "$OUTPUT_DIR/Photo Test User.md" | head -1 | cut -d: -f1)
        photo_line=$(grep -n "PHOTO:" "$OUTPUT_DIR/Photo Test User.md" | head -1 | cut -d: -f1)
        
        if [[ -n "$fn_line" && -n "$photo_line" && "$photo_line" -gt "$fn_line" ]]; then
            echo "✓ Test 5 passed: PHOTO field appears after FN field"
        else
            echo "✗ Test 5 failed: PHOTO field position incorrect (FN:$fn_line, PHOTO:$photo_line)"
            cat "$OUTPUT_DIR/Photo Test User.md"
            exit 1
        fi
    else
        echo "✗ Test 5 failed: Output file not created"
        exit 1
    fi
else
    echo "✗ Test 5 failed: Conversion failed"
    exit 1
fi

echo "All PHOTO field support tests passed! ✅"
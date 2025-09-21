#!/bin/bash

# test_shell_compatibility.sh
# Tests for shell compatibility and error handling

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/../../scripts/vcf-to-obsidian.sh"

echo "Running shell compatibility tests..."

# Test 1: Verify script works with bash
echo "Test 1: Testing bash compatibility..."
if bash "$MAIN_SCRIPT" --help > /dev/null 2>&1; then
    echo "✓ Test 1 passed: Script works with bash"
else
    echo "✗ Test 1 failed: Script should work with bash"
    exit 1
fi

# Test 2: Verify script provides helpful error with zsh  
echo "Test 2: Testing zsh error handling..."
if which zsh > /dev/null 2>&1; then
    if zsh "$MAIN_SCRIPT" --help > /dev/null 2>&1; then
        echo "✗ Test 2 failed: Script should fail with zsh"
        exit 1
    else
        # Check if error message mentions zsh specifically
        ERROR_OUTPUT=$(zsh "$MAIN_SCRIPT" --help 2>&1)
        if echo "$ERROR_OUTPUT" | grep -q "zsh"; then
            echo "✓ Test 2 passed: Script provides zsh-specific error message"
        else
            echo "✗ Test 2 failed: Error message should mention zsh"
            echo "Actual error: $ERROR_OUTPUT"
            exit 1
        fi
    fi
else
    echo "⚠ Test 2 skipped: zsh not available"
fi

# Test 3: Verify typeset -A is used instead of declare -A
echo "Test 3: Testing portable associative array usage..."
if grep -q "declare -A" "$MAIN_SCRIPT"; then
    echo "✗ Test 3 failed: Script still uses 'declare -A' which is not portable"
    exit 1
elif grep -q "typeset -A" "$MAIN_SCRIPT"; then
    echo "✓ Test 3 passed: Script uses 'typeset -A' for portability"
else
    echo "✗ Test 3 failed: Script should use 'typeset -A' for associative arrays"
    exit 1
fi

# Test 4: Verify normal shebang execution works
echo "Test 4: Testing normal shebang execution..."
if "$MAIN_SCRIPT" --help > /dev/null 2>&1; then
    echo "✓ Test 4 passed: Normal execution via shebang works"
else
    echo "✗ Test 4 failed: Normal shebang execution should work"
    exit 1
fi

echo "All shell compatibility tests passed! ✅"
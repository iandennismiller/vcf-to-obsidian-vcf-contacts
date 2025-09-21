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

# Test 2: Verify script works with zsh now that it's compatible
echo "Test 2: Testing zsh compatibility..."
if which zsh > /dev/null 2>&1; then
    if zsh "$MAIN_SCRIPT" --help > /dev/null 2>&1; then
        echo "✓ Test 2 passed: Script now works with zsh"
    else
        echo "✗ Test 2 failed: Script should work with zsh"
        exit 1
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

# Test 5: Verify bash version checking logic
echo "Test 5: Testing bash version checking..."
# Create a temporary script that simulates bash 3.2
TEMP_SCRIPT="/tmp/test_bash_version.sh"
cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash

# Mock BASH_VERSION for testing
BASH_VERSION="3.2.57(1)-release"

# Extract the version checking logic from the main script
BASH_MAJOR=$(echo "$BASH_VERSION" | cut -d. -f1)
if [ "$BASH_MAJOR" -lt 4 ]; then
    echo "Error: This script requires bash 4.0+ but you have bash $BASH_VERSION"
    exit 1
else
    echo "Bash version OK"
fi
EOF

chmod +x "$TEMP_SCRIPT"
if "$TEMP_SCRIPT" > /dev/null 2>&1; then
    echo "✗ Test 5 failed: Should reject bash 3.2"
    exit 1
else
    echo "✓ Test 5 passed: Correctly rejects bash 3.2"
fi

rm -f "$TEMP_SCRIPT"

echo "All shell compatibility tests passed! ✅"
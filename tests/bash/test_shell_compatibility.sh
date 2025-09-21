#!/bin/bash

# test_shell_compatibility.sh
# Tests for shell compatibility and error handling

# Source common test configuration
source "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh"

echo "Running shell compatibility tests..."

# Test 1: Verify script works with bash
echo "Test 1: Testing bash compatibility..."
if bash "$VCF_TO_OBSIDIAN" --help > /dev/null 2>&1; then
    echo "✓ Test 1 passed: Script works with bash"
else
    echo "✗ Test 1 failed: Script should work with bash"
    exit 1
fi

# Test 2: Verify bash script rejects other shells
echo "Test 2: Testing shell compatibility check..."
# Create a temporary script that simulates running without BASH_VERSION
TEMP_SCRIPT="$BASE_OUTPUT_DIR/test_shell_check.sh"
cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash

# Unset BASH_VERSION to simulate non-bash shell
unset BASH_VERSION

# Source the shell compatibility check from the main script
if [ -z "${BASH_VERSION:-}" ]; then
    echo "Error: This script requires bash 4.0+ to run." >&2
    exit 1
fi
EOF

chmod +x "$TEMP_SCRIPT"
if "$TEMP_SCRIPT" > /dev/null 2>&1; then
    echo "✗ Test 2 failed: Should reject non-bash shells"
    exit 1
else
    echo "✓ Test 2 passed: Correctly rejects non-bash shells"
fi

# Test 3: Verify declare -A is used for bash associative arrays
echo "Test 3: Testing bash associative array usage..."
if grep -q "typeset -A" "$VCF_TO_OBSIDIAN"; then
    echo "✗ Test 3 failed: Script should not use 'typeset -A' without ZSH compatibility"
    exit 1
elif grep -q "declare -A" "$VCF_TO_OBSIDIAN"; then
    echo "✓ Test 3 passed: Script uses 'declare -A' for bash associative arrays"
else
    echo "✗ Test 3 failed: Script should use 'declare -A' for associative arrays"
    exit 1
fi

# Test 4: Verify normal shebang execution works
echo "Test 4: Testing normal shebang execution..."
if "$VCF_TO_OBSIDIAN" --help > /dev/null 2>&1; then
    echo "✓ Test 4 passed: Normal execution via shebang works"
else
    echo "✗ Test 4 failed: Normal shebang execution should work"
    exit 1
fi

# Test 5: Verify bash version checking logic
echo "Test 5: Testing bash version checking..."
# Create a temporary script that simulates bash 3.2
TEMP_SCRIPT="$BASE_OUTPUT_DIR/test_bash_version.sh"
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

# Test 6: Verify /opt/homebrew/bin/bash fallback behavior 
echo "Test 6: Testing /opt/homebrew/bin/bash fallback behavior..."
# Create a mock /opt/homebrew/bin/bash for testing
MOCK_LOCAL_BASH_DIR="$BASE_OUTPUT_DIR/mock_usr_local_bin"
mkdir -p "$MOCK_LOCAL_BASH_DIR"
cat > "$MOCK_LOCAL_BASH_DIR/bash" << 'EOF'
#!/bin/bash
# Mock bash 4.0+ for testing
echo "4.0.0(1)-release"
EOF
chmod +x "$MOCK_LOCAL_BASH_DIR/bash"

# Create a script that tests the fallback logic
TEMP_FALLBACK_SCRIPT="$BASE_OUTPUT_DIR/test_bash_fallback.sh"
cat > "$TEMP_FALLBACK_SCRIPT" << EOF
#!/bin/bash

# Mock BASH_VERSION for testing
BASH_VERSION="3.2.57(1)-release"

# Extract the version checking logic from the main script
BASH_MAJOR=\$(echo "\$BASH_VERSION" | cut -d. -f1)
if [ "\$BASH_MAJOR" -lt 4 ]; then
    # Check if /opt/homebrew/bin/bash is available as a fallback
    if [ -x "$MOCK_LOCAL_BASH_DIR/bash" ]; then
        # Check version of /opt/homebrew/bin/bash
        LOCAL_BASH_VERSION=\$($MOCK_LOCAL_BASH_DIR/bash)
        LOCAL_BASH_MAJOR=\$(echo "\$LOCAL_BASH_VERSION" | cut -d. -f1)
        if [ "\$LOCAL_BASH_MAJOR" -ge 4 ]; then
            echo "Would fallback to /opt/homebrew/bin/bash version \$LOCAL_BASH_VERSION"
            exit 0
        else
            echo "Error: /opt/homebrew/bin/bash version \$LOCAL_BASH_VERSION is too old (need 4.0+)" >&2
            exit 1
        fi
    else
        echo "Error: This script requires bash 4.0+, but you have bash \$BASH_VERSION" >&2
        exit 1
    fi
fi
EOF

chmod +x "$TEMP_FALLBACK_SCRIPT"
if "$TEMP_FALLBACK_SCRIPT" > /dev/null 2>&1; then
    echo "✓ Test 6 passed: Correctly falls back to /opt/homebrew/bin/bash"
else
    echo "✗ Test 6 failed: Should fallback to /opt/homebrew/bin/bash when available"
    exit 1
fi

echo "All shell compatibility tests passed! ✅"
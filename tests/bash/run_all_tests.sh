#!/bin/bash

# Main test runner for bash implementation tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧪 Running all bash implementation tests..."
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test files to run in order
TEST_FILES=(
    "test_file_processing.sh"
    "test_filename_priority.sh"
    "test_special_characters.sh"
    "test_content_validation.sh"
    "test_vcard_support.sh"
    "test_cli_options.sh"
)

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a single test file
run_test() {
    local test_file="$1"
    local test_path="$SCRIPT_DIR/$test_file"
    
    echo ""
    echo -e "${YELLOW}Running $test_file...${NC}"
    echo "----------------------------------------"
    
    if [[ ! -f "$test_path" ]]; then
        echo -e "${RED}❌ Test file not found: $test_path${NC}"
        return 1
    fi
    
    if [[ ! -x "$test_path" ]]; then
        chmod +x "$test_path"
    fi
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if "$test_path"; then
        echo -e "${GREEN}✅ $test_file PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ $test_file FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Function to print summary
print_summary() {
    echo ""
    echo "========================================"
    echo "🎯 Test Summary"
    echo "========================================"
    echo "Total test suites: $TOTAL_TESTS"
    echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
    
    if [[ $FAILED_TESTS -eq 0 ]]; then
        echo ""
        echo -e "${GREEN}🎉 All tests passed! ✅${NC}"
        echo ""
        echo "The bash implementation is working correctly!"
        return 0
    else
        echo ""
        echo -e "${RED}💥 Some tests failed! ❌${NC}"
        echo ""
        echo "Please check the test output above for details."
        return 1
    fi
}

# Cleanup function
cleanup() {
    echo ""
    echo "🧹 Cleaning up temporary test files..."
    rm -rf /tmp/vcf_to_obsidian_test_*
    rm -rf /tmp/test_vcf_subset
    rm -rf /tmp/test_mixed_vcards
    rm -rf /tmp/empty_vcf_dir
    rm -rf /tmp/test_obsidian*
    echo "Cleanup complete."
}

# Set up trap for cleanup
trap cleanup EXIT

# Main execution
echo "Starting bash implementation test suite..."
echo "Script directory: $SCRIPT_DIR"
<<<<<<< HEAD:bash_tests/run_all_tests.sh
echo "Testing script: $SCRIPT_DIR/../scripts/vcf-to-obsidian.sh"

# Verify the main script exists
if [[ ! -f "$SCRIPT_DIR/../scripts/vcf-to-obsidian.sh" ]]; then
    echo -e "${RED}❌ Main script not found: $SCRIPT_DIR/../scripts/vcf-to-obsidian.sh${NC}"
    exit 1
fi

if [[ ! -x "$SCRIPT_DIR/../scripts/vcf-to-obsidian.sh" ]]; then
    echo "Making main script executable..."
    chmod +x "$SCRIPT_DIR/../scripts/vcf-to-obsidian.sh"
=======
echo "Testing script: $SCRIPT_DIR/../../vcf-to-obsidian.sh"

# Verify the main script exists
if [[ ! -f "$SCRIPT_DIR/../../vcf-to-obsidian.sh" ]]; then
    echo -e "${RED}❌ Main script not found: $SCRIPT_DIR/../../vcf-to-obsidian.sh${NC}"
    exit 1
fi

if [[ ! -x "$SCRIPT_DIR/../../vcf-to-obsidian.sh" ]]; then
    echo "Making main script executable..."
    chmod +x "$SCRIPT_DIR/../../vcf-to-obsidian.sh"
>>>>>>> main:tests/bash/run_all_tests.sh
fi

# Verify test data exists
if [[ ! -d "$SCRIPT_DIR/../data/vcf" ]]; then
    echo -e "${RED}❌ Test data directory not found: $SCRIPT_DIR/../data/vcf${NC}"
    exit 1
fi

echo "Test data directory: $SCRIPT_DIR/../data/vcf"
vcf_count=$(find "$SCRIPT_DIR/../data/vcf" -name "*.vcf" | wc -l)
echo "Found $vcf_count VCF test files"

# Run all tests
for test_file in "${TEST_FILES[@]}"; do
    run_test "$test_file" || true  # Continue even if a test fails
done

# Print final summary and exit with appropriate code
print_summary
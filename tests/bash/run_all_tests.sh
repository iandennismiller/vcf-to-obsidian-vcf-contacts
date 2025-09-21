#!/bin/bash

# Main test runner for bash implementation tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/../../scripts/vcf-to-obsidian.sh"

# Common test configuration (merged from test_common.sh)
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../../scripts/vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../data"
BASE_OUTPUT_DIR="/tmp/vcf_to_obsidian_test"

# Create a unique test output directory
# Usage: OUTPUT_DIR=$(create_unique_test_dir "test_name")
create_unique_test_dir() {
    local test_name="$1"
    local timestamp=$(date +%s)
    local unique_dir="$BASE_OUTPUT_DIR/${test_name}_${timestamp}_$$"
    
    mkdir -p "$unique_dir"
    echo "$unique_dir"
}

# Ensure base test directory exists
mkdir -p "$BASE_OUTPUT_DIR"

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
    "test_shell_compatibility.sh"
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
    rm -rf "$BASE_OUTPUT_DIR"
    echo "Cleanup complete."
}

# Set up trap for cleanup
trap cleanup EXIT

# Only run the main execution if this script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then

echo "🧪 Running all bash implementation tests..."
echo "========================================"

# Main execution
echo "Starting bash implementation test suite..."
echo "Script directory: $SCRIPT_DIR"
echo "Testing script: $MAIN_SCRIPT"

# Verify the main script exists
if [[ ! -f "$MAIN_SCRIPT" ]]; then
    echo -e "${RED}❌ Main script not found: $MAIN_SCRIPT${NC}"
    exit 1
fi

if [[ ! -x "$MAIN_SCRIPT" ]]; then
    echo "Making main script executable..."
    chmod +x "$MAIN_SCRIPT"
fi

# Verify test data exists
if [[ ! -d "$TEST_DATA_DIR" ]]; then
    echo -e "${RED}❌ Test data directory not found: $TEST_DATA_DIR${NC}"
    exit 1
fi

echo "Test data directory: $TEST_DATA_DIR"
vcf_count=$(find "$TEST_DATA_DIR" -name "*.vcf" | wc -l)
echo "Found $vcf_count VCF test files"

# Run all tests
for test_file in "${TEST_FILES[@]}"; do
    run_test "$test_file" || true  # Continue even if a test fails
done

# Print final summary and exit with appropriate code
print_summary

fi  # End of direct execution check
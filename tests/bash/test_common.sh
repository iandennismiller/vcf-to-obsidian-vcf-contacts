#!/bin/bash

# Common test configuration for bash tests
# This file should be sourced by all test scripts

# Common paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VCF_TO_OBSIDIAN="$SCRIPT_DIR/../../scripts/vcf-to-obsidian.sh"
TEST_DATA_DIR="$SCRIPT_DIR/../data/vcf"
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
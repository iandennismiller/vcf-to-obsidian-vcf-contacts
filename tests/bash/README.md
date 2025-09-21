# Bash Tests

This directory contains comprehensive tests for the bash implementation (`vcf-to-obsidian.sh`).

## Test Structure

The tests are organized by functionality into separate test files:

- **`test_file_processing.sh`** - Tests single file, folder, and mixed source processing
- **`test_filename_priority.sh`** - Tests filename generation priority logic (FN > constructed name > UID > filename)
- **`test_special_characters.sh`** - Tests special character handling in filenames and UIDs
- **`test_content_validation.sh`** - Tests output content format and structure validation
- **`test_vcard_support.sh`** - Tests VCard 3.0 and 4.0 format support
- **`test_cli_options.sh`** - Tests command line interface options and error handling
- **`test_shell_compatibility.sh`** - Tests bash version requirements and shell detection

## Running Tests

### Run All Tests

To run the complete test suite:

```bash
./bash_tests/run_all_tests.sh
```

This will execute all test files in sequence and provide a summary report.

### Run Individual Test Files

To run a specific test file:

```bash
./bash_tests/test_file_processing.sh
./bash_tests/test_filename_priority.sh
./bash_tests/test_special_characters.sh
./bash_tests/test_content_validation.sh
./bash_tests/test_vcard_support.sh
./bash_tests/test_cli_options.sh
./bash_tests/test_shell_compatibility.sh
```

## Test Output

Each test file provides:
- ✅ Individual test case results
- 🎯 Summary of passed/failed tests
- 🧹 Automatic cleanup of temporary files

The main test runner (`run_all_tests.sh`) provides:
- 📊 Color-coded output
- 📈 Overall test statistics
- 🧪 Comprehensive test coverage report

## Test Data

Tests use the VCF files in `../data/vcf/` which contain various test scenarios:
- Different VCard versions (3.0 and 4.0)
- Various field combinations
- Special characters and edge cases
- Priority testing scenarios

## Requirements

- Bash 4.0+ (for array support and advanced features)
- Standard Unix tools (`sed`, `grep`, `find`, etc.)
- Write access to `/tmp` directory for test outputs

## Adding New Tests

To add a new test file:

1. Create a new test file following the naming pattern `test_<functionality>.sh`
2. Make it executable: `chmod +x test_<functionality>.sh`
3. Add it to the `TEST_FILES` array in `run_all_tests.sh`
4. Follow the existing test structure and conventions

## Test Conventions

- Use descriptive test names and clear output messages
- Clean up temporary files in each test
- Use unique temporary directory names to avoid conflicts
- Exit with code 0 on success, non-zero on failure
- Provide clear failure messages with expected vs actual results
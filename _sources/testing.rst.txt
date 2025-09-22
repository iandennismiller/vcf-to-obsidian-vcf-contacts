Testing
=======

The project includes a comprehensive test suite to ensure reliability and correctness, organized using pytest.

Running Tests
-------------

Run the test suite using pytest:

::

   pytest


Or run with verbose output:

::

   pytest -v


Run tests for a specific functionality:

::

   pytest tests/test_vcf_reading.py      # VCF parsing tests
   pytest tests/test_markdown_writing.py # Markdown generation tests
   pytest tests/test_command_line.py     # CLI functionality tests
   pytest tests/test_filename_generation.py # Filename logic tests
   pytest tests/test_integration.py      # End-to-end integration tests


Test Organization
-----------------

Tests are organized into separate files by functionality:

- **``tests/test_vcf_reading.py``** - VCF file parsing and data extraction
- **``tests/test_markdown_writing.py``** - Markdown content generation
- **``tests/test_command_line.py``** - Command line interface functionality
- **``tests/test_filename_generation.py``** - Filename generation logic and special character handling
- **``tests/test_integration.py``** - End-to-end integration tests

Test Coverage
-------------

The test suite covers:

- VCF parsing with various field combinations
- Filename generation priority logic (FN > constructed name > UID > filename)
- Special character handling in filenames and UIDs
- Markdown content generation and frontmatter
- Template system functionality
- Command line interface behavior
- Edge cases (empty fields, missing data)
- Error handling scenarios

Bash Tests
----------

The bash implementation has its own comprehensive test suite located in ``tests/bash/``.

Test Structure
^^^^^^^^^^^^^^

The bash tests are organized by functionality into separate test files:

- **``test_file_processing.sh``** - Tests single file, folder, and mixed source processing
- **``test_filename_priority.sh``** - Tests filename generation priority logic (FN > constructed name > UID > filename)
- **``test_special_characters.sh``** - Tests special character handling in filenames and UIDs
- **``test_content_validation.sh``** - Tests output content format and structure validation
- **``test_vcard_support.sh``** - Tests VCard 3.0 and 4.0 format support
- **``test_cli_options.sh``** - Tests command line interface options and error handling
- **``test_shell_compatibility.sh``** - Tests bash version requirements and shell detection

Running Bash Tests
^^^^^^^^^^^^^^^^^^

Run All Tests
"""""""""""""

To run the complete bash test suite:

::

   ./tests/bash/run_all_tests.sh


This will execute all test files in sequence and provide a summary report.

Run Individual Test Files
"""""""""""""""""""""""""

To run a specific test file:

::

   ./tests/bash/test_file_processing.sh
   ./tests/bash/test_filename_priority.sh
   ./tests/bash/test_special_characters.sh
   ./tests/bash/test_content_validation.sh
   ./tests/bash/test_vcard_support.sh
   ./tests/bash/test_cli_options.sh
   ./tests/bash/test_shell_compatibility.sh


Using Make Commands
"""""""""""""""""""

You can also use the provided Makefile commands:

::

   make test-bash          # Run bash implementation tests
   make test-all           # Run all tests (bash and python if available)


Test Output
^^^^^^^^^^^

Each test file provides:
- ✅ Individual test case results
- 🎯 Summary of passed/failed tests
- 🧹 Automatic cleanup of temporary files

The main test runner (``run_all_tests.sh``) provides:
- 📊 Color-coded output
- 📈 Overall test statistics
- 🧪 Comprehensive test coverage report

Test Data
^^^^^^^^^

Tests use the VCF files in ``tests/data/`` which contain various test scenarios:
- Different VCard versions (3.0 and 4.0)
- Various field combinations
- Special characters and edge cases
- Priority testing scenarios

VCF Test Files
""""""""""""""

Each test file represents a specific test scenario and is designed to test specific filename generation logic and VCF parsing scenarios:

- ``constructed_name_fallback.vcf`` - Contact with N (structured name) but no FN or UID
- ``content_generation_test.vcf`` - Complete contact with all fields for markdown generation testing
- ``empty_uid.vcf`` - Contact with empty UID field
- ``fn_preferred.vcf`` - Contact with both FN and UID to test FN preference
- ``full_name_and_uid.vcf`` - Contact with both full name and UID
- ``full_name_only.vcf`` - Contact with FN but no UID
- ``minimal_contact.vcf`` - Minimal contact with only organization
- ``priority_test_constructed_over_uid.vcf`` - Test constructed name priority over UID
- ``priority_test_fn_over_uid.vcf`` - Test FN priority over UID
- ``special_characters_filename.vcf`` - Contact with special characters in FN
- ``special_characters_uid.vcf`` - Contact with special characters in UID
- ``uid_fallback.vcf`` - Contact with UID and structured name
- ``uid_only.vcf`` - Contact with UID but no FN
- ``uid_only_no_names.vcf`` - Contact with only UID, no name information
- ``uid_special_chars_fallback.vcf`` - UID with special characters when used as fallback

Requirements
^^^^^^^^^^^^

- Bash 4.0+ (for array support and advanced features)
- Standard Unix tools (``sed``, ``grep``, ``find``, etc.)
- Write access to ``/tmp`` directory for test outputs

Adding New Tests
^^^^^^^^^^^^^^^^

To add a new test file:

1. Create a new test file following the naming pattern ``test_<functionality>.sh``
2. Make it executable: ``chmod +x test_<functionality>.sh``
3. Add it to the ``TEST_FILES`` array in ``run_all_tests.sh``
4. Follow the existing test structure and conventions

Test Conventions
^^^^^^^^^^^^^^^^

- Use descriptive test names and clear output messages
- Clean up temporary files in each test
- Use unique temporary directory names to avoid conflicts
- Exit with code 0 on success, non-zero on failure
- Provide clear failure messages with expected vs actual results
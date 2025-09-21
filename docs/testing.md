# Testing

The project includes a comprehensive test suite to ensure reliability and correctness, organized using pytest.

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

Or run with verbose output:

```bash
pytest -v
```

Run tests for a specific functionality:

```bash
pytest tests/test_vcf_reading.py      # VCF parsing tests
pytest tests/test_markdown_writing.py # Markdown generation tests
pytest tests/test_command_line.py     # CLI functionality tests
pytest tests/test_filename_generation.py # Filename logic tests
pytest tests/test_integration.py      # End-to-end integration tests
```

## Test Organization

Tests are organized into separate files by functionality:

- **`tests/test_vcf_reading.py`** - VCF file parsing and data extraction
- **`tests/test_markdown_writing.py`** - Markdown content generation
- **`tests/test_command_line.py`** - Command line interface functionality
- **`tests/test_filename_generation.py`** - Filename generation logic and special character handling
- **`tests/test_integration.py`** - End-to-end integration tests

## Test Coverage

The test suite covers:

- VCF parsing with various field combinations
- Filename generation priority logic (FN > constructed name > UID > filename)
- Special character handling in filenames and UIDs
- Markdown content generation and frontmatter
- Template system functionality
- Command line interface behavior
- Edge cases (empty fields, missing data)
- Error handling scenarios

## Bash Tests

The bash implementation has its own comprehensive test suite located in `tests/bash/`. See the [bash tests README](../tests/bash/README.md) for more details on running and organizing bash-specific tests.
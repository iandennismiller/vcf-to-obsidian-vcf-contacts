Development and Maintenance
===========================

This project includes a comprehensive Makefile for installation, testing, linting, and other maintenance tasks.

Quick Setup
-----------

::

   # Set up development environment
   make setup-dev

   # Run all tests
   make test-all

   # Run linting
   make lint

   # Show all available targets
   make help


Available Make Targets
----------------------

**Installation:**
- ``make install`` - Install package dependencies
- ``make install-dev`` - Install development dependencies (includes pytest)
- ``make install-lint`` - Install linting tools (flake8, black, isort, mypy)
- ``make setup-dev`` - Set up complete development environment

**Testing:**
- ``make test`` - Run all available tests
- ``make test-bash`` - Run bash implementation tests
- ``make test-python`` - Run Python tests with pytest
- ``make test-all`` - Run all tests (bash and python if available)

**Linting and Code Quality:**
- ``make lint`` - Run all linting tools
- ``make lint-python`` - Run Python linting (flake8, black, isort, mypy)
- ``make lint-bash`` - Run bash script linting (shellcheck)
- ``make format`` - Format code using black and isort

**Build and Package:**
- ``make build`` - Build package (syntax check, make executable)
- ``make package`` - Create distributable package
- ``make check-deps`` - Check if required dependencies are available

**Maintenance:**
- ``make clean`` - Clean temporary files and build artifacts
- ``make docs`` - Show usage documentation
- ``make demo`` - Run a quick demo with test data

**Development Workflows:**
- ``make ci`` - Run full CI pipeline (install, test, lint)
- ``make dev-check`` - Quick development check (test + lint)
- ``make quick-start`` - Show quick start guide

Dependencies
------------

The Makefile handles dependency installation automatically. For manual installation:

**Required for Python implementation:**
- Python 3.12+
- vobject 0.9.0+
- click 8.0.0+

**Development dependencies:**
- pytest 7.0.0+

**Linting tools (optional):**
- flake8, black, isort, mypy for Python
- shellcheck for bash scripts

Error Handling
--------------

The script includes robust error handling for:

- Non-existent source directories
- Empty directories with no VCF files
- Malformed VCF files
- File system permissions issues
- Invalid characters in filenames
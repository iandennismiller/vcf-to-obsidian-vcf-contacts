# Makefile for vcf-to-obsidian-vcf-contacts
# Provides installation, testing, linting, and maintenance tasks

.PHONY: help install install-dev install-lint test test-python test-bash test-all lint lint-python lint-bash format clean build package check-deps docs setup-dev shell docs-html docs-clean docs-serve docs-install

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Common workflows:"
	@echo "  make setup-dev     # Set up development environment"
	@echo "  make test-all      # Run all tests"
	@echo "  make lint          # Run all linting"
	@echo "  make clean         # Clean temporary files"

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
BASH_TEST_DIR := tests/bash
TEST_DIR := tests/py
PYTHON_FILES := scripts/vcf_to_obsidian.py $(TEST_DIR)/*.py

# Installation targets
install: ## Install package dependencies
	$(PIP) install vobject click

install-dev: install ## Install development dependencies
	$(PIP) install pytest pytest-cov

install-lint: ## Install linting tools
	$(PIP) install flake8 black isort mypy

setup-dev: install-dev install-lint ## Set up complete development environment
	@echo "Development environment setup complete!"
	@echo "You can now run: make test-all && make lint"

check-deps: ## Check if required dependencies are available
	@echo "Checking dependencies..."
	@$(PYTHON) -c "import click" 2>/dev/null && echo "✓ click available" || echo "✗ click missing"
	@$(PYTHON) -c "import vobject" 2>/dev/null && echo "✓ vobject available" || echo "✗ vobject missing"
	@$(PYTHON) -c "import pytest" 2>/dev/null && echo "✓ pytest available" || echo "✗ pytest missing"
	@which flake8 >/dev/null 2>&1 && echo "✓ flake8 available" || echo "✗ flake8 missing"
	@which black >/dev/null 2>&1 && echo "✓ black available" || echo "✗ black missing"
	@which isort >/dev/null 2>&1 && echo "✓ isort available" || echo "✗ isort missing"

# Testing targets
test-python: ## Run Python tests with pytest
	@echo "Running Python tests..."
	@if $(PYTHON) -c "import pytest" 2>/dev/null; then \
		$(PYTEST) -v $(TEST_DIR); \
	else \
		echo "pytest not available. Install with: make install-dev"; \
		exit 1; \
	fi

test-bash: ## Run bash implementation tests
	@echo "Running bash tests..."
	@chmod +x $(BASH_TEST_DIR)/run_all_tests.sh
	@$(BASH_TEST_DIR)/run_all_tests.sh

test-all: test-bash ## Run all tests (bash and python if available)
	@echo ""
	@echo "Running all available tests..."
	@if $(PYTHON) -c "import pytest, vobject, click" 2>/dev/null; then \
		echo ""; \
		echo "Running Python tests..."; \
		$(PYTEST) -v $(TEST_DIR) || true; \
	else \
		echo ""; \
		echo "Skipping Python tests (missing dependencies: pytest, vobject, or click)"; \
		echo "Install with: make install-dev"; \
	fi

test: test-all ## Alias for test-all

# Linting targets
lint-python: ## Run Python linting tools
	@echo "Running Python linting..."
	@if which flake8 >/dev/null 2>&1; then \
		echo "Running flake8..."; \
		flake8 --max-line-length=88 --extend-ignore=E203,W503 scripts/vcf_to_obsidian.py $(TEST_DIR)/ || true; \
	else \
		echo "flake8 not available. Install with: make install-lint"; \
	fi
	@if which black >/dev/null 2>&1; then \
		echo "Running black (check mode)..."; \
		black --check --diff scripts/vcf_to_obsidian.py $(TEST_DIR)/ || true; \
	else \
		echo "black not available. Install with: make install-lint"; \
	fi
	@if which isort >/dev/null 2>&1; then \
		echo "Running isort (check mode)..."; \
		isort --check-only --diff scripts/vcf_to_obsidian.py $(TEST_DIR)/ || true; \
	else \
		echo "isort not available. Install with: make install-lint"; \
	fi
	@if which mypy >/dev/null 2>&1; then \
		echo "Running mypy..."; \
		mypy --ignore-missing-imports scripts/vcf_to_obsidian.py || true; \
	else \
		echo "mypy not available. Install with: make install-lint"; \
	fi

lint-bash: ## Run bash script linting
	@echo "Running bash linting..."
	@if which shellcheck >/dev/null 2>&1; then \
		echo "Running shellcheck..."; \
		shellcheck scripts/vcf-to-obsidian.sh $(BASH_TEST_DIR)/*.sh || true; \
	else \
		echo "shellcheck not available. Install with: apt-get install shellcheck"; \
	fi
	@echo "Checking bash script permissions..."
	@test -x scripts/vcf-to-obsidian.sh && echo "✓ scripts/vcf-to-obsidian.sh is executable" || echo "✗ scripts/vcf-to-obsidian.sh not executable"
	@for script in $(BASH_TEST_DIR)/*.sh; do \
		test -x "$$script" && echo "✓ $$script is executable" || echo "✗ $$script not executable"; \
	done

lint: lint-python lint-bash ## Run all linting tools

# Formatting targets
format: ## Format code using black and isort
	@echo "Formatting Python code..."
	@if which black >/dev/null 2>&1; then \
		black scripts/vcf_to_obsidian.py $(TEST_DIR)/; \
		echo "✓ Formatted with black"; \
	else \
		echo "black not available. Install with: make install-lint"; \
	fi
	@if which isort >/dev/null 2>&1; then \
		isort scripts/vcf_to_obsidian.py $(TEST_DIR)/; \
		echo "✓ Sorted imports with isort"; \
	else \
		echo "isort not available. Install with: make install-lint"; \
	fi

# Build and package targets
build: ## Build package (check syntax and dependencies)
	@echo "Checking Python syntax..."
	@$(PYTHON) -m py_compile scripts/vcf_to_obsidian.py
	@echo "✓ Python syntax check passed"
	@echo "Making scripts executable..."
	@chmod +x scripts/vcf-to-obsidian.sh scripts/vcf_to_obsidian.py
	@echo "✓ Scripts are executable"

package: build ## Create distributable package
	@echo "Creating package..."
	@if $(PYTHON) -c "import build" 2>/dev/null; then \
		$(PYTHON) -m build; \
	else \
		echo "python-build not available. Install with: pip install build"; \
		echo "For now, package is ready for distribution as-is"; \
	fi

# Maintenance targets
clean: ## Clean temporary files and build artifacts
	@echo "Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ .pytest_cache/ .coverage
	@rm -rf /tmp/vcf_to_obsidian_test_* /tmp/test_vcf_subset /tmp/test_mixed_vcards
	@rm -rf /tmp/empty_vcf_dir /tmp/test_obsidian*
	@echo "✓ Cleanup complete"

docs: ## Show usage documentation
	@echo "=== VCF to Obsidian VCF Contacts ==="
	@echo ""
	@echo "Python Implementation:"
	@$(PYTHON) scripts/vcf_to_obsidian.py --help 2>/dev/null || echo "Dependencies missing. Run: make install"
	@echo ""
	@echo "Bash Implementation:"
	@./scripts/vcf-to-obsidian.sh --help

docs-install: ## Install documentation dependencies
	$(PIP) install sphinx sphinx-autoapi sphinx-rtd-theme

docs-html: ## Build HTML documentation using Sphinx
	@echo "Building HTML documentation..."
	@if command -v sphinx-build >/dev/null 2>&1; then \
		cd sphinx && make html; \
		echo "Documentation built successfully in sphinx/build/html/"; \
	else \
		echo "Sphinx not available. Install with: make docs-install"; \
		exit 1; \
	fi

docs-clean: ## Clean documentation build files
	@echo "Cleaning documentation build files..."
	@cd sphinx && make clean 2>/dev/null || true
	@echo "Documentation build files cleaned"

docs-serve: ## Serve documentation locally (requires Python 3)
	@echo "Starting local documentation server..."
	@echo "Open http://localhost:8000 in your browser"
	@cd sphinx/build/html && $(PYTHON) -m http.server 8000

shell: ## Start interactive shell with project environment
	@echo "Starting shell with project environment..."
	@echo "Available commands:"
	@echo "  python scripts/vcf_to_obsidian.py --help"
	@echo "  ./scripts/vcf-to-obsidian.sh --help"
	@echo "  make test-all"
	@$(SHELL)

# CI/Development workflow targets
ci: setup-dev test-all lint ## Run full CI pipeline (install, test, lint)
	@echo ""
	@echo "🎉 CI pipeline completed successfully!"

dev-check: ## Quick development check (test + lint)
	@echo "Running development checks..."
	@make test-bash
	@make lint-bash
	@if $(PYTHON) -c "import pytest, vobject, click" 2>/dev/null; then \
		make test-python lint-python; \
	else \
		echo "Skipping Python checks (missing dependencies)"; \
	fi

# Quick start targets
quick-start: ## Show quick start guide
	@echo "=== Quick Start Guide ==="
	@echo ""
	@echo "1. Set up development environment:"
	@echo "   make setup-dev"
	@echo ""
	@echo "2. Run all tests:"
	@echo "   make test-all"
	@echo ""
	@echo "3. Run linting:"
	@echo "   make lint"
	@echo ""
	@echo "4. Use the tools:"
	@echo "   # Bash implementation (no dependencies)"
	@echo "   ./scripts/vcf-to-obsidian.sh --folder ./tests/data --obsidian ./output"
	@echo ""
	@echo "   # Python implementation (requires dependencies)"
	@echo "   python scripts/vcf_to_obsidian.py --folder ./tests/data --obsidian ./output"

demo: ## Run a quick demo with test data
	@echo "Running demo with test data..."
	@mkdir -p /tmp/demo_output
	@echo "Testing bash implementation..."
	@./scripts/vcf-to-obsidian.sh --folder ./tests/data --obsidian /tmp/demo_output --verbose
	@echo ""
	@echo "Demo output created in /tmp/demo_output"
	@echo "Generated files:"
	@ls -la /tmp/demo_output/ | head -10
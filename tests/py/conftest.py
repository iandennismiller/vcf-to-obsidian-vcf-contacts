"""
Shared pytest fixtures for vcf-to-obsidian tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import os
import sys

# Add the project root to Python path to import the module
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import classes that will be used by tests
from vcf_to_obsidian import VCFConverter, MarkdownWriter


@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing."""
    test_dir = tempfile.mkdtemp()
    test_vcf_dir = Path(test_dir) / "vcf"
    test_output_dir = Path(test_dir) / "output"
    test_vcf_dir.mkdir()
    test_output_dir.mkdir()
    
    yield {
        'test_dir': Path(test_dir),
        'test_vcf_dir': test_vcf_dir,
        'test_output_dir': test_output_dir
    }
    
    # Cleanup
    shutil.rmtree(test_dir)


@pytest.fixture
def test_data_dir():
    """Path to the test data directory."""
    return Path(__file__).parent.parent / "data" / "vcf"


def create_test_vcf(test_vcf_dir, filename, content):
    """Helper function to create a test VCF file."""
    vcf_path = test_vcf_dir / filename
    with open(vcf_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return vcf_path


def load_test_vcf(test_data_dir, test_vcf_dir, test_vcf_filename, target_filename=None):
    """Helper function to load a VCF file from test data and copy it to test directory."""
    if target_filename is None:
        target_filename = test_vcf_filename
    
    source_path = test_data_dir / test_vcf_filename
    if not source_path.exists():
        raise FileNotFoundError(f"Test VCF file not found: {source_path}")
    
    target_path = test_vcf_dir / target_filename
    shutil.copy2(source_path, target_path)
    return target_path
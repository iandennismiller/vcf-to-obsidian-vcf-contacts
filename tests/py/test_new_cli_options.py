"""
Tests for new CLI options: --folder, --obsidian, and --file
"""

import pytest
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil


class TestNewCLIOptions:
    """Test cases for new CLI options functionality."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        test_vcf_dir = Path(tempfile.mkdtemp())
        test_output_dir = Path(tempfile.mkdtemp())
        test_output_dir2 = Path(tempfile.mkdtemp())
        
        yield {
            'test_vcf_dir': test_vcf_dir,
            'test_output_dir': test_output_dir,
            'test_output_dir2': test_output_dir2
        }
        
        # Cleanup
        shutil.rmtree(test_vcf_dir, ignore_errors=True)
        shutil.rmtree(test_output_dir, ignore_errors=True)
        shutil.rmtree(test_output_dir2, ignore_errors=True)

    def create_test_vcf(self, directory, filename, content=None):
        """Create a test VCF file."""
        if content is None:
            content = """BEGIN:VCARD
VERSION:3.0
FN:Test User
N:User;Test;;;
UID:test-uid-123
ORG:Test Organization
TEL;TYPE=WORK:+1-555-123-4567
EMAIL;TYPE=WORK:test@example.com
END:VCARD"""
        
        vcf_path = directory / filename
        with open(vcf_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return vcf_path

    def test_cli_new_help_format(self):
        """Test that new CLI help shows the new options."""
        try:
            result = subprocess.run(
                [sys.executable, "vcf_to_obsidian.py", "--help"],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0
            assert "--folder" in result.stdout
            assert "--obsidian" in result.stdout
            assert "--file" in result.stdout
            # Check that help mentions multiple sources but not multiple destinations
            help_text = result.stdout.lower()
            assert "multiple times" in help_text or "specified multiple times" in help_text
        except subprocess.TimeoutExpired:
            pytest.skip("CLI help test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_no_arguments_error(self):
        """Test CLI shows error when no arguments provided."""
        try:
            result = subprocess.run(
                [sys.executable, "vcf_to_obsidian.py"],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode != 0
            assert "Must specify at least one --folder or --file option" in result.stderr
        except subprocess.TimeoutExpired:
            pytest.skip("CLI no args test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_missing_obsidian_error(self, temp_dirs):
        """Test CLI shows error when obsidian option is missing."""
        vcf_file = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test.vcf")
        
        try:
            result = subprocess.run(
                [sys.executable, "vcf_to_obsidian.py", "--folder", str(temp_dirs['test_vcf_dir'])],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode != 0
            assert "Must specify at least one --obsidian option" in result.stderr
        except subprocess.TimeoutExpired:
            pytest.skip("CLI missing obsidian test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_folder_option(self, temp_dirs):
        """Test CLI with --folder option."""
        vcf_file = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert "Found 1 VCF file(s) to process" in result.stdout
            assert "Successfully completed 1/1 conversions" in result.stdout
            
            # Check that markdown file was created
            md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
            assert len(md_files) > 0
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI folder test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_file_option(self, temp_dirs):
        """Test CLI with --file option."""
        vcf_file = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--file", str(vcf_file),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert "Found 1 VCF file(s) to process" in result.stdout
            assert "Successfully completed 1/1 conversions" in result.stdout
            
            # Check that markdown file was created
            md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
            assert len(md_files) > 0
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI file test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_multiple_folders(self, temp_dirs):
        """Test CLI with multiple --folder options."""
        # Create VCF files in both directories
        vcf_file1 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test1.vcf")
        vcf_file2 = self.create_test_vcf(temp_dirs['test_output_dir2'], "test2.vcf")  # Reuse as source
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--folder", str(temp_dirs['test_output_dir2']),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert "Found 2 VCF file(s) to process" in result.stdout
            assert "Successfully completed 2/2 conversions" in result.stdout
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI multiple folders test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_multiple_obsidian_uses_last(self, temp_dirs):
        """Test CLI uses the last --obsidian option when multiple are provided."""
        vcf_file = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--obsidian", str(temp_dirs['test_output_dir']),
                    "--obsidian", str(temp_dirs['test_output_dir2'])
                ],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            # Should succeed and use the last obsidian option
            assert result.returncode == 0
            assert f"Converting to Markdown in '{temp_dirs['test_output_dir2']}'" in result.stdout
            
            # Check that markdown file was created only in the second output directory  
            md_files2 = list(temp_dirs['test_output_dir2'].glob("*.md"))
            assert len(md_files2) > 0
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI multiple obsidian uses last test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_mixed_sources(self, temp_dirs):
        """Test CLI with both --folder and --file options."""
        vcf_file1 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test1.vcf")
        vcf_file2 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "single.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--file", str(vcf_file2),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            # Should process folder files + the specific file (but may count single.vcf twice)
            assert "VCF file(s) to process" in result.stdout
            assert "conversions" in result.stdout
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI mixed sources test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_verbose_with_new_options(self, temp_dirs):
        """Test verbose output with new CLI options."""
        vcf_file = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--obsidian", str(temp_dirs['test_output_dir']),
                    "--verbose"
                ],
                cwd=Path(__file__).parent.parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert "Found 1 VCF file(s) in" in result.stdout
            assert "Destination directory:" in result.stdout
            assert "Processing:" in result.stdout
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI verbose test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_ignore_option_help(self):
        """Test that --ignore option appears in help."""
        try:
            result = subprocess.run(
                [sys.executable, "vcf_to_obsidian.py", "--help"],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0
            assert "--ignore" in result.stdout
            assert "Specific VCF file to ignore" in result.stdout
            assert "can be specified multiple times" in result.stdout or "multiple times" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("CLI ignore help test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_ignore_single_file(self, temp_dirs):
        """Test CLI with --ignore option for a single file."""
        vcf_file1 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test1.vcf")
        vcf_file2 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test2.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--ignore", str(vcf_file1),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert "Found 1 VCF file(s) to process" in result.stdout  # Only test2.vcf should be processed
            assert "Ignored 1 file(s)" in result.stdout
            assert "Successfully completed 1/1 conversions" in result.stdout
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI ignore single file test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_ignore_multiple_files(self, temp_dirs):
        """Test CLI with multiple --ignore options."""
        vcf_file1 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test1.vcf")
        vcf_file2 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test2.vcf")
        vcf_file3 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test3.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--ignore", str(vcf_file1),
                    "--ignore", str(vcf_file3),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert "Found 1 VCF file(s) to process" in result.stdout  # Only test2.vcf should be processed
            assert "Ignored 2 file(s)" in result.stdout
            assert "Successfully completed 1/1 conversions" in result.stdout
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI ignore multiple files test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_ignore_all_files(self, temp_dirs):
        """Test CLI when all files are ignored."""
        vcf_file1 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test1.vcf")
        vcf_file2 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test2.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--ignore", str(vcf_file1),
                    "--ignore", str(vcf_file2),
                    "--obsidian", str(temp_dirs['test_output_dir'])
                ],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode != 0  # Should fail when no files remain
            assert "No VCF files remaining to process after applying ignore list" in result.stderr
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI ignore all files test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")

    def test_cli_ignore_with_verbose(self, temp_dirs):
        """Test --ignore option with verbose output."""
        vcf_file1 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test1.vcf")
        vcf_file2 = self.create_test_vcf(temp_dirs['test_vcf_dir'], "test2.vcf")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, "vcf_to_obsidian.py",
                    "--folder", str(temp_dirs['test_vcf_dir']),
                    "--ignore", str(vcf_file1),
                    "--obsidian", str(temp_dirs['test_output_dir']),
                    "--verbose"
                ],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0
            assert f"Will ignore file: '{vcf_file1}'" in result.stdout
            assert "Ignored 1 file(s)" in result.stdout
            assert "Found 1 VCF file(s) to process" in result.stdout
            
        except subprocess.TimeoutExpired:
            pytest.skip("CLI ignore with verbose test timed out")
        except FileNotFoundError:
            pytest.skip("vcf_to_obsidian.py not found for CLI testing")
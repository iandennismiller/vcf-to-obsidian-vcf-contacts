"""
Tests for VCF file reading and parsing functionality.
"""

from conftest import create_test_vcf


class TestVCFReading:
    """Test cases for VCF file reading and parsing."""

    def test_uuid_validation_function(self):
        """Test the UUID validation function directly."""
        from vcf_to_obsidian.vcf_reader import VCFReader

        reader = VCFReader()

        # Test valid UUIDs
        valid_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "550e8400-e29b-41d4-a716-446655440000",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        ]

        for uid in valid_uuids:
            assert reader.is_valid_uuid(uid), f"Expected {uid} to be valid"

        # Test invalid UUIDs
        invalid_uuids = [
            "invalid-uuid-format",
            "content-test-123",
            "123",
            "not-a-uuid-at-all",
            "",
            None,
            "123e4567-e89b-12d3-a456-42661417400",  # Too short
            "123e4567-e89b-12d3-a456-426614174000x",  # Too long
            "123e4567-e89b-12d3-a456-42661417400g",  # Invalid character
        ]

        for uid in invalid_uuids:
            assert not reader.is_valid_uuid(uid), f"Expected {uid} to be invalid"

    def test_convert_vcf_accepts_invalid_uuid(self, temp_dirs):
        """Test that VCF files with invalid UUIDs are now processed normally (UUID validation removed)."""
        from vcf_to_obsidian.vcf_converter import VCFConverter
        import io
        from contextlib import redirect_stdout

        # Create a VCF file with invalid UUID
        invalid_uuid_content = """BEGIN:VCARD
VERSION:3.0
UID:invalid-uuid-format
FN:Invalid UUID Test
N:Test;Invalid UUID;;;
END:VCARD"""

        vcf_path = create_test_vcf(temp_dirs['test_vcf_dir'], "invalid_uuid.vcf", invalid_uuid_content)

        converter = VCFConverter()

        # Capture stdout to check no warning message
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = converter.convert_vcf_to_markdown(vcf_path, temp_dirs['test_output_dir'])

        output = captured_output.getvalue()

        # Should return True and not print validation warnings (UUID validation removed)
        assert result is True
        assert "Warning: VCF file" not in output or "invalid UUID" not in output
        assert "skipping file" not in output
        assert "Converted:" in output

        # Markdown file should be created
        md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
        assert len(md_files) > 0

    def test_convert_vcf_accepts_valid_uuid(self, temp_dirs):
        """Test that VCF files with valid UUIDs are processed normally."""
        from vcf_to_obsidian.vcf_converter import VCFConverter
        import io
        from contextlib import redirect_stdout

        # Create a VCF file with valid UUID
        valid_uuid_content = """BEGIN:VCARD
VERSION:3.0
UID:123e4567-e89b-12d3-a456-426614174000
FN:Valid UUID Test
N:Test;Valid UUID;;;
END:VCARD"""

        vcf_path = create_test_vcf(temp_dirs['test_vcf_dir'], "valid_uuid.vcf", valid_uuid_content)

        converter = VCFConverter()

        # Capture stdout
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = converter.convert_vcf_to_markdown(vcf_path, temp_dirs['test_output_dir'])

        output = captured_output.getvalue()

        # Should return True and not print warning
        assert result is True
        assert "Warning:" not in output
        assert "invalid UUID" not in output
        assert "skipping file" not in output
        assert "Converted:" in output

        # Markdown file should be created
        md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
        assert len(md_files) > 0

    def test_convert_vcf_accepts_no_uid(self, temp_dirs):
        """Test that VCF files with no UID are processed normally."""
        from vcf_to_obsidian.vcf_converter import VCFConverter
        import io
        from contextlib import redirect_stdout

        # Create a VCF file with no UID
        no_uid_content = """BEGIN:VCARD
VERSION:3.0
FN:No UID Test
N:Test;No UID;;;
END:VCARD"""

        vcf_path = create_test_vcf(temp_dirs['test_vcf_dir'], "no_uid.vcf", no_uid_content)

        converter = VCFConverter()

        # Capture stdout
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = converter.convert_vcf_to_markdown(vcf_path, temp_dirs['test_output_dir'])

        output = captured_output.getvalue()

        # Should return True and not print warning (no UID is fine)
        assert result is True
        assert "Warning:" not in output
        assert "invalid UUID" not in output
        assert "skipping file" not in output
        assert "Converted:" in output

        # Markdown file should be created
        md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
        assert len(md_files) > 0

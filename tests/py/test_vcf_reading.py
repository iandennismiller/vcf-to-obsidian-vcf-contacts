"""
Tests for VCF file reading and parsing functionality.
"""

import pytest
from conftest import load_test_vcf, create_test_vcf
from vcf_to_obsidian import parse_vcf_file


class TestVCFReading:
    """Test cases for VCF file reading and parsing."""

    def test_parse_vcf_with_full_name_and_uid(self, temp_dirs, test_data_dir):
        """Test parsing VCF with both full name and UID."""
        vcf_path = load_test_vcf(test_data_dir, temp_dirs['test_vcf_dir'], "full_name_and_uid.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        assert contact_data['uid'] == '12345-abcde-67890'
        assert contact_data['full_name'] == 'John Doe'
        assert contact_data['given_name'] == 'John'
        assert contact_data['family_name'] == 'Doe'
        assert contact_data['organization'] == 'Acme Corporation'
        assert '+1-555-123-4567' in contact_data['phone_numbers']
        assert 'john.doe@acme.com' in contact_data['email_addresses']

    def test_parse_vcf_with_uid_only(self, temp_dirs, test_data_dir):
        """Test parsing VCF with UID but no full name."""
        vcf_path = load_test_vcf(test_data_dir, temp_dirs['test_vcf_dir'], "uid_only.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        assert contact_data['uid'] == 'uid-only-12345'
        assert contact_data['full_name'] == ''
        assert contact_data['given_name'] == 'Jane'
        assert contact_data['family_name'] == 'Smith'

    def test_parse_vcf_with_full_name_only(self, temp_dirs, test_data_dir):
        """Test parsing VCF with full name but no UID."""
        vcf_path = load_test_vcf(test_data_dir, temp_dirs['test_vcf_dir'], "full_name_only.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        assert contact_data['uid'] == ''
        assert contact_data['full_name'] == 'Bob Wilson'
        assert contact_data['given_name'] == 'Bob'
        assert contact_data['family_name'] == 'Wilson'

    def test_parse_vcf_with_empty_uid(self, temp_dirs, test_data_dir):
        """Test parsing VCF with empty UID field."""
        vcf_path = load_test_vcf(test_data_dir, temp_dirs['test_vcf_dir'], "empty_uid.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        assert contact_data['uid'] == ''
        assert contact_data['full_name'] == 'Empty UID Test'

    def test_vcard4_support(self, temp_dirs, test_data_dir):
        """Test that vCard 4.0 format is properly supported with vobject."""
        # Test the vCard 4.0 file we created
        vcf_path = test_data_dir / "vcard4_test.vcf"
        if vcf_path.exists():
            contact_data = parse_vcf_file(vcf_path)
            # Should be able to parse without errors
            assert isinstance(contact_data, dict)
            assert 'uid' in contact_data
            assert 'full_name' in contact_data

    def test_vobject_fallback(self, temp_dirs, test_data_dir):
        """Test that fallback to legacy parser works when vobject fails."""
        import vcf_to_obsidian
        
        # Save original state
        original_has_vobject = vcf_to_obsidian.HAS_VOBJECT
        
        try:
            # Force fallback by disabling vobject
            vcf_to_obsidian.HAS_VOBJECT = False
            
            # Test with a regular VCF file
            vcf_path = load_test_vcf(test_data_dir, temp_dirs['test_vcf_dir'], "full_name_and_uid.vcf", "fallback_test.vcf")
            contact_data = parse_vcf_file(vcf_path)
            
            # Should still work with legacy parser
            assert contact_data['uid'] == '12345-abcde-67890'
            assert contact_data['full_name'] == 'John Doe'
            assert contact_data['given_name'] == 'John'
            assert contact_data['family_name'] == 'Doe'
            assert contact_data['organization'] == 'Acme Corporation'
            assert '+1-555-123-4567' in contact_data['phone_numbers']
            assert 'john.doe@acme.com' in contact_data['email_addresses']
            
        finally:
            # Restore original state
            vcf_to_obsidian.HAS_VOBJECT = original_has_vobject

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
            "123e4567-e89b-12d3-a456-426614174000x", # Too long
            "123e4567-e89b-12d3-a456-42661417400g",  # Invalid character
        ]
        
        for uid in invalid_uuids:
            assert not reader.is_valid_uuid(uid), f"Expected {uid} to be invalid"

    def test_convert_vcf_skips_invalid_uuid(self, temp_dirs):
        """Test that VCF files with invalid UUIDs are skipped."""
        from vcf_to_obsidian.cli import CLI
        import io
        import sys
        from contextlib import redirect_stdout
        
        # Create a VCF file with invalid UUID
        invalid_uuid_content = """BEGIN:VCARD
VERSION:3.0
UID:invalid-uuid-format
FN:Invalid UUID Test
N:Test;Invalid UUID;;;
END:VCARD"""
        
        vcf_path = create_test_vcf(temp_dirs['test_vcf_dir'], "invalid_uuid.vcf", invalid_uuid_content)
        
        cli = CLI()
        
        # Capture stdout to check warning message
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = cli.convert_vcf_to_markdown(vcf_path, temp_dirs['test_output_dir'])
        
        output = captured_output.getvalue()
        
        # Should return False and print warning
        assert result == False
        assert "Warning: VCF file" in output
        assert "contains invalid UUID" in output
        assert "invalid-uuid-format" in output
        assert "skipping file" in output
        
        # No markdown file should be created
        md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
        assert len(md_files) == 0

    def test_convert_vcf_accepts_valid_uuid(self, temp_dirs):
        """Test that VCF files with valid UUIDs are processed normally."""
        from vcf_to_obsidian.cli import CLI
        import io
        import sys
        from contextlib import redirect_stdout
        
        # Create a VCF file with valid UUID
        valid_uuid_content = """BEGIN:VCARD
VERSION:3.0
UID:123e4567-e89b-12d3-a456-426614174000
FN:Valid UUID Test
N:Test;Valid UUID;;;
END:VCARD"""
        
        vcf_path = create_test_vcf(temp_dirs['test_vcf_dir'], "valid_uuid.vcf", valid_uuid_content)
        
        cli = CLI()
        
        # Capture stdout
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = cli.convert_vcf_to_markdown(vcf_path, temp_dirs['test_output_dir'])
        
        output = captured_output.getvalue()
        
        # Should return True and not print warning
        assert result == True
        assert "Warning:" not in output
        assert "invalid UUID" not in output
        assert "skipping file" not in output
        assert "Converted:" in output
        
        # Markdown file should be created
        md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
        assert len(md_files) > 0

    def test_convert_vcf_accepts_no_uid(self, temp_dirs):
        """Test that VCF files with no UID are processed normally."""
        from vcf_to_obsidian.cli import CLI
        import io
        import sys
        from contextlib import redirect_stdout
        
        # Create a VCF file with no UID
        no_uid_content = """BEGIN:VCARD
VERSION:3.0
FN:No UID Test
N:Test;No UID;;;
END:VCARD"""
        
        vcf_path = create_test_vcf(temp_dirs['test_vcf_dir'], "no_uid.vcf", no_uid_content)
        
        cli = CLI()
        
        # Capture stdout
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = cli.convert_vcf_to_markdown(vcf_path, temp_dirs['test_output_dir'])
        
        output = captured_output.getvalue()
        
        # Should return True and not print warning (no UID is fine)
        assert result == True
        assert "Warning:" not in output
        assert "invalid UUID" not in output
        assert "skipping file" not in output
        assert "Converted:" in output
        
        # Markdown file should be created
        md_files = list(temp_dirs['test_output_dir'].glob("*.md"))
        assert len(md_files) > 0
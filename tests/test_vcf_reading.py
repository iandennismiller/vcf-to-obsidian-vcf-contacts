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
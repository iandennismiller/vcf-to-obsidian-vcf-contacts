#!/usr/bin/env python3
"""
Test suite for vcf_to_obsidian.py

This module contains comprehensive tests for the VCF to Obsidian converter,
testing various scenarios including filename generation logic and VCF parsing.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import os
import sys

# Add the current directory to Python path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vcf_to_obsidian import parse_vcf_file, convert_vcf_to_markdown, generate_obsidian_markdown


class TestVCFToObsidian(unittest.TestCase):
    """Test cases for VCF to Obsidian converter."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.test_vcf_dir = Path(self.test_dir) / "vcf"
        self.test_output_dir = Path(self.test_dir) / "output"
        self.test_vcf_dir.mkdir()
        self.test_output_dir.mkdir()
        
        # Path to the test data directory
        self.test_data_dir = Path(__file__).parent / "test_data" / "vcf"

    def tearDown(self):
        """Clean up after each test method."""
        shutil.rmtree(self.test_dir)

    def create_test_vcf(self, filename, content):
        """Helper method to create a test VCF file."""
        vcf_path = self.test_vcf_dir / filename
        with open(vcf_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return vcf_path
    
    def load_test_vcf(self, test_vcf_filename, target_filename=None):
        """Helper method to load a VCF file from test data and copy it to test directory."""
        if target_filename is None:
            target_filename = test_vcf_filename
        
        source_path = self.test_data_dir / test_vcf_filename
        target_path = self.test_vcf_dir / target_filename
        
        # Copy the test VCF file to the test directory
        shutil.copy2(source_path, target_path)
        return target_path

    def test_parse_vcf_with_full_name_and_uid(self):
        """Test parsing VCF with both full name and UID."""
        vcf_path = self.load_test_vcf("full_name_and_uid.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        self.assertEqual(contact_data['uid'], '12345-abcde-67890')
        self.assertEqual(contact_data['full_name'], 'John Doe')
        self.assertEqual(contact_data['given_name'], 'John')
        self.assertEqual(contact_data['family_name'], 'Doe')
        self.assertEqual(contact_data['organization'], 'Acme Corporation')
        self.assertEqual(contact_data['phone_numbers'], ['+1-555-123-4567'])
        self.assertEqual(contact_data['email_addresses'], ['john.doe@acme.com'])

    def test_parse_vcf_with_uid_only(self):
        """Test parsing VCF with UID but no full name."""
        vcf_path = self.load_test_vcf("uid_only.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        self.assertEqual(contact_data['uid'], 'uid-only-12345')
        self.assertEqual(contact_data['full_name'], '')
        self.assertEqual(contact_data['given_name'], 'Jane')
        self.assertEqual(contact_data['family_name'], 'Smith')

    def test_parse_vcf_with_full_name_only(self):
        """Test parsing VCF with full name but no UID."""
        vcf_path = self.load_test_vcf("full_name_only.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        self.assertEqual(contact_data['uid'], '')
        self.assertEqual(contact_data['full_name'], 'Bob Wilson')
        self.assertEqual(contact_data['given_name'], 'Bob')
        self.assertEqual(contact_data['family_name'], 'Wilson')

    def test_parse_vcf_with_empty_uid(self):
        """Test parsing VCF with empty UID field."""
        vcf_path = self.load_test_vcf("empty_uid.vcf", "test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        self.assertEqual(contact_data['uid'], '')
        self.assertEqual(contact_data['full_name'], 'Empty UID Test')

    def test_filename_generation_fn_preferred(self):
        """Test that FN (full name) is preferred over UID for filename generation."""
        vcf_path = self.load_test_vcf("fn_preferred.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should use full name, not UID
        expected_file = self.test_output_dir / "John Doe.md"
        self.assertTrue(expected_file.exists())
        
        # Should NOT create UID-based file
        uid_file = self.test_output_dir / "12345-abcde-67890.md"
        self.assertFalse(uid_file.exists())

    def test_filename_generation_uid_fallback(self):
        """Test that UID is used as fallback when no full name is available."""
        vcf_path = self.load_test_vcf("uid_fallback.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should use constructed name (Jane Smith) since we have given+family names
        # UID is only used when no name information is available at all
        expected_file = self.test_output_dir / "Jane Smith.md"
        self.assertTrue(expected_file.exists())
        
        # Should NOT use UID since we have name components
        uid_file = self.test_output_dir / "fallback-uid-12345.md"
        self.assertFalse(uid_file.exists())

    def test_filename_generation_constructed_name_fallback(self):
        """Test that constructed name (given+family) is used when no FN or UID."""
        vcf_path = self.load_test_vcf("constructed_name_fallback.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should use constructed name from given+family
        expected_file = self.test_output_dir / "Alice Brown.md"
        self.assertTrue(expected_file.exists())

    def test_filename_generation_vcf_filename_fallback(self):
        """Test that VCF filename is used as final fallback."""
        vcf_path = self.load_test_vcf("minimal_contact.vcf", "minimal_contact.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should fall back to VCF filename
        expected_file = self.test_output_dir / "minimal_contact.md"
        self.assertTrue(expected_file.exists())

    def test_special_characters_in_filename(self):
        """Test that special characters in names are properly sanitized."""
        vcf_path = self.load_test_vcf("special_characters_filename.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Special characters should be replaced with underscores
        expected_file = self.test_output_dir / "John _Doe_ _test@email.com_.md"
        self.assertTrue(expected_file.exists())

    def test_special_characters_in_uid(self):
        """Test that special characters in UID are properly sanitized."""
        vcf_path = self.load_test_vcf("special_characters_uid.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should use constructed name (User Test) since we have given+family names
        # UID is only used when no name information is available
        expected_file = self.test_output_dir / "User Test.md"
        self.assertTrue(expected_file.exists())
        
        # Should NOT use UID since we have name components
        uid_file = self.test_output_dir / "special_chars_in_uid_file_name_.md"
        self.assertFalse(uid_file.exists())

    def test_uid_fallback_when_no_names(self):
        """Test that UID is used as fallback when no name information is available."""
        vcf_path = self.load_test_vcf("uid_only_no_names.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should use UID since no name information is available
        expected_file = self.test_output_dir / "only-uid-available-12345.md"
        self.assertTrue(expected_file.exists())

    def test_uid_special_chars_fallback(self):
        """Test UID with special characters when used as fallback."""
        vcf_path = self.load_test_vcf("uid_special_chars_fallback.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        # Should use UID since no name information, with special chars sanitized
        expected_file = self.test_output_dir / "special_chars_in_uid_file_name_.md"
        self.assertTrue(expected_file.exists())

    def test_markdown_content_generation(self):
        """Test that markdown content is generated correctly."""
        vcf_path = self.load_test_vcf("content_generation_test.vcf", "test.vcf")
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result)
        
        # Check that markdown file was created with FN-based name
        md_file = self.test_output_dir / "Test User.md"
        self.assertTrue(md_file.exists())
        
        # Read and verify content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check frontmatter
        self.assertIn('vcf-contact: true', content)
        self.assertIn('name: "Test User"', content)
        self.assertIn('given-name: "Test"', content)
        self.assertIn('family-name: "User"', content)
        self.assertIn('organization: "Test Organization"', content)
        self.assertIn('"+1-555-123-4567"', content)
        self.assertIn('test@example.com', content)
        self.assertIn('url: "https://example.com"', content)
        self.assertIn('birthday: "1990-01-01"', content)
        
        # Check markdown content
        self.assertIn('# Test User', content)
        self.assertIn('**Organization:** Test Organization', content)
        self.assertIn('**Phone Numbers:**', content)
        self.assertIn('**Email Addresses:**', content)
        self.assertIn('**Website:** https://example.com', content)
        self.assertIn('**Birthday:** 1990-01-01', content)
        self.assertIn('**Notes:**', content)
        self.assertIn('Test note content', content)

    def test_priority_order(self):
        """Test the complete priority order: FN > constructed name > UID > filename."""
        # Test case 1: FN takes priority over UID
        vcf_path_1 = self.load_test_vcf("priority_test_fn_over_uid.vcf", "priority1.vcf")
        result_1 = convert_vcf_to_markdown(vcf_path_1, self.test_output_dir)
        
        self.assertTrue(result_1)
        fn_file = self.test_output_dir / "Priority Test 1.md"
        uid_file = self.test_output_dir / "should-not-be-used.md"
        self.assertTrue(fn_file.exists())
        self.assertFalse(uid_file.exists())

        # Test case 2: Constructed name takes priority over UID when no FN
        vcf_path_2 = self.load_test_vcf("priority_test_constructed_over_uid.vcf", "priority2.vcf")
        result_2 = convert_vcf_to_markdown(vcf_path_2, self.test_output_dir)
        
        self.assertTrue(result_2)
        constructed_file = self.test_output_dir / "Priority ConstructedTest.md"
        uid_file_2 = self.test_output_dir / "should-not-be-used-2.md"
        self.assertTrue(constructed_file.exists())
        self.assertFalse(uid_file_2.exists())


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestVCFToObsidian)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    # Allow running tests directly
    unittest.main()
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
        
        # Check frontmatter - new format
        self.assertIn('N.FN: User', content)
        self.assertIn('N.GN: Test', content)
        self.assertIn('FN: Test User', content)
        self.assertIn('ORG: Test Organization', content)
        self.assertIn('"TEL[WORK]": "+1-555-123-4567"', content)
        self.assertIn('"EMAIL[WORK]": test@example.com', content)
        self.assertIn('"URL[DEFAULT]": https://example.com', content)
        self.assertIn('BDAY: 1990-01-01', content)
        self.assertIn('UID: content-test-123', content)
        self.assertIn('VERSION: "3.0"', content)
        
        # Check notes section
        self.assertIn('#### Notes', content)
        self.assertIn('#Contact', content)

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

    def test_custom_template(self):
        """Test that custom templates work correctly."""
        # Create a simple custom template
        custom_template_content = """---
vcf-contact: true
custom-template: true
{%- if title %}
name: "{{ title }}"
{%- endif %}
---

# Custom Template: {{ title or "Unknown" }}

{%- if organization %}
Company: {{ organization }}
{%- endif %}

{%- if phone_numbers %}
Phone: {{ phone_numbers[0] }}
{%- endif %}
"""
        
        template_path = Path(self.test_dir) / "custom.md.j2"
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(custom_template_content)
        
        # Create test VCF
        vcf_content = """BEGIN:VCARD
VERSION:3.0
FN:Custom Test
N:Test;Custom;;;
ORG:Custom Organization
TEL:+1-555-999-8888
END:VCARD"""
        
        vcf_path = self.create_test_vcf("custom_test.vcf", vcf_content)
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir, str(template_path))
        
        self.assertTrue(result)
        
        # Check that markdown file was created
        md_file = self.test_output_dir / "Custom Test.md"
        self.assertTrue(md_file.exists())
        
        # Read and verify content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check custom template elements
        self.assertIn('custom-template: true', content)
        self.assertIn('# Custom Template: Custom Test', content)
        self.assertIn('Company: Custom Organization', content)
        self.assertIn('Phone: +1-555-999-8888', content)
        
        # Should NOT contain the default template structure
        self.assertNotIn('**Organization:**', content)

    def test_template_with_all_fields(self):
        """Test template rendering with all possible fields."""
        vcf_content = """BEGIN:VCARD
VERSION:3.0
UID:all-fields-test
FN:Full Test User
N:User;Full;Middle;Dr.;Jr.
ORG:Complete Organization
TEL;TYPE=HOME:+1-555-111-1111
TEL;TYPE=WORK:+1-555-222-2222
EMAIL;TYPE=HOME:home@example.com
EMAIL;TYPE=WORK:work@example.com
ADR;TYPE=HOME:;;123 Main St;City;State;12345;Country
ADR;TYPE=WORK:;;456 Work Ave;Work City;Work State;67890;Work Country
NOTE:Complete test note with multiple lines
URL:https://complete.example.com
BDAY:1985-05-15
END:VCARD"""
        
        vcf_path = self.create_test_vcf("complete_test.vcf", vcf_content)
        contact_data = parse_vcf_file(vcf_path)
        markdown_content = generate_obsidian_markdown(contact_data)
        
        # Check all fields are present in new format
        self.assertIn('N.FN: User', markdown_content)
        self.assertIn('N.GN: Full', markdown_content)
        self.assertIn('FN: Full Test User', markdown_content)
        self.assertIn('ORG: Complete Organization', markdown_content)
        self.assertIn('"TEL[HOME]": "+1-555-111-1111"', markdown_content)
        self.assertIn('"TEL[WORK]": "+1-555-222-2222"', markdown_content)
        self.assertIn('"EMAIL[HOME]": home@example.com', markdown_content)
        self.assertIn('"EMAIL[WORK]": work@example.com', markdown_content)
        self.assertIn('"URL[DEFAULT]": https://complete.example.com', markdown_content)
        self.assertIn('BDAY: 1985-05-15', markdown_content)
        self.assertIn('UID: all-fields-test', markdown_content)
        self.assertIn('VERSION: "3.0"', markdown_content)
        
        # Check address components
        self.assertIn('"ADR[HOME].STREET": 123 Main St', markdown_content)
        self.assertIn('"ADR[HOME].LOCALITY": City', markdown_content)
        self.assertIn('"ADR[HOME].REGION": State', markdown_content)
        self.assertIn('"ADR[HOME].POSTAL": "12345"', markdown_content)
        self.assertIn('"ADR[HOME].COUNTRY": Country', markdown_content)
        self.assertIn('"ADR[WORK].STREET": 456 Work Ave', markdown_content)
        self.assertIn('"ADR[WORK].LOCALITY": Work City', markdown_content)
        self.assertIn('"ADR[WORK].REGION": Work State', markdown_content)
        self.assertIn('"ADR[WORK].POSTAL": "67890"', markdown_content)
        self.assertIn('"ADR[WORK].COUNTRY": Work Country', markdown_content)
        
        # Check notes section structure
        self.assertIn('#### Notes', markdown_content)
        self.assertIn('#Contact', markdown_content)

    def test_template_fallback_when_file_missing(self):
        """Test that default template is used when custom template file doesn't exist."""
        vcf_content = """BEGIN:VCARD
VERSION:3.0
FN:Fallback Test
N:Test;Fallback;;;
END:VCARD"""
        
        vcf_path = self.create_test_vcf("fallback_test.vcf", vcf_content)
        # Use a non-existent template path
        result = convert_vcf_to_markdown(vcf_path, self.test_output_dir, "/path/does/not/exist.j2")
        
        self.assertTrue(result)
        
        # Should still create the file using the default template
        md_file = self.test_output_dir / "Fallback Test.md"
        self.assertTrue(md_file.exists())
        
        # Read and verify it uses default template format (new format)
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('N.FN: Test', content)
        self.assertIn('N.GN: Fallback', content)
        self.assertIn('FN: Fallback Test', content)
        self.assertIn('VERSION: "3.0"', content)
        # Should NOT contain custom template markers
        self.assertNotIn('custom-template: true', content)

    def test_vcard4_support(self):
        """Test that vCard 4.0 format is properly supported with vobject."""
        # Test the vCard 4.0 file we created
        vcf_path = self.test_data_dir / "vcard4_test.vcf"
        contact_data = parse_vcf_file(vcf_path)
        
        # Verify all fields are correctly parsed
        self.assertEqual(contact_data['uid'], 'vcard4-test-uuid')
        self.assertEqual(contact_data['full_name'], 'Jane Doe')
        self.assertEqual(contact_data['given_name'], 'Jane')
        self.assertEqual(contact_data['family_name'], 'Doe')
        self.assertEqual(contact_data['organization'], 'Tech Corp')
        self.assertEqual(len(contact_data['phone_numbers']), 2)
        self.assertIn('+1-555-111-1111', contact_data['phone_numbers'])
        self.assertIn('+1-555-222-2222', contact_data['phone_numbers'])
        self.assertEqual(len(contact_data['email_addresses']), 2)
        self.assertIn('jane.doe@personal.com', contact_data['email_addresses'])
        self.assertIn('jane.doe@techcorp.com', contact_data['email_addresses'])
        self.assertEqual(len(contact_data['addresses']), 2)
        self.assertIn('123 Main St, Anytown, State, 12345, USA', contact_data['addresses'])
        self.assertIn('456 Business Ave, Work City, Work State, 67890, USA', contact_data['addresses'])
        self.assertEqual(contact_data['notes'], 'This is a vCard 4.0 format test contact')
        self.assertEqual(contact_data['url'], 'https://janedoe.example.com')
        self.assertEqual(contact_data['birthday'], '19850315')

    def test_vobject_parsing(self):
        """Test that vobject parser works correctly for all standard VCF data."""
        # Test with a regular VCF file
        vcf_path = self.load_test_vcf("full_name_and_uid.vcf", "vobject_test.vcf")
        contact_data = parse_vcf_file(vcf_path)
        
        # Should correctly parse all fields
        self.assertEqual(contact_data['uid'], '12345-abcde-67890')
        self.assertEqual(contact_data['full_name'], 'John Doe')
        self.assertEqual(contact_data['given_name'], 'John')
        self.assertEqual(contact_data['family_name'], 'Doe')
        self.assertEqual(contact_data['organization'], 'Acme Corporation')
        self.assertEqual(contact_data['phone_numbers'], ['+1-555-123-4567'])
        self.assertEqual(contact_data['email_addresses'], ['john.doe@acme.com'])

    def test_fn_change_with_same_uid(self):
        """Test that when FN changes but UID stays the same, the old file is removed and new file is created."""
        # First, create a contact with the original FN
        vcf_path_1 = self.load_test_vcf("fn_change_before.vcf", "contact.vcf")
        result_1 = convert_vcf_to_markdown(vcf_path_1, self.test_output_dir)
        
        self.assertTrue(result_1)
        # Should create file with original FN
        original_file = self.test_output_dir / "John Smith.md"
        self.assertTrue(original_file.exists())
        
        # Verify the UID in the original file content
        with open(original_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        self.assertIn('UID: test-uid-12345', original_content)
        
        # Now, update the VCF with a new FN but same UID
        vcf_path_2 = self.load_test_vcf("fn_change_after.vcf", "contact.vcf")
        result_2 = convert_vcf_to_markdown(vcf_path_2, self.test_output_dir)
        
        self.assertTrue(result_2)
        # Should create file with new FN
        new_file = self.test_output_dir / "John Doe.md"
        self.assertTrue(new_file.exists())
        
        # Verify the UID in the new file content
        with open(new_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
        self.assertIn('UID: test-uid-12345', new_content)
        self.assertIn('FN: John Doe', new_content)
        
        # Old file should be removed since it has the same UID
        self.assertFalse(original_file.exists())

    def test_fn_change_same_filename_no_removal(self):
        """Test that when converting the same contact with same FN, the file is not removed."""
        # Create a contact
        vcf_path = self.load_test_vcf("fn_change_before.vcf", "contact.vcf")
        result_1 = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result_1)
        original_file = self.test_output_dir / "John Smith.md"
        self.assertTrue(original_file.exists())
        
        # Convert the same contact again (same FN, same UID)
        result_2 = convert_vcf_to_markdown(vcf_path, self.test_output_dir)
        
        self.assertTrue(result_2)
        # File should still exist (not removed and recreated)
        self.assertTrue(original_file.exists())

    def test_fn_change_no_uid_no_removal(self):
        """Test that when there's no UID, old files are not removed."""
        # Create VCF without UID
        vcf_content_1 = """BEGIN:VCARD
VERSION:3.0
FN:John Smith
N:Smith;John;;;
EMAIL:john.smith@example.com
END:VCARD"""
        
        vcf_content_2 = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:Doe;John;;;
EMAIL:john.smith@example.com
END:VCARD"""
        
        vcf_path_1 = self.create_test_vcf("contact1.vcf", vcf_content_1)
        result_1 = convert_vcf_to_markdown(vcf_path_1, self.test_output_dir)
        
        self.assertTrue(result_1)
        file_1 = self.test_output_dir / "John Smith.md"
        self.assertTrue(file_1.exists())
        
        vcf_path_2 = self.create_test_vcf("contact2.vcf", vcf_content_2)
        result_2 = convert_vcf_to_markdown(vcf_path_2, self.test_output_dir)
        
        self.assertTrue(result_2)
        file_2 = self.test_output_dir / "John Doe.md"
        self.assertTrue(file_2.exists())
        
        # Both files should exist since there's no UID to match
        self.assertTrue(file_1.exists())
        self.assertTrue(file_2.exists())


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
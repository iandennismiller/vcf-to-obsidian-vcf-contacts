# Test Data

This directory contains VCF test files used by the test suite. Each file represents a specific test scenario.

## VCF Files

- `constructed_name_fallback.vcf` - Contact with N (structured name) but no FN or UID
- `content_generation_test.vcf` - Complete contact with all fields for markdown generation testing
- `empty_uid.vcf` - Contact with empty UID field
- `fn_preferred.vcf` - Contact with both FN and UID to test FN preference
- `full_name_and_uid.vcf` - Contact with both full name and UID
- `full_name_only.vcf` - Contact with FN but no UID
- `minimal_contact.vcf` - Minimal contact with only organization
- `priority_test_constructed_over_uid.vcf` - Test constructed name priority over UID
- `priority_test_fn_over_uid.vcf` - Test FN priority over UID
- `special_characters_filename.vcf` - Contact with special characters in FN
- `special_characters_uid.vcf` - Contact with special characters in UID
- `uid_fallback.vcf` - Contact with UID and structured name
- `uid_only.vcf` - Contact with UID but no FN
- `uid_only_no_names.vcf` - Contact with only UID, no name information
- `uid_special_chars_fallback.vcf` - UID with special characters when used as fallback

Each file is designed to test specific filename generation logic and VCF parsing scenarios.
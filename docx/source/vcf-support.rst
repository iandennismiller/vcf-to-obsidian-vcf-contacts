VCF Support
===========

The script supports both vCard 3.0 and vCard 4.0 formats and extracts the following fields:

- **UID**: Unique Identifier (used for stable filename generation)
- **FN**: Full Name
- **N**: Structured Name (Family;Given;Additional;Prefix;Suffix)
- **ORG**: Organization
- **TEL**: Phone Numbers (with type detection)
- **EMAIL**: Email Addresses (with type detection)
- **ADR**: Addresses (with type detection)
- **URL**: Website URL
- **BDAY**: Birthday
- **NOTE**: Notes/Comments

vCard 4.0 Support
-----------------

The script uses the ``vobject`` library for enhanced vCard parsing, which provides:

- **Better vCard 4.0 compatibility**: Improved parsing of modern vCard format
- **Robust field handling**: More accurate extraction of complex fields like addresses
- **Type parameter support**: Proper handling of type parameters (HOME, WORK, etc.)

Parsing Engine
--------------

The script uses the ``vobject`` library for comprehensive vCard 3.0/4.0 support. This ensures reliable parsing of VCF files while taking advantage of modern parsing capabilities.

Filename Generation
-------------------

The script uses a priority-based approach for generating Markdown filenames:

1. **Full Name (FN)** (highest priority): Uses the full name from the VCF FN field (e.g., ``John Doe.md``)
2. **Constructed Name** (fallback): If no FN field, combines given and family names (e.g., ``John Smith.md``)  
3. **UID** (fallback): If no name is available, uses the UID field (e.g., ``12345-abcde-67890.md``)
4. **VCF Filename** (final fallback): Uses the original VCF filename if no other options are available

This approach prioritizes human-readable filenames while providing UID-based fallback for stability when contact information is incomplete.
"""
VCF Reader module for parsing VCF files.
"""

import vobject
import uuid
from pathlib import Path


class VCFReader:
    """Class responsible for reading and parsing VCF files."""
    
    def __init__(self):
        """Initialize the VCF reader."""
        pass
    
    def is_valid_uuid(self, uid_value):
        """
        Check if a UID value is a valid UUID.
        
        Args:
            uid_value (str): UID value to validate
            
        Returns:
            bool: True if valid UUID, False otherwise
        """
        if not uid_value:
            return False
        
        try:
            uuid.UUID(uid_value)
            return True
        except (ValueError, TypeError):
            return False
    
    def read_vcf_file(self, vcf_path):
        """
        Read and parse a VCF file using vobject.
        
        Args:
            vcf_path (Path): Path to the VCF file
            
        Returns:
            vobject.vCard: Parsed vCard object
            
        Raises:
            Exception: If file cannot be read or parsed
        """
        with open(vcf_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        vcard = vobject.readOne(content)
        return vcard
    
    def parse_vcf_file(self, vcf_path):
        """
        Parse a VCF file and return a dictionary of contact data.
        
        This method provides backward compatibility with existing tests
        that expect a dictionary return format.
        
        Args:
            vcf_path (Path): Path to the VCF file
            
        Returns:
            dict: Dictionary containing contact data
        """
        try:
            vcard = self.read_vcf_file(vcf_path)
            
            # Extract data into dictionary format for compatibility
            contact_data = {}
            
            # Full name
            if hasattr(vcard, 'fn') and vcard.fn.value:
                contact_data['full_name'] = vcard.fn.value
            else:
                contact_data['full_name'] = ''
            
            # UID
            if hasattr(vcard, 'uid') and vcard.uid.value:
                contact_data['uid'] = vcard.uid.value
            else:
                contact_data['uid'] = ''
            
            # Structured name
            if hasattr(vcard, 'n') and vcard.n.value:
                n = vcard.n.value
                contact_data['given_name'] = getattr(n, 'given', '') or ''
                contact_data['family_name'] = getattr(n, 'family', '') or ''
            else:
                contact_data['given_name'] = ''
                contact_data['family_name'] = ''
            
            # Organization
            if hasattr(vcard, 'org') and vcard.org.value:
                org_value = vcard.org.value
                if isinstance(org_value, list) and org_value:
                    contact_data['organization'] = org_value[0]
                elif isinstance(org_value, str):
                    contact_data['organization'] = org_value
                else:
                    contact_data['organization'] = ''
            else:
                contact_data['organization'] = ''
            
            # Phone numbers
            contact_data['phone_numbers'] = []
            if hasattr(vcard, 'tel_list'):
                for tel in vcard.tel_list:
                    contact_data['phone_numbers'].append(tel.value)
            
            # Email addresses
            contact_data['email_addresses'] = []
            if hasattr(vcard, 'email_list'):
                for email in vcard.email_list:
                    contact_data['email_addresses'].append(email.value)
            
            return contact_data
            
        except Exception as e:
            raise Exception(f"Error parsing VCF file {vcf_path}: {e}")
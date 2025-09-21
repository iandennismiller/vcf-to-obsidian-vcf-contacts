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
    

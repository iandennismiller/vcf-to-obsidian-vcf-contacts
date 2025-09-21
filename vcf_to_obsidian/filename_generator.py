"""
Filename Generator module for creating output filenames from VCF data.
"""

import re
from pathlib import Path


class FilenameGenerator:
    """Class responsible for generating output filenames from vCard objects."""
    
    def __init__(self):
        """Initialize the filename generator."""
        pass
    
    def generate_filename(self, vcard, vcf_path):
        """
        Generate an output filename based on vCard data with priority logic.
        
        Priority:
        1. Full Name (FN) field
        2. Constructed name from given + family names
        3. UID field
        4. Original VCF filename
        
        Args:
            vcard: vobject vCard object
            vcf_path (Path): Original VCF file path
            
        Returns:
            str: Safe filename (without extension)
        """
        contact_name = ''
        
        # Priority 1: Use FN (Full Name) if available
        if hasattr(vcard, 'fn') and vcard.fn.value:
            contact_name = vcard.fn.value
        # Priority 2: Construct name from N fields (Given + Family)
        elif hasattr(vcard, 'n') and vcard.n.value:
            n = vcard.n.value
            given_name = getattr(n, 'given', '') or ''
            family_name = getattr(n, 'family', '') or ''
            if given_name or family_name:
                contact_name = f"{given_name} {family_name}".strip()
        # Priority 3: Use UID if no name is available
        elif hasattr(vcard, 'uid') and vcard.uid.value:
            contact_name = vcard.uid.value
        # Priority 4: Use VCF filename as final fallback
        else:
            contact_name = Path(vcf_path).stem
        
        # Clean the filename to be filesystem-safe
        return self._clean_filename(contact_name)
    
    def _clean_filename(self, filename):
        """
        Clean a filename to make it filesystem-safe.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Cleaned filename safe for filesystem use
        """
        # Replace problematic characters with underscores
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove any leading/trailing whitespace and dots
        safe_filename = safe_filename.strip(' .')
        
        # Ensure it's not empty
        if not safe_filename:
            safe_filename = 'untitled'
        
        return safe_filename
    
    def find_existing_files_with_uid(self, output_dir, uid):
        """
        Find existing Markdown files in output directory that have the same UID.
        
        Args:
            output_dir (Path): Output directory to search
            uid (str): UID to search for
            
        Returns:
            list: List of Path objects for files with matching UID
        """
        if not uid:
            return []
        
        output_dir = Path(output_dir)
        matching_files = []
        
        try:
            md_files = output_dir.glob("*.md")
            
            for md_file in md_files:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Look for UID line in the content
                        if f"UID: {uid}" in content:
                            matching_files.append(md_file)
                except Exception:
                    # Skip files that can't be read
                    continue
        except Exception:
            # Skip if directory doesn't exist or can't be accessed
            pass
        
        return matching_files
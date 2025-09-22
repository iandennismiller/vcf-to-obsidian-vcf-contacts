"""
Markdown Writer module for generating Markdown content from VCF data.
"""

from datetime import datetime, timezone


class MarkdownWriter:
    """Class responsible for generating Markdown content from vCard objects."""
    
    def __init__(self):
        """Initialize the Markdown writer."""
        pass
    
    def generate_obsidian_markdown(self, vcard):
        """
        Generate Markdown content compatible with obsidian-vcf-contacts plugin.
        Works directly with vobject instead of intermediate representation.
        
        Args:
            vcard: vobject vCard object
            
        Returns:
            str: Markdown content with frontmatter
        """
        # Build the markdown content directly from vobject
        lines = ["---"]
        
        # Extract structured name
        if hasattr(vcard, 'n') and vcard.n.value:
            n = vcard.n.value
            if hasattr(n, 'family') and n.family:
                lines.append(f"N.FN: {n.family}")
            if hasattr(n, 'given') and n.given:
                lines.append(f"N.GN: {n.given}")
        
        # Extract Full Name
        if hasattr(vcard, 'fn') and vcard.fn.value:
            lines.append(f"FN: {vcard.fn.value}")
        
        # Extract photo
        if hasattr(vcard, 'photo') and vcard.photo.value:
            # ignore if vcard.photo.value data type is bytes
            if not isinstance(vcard.photo.value, bytes):
                # ignore if PHOTO is not a URL
                if not vcard.photo.value.startswith("http"):
                    lines.append(f"PHOTO: {vcard.photo.value}")

        # Extract email addresses with type information
        if hasattr(vcard, 'email_list'):
            for email in vcard.email_list:
                type_label = 'DEFAULT'
                if hasattr(email, 'params') and 'TYPE' in email.params:
                    type_values = email.params['TYPE']
                    if isinstance(type_values, list) and type_values:
                        type_label = type_values[0].upper()
                    elif isinstance(type_values, str):
                        type_label = type_values.upper()
                
                field_key = f"EMAIL[{type_label}]"
                lines.append(f'"{field_key}": {email.value}')
        
        # Extract phone numbers with type information
        if hasattr(vcard, 'tel_list'):
            for tel in vcard.tel_list:
                type_label = 'DEFAULT'
                if hasattr(tel, 'params') and 'TYPE' in tel.params:
                    type_values = tel.params['TYPE']
                    if isinstance(type_values, list) and type_values:
                        type_label = type_values[0].upper()
                    elif isinstance(type_values, str):
                        type_label = type_values.upper()
                
                field_key = f"TEL[{type_label}]"
                lines.append(f'"{field_key}": "{tel.value}"')
        
        # Extract birthday
        if hasattr(vcard, 'bday') and vcard.bday.value:
            lines.append(f"BDAY: {vcard.bday.value}")
        
        # Extract URLs with type information
        if hasattr(vcard, 'url') and vcard.url.value:
            type_label = 'DEFAULT'
            if hasattr(vcard.url, 'params') and 'TYPE' in vcard.url.params:
                type_values = vcard.url.params['TYPE']
                if isinstance(type_values, list) and type_values:
                    type_label = type_values[0].upper()
                elif isinstance(type_values, str):
                    type_label = type_values.upper()
            
            field_key = f"URL[{type_label}]"
            lines.append(f'"{field_key}": {vcard.url.value}')
        
        # Extract organization
        if hasattr(vcard, 'org') and vcard.org.value:
            org_value = vcard.org.value
            if isinstance(org_value, list) and org_value:
                lines.append(f"ORG: {org_value[0]}")
            elif isinstance(org_value, str):
                lines.append(f"ORG: {org_value}")
        
        # Extract addresses with type information
        if hasattr(vcard, 'adr_list'):
            for adr in vcard.adr_list:
                adr_value = adr.value
                type_label = 'DEFAULT'
                if hasattr(adr, 'params') and 'TYPE' in adr.params:
                    type_values = adr.params['TYPE']
                    if isinstance(type_values, list) and type_values:
                        type_label = type_values[0].upper()
                    elif isinstance(type_values, str):
                        type_label = type_values.upper()
                
                base_key = f"ADR[{type_label}]"
                
                if hasattr(adr_value, 'box') and adr_value.box:
                    lines.append(f'"{base_key}.POBOX": {adr_value.box}')
                if hasattr(adr_value, 'extended') and adr_value.extended:
                    lines.append(f'"{base_key}.EXTENDED": {adr_value.extended}')
                if hasattr(adr_value, 'street') and adr_value.street:
                    lines.append(f'"{base_key}.STREET": {adr_value.street}')
                if hasattr(adr_value, 'city') and adr_value.city:
                    lines.append(f'"{base_key}.LOCALITY": {adr_value.city}')
                if hasattr(adr_value, 'region') and adr_value.region:
                    lines.append(f'"{base_key}.REGION": {adr_value.region}')
                if hasattr(adr_value, 'code') and adr_value.code:
                    lines.append(f'"{base_key}.POSTAL": "{adr_value.code}"')
                if hasattr(adr_value, 'country') and adr_value.country:
                    lines.append(f'"{base_key}.COUNTRY": {adr_value.country}')
        
        # Extract categories
        if hasattr(vcard, 'categories') and vcard.categories.value:
            lines.append(f"CATEGORIES: {vcard.categories.value}")
        
        # Extract UID
        if hasattr(vcard, 'uid') and vcard.uid.value:
            lines.append(f"UID: {vcard.uid.value}")
        
        # Extract version
        if hasattr(vcard, 'version') and vcard.version.value:
            lines.append(f'VERSION: "{vcard.version.value}"')
        
        # Add REV timestamp - always current time when markdown is created/updated
        current_time = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        lines.append(f"REV: {current_time}")
        
        lines.append("")
        lines.append("---")
        
        # Add notes section if available
        notes_added = False
        if hasattr(vcard, 'note') and vcard.note.value:
            notes_added = True
        if hasattr(vcard, 'categories') and vcard.categories.value:
            notes_added = True
        
        if notes_added:
            lines.append("#### Notes")
            lines.append("")
            
            if hasattr(vcard, 'categories') and vcard.categories.value:
                category_list = vcard.categories.value.split(',')
                contact_line = "#Contact"
                for category in category_list:
                    contact_line += f" #{category.strip()}"
                lines.append(contact_line)
            else:
                lines.append("#Contact")
        
        return '\n'.join(lines) + '\n'
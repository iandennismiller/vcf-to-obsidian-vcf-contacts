#!/bin/bash

# vcf-to-obsidian.sh
# Pure bash implementation of VCF to Obsidian Markdown converter
# Processes VCF files one line at a time to generate Obsidian-compatible Markdown files
#
# Author: Ian Dennis Miller
# License: MIT

set -euo pipefail

# Global variables
VERBOSE=false
SOURCES=()
DESTINATION=""
SUCCESSFUL_CONVERSIONS=0
TOTAL_FILES=0

# Help function
show_help() {
    cat << EOF
vcf-to-obsidian.sh - Convert VCF files to Obsidian-compatible Markdown

Usage:
    vcf-to-obsidian.sh --folder <source_directory> --obsidian <destination_directory>
    vcf-to-obsidian.sh --file <vcf_file> --obsidian <destination_directory>

Options:
    --folder DIR     Source directory containing VCF files (can be specified multiple times)
    --file FILE      Specific VCF file to process (can be specified multiple times)
    --obsidian DIR   Destination directory for generated Markdown files (required)
    --verbose, -v    Enable verbose output
    --help, -h       Show this help message

Examples:
    vcf-to-obsidian.sh --folder ./contacts --obsidian ./obsidian-vault/contacts
    vcf-to-obsidian.sh --file ./contact.vcf --obsidian ./obsidian-vault/contacts
    vcf-to-obsidian.sh --folder ./contacts1 --folder ./contacts2 --obsidian ./vault

Note: You must specify at least one source (--folder or --file) and exactly one destination (--obsidian).
EOF
}

# Logging function
log() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo "$@" >&2
    fi
}

# Clean filename by replacing invalid characters
clean_filename() {
    local filename="$1"
    # Replace invalid filename characters with underscores
    echo "$filename" | sed 's/[<>:"/\\|?*]/_/g'
}

# Parse VCF file and extract fields
parse_vcf_file() {
    local vcf_file="$1"
    local -A fields
    
    # Initialize all fields as empty
    fields[FN]=""
    fields[N_FAMILY]=""
    fields[N_GIVEN]=""
    fields[UID]=""
    fields[ORG]=""
    fields[VERSION]=""
    fields[BDAY]=""
    fields[NOTE]=""
    fields[URL]=""
    fields[CATEGORIES]=""
    fields[PHOTO]=""
    
    # Arrays for multiple-value fields
    local -a tel_fields
    local -a email_fields
    local -a adr_fields
    
    local in_vcard=false
    
    while IFS= read -r line; do
        # Remove carriage returns if present
        line="${line%$'\r'}"
        
        # Check for vCard boundaries
        if [[ "$line" == "BEGIN:VCARD" ]]; then
            in_vcard=true
            continue
        elif [[ "$line" == "END:VCARD" ]]; then
            break
        elif [[ "$in_vcard" != "true" ]]; then
            continue
        fi
        
        # Handle line folding (lines starting with space or tab continue previous line)
        if [[ "$line" =~ ^[[:space:]] ]]; then
            # This is a continuation of the previous line - skip for simplicity
            continue
        fi
        
        # Parse field:value pairs
        if [[ "$line" =~ ^([^:;]+)(;[^:]*)?:(.*)$ ]]; then
            local field="${BASH_REMATCH[1]}"
            local params="${BASH_REMATCH[2]}"
            local value="${BASH_REMATCH[3]}"
            
            case "$field" in
                "FN")
                    fields[FN]="$value"
                    ;;
                "N")
                    # N field format: Family;Given;Additional;Prefix;Suffix
                    IFS=';' read -ra name_parts <<< "$value"
                    fields[N_FAMILY]="${name_parts[0]:-}"
                    fields[N_GIVEN]="${name_parts[1]:-}"
                    ;;
                "UID")
                    fields[UID]="$value"
                    ;;
                "ORG")
                    fields[ORG]="$value"
                    ;;
                "VERSION")
                    fields[VERSION]="$value"
                    ;;
                "BDAY")
                    fields[BDAY]="$value"
                    ;;
                "NOTE")
                    fields[NOTE]="$value"
                    ;;
                "URL")
                    # Extract type from parameters if present
                    local type="DEFAULT"
                    if [[ "$params" =~ TYPE=([^;]*) ]]; then
                        type=$(echo "${BASH_REMATCH[1]}" | tr '[:lower:]' '[:upper:]')
                    fi
                    fields[URL]="$value"
                    fields[URL_TYPE]="$type"
                    ;;
                "CATEGORIES")
                    fields[CATEGORIES]="$value"
                    ;;
                "PHOTO")
                    # Only include PHOTO if it's a URL (starts with http:// or https://)
                    if [[ "$value" =~ ^https?:// ]]; then
                        fields[PHOTO]="$value"
                    fi
                    ;;
                "TEL")
                    # Extract type from parameters if present
                    local type="DEFAULT"
                    if [[ "$params" =~ TYPE=([^;]*) ]]; then
                        type=$(echo "${BASH_REMATCH[1]}" | tr '[:lower:]' '[:upper:]')
                    fi
                    tel_fields+=("$type:$value")
                    ;;
                "EMAIL")
                    # Extract type from parameters if present
                    local type="DEFAULT"
                    if [[ "$params" =~ TYPE=([^;]*) ]]; then
                        type=$(echo "${BASH_REMATCH[1]}" | tr '[:lower:]' '[:upper:]')
                    fi
                    email_fields+=("$type:$value")
                    ;;
                "ADR")
                    # Extract type from parameters if present
                    local type="DEFAULT"
                    if [[ "$params" =~ TYPE=([^;]*) ]]; then
                        type=$(echo "${BASH_REMATCH[1]}" | tr '[:lower:]' '[:upper:]')
                    fi
                    # ADR format: POBOX;EXTENDED;STREET;LOCALITY;REGION;POSTAL;COUNTRY
                    IFS=';' read -ra adr_parts <<< "$value"
                    local adr_data="$type"
                    for i in "${!adr_parts[@]}"; do
                        case $i in
                            0) adr_data="$adr_data:POBOX:${adr_parts[i]}" ;;
                            1) adr_data="$adr_data:EXTENDED:${adr_parts[i]}" ;;
                            2) adr_data="$adr_data:STREET:${adr_parts[i]}" ;;
                            3) adr_data="$adr_data:LOCALITY:${adr_parts[i]}" ;;
                            4) adr_data="$adr_data:REGION:${adr_parts[i]}" ;;
                            5) adr_data="$adr_data:POSTAL:${adr_parts[i]}" ;;
                            6) adr_data="$adr_data:COUNTRY:${adr_parts[i]}" ;;
                        esac
                    done
                    adr_fields+=("$adr_data")
                    ;;
            esac
        fi
    done < "$vcf_file"
    
    # Output all fields in a format that can be read by the calling function
    for field in "${!fields[@]}"; do
        echo "FIELD:$field:${fields[$field]}"
    done
    
    # Output arrays
    for tel in "${tel_fields[@]}"; do
        echo "TEL:$tel"
    done
    
    for email in "${email_fields[@]}"; do
        echo "EMAIL:$email"
    done
    
    for adr in "${adr_fields[@]}"; do
        echo "ADR:$adr"
    done
}

# Generate Obsidian markdown content
generate_markdown() {
    local -A fields
    local -a tel_list
    local -a email_list
    local -a adr_list
    
    # Read parsed VCF data
    while IFS= read -r line; do
        if [[ "$line" =~ ^FIELD:([^:]+):(.*)$ ]]; then
            fields["${BASH_REMATCH[1]}"]="${BASH_REMATCH[2]}"
        elif [[ "$line" =~ ^TEL:(.*)$ ]]; then
            tel_list+=("${BASH_REMATCH[1]}")
        elif [[ "$line" =~ ^EMAIL:(.*)$ ]]; then
            email_list+=("${BASH_REMATCH[1]}")
        elif [[ "$line" =~ ^ADR:(.*)$ ]]; then
            adr_list+=("${BASH_REMATCH[1]}")
        fi
    done
    
    # Start markdown output
    echo "---"
    
    # Extract structured name
    if [[ -n "${fields[N_FAMILY]:-}" ]]; then
        echo "N.FN: ${fields[N_FAMILY]}"
    fi
    if [[ -n "${fields[N_GIVEN]:-}" ]]; then
        echo "N.GN: ${fields[N_GIVEN]}"
    fi
    
    # Extract Full Name
    if [[ -n "${fields[FN]:-}" ]]; then
        echo "FN: ${fields[FN]}"
    fi
    
    # Extract photo - only if it's a URL
    if [[ -n "${fields[PHOTO]:-}" ]]; then
        echo "PHOTO: ${fields[PHOTO]}"
    fi
    
    # Extract email addresses with type information
    for email in "${email_list[@]}"; do
        IFS=':' read -r type value <<< "$email"
        echo "\"EMAIL[$type]\": $value"
    done
    
    # Extract phone numbers with type information
    for tel in "${tel_list[@]}"; do
        IFS=':' read -r type value <<< "$tel"
        echo "\"TEL[$type]\": \"$value\""
    done
    
    # Extract birthday
    if [[ -n "${fields[BDAY]:-}" ]]; then
        echo "BDAY: ${fields[BDAY]}"
    fi
    
    # Extract URLs with type information
    if [[ -n "${fields[URL]:-}" ]]; then
        local type="${fields[URL_TYPE]:-DEFAULT}"
        echo "\"URL[$type]\": ${fields[URL]}"
    fi
    
    # Extract organization
    if [[ -n "${fields[ORG]:-}" ]]; then
        echo "ORG: ${fields[ORG]}"
    fi
    
    # Extract addresses with type information
    for adr in "${adr_list[@]}"; do
        IFS=':' read -r type rest <<< "$adr"
        local base_key="ADR[$type]"
        
        # Parse the address components
        local components=()
        IFS=':' read -ra components <<< "$rest"
        
        for ((i=0; i<${#components[@]}; i+=2)); do
            local comp_name="${components[i]}"
            local comp_value="${components[i+1]:-}"
            if [[ -n "$comp_value" ]]; then
                case "$comp_name" in
                    "POBOX") echo "\"$base_key.POBOX\": $comp_value" ;;
                    "EXTENDED") echo "\"$base_key.EXTENDED\": $comp_value" ;;
                    "STREET") echo "\"$base_key.STREET\": $comp_value" ;;
                    "LOCALITY") echo "\"$base_key.LOCALITY\": $comp_value" ;;
                    "REGION") echo "\"$base_key.REGION\": $comp_value" ;;
                    "POSTAL") echo "\"$base_key.POSTAL\": \"$comp_value\"" ;;
                    "COUNTRY") echo "\"$base_key.COUNTRY\": $comp_value" ;;
                esac
            fi
        done
    done
    
    # Extract categories
    if [[ -n "${fields[CATEGORIES]:-}" ]]; then
        echo "CATEGORIES: ${fields[CATEGORIES]}"
    fi
    
    # Extract UID - ensure it has urn:uuid: namespace prefix
    if [[ -n "${fields[UID]:-}" ]]; then
        local uid_value="${fields[UID]}"
        if [[ ! "$uid_value" =~ ^urn:uuid: ]]; then
            uid_value="urn:uuid:$uid_value"
        fi
        echo "UID: $uid_value"
    fi
    
    # Extract version
    if [[ -n "${fields[VERSION]:-}" ]]; then
        echo "VERSION: \"${fields[VERSION]}\""
    fi
    
    echo ""
    echo "---"
    
    # Add notes section if available
    local notes_added=false
    if [[ -n "${fields[NOTE]:-}" || -n "${fields[CATEGORIES]:-}" ]]; then
        notes_added=true
        echo "#### Notes"
        echo ""
        
        if [[ -n "${fields[CATEGORIES]:-}" ]]; then
            local contact_line="#Contact"
            IFS=',' read -ra categories <<< "${fields[CATEGORIES]}"
            for category in "${categories[@]}"; do
                # Trim whitespace
                category=$(echo "$category" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                contact_line="$contact_line #$category"
            done
            echo "$contact_line"
        else
            echo "#Contact"
        fi
    fi
}

# Determine output filename based on priority
determine_filename() {
    local -A fields
    local vcf_filename="$1"
    
    # Read parsed VCF data to get field values
    while IFS= read -r line; do
        if [[ "$line" =~ ^FIELD:([^:]+):(.*)$ ]]; then
            fields["${BASH_REMATCH[1]}"]="${BASH_REMATCH[2]}"
        fi
    done
    
    local contact_name=""
    
    # Priority 1: Use FN (Full Name) if available
    if [[ -n "${fields[FN]:-}" ]]; then
        contact_name="${fields[FN]}"
    # Priority 2: Construct name from N fields (Given + Family)
    elif [[ -n "${fields[N_GIVEN]:-}" || -n "${fields[N_FAMILY]:-}" ]]; then
        local given="${fields[N_GIVEN]:-}"
        local family="${fields[N_FAMILY]:-}"
        contact_name=$(echo "$given $family" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    # Priority 3: Use UID if no name is available
    elif [[ -n "${fields[UID]:-}" ]]; then
        contact_name="${fields[UID]}"
    # Priority 4: Use VCF filename as final fallback
    else
        contact_name="$(basename "$vcf_filename" .vcf)"
    fi
    
    # Clean the filename
    clean_filename "$contact_name"
}

# Convert a single VCF file to Markdown
convert_vcf_file() {
    local vcf_file="$1"
    local output_dir="$2"
    
    log "Processing: $vcf_file -> $output_dir"
    
    if [[ ! -f "$vcf_file" ]]; then
        echo "Error: VCF file not found: $vcf_file" >&2
        return 1
    fi
    
    # Parse VCF file
    local parsed_data
    parsed_data=$(parse_vcf_file "$vcf_file")
    
    # Determine output filename
    local output_filename
    output_filename=$(echo "$parsed_data" | determine_filename "$vcf_file")
    
    local output_file="$output_dir/${output_filename}.md"
    
    # Generate markdown content
    local markdown_content
    markdown_content=$(echo "$parsed_data" | generate_markdown)
    
    # Write to output file
    echo "$markdown_content" > "$output_file"
    
    echo "Converted: $(basename "$vcf_file") -> ${output_filename}.md"
    return 0
}

# Find VCF files in a directory
find_vcf_files() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory not found: $dir" >&2
        return 1
    fi
    
    find "$dir" -name "*.vcf" -type f
}

# Process all sources
process_sources() {
    local -a all_vcf_files
    
    # Collect all VCF files from sources
    for source in "${SOURCES[@]}"; do
        if [[ -f "$source" ]]; then
            # Single file
            if [[ "$source" == *.vcf ]]; then
                all_vcf_files+=("$source")
                log "Added file: $source"
            else
                echo "Warning: $source is not a VCF file" >&2
            fi
        elif [[ -d "$source" ]]; then
            # Directory
            log "Scanning directory: $source"
            local dir_files
            dir_files=$(find_vcf_files "$source")
            if [[ -n "$dir_files" ]]; then
                while IFS= read -r vcf_file; do
                    all_vcf_files+=("$vcf_file")
                    log "Found file: $vcf_file"
                done <<< "$dir_files"
            else
                echo "Warning: No VCF files found in directory: $source" >&2
            fi
        else
            echo "Error: Source not found: $source" >&2
            return 1
        fi
    done
    
    TOTAL_FILES=${#all_vcf_files[@]}
    
    if [[ $TOTAL_FILES -eq 0 ]]; then
        echo "Error: No VCF files found to process" >&2
        return 1
    fi
    
    log "Found $TOTAL_FILES VCF file(s) total"
    log "Destination directory: $DESTINATION"
    
    # Ensure output directory exists
    mkdir -p "$DESTINATION"
    
    # Process each VCF file
    for vcf_file in "${all_vcf_files[@]}"; do
        if convert_vcf_file "$vcf_file" "$DESTINATION"; then
            SUCCESSFUL_CONVERSIONS=$((SUCCESSFUL_CONVERSIONS + 1))
        fi
    done
    
    echo "Successfully completed $SUCCESSFUL_CONVERSIONS/$TOTAL_FILES conversions."
}

# Parse command line arguments
parse_args() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 1
    fi
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --folder)
                if [[ -z "${2:-}" ]]; then
                    echo "Error: --folder requires a directory argument" >&2
                    exit 1
                fi
                SOURCES+=("$2")
                shift 2
                ;;
            --file)
                if [[ -z "${2:-}" ]]; then
                    echo "Error: --file requires a file argument" >&2
                    exit 1
                fi
                SOURCES+=("$2")
                shift 2
                ;;
            --obsidian)
                if [[ -z "${2:-}" ]]; then
                    echo "Error: --obsidian requires a directory argument" >&2
                    exit 1
                fi
                if [[ -n "$DESTINATION" ]]; then
                    echo "Warning: Multiple --obsidian options specified, using the last one" >&2
                fi
                DESTINATION="$2"
                shift 2
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "Error: Unknown option: $1" >&2
                echo "Use --help for usage information" >&2
                exit 1
                ;;
        esac
    done
    
    # Validate arguments
    if [[ ${#SOURCES[@]} -eq 0 ]]; then
        echo "Error: At least one source (--folder or --file) must be specified" >&2
        exit 1
    fi
    
    if [[ -z "$DESTINATION" ]]; then
        echo "Error: Destination directory (--obsidian) must be specified" >&2
        exit 1
    fi
}

# Main function
main() {
    parse_args "$@"
    process_sources
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
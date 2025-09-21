# Implementation Comparison

This repository provides two implementations with different trade-offs:

| Feature | Bash Script | Python Script |
|---------|-------------|---------------|
| **Dependencies** | None (standard Unix tools) | Python 3.12+, vobject, click |
| **Performance** | Fast (line-by-line processing) | Fast (vobject parsing) |
| **VCard Support** | 3.0 and 4.0 | 3.0 and 4.0 (via vobject) |
| **Field Parsing** | Manual regex-based | Library-based |
| **Error Handling** | Basic | Comprehensive |
| **Portability** | Unix/Linux/macOS (requires bash) | Cross-platform |
| **Maintenance** | Self-contained | Library dependencies |

## When to use the bash script:

- No Python environment available
- Minimal dependencies preferred  
- Unix/Linux/macOS environments with bash
- Simple deployment scenarios
- Note: Requires bash shell (not compatible with zsh)

## When to use the Python script:

- Python environment already available
- Cross-platform compatibility needed
- More robust error handling required
- Integration with Python workflows

Both implementations produce identical output format and support the same command line interface.
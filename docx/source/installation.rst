Installation
============

This repository provides two implementations with different installation requirements:

Python Implementation
---------------------

For the Python implementation, you need:

- Python 3.12+ (tested with Python 3.12.3)
- vobject 0.9.0+ (for enhanced vCard 3.0/4.0 parsing)
- click 8.0.0+ (for command line interface)

Option 1: Install with pip (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   pip install vcf-to-obsidian-vcf-contacts


Option 2: Install with pipx (For CLI tools)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   pipx install vcf-to-obsidian-vcf-contacts


Option 3: Development Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Clone this repository:
::

   git clone https://github.com/iandennismiller/vcf-to-obsidian-vcf-contacts.git
   cd vcf-to-obsidian-vcf-contacts


2. Install in development mode with testing dependencies:
::

   pip install -e .[dev]


This installs the package in editable mode along with pytest for running tests.

Bash Implementation (No Dependencies)
-------------------------------------

The bash script requires only standard Unix tools and works on any system with bash:

::

   # Make executable
   chmod +x scripts/vcf-to-obsidian.sh


No additional installation is required for the bash implementation.
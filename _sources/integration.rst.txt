Integration
===========

This document explains how to integrate vcf-to-obsidian-vcf-contacts with external tools and workflows.

vdirsyncer Integration
----------------------

`vdirsyncer <https://github.com/pimutils/vdirsyncer>`_ is a command-line tool for synchronizing calendars and contacts between various servers and local storages. You can configure vdirsyncer to automatically convert VCF files to Obsidian-compatible Markdown files after synchronization using post-hooks.

Configuration
^^^^^^^^^^^^^

Add the following configuration to your vdirsyncer config file (typically ``~/.config/vdirsyncer/config``):

.. code-block:: ini

   [storage my_contacts_local]
   type = "filesystem"
   path = "~/.contacts/"
   fileext = ".vcf"
   post_hook = ["command", "HOMEDIR/.virtualenvs/vcf-to-obsidian-vcf-contacts/bin/python3", "HOMEDIR/Work/vcf-to-obsidian-vcf-contacts/scripts/vcf_to_obsidian.py", "--folder", "HOMEDIR/.contacts/Default", "--obsidian", "HOMEDIR/Library/Notes/Contacts"]

Configuration Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

The post_hook command includes the following parameters:

- **command**: The post-hook type (always "command" for shell commands)
- **python3 path**: Full path to your Python interpreter in the virtual environment
- **script path**: Full path to the vcf_to_obsidian.py script
- **--folder**: Source directory containing the synchronized VCF files
- **--obsidian**: Destination directory for generated Markdown files in your Obsidian vault

Customizing Paths
^^^^^^^^^^^^^^^^^

You'll need to adjust the following paths in the configuration:

1. **Python interpreter path**: ``HOMEDIR/.virtualenvs/vcf-to-obsidian-vcf-contacts/bin/python3``
   
   - Replace ``HOMEDIR`` with your actual home directory path (e.g., ``/Users/yourusername`` on macOS, ``/home/yourusername`` on Linux)
   - Replace with your actual virtual environment Python path
   - Use ``which python3`` in your activated virtual environment to find the correct path

2. **Script path**: ``HOMEDIR/Work/vcf-to-obsidian-vcf-contacts/scripts/vcf_to_obsidian.py``
   
   - Replace ``HOMEDIR`` with your actual home directory path
   - Replace with the actual path to where you cloned this repository

3. **Source folder**: ``HOMEDIR/.contacts/Default``
   
   - Replace ``HOMEDIR`` with your actual home directory path
   - This should match the subdirectory where vdirsyncer stores your contacts
   - Typically this will be a subdirectory of the ``path`` specified in your storage config

4. **Obsidian vault path**: ``HOMEDIR/Library/Notes/Contacts``
   
   - Replace ``HOMEDIR`` with your actual home directory path
   - Replace with the actual path to your Obsidian contacts folder

**Example for macOS:**

Replace ``HOMEDIR`` with ``/Users/yourusername`` (where ``yourusername`` is your actual username)

**Example for Linux:**

Replace ``HOMEDIR`` with ``/home/yourusername`` (where ``yourusername`` is your actual username)

**How to find your home directory:**

- On macOS/Linux: Run ``echo $HOME`` in your terminal
- You can also use ``~`` (tilde) as a shortcut for your home directory in most contexts

Workflow
^^^^^^^^

With this configuration, the workflow will be:

1. vdirsyncer synchronizes contacts from your remote server to the local filesystem
2. After synchronization completes, the post_hook automatically runs
3. vcf-to-obsidian-vcf-contacts converts all VCF files to Markdown format
4. The generated Markdown files are saved to your Obsidian vault
5. Obsidian will automatically detect and display the updated contact files

Alternative Installation Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you installed vcf-to-obsidian-vcf-contacts via pip or pipx, you can simplify the post_hook command:

**Using pip installation:**

.. code-block:: ini

   post_hook = ["vcf-to-obsidian", "--folder", "HOMEDIR/.contacts/Default", "--obsidian", "HOMEDIR/Library/Notes/Contacts"]

**Using pipx installation:**

.. code-block:: ini

   post_hook = ["vcf-to-obsidian", "--folder", "HOMEDIR/.contacts/Default", "--obsidian", "HOMEDIR/Library/Notes/Contacts"]

Troubleshooting
^^^^^^^^^^^^^^^

If the post_hook fails to execute:

1. **Check paths**: Ensure all file and directory paths in the configuration exist and are accessible
2. **Test manually**: Run the vcf-to-obsidian command manually to verify it works:

   .. code-block:: bash

      HOMEDIR/.virtualenvs/vcf-to-obsidian-vcf-contacts/bin/python3 \
        HOMEDIR/Work/vcf-to-obsidian-vcf-contacts/scripts/vcf_to_obsidian.py \
        --folder HOMEDIR/.contacts/Default \
        --obsidian HOMEDIR/Library/Notes/Contacts \
        --verbose

3. **Check permissions**: Ensure the Python interpreter and script have execute permissions
4. **View logs**: Use vdirsyncer's verbose mode to see post_hook execution details:

   .. code-block:: bash

      vdirsyncer sync --verbosity debug

Additional Options
^^^^^^^^^^^^^^^^^^

You can enhance the post_hook command with additional vcf-to-obsidian options:

**Enable verbose output for debugging:**

.. code-block:: ini

   post_hook = ["command", "/path/to/python3", "/path/to/vcf_to_obsidian.py", "--folder", "/path/to/contacts", "--obsidian", "/path/to/vault", "--verbose"]

**Process specific files only:**

.. code-block:: ini

   post_hook = ["command", "/path/to/python3", "/path/to/vcf_to_obsidian.py", "--file", "/path/to/specific.vcf", "--obsidian", "/path/to/vault"]

**Ignore certain files:**

.. code-block:: ini

   post_hook = ["command", "/path/to/python3", "/path/to/vcf_to_obsidian.py", "--folder", "/path/to/contacts", "--ignore", "/path/to/unwanted.vcf", "--obsidian", "/path/to/vault"]

For more information on command-line options, see the :doc:`usage` documentation.
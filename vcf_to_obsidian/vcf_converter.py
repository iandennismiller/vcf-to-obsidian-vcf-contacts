"""
VCF Converter module for handling VCF to Markdown conversion.
"""

from pathlib import Path
from queue import Queue
from threading import Thread
from .vcf_reader import VCFReader
from .markdown_writer import MarkdownWriter
from .filename_generator import FilenameGenerator


class VCFConverter:
    """Class responsible for converting VCF files to Markdown format."""
    
    def __init__(self):
        """Initialize the VCF converter."""
        self.reader = VCFReader()
        self.writer = MarkdownWriter()
        self.filename_gen = FilenameGenerator()
    
    def convert_vcf_to_markdown(self, vcf_path, output_dir):
        """
        Convert a single VCF file to Markdown format.
        
        Args:
            vcf_path (Path): Path to the VCF file
            output_dir (Path): Output directory for Markdown files
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read VCF file
            vcard = self.reader.read_vcf_file(vcf_path)
            
            # Generate markdown content
            markdown_content = self.writer.generate_obsidian_markdown(vcard)
            
            # Generate filename
            output_filename = self.filename_gen.generate_filename(vcard, vcf_path)
            output_file = Path(output_dir) / f"{output_filename}.md"
            
            # Remove existing files with the same UID if the filename would be different
            if hasattr(vcard, 'uid') and vcard.uid and vcard.uid.value:
                existing_files = self.filename_gen.find_existing_files_with_uid(output_dir, vcard.uid.value)
                for existing_file in existing_files:
                    if existing_file != output_file:
                        try:
                            existing_file.unlink()
                            print(f"Removed old file: {existing_file.name}")
                        except Exception as e:
                            print(f"Warning: Could not remove old file {existing_file.name}: {e}")
            
            # Write Markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Converted: {vcf_path.name} -> {output_file.name}")
            return True
            
        except Exception as e:
            print(f"Error converting {vcf_path}: {e}")
            return False
    
    
    def create_conversion_task_queue(self, vcf_files, output_dir):
        """
        Create a task queue for VCF file conversion.
        
        Args:
            vcf_files (list): List of VCF file paths
            output_dir (Path): Output directory for Markdown files
            
        Returns:
            Queue: Queue containing conversion tasks
        """
        task_queue = Queue()
        
        for vcf_file in vcf_files:
            task_queue.put((vcf_file, output_dir))
        
        return task_queue
    
    def process_task_queue(self, task_queue, num_workers=1, validate_uuids=False):
        """
        Process a task queue for VCF file conversion.
        
        Args:
            task_queue (Queue): Queue containing conversion tasks
            num_workers (int): Number of worker threads to use
            validate_uuids (bool): Whether to validate UUIDs before conversion
            
        Returns:
            tuple: (successful_count, total_count)
        """
        successful_count = 0
        total_count = task_queue.qsize()
        results_queue = Queue()
        
        def worker():
            while True:
                try:
                    vcf_file, output_dir = task_queue.get(block=False)
                    # Always use convert_vcf_to_markdown now, validate_uuids parameter is ignored
                    result = self.convert_vcf_to_markdown(vcf_file, output_dir)
                    results_queue.put(result)
                    task_queue.task_done()
                except:
                    break
        
        # Start worker threads
        threads = []
        for _ in range(num_workers):
            thread = Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        # Wait for all tasks to complete
        task_queue.join()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        # Count successful conversions
        while not results_queue.empty():
            if results_queue.get():
                successful_count += 1
        
        return successful_count, total_count
    
    def convert_vcf_files_from_sources(self, folder_sources, file_sources, output_dir, ignore_files=None, verbose=False):
        """
        Convert VCF files from multiple sources (folders and individual files) to Markdown format.
        
        This method collects VCF files from the specified sources, applies ignore filters,
        and processes them using the task queue system.
        
        Args:
            folder_sources (list): List of Path objects for directories containing VCF files
            file_sources (list): List of Path objects for individual VCF files
            output_dir (Path): Output directory for Markdown files
            ignore_files (list, optional): List of Path objects for files to ignore
            verbose (bool): Whether to enable verbose output
            
        Returns:
            tuple: (successful_count, total_count, all_vcf_files)
        """
        import click
        import sys
        
        # Collect all VCF files to process
        all_vcf_files = []
        processed_paths = set()  # Track processed file paths to avoid duplicates
        
        # Process folder sources
        for source_path in folder_sources:
            if not source_path.is_dir():
                if verbose:
                    click.echo(f"Error: Source path '{source_path}' is not a directory.", err=True)
                continue
            
            # Find all VCF files in this directory
            vcf_files = list(source_path.glob("*.vcf")) + list(source_path.glob("*.VCF"))
            new_files_count = 0
            for vcf_file in vcf_files:
                absolute_path = vcf_file.resolve()
                if absolute_path not in processed_paths:
                    all_vcf_files.append(vcf_file)
                    processed_paths.add(absolute_path)
                    new_files_count += 1
            
            if verbose:
                if new_files_count < len(vcf_files):
                    click.echo(f"Found {len(vcf_files)} VCF file(s) in '{source_path}' ({new_files_count} new, {len(vcf_files) - new_files_count} duplicates)")
                else:
                    click.echo(f"Found {len(vcf_files)} VCF file(s) in '{source_path}'")
        
        # Process individual file sources
        for file_path in file_sources:
            if not file_path.exists():
                if verbose:
                    click.echo(f"Error: File '{file_path}' does not exist.", err=True)
                continue
            
            if not file_path.is_file():
                if verbose:
                    click.echo(f"Error: Path '{file_path}' is not a file.", err=True)
                continue
            
            # Check if it's a VCF file by extension
            if file_path.suffix.lower() not in ['.vcf']:
                if verbose:
                    click.echo(f"Warning: File '{file_path}' does not have a .vcf extension.", err=True)
            
            absolute_path = file_path.resolve()
            if absolute_path not in processed_paths:
                all_vcf_files.append(file_path)
                processed_paths.add(absolute_path)
                
                if verbose:
                    click.echo(f"Added individual file: '{file_path}'")
            else:
                if verbose:
                    click.echo(f"Skipping duplicate file: '{file_path}'")
        
        # Process ignore list - remove specified files from the task queue
        if ignore_files:
            ignore_paths = set()
            for ignore_path in ignore_files:
                absolute_ignore_path = ignore_path.resolve()
                ignore_paths.add(absolute_ignore_path)
                if verbose:
                    click.echo(f"Will ignore file: '{ignore_path}'")
            
            # Filter out ignored files
            initial_count = len(all_vcf_files)
            all_vcf_files = [vcf_file for vcf_file in all_vcf_files 
                           if vcf_file.resolve() not in ignore_paths]
            ignored_count = initial_count - len(all_vcf_files)
            
            if ignored_count > 0 and verbose:
                click.echo(f"Ignored {ignored_count} file(s)")
        
        # Create destination directory
        output_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            click.echo(f"Destination directory: '{output_dir}'")
        
        if verbose:
            click.echo(f"Converting to Markdown in '{output_dir}'")
        
        # Convert each VCF file to the destination using task queue
        if all_vcf_files:
            task_queue = self.create_conversion_task_queue(all_vcf_files, output_dir)
            successful_conversions, total_conversions = self.process_task_queue(task_queue, validate_uuids=True)
        else:
            successful_conversions, total_conversions = 0, 0
        
        return successful_conversions, total_conversions, all_vcf_files
    
    def process_tasks(self, folder, obsidian, file, verbose, ignore):
        """
        Process VCF conversion tasks from CLI arguments.
        
        This method handles the complete CLI workflow including validation, 
        file collection, processing, and reporting.
        
        Args:
            folder: Tuple/list of folder paths containing VCF files
            obsidian: Path to destination directory for Markdown files
            file: Tuple/list of individual VCF file paths to process
            verbose: Boolean flag for verbose output
            ignore: Tuple/list of VCF file paths to ignore
        """
        import click
        import sys
        
        # Validate that at least one source is specified
        if not folder and not file:
            click.echo("Error: Must specify at least one --folder or --file option.", err=True)
            sys.exit(1)
        
        # Validate file and folder sources exist before processing
        for folder_path in folder:
            if not folder_path.is_dir():
                click.echo(f"Error: Source path '{folder_path}' is not a directory.", err=True)
                sys.exit(1)
        
        for file_path in file:
            if not file_path.exists():
                click.echo(f"Error: File '{file_path}' does not exist.", err=True)
                sys.exit(1)
            if not file_path.is_file():
                click.echo(f"Error: Path '{file_path}' is not a file.", err=True)
                sys.exit(1)
        
        # Convert tuples to lists for easier handling
        folder_sources = list(folder) if folder else []
        file_sources = list(file) if file else []
        ignore_files = list(ignore) if ignore else []
        
        # Use existing method to handle the conversion
        successful_conversions, total_conversions, all_vcf_files = self.convert_vcf_files_from_sources(
            folder_sources=folder_sources,
            file_sources=file_sources,
            output_dir=obsidian,
            ignore_files=ignore_files,
            verbose=verbose
        )
        
        # Handle edge cases for messaging
        if not all_vcf_files:
            if not folder_sources and not file_sources:
                click.echo("No VCF files found to process.", err=True)
            else:
                click.echo("No VCF files remaining to process after applying ignore list.", err=True)
            sys.exit(1)
        
        # Report final results
        click.echo(f"Found {len(all_vcf_files)} VCF file(s) to process")
        click.echo(f"Successfully completed {successful_conversions}/{len(all_vcf_files)} conversions.")
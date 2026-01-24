import os
import shutil
import argparse
import logging
from pathlib import Path

def setup_logging(log_file=None):
    """Sets up logging to console and optionally to a file."""
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def get_unique_filename(destination_folder, filename):
    """
    Checks if a file exists in the destination folder.
    If it does, appends a counter to the filename to make it unique.
    Returns the full path to the unique filename.
    """
    base_name = filename.stem
    extension = filename.suffix
    counter = 1
    new_filename = filename.name
    dest_path = destination_folder / new_filename

    while dest_path.exists():
        new_filename = f"{base_name}_{counter}{extension}"
        dest_path = destination_folder / new_filename
        counter += 1
    
    return dest_path

# File Categories
EXTENSION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.heic', '.raw'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.rtf', '.odt', '.md'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso'],
    'Programs': ['.exe', '.msi', '.bat', '.sh', '.apk', '.app', '.dmg'],
    'Scripts': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
}

def get_category(extension):
    """Returns the category for a given extension."""
    extension = extension.lower()
    if not extension.startswith('.'):
        extension = '.' + extension
        
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            return category
            
    return 'Others'

def organize_files(target_dir, dry_run=False):
    """
    Scans the target directory and moves files into subfolders based on category.
    """
    target_path = Path(target_dir)
    
    if not target_path.exists():
        logging.error(f"Target directory '{target_dir}' does not exist.")
        return

    logging.info(f"Starting organization of '{target_dir}' {'(DRY RUN)' if dry_run else ''}")

    items = list(target_path.iterdir())
    files_moved = 0
    
    for item in items:
        # Skip directories, the script itself, log file, and specific folders we might be creating
        if item.is_file() and item.name != os.path.basename(__file__) and item.name != "organizer.log":
            
            category = get_category(item.suffix)
                
            # Destination folder
            dest_folder = target_path / category
            
            # Determine destination file path
            try:
                if not dry_run:
                    dest_folder.mkdir(exist_ok=True)
                
                dest_file_path = get_unique_filename(dest_folder, item)
                
                logging.info(f"Moving '{item.name}' to '{category}\\{dest_file_path.name}'")
                
                if not dry_run:
                    shutil.move(str(item), str(dest_file_path))
                
                files_moved += 1

            except Exception as e:
                logging.error(f"Error moving '{item.name}': {e}")

    logging.info(f"Organization complete. {files_moved} files processed.")

def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory by extension.")
    parser.add_argument("target_dir", nargs='?', help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the organization without moving files")
    parser.add_argument("--log-file", help="Path to save the log file", default="organizer.log")
    
    args = parser.parse_args()
    
    target_dir = args.target_dir
    
    if not target_dir:
        # If no argument, ask invalid interactively
        try:
            target_dir = input("Enter the full path of the folder to organize: ").strip()
            # Remove quotes if user added them
            if (target_dir.startswith('"') and target_dir.endswith('"')) or (target_dir.startswith("'") and target_dir.endswith("'")):
                 target_dir = target_dir[1:-1]
        except EOFError:
            pass

    if not target_dir:
        print("No directory specified. Exiting.")
        return
    
    # expand user path if needed
    target_dir = os.path.expanduser(target_dir)
    
    # Setup logging relative to where we are running, or maybe in the target dir?
    # Usually log in the script dir is safer if target is unwritable, but let's stick to default.
    setup_logging(args.log_file)
    
    organize_files(target_dir, args.dry_run)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

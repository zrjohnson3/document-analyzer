import os
import shutil
from pathlib import Path

# Define storage directories
UPLOAD_DIR = "storage/uploads"
OUTPUT_DIR = "storage/outputs"

def ensure_storage_dirs():
    """Ensure all storage directories exist"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_file_info(file_path):
    """Get file information including name, size, and type"""
    path = Path(file_path)
    return {
        "name": path.name,
        "path": str(path),
        "size": os.path.getsize(path) if os.path.exists(path) else 0,
        "type": path.suffix.lower().replace('.', '')
    }

def list_uploaded_files():
    """List all uploaded files"""
    ensure_storage_dirs()
    files = []
    
    for file_name in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.isfile(file_path):
            files.append(get_file_info(file_path))
    
    return files

def list_output_files():
    """List all generated output files"""
    ensure_storage_dirs()
    files = []
    
    for file_name in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, file_name)
        if os.path.isfile(file_path):
            files.append(get_file_info(file_path))
    
    return files

def delete_file(file_path):
    """Delete a file from storage"""
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        return True
    return False

def clean_storage(older_than_days=None):
    """Clean storage directories by removing old files"""
    if older_than_days is None:
        # Just ensure directories exist but don't delete anything
        ensure_storage_dirs()
        return
        
    # Implementation would check file creation/modification dates
    # and remove files older than the specified number of days
    # This is a placeholder for future implementation
    pass

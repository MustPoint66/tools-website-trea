import os
import shutil
import uuid
from typing import List, Optional
from fastapi import UploadFile
from app.config import settings

def create_temp_dir(prefix: str = "") -> str:
    """
    Create a temporary directory with a unique name
    
    Args:
        prefix: Optional prefix for the directory name
        
    Returns:
        Path to the created temporary directory
    """
    unique_id = str(uuid.uuid4())
    dir_name = f"{prefix}_{unique_id}" if prefix else unique_id
    temp_dir = os.path.join(settings.TEMP_DIR, dir_name)
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

async def save_upload_file(upload_file: UploadFile, directory: str) -> str:
    """
    Save an uploaded file to the specified directory
    
    Args:
        upload_file: The uploaded file
        directory: Directory to save the file in
        
    Returns:
        Path to the saved file
    """
    file_path = os.path.join(directory, upload_file.filename)
    
    # Read file content
    content = await upload_file.read()
    
    # Write to file
    with open(file_path, "wb") as f:
        f.write(content)
    
    return file_path

async def save_upload_files(upload_files: List[UploadFile], directory: str) -> List[str]:
    """
    Save multiple uploaded files to the specified directory
    
    Args:
        upload_files: List of uploaded files
        directory: Directory to save the files in
        
    Returns:
        List of paths to the saved files
    """
    saved_paths = []
    for upload_file in upload_files:
        file_path = await save_upload_file(upload_file, directory)
        saved_paths.append(file_path)
    
    return saved_paths

def cleanup_directory(directory: str, delete_dir: bool = True) -> None:
    """
    Clean up a directory by removing all files and optionally the directory itself
    
    Args:
        directory: Path to the directory to clean up
        delete_dir: Whether to delete the directory itself
    """
    if os.path.exists(directory):
        # Remove all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        # Remove the directory itself if requested
        if delete_dir:
            os.rmdir(directory)
import os
import uuid
import shutil
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from app.services.conversion_service import convert_file, detect_file_type
from app.utils.file_utils import create_temp_dir, save_upload_file, cleanup_directory

router = APIRouter()

@router.post("/convert", summary="Convert files between different formats")
async def convert_file_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="File to convert"),
    target_format: str = Form(..., description="Target format (pdf, image, text)"),
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Detect source file type
    source_type = detect_file_type(file.filename)
    if source_type == "unknown":
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
    
    # Validate target format
    valid_formats = ["pdf", "image", "text"]
    if target_format not in valid_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported target format. Must be one of: {', '.join(valid_formats)}")
    
    # Check if conversion is supported
    supported_conversions = {
        "word": ["pdf"],
        "excel": ["pdf"],
        "powerpoint": ["pdf"],
        "pdf": ["image", "text"],
        "image": ["pdf"],
        "text": ["pdf"]
    }
    
    if source_type not in supported_conversions or target_format not in supported_conversions.get(source_type, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Conversion from {source_type} to {target_format} is not supported"
        )
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"convert_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Determine output filename and path
    input_filename = os.path.basename(input_path)
    input_name = os.path.splitext(input_filename)[0]
    
    # Set output extension based on target format
    if target_format == "pdf":
        output_ext = ".pdf"
    elif target_format == "image":
        output_ext = ".jpg"  # Default to jpg for images
    elif target_format == "text":
        output_ext = ".txt"
    else:
        output_ext = ".out"  # Generic extension
    
    output_filename = f"{input_name}_converted{output_ext}"
    output_path = os.path.join(temp_dir, output_filename)
    
    # Convert file
    try:
        success = convert_file(input_path, output_path, target_format)
        if not success:
            raise HTTPException(status_code=500, detail="File conversion failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")
    
    # Special case for PDF to images - return a zip file with all images
    if source_type == "pdf" and target_format == "image":
        # Create a zip file with all images
        import zipfile
        zip_path = os.path.join(temp_dir, f"{input_name}_images.zip")
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(temp_dir):
                if file.startswith("page_") and file.endswith(".jpg"):
                    file_path = os.path.join(temp_dir, file)
                    zipf.write(file_path, arcname=file)
        
        # Schedule cleanup after response is sent
        background_tasks.add_task(cleanup_directory, temp_dir)
        
        return FileResponse(
            path=zip_path,
            filename=f"{input_name}_images.zip",
            media_type="application/zip",
            background=background_tasks
        )
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    # Determine media type for response
    if target_format == "pdf":
        media_type = "application/pdf"
    elif target_format == "image":
        media_type = "image/jpeg"
    elif target_format == "text":
        media_type = "text/plain"
    else:
        media_type = "application/octet-stream"
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type=media_type,
        background=background_tasks
    )
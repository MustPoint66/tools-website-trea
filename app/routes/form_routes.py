import os
import uuid
import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Query, Body
from fastapi.responses import FileResponse, JSONResponse
from app.services.form_service import detect_form_fields, fill_form, get_form_preview, update_profile
from app.utils.file_utils import create_temp_dir, save_upload_file, cleanup_directory

router = APIRouter()

@router.post("/detect", summary="Detect form fields in a PDF")
async def detect_form_fields_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF form to analyze"),
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext != ".pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"form_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Detect form fields
    fields = detect_form_fields(input_path)
    
    # Schedule cleanup of temp directory
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return JSONResponse(
        content={
            "message": "Form fields detected successfully",
            "fields": fields
        },
        status_code=200
    )

@router.post("/preview", summary="Get a preview of how the form would be filled")
async def preview_form_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF form to preview"),
    field_values: Optional[str] = Form(None, description="JSON string of field values to override defaults"),
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext != ".pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Parse field values if provided
    values_dict = {}
    if field_values:
        try:
            values_dict = json.loads(field_values)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in field_values")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"form_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Get form preview
    preview = get_form_preview(input_path, values_dict)
    
    # Schedule cleanup of temp directory
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return JSONResponse(
        content=preview,
        status_code=200
    )

@router.post("/fill", summary="Fill a PDF form with provided values")
async def fill_form_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF form to fill"),
    field_values: Optional[str] = Form(None, description="JSON string of field values to override defaults"),
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext != ".pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Parse field values if provided
    values_dict = {}
    if field_values:
        try:
            values_dict = json.loads(field_values)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in field_values")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"form_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Determine output filename and path
    input_filename = os.path.basename(input_path)
    input_name = os.path.splitext(input_filename)[0]
    output_filename = f"{input_name}_filled.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    # Fill the form
    success = fill_form(input_path, output_path, values_dict)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to fill form")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )

@router.put("/profile", summary="Update the default profile for form filling")
async def update_profile_endpoint(
    profile_data: Dict[str, Dict[str, str]] = Body(..., description="Profile data to update"),
):
    # Update the profile
    success = update_profile(profile_data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update profile")
    
    return JSONResponse(
        content={
            "message": "Profile updated successfully"
        },
        status_code=200
    )
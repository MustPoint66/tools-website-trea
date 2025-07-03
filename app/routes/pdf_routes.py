from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks, Form, Query, Path, Body
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional, Dict, Any, Tuple
import os
import uuid
import shutil
import fitz  # PyMuPDF
import asyncio
import time
import json
from datetime import datetime, timedelta
from app.config import settings
from app.services.pdf_service import (
    merge_pdfs, split_pdf, split_pdf_by_page_count, rotate_pdf,
    add_watermark, add_image_watermark, crop_pdf, compress_pdf
)
from app.utils.file_utils import create_temp_dir, save_upload_file, save_upload_files, cleanup_directory

router = APIRouter()

# In-memory storage for task progress (use Redis in production)
task_progress: Dict[str, Dict[str, Any]] = {}
task_results: Dict[str, Dict[str, Any]] = {}

def update_task_progress(task_id: str, progress: int, status: str, message: str = ""):
    """Update task progress"""
    task_progress[task_id] = {
        "progress": progress,
        "status": status,
        "message": message,
        "updated_at": datetime.now()
    }

def store_task_result(task_id: str, file_path: str, filename: str, media_type: str):
    """Store task result for later download"""
    task_results[task_id] = {
        "file_path": file_path,
        "filename": filename,
        "media_type": media_type,
        "created_at": datetime.now()
    }

def cleanup_old_tasks():
    """Clean up old task data (older than 1 hour)"""
    cutoff_time = datetime.now() - timedelta(hours=1)
    
    # Clean progress data
    expired_progress = [task_id for task_id, data in task_progress.items() 
                       if data.get("updated_at", datetime.min) < cutoff_time]
    for task_id in expired_progress:
        del task_progress[task_id]
    
    # Clean result data and files
    expired_results = [task_id for task_id, data in task_results.items() 
                      if data.get("created_at", datetime.min) < cutoff_time]
    for task_id in expired_results:
        result = task_results[task_id]
        if os.path.exists(result["file_path"]):
            try:
                os.remove(result["file_path"])
            except Exception:
                pass
        del task_results[task_id]

@router.post("/merge", summary="Merge multiple PDF files into one")
async def merge_pdf_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(..., description="Multiple PDF files to merge")
):
    # Validate files
    if not files or len(files) < 2:
        raise HTTPException(status_code=400, detail="At least 2 PDF files are required")
    
    # Check file types
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = os.path.join(settings.TEMP_DIR, operation_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save uploaded files to temp directory
    input_paths = []
    for file in files:
        temp_file_path = os.path.join(temp_dir, file.filename)
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        input_paths.append(temp_file_path)
    
    # Merge PDFs
    output_path = os.path.join(temp_dir, "merged.pdf")
    merge_pdfs(input_paths, output_path)
    
    # Schedule cleanup after response is sent
    def cleanup_temp_files():
        for file_path in input_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    
    background_tasks.add_task(cleanup_temp_files)
    
    return FileResponse(
        path=output_path,
        filename="merged.pdf",
        media_type="application/pdf",
        background=background_tasks
    )


@router.post("/split", summary="Split a PDF file into multiple PDFs")
async def split_pdf_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to split"),
    split_type: str = Form("page", description="Split type: 'page' (each page) or 'range' (page ranges)"),
    page_ranges: Optional[str] = Form(None, description="Page ranges in format '1-3,5-7' (0-indexed)"),
    pages_per_file: Optional[int] = Form(None, description="Number of pages per output file")
):
    # Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"split_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Create output directory
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Process based on split type
    if split_type == "range" and page_ranges:
        # Parse page ranges
        ranges = []
        for range_str in page_ranges.split(","):
            if "-" in range_str:
                start, end = map(int, range_str.split("-"))
                ranges.append((start, end))
            else:
                page = int(range_str)
                ranges.append((page, page))
        
        # Split PDF by ranges
        output_paths = split_pdf(input_path, output_dir, ranges)
    elif split_type == "count" and pages_per_file and pages_per_file > 0:
        # Split PDF by page count
        output_paths = split_pdf_by_page_count(input_path, output_dir, pages_per_file)
    else:
        # Default: split into individual pages
        output_paths = split_pdf(input_path, output_dir)
    
    # Create a zip file with all split PDFs
    import zipfile
    zip_path = os.path.join(temp_dir, "split_pdfs.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for output_path in output_paths:
            zipf.write(output_path, os.path.basename(output_path))
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=zip_path,
        filename="split_pdfs.zip",
        media_type="application/zip",
        background=background_tasks
    )


@router.post("/rotate", summary="Rotate pages in a PDF file")
async def rotate_pdf_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to rotate"),
    rotation: int = Form(..., description="Rotation angle in degrees (90, 180, 270)"),
    page_numbers: Optional[str] = Form(None, description="Page numbers to rotate (0-indexed, comma-separated)")
):
    # Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Validate rotation angle
    if rotation not in [90, 180, 270]:
        raise HTTPException(status_code=400, detail="Rotation angle must be 90, 180, or 270 degrees")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"rotate_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Parse page numbers if provided
    pages_to_rotate = None
    if page_numbers:
        try:
            pages_to_rotate = [int(p.strip()) for p in page_numbers.split(",") if p.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid page numbers format")
    
    # Rotate PDF
    output_filename = f"rotated_{os.path.basename(file.filename)}"
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        rotate_pdf(input_path, output_path, rotation, pages_to_rotate)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rotating PDF: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )



@router.post("/crop", summary="Crop a PDF file")
async def crop_pdf_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to crop"),
    left: float = Form(..., description="Left margin in points (1/72 inch)"),
    bottom: float = Form(..., description="Bottom margin in points (1/72 inch)"),
    right: float = Form(..., description="Right margin in points (1/72 inch)"),
    top: float = Form(..., description="Top margin in points (1/72 inch)"),
    page_numbers: Optional[str] = Form(None, description="Page numbers to crop (0-indexed, comma-separated)")
):
    # Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Validate crop box values
    if left < 0 or bottom < 0 or right < 0 or top < 0:
        raise HTTPException(status_code=400, detail="Crop margins must be non-negative")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"crop_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Parse page numbers if provided
    pages_to_crop = None
    if page_numbers:
        try:
            pages_to_crop = [int(p.strip()) for p in page_numbers.split(",") if p.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid page numbers format")
    
    # Crop PDF
    output_filename = f"cropped_{os.path.basename(file.filename)}"
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        # Create crop box tuple (left, bottom, right, top)
        crop_box = (left, bottom, right, top)
        crop_pdf(input_path, output_path, crop_box, pages_to_crop)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cropping PDF: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )

@router.post("/compress", summary="Compress a PDF file")
async def compress_pdf_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to compress"),
    compression_level: str = Form("medium", description="Compression level (low, medium, high)")
):
    # Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Validate compression level
    valid_levels = ["low", "medium", "high"]
    if compression_level not in valid_levels:
        raise HTTPException(status_code=400, detail=f"Compression level must be one of: {', '.join(valid_levels)}")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"compress_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Compress PDF
    output_filename = f"compressed_{os.path.basename(file.filename)}"
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        compress_pdf(input_path, output_path, compression_level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error compressing PDF: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )

@router.post("/watermark/text", summary="Add text watermark to a PDF file")
async def add_text_watermark(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to watermark"),
    watermark_text: str = Form(..., description="Text to use as watermark"),
    opacity: float = Form(0.5, description="Opacity of the watermark (0.0 to 1.0)"),
    font_size: int = Form(20, description="Font size for the watermark text"),
    page_numbers: Optional[str] = Form(None, description="Page numbers to watermark (0-indexed, comma-separated)")
):
    # Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Validate opacity
    if not 0.0 <= opacity <= 1.0:
        raise HTTPException(status_code=400, detail="Opacity must be between 0.0 and 1.0")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"watermark_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Parse page numbers if provided
    pages_to_watermark = None
    if page_numbers:
        try:
            pages_to_watermark = [int(p.strip()) for p in page_numbers.split(",") if p.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid page numbers format")
    
    # Add watermark
    output_filename = f"watermarked_{os.path.basename(file.filename)}"
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        add_watermark(
            input_path, 
            output_path, 
            watermark_text, 
            opacity, 
            font_size, 
            (0.5, 0.5, 0.5),  # Default gray color
            pages_to_watermark
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding watermark: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )


@router.post("/watermark/image", summary="Add image watermark to a PDF file")
async def add_image_watermark_route(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to watermark"),
    watermark_image: UploadFile = File(..., description="Image to use as watermark"),
    opacity: float = Form(0.5, description="Opacity of the watermark (0.0 to 1.0)"),
    scale: float = Form(0.3, description="Scale factor for the watermark image"),
    position: str = Form("center", description="Position of the watermark (center, top-left, top-right, bottom-left, bottom-right)"),
    page_numbers: Optional[str] = Form(None, description="Page numbers to watermark (0-indexed, comma-separated)")
):
    # Validate files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Validate image file
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".pdf"]
    if not any(watermark_image.filename.lower().endswith(ext) for ext in valid_image_extensions):
        raise HTTPException(status_code=400, detail=f"Watermark file {watermark_image.filename} is not a supported image format")
    
    # Validate opacity and scale
    if not 0.0 <= opacity <= 1.0:
        raise HTTPException(status_code=400, detail="Opacity must be between 0.0 and 1.0")
    if not 0.0 < scale <= 1.0:
        raise HTTPException(status_code=400, detail="Scale must be between 0.0 and 1.0")
    
    # Validate position
    valid_positions = ["center", "top-left", "top-right", "bottom-left", "bottom-right"]
    if position not in valid_positions:
        raise HTTPException(status_code=400, detail=f"Position must be one of: {', '.join(valid_positions)}")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"watermark_img_{operation_id}")
    
    # Save uploaded files to temp directory
    input_path = await save_upload_file(file, temp_dir)
    watermark_path = await save_upload_file(watermark_image, temp_dir)
    
    # Parse page numbers if provided
    pages_to_watermark = None
    if page_numbers:
        try:
            pages_to_watermark = [int(p.strip()) for p in page_numbers.split(",") if p.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid page numbers format")
    
    # Add watermark
    output_filename = f"watermarked_{os.path.basename(file.filename)}"
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        add_image_watermark(
            input_path, 
            output_path, 
            watermark_path, 
            opacity, 
            scale, 
            position, 
            pages_to_watermark
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding image watermark: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )


# Progress tracking endpoints
@router.get("/progress/{task_id}", summary="Get task progress")
async def get_task_progress(task_id: str):
    """Get the progress of a specific task"""
    # Clean up old tasks first
    cleanup_old_tasks()
    
    if task_id not in task_progress:
        raise HTTPException(status_code=404, detail="Task not found")
    
    progress_data = task_progress[task_id]
    return JSONResponse(content={
        "task_id": task_id,
        "progress": progress_data["progress"],
        "status": progress_data["status"],
        "message": progress_data["message"],
        "updated_at": progress_data["updated_at"].isoformat()
    })


@router.get("/download/{task_id}", summary="Download processed file")
async def download_task_result(task_id: str, background_tasks: BackgroundTasks):
    """Download the result file for a completed task"""
    # Clean up old tasks first
    cleanup_old_tasks()
    
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Task result not found or expired")
    
    result = task_results[task_id]
    file_path = result["file_path"]
    
    if not os.path.exists(file_path):
        # Remove the expired entry
        del task_results[task_id]
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    # Schedule cleanup of this specific file after download
    def cleanup_file():
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            # Remove from results after successful download
            if task_id in task_results:
                del task_results[task_id]
        except Exception:
            pass
    
    background_tasks.add_task(cleanup_file)
    
    return FileResponse(
        path=file_path,
        filename=result["filename"],
        media_type=result["media_type"],
        background=background_tasks
    )


# Enhanced operations with progress tracking
async def process_pdf_with_progress(
    task_id: str,
    operation: str,
    files: List[UploadFile],
    options: Dict[str, Any] = None
):
    """Process PDF with progress tracking"""
    try:
        update_task_progress(task_id, 10, "processing", "Starting processing...")
        
        # Create temp directory
        temp_dir = os.path.join(settings.TEMP_DIR, task_id)
        os.makedirs(temp_dir, exist_ok=True)
        
        update_task_progress(task_id, 20, "processing", "Saving uploaded files...")
        
        # Save uploaded files
        input_paths = []
        for i, file in enumerate(files):
            temp_file_path = os.path.join(temp_dir, file.filename)
            with open(temp_file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            input_paths.append(temp_file_path)
            
            # Update progress for file saving
            progress = 20 + (i + 1) * 20 // len(files)
            update_task_progress(task_id, progress, "processing", f"Saved {i + 1}/{len(files)} files")
        
        # Process based on operation
        output_path = None
        output_filename = None
        media_type = "application/pdf"
        
        if operation == "merge":
            update_task_progress(task_id, 60, "processing", "Merging PDFs...")
            output_path = os.path.join(temp_dir, "merged.pdf")
            output_filename = "merged.pdf"
            merge_pdfs(input_paths, output_path)
            
        elif operation == "compress":
            update_task_progress(task_id, 60, "processing", "Compressing PDF...")
            compression_level = options.get("compressionLevel", "medium")
            output_filename = f"compressed_{files[0].filename}"
            output_path = os.path.join(temp_dir, output_filename)
            compress_pdf(input_paths[0], output_path, compression_level)
            
        elif operation == "split":
            update_task_progress(task_id, 60, "processing", "Splitting PDF...")
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(output_dir, exist_ok=True)
            
            split_mode = options.get("splitMode", "pages")
            if split_mode == "pages" and options.get("splitPages"):
                ranges = [(p, p) for p in options["splitPages"]]
                output_paths = split_pdf(input_paths[0], output_dir, ranges)
            else:
                output_paths = split_pdf(input_paths[0], output_dir)
            
            # Create zip file
            import zipfile
            output_path = os.path.join(temp_dir, "split_pdfs.zip")
            output_filename = "split_pdfs.zip"
            media_type = "application/zip"
            
            with zipfile.ZipFile(output_path, "w") as zipf:
                for path in output_paths:
                    zipf.write(path, os.path.basename(path))
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported operation: {operation}")
        
        update_task_progress(task_id, 90, "processing", "Finalizing...")
        
        # Store result for download
        store_task_result(task_id, output_path, output_filename, media_type)
        
        update_task_progress(task_id, 100, "completed", "Processing completed successfully")
        
        return {
            "task_id": task_id,
            "status": "completed",
            "message": "Processing completed successfully"
        }
        
    except Exception as e:
        update_task_progress(task_id, 0, "error", str(e))
        # Clean up temp directory on error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{operation}", summary="Process PDF with progress tracking")
async def process_pdf_operation(
    operation: str,
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    task_id: Optional[str] = Form(None),
    options: Optional[str] = Form(None)
):
    """Generic PDF processing endpoint with progress tracking"""
    # Generate task ID if not provided
    if not task_id:
        task_id = f"task_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    
    # Parse options
    parsed_options = {}
    if options:
        try:
            parsed_options = json.loads(options)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid options JSON")
    
    # Validate operation
    valid_operations = ["merge", "split", "compress", "rotate", "crop"]
    if operation not in valid_operations:
        raise HTTPException(status_code=400, detail=f"Unsupported operation: {operation}")
    
    # Validate files
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    # Start processing in background
    background_tasks.add_task(
        process_pdf_with_progress,
        task_id,
        operation,
        files,
        parsed_options
    )
    
    # Initialize progress tracking
    update_task_progress(task_id, 0, "processing", "Task started")
    
    return JSONResponse(content={
        "task_id": task_id,
        "status": "processing",
        "message": "Task started successfully"
    })



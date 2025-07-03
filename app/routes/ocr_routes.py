import os
import uuid
import shutil
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from app.services.ocr_service import ocr_image, ocr_pdf, save_text_to_file
from app.utils.file_utils import create_temp_dir, save_upload_file, cleanup_directory

router = APIRouter()

@router.post("/ocr/image", summary="Perform OCR on an image")
async def ocr_image_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Image file to OCR"),
    output_format: str = Form("txt", description="Output format (txt or docx)"),
    ocr_engine: str = Form("tesseract", description="OCR engine to use (tesseract or easyocr)"),
    language: str = Form("eng", description="Language for OCR"),
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file extension
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in valid_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Must be one of: {', '.join(valid_extensions)}"
        )
    
    # Validate output format
    if output_format not in ["txt", "docx"]:
        raise HTTPException(status_code=400, detail="Output format must be 'txt' or 'docx'")
    
    # Validate OCR engine
    if ocr_engine not in ["tesseract", "easyocr"]:
        raise HTTPException(status_code=400, detail="OCR engine must be 'tesseract' or 'easyocr'")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"ocr_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Perform OCR
    try:
        extracted_text = ocr_image(input_path, engine=ocr_engine, lang=language)
        if not extracted_text:
            raise HTTPException(status_code=500, detail="OCR failed to extract text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing OCR: {str(e)}")
    
    # Determine output filename and path
    input_filename = os.path.basename(input_path)
    input_name = os.path.splitext(input_filename)[0]
    output_filename = f"{input_name}_ocr.{output_format}"
    output_path = os.path.join(temp_dir, output_filename)
    
    # Save extracted text to file
    try:
        save_text_to_file(extracted_text, output_path, format=output_format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving OCR result: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    # Determine media type for response
    if output_format == "txt":
        media_type = "text/plain"
    else:  # docx
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type=media_type,
        background=background_tasks
    )

@router.post("/ocr/pdf", summary="Perform OCR on a PDF")
async def ocr_pdf_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to OCR"),
    output_format: str = Form("txt", description="Output format (txt or docx)"),
    ocr_engine: str = Form("tesseract", description="OCR engine to use (tesseract or easyocr)"),
    language: str = Form("eng", description="Language for OCR"),
    pages: Optional[str] = Form(None, description="Pages to OCR (e.g., '1,3-5,7'). Leave empty for all pages."),
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext != ".pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Validate output format
    if output_format not in ["txt", "docx"]:
        raise HTTPException(status_code=400, detail="Output format must be 'txt' or 'docx'")
    
    # Validate OCR engine
    if ocr_engine not in ["tesseract", "easyocr"]:
        raise HTTPException(status_code=400, detail="OCR engine must be 'tesseract' or 'easyocr'")
    
    # Parse page numbers if provided
    page_numbers = None
    if pages:
        try:
            page_numbers = []
            for part in pages.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    page_numbers.extend(range(start, end + 1))
                else:
                    page_numbers.append(int(part))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid page format. Use format like '1,3-5,7'")
    
    # Generate unique ID for this operation
    operation_id = str(uuid.uuid4())
    temp_dir = create_temp_dir(f"ocr_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Perform OCR
    try:
        extracted_text = ocr_pdf(input_path, pages=page_numbers, engine=ocr_engine, lang=language)
        if not extracted_text:
            raise HTTPException(status_code=500, detail="OCR failed to extract text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing OCR: {str(e)}")
    
    # Determine output filename and path
    input_filename = os.path.basename(input_path)
    input_name = os.path.splitext(input_filename)[0]
    output_filename = f"{input_name}_ocr.{output_format}"
    output_path = os.path.join(temp_dir, output_filename)
    
    # Save extracted text to file
    try:
        save_text_to_file(extracted_text, output_path, format=output_format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving OCR result: {str(e)}")
    
    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    # Determine media type for response
    if output_format == "txt":
        media_type = "text/plain"
    else:  # docx
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type=media_type,
        background=background_tasks
    )
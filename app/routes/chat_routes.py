import os
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Query, Body
from fastapi.responses import FileResponse, JSONResponse
from app.services.chat_service import process_pdf_for_chat, query_pdf, list_available_pdfs, delete_pdf_index
from app.utils.file_utils import create_temp_dir, save_upload_file, cleanup_directory

router = APIRouter()

@router.post("/upload", summary="Upload a PDF for chat")
async def upload_pdf_for_chat(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to process for chat"),
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
    temp_dir = create_temp_dir(f"chat_{operation_id}")
    
    # Save uploaded file to temp directory
    input_path = await save_upload_file(file, temp_dir)
    
    # Process PDF for chat
    pdf_id = process_pdf_for_chat(input_path)
    if not pdf_id:
        raise HTTPException(status_code=500, detail="Failed to process PDF for chat")
    
    # Schedule cleanup of temp directory
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return JSONResponse(
        content={
            "message": "PDF processed successfully",
            "pdf_id": pdf_id
        },
        status_code=200
    )

@router.post("/query", summary="Query a PDF with a question")
async def query_pdf_endpoint(
    pdf_id: str = Form(..., description="ID of the PDF to query"),
    question: str = Form(..., description="Question to ask about the PDF"),
):
    # Validate inputs
    if not pdf_id:
        raise HTTPException(status_code=400, detail="PDF ID is required")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    
    # Query the PDF
    result = query_pdf(pdf_id, question)
    
    return JSONResponse(
        content=result,
        status_code=200
    )

@router.get("/list", summary="List available PDFs for chat")
async def list_pdfs_endpoint():
    # Get list of available PDFs
    pdfs = list_available_pdfs()
    
    return JSONResponse(
        content={
            "pdfs": pdfs
        },
        status_code=200
    )

@router.delete("/delete/{pdf_id}", summary="Delete a PDF from chat")
async def delete_pdf_endpoint(
    pdf_id: str,
):
    # Validate input
    if not pdf_id:
        raise HTTPException(status_code=400, detail="PDF ID is required")
    
    # Delete the PDF
    success = delete_pdf_index(pdf_id)
    if not success:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return JSONResponse(
        content={
            "message": "PDF deleted successfully"
        },
        status_code=200
    )
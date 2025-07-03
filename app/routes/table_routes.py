import os
import uuid
import shutil
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.services.table_service import (
    extract_tables,
    clean_table,
    save_tables_to_excel,
    get_table_preview,
    merge_tables
)
from app.config import settings

router = APIRouter()

# Models for request/response
class TableExtractionRequest(BaseModel):
    methods: List[str] = ['pdfplumber', 'tabula', 'camelot']

class TablePreview(BaseModel):
    metadata: Dict[str, Any]
    columns: List[str]
    preview_rows: List[List[Any]]
    total_rows: int

class TableExtractionResponse(BaseModel):
    job_id: str
    tables: Dict[str, List[TablePreview]]
    total_tables: int

class TableCleanupRequest(BaseModel):
    job_id: str
    selected_tables: List[Dict[str, Any]]

# In-memory storage for extracted tables
table_storage = {}

@router.post("/extract", response_model=TableExtractionResponse)
async def extract_tables_from_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    methods: List[str] = Query(['pdfplumber', 'tabula', 'camelot'])
):
    """
    Extract tables from a PDF file using specified methods.
    
    Returns previews of all extracted tables.
    """
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Create a unique job ID
    job_id = str(uuid.uuid4())
    
    # Save the uploaded file
    temp_dir = os.path.join(settings.TEMP_DIR, job_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract tables using specified methods
    tables_dict = extract_tables(file_path, methods=methods)
    
    # Generate previews for all tables
    previews = {}
    total_tables = 0
    
    for method, tables in tables_dict.items():
        previews[method] = []
        for table in tables:
            # Clean the table
            cleaned_table = clean_table(table)
            # Generate preview
            preview = get_table_preview(cleaned_table)
            previews[method].append(preview)
            total_tables += 1
    
    # Store tables in memory
    table_storage[job_id] = {
        'tables_dict': tables_dict,
        'file_path': file_path
    }
    
    # Schedule cleanup of temporary files
    background_tasks.add_task(cleanup_temp_files, temp_dir, job_id, 3600)  # Cleanup after 1 hour
    
    return {
        "job_id": job_id,
        "tables": previews,
        "total_tables": total_tables
    }

@router.post("/download")
async def download_tables_as_excel(
    request: TableCleanupRequest,
    background_tasks: BackgroundTasks
):
    """
    Download selected tables as an Excel file.
    
    The request should include the job_id and a list of selected tables.
    Each selected table should have method, page, and table_index.
    """
    job_id = request.job_id
    
    # Check if job exists
    if job_id not in table_storage:
        raise HTTPException(status_code=404, detail="Job not found or expired")
    
    job_data = table_storage[job_id]
    tables_dict = job_data['tables_dict']
    
    # Collect selected tables
    selected_dfs = []
    
    for selection in request.selected_tables:
        method = selection.get('method')
        page = selection.get('page')
        table_index = selection.get('table_index')
        
        if method not in tables_dict:
            continue
        
        # Find the matching table
        for table in tables_dict[method]:
            table_page = table.attrs.get('page')
            table_idx = table.attrs.get('table_index')
            
            if (table_page == page and table_idx == table_index):
                # Clean the table before adding
                cleaned_table = clean_table(table)
                selected_dfs.append(cleaned_table)
                break
    
    if not selected_dfs:
        raise HTTPException(status_code=400, detail="No valid tables selected")
    
    # Create Excel file
    excel_path = os.path.join(settings.TEMP_DIR, f"{job_id}_tables.xlsx")
    save_tables_to_excel(selected_dfs, excel_path)
    
    # Schedule cleanup of Excel file
    background_tasks.add_task(cleanup_excel_file, excel_path, 300)  # Cleanup after 5 minutes
    
    return FileResponse(
        path=excel_path,
        filename="extracted_tables.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/merge")
async def merge_selected_tables(
    request: TableCleanupRequest,
    background_tasks: BackgroundTasks
):
    """
    Merge selected tables into a single Excel file.
    
    The request should include the job_id and a list of selected tables.
    Each selected table should have method, page, and table_index.
    """
    job_id = request.job_id
    
    # Check if job exists
    if job_id not in table_storage:
        raise HTTPException(status_code=404, detail="Job not found or expired")
    
    job_data = table_storage[job_id]
    tables_dict = job_data['tables_dict']
    
    # Collect selected tables
    selected_dfs = []
    
    for selection in request.selected_tables:
        method = selection.get('method')
        page = selection.get('page')
        table_index = selection.get('table_index')
        
        if method not in tables_dict:
            continue
        
        # Find the matching table
        for table in tables_dict[method]:
            table_page = table.attrs.get('page')
            table_idx = table.attrs.get('table_index')
            
            if (table_page == page and table_idx == table_index):
                # Clean the table before adding
                cleaned_table = clean_table(table)
                selected_dfs.append(cleaned_table)
                break
    
    if not selected_dfs:
        raise HTTPException(status_code=400, detail="No valid tables selected")
    
    # Merge tables
    merged_df = merge_tables(selected_dfs)
    
    # Create Excel file with merged table
    excel_path = os.path.join(settings.TEMP_DIR, f"{job_id}_merged.xlsx")
    merged_df.to_excel(excel_path, index=False)
    
    # Schedule cleanup of Excel file
    background_tasks.add_task(cleanup_excel_file, excel_path, 300)  # Cleanup after 5 minutes
    
    return FileResponse(
        path=excel_path,
        filename="merged_table.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.delete("/cleanup/{job_id}")
async def cleanup_job(job_id: str):
    """
    Clean up resources associated with a job.
    """
    if job_id in table_storage:
        job_data = table_storage[job_id]
        file_path = job_data['file_path']
        
        # Remove from storage
        del table_storage[job_id]
        
        # Delete temporary directory
        temp_dir = os.path.dirname(file_path)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return {"status": "success", "message": "Job cleaned up successfully"}
    
    return {"status": "not_found", "message": "Job not found or already cleaned up"}

def cleanup_temp_files(temp_dir: str, job_id: str, delay: int = 3600):
    """
    Background task to clean up temporary files after a delay.
    """
    import time
    import asyncio
    
    # Wait for the specified delay
    time.sleep(delay)
    
    # Remove from storage
    if job_id in table_storage:
        del table_storage[job_id]
    
    # Delete temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

def cleanup_excel_file(file_path: str, delay: int = 300):
    """
    Background task to clean up Excel file after a delay.
    """
    import time
    
    # Wait for the specified delay
    time.sleep(delay)
    
    # Delete file
    if os.path.exists(file_path):
        os.remove(file_path)
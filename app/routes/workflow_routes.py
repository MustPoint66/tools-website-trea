import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Body
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.services.workflow_service import (
    execute_workflow,
    validate_workflow,
    get_available_tools
)
from app.config import settings

router = APIRouter()

# Models for request/response
class WorkflowStep(BaseModel):
    tool: str
    params: Dict[str, Any] = {}

class WorkflowRequest(BaseModel):
    steps: List[WorkflowStep]

class WorkflowResponse(BaseModel):
    job_id: str
    output_path: str
    steps_executed: int

class WorkflowValidationResponse(BaseModel):
    is_valid: bool
    error_message: Optional[str] = None

@router.post("/execute", response_model=WorkflowResponse)
async def execute_workflow_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    workflow: str = Form(...)
):
    """
    Execute a workflow on a PDF document.
    
    The workflow should be a JSON string representing a list of steps.
    Each step should have a 'tool' field and an optional 'params' field.
    """
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Parse workflow JSON
    try:
        import json
        workflow_steps = json.loads(workflow)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid workflow JSON")
    
    # Validate workflow
    is_valid, error_message = validate_workflow(workflow_steps)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Create a unique job ID
    job_id = str(uuid.uuid4())
    
    # Save the uploaded file
    temp_dir = os.path.join(settings.TEMP_DIR, job_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Execute the workflow
        output_path = execute_workflow(input_path, workflow_steps)
        
        # Schedule cleanup of temporary files
        background_tasks.add_task(cleanup_temp_files, temp_dir, output_path, 3600)  # Cleanup after 1 hour
        
        return {
            "job_id": job_id,
            "output_path": output_path,
            "steps_executed": len(workflow_steps)
        }
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate", response_model=WorkflowValidationResponse)
async def validate_workflow_endpoint(workflow: List[Dict[str, Any]] = Body(...)):
    """
    Validate a workflow definition without executing it.
    """
    is_valid, error_message = validate_workflow(workflow)
    
    return {
        "is_valid": is_valid,
        "error_message": error_message if not is_valid else None
    }

@router.get("/tools")
async def get_tools():
    """
    Get information about available tools.
    """
    return get_available_tools()

@router.get("/download/{job_id}")
async def download_workflow_result(job_id: str, background_tasks: BackgroundTasks):
    """
    Download the result of a workflow execution.
    """
    # Construct the expected output path
    temp_dir = os.path.join(settings.TEMP_DIR, job_id)
    
    # Find the output file (should be a PDF)
    output_files = [f for f in os.listdir(temp_dir) if f.endswith('.pdf') and f != 'input.pdf']
    
    if not output_files:
        raise HTTPException(status_code=404, detail="Workflow result not found or expired")
    
    output_path = os.path.join(temp_dir, output_files[0])
    
    # Schedule cleanup of the file after download
    background_tasks.add_task(cleanup_file, output_path, 300)  # Cleanup after 5 minutes
    
    return FileResponse(
        path=output_path,
        filename=f"workflow_result_{job_id}.pdf",
        media_type="application/pdf"
    )

def cleanup_temp_files(temp_dir: str, output_path: str, delay: int = 3600):
    """
    Background task to clean up temporary files after a delay.
    """
    import time
    
    # Wait for the specified delay
    time.sleep(delay)
    
    # Delete temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

def cleanup_file(file_path: str, delay: int = 300):
    """
    Background task to clean up a file after a delay.
    """
    import time
    
    # Wait for the specified delay
    time.sleep(delay)
    
    # Delete file
    if os.path.exists(file_path):
        os.remove(file_path)
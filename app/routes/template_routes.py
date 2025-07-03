from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks, Query
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Dict, Any, Optional
import os
import json
import shutil
from pydantic import BaseModel

from app.services.template_service import (
    get_all_templates,
    get_templates_by_category,
    get_template_by_id,
    get_template_categories,
    get_template_fields,
    fill_template,
    add_template,
    delete_template,
    search_templates,
    get_template_path,
    TEMPLATES_DIR
)
from app.utils.file_utils import save_upload_file, create_temp_dir, cleanup_directory
from app.config import settings

router = APIRouter(prefix="/templates", tags=["templates"])

# Pydantic models for request/response validation
class TemplateBase(BaseModel):
    name: str
    description: str
    category: str
    tags: List[str]

class TemplateResponse(TemplateBase):
    template_id: str
    preview_image: str
    file_path: str

class TemplateFieldValue(BaseModel):
    field_name: str
    value: str

class TemplateFillRequest(BaseModel):
    template_id: str
    field_values: Dict[str, str]

class TemplateSearchRequest(BaseModel):
    query: str

@router.get("/categories", response_model=Dict[str, str])
async def get_categories():
    """Get all template categories."""
    return get_template_categories()

@router.get("/", response_model=List[Dict[str, Any]])
async def list_templates(category: Optional[str] = None, query: Optional[str] = None):
    """List all templates, optionally filtered by category or search query."""
    if query:
        return search_templates(query)
    elif category:
        return get_templates_by_category(category)
    else:
        return get_all_templates()

@router.get("/{template_id}", response_model=Dict[str, Any])
async def get_template(template_id: str):
    """Get a specific template by ID."""
    template = get_template_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.get("/{template_id}/fields", response_model=List[Dict[str, Any]])
async def get_fields(template_id: str):
    """Get form fields for a specific template."""
    fields = get_template_fields(template_id)
    if not fields:
        raise HTTPException(status_code=404, detail="Template not found or has no fields")
    return fields

@router.get("/{template_id}/preview")
async def get_template_preview(template_id: str):
    """Get the preview image for a template."""
    template = get_template_by_id(template_id)
    if not template or not template["preview_image"]:
        raise HTTPException(status_code=404, detail="Template preview not found")
    
    preview_path = os.path.join(TEMPLATES_DIR, template["preview_image"])
    if not os.path.exists(preview_path):
        raise HTTPException(status_code=404, detail="Template preview file not found")
    
    return FileResponse(preview_path)

@router.get("/{template_id}/download")
async def download_template(template_id: str):
    """Download the original template file."""
    template_path = get_template_path(template_id)
    if not template_path or not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    return FileResponse(
        path=template_path,
        filename=os.path.basename(template_path),
        media_type="application/pdf"
    )

@router.post("/fill")
async def fill_template_endpoint(request: TemplateFillRequest, background_tasks: BackgroundTasks):
    """Fill a template with provided values and return the filled PDF."""
    # Create a temporary directory for the output
    temp_dir = create_temp_dir()
    output_filename = f"filled_{request.template_id}.pdf"
    output_path = os.path.join(temp_dir, output_filename)
    
    # Fill the template
    success = fill_template(request.template_id, request.field_values, output_path)
    if not success:
        cleanup_directory(temp_dir)
        raise HTTPException(status_code=404, detail="Failed to fill template")
    
    # Schedule cleanup
    background_tasks.add_task(cleanup_directory, temp_dir)
    
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/pdf",
        background=background_tasks
    )

@router.post("/add", response_model=Dict[str, str])
async def add_template_endpoint(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    tags: str = Form(...),  # Comma-separated tags
    template_file: UploadFile = File(...),
    preview_image: Optional[UploadFile] = File(None)
):
    """Add a new template to the collection."""
    # Create a temporary directory for processing
    temp_dir = create_temp_dir()
    
    try:
        # Save the uploaded template file
        template_path = os.path.join(temp_dir, template_file.filename)
        with open(template_path, "wb") as f:
            f.write(template_file.file.read())
        
        # Save the preview image if provided
        preview_path = None
        if preview_image:
            preview_path = os.path.join(temp_dir, preview_image.filename)
            with open(preview_path, "wb") as f:
                f.write(preview_image.file.read())
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        # Add the template
        template_id = add_template(
            name=name,
            description=description,
            category=category,
            tags=tag_list,
            file_path=template_path,
            preview_image_path=preview_path
        )
        
        return {"template_id": template_id, "status": "success"}
    
    finally:
        # Clean up temporary directory
        cleanup_directory(temp_dir)

@router.delete("/{template_id}", response_model=Dict[str, str])
async def delete_template_endpoint(template_id: str):
    """Delete a template from the collection."""
    success = delete_template(template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {"status": "success", "message": f"Template {template_id} deleted successfully"}

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_templates_endpoint(request: TemplateSearchRequest):
    """Search templates by name, description, or tags."""
    results = search_templates(request.query)
    return results
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks, Query, Body
from fastapi.responses import FileResponse, JSONResponse, Response
from typing import List, Dict, Any, Optional
import os
import json
import base64
from pydantic import BaseModel

from app.services.editor_service import (
    create_editor_session,
    get_editor_session,
    add_text_operation,
    add_image_operation,
    add_signature_operation,
    add_highlight_operation,
    reorder_pages,
    delete_pages,
    rotate_page,
    get_operations,
    clear_operations,
    apply_operations,
    get_page_count,
    cleanup_session,
    get_page_thumbnail,
    get_page_image
)
from app.utils.file_utils import save_upload_file, create_temp_dir as create_temp_directory, cleanup_directory
from app.config import settings

router = APIRouter(prefix="/editor", tags=["editor"])

# Pydantic models for request/response validation
class EditorSessionResponse(BaseModel):
    session_id: str
    page_count: int

class TextOperationRequest(BaseModel):
    page: int
    text: str
    x: float
    y: float
    font_size: int = 12
    color: str = "#000000"
    font_name: str = "helv"

class ImageOperationRequest(BaseModel):
    page: int
    image_data: Optional[str] = None
    x: float = 100
    y: float = 100
    width: float = 100
    height: float = 100
    rotation: float = 0

class SignatureOperationRequest(BaseModel):
    page: int
    signature_data: str
    x: float = 100
    y: float = 100
    width: float = 150
    height: float = 50

class HighlightOperationRequest(BaseModel):
    page: int
    x1: float
    y1: float
    x2: float
    y2: float
    color: str = "#FFFF00"

class ReorderPagesRequest(BaseModel):
    new_order: List[int]

class DeletePagesRequest(BaseModel):
    page_numbers: List[int]

class RotatePageRequest(BaseModel):
    page: int
    angle: int = 90

class OperationResponse(BaseModel):
    operation_id: int

@router.post("/session", response_model=EditorSessionResponse)
async def create_session(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Create a new editor session for a PDF file."""
    # Create a temporary directory for the uploaded file
    temp_dir = create_temp_directory()
    file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        # Create an editor session
        session_id = create_editor_session(file_path)
        session = get_editor_session(session_id)
        
        # Schedule cleanup of the temporary directory
        background_tasks.add_task(cleanup_directory, temp_dir)
        
        return {
            "session_id": session_id,
            "page_count": session.page_count
        }
    
    except Exception as e:
        cleanup_directory(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}", response_model=Dict[str, Any])
async def get_session(session_id: str):
    """Get information about an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "page_count": session.page_count,
        "operation_count": len(session.operations)
    }

@router.post("/session/{session_id}/text", response_model=OperationResponse)
async def add_text(session_id: str, request: TextOperationRequest):
    """Add a text operation to an editor session."""
    try:
        operation_id = add_text_operation(
            session_id=session_id,
            page=request.page,
            text=request.text,
            x=request.x,
            y=request.y,
            font_size=request.font_size,
            color=request.color,
            font_name=request.font_name
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/image", response_model=OperationResponse)
async def add_image(session_id: str, request: ImageOperationRequest = Body(...), 
                   image: Optional[UploadFile] = File(None)):
    """Add an image operation to an editor session."""
    try:
        image_path = None
        image_data = request.image_data
        
        # If an image file was uploaded, save it
        if image:
            temp_dir = create_temp_directory()
            image_path = os.path.join(temp_dir, image.filename)
            with open(image_path, "wb") as f:
                f.write(image.file.read())
        
        operation_id = add_image_operation(
            session_id=session_id,
            page=request.page,
            image_path=image_path,
            image_data=image_data,
            x=request.x,
            y=request.y,
            width=request.width,
            height=request.height,
            rotation=request.rotation
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/signature", response_model=OperationResponse)
async def add_signature(session_id: str, request: SignatureOperationRequest):
    """Add a signature operation to an editor session."""
    try:
        operation_id = add_signature_operation(
            session_id=session_id,
            page=request.page,
            signature_data=request.signature_data,
            x=request.x,
            y=request.y,
            width=request.width,
            height=request.height
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/highlight", response_model=OperationResponse)
async def add_highlight(session_id: str, request: HighlightOperationRequest):
    """Add a highlight operation to an editor session."""
    try:
        operation_id = add_highlight_operation(
            session_id=session_id,
            page=request.page,
            x1=request.x1,
            y1=request.y1,
            x2=request.x2,
            y2=request.y2,
            color=request.color
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/reorder", response_model=OperationResponse)
async def reorder_pages_endpoint(session_id: str, request: ReorderPagesRequest):
    """Reorder pages in an editor session."""
    try:
        operation_id = reorder_pages(
            session_id=session_id,
            new_order=request.new_order
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/delete", response_model=OperationResponse)
async def delete_pages_endpoint(session_id: str, request: DeletePagesRequest):
    """Delete pages in an editor session."""
    try:
        operation_id = delete_pages(
            session_id=session_id,
            page_numbers=request.page_numbers
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/rotate", response_model=OperationResponse)
async def rotate_page_endpoint(session_id: str, request: RotatePageRequest):
    """Rotate a page in an editor session."""
    try:
        operation_id = rotate_page(
            session_id=session_id,
            page=request.page,
            angle=request.angle
        )
        
        return {"operation_id": operation_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}/operations", response_model=List[Dict[str, Any]])
async def get_operations_endpoint(session_id: str):
    """Get all operations in an editor session."""
    try:
        operations = get_operations(session_id)
        return operations
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}/operations", response_model=Dict[str, str])
async def clear_operations_endpoint(session_id: str):
    """Clear all operations in an editor session."""
    try:
        clear_operations(session_id)
        return {"status": "success"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/apply")
async def apply_operations_endpoint(session_id: str, background_tasks: BackgroundTasks):
    """Apply all operations in an editor session and return the result file."""
    try:
        result_path = apply_operations(session_id)
        
        # Schedule cleanup of the session after the file is downloaded
        background_tasks.add_task(cleanup_session, session_id)
        
        return FileResponse(
            path=result_path,
            filename=f"edited_{os.path.basename(result_path)}",
            media_type="application/pdf",
            background=background_tasks
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}/thumbnail/{page_num}")
async def get_thumbnail(session_id: str, page_num: int, 
                       width: int = Query(200, ge=50, le=500), 
                       height: int = Query(300, ge=50, le=700)):
    """Get a thumbnail image of a specific page."""
    try:
        img_data, content_type = get_page_thumbnail(
            session_id=session_id,
            page_num=page_num,
            width=width,
            height=height
        )
        
        return Response(content=img_data, media_type=content_type)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}/image/{page_num}")
async def get_image(session_id: str, page_num: int, 
                  dpi: int = Query(150, ge=72, le=300)):
    """Get a high-resolution image of a specific page."""
    try:
        img_data, content_type = get_page_image(
            session_id=session_id,
            page_num=page_num,
            dpi=dpi
        )
        
        return Response(content=img_data, media_type=content_type)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete an editor session."""
    try:
        cleanup_session(session_id)
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
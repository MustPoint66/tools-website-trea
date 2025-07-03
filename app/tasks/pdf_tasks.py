import asyncio
import os
import uuid
from typing import Dict, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor
import json
import time
from datetime import datetime, timedelta
import logging

# In-memory task storage (in production, use Redis)
TASK_STORAGE: Dict[str, Dict[str, Any]] = {}

# Thread pool for CPU-intensive operations
executor = ThreadPoolExecutor(max_workers=4)

class TaskStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

async def create_task(task_type: str, task_data: Dict[str, Any]) -> str:
    """Create a new background task"""
    task_id = str(uuid.uuid4())
    
    TASK_STORAGE[task_id] = {
        "id": task_id,
        "type": task_type,
        "status": TaskStatus.PENDING,
        "progress": 0,
        "data": task_data,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    
    return task_id

async def update_task_progress(task_id: str, progress: int, status: Optional[str] = None):
    """Update task progress and status"""
    if task_id in TASK_STORAGE:
        TASK_STORAGE[task_id]["progress"] = min(100, max(0, progress))
        TASK_STORAGE[task_id]["updated_at"] = datetime.now().isoformat()
        
        if status:
            TASK_STORAGE[task_id]["status"] = status

async def complete_task(task_id: str, result: Dict[str, Any]):
    """Mark task as completed with result"""
    if task_id in TASK_STORAGE:
        TASK_STORAGE[task_id]["status"] = TaskStatus.COMPLETED
        TASK_STORAGE[task_id]["progress"] = 100
        TASK_STORAGE[task_id]["result"] = result
        TASK_STORAGE[task_id]["updated_at"] = datetime.now().isoformat()

async def fail_task(task_id: str, error: str):
    """Mark task as failed with error message"""
    if task_id in TASK_STORAGE:
        TASK_STORAGE[task_id]["status"] = TaskStatus.FAILED
        TASK_STORAGE[task_id]["error"] = error
        TASK_STORAGE[task_id]["updated_at"] = datetime.now().isoformat()

async def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Get current task status"""
    return TASK_STORAGE.get(task_id)

async def cancel_task(task_id: str):
    """Cancel a running task"""
    if task_id in TASK_STORAGE:
        TASK_STORAGE[task_id]["status"] = TaskStatus.CANCELLED
        TASK_STORAGE[task_id]["updated_at"] = datetime.now().isoformat()

def cleanup_old_tasks():
    """Remove tasks older than 1 hour"""
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(hours=1)
    
    tasks_to_remove = []
    for task_id, task_data in TASK_STORAGE.items():
        created_at = datetime.fromisoformat(task_data["created_at"])
        if created_at < cutoff_time:
            tasks_to_remove.append(task_id)
    
    for task_id in tasks_to_remove:
        del TASK_STORAGE[task_id]

async def process_pdf_async(task_id: str, operation: str, **kwargs):
    """Process PDF operations asynchronously with progress tracking"""
    try:
        await update_task_progress(task_id, 10, TaskStatus.PROCESSING)
        
        if operation == "merge":
            result = await _merge_pdfs_async(task_id, **kwargs)
        elif operation == "split":
            result = await _split_pdf_async(task_id, **kwargs)
        elif operation == "compress":
            result = await _compress_pdf_async(task_id, **kwargs)
        elif operation == "rotate":
            result = await _rotate_pdf_async(task_id, **kwargs)
        elif operation == "watermark":
            result = await _watermark_pdf_async(task_id, **kwargs)
        elif operation == "crop":
            result = await _crop_pdf_async(task_id, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        await complete_task(task_id, result)
        
    except Exception as e:
        logging.error(f"Task {task_id} failed: {str(e)}")
        await fail_task(task_id, str(e))

async def _merge_pdfs_async(task_id: str, input_paths: list, output_path: str):
    """Merge PDFs with progress tracking"""
    from app.services.pdf_service import merge_pdfs
    
    await update_task_progress(task_id, 30)
    
    # Run the CPU-intensive operation in thread pool
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, merge_pdfs, input_paths, output_path)
    
    await update_task_progress(task_id, 90)
    
    # Get file size for response
    file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    
    return {
        "output_path": output_path,
        "file_size": file_size,
        "page_count": len(input_paths)  # Approximate
    }

async def _split_pdf_async(task_id: str, input_path: str, output_dir: str, **kwargs):
    """Split PDF with progress tracking"""
    from app.services.pdf_service import split_pdf, split_pdf_by_page_count
    
    await update_task_progress(task_id, 30)
    
    # Determine split method
    if "pages_per_file" in kwargs:
        loop = asyncio.get_event_loop()
        output_paths = await loop.run_in_executor(
            executor, 
            split_pdf_by_page_count, 
            input_path, 
            output_dir, 
            kwargs["pages_per_file"]
        )
    else:
        page_ranges = kwargs.get("page_ranges")
        loop = asyncio.get_event_loop()
        output_paths = await loop.run_in_executor(
            executor, 
            split_pdf, 
            input_path, 
            output_dir, 
            page_ranges
        )
    
    await update_task_progress(task_id, 90)
    
    # Create zip file if multiple outputs
    if len(output_paths) > 1:
        import zipfile
        zip_path = os.path.join(output_dir, "split_pdfs.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for output_path in output_paths:
                zipf.write(output_path, os.path.basename(output_path))
        
        return {
            "output_path": zip_path,
            "file_count": len(output_paths),
            "file_size": os.path.getsize(zip_path)
        }
    else:
        return {
            "output_path": output_paths[0] if output_paths else None,
            "file_count": len(output_paths),
            "file_size": os.path.getsize(output_paths[0]) if output_paths else 0
        }

async def _compress_pdf_async(task_id: str, input_path: str, output_path: str, compression_level: str):
    """Compress PDF with progress tracking"""
    from app.services.pdf_service import compress_pdf
    
    await update_task_progress(task_id, 30)
    
    # Get original file size
    original_size = os.path.getsize(input_path)
    
    # Run compression in thread pool
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, compress_pdf, input_path, output_path, compression_level)
    
    await update_task_progress(task_id, 90)
    
    # Get compressed file size
    compressed_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    
    return {
        "output_path": output_path,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": round(compression_ratio, 2)
    }

async def _rotate_pdf_async(task_id: str, input_path: str, output_path: str, rotation: int, page_numbers: list = None):
    """Rotate PDF with progress tracking"""
    from app.services.pdf_service import rotate_pdf
    
    await update_task_progress(task_id, 30)
    
    # Run rotation in thread pool
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, rotate_pdf, input_path, output_path, rotation, page_numbers)
    
    await update_task_progress(task_id, 90)
    
    return {
        "output_path": output_path,
        "rotation": rotation,
        "pages_rotated": len(page_numbers) if page_numbers else "all"
    }

async def _watermark_pdf_async(task_id: str, input_path: str, output_path: str, **kwargs):
    """Add watermark with progress tracking"""
    from app.services.pdf_service import add_watermark, add_image_watermark
    
    await update_task_progress(task_id, 30)
    
    # Determine watermark type
    if "watermark_image_path" in kwargs:
        # Image watermark
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            executor, 
            add_image_watermark, 
            input_path, 
            output_path, 
            kwargs["watermark_image_path"],
            kwargs.get("opacity", 0.5),
            kwargs.get("scale", 0.3),
            kwargs.get("position", "center"),
            kwargs.get("page_numbers")
        )
    else:
        # Text watermark
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            executor, 
            add_watermark, 
            input_path, 
            output_path, 
            kwargs["watermark_text"],
            kwargs.get("opacity", 0.5),
            kwargs.get("font_size", 20),
            kwargs.get("color", (0.5, 0.5, 0.5)),
            kwargs.get("page_numbers")
        )
    
    await update_task_progress(task_id, 90)
    
    return {
        "output_path": output_path,
        "watermark_type": "image" if "watermark_image_path" in kwargs else "text"
    }

async def _crop_pdf_async(task_id: str, input_path: str, output_path: str, crop_box: tuple, page_numbers: list = None):
    """Crop PDF with progress tracking"""
    from app.services.pdf_service import crop_pdf
    
    await update_task_progress(task_id, 30)
    
    # Run cropping in thread pool
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, crop_pdf, input_path, output_path, crop_box, page_numbers)
    
    await update_task_progress(task_id, 90)
    
    return {
        "output_path": output_path,
        "crop_box": crop_box,
        "pages_cropped": len(page_numbers) if page_numbers else "all"
    }

async def cleanup_files(file_paths: list, delay_seconds: int = 3600):
    """Schedule file cleanup after delay (default 1 hour)"""
    await asyncio.sleep(delay_seconds)
    
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
        except Exception as e:
            logging.error(f"Failed to cleanup {file_path}: {str(e)}")

# Background task to cleanup old tasks and files
async def background_cleanup():
    """Background task that runs every 30 minutes to cleanup old tasks"""
    while True:
        try:
            cleanup_old_tasks()
            await asyncio.sleep(1800)  # 30 minutes
        except Exception as e:
            logging.error(f"Background cleanup failed: {str(e)}")
            await asyncio.sleep(300)  # 5 minutes before retry

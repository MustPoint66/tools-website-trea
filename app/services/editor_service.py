import os
import json
import uuid
import base64
from typing import List, Dict, Any, Optional, Tuple
import fitz  # PyMuPDF
from PIL import Image
import io

from app.config import settings
from app.utils.file_utils import create_temp_dir, cleanup_directory

# Define constants for editor operations
OPERATION_TEXT = "text"
OPERATION_IMAGE = "image"
OPERATION_SIGNATURE = "signature"
OPERATION_HIGHLIGHT = "highlight"
OPERATION_REORDER = "reorder"
OPERATION_DELETE = "delete"
OPERATION_ROTATE = "rotate"

# Define editor session storage
EDITOR_SESSIONS = {}

class EditorSession:
    def __init__(self, file_path: str):
        self.session_id = str(uuid.uuid4())
        self.file_path = file_path
        self.temp_dir = create_temp_dir()
        self.working_file = os.path.join(self.temp_dir, f"working_{os.path.basename(file_path)}")
        self.operations = []
        self.page_count = 0
        
        # Copy the original file to working file
        self._initialize_working_file()
    
    def _initialize_working_file(self):
        """Initialize the working file by copying the original."""
        try:
            # Open the original document
            doc = fitz.open(self.file_path)
            # Save a copy as the working file
            doc.save(self.working_file)
            self.page_count = doc.page_count
            doc.close()
        except Exception as e:
            raise Exception(f"Failed to initialize working file: {str(e)}")
    
    def add_operation(self, operation: Dict[str, Any]):
        """Add an operation to the session."""
        self.operations.append(operation)
        return len(self.operations) - 1  # Return the operation index
    
    def get_operations(self) -> List[Dict[str, Any]]:
        """Get all operations in the session."""
        return self.operations
    
    def clear_operations(self):
        """Clear all operations in the session."""
        self.operations = []
    
    def apply_operations(self) -> str:
        """Apply all operations to the working file and return the path."""
        try:
            # Open the working document
            doc = fitz.open(self.working_file)
            
            # Process reorder operations first
            reorder_ops = [op for op in self.operations if op["type"] == OPERATION_REORDER]
            if reorder_ops:
                # Use the last reorder operation
                last_reorder = reorder_ops[-1]
                doc = self._apply_reorder(doc, last_reorder)
            
            # Process delete operations
            delete_ops = [op for op in self.operations if op["type"] == OPERATION_DELETE]
            for op in delete_ops:
                doc = self._apply_delete(doc, op)
            
            # Process rotate operations
            rotate_ops = [op for op in self.operations if op["type"] == OPERATION_ROTATE]
            for op in rotate_ops:
                self._apply_rotate(doc, op)
            
            # Process text, image, signature, and highlight operations
            for op in self.operations:
                if op["type"] == OPERATION_TEXT:
                    self._apply_text(doc, op)
                elif op["type"] == OPERATION_IMAGE:
                    self._apply_image(doc, op)
                elif op["type"] == OPERATION_SIGNATURE:
                    self._apply_signature(doc, op)
                elif op["type"] == OPERATION_HIGHLIGHT:
                    self._apply_highlight(doc, op)
            
            # Save the result
            result_path = os.path.join(self.temp_dir, f"result_{os.path.basename(self.file_path)}")
            doc.save(result_path)
            doc.close()
            
            return result_path
        
        except Exception as e:
            raise Exception(f"Failed to apply operations: {str(e)}")
    
    def _apply_text(self, doc: fitz.Document, operation: Dict[str, Any]) -> None:
        """Apply a text operation to the document."""
        page_num = operation.get("page", 0)
        if page_num >= doc.page_count:
            return
        
        page = doc[page_num]
        text = operation.get("text", "")
        x = operation.get("x", 100)
        y = operation.get("y", 100)
        font_size = operation.get("fontSize", 12)
        color = operation.get("color", (0, 0, 0))
        font_name = operation.get("fontName", "helv")
        
        # Convert color from hex to RGB tuple if needed
        if isinstance(color, str) and color.startswith("#"):
            color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        
        # Add text to the page
        page.insert_text(
            point=(x, y),
            text=text,
            fontsize=font_size,
            fontname=font_name,
            color=color
        )
    
    def _apply_image(self, doc: fitz.Document, operation: Dict[str, Any]) -> None:
        """Apply an image operation to the document."""
        page_num = operation.get("page", 0)
        if page_num >= doc.page_count:
            return
        
        page = doc[page_num]
        image_path = operation.get("imagePath")
        image_data = operation.get("imageData")
        x = operation.get("x", 100)
        y = operation.get("y", 100)
        width = operation.get("width", 100)
        height = operation.get("height", 100)
        rotation = operation.get("rotation", 0)
        
        # Handle image source
        if image_path and os.path.exists(image_path):
            # Load image from file
            img_rect = fitz.Rect(x, y, x + width, y + height)
            page.insert_image(img_rect, filename=image_path, rotate=rotation)
        
        elif image_data:
            # Handle base64 encoded image data
            if image_data.startswith("data:image"):
                # Extract the base64 part
                image_data = image_data.split(",")[1]
            
            try:
                # Decode base64 data
                img_bytes = base64.b64decode(image_data)
                img_rect = fitz.Rect(x, y, x + width, y + height)
                page.insert_image(img_rect, stream=img_bytes, rotate=rotation)
            except Exception as e:
                print(f"Error inserting image: {str(e)}")
    
    def _apply_signature(self, doc: fitz.Document, operation: Dict[str, Any]) -> None:
        """Apply a signature operation to the document."""
        # Signatures are handled similarly to images
        page_num = operation.get("page", 0)
        if page_num >= doc.page_count:
            return
        
        page = doc[page_num]
        signature_data = operation.get("signatureData")
        x = operation.get("x", 100)
        y = operation.get("y", 100)
        width = operation.get("width", 150)
        height = operation.get("height", 50)
        
        if signature_data:
            # Handle base64 encoded signature data
            if signature_data.startswith("data:image"):
                # Extract the base64 part
                signature_data = signature_data.split(",")[1]
            
            try:
                # Decode base64 data
                img_bytes = base64.b64decode(signature_data)
                img_rect = fitz.Rect(x, y, x + width, y + height)
                page.insert_image(img_rect, stream=img_bytes)
            except Exception as e:
                print(f"Error inserting signature: {str(e)}")
    
    def _apply_highlight(self, doc: fitz.Document, operation: Dict[str, Any]) -> None:
        """Apply a highlight operation to the document."""
        page_num = operation.get("page", 0)
        if page_num >= doc.page_count:
            return
        
        page = doc[page_num]
        x1 = operation.get("x1", 100)
        y1 = operation.get("y1", 100)
        x2 = operation.get("x2", 200)
        y2 = operation.get("y2", 120)
        color = operation.get("color", (1, 1, 0))  # Default yellow
        
        # Convert color from hex to RGB tuple if needed
        if isinstance(color, str) and color.startswith("#"):
            color = tuple(int(color[i:i+2], 16)/255 for i in (1, 3, 5))
        
        # Create highlight rectangle
        highlight_rect = fitz.Rect(x1, y1, x2, y2)
        page.add_highlight_annot(highlight_rect)
        
        # Get the created annotation and modify its color
        for annot in page.annots():
            if annot.rect == highlight_rect and annot.type[0] == 8:  # Highlight annotation
                annot.set_colors(stroke=color, fill=color)
                annot.update()
                break
    
    def _apply_reorder(self, doc: fitz.Document, operation: Dict[str, Any]) -> fitz.Document:
        """Apply a page reorder operation to the document."""
        new_order = operation.get("newOrder", [])
        if not new_order or len(new_order) != doc.page_count:
            return doc
        
        # Create a new document with reordered pages
        new_doc = fitz.open()
        for page_idx in new_order:
            if 0 <= page_idx < doc.page_count:
                new_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
        
        # Save and reload the document
        temp_path = os.path.join(self.temp_dir, f"reordered_{uuid.uuid4()}.pdf")
        new_doc.save(temp_path)
        new_doc.close()
        doc.close()
        
        return fitz.open(temp_path)
    
    def _apply_delete(self, doc: fitz.Document, operation: Dict[str, Any]) -> fitz.Document:
        """Apply a page delete operation to the document."""
        page_numbers = operation.get("pages", [])
        if not page_numbers:
            return doc
        
        # Sort page numbers in descending order to avoid index shifting
        page_numbers = sorted(page_numbers, reverse=True)
        
        # Create a new document without the deleted pages
        new_doc = fitz.open()
        for i in range(doc.page_count):
            if i not in page_numbers:
                new_doc.insert_pdf(doc, from_page=i, to_page=i)
        
        # Save and reload the document
        temp_path = os.path.join(self.temp_dir, f"deleted_{uuid.uuid4()}.pdf")
        new_doc.save(temp_path)
        new_doc.close()
        doc.close()
        
        return fitz.open(temp_path)
    
    def _apply_rotate(self, doc: fitz.Document, operation: Dict[str, Any]) -> None:
        """Apply a page rotation operation to the document."""
        page_num = operation.get("page", 0)
        angle = operation.get("angle", 90)  # Default 90 degrees clockwise
        
        if page_num >= doc.page_count:
            return
        
        # Rotate the page
        page = doc[page_num]
        current_rotation = page.rotation
        new_rotation = (current_rotation + angle) % 360
        page.set_rotation(new_rotation)
    
    def cleanup(self):
        """Clean up temporary files."""
        cleanup_directory(self.temp_dir)

# Editor service functions
def create_editor_session(file_path: str) -> str:
    """Create a new editor session for a PDF file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    session = EditorSession(file_path)
    EDITOR_SESSIONS[session.session_id] = session
    
    return session.session_id

def get_editor_session(session_id: str) -> Optional[EditorSession]:
    """Get an editor session by ID."""
    return EDITOR_SESSIONS.get(session_id)

def add_text_operation(session_id: str, page: int, text: str, x: float, y: float, 
                      font_size: int = 12, color: str = "#000000", 
                      font_name: str = "helv") -> int:
    """Add a text operation to an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    operation = {
        "type": OPERATION_TEXT,
        "page": page,
        "text": text,
        "x": x,
        "y": y,
        "fontSize": font_size,
        "color": color,
        "fontName": font_name
    }
    
    return session.add_operation(operation)

def add_image_operation(session_id: str, page: int, image_path: Optional[str] = None, 
                       image_data: Optional[str] = None, x: float = 100, y: float = 100, 
                       width: float = 100, height: float = 100, 
                       rotation: float = 0) -> int:
    """Add an image operation to an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    if not image_path and not image_data:
        raise ValueError("Either image_path or image_data must be provided")
    
    operation = {
        "type": OPERATION_IMAGE,
        "page": page,
        "imagePath": image_path,
        "imageData": image_data,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "rotation": rotation
    }
    
    return session.add_operation(operation)

def add_signature_operation(session_id: str, page: int, signature_data: str, 
                          x: float = 100, y: float = 100, 
                          width: float = 150, height: float = 50) -> int:
    """Add a signature operation to an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    operation = {
        "type": OPERATION_SIGNATURE,
        "page": page,
        "signatureData": signature_data,
        "x": x,
        "y": y,
        "width": width,
        "height": height
    }
    
    return session.add_operation(operation)

def add_highlight_operation(session_id: str, page: int, x1: float, y1: float, 
                          x2: float, y2: float, color: str = "#FFFF00") -> int:
    """Add a highlight operation to an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    operation = {
        "type": OPERATION_HIGHLIGHT,
        "page": page,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "color": color
    }
    
    return session.add_operation(operation)

def reorder_pages(session_id: str, new_order: List[int]) -> int:
    """Reorder pages in an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    operation = {
        "type": OPERATION_REORDER,
        "newOrder": new_order
    }
    
    return session.add_operation(operation)

def delete_pages(session_id: str, page_numbers: List[int]) -> int:
    """Delete pages in an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    operation = {
        "type": OPERATION_DELETE,
        "pages": page_numbers
    }
    
    return session.add_operation(operation)

def rotate_page(session_id: str, page: int, angle: int = 90) -> int:
    """Rotate a page in an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    operation = {
        "type": OPERATION_ROTATE,
        "page": page,
        "angle": angle
    }
    
    return session.add_operation(operation)

def get_operations(session_id: str) -> List[Dict[str, Any]]:
    """Get all operations in an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    return session.get_operations()

def clear_operations(session_id: str) -> None:
    """Clear all operations in an editor session."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    session.clear_operations()

def apply_operations(session_id: str) -> str:
    """Apply all operations in an editor session and return the result file path."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    return session.apply_operations()

def get_page_count(session_id: str) -> int:
    """Get the number of pages in the document."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    return session.page_count

def cleanup_session(session_id: str) -> None:
    """Clean up an editor session."""
    session = get_editor_session(session_id)
    if session:
        session.cleanup()
        del EDITOR_SESSIONS[session_id]

def get_page_thumbnail(session_id: str, page_num: int, width: int = 200, height: int = 300) -> Tuple[bytes, str]:
    """Get a thumbnail image of a specific page."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    if page_num < 0 or page_num >= session.page_count:
        raise ValueError(f"Invalid page number: {page_num}")
    
    try:
        # Open the document
        doc = fitz.open(session.working_file)
        page = doc[page_num]
        
        # Calculate zoom factors to fit the requested dimensions
        page_rect = page.rect
        zoom_x = width / page_rect.width
        zoom_y = height / page_rect.height
        zoom = min(zoom_x, zoom_y)
        
        # Create a pixmap
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix)
        
        # Convert to PIL Image and then to bytes
        img_data = pix.tobytes("png")
        
        doc.close()
        
        return img_data, "image/png"
    
    except Exception as e:
        raise Exception(f"Failed to get page thumbnail: {str(e)}")

def get_page_image(session_id: str, page_num: int, dpi: int = 150) -> Tuple[bytes, str]:
    """Get a high-resolution image of a specific page."""
    session = get_editor_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    
    if page_num < 0 or page_num >= session.page_count:
        raise ValueError(f"Invalid page number: {page_num}")
    
    try:
        # Open the document
        doc = fitz.open(session.working_file)
        page = doc[page_num]
        
        # Calculate zoom factor based on DPI
        zoom = dpi / 72  # 72 DPI is the default PDF resolution
        
        # Create a pixmap
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix)
        
        # Convert to PIL Image and then to bytes
        img_data = pix.tobytes("png")
        
        doc.close()
        
        return img_data, "image/png"
    
    except Exception as e:
        raise Exception(f"Failed to get page image: {str(e)}")
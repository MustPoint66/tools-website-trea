import os
import json
import uuid
from typing import List, Dict, Any, Optional, Callable, Union, Tuple
import fitz  # PyMuPDF
from PIL import Image
import io

# Import services that provide tools
from app.services.pdf_service import compress_pdf, add_watermark
from app.services.ocr_service import ocr_image, ocr_pdf
from app.services.conversion_service import convert_file
from app.services.table_service import extract_tables, save_tables_to_excel
from app.services.form_service import fill_form
from app.config import settings

# Define available tools and their handlers
TOOL_REGISTRY = {}

def register_tool(name: str):
    """
    Decorator to register a tool in the tool registry.
    
    Args:
        name: The name of the tool to register
    """
    def decorator(func):
        TOOL_REGISTRY[name] = func
        return func
    return decorator

@register_tool('compress')
def tool_compress(doc: fitz.Document, params: Dict[str, Any]) -> fitz.Document:
    """
    Compress a PDF document.
    
    Args:
        doc: The PDF document to compress
        params: Parameters for compression
            - quality: Compression quality (low, medium, high)
    
    Returns:
        Compressed PDF document
    """
    quality = params.get('quality', 'medium')
    
    # Save the document to a temporary file
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(temp_path)
    
    # Compress the PDF
    compressed_path = compress_pdf(temp_path, quality)
    
    # Load the compressed document
    compressed_doc = fitz.open(compressed_path)
    
    # Clean up temporary files
    try:
        os.remove(temp_path)
    except:
        pass
    
    return compressed_doc

@register_tool('watermark')
def tool_watermark(doc: fitz.Document, params: Dict[str, Any]) -> fitz.Document:
    """
    Add a watermark to a PDF document.
    
    Args:
        doc: The PDF document to watermark
        params: Parameters for watermarking
            - text: Watermark text
            - opacity: Watermark opacity (0-1)
            - rotation: Watermark rotation angle
    
    Returns:
        Watermarked PDF document
    """
    text = params.get('text', 'Watermark')
    opacity = params.get('opacity', 0.5)
    rotation = params.get('rotation', 45)
    
    # Save the document to a temporary file
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(temp_path)
    
    # Add watermark to the PDF
    watermarked_path = add_watermark(temp_path, text, opacity, rotation)
    
    # Load the watermarked document
    watermarked_doc = fitz.open(watermarked_path)
    
    # Clean up temporary files
    try:
        os.remove(temp_path)
    except:
        pass
    
    return watermarked_doc

@register_tool('ocr')
def tool_ocr(doc: fitz.Document, params: Dict[str, Any]) -> fitz.Document:
    """
    Perform OCR on a PDF document.
    
    Args:
        doc: The PDF document to OCR
        params: Parameters for OCR
            - engine: OCR engine to use (tesseract, easyocr)
            - language: Language for OCR
            - output_format: Format for OCR output (pdf, txt, docx)
    
    Returns:
        OCR'd PDF document
    """
    engine = params.get('engine', 'tesseract')
    language = params.get('language', 'eng')
    output_format = params.get('output_format', 'pdf')
    
    # Save the document to a temporary file
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(temp_path)
    
    # Perform OCR on the PDF
    ocr_result_path = ocr_pdf(
        temp_path, 
        engine=engine,
        language=language,
        output_format=output_format
    )
    
    # Load the OCR'd document
    if output_format == 'pdf':
        ocr_doc = fitz.open(ocr_result_path)
    else:
        # If output is not PDF, we'll return the original document
        # The OCR result is saved separately
        ocr_doc = doc
    
    # Clean up temporary files
    try:
        os.remove(temp_path)
    except:
        pass
    
    return ocr_doc

@register_tool('extract_tables')
def tool_extract_tables(doc: fitz.Document, params: Dict[str, Any]) -> fitz.Document:
    """
    Extract tables from a PDF document.
    
    Args:
        doc: The PDF document to extract tables from
        params: Parameters for table extraction
            - methods: List of extraction methods to use
            - output_path: Path to save extracted tables
    
    Returns:
        Original PDF document (tables are saved separately)
    """
    methods = params.get('methods', ['pdfplumber', 'tabula', 'camelot'])
    output_path = params.get('output_path', None)
    
    # Save the document to a temporary file
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(temp_path)
    
    # Extract tables from the PDF
    tables_dict = extract_tables(temp_path, methods=methods)
    
    # Flatten the dictionary of tables into a single list
    all_tables = []
    for method, tables in tables_dict.items():
        all_tables.extend(tables)
    
    # Save tables to Excel if output_path is provided
    if output_path and all_tables:
        save_tables_to_excel(all_tables, output_path)
    
    # Clean up temporary files
    try:
        os.remove(temp_path)
    except:
        pass
    
    # Return the original document
    return doc

@register_tool('fill_form')
def tool_fill_form(doc: fitz.Document, params: Dict[str, Any]) -> fitz.Document:
    """
    Fill form fields in a PDF document.
    
    Args:
        doc: The PDF document with form fields
        params: Parameters for form filling
            - values: Dictionary of field names and values
            - use_default_profile: Whether to use default profile for missing values
    
    Returns:
        PDF document with filled form fields
    """
    values = params.get('values', {})
    use_default_profile = params.get('use_default_profile', True)
    
    # Save the document to a temporary file
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(temp_path)
    
    # Fill the form
    filled_path = fill_form(temp_path, values, use_default_profile)
    
    # Load the filled document
    filled_doc = fitz.open(filled_path)
    
    # Clean up temporary files
    try:
        os.remove(temp_path)
    except:
        pass
    
    return filled_doc

@register_tool('convert')
def tool_convert(doc: fitz.Document, params: Dict[str, Any]) -> fitz.Document:
    """
    Convert a PDF document to another format.
    
    Args:
        doc: The PDF document to convert
        params: Parameters for conversion
            - output_format: Format to convert to
            - options: Additional conversion options
    
    Returns:
        Converted document (if output is PDF) or original document
    """
    output_format = params.get('output_format', 'pdf')
    options = params.get('options', {})
    
    # Save the document to a temporary file
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(temp_path)
    
    # Convert the document
    converted_path = convert_file(temp_path, output_format, **options)
    
    # If output is PDF, load the converted document
    if output_format.lower() == 'pdf':
        converted_doc = fitz.open(converted_path)
    else:
        # If output is not PDF, we'll return the original document
        # The converted file is saved separately
        converted_doc = doc
    
    # Clean up temporary files
    try:
        os.remove(temp_path)
    except:
        pass
    
    return converted_doc

def validate_workflow(workflow: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validate a workflow definition.
    
    Args:
        workflow: List of workflow steps
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(workflow, list):
        return False, "Workflow must be a list of steps"
    
    for i, step in enumerate(workflow):
        if not isinstance(step, dict):
            return False, f"Step {i} must be a dictionary"
        
        if 'tool' not in step:
            return False, f"Step {i} is missing 'tool' field"
        
        tool_name = step['tool']
        if tool_name not in TOOL_REGISTRY:
            return False, f"Unknown tool '{tool_name}' in step {i}"
        
        if 'params' in step and not isinstance(step['params'], dict):
            return False, f"'params' in step {i} must be a dictionary"
    
    return True, ""

def execute_workflow(pdf_path: str, workflow: List[Dict[str, Any]]) -> str:
    """
    Execute a workflow on a PDF document.
    
    Args:
        pdf_path: Path to the input PDF document
        workflow: List of workflow steps
    
    Returns:
        Path to the output document
    """
    # Validate the workflow
    is_valid, error_message = validate_workflow(workflow)
    if not is_valid:
        raise ValueError(f"Invalid workflow: {error_message}")
    
    # Open the input document
    doc = fitz.open(pdf_path)
    
    # Execute each step in the workflow
    for i, step in enumerate(workflow):
        tool_name = step['tool']
        params = step.get('params', {})
        
        # Get the tool handler
        tool_handler = TOOL_REGISTRY[tool_name]
        
        # Execute the tool
        doc = tool_handler(doc, params)
    
    # Save the final document
    output_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.pdf")
    doc.save(output_path)
    doc.close()
    
    return output_path

def get_available_tools() -> Dict[str, Dict[str, Any]]:
    """
    Get information about available tools.
    
    Returns:
        Dictionary of tool information
    """
    tools_info = {}
    
    for tool_name, tool_handler in TOOL_REGISTRY.items():
        # Get tool documentation from docstring
        doc = tool_handler.__doc__ or ""
        
        # Extract parameter information from docstring
        param_info = {}
        if 'params:' in doc:
            params_section = doc.split('params:')[1].split('Returns:')[0]
            for line in params_section.strip().split('\n'):
                line = line.strip()
                if line and '-' in line:
                    param_name, param_desc = line.split('-', 1)
                    param_info[param_name.strip()] = param_desc.strip()
        
        tools_info[tool_name] = {
            'description': doc.split('\n\n')[0].strip(),
            'parameters': param_info
        }
    
    return tools_info
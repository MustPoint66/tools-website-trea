import os
import io
import tempfile
from typing import Optional, List, Dict, Any, Union, Tuple
from pathlib import Path
import pytesseract
from PIL import Image
import pdf2image
import fitz  # PyMuPDF
from docx import Document
from app.config import settings
from app.services.ai_ocr_service import ai_ocr_image, ai_ocr_pdf


def setup_pytesseract():
    """
    Setup pytesseract with the correct path to the Tesseract executable
    """
    # Check if Tesseract path is already set
    if not pytesseract.pytesseract.tesseract_cmd or not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        # Common Tesseract installation paths on Windows
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        
        # Try to find Tesseract
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
                
        # If not found, try to use the one in PATH
        try:
            import subprocess
            result = subprocess.run(["where", "tesseract"], capture_output=True, text=True, check=False)
            if result.stdout.strip():
                pytesseract.pytesseract.tesseract_cmd = result.stdout.strip().split('\n')[0]
                return True
        except Exception:
            pass
            
        return False
    return True


def ocr_image(image_path: str, lang: str = "eng", engine: str = "tesseract") -> str:
    """
    Perform OCR on an image file
    
    Args:
        image_path: Path to the image file
        lang: Language for OCR (default: eng)
        engine: OCR engine to use (tesseract or easyocr)
        
    Returns:
        Extracted text as a string
    """
    # Use AI-based OCR if easyocr engine is specified
    if engine.lower() == "easyocr":
        return ai_ocr_image(image_path)
    
    # Otherwise use Tesseract
    if not setup_pytesseract():
        raise RuntimeError("Tesseract OCR not found. Please install Tesseract OCR.")
        
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(image, lang=lang)
        
        return text
    except Exception as e:
        print(f"Error performing OCR on image: {str(e)}")
        return ""


def ocr_pdf(pdf_path: str, lang: str = "eng", dpi: int = 300) -> str:
    """
    Perform OCR on a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        lang: Language for OCR (default: eng)
        dpi: DPI for image conversion (default: 300)
        
    Returns:
        Extracted text as a string
    """
    if not setup_pytesseract():
        raise RuntimeError("Tesseract OCR not found. Please install Tesseract OCR.")
        
    try:
        # First try to extract text directly from the PDF
        doc = fitz.open(pdf_path)
        text = ""
        has_text = False
        
        # Check if the PDF already has text
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                has_text = True
                text += page_text + "\n\n"
        
        # If the PDF has text, return it
        if has_text and len(text.strip()) > 100:  # Arbitrary threshold to determine if text extraction was successful
            return text
        
        # If no text was found, convert PDF to images and perform OCR
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert PDF to images
            images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
            
            # Perform OCR on each image
            full_text = ""
            for i, image in enumerate(images):
                # Save the image temporarily
                image_path = os.path.join(temp_dir, f"page_{i+1}.png")
                image.save(image_path, "PNG")
                
                # Perform OCR
                page_text = ocr_image(image_path, lang=lang)
                full_text += page_text + "\n\n"
            
            return full_text
    except Exception as e:
        print(f"Error performing OCR on PDF: {str(e)}")
        return ""


def save_text_to_file(text: str, output_path: str, format: str = "txt") -> bool:
    """
    Save extracted text to a file
    
    Args:
        text: Text to save
        output_path: Path to save the output file
        format: Output format (txt or docx)
        
    Returns:
        bool: True if saving was successful, False otherwise
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as TXT
        if format.lower() == "txt":
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
        
        # Save as DOCX
        elif format.lower() == "docx":
            doc = Document()
            
            # Split text into paragraphs and add to document
            paragraphs = text.split("\n\n")
            for paragraph in paragraphs:
                if paragraph.strip():
                    doc.add_paragraph(paragraph.strip())
            
            doc.save(output_path)
        
        else:
            raise ValueError(f"Unsupported output format: {format}")
        
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Error saving text to file: {str(e)}")
        return False


def clean_ocr_text(text: str) -> str:
    """
    Clean OCR text by removing extra whitespace, fixing common OCR errors, etc.
    
    Args:
        text: OCR text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Replace multiple newlines with a single newline
    import re
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix common OCR errors (can be expanded based on specific needs)
    replacements = {
        "l\n": "I",  # lowercase L at end of line is often a capital I
        "0\n": "O",  # zero at end of line is often capital O
        "1\n": "I",  # one at end of line is often capital I
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text
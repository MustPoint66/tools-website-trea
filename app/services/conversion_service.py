import os
import subprocess
import tempfile
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path
from PIL import Image
import pdf2image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from app.config import settings


def convert_office_to_pdf(input_path: str, output_path: str) -> bool:
    """
    Convert Office documents (Word, Excel, PowerPoint) to PDF using LibreOffice
    
    Args:
        input_path: Path to the input file
        output_path: Path to save the output PDF
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Check if LibreOffice is installed and available
        result = subprocess.run(
            ["where", "soffice"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if "soffice" not in result.stdout.lower():
            # Use direct LibreOffice path if not in PATH
            libreoffice_paths = [
                "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
                "C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe"
            ]
            
            soffice_path = None
            for path in libreoffice_paths:
                if os.path.exists(path):
                    soffice_path = path
                    break
                    
            if not soffice_path:
                raise FileNotFoundError("LibreOffice not found. Please install LibreOffice.")
        else:
            soffice_path = "soffice"
        
        # Convert to PDF using LibreOffice
        subprocess.run(
            [
                soffice_path,
                "--headless",
                "--convert-to", "pdf",
                "--outdir", os.path.dirname(output_path),
                input_path
            ],
            check=True,
            capture_output=True
        )
        
        # LibreOffice creates the PDF with the same name as the input file
        # but with .pdf extension in the output directory
        input_filename = os.path.basename(input_path)
        input_name = os.path.splitext(input_filename)[0]
        temp_output_path = os.path.join(os.path.dirname(output_path), f"{input_name}.pdf")
        
        # Rename the file if needed
        if temp_output_path != output_path and os.path.exists(temp_output_path):
            os.rename(temp_output_path, output_path)
            
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Error converting Office document to PDF: {str(e)}")
        return False


def convert_pdf_to_images(input_path: str, output_dir: str, dpi: int = 200, 
                         format: str = "jpeg") -> List[str]:
    """
    Convert PDF to images using pdf2image
    
    Args:
        input_path: Path to the input PDF file
        output_dir: Directory to save the output images
        dpi: DPI for the output images
        format: Output image format (jpeg, png, etc.)
        
    Returns:
        List of paths to the generated images
    """
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_path(
            input_path,
            dpi=dpi,
            fmt=format
        )
        
        # Save images
        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"page_{i+1}.{format}")
            image.save(image_path, format.upper())
            image_paths.append(image_path)
            
        return image_paths
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        return []


def convert_images_to_pdf(image_paths: List[str], output_path: str) -> bool:
    """
    Convert images to PDF using Pillow
    
    Args:
        image_paths: List of paths to the input images
        output_path: Path to save the output PDF
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        if not image_paths:
            return False
            
        # Open the first image to get its size
        first_image = Image.open(image_paths[0])
        width, height = first_image.size
        
        # Create a PDF with the same size as the images
        c = canvas.Canvas(output_path, pagesize=(width, height))
        
        # Add each image as a page in the PDF
        for image_path in image_paths:
            img = Image.open(image_path)
            c.drawImage(image_path, 0, 0, width, height)
            c.showPage()
            
        c.save()
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Error converting images to PDF: {str(e)}")
        return False


def convert_text_to_pdf(input_path: str, output_path: str) -> bool:
    """
    Convert text file to PDF using ReportLab
    
    Args:
        input_path: Path to the input text file
        output_path: Path to save the output PDF
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Read the text file
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Create a PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        
        # Split the text into paragraphs
        paragraphs = [Paragraph(line, style) for line in text.split('\n') if line.strip()]
        
        # Build the PDF
        doc.build(paragraphs)
        
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Error converting text to PDF: {str(e)}")
        return False


def convert_pdf_to_text(input_path: str, output_path: str) -> bool:
    """
    Extract text from PDF and save to a text file
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the output text file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        import fitz  # PyMuPDF
        
        # Open the PDF
        doc = fitz.open(input_path)
        text = ""
        
        # Extract text from each page
        for page in doc:
            text += page.get_text()
        
        # Save the text to a file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Error converting PDF to text: {str(e)}")
        return False


def detect_file_type(file_path: str) -> str:
    """
    Detect the file type based on extension
    
    Args:
        file_path: Path to the file
        
    Returns:
        File type as a string (pdf, word, excel, image, text, etc.)
    """
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension in [".pdf"]:
        return "pdf"
    elif extension in [".doc", ".docx"]:
        return "word"
    elif extension in [".xls", ".xlsx"]:
        return "excel"
    elif extension in [".ppt", ".pptx"]:
        return "powerpoint"
    elif extension in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]:
        return "image"
    elif extension in [".txt"]:
        return "text"
    else:
        return "unknown"


def convert_file(input_path: str, output_path: str, target_format: str) -> bool:
    """
    Convert a file to the specified format
    
    Args:
        input_path: Path to the input file
        output_path: Path to save the output file
        target_format: Target format (pdf, image, text)
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    input_type = detect_file_type(input_path)
    
    # Word/Excel/PowerPoint to PDF
    if input_type in ["word", "excel", "powerpoint"] and target_format == "pdf":
        return convert_office_to_pdf(input_path, output_path)
    
    # PDF to images
    elif input_type == "pdf" and target_format == "image":
        output_dir = os.path.dirname(output_path)
        image_paths = convert_pdf_to_images(input_path, output_dir)
        return len(image_paths) > 0
    
    # Images to PDF
    elif input_type == "image" and target_format == "pdf":
        return convert_images_to_pdf([input_path], output_path)
    
    # Text to PDF
    elif input_type == "text" and target_format == "pdf":
        return convert_text_to_pdf(input_path, output_path)
    
    # PDF to text
    elif input_type == "pdf" and target_format == "text":
        return convert_pdf_to_text(input_path, output_path)
    
    else:
        print(f"Conversion from {input_type} to {target_format} is not supported")
        return False
import fitz  # PyMuPDF
import os
import io
import tempfile
import subprocess
from typing import List, Optional, Tuple, Dict, Union
from PIL import Image
import math

def merge_pdfs(input_paths: List[str], output_path: str) -> str:
    """
    Merge multiple PDF files into a single PDF
    
    Args:
        input_paths: List of paths to input PDF files
        output_path: Path where the merged PDF will be saved
        
    Returns:
        Path to the merged PDF file
    """
    # Create a new PDF document
    merged_pdf = fitz.open()
    
    # Add pages from each input PDF
    for pdf_path in input_paths:
        try:
            pdf_document = fitz.open(pdf_path)
            merged_pdf.insert_pdf(pdf_document)
            pdf_document.close()
        except Exception as e:
            # Close the merged PDF to avoid memory leaks
            merged_pdf.close()
            raise Exception(f"Error merging PDF {pdf_path}: {str(e)}")
    
    # Save the merged PDF
    merged_pdf.save(output_path)
    merged_pdf.close()
    
    return output_path


def merge_pdfs_in_memory(pdf_contents: List[bytes]) -> bytes:
    """
    Merge multiple PDF files in memory without saving to disk
    
    Args:
        pdf_contents: List of PDF file contents as bytes
        
    Returns:
        Merged PDF as bytes
    """
    # Create a new PDF document
    merged_pdf = fitz.open()
    
    # Add pages from each input PDF
    for pdf_content in pdf_contents:
        try:
            # Open PDF from memory
            memory_stream = io.BytesIO(pdf_content)
            pdf_document = fitz.open(stream=memory_stream, filetype="pdf")
            merged_pdf.insert_pdf(pdf_document)
            pdf_document.close()
        except Exception as e:
            # Close the merged PDF to avoid memory leaks
            merged_pdf.close()
            raise Exception(f"Error merging PDF: {str(e)}")
    
    # Save the merged PDF to a bytes buffer
    output_buffer = io.BytesIO()
    merged_pdf.save(output_buffer)
    merged_pdf.close()
    
    # Return the merged PDF as bytes
    output_buffer.seek(0)
    return output_buffer.getvalue()


def split_pdf(input_path: str, output_dir: str, page_ranges: Optional[List[Tuple[int, int]]] = None) -> List[str]:
    """
    Split a PDF file into multiple PDFs based on page ranges
    
    Args:
        input_path: Path to the input PDF file
        output_dir: Directory where the split PDFs will be saved
        page_ranges: List of tuples (start_page, end_page) for splitting
                    If None, each page becomes a separate PDF
    
    Returns:
        List of paths to the split PDF files
    """
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    total_pages = len(pdf_document)
    output_paths = []
    
    # If no page ranges provided, split into individual pages
    if not page_ranges:
        page_ranges = [(i, i) for i in range(total_pages)]
    
    # Process each page range
    for i, (start_page, end_page) in enumerate(page_ranges):
        # Validate page range
        if start_page < 0 or end_page >= total_pages or start_page > end_page:
            continue
        
        # Create a new PDF for this range
        output_pdf = fitz.open()
        
        # Add pages from the range
        for page_num in range(start_page, end_page + 1):
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        
        # Save the output PDF
        output_filename = f"split_{i+1}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        output_pdf.save(output_path)
        output_pdf.close()
        
        output_paths.append(output_path)
    
    # Close the input document
    pdf_document.close()
    
    return output_paths


def split_pdf_by_page_count(input_path: str, output_dir: str, pages_per_file: int) -> List[str]:
    """
    Split a PDF file into multiple PDFs with a fixed number of pages per file
    
    Args:
        input_path: Path to the input PDF file
        output_dir: Directory where the split PDFs will be saved
        pages_per_file: Number of pages per output file
    
    Returns:
        List of paths to the split PDF files
    """
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    total_pages = len(pdf_document)
    
    # Calculate page ranges
    page_ranges = []
    for i in range(0, total_pages, pages_per_file):
        start_page = i
        end_page = min(i + pages_per_file - 1, total_pages - 1)
        page_ranges.append((start_page, end_page))
    
    # Split the PDF using the calculated page ranges
    output_paths = split_pdf(input_path, output_dir, page_ranges)
    
    return output_paths


def rotate_pdf(input_path: str, output_path: str, rotation: int, page_numbers: Optional[List[int]] = None) -> str:
    """
    Rotate pages in a PDF file
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the rotated PDF will be saved
        rotation: Rotation angle in degrees (90, 180, 270)
        page_numbers: List of page numbers to rotate (0-indexed)
                     If None, all pages are rotated
    
    Returns:
        Path to the rotated PDF file
    """
    # Validate rotation angle
    if rotation not in [90, 180, 270]:
        raise ValueError("Rotation angle must be 90, 180, or 270 degrees")
    
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    total_pages = len(pdf_document)
    
    # If no page numbers provided, rotate all pages
    if page_numbers is None:
        page_numbers = list(range(total_pages))
    
    # Validate page numbers
    valid_page_numbers = [p for p in page_numbers if 0 <= p < total_pages]
    
    # Apply rotation to specified pages
    for page_num in valid_page_numbers:
        page = pdf_document[page_num]
        # PyMuPDF uses counterclockwise rotation, so we need to convert
        # 90 -> 270, 270 -> 90, 180 stays the same
        pymupdf_rotation = 360 - rotation if rotation != 180 else 180
        page.set_rotation(pymupdf_rotation)
    
    # Save the rotated PDF
    pdf_document.save(output_path)
    pdf_document.close()
    
    return output_path


def add_watermark(input_path: str, output_path: str, watermark_text: str, opacity: float = 0.5, 
                 font_size: int = 20, color: Tuple[float, float, float] = (0.5, 0.5, 0.5),
                 page_numbers: Optional[List[int]] = None) -> str:
    """
    Add a text watermark to a PDF file
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the watermarked PDF will be saved
        watermark_text: Text to use as watermark
        opacity: Opacity of the watermark (0.0 to 1.0)
        font_size: Font size for the watermark text
        color: RGB color tuple (0.0 to 1.0 for each component)
        page_numbers: List of page numbers to watermark (0-indexed)
                     If None, all pages are watermarked
    
    Returns:
        Path to the watermarked PDF file
    """
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    total_pages = len(pdf_document)
    
    # If no page numbers provided, watermark all pages
    if page_numbers is None:
        page_numbers = list(range(total_pages))
    
    # Validate page numbers
    valid_page_numbers = [p for p in page_numbers if 0 <= p < total_pages]
    
    # Apply watermark to specified pages
    for page_num in valid_page_numbers:
        page = pdf_document[page_num]
        
        # Get page dimensions
        rect = page.rect
        width, height = rect.width, rect.height
        
        # Create a transparent layer for the watermark
        # We'll use a diagonal watermark pattern
        for i in range(0, int(height + width), font_size * 4):
            # Calculate position for diagonal watermark
            x = i - font_size * len(watermark_text) / 2
            y = height - i + font_size / 2
            
            # Skip if outside page bounds
            if x > width or y < 0:
                continue
                
            # Insert the watermark text
            text_point = fitz.Point(x, y)
            page.insert_text(
                text_point,
                watermark_text,
                fontsize=font_size,
                color=color,
                opacity=opacity,
                rotate=45  # Diagonal watermark
            )
    
    # Save the watermarked PDF
    pdf_document.save(output_path)
    pdf_document.close()
    
    return output_path


def add_image_watermark(input_path: str, output_path: str, watermark_image_path: str, 
                       opacity: float = 0.5, scale: float = 0.3,
                       position: str = "center", page_numbers: Optional[List[int]] = None) -> str:
    """
    Add an image watermark to a PDF file
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the watermarked PDF will be saved
        watermark_image_path: Path to the image to use as watermark
        opacity: Opacity of the watermark (0.0 to 1.0)
        scale: Scale factor for the watermark image (relative to page size)
        position: Position of the watermark ("center", "top-left", "top-right", "bottom-left", "bottom-right")
        page_numbers: List of page numbers to watermark (0-indexed)
                     If None, all pages are watermarked
    
    Returns:
        Path to the watermarked PDF file
    """
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    total_pages = len(pdf_document)
    
    # If no page numbers provided, watermark all pages
    if page_numbers is None:
        page_numbers = list(range(total_pages))
    
    # Validate page numbers
    valid_page_numbers = [p for p in page_numbers if 0 <= p < total_pages]
    
    # Load the watermark image
    watermark_image = fitz.open(watermark_image_path)
    if watermark_image.page_count == 0:
        raise ValueError("Invalid watermark image")
    
    # Get the first page of the image (if it's a PDF)
    watermark_page = watermark_image[0]
    
    # Apply watermark to specified pages
    for page_num in valid_page_numbers:
        page = pdf_document[page_num]
        
        # Get page dimensions
        rect = page.rect
        page_width, page_height = rect.width, rect.height
        
        # Calculate watermark dimensions based on scale
        watermark_width = page_width * scale
        watermark_height = page_height * scale
        
        # Calculate position
        if position == "center":
            x = (page_width - watermark_width) / 2
            y = (page_height - watermark_height) / 2
        elif position == "top-left":
            x, y = 0, 0
        elif position == "top-right":
            x, y = page_width - watermark_width, 0
        elif position == "bottom-left":
            x, y = 0, page_height - watermark_height
        elif position == "bottom-right":
            x, y = page_width - watermark_width, page_height - watermark_height
        else:  # Default to center
            x = (page_width - watermark_width) / 2
            y = (page_height - watermark_height) / 2
        
        # Create a rectangle for the watermark
        watermark_rect = fitz.Rect(x, y, x + watermark_width, y + watermark_height)
        
        # Insert the watermark image
        page.insert_image(watermark_rect, pixmap=watermark_page.get_pixmap(), overlay=True, opacity=opacity)
    
    # Close the watermark image
    watermark_image.close()
    
    # Save the watermarked PDF
    pdf_document.save(output_path)
    pdf_document.close()
    
    return output_path


def crop_pdf(input_path: str, output_path: str, crop_box: Tuple[float, float, float, float], 
            page_numbers: Optional[List[int]] = None) -> str:
    """
    Crop pages in a PDF file
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the cropped PDF will be saved
        crop_box: Tuple (left, bottom, right, top) defining the crop box
                 Values are in points (1/72 inch)
        page_numbers: List of page numbers to crop (0-indexed)
                     If None, all pages are cropped
    
    Returns:
        Path to the cropped PDF file
    """
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    total_pages = len(pdf_document)
    
    # If no page numbers provided, crop all pages
    if page_numbers is None:
        page_numbers = list(range(total_pages))
    
    # Validate page numbers
    valid_page_numbers = [p for p in page_numbers if 0 <= p < total_pages]
    
    # Apply crop to specified pages
    for page_num in valid_page_numbers:
        page = pdf_document[page_num]
        
        # Create a rectangle for the crop box
        crop_rect = fitz.Rect(crop_box)
        
        # Set the crop box
        page.set_cropbox(crop_rect)
    
    # Save the cropped PDF
    pdf_document.save(output_path)
    pdf_document.close()
    
    return output_path


def compress_pdf(input_path: str, output_path: str, compression_level: str = "medium") -> str:
    """
    Compress a PDF file to reduce its size
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the compressed PDF will be saved
        compression_level: Level of compression ("low", "medium", "high")
    
    Returns:
        Path to the compressed PDF file
    """
    # Define compression parameters based on level
    if compression_level == "low":
        image_dpi = 150
        jpeg_quality = 70
    elif compression_level == "medium":
        image_dpi = 120
        jpeg_quality = 60
    elif compression_level == "high":
        image_dpi = 90
        jpeg_quality = 50
    else:  # Default to medium
        image_dpi = 120
        jpeg_quality = 60
    
    # Open the PDF document
    pdf_document = fitz.open(input_path)
    
    # Process each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get the page's images
        image_list = page.get_images(full=True)
        
        # If the page has images, process them
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]  # Get the image reference
            
            # Extract the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Process the image with PIL
            with Image.open(io.BytesIO(image_bytes)) as img:
                # Calculate new size based on DPI reduction
                original_width, original_height = img.size
                original_dpi = base_image.get("dpi", (300, 300))
                scale_factor = image_dpi / max(original_dpi)
                
                if scale_factor < 1:  # Only resize if we're reducing the image
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    
                    # Resize the image
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Convert to RGB if RGBA (to avoid JPEG issues)
                    if img.mode == "RGBA":
                        img = img.convert("RGB")
                    
                    # Save the compressed image to a buffer
                    output_buffer = io.BytesIO()
                    img.save(output_buffer, format="JPEG", quality=jpeg_quality, optimize=True)
                    output_buffer.seek(0)
                    
                    # Replace the image in the PDF
                    pdf_document.replace_image(xref, output_buffer.getvalue())
    
    # Save with reduced size
    pdf_document.save(output_path, garbage=4, deflate=True, clean=True)
    pdf_document.close()
    
    return output_path
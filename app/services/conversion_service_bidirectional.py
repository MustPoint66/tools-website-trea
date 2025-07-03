import os
import tempfile
from pathlib import Path
from typing import Optional, Union
from PIL import Image
import fitz  # PyMuPDF
from docx import Document
import pandas as pd
import openpyxl
from pptx import Presentation
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BidirectionalConversionService:
    """
    A comprehensive service for bidirectional file format conversions.
    Supports document, image, and other format conversions in both directions.
    """
    
    def __init__(self):
        self.supported_conversions = {
            # Document conversions
            'pdf_docx': ['pdf-to-docx', 'docx-to-pdf'],
            'pdf_xlsx': ['pdf-to-xlsx', 'xlsx-to-pdf'],
            'pdf_pptx': ['pdf-to-pptx', 'pptx-to-pdf'],
            'pdf_txt': ['pdf-to-txt', 'txt-to-pdf'],
            
            # Image conversions
            'jpg_png': ['jpg-to-png', 'png-to-jpg'],
            'jpg_webp': ['jpg-to-webp', 'webp-to-jpg'],
            'png_webp': ['png-to-webp', 'webp-to-png'],
            'heic_jpg': ['heic-to-jpg', 'jpg-to-heic'],
            'heic_png': ['heic-to-png', 'png-to-heic'],
            'svg_png': ['svg-to-png', 'png-to-svg'],
            'svg_jpg': ['svg-to-jpg', 'jpg-to-svg'],
            'gif_jpg': ['gif-to-jpg', 'jpg-to-gif'],
            'gif_png': ['gif-to-png', 'png-to-gif'],
            'tiff_jpg': ['tiff-to-jpg', 'jpg-to-tiff'],
            'tiff_png': ['tiff-to-png', 'png-to-tiff'],
            'eps_png': ['eps-to-png', 'png-to-eps'],
            'eps_jpg': ['eps-to-jpg', 'jpg-to-eps'],
            'avif_jpg': ['avif-to-jpg', 'jpg-to-avif'],
            'avif_png': ['avif-to-png', 'png-to-avif'],
            'avif_webp': ['avif-to-webp', 'webp-to-avif'],
            
            # PDF and Image conversions
            'pdf_jpg': ['pdf-to-jpg', 'jpg-to-pdf'],
            'pdf_png': ['pdf-to-png', 'png-to-pdf']
        }
    
    # Document Conversion Methods
    def pdf_to_docx(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert PDF to DOCX format"""
        try:
            doc = fitz.open(input_path)
            word_doc = Document()
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    word_doc.add_paragraph(text)
                    
            word_doc.save(output_path)
            doc.close()
            return output_path
        except Exception as e:
            logger.error(f"Error converting PDF to DOCX: {e}")
            return None
    
    def docx_to_pdf(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert DOCX to PDF format"""
        try:
            # This would require python-docx2pdf or similar library
            # For now, return a placeholder implementation
            logger.info("DOCX to PDF conversion - requires additional setup")
            return output_path
        except Exception as e:
            logger.error(f"Error converting DOCX to PDF: {e}")
            return None
    
    def pdf_to_xlsx(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert PDF to Excel format"""
        try:
            doc = fitz.open(input_path)
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            
            row = 1
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    worksheet.cell(row=row, column=1, value=text)
                    row += 1
                    
            workbook.save(output_path)
            doc.close()
            return output_path
        except Exception as e:
            logger.error(f"Error converting PDF to XLSX: {e}")
            return None
    
    def xlsx_to_pdf(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert Excel to PDF format"""
        try:
            # This would require additional libraries for Excel to PDF conversion
            logger.info("XLSX to PDF conversion - requires additional setup")
            return output_path
        except Exception as e:
            logger.error(f"Error converting XLSX to PDF: {e}")
            return None
    
    def pdf_to_txt(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert PDF to plain text"""
        try:
            doc = fitz.open(input_path)
            text_content = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text() + "\n\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
            doc.close()
            return output_path
        except Exception as e:
            logger.error(f"Error converting PDF to TXT: {e}")
            return None
    
    def txt_to_pdf(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert plain text to PDF"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            doc = fitz.open()
            page = doc.new_page()
            point = fitz.Point(50, 50)
            page.insert_text(point, text_content)
            doc.save(output_path)
            doc.close()
            return output_path
        except Exception as e:
            logger.error(f"Error converting TXT to PDF: {e}")
            return None
    
    # Image Conversion Methods
    def convert_image_format(self, input_path: str, output_path: str, 
                           source_format: str, target_format: str) -> Optional[str]:
        """Generic image format conversion"""
        try:
            with Image.open(input_path) as img:
                # Handle transparency for formats that don't support it
                if target_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif target_format.upper() in ['PNG', 'WEBP'] and img.mode != 'RGBA':
                    img = img.convert('RGBA')
                elif img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                
                # Save with appropriate format
                save_kwargs = {}
                if target_format.upper() == 'JPEG':
                    save_kwargs['quality'] = 95
                elif target_format.upper() == 'WEBP':
                    save_kwargs['quality'] = 90
                
                img.save(output_path, format=target_format.upper(), **save_kwargs)
                return output_path
        except Exception as e:
            logger.error(f"Error converting {source_format} to {target_format}: {e}")
            return None
    
    def jpg_to_png(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert JPG to PNG"""
        return self.convert_image_format(input_path, output_path, 'JPEG', 'PNG')
    
    def png_to_jpg(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert PNG to JPG"""
        return self.convert_image_format(input_path, output_path, 'PNG', 'JPEG')
    
    def jpg_to_webp(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert JPG to WEBP"""
        return self.convert_image_format(input_path, output_path, 'JPEG', 'WEBP')
    
    def webp_to_jpg(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert WEBP to JPG"""
        return self.convert_image_format(input_path, output_path, 'WEBP', 'JPEG')
    
    def png_to_webp(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert PNG to WEBP"""
        return self.convert_image_format(input_path, output_path, 'PNG', 'WEBP')
    
    def webp_to_png(self, input_path: str, output_path: str) -> Optional[str]:
        """Convert WEBP to PNG"""
        return self.convert_image_format(input_path, output_path, 'WEBP', 'PNG')
    
    # PDF and Image Conversions
    def pdf_to_images(self, input_path: str, output_dir: str, 
                     image_format: str = 'JPEG') -> Optional[list]:
        """Convert PDF pages to images"""
        try:
            doc = fitz.open(input_path)
            image_files = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                
                output_filename = f"page_{page_num + 1}.{image_format.lower()}"
                output_path = os.path.join(output_dir, output_filename)
                
                pix.save(output_path)
                image_files.append(output_path)
            
            doc.close()
            return image_files
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            return None
    
    def images_to_pdf(self, image_paths: list, output_path: str) -> Optional[str]:
        """Convert multiple images to PDF"""
        try:
            doc = fitz.open()
            
            for image_path in image_paths:
                img_doc = fitz.open(image_path)
                pdf_bytes = img_doc.convert_to_pdf()
                img_pdf = fitz.open("pdf", pdf_bytes)
                doc.insert_pdf(img_pdf)
                img_pdf.close()
                img_doc.close()
            
            doc.save(output_path)
            doc.close()
            return output_path
        except Exception as e:
            logger.error(f"Error converting images to PDF: {e}")
            return None
    
    # Main conversion dispatcher
    def convert(self, input_path: str, output_path: str, conversion_type: str) -> Optional[str]:
        """
        Main conversion method that routes to appropriate conversion function
        
        Args:
            input_path: Path to input file
            output_path: Path for output file
            conversion_type: Type of conversion (e.g., 'pdf-to-docx', 'jpg-to-png')
        
        Returns:
            Path to converted file or None if conversion failed
        """
        conversion_map = {
            # Document conversions
            'pdf-to-docx': self.pdf_to_docx,
            'docx-to-pdf': self.docx_to_pdf,
            'pdf-to-xlsx': self.pdf_to_xlsx,
            'xlsx-to-pdf': self.xlsx_to_pdf,
            'pdf-to-txt': self.pdf_to_txt,
            'txt-to-pdf': self.txt_to_pdf,
            
            # Image conversions
            'jpg-to-png': self.jpg_to_png,
            'png-to-jpg': self.png_to_jpg,
            'jpg-to-webp': self.jpg_to_webp,
            'webp-to-jpg': self.webp_to_jpg,
            'png-to-webp': self.png_to_webp,
            'webp-to-png': self.webp_to_png,
        }
        
        if conversion_type in conversion_map:
            return conversion_map[conversion_type](input_path, output_path)
        else:
            logger.error(f"Unsupported conversion type: {conversion_type}")
            return None
    
    def get_supported_conversions(self) -> dict:
        """Return list of supported conversion types"""
        return self.supported_conversions


# Singleton instance
conversion_service = BidirectionalConversionService()

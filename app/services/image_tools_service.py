import os
from PIL import Image, UnidentifiedImageError
from typing import Optional
from pdf2image import convert_from_path
import io

def convert_heic_to_jpg(input_path: str, output_path: str) -> Optional[str]:
    """
    Convert a HEIC image to JPG format.
    """
    try:
        image = Image.open(input_path)
        image = image.convert('RGB')
        image.save(output_path, 'JPEG')
        return output_path
    except UnidentifiedImageError as e:
        print(f"Error converting HEIC to JPG: {e}")
        return None

def upscale_image(input_path: str, output_path: str, scale_factor: int = 2) -> Optional[str]:
    """
    Upscale an image by a given scale_factor using nearest-neighbor approach.
    """
    try:
        image = Image.open(input_path)
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        upscaled_image = image.resize(new_size, Image.NEAREST)
        upscaled_image.save(output_path)
        return output_path
    except UnidentifiedImageError as e:
        print(f"Error upscaling image: {e}")
        return None

def compress_image(input_path: str, output_path: str, quality: int = 85) -> Optional[str]:
    """
    Compress an image to reduce file size.
    """
    try:
        image = Image.open(input_path)
        image.save(output_path, quality=quality)
        return output_path
    except UnidentifiedImageError as e:
        print(f"Error compressing image: {e}")
        return None

def remove_background(input_path: str, output_path: str) -> Optional[str]:
    """
    Remove background from an image using a simple threshold-based approach.
    """
    try:
        image = Image.open(input_path)
        # For demonstration purposes, convert image to grayscale and threshold
        grayscale = image.convert('L')
        binary = grayscale.point(lambda x: 0 if x < 128 else 255, '1')
        binary.save(output_path)
        return output_path
    except UnidentifiedImageError as e:
        print(f"Error removing background: {e}")
        return None

def pdf_to_jpg(input_path: str, output_folder: str) -> Optional[list]:
    """
    Convert each page of a PDF to a JPG image.
    """
    try:
        images = convert_from_path(input_path)
        jpg_files = []
        for i, image in enumerate(images, start=1):
            jpg_path = os.path.join(output_folder, f"page_{i}.jpg")
            image.save(jpg_path, 'JPEG')
            jpg_files.append(jpg_path)
        return jpg_files
    except Exception as e:
        print(f"Error converting PDF to JPG: {e}")
        return None

# More tool functions can be implemented similarly...

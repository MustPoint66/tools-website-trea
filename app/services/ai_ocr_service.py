import os
import base64
from typing import Optional, List, Dict, Any
from openai import OpenAI
from app.config import settings

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to base64 string
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_openai_client():
    """
    Initialize and return an OpenAI client configured with OpenRouter
    """
    # Get API key from settings
    api_key = settings.OPENAI_API_KEY
    
    # Initialize OpenAI client with OpenRouter base URL
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://toolswebsite.com",  # Required by OpenRouter
            "X-Title": "Tools Website"  # Optional, helps OpenRouter identify your app
        }
    )
    
    return client

def ai_ocr_image(image_path: str, model: Optional[str] = None) -> str:
    """
    Perform OCR on an image using AI models via OpenRouter
    
    Args:
        image_path: Path to the image file
        model: AI model to use (defaults to settings.DEFAULT_MODEL)
        
    Returns:
        Extracted text as a string
    """
    try:
        # Get the client
        client = get_openai_client()
        
        # Use default model if none specified
        if not model:
            model = settings.DEFAULT_MODEL
        
        # Encode the image
        base64_image = encode_image_to_base64(image_path)
        
        # Create the API request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": "You are an OCR assistant. Extract all text from the provided image accurately. Only return the extracted text, nothing else."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this image:"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        # Extract the text from the response
        extracted_text = response.choices[0].message.content
        return extracted_text
    
    except Exception as e:
        print(f"Error performing AI OCR on image: {str(e)}")
        return ""

def ai_ocr_pdf(pdf_path: str, image_paths: List[str], model: Optional[str] = None) -> str:
    """
    Perform OCR on PDF images using AI models via OpenRouter
    
    Args:
        pdf_path: Path to the original PDF (for reference only)
        image_paths: List of paths to the extracted page images
        model: AI model to use (defaults to settings.DEFAULT_MODEL)
        
    Returns:
        Extracted text as a string
    """
    try:
        # Process each image and combine the results
        full_text = ""
        for i, image_path in enumerate(image_paths):
            page_text = ai_ocr_image(image_path, model=model)
            if page_text:
                full_text += f"--- Page {i+1} ---\n{page_text}\n\n"
        
        return full_text
    
    except Exception as e:
        print(f"Error performing AI OCR on PDF: {str(e)}")
        return ""
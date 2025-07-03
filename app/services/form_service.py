import os
import json
import fitz  # PyMuPDF
from typing import Dict, List, Any, Optional, Tuple
from app.config import settings

# Mock profile data for form filling
DEFAULT_PROFILE = {
    "personal": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "(555) 123-4567",
        "address": "123 Main Street",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
        "country": "USA",
        "birth_date": "01/01/1980",
        "ssn": "XXX-XX-XXXX"
    },
    "employment": {
        "company": "ACME Corporation",
        "title": "Software Engineer",
        "department": "Engineering",
        "manager": "Jane Smith",
        "start_date": "01/01/2020",
        "salary": "100000"
    },
    "education": {
        "university": "State University",
        "degree": "Bachelor of Science",
        "major": "Computer Science",
        "graduation_year": "2015"
    }
}

# Field type mapping for better form filling
FIELD_TYPE_MAPPING = {
    # Personal information
    "name": ["first_name", "last_name"],
    "full name": ["first_name", "last_name"],
    "firstname": ["first_name"],
    "first": ["first_name"],
    "lastname": ["last_name"],
    "last": ["last_name"],
    "email": ["email"],
    "phone": ["phone"],
    "telephone": ["phone"],
    "mobile": ["phone"],
    "address": ["address"],
    "street": ["address"],
    "city": ["city"],
    "state": ["state"],
    "province": ["state"],
    "zip": ["zip"],
    "zipcode": ["zip"],
    "postal": ["zip"],
    "country": ["country"],
    "birth": ["birth_date"],
    "dob": ["birth_date"],
    "ssn": ["ssn"],
    "social": ["ssn"],
    
    # Employment information
    "company": ["company"],
    "employer": ["company"],
    "title": ["title"],
    "position": ["title"],
    "job": ["title"],
    "department": ["department"],
    "dept": ["department"],
    "manager": ["manager"],
    "supervisor": ["manager"],
    "start": ["start_date"],
    "hire": ["start_date"],
    "salary": ["salary"],
    "income": ["salary"],
    "wage": ["salary"],
    
    # Education information
    "university": ["university"],
    "college": ["university"],
    "school": ["university"],
    "degree": ["degree"],
    "major": ["major"],
    "graduation": ["graduation_year"],
    "grad": ["graduation_year"]
}

def detect_form_fields(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Detect form fields in a PDF using PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with field information
    """
    fields = []
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Get all form fields
        for page_num, page in enumerate(doc):
            widgets = page.widgets()
            for widget in widgets:
                field = {
                    "name": widget.field_name or "",
                    "type": widget.field_type_string,
                    "value": widget.field_value or "",
                    "rect": list(widget.rect),  # Convert rect to list for JSON serialization
                    "page": page_num,
                    "options": widget.choice_values if hasattr(widget, "choice_values") else [],
                    "is_required": False,  # Default value, not easily detectable
                    "mapped_to": "",  # Will be filled later
                }
                fields.append(field)
        
        # Close the document
        doc.close()
    except Exception as e:
        print(f"Error detecting form fields: {str(e)}")
        return []
    
    # Map fields to profile data
    for field in fields:
        field["mapped_to"] = map_field_to_profile(field["name"])
    
    return fields

def map_field_to_profile(field_name: str) -> str:
    """
    Map a form field name to a profile field.
    
    Args:
        field_name: Name of the form field
        
    Returns:
        Mapped profile field path (e.g., "personal.first_name")
    """
    if not field_name:
        return ""
    
    # Convert to lowercase for better matching
    field_name_lower = field_name.lower()
    
    # Check for exact matches in the mapping
    for key, values in FIELD_TYPE_MAPPING.items():
        if key in field_name_lower:
            value = values[0]  # Take the first mapping
            
            # Determine which category the field belongs to
            if value in DEFAULT_PROFILE["personal"]:
                return f"personal.{value}"
            elif value in DEFAULT_PROFILE["employment"]:
                return f"employment.{value}"
            elif value in DEFAULT_PROFILE["education"]:
                return f"education.{value}"
    
    return ""  # No mapping found

def fill_form(pdf_path: str, output_path: str, field_values: Dict[str, str] = None) -> bool:
    """
    Fill a PDF form with provided values or default profile data.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path to save the filled PDF
        field_values: Dictionary of field names and values to fill
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # If no field values provided, use default profile
        if not field_values:
            field_values = {}
        
        # Get all form fields
        for page in doc:
            widgets = page.widgets()
            for widget in widgets:
                field_name = widget.field_name
                
                # Skip if field has no name
                if not field_name:
                    continue
                
                # Check if value is provided in field_values
                if field_name in field_values:
                    widget.field_value = field_values[field_name]
                    widget.update()
                else:
                    # Try to fill with default profile data
                    mapped_field = map_field_to_profile(field_name)
                    if mapped_field:
                        category, field = mapped_field.split(".")
                        value = DEFAULT_PROFILE[category][field]
                        widget.field_value = value
                        widget.update()
        
        # Save the filled PDF
        doc.save(output_path)
        doc.close()
        
        return True
    except Exception as e:
        print(f"Error filling form: {str(e)}")
        return False

def get_form_preview(pdf_path: str, field_values: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Get a preview of how the form would be filled.
    
    Args:
        pdf_path: Path to the PDF file
        field_values: Dictionary of field names and values to fill
        
    Returns:
        Dictionary with field information and preview values
    """
    # Detect form fields
    fields = detect_form_fields(pdf_path)
    
    # If no field values provided, use empty dict
    if not field_values:
        field_values = {}
    
    # Add preview values to fields
    for field in fields:
        field_name = field["name"]
        
        # Check if value is provided in field_values
        if field_name in field_values:
            field["preview_value"] = field_values[field_name]
        else:
            # Try to fill with default profile data
            mapped_field = field["mapped_to"]
            if mapped_field:
                category, field_key = mapped_field.split(".")
                field["preview_value"] = DEFAULT_PROFILE[category][field_key]
            else:
                field["preview_value"] = ""
    
    return {
        "fields": fields,
        "profile": DEFAULT_PROFILE
    }

def update_profile(profile_data: Dict[str, Dict[str, str]]) -> bool:
    """
    Update the default profile with new data.
    
    Args:
        profile_data: New profile data
        
    Returns:
        True if successful, False otherwise
    """
    global DEFAULT_PROFILE
    
    try:
        # Update each category in the profile
        for category, data in profile_data.items():
            if category in DEFAULT_PROFILE:
                # Update only existing fields
                for field, value in data.items():
                    if field in DEFAULT_PROFILE[category]:
                        DEFAULT_PROFILE[category][field] = value
        
        return True
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return False
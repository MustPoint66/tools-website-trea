import os
import json
import shutil
import uuid
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF
from app.config import settings
from app.services.form_service import detect_form_fields, fill_form

# Define the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Template categories
TEMPLATE_CATEGORIES = {
    "resume": "Resume Templates",
    "cv": "CV Templates",
    "cover_letter": "Cover Letter Templates",
    "invoice": "Invoice Templates",
    "contract": "Contract Templates",
    "business": "Business Documents",
    "personal": "Personal Documents",
    "legal": "Legal Documents",
    "academic": "Academic Documents",
    "other": "Other Templates"
}

# Template metadata structure
class TemplateMetadata:
    def __init__(self, 
                 template_id: str,
                 name: str,
                 description: str,
                 category: str,
                 tags: List[str],
                 preview_image: str,
                 file_path: str):
        self.template_id = template_id
        self.name = name
        self.description = description
        self.category = category
        self.tags = tags
        self.preview_image = preview_image
        self.file_path = file_path
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "preview_image": self.preview_image,
            "file_path": self.file_path
        }

# Sample templates data
SAMPLE_TEMPLATES = [
    {
        "template_id": "resume-basic",
        "name": "Basic Resume",
        "description": "A clean, simple resume template suitable for most job applications.",
        "category": "resume",
        "tags": ["simple", "professional", "clean"],
        "preview_image": "resume-basic.png",
        "file_path": "resume/basic-resume.pdf"
    },
    {
        "template_id": "resume-creative",
        "name": "Creative Resume",
        "description": "A modern, creative resume template for design and creative roles.",
        "category": "resume",
        "tags": ["creative", "modern", "design"],
        "preview_image": "resume-creative.png",
        "file_path": "resume/creative-resume.pdf"
    },
    {
        "template_id": "cv-academic",
        "name": "Academic CV",
        "description": "Comprehensive CV template for academic and research positions.",
        "category": "cv",
        "tags": ["academic", "research", "detailed"],
        "preview_image": "cv-academic.png",
        "file_path": "cv/academic-cv.pdf"
    },
    {
        "template_id": "invoice-standard",
        "name": "Standard Invoice",
        "description": "Professional invoice template for businesses.",
        "category": "invoice",
        "tags": ["business", "finance", "professional"],
        "preview_image": "invoice-standard.png",
        "file_path": "invoice/standard-invoice.pdf"
    },
    {
        "template_id": "contract-employment",
        "name": "Employment Contract",
        "description": "Standard employment contract template.",
        "category": "contract",
        "tags": ["legal", "employment", "business"],
        "preview_image": "contract-employment.png",
        "file_path": "contract/employment-contract.pdf"
    },
    {
        "template_id": "contract-nda",
        "name": "Non-Disclosure Agreement",
        "description": "Standard NDA template for business confidentiality.",
        "category": "contract",
        "tags": ["legal", "confidentiality", "business"],
        "preview_image": "contract-nda.png",
        "file_path": "contract/nda-contract.pdf"
    },
    {
        "template_id": "cover-letter-basic",
        "name": "Basic Cover Letter",
        "description": "Simple, professional cover letter template.",
        "category": "cover_letter",
        "tags": ["simple", "professional", "job application"],
        "preview_image": "cover-letter-basic.png",
        "file_path": "cover_letter/basic-cover-letter.pdf"
    },
    {
        "template_id": "invoice-freelance",
        "name": "Freelance Invoice",
        "description": "Invoice template designed for freelancers and contractors.",
        "category": "invoice",
        "tags": ["freelance", "contractor", "simple"],
        "preview_image": "invoice-freelance.png",
        "file_path": "invoice/freelance-invoice.pdf"
    },
    {
        "template_id": "business-letterhead",
        "name": "Business Letterhead",
        "description": "Professional letterhead template for business correspondence.",
        "category": "business",
        "tags": ["letterhead", "correspondence", "professional"],
        "preview_image": "business-letterhead.png",
        "file_path": "business/letterhead.pdf"
    },
    {
        "template_id": "legal-will",
        "name": "Last Will and Testament",
        "description": "Basic will template for personal estate planning.",
        "category": "legal",
        "tags": ["will", "estate", "personal"],
        "preview_image": "legal-will.png",
        "file_path": "legal/will-template.pdf"
    }
]

# Initialize templates directory with sample templates
def initialize_templates():
    """Initialize the templates directory with sample templates if it doesn't exist."""
    # Create metadata file if it doesn't exist
    metadata_path = os.path.join(TEMPLATES_DIR, "metadata.json")
    if not os.path.exists(metadata_path):
        # Create template subdirectories
        for category in TEMPLATE_CATEGORIES.keys():
            os.makedirs(os.path.join(TEMPLATES_DIR, category), exist_ok=True)
        
        # Save metadata
        with open(metadata_path, "w") as f:
            json.dump(SAMPLE_TEMPLATES, f, indent=4)

# Call initialization
initialize_templates()

def get_all_templates() -> List[Dict[str, Any]]:
    """Get all available templates."""
    metadata_path = os.path.join(TEMPLATES_DIR, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            return json.load(f)
    return []

def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
    """Get templates filtered by category."""
    templates = get_all_templates()
    return [t for t in templates if t["category"] == category]

def get_template_by_id(template_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific template by ID."""
    templates = get_all_templates()
    for template in templates:
        if template["template_id"] == template_id:
            return template
    return None

def get_template_categories() -> Dict[str, str]:
    """Get all template categories."""
    return TEMPLATE_CATEGORIES

def get_template_path(template_id: str) -> Optional[str]:
    """Get the file path for a template."""
    template = get_template_by_id(template_id)
    if template:
        return os.path.join(TEMPLATES_DIR, template["file_path"])
    return None

def get_template_fields(template_id: str) -> List[Dict[str, Any]]:
    """Get form fields for a specific template."""
    template_path = get_template_path(template_id)
    if not template_path or not os.path.exists(template_path):
        return []
    
    return detect_form_fields(template_path)

def fill_template(template_id: str, field_values: Dict[str, str], output_path: str) -> bool:
    """Fill a template with provided values."""
    template_path = get_template_path(template_id)
    if not template_path or not os.path.exists(template_path):
        return False
    
    return fill_form(template_path, output_path, field_values)

def add_template(name: str, description: str, category: str, tags: List[str], 
                 file_path: str, preview_image_path: Optional[str] = None) -> str:
    """Add a new template to the collection."""
    # Generate a unique ID
    template_id = f"{category}-{str(uuid.uuid4())[:8]}"
    
    # Determine target paths
    target_dir = os.path.join(TEMPLATES_DIR, category)
    os.makedirs(target_dir, exist_ok=True)
    
    # Get filename from path
    filename = os.path.basename(file_path)
    target_file_path = os.path.join(category, filename)
    full_target_path = os.path.join(TEMPLATES_DIR, target_file_path)
    
    # Copy the template file
    shutil.copy2(file_path, full_target_path)
    
    # Handle preview image
    preview_filename = f"{template_id}.png"
    preview_path = os.path.join(category, preview_filename)
    
    if preview_image_path and os.path.exists(preview_image_path):
        # Copy provided preview image
        full_preview_path = os.path.join(TEMPLATES_DIR, preview_path)
        shutil.copy2(preview_image_path, full_preview_path)
    else:
        # Generate preview image from first page of PDF
        try:
            doc = fitz.open(full_target_path)
            if doc.page_count > 0:
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
                full_preview_path = os.path.join(TEMPLATES_DIR, preview_path)
                pix.save(full_preview_path)
            doc.close()
        except Exception as e:
            print(f"Error generating preview: {str(e)}")
            preview_path = ""
    
    # Create template metadata
    new_template = {
        "template_id": template_id,
        "name": name,
        "description": description,
        "category": category,
        "tags": tags,
        "preview_image": preview_path,
        "file_path": target_file_path
    }
    
    # Update metadata file
    templates = get_all_templates()
    templates.append(new_template)
    
    metadata_path = os.path.join(TEMPLATES_DIR, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(templates, f, indent=4)
    
    return template_id

def delete_template(template_id: str) -> bool:
    """Delete a template from the collection."""
    template = get_template_by_id(template_id)
    if not template:
        return False
    
    # Delete the template file
    template_path = os.path.join(TEMPLATES_DIR, template["file_path"])
    if os.path.exists(template_path):
        os.remove(template_path)
    
    # Delete the preview image
    if template["preview_image"]:
        preview_path = os.path.join(TEMPLATES_DIR, template["preview_image"])
        if os.path.exists(preview_path):
            os.remove(preview_path)
    
    # Update metadata file
    templates = get_all_templates()
    templates = [t for t in templates if t["template_id"] != template_id]
    
    metadata_path = os.path.join(TEMPLATES_DIR, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(templates, f, indent=4)
    
    return True

def search_templates(query: str) -> List[Dict[str, Any]]:
    """Search templates by name, description, or tags."""
    templates = get_all_templates()
    query = query.lower()
    
    results = []
    for template in templates:
        # Check if query matches name, description, or tags
        if (query in template["name"].lower() or 
            query in template["description"].lower() or 
            any(query in tag.lower() for tag in template["tags"])):
            results.append(template)
    
    return results
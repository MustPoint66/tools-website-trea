from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import pdf_routes, conversion_routes, ocr_routes, chat_routes, form_routes, table_routes, workflow_routes, template_routes, editor_routes
from app.config import settings
import os

# Enhanced OpenAPI documentation metadata
api_description = """
## Privacy-First Document Processing Platform

A comprehensive suite of document processing tools designed with privacy and security at its core.

### Key Features
- **Privacy-First**: No cloud storage, files auto-deleted after processing
- **40+ Tools**: PDF manipulation, file conversion, OCR, AI chat, and more
- **Fast Processing**: Optimized for speed and efficiency
- **No Registration**: Use tools instantly without creating accounts
- **API Access**: RESTful APIs for developers

### Tool Categories
1. **PDF Tools**: Merge, split, compress, edit, convert PDFs
2. **File Conversion**: Convert between multiple file formats
3. **OCR Tools**: Extract text from images and scanned documents
4. **AI Chat**: Interactive PDF document analysis
5. **Form Processing**: Auto-fill and extract form data
6. **Table Extraction**: Extract structured data from documents
7. **Workflow Engine**: Chain multiple tools together
8. **Document Templates**: Generate documents from templates
9. **Document Editor**: Real-time collaborative editing

### Privacy & Security
- All processing happens locally or on secure servers
- Files are automatically deleted after processing
- No user data is stored or tracked
- GDPR and privacy regulation compliant
"""

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="Tools Website - Document Processing SaaS",
    description=api_description,
    version="1.0.0",
    terms_of_service="https://toolswebsite.com/terms",
    contact={
        "name": "Tools Website Support",
        "url": "https://toolswebsite.com/contact",
        "email": "support@toolswebsite.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "PDF Tools",
            "description": "Comprehensive PDF manipulation tools including merge, split, compress, and edit operations.",
        },
        {
            "name": "File Conversion",
            "description": "Convert between various file formats with high fidelity and fast processing.",
        },
        {
            "name": "OCR Tools",
            "description": "Optical Character Recognition tools to extract text from images and scanned documents.",
        },
        {
            "name": "AI PDF Chat",
            "description": "AI-powered document analysis and interactive chat with PDF content.",
        },
        {
            "name": "Auto Form Fill",
            "description": "Automatically fill forms and extract structured data from documents.",
        },
        {
            "name": "Table Extractor",
            "description": "Extract and structure table data from various document formats.",
        },
        {
            "name": "Tool Workflow Engine",
            "description": "Chain multiple document processing tools into automated workflows.",
        },
        {
            "name": "Document Templates",
            "description": "Generate documents from predefined templates with dynamic content.",
        },
        {
            "name": "Document Editor",
            "description": "Real-time collaborative document editing with rich formatting options.",
        },
    ],
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.toolswebsite.com",
            "description": "Production server"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdf_routes.router, prefix="/api/pdf", tags=["PDF Tools"])
app.include_router(conversion_routes.router, prefix="/api/conversion", tags=["File Conversion"])
app.include_router(ocr_routes.router, prefix="/api/ocr", tags=["OCR Tools"])
app.include_router(chat_routes.router, prefix="/api/chat-pdf", tags=["AI PDF Chat"])
app.include_router(form_routes.router, prefix="/api/form", tags=["Auto Form Fill"])
app.include_router(table_routes.router, prefix="/api/table", tags=["Table Extractor"])
app.include_router(workflow_routes.router, prefix="/api/workflow", tags=["Tool Workflow Engine"])
app.include_router(template_routes.router, prefix="/api/template", tags=["Document Templates"])
app.include_router(editor_routes.router, prefix="/api/editor", tags=["Document Editor"])

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Tools Website API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "redis_connected": True}  # TODO: Add actual Redis check

# Ensure temp directory exists
os.makedirs(settings.TEMP_DIR, exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
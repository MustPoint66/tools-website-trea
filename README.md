# Tools Website - Privacy-First Document Processing SaaS

A Python-based SaaS platform offering 40+ file tools such as PDF editing, document conversion, OCR, and image tools. The project is privacy-first: no user files are stored in the cloud. All processing happens in memory or in a temporary folder, and files are deleted immediately after the result is downloaded.

**API Documentation**: Visit `/docs` for interactive Swagger UI or `/redoc` for ReDoc documentation.

## 🚀 Features

### Core PDF Tools
- **PDF Merge**: Combine multiple PDFs into one
- **PDF Split**: Extract specific pages or split by page ranges
- **PDF Compress**: Reduce file size while maintaining quality
- **PDF Rotate**: Rotate pages individually or in bulk
- **PDF Watermark**: Add text or image watermarks
- **PDF Crop**: Remove unwanted margins and areas
- **PDF Protect**: Add password protection and permissions

### Advanced Document Processing
- **File Conversion**: PDF ⇄ Word, Excel, PPT, JPG, PNG, TXT
- **OCR**: Printed and Handwritten text from image or PDF
- **Intelligent Table Extractor**: PDF Table → Clean Excel
- **AI PDF Chat**: Chat with the document content (Premium)
- **Auto Form Fill**: Detect and fill PDF form fields
- **Tool Workflow Engine**: User defines steps: compress → sign → watermark (Premium)

### Privacy & User Experience
- **No-Cloud Mode**: Default setting: delete files instantly
- **Templates Hub**: Choose resume, contracts, etc. → fill → export
- **Live PDF Editor**: Drag/drop UI for page reorder, text add
- **QR Sync**: Generate link + QR to continue work on phone
- **AI Tool Assistant**: Suggest tools based on text prompt

## 🧱 Tech Stack

### Backend
- Python + FastAPI
- Celery + Redis (for long tasks like OCR)
- PyMuPDF, pdfplumber, pytesseract, reportlab, pdf2image, camelot, unoconv, LibreOffice
- FileResponse and StreamingResponse for downloads

### Frontend (Coming Soon)
- React (or Next.js) with Tailwind
- PDF.js for live PDF preview
- File drag/drop, conversion previews, QR code support

### Optional Services
- Neon (PostgreSQL)
- Prisma (ORM)
- Clerk (Authentication)
- Stripe (for billing)

## 📋 Setup Instructions

### Prerequisites

- Python 3.8+
- Redis (or Memurai for Windows)
- Node.js and npm (for frontend, coming soon)

### Installation

1. Clone the repository

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root (or use the existing one)

5. Start Redis/Memurai

### Running the Application

1. Start the FastAPI server:
   ```bash
   python run.py
   ```

2. Start the Celery worker (in a separate terminal):
   ```bash
   python worker.py
   ```

3. Access the API at http://localhost:8000

## 📝 API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints Overview

#### PDF Tools
- `POST /pdf/merge` - Merge multiple PDF files
- `POST /pdf/split` - Split PDF into separate pages or ranges
- `POST /pdf/compress` - Compress PDF file size
- `POST /pdf/rotate` - Rotate PDF pages
- `POST /pdf/watermark` - Add watermark to PDF
- `POST /pdf/crop` - Crop PDF pages
- `POST /pdf/protect` - Add password protection
- `POST /pdf/unlock` - Remove password protection

#### Document Conversion
- `POST /convert/pdf-to-word` - Convert PDF to Word document
- `POST /convert/pdf-to-excel` - Convert PDF to Excel spreadsheet
- `POST /convert/pdf-to-powerpoint` - Convert PDF to PowerPoint
- `POST /convert/pdf-to-image` - Convert PDF pages to images
- `POST /convert/word-to-pdf` - Convert Word to PDF
- `POST /convert/excel-to-pdf` - Convert Excel to PDF
- `POST /convert/powerpoint-to-pdf` - Convert PowerPoint to PDF
- `POST /convert/image-to-pdf` - Convert images to PDF

#### OCR & Text Processing
- `POST /ocr/extract-text` - Extract text from images or PDFs
- `POST /ocr/handwriting` - Extract handwritten text
- `POST /table/extract` - Extract tables from PDF to Excel

#### AI-Powered Features (Premium)
- `POST /ai/chat` - Chat with PDF content
- `POST /ai/summarize` - Summarize document content
- `POST /ai/translate` - Translate document text
- `POST /workflow/create` - Create custom tool workflow
- `POST /workflow/execute` - Execute workflow on files

#### Form & Template Tools
- `POST /form/detect-fields` - Detect form fields in PDF
- `POST /form/fill` - Auto-fill form fields
- `GET /templates/list` - List available templates
- `POST /templates/apply` - Apply template to data

#### Utility Endpoints
- `GET /health` - Health check
- `GET /tools/list` - List all available tools
- `POST /qr/generate` - Generate QR code for file sharing
- `GET /file/{file_id}` - Download processed file

### Example API Usage

#### Merge PDFs
```bash
curl -X POST "http://localhost:8000/pdf/merge" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@file1.pdf" \
  -F "files=@file2.pdf" \
  --output merged.pdf
```

#### Convert PDF to Word
```bash
curl -X POST "http://localhost:8000/convert/pdf-to-word" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  --output document.docx
```

#### Extract Text with OCR
```bash
curl -X POST "http://localhost:8000/ocr/extract-text" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg" \
  -F "language=eng"
```

### Response Format

All API endpoints return responses in the following format:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "file_url": "/download/abc123",
    "file_size": 1024,
    "processing_time": 1.23
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid file format",
  "details": "Only PDF files are supported for this operation"
}
```

## 🔒 Privacy First

This application follows strict privacy principles:

1. No user-uploaded files are stored in the cloud or on disk beyond temporary processing
2. Every upload is deleted after the response is sent
3. For memory-intensive tasks, processing happens in memory when possible
4. All tools are designed to be privacy-respecting by default

## 🧩 Project Structure

```
/
├── app/                    # Main application package
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── tasks/              # Celery tasks
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration
│   └── main.py             # FastAPI application
├── temp/                   # Temporary file storage (auto-created)
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── run.py                  # Script to run the server
└── worker.py               # Script to run the Celery worker
```

## 📊 Current Implementation Status

- [x] Project Bootstrap
- [x] PDF Merge Tool
- [ ] Additional PDF Tools
- [ ] File Conversion Module
- [ ] OCR Module
- [ ] AI PDF Chat
- [ ] Auto Form Fill
- [ ] Table Extractor
- [ ] Tool Workflow Engine
- [ ] Template Hub
- [ ] Live PDF Editor
- [ ] QR Sync
- [ ] Frontend Implementation

## 📄 License

This project is licensed under the MIT License.
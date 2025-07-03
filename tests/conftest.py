"""
Test configuration and fixtures for the Tools Website project.
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
import tempfile
import os
from pathlib import Path
from typing import Generator, AsyncGenerator
import asyncio

# Import your FastAPI app
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a sample PDF file for testing."""
    # This would create a minimal PDF for testing
    # For now, we'll just create a placeholder
    pdf_path = temp_dir / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n")
    return pdf_path


@pytest.fixture
def sample_text_file(temp_dir):
    """Create a sample text file for testing."""
    text_path = temp_dir / "sample.txt"
    text_path.write_text("This is a sample text file for testing.")
    return text_path


@pytest.fixture
def sample_image_path(temp_dir):
    """Create a sample image file for testing."""
    # Create a minimal PNG file
    image_path = temp_dir / "sample.png"
    # Minimal PNG header
    png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
    image_path.write_bytes(png_header)
    return image_path


@pytest.fixture
def mock_file_upload():
    """Create a mock file upload object."""
    from fastapi import UploadFile
    from io import BytesIO
    
    def _create_upload_file(filename: str, content: bytes, content_type: str = "application/octet-stream"):
        return UploadFile(
            filename=filename,
            file=BytesIO(content),
            headers={"content-type": content_type}
        )
    
    return _create_upload_file


@pytest.fixture
def api_headers():
    """Standard headers for API requests."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@pytest.fixture
def multipart_headers():
    """Headers for multipart form data requests."""
    return {
        "Accept": "application/json"
    }


# Test data fixtures
@pytest.fixture
def sample_pdf_data():
    """Sample PDF form data for testing."""
    return {
        "title": "Test Document",
        "author": "Test Author",
        "subject": "Test Subject"
    }


@pytest.fixture
def sample_ocr_data():
    """Sample OCR request data for testing."""
    return {
        "language": "en",
        "output_format": "text",
        "preprocessing": True
    }


@pytest.fixture
def sample_conversion_data():
    """Sample conversion request data for testing."""
    return {
        "input_format": "pdf",
        "output_format": "docx",
        "quality": "high"
    }


@pytest.fixture
def sample_workflow_data():
    """Sample workflow configuration for testing."""
    return {
        "name": "Test Workflow",
        "steps": [
            {"type": "pdf_split", "parameters": {"pages": "1-3"}},
            {"type": "ocr", "parameters": {"language": "en"}},
            {"type": "export", "parameters": {"format": "text"}}
        ]
    }


# Database fixtures (if using a database)
@pytest.fixture
def db_session():
    """Create a database session for testing."""
    # This would set up a test database session
    # For now, we'll just pass
    pass


# Environment setup
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Set up test environment variables."""
    test_env_vars = {
        "TESTING": "true",
        "LOG_LEVEL": "DEBUG",
        "UPLOAD_DIR": "/tmp/test_uploads",
        "MAX_FILE_SIZE": "10485760",  # 10MB
    }
    
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)


# Clean up fixtures
@pytest.fixture(autouse=True)
def cleanup_files():
    """Clean up any created files after tests."""
    created_files = []
    
    def track_file(filepath):
        created_files.append(filepath)
    
    yield track_file
    
    # Clean up after test
    for filepath in created_files:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass  # Ignore cleanup errors

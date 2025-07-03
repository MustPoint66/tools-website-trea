"""
Test cases for the main API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import json
import io
from pathlib import Path


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client: TestClient):
        """Test the health check endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Test root API endpoint."""
    
    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or "name" in data


class TestPDFEndpoints:
    """Test PDF-related endpoints."""
    
    @pytest.mark.pdf
    def test_pdf_upload_validation(self, client: TestClient):
        """Test PDF upload with invalid file."""
        # Test with no file
        response = client.post("/api/pdf/merge")
        assert response.status_code in [400, 422]  # Bad request or unprocessable entity
    
    @pytest.mark.pdf
    def test_pdf_merge_endpoint_exists(self, client: TestClient):
        """Test that PDF merge endpoint exists."""
        # Test endpoint exists (even if it returns error without proper data)
        response = client.post("/api/pdf/merge")
        # Should not return 404 (not found)
        assert response.status_code != 404
    
    @pytest.mark.pdf
    def test_pdf_split_endpoint_exists(self, client: TestClient):
        """Test that PDF split endpoint exists."""
        response = client.post("/api/pdf/split")
        assert response.status_code != 404
    
    @pytest.mark.pdf
    def test_pdf_compress_endpoint_exists(self, client: TestClient):
        """Test that PDF compress endpoint exists."""
        response = client.post("/api/pdf/compress")
        assert response.status_code != 404
    
    @pytest.mark.pdf
    def test_pdf_with_mock_file(self, client: TestClient, mock_file_upload):
        """Test PDF endpoint with mock file upload."""
        # Create a mock PDF file
        pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        files = {"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
        
        response = client.post("/api/pdf/compress", files=files)
        # Should not return 404, and should handle the request
        assert response.status_code != 404


class TestConversionEndpoints:
    """Test file conversion endpoints."""
    
    @pytest.mark.conversion
    def test_convert_endpoint_exists(self, client: TestClient):
        """Test that convert endpoint exists."""
        response = client.post("/api/convert")
        assert response.status_code != 404
    
    @pytest.mark.conversion
    def test_conversion_with_invalid_format(self, client: TestClient):
        """Test conversion with invalid format parameters."""
        data = {
            "input_format": "invalid",
            "output_format": "also_invalid"
        }
        response = client.post("/api/convert", json=data)
        # Should return some error, but not 404
        assert response.status_code != 404


class TestOCREndpoints:
    """Test OCR-related endpoints."""
    
    @pytest.mark.ocr
    def test_ocr_endpoint_exists(self, client: TestClient):
        """Test that OCR endpoint exists."""
        response = client.post("/api/ocr")
        assert response.status_code != 404
    
    @pytest.mark.ocr
    def test_ocr_with_mock_image(self, client: TestClient, mock_file_upload):
        """Test OCR endpoint with mock image."""
        # Create a mock image file
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
        files = {"file": ("test.png", io.BytesIO(image_content), "image/png")}
        
        response = client.post("/api/ocr", files=files)
        assert response.status_code != 404


class TestChatEndpoints:
    """Test AI chat endpoints."""
    
    @pytest.mark.api
    def test_chat_endpoint_exists(self, client: TestClient):
        """Test that chat endpoint exists."""
        response = client.post("/api/chat")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_chat_with_message(self, client: TestClient, api_headers):
        """Test chat endpoint with a message."""
        data = {
            "message": "Hello, how can you help me with PDFs?",
            "context": "pdf_tools"
        }
        response = client.post("/api/chat", json=data, headers=api_headers)
        # Should handle the request, even if it returns an error
        assert response.status_code != 404


class TestWorkflowEndpoints:
    """Test workflow engine endpoints."""
    
    @pytest.mark.api
    def test_workflow_create_endpoint(self, client: TestClient):
        """Test workflow creation endpoint."""
        response = client.post("/api/workflows")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_workflow_list_endpoint(self, client: TestClient):
        """Test workflow listing endpoint."""
        response = client.get("/api/workflows")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_workflow_execute_endpoint(self, client: TestClient, sample_workflow_data):
        """Test workflow execution endpoint."""
        # First try to create a workflow
        response = client.post("/api/workflows", json=sample_workflow_data)
        
        # Then try to execute (this might require workflow ID)
        response = client.post("/api/workflows/execute")
        assert response.status_code != 404


class TestFormEndpoints:
    """Test form-related endpoints."""
    
    @pytest.mark.api
    def test_forms_endpoint_exists(self, client: TestClient):
        """Test that forms endpoint exists."""
        response = client.get("/api/forms")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_form_create_endpoint(self, client: TestClient):
        """Test form creation endpoint."""
        form_data = {
            "name": "Test Form",
            "fields": [
                {"name": "email", "type": "email", "required": True},
                {"name": "message", "type": "textarea", "required": False}
            ]
        }
        response = client.post("/api/forms", json=form_data)
        assert response.status_code != 404


class TestTableEndpoints:
    """Test table processing endpoints."""
    
    @pytest.mark.api
    def test_tables_endpoint_exists(self, client: TestClient):
        """Test that tables endpoint exists."""
        response = client.get("/api/tables")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_table_extract_endpoint(self, client: TestClient):
        """Test table extraction endpoint."""
        response = client.post("/api/tables/extract")
        assert response.status_code != 404


class TestTemplateEndpoints:
    """Test template-related endpoints."""
    
    @pytest.mark.api
    def test_templates_endpoint_exists(self, client: TestClient):
        """Test that templates endpoint exists."""
        response = client.get("/api/templates")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_template_create_endpoint(self, client: TestClient):
        """Test template creation endpoint."""
        template_data = {
            "name": "Test Template",
            "content": "This is a test template with {{variable}}",
            "variables": ["variable"]
        }
        response = client.post("/api/templates", json=template_data)
        assert response.status_code != 404


class TestEditorEndpoints:
    """Test document editor endpoints."""
    
    @pytest.mark.api
    def test_editor_endpoint_exists(self, client: TestClient):
        """Test that editor endpoint exists."""
        response = client.get("/api/editor")
        assert response.status_code != 404
    
    @pytest.mark.api
    def test_editor_save_endpoint(self, client: TestClient):
        """Test editor save endpoint."""
        document_data = {
            "content": "This is test document content",
            "format": "markdown"
        }
        response = client.post("/api/editor/save", json=document_data)
        assert response.status_code != 404


class TestErrorHandling:
    """Test error handling across endpoints."""
    
    def test_404_for_nonexistent_endpoint(self, client: TestClient):
        """Test that non-existent endpoints return 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_405_for_wrong_method(self, client: TestClient):
        """Test method not allowed responses."""
        # Assuming /api/pdf/merge only accepts POST
        response = client.get("/api/pdf/merge")
        assert response.status_code in [404, 405]  # Not found or method not allowed
    
    def test_large_request_handling(self, client: TestClient):
        """Test handling of large requests."""
        # Create a large JSON payload
        large_data = {"data": "x" * 10000}  # 10KB of data
        response = client.post("/api/chat", json=large_data)
        # Should handle gracefully, not crash
        assert response.status_code != 500


@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Test endpoints with async client."""
    
    async def test_async_health_check(self, async_client: AsyncClient):
        """Test health check with async client."""
        response = await async_client.get("/health")
        assert response.status_code == 200
    
    async def test_async_chat_endpoint(self, async_client: AsyncClient):
        """Test chat endpoint with async client."""
        data = {"message": "Test message"}
        response = await async_client.post("/api/chat", json=data)
        assert response.status_code != 404


class TestSecurityHeaders:
    """Test security-related headers and responses."""
    
    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present."""
        response = client.options("/api/chat")
        # CORS headers should be present for OPTIONS requests
        assert "access-control-allow-origin" in response.headers or response.status_code == 404
    
    def test_security_headers(self, client: TestClient):
        """Test security headers in responses."""
        response = client.get("/health")
        # Common security headers
        headers = response.headers
        # At minimum, should not expose server details unnecessarily
        assert "Server" not in headers or "FastAPI" not in headers.get("Server", "")


class TestRateLimiting:
    """Test rate limiting if implemented."""
    
    @pytest.mark.integration
    def test_rate_limiting_behavior(self, client: TestClient):
        """Test that rate limiting works if implemented."""
        # Make multiple rapid requests
        responses = []
        for i in range(10):
            response = client.get("/health")
            responses.append(response.status_code)
        
        # Should not all fail with 500 errors
        assert not all(status == 500 for status in responses)
        # Most should succeed
        success_count = sum(1 for status in responses if status == 200)
        assert success_count >= 5  # At least half should succeed

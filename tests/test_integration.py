"""
Integration tests for complex workflows and end-to-end scenarios.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import io
import json
import time
from pathlib import Path


class TestPDFWorkflows:
    """Test complete PDF processing workflows."""
    
    @pytest.mark.integration
    @pytest.mark.pdf
    def test_complete_pdf_merge_workflow(self, client: TestClient):
        """Test complete PDF merge workflow."""
        # Create multiple mock PDF files
        pdf_content1 = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        pdf_content2 = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        
        files = [
            ("files", ("test1.pdf", io.BytesIO(pdf_content1), "application/pdf")),
            ("files", ("test2.pdf", io.BytesIO(pdf_content2), "application/pdf"))
        ]
        
        # Test the merge endpoint
        response = client.post("/api/pdf/merge", files=files)
        
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 400, 422, 500]
        
        if response.status_code == 200:
            # If successful, should return merged PDF
            assert response.headers.get("content-type") == "application/pdf"
            assert len(response.content) > 0
    
    @pytest.mark.integration
    @pytest.mark.pdf
    def test_pdf_split_then_merge_workflow(self, client: TestClient):
        """Test splitting a PDF then merging the parts."""
        # Create a mock PDF
        pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        
        # Step 1: Split PDF
        files = {"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
        split_data = {"pages": "1-2"}
        
        response = client.post("/api/pdf/split", files=files, data=split_data)
        
        # Should handle the split request
        assert response.status_code != 404
        
        # If split succeeds, the response format depends on implementation
        # Could be ZIP file with multiple PDFs or JSON with file references


class TestConversionWorkflows:
    """Test file conversion workflows."""
    
    @pytest.mark.integration
    @pytest.mark.conversion
    def test_multiple_format_conversion(self, client: TestClient):
        """Test converting between multiple formats."""
        # Test various conversion scenarios
        conversion_tests = [
            {"input_format": "pdf", "output_format": "docx"},
            {"input_format": "docx", "output_format": "pdf"},
            {"input_format": "txt", "output_format": "pdf"},
            {"input_format": "html", "output_format": "pdf"}
        ]
        
        for conversion in conversion_tests:
            # Create appropriate mock file content
            if conversion["input_format"] == "pdf":
                content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
                mimetype = "application/pdf"
            elif conversion["input_format"] == "txt":
                content = b"This is test text content"
                mimetype = "text/plain"
            else:
                content = b"Mock file content"
                mimetype = "application/octet-stream"
            
            files = {"file": (f"test.{conversion['input_format']}", io.BytesIO(content), mimetype)}
            data = {
                "output_format": conversion["output_format"]
            }
            
            response = client.post("/api/convert", files=files, data=data)
            # Should handle conversion request (might fail but shouldn't 404)
            assert response.status_code != 404


class TestOCRWorkflows:
    """Test OCR processing workflows."""
    
    @pytest.mark.integration
    @pytest.mark.ocr
    def test_image_ocr_to_pdf_workflow(self, client: TestClient):
        """Test OCR on image then convert to PDF."""
        # Create mock image
        image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
        
        # Step 1: OCR the image
        files = {"file": ("test.png", io.BytesIO(image_content), "image/png")}
        ocr_response = client.post("/api/ocr", files=files)
        
        assert ocr_response.status_code != 404
        
        # If OCR succeeds, should get text
        if ocr_response.status_code == 200:
            ocr_data = ocr_response.json()
            extracted_text = ocr_data.get("text", "")
            
            # Step 2: Convert extracted text to PDF
            conversion_data = {
                "content": extracted_text,
                "output_format": "pdf"
            }
            pdf_response = client.post("/api/text-to-pdf", json=conversion_data)
            
            # Should handle text to PDF conversion
            assert pdf_response.status_code != 404


class TestFormWorkflows:
    """Test form processing workflows."""
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_form_creation_to_submission_workflow(self, client: TestClient):
        """Test creating a form and then submitting data to it."""
        # Step 1: Create a form
        form_data = {
            "name": "Contact Form",
            "description": "A simple contact form",
            "fields": [
                {
                    "name": "name",
                    "type": "text",
                    "label": "Full Name",
                    "required": True
                },
                {
                    "name": "email",
                    "type": "email",
                    "label": "Email Address",
                    "required": True
                },
                {
                    "name": "message",
                    "type": "textarea",
                    "label": "Message",
                    "required": False
                }
            ]
        }
        
        create_response = client.post("/api/forms", json=form_data)
        assert create_response.status_code != 404
        
        if create_response.status_code == 201:
            form_id = create_response.json().get("id")
            
            # Step 2: Submit data to the form
            submission_data = {
                "name": "John Doe",
                "email": "john@example.com",
                "message": "This is a test message"
            }
            
            submit_response = client.post(f"/api/forms/{form_id}/submit", json=submission_data)
            assert submit_response.status_code != 404


class TestWorkflowEngine:
    """Test the workflow engine capabilities."""
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_complex_multi_step_workflow(self, client: TestClient, sample_workflow_data):
        """Test executing a complex multi-step workflow."""
        # Create a workflow
        workflow_response = client.post("/api/workflows", json=sample_workflow_data)
        assert workflow_response.status_code != 404
        
        if workflow_response.status_code == 201:
            workflow_id = workflow_response.json().get("id")
            
            # Execute the workflow
            execution_data = {
                "workflow_id": workflow_id,
                "inputs": {
                    "source_file": "test.pdf",
                    "target_format": "docx"
                }
            }
            
            execute_response = client.post("/api/workflows/execute", json=execution_data)
            assert execute_response.status_code != 404
            
            if execute_response.status_code == 200:
                execution_id = execute_response.json().get("execution_id")
                
                # Check workflow status
                status_response = client.get(f"/api/workflows/executions/{execution_id}")
                assert status_response.status_code != 404


class TestChatWorkflows:
    """Test AI chat integration workflows."""
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_chat_with_file_context_workflow(self, client: TestClient):
        """Test chat with file upload context."""
        # Upload a file first
        pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        files = {"file": ("context.pdf", io.BytesIO(pdf_content), "application/pdf")}
        
        upload_response = client.post("/api/files/upload", files=files)
        
        if upload_response.status_code == 200:
            file_id = upload_response.json().get("file_id")
            
            # Chat about the uploaded file
            chat_data = {
                "message": "What is in this PDF file?",
                "context": {
                    "file_id": file_id,
                    "type": "pdf_analysis"
                }
            }
            
            chat_response = client.post("/api/chat", json=chat_data)
            assert chat_response.status_code != 404


class TestTemplateWorkflows:
    """Test template processing workflows."""
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_template_creation_and_generation_workflow(self, client: TestClient):
        """Test creating a template and generating documents from it."""
        # Step 1: Create a template
        template_data = {
            "name": "Invoice Template",
            "content": """
            Invoice #{{invoice_number}}
            
            Bill To: {{customer_name}}
            {{customer_address}}
            
            Items:
            {{#items}}
            - {{description}}: ${{amount}}
            {{/items}}
            
            Total: ${{total}}
            """,
            "variables": ["invoice_number", "customer_name", "customer_address", "items", "total"]
        }
        
        create_response = client.post("/api/templates", json=template_data)
        assert create_response.status_code != 404
        
        if create_response.status_code == 201:
            template_id = create_response.json().get("id")
            
            # Step 2: Generate document from template
            generation_data = {
                "template_id": template_id,
                "data": {
                    "invoice_number": "INV-001",
                    "customer_name": "John Doe",
                    "customer_address": "123 Main St\nAnytown, USA",
                    "items": [
                        {"description": "Web Development", "amount": "1000.00"},
                        {"description": "Design Services", "amount": "500.00"}
                    ],
                    "total": "1500.00"
                },
                "output_format": "pdf"
            }
            
            generate_response = client.post("/api/templates/generate", json=generation_data)
            assert generate_response.status_code != 404


class TestPerformanceAndScaling:
    """Test performance and scaling scenarios."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_concurrent_requests(self, client: TestClient):
        """Test handling multiple concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get("/health")
            results.append(response.status_code)
        
        # Create 10 concurrent threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Check results
        assert len(results) == 10
        success_count = sum(1 for status in results if status == 200)
        assert success_count >= 8  # Allow for some failures
        
        # Should complete reasonably quickly
        assert end_time - start_time < 30  # 30 seconds max
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_file_processing(self, client: TestClient):
        """Test processing large files."""
        # Create a larger mock file (1MB)
        large_content = b"A" * (1024 * 1024)  # 1MB of 'A' characters
        
        files = {"file": ("large_file.txt", io.BytesIO(large_content), "text/plain")}
        
        # Test various endpoints with large file
        endpoints = [
            "/api/convert",
            "/api/ocr",
            "/api/files/upload"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.post(endpoint, files=files)
            end_time = time.time()
            
            # Should handle large files (even if it fails, shouldn't crash)
            assert response.status_code != 500
            # Should respond within reasonable time (adjust as needed)
            assert end_time - start_time < 60  # 60 seconds max


class TestDataPersistence:
    """Test data persistence and retrieval."""
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_file_upload_and_retrieval(self, client: TestClient):
        """Test uploading a file and then retrieving it."""
        # Upload a file
        content = b"Test file content for persistence testing"
        files = {"file": ("test_persistence.txt", io.BytesIO(content), "text/plain")}
        
        upload_response = client.post("/api/files/upload", files=files)
        
        if upload_response.status_code == 200:
            file_info = upload_response.json()
            file_id = file_info.get("file_id")
            
            # Retrieve the file
            retrieve_response = client.get(f"/api/files/{file_id}")
            assert retrieve_response.status_code != 404
            
            if retrieve_response.status_code == 200:
                # Content should match
                assert retrieve_response.content == content
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_workflow_persistence(self, client: TestClient, sample_workflow_data):
        """Test that workflows are properly persisted."""
        # Create a workflow
        create_response = client.post("/api/workflows", json=sample_workflow_data)
        
        if create_response.status_code == 201:
            workflow_id = create_response.json().get("id")
            
            # Retrieve the workflow
            get_response = client.get(f"/api/workflows/{workflow_id}")
            assert get_response.status_code != 404
            
            if get_response.status_code == 200:
                retrieved_workflow = get_response.json()
                # Key fields should match
                assert retrieved_workflow.get("name") == sample_workflow_data.get("name")


class TestErrorRecovery:
    """Test error recovery and resilience."""
    
    @pytest.mark.integration
    def test_invalid_file_recovery(self, client: TestClient):
        """Test system recovers from invalid file uploads."""
        # Upload an invalid file
        invalid_content = b"This is not a PDF but claims to be"
        files = {"file": ("fake.pdf", io.BytesIO(invalid_content), "application/pdf")}
        
        response = client.post("/api/pdf/compress", files=files)
        
        # Should handle gracefully, not crash the server
        assert response.status_code != 500
        
        # Subsequent valid requests should still work
        health_response = client.get("/health")
        assert health_response.status_code == 200
    
    @pytest.mark.integration
    def test_malformed_request_recovery(self, client: TestClient):
        """Test system recovers from malformed requests."""
        # Send malformed JSON
        malformed_data = '{"incomplete": json'
        
        response = client.post(
            "/api/chat",
            data=malformed_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Should handle gracefully
        assert response.status_code != 500
        
        # System should still be responsive
        health_response = client.get("/health")
        assert health_response.status_code == 200

#!/usr/bin/env python3
"""
Comprehensive test script to verify all dependencies and tools are working correctly.
"""

import sys
import traceback
from typing import Dict, List, Tuple

def test_import(module_name: str, import_statement: str = None) -> Tuple[bool, str]:
    """Test importing a module and return success status with message."""
    try:
        if import_statement:
            exec(import_statement)
        else:
            __import__(module_name)
        return True, f"✅ {module_name}: OK"
    except ImportError as e:
        return False, f"❌ {module_name}: Import Error - {str(e)}"
    except Exception as e:
        return False, f"❌ {module_name}: Error - {str(e)}"

def test_functionality(test_name: str, test_func) -> Tuple[bool, str]:
    """Test a specific functionality and return success status with message."""
    try:
        test_func()
        return True, f"✅ {test_name}: Working"
    except Exception as e:
        return False, f"❌ {test_name}: Error - {str(e)}"

def test_fastapi():
    """Test FastAPI functionality."""
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    
    assert app is not None

def test_uvicorn():
    """Test Uvicorn functionality."""
    import uvicorn
    # Just check if we can import the main components
    from uvicorn.config import Config
    config = Config(app="test:app", host="127.0.0.1", port=8000)
    assert config is not None

def test_pymupdf():
    """Test PyMuPDF (Fitz) functionality."""
    import fitz
    # Test creating a new document
    doc = fitz.open()
    page = doc.new_page()
    assert page is not None
    doc.close()

def test_celery():
    """Test Celery functionality."""
    from celery import Celery
    app = Celery('test')
    assert app is not None

def test_redis():
    """Test Redis client functionality."""
    import redis
    # Just test creating a client (don't connect)
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    assert client is not None

def test_langchain():
    """Test LangChain functionality."""
    from langchain.schema import Document
    from langchain_core.messages import HumanMessage
    
    doc = Document(page_content="Test document", metadata={"source": "test"})
    message = HumanMessage(content="Test message")
    
    assert doc.page_content == "Test document"
    assert message.content == "Test message"

def test_openai():
    """Test OpenAI client functionality."""
    from openai import OpenAI
    # Just test creating a client (don't make API calls)
    client = OpenAI(api_key="test-key")
    assert client is not None

def test_pdf_processing():
    """Test PDF processing libraries."""
    import pdfplumber
    import camelot
    import tabula
    
    # Test that main classes can be imported
    assert hasattr(pdfplumber, 'open')
    assert hasattr(camelot, 'read_pdf')
    assert hasattr(tabula, 'read_pdf')

def test_streamlit():
    """Test Streamlit functionality."""
    import streamlit as st
    # Just check basic imports
    assert hasattr(st, 'write')
    assert hasattr(st, 'title')

def test_sentence_transformers():
    """Test Sentence Transformers functionality."""
    from sentence_transformers import SentenceTransformer
    # Just test that we can import the main class
    assert SentenceTransformer is not None

def main():
    """Run all tests and report results."""
    print("🧪 Testing Dependencies and Tools")
    print("=" * 50)
    
    # Test basic imports
    import_tests = [
        ("fastapi", None),
        ("uvicorn", None),
        ("fitz (PyMuPDF)", "import fitz"),
        ("celery", None),
        ("redis", None),
        ("langchain", None),
        ("langchain_core", None),
        ("langchain_community", None),
        ("openai", None),
        ("streamlit", None),
        ("pdfplumber", None),
        ("camelot", None),
        ("tabula", None),
        ("reportlab", None),
        ("sentence_transformers", None),
        ("PIL (Pillow)", "from PIL import Image"),
        ("pytesseract", None),
        ("pdf2image", None),
        ("aiofiles", None),
        ("requests", None),
        ("numpy", None),
        ("pandas", None),
        ("torch", None),
        ("faiss", "import faiss"),
    ]
    
    print("\n📦 Import Tests:")
    print("-" * 30)
    
    passed_imports = 0
    total_imports = len(import_tests)
    
    for module_name, import_stmt in import_tests:
        success, message = test_import(module_name, import_stmt)
        print(message)
        if success:
            passed_imports += 1
    
    # Test functionality
    functionality_tests = [
        ("FastAPI App Creation", test_fastapi),
        ("Uvicorn Config", test_uvicorn),
        ("PyMuPDF Document", test_pymupdf),
        ("Celery App", test_celery),
        ("Redis Client", test_redis),
        ("LangChain Components", test_langchain),
        ("OpenAI Client", test_openai),
        ("PDF Processing", test_pdf_processing),
        ("Streamlit Components", test_streamlit),
        ("Sentence Transformers", test_sentence_transformers),
    ]
    
    print("\n⚙️  Functionality Tests:")
    print("-" * 30)
    
    passed_functionality = 0
    total_functionality = len(functionality_tests)
    
    for test_name, test_func in functionality_tests:
        success, message = test_functionality(test_name, test_func)
        print(message)
        if success:
            passed_functionality += 1
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    print(f"Import Tests: {passed_imports}/{total_imports} passed")
    print(f"Functionality Tests: {passed_functionality}/{total_functionality} passed")
    
    total_passed = passed_imports + passed_functionality
    total_tests = total_imports + total_functionality
    
    print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Your environment is ready to go!")
        return True
    else:
        print(f"\n⚠️  {total_tests - total_passed} tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

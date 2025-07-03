import os
import uuid
import json
import pdfplumber
import faiss
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS as LangchainFAISS
# from langchain_huggingface import HuggingFaceEmbeddings  # Temporarily disabled due to dependency issues
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
# from langchain_openai import OpenAI  # Temporarily disabled due to dependency issues
from app.config import settings

# Directory to store FAISS indexes
INDEX_DIR = os.path.join(settings.TEMP_DIR, "indexes")
os.makedirs(INDEX_DIR, exist_ok=True)

# Simple wrapper to make SentenceTransformer compatible with LangChain
class SimpleSentenceTransformerEmbeddings:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()
    
    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
langchain_embeddings = SimpleSentenceTransformerEmbeddings()

# Initialize text splitter for chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

# Initialize HuggingFace embeddings for LangChain

# Initialize OpenRouter LLM (compatible with OpenAI API)
llm = None
if settings.OPENAI_API_KEY:  # We'll use the same env var for OpenRouter key
    try:
        from openai import OpenAI
        # Configure for OpenRouter
        api_key = settings.OPENAI_API_KEY
        # Ensure we have a valid API key format
        if not api_key.startswith('sk-or-'):
            print(f"Warning: OpenRouter API key does not have the expected format. It should start with 'sk-or-'")
            # Use the hardcoded key from .env as fallback
            api_key = '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'
        
        llm = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://toolswebsite.com",  # Required by OpenRouter
                "X-Title": "Tools Website"  # Optional, but helps OpenRouter identify your app
            }
        )
    except ImportError:
        print("OpenAI library not available")

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text from the PDF
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""
    
    return text

def chunk_text(text: str) -> List[str]:
    """
    Split text into chunks using LangChain's text splitter.
    
    Args:
        text: Text to split into chunks
        
    Returns:
        List of text chunks
    """
    chunks = text_splitter.split_text(text)
    return chunks

def create_faiss_index(chunks: List[str], pdf_id: str) -> bool:
    """
    Create a FAISS index from text chunks and save it to disk.
    
    Args:
        chunks: List of text chunks
        pdf_id: Unique ID for the PDF
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create documents for LangChain
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        # Create FAISS index using LangChain
        vectorstore = LangchainFAISS.from_documents(documents, langchain_embeddings)
        
        # Save the index
        index_path = os.path.join(INDEX_DIR, pdf_id)
        vectorstore.save_local(index_path)
        
        # Save metadata
        metadata = {
            "pdf_id": pdf_id,
            "chunk_count": len(chunks),
            "created_at": str(uuid.uuid4())  # Using UUID as timestamp for simplicity
        }
        
        with open(os.path.join(index_path, "metadata.json"), "w") as f:
            json.dump(metadata, f)
            
        return True
    except Exception as e:
        print(f"Error creating FAISS index: {str(e)}")
        return False

def process_pdf_for_chat(pdf_path: str) -> str:
    """
    Process a PDF file for chat: extract text, chunk it, and create a FAISS index.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        PDF ID if successful, empty string otherwise
    """
    # Generate a unique ID for this PDF
    pdf_id = str(uuid.uuid4())
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return ""
    
    # Chunk the text
    chunks = chunk_text(text)
    if not chunks:
        return ""
    
    # Create FAISS index
    success = create_faiss_index(chunks, pdf_id)
    if not success:
        return ""
    
    return pdf_id

def query_pdf(pdf_id: str, question: str) -> Dict[str, Any]:
    """
    Query a PDF with a question using the FAISS index and LLM.
    
    Args:
        pdf_id: ID of the PDF to query
        question: Question to ask about the PDF
        
    Returns:
        Dictionary with answer and relevant chunks
    """
    # Check if PDF index exists
    index_path = os.path.join(INDEX_DIR, pdf_id)
    if not os.path.exists(index_path):
        return {
            "answer": "PDF not found. Please upload the PDF first.",
            "sources": []
        }
    
    try:
        # Load the FAISS index
        vectorstore = LangchainFAISS.load_local(index_path, langchain_embeddings)
        
        # Search for relevant documents
        docs = vectorstore.similarity_search(question, k=4)
        
        # Extract the content from the documents
        sources = [doc.page_content for doc in docs]
        
        # If OpenRouter/DeepSeek API is available, use it to generate an answer
        if llm and settings.OPENAI_API_KEY:
            try:
                # Prepare context from retrieved documents
                context = "\n\n".join([doc.page_content for doc in docs])
                
                # Create prompt for the LLM
                prompt = f"""Based on the following context from a PDF document, please answer the question.

Context:
{context}

Question: {question}

Answer:"""
                
                # Call OpenRouter API (DeepSeek)
                response = llm.chat.completions.create(
                    model=settings.DEFAULT_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions based on provided PDF content. Be accurate and cite specific parts of the content when possible."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                
            except Exception as e:
                answer = f"Error generating AI response: {str(e)}. Here are the relevant sections from the document:"
        else:
            # If no LLM is available, just return the most relevant chunks
            answer = "No AI model available. Here are the most relevant sections from the document:"
        
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        return {
            "answer": f"Error querying PDF: {str(e)}",
            "sources": []
        }

def list_available_pdfs() -> List[Dict[str, Any]]:
    """
    List all available PDFs that have been processed for chat.
    
    Returns:
        List of dictionaries with PDF IDs and metadata
    """
    pdfs = []
    
    # Check if index directory exists
    if not os.path.exists(INDEX_DIR):
        return pdfs
    
    # List all subdirectories in the index directory
    for pdf_id in os.listdir(INDEX_DIR):
        index_path = os.path.join(INDEX_DIR, pdf_id)
        
        # Check if it's a directory and has metadata
        if os.path.isdir(index_path) and os.path.exists(os.path.join(index_path, "metadata.json")):
            try:
                # Load metadata
                with open(os.path.join(index_path, "metadata.json"), "r") as f:
                    metadata = json.load(f)
                
                pdfs.append({
                    "pdf_id": pdf_id,
                    **metadata
                })
            except Exception:
                # Skip if metadata can't be loaded
                continue
    
    return pdfs

def delete_pdf_index(pdf_id: str) -> bool:
    """
    Delete a PDF index.
    
    Args:
        pdf_id: ID of the PDF to delete
        
    Returns:
        True if successful, False otherwise
    """
    index_path = os.path.join(INDEX_DIR, pdf_id)
    
    # Check if index exists
    if not os.path.exists(index_path):
        return False
    
    try:
        # Delete the index directory
        import shutil
        shutil.rmtree(index_path)
        return True
    except Exception as e:
        print(f"Error deleting PDF index: {str(e)}")
        return False
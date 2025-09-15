#!/usr/bin/env python3
"""
Simplified FastAPI server for Docling Parser
Document parsing API without advanced PDF options (for troubleshooting)
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

from docling.document_converter import DocumentConverter

# Models
class URLParseRequest(BaseModel):
    url: HttpUrl
    format: str = "markdown"  # markdown, json

class ParseResponse(BaseModel):
    success: bool
    message: str
    format: str
    content: str
    metadata: Optional[dict] = None

# FastAPI app
app = FastAPI(
    title="Docling Parser API (Simplified)",
    description="Simplified document parsing API using Docling library.",
    version="1.0.0-simple",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global converter instance
converter = DocumentConverter()

# Supported formats (simplified)
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.html', '.htm', '.png', '.jpg', '.jpeg', '.tiff']

def parse_document_content(file_path: str, format_type: str = "markdown") -> ParseResponse:
    """Parse document and return specified format (simplified version)."""
    try:
        # Use basic converter without advanced options
        result = converter.convert(file_path)
        
        # Export to requested format
        if format_type.lower() == "markdown":
            content = result.document.export_to_markdown()
        elif format_type.lower() == "json":
            content = result.document.export_to_dict()
        else:
            content = result.document.export_to_markdown()
            format_type = "markdown"
        
        # Get basic metadata
        metadata = {
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else None,
        }
        
        return ParseResponse(
            success=True,
            message="Document parsed successfully",
            format=format_type,
            content=content if isinstance(content, str) else str(content),
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing document: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Docling Parser API (Simplified)",
        "version": "1.0.0-simple",
        "docs": "/docs",
        "supported_extensions": SUPPORTED_EXTENSIONS,
        "endpoints": {
            "upload": "/upload",
            "parse_url": "/parse-url", 
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Docling Parser API (Simplified)"}

@app.post("/upload", response_model=ParseResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    format: str = Form("markdown")
):
    """
    Upload and parse a document file (simplified version).
    
    - **file**: Document file to parse
    - **format**: Output format (markdown, json)
    """
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported: {SUPPORTED_EXTENSIONS}"
        )
    
    # Create temporary file
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse document
        result = parse_document_content(temp_file_path, format)
        
        # Schedule cleanup
        background_tasks.add_task(shutil.rmtree, temp_dir)
        
        return result
        
    except Exception as e:
        # Cleanup on error
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

@app.post("/parse-url", response_model=ParseResponse)
async def parse_url(request: URLParseRequest):
    """
    Parse document from URL (simplified version).
    
    - **url**: URL to the document
    - **format**: Output format (markdown, json)
    """
    
    try:
        # Parse document from URL
        result = parse_document_content(str(request.url), request.format)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing URL: {str(e)}"
        )

@app.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats."""
    return {
        "supported_formats": {
            "input": SUPPORTED_EXTENSIONS,
            "output": ["markdown", "json"]
        },
        "note": "This is a simplified version. Advanced PDF options not available."
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, List
import mimetypes

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.format_option import PdfFormatOption

# Models
class URLParseRequest(BaseModel):
    url: HttpUrl
    format: str = "markdown"  # markdown, json, html
    enable_ocr: bool = False
    enable_table_structure: bool = True

class ParseResponse(BaseModel):
    success: bool
    message: str
    format: str
    content: str
    metadata: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None

# FastAPI app
app = FastAPI(
    title="Docling Parser API",
    description="Document parsing API using Docling library. Supports PDF, DOCX, PPTX, images and more.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global converter instance
converter = DocumentConverter()

# Supported formats mapping
SUPPORTED_FORMATS = {
    '.pdf': InputFormat.PDF,
    '.docx': InputFormat.DOCX,
    '.pptx': InputFormat.PPTX,
    '.html': InputFormat.HTML,
    '.htm': InputFormat.HTML,
    '.png': InputFormat.IMAGE,
    '.jpg': InputFormat.IMAGE,
    '.jpeg': InputFormat.IMAGE,
    '.tiff': InputFormat.IMAGE,
    '.tif': InputFormat.IMAGE,
}

def get_file_format(filename: str) -> Optional[InputFormat]:
    """Get input format from filename extension."""
    ext = Path(filename).suffix.lower()
    return SUPPORTED_FORMATS.get(ext)

def parse_document_content(file_path: str, format_type: str = "markdown", 
                          enable_ocr: bool = False, 
                          enable_table_structure: bool = True) -> ParseResponse:
    """Parse document and return specified format."""
    try:
        # Configure pipeline options for PDFs
        if file_path.lower().endswith('.pdf'):
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = enable_ocr
            pipeline_options.do_table_structure = enable_table_structure
            
            pdf_format_option = PdfFormatOption(pipeline_options=pipeline_options)
            local_converter = DocumentConverter(format_options={InputFormat.PDF: pdf_format_option})
        else:
            local_converter = converter
        
        # Convert document
        result = local_converter.convert(file_path)
        
        # Export to requested format
        if format_type.lower() == "markdown":
            content = result.document.export_to_markdown()
        elif format_type.lower() == "json":
            content = result.document.export_to_dict()
        elif format_type.lower() == "html":
            # If HTML export is available
            try:
                content = result.document.export_to_html()
            except AttributeError:
                content = result.document.export_to_markdown()
                format_type = "markdown"  # Fallback
        else:
            content = result.document.export_to_markdown()
            format_type = "markdown"
        
        # Get metadata
        metadata = {
            "num_pages": getattr(result.document, 'num_pages', None),
            "title": getattr(result.document, 'title', None),
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
        "message": "Docling Parser API",
        "version": "1.0.0",
        "docs": "/docs",
        "supported_formats": list(SUPPORTED_FORMATS.keys()),
        "endpoints": {
            "upload": "/upload",
            "parse_url": "/parse-url",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Docling Parser API"}

@app.post("/upload", response_model=ParseResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    format: str = Form("markdown"),
    enable_ocr: bool = Form(False),
    enable_table_structure: bool = Form(True)
):
    """
    Upload and parse a document file.
    
    - **file**: Document file to parse (PDF, DOCX, PPTX, images, etc.)
    - **format**: Output format (markdown, json, html)
    - **enable_ocr**: Enable OCR for image text extraction
    - **enable_table_structure**: Enable table structure detection
    """
    
    # Validate file format
    input_format = get_file_format(file.filename)
    if not input_format:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported: {list(SUPPORTED_FORMATS.keys())}"
        )
    
    # Create temporary file
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse document
        result = parse_document_content(
            temp_file_path, 
            format, 
            enable_ocr, 
            enable_table_structure
        )
        
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
    Parse document from URL.
    
    - **url**: URL to the document
    - **format**: Output format (markdown, json, html)
    - **enable_ocr**: Enable OCR for image text extraction
    - **enable_table_structure**: Enable table structure detection
    """
    
    try:
        # Parse document from URL
        result = parse_document_content(
            str(request.url),
            request.format,
            request.enable_ocr,
            request.enable_table_structure
        )
        
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
            "input": list(SUPPORTED_FORMATS.keys()),
            "output": ["markdown", "json", "html"]
        },
        "format_details": {
            "pdf": "Portable Document Format - supports OCR and table detection",
            "docx": "Microsoft Word documents",
            "pptx": "Microsoft PowerPoint presentations", 
            "html": "HTML web pages",
            "images": "PNG, JPEG, TIFF images - requires OCR for text extraction"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "available_endpoints": ["/", "/upload", "/parse-url", "/docs"]}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "Please check server logs"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

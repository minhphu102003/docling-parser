# Docling Parser API

FastAPI server for Docling Parser project - provides RESTful API for document parsing.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -e .
# or
uv sync
```

### 2. Run API Server
```bash
# Method 1: Using script
python start_api.py

# Method 2: Using command line
docling-api

# Method 3: Direct uvicorn
uvicorn api.main_simple:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000

## 📡 API Endpoints

### `GET /`
API information and available endpoints

### `GET /health`
Health check endpoint

### `POST /upload`
Upload and parse document files

**Parameters:**
- `file`: Document file (PDF, DOCX, PPTX, images...)
- `format`: Output format (`markdown`, `json`)

**Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "format=markdown"
```

### `POST /parse-url`
Parse document from URL

**Body:**
```json
{
  "url": "https://arxiv.org/pdf/2408.09869",
  "format": "markdown"
}
```

### `GET /supported-formats`
List of supported file formats

## 📄 Supported Formats

### Input Formats
- **PDF** (.pdf) - Basic parsing (advanced options in development)
- **Microsoft Word** (.docx)
- **Microsoft PowerPoint** (.pptx)
- **HTML** (.html, .htm)
- **Images** (.png, .jpg, .jpeg, .tiff) - Requires OCR for text extraction

### Output Formats
- **Markdown** - Default format, human-readable
- **JSON** - Structured data with metadata

## 🧪 Testing

### Run Example Client
```bash
# Test all endpoints
python api/example_client.py
```

### Manual Testing with curl

**Health check:**
```bash
curl http://localhost:8000/health
```

**Upload file:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf" \
  -F "format=markdown"
```

**Parse from URL:**
```bash
curl -X POST "http://localhost:8000/parse-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://arxiv.org/pdf/2408.09869",
    "format": "markdown"
  }'
```

## 📦 Response Format

### Success Response
```json
{
  "success": true,
  "message": "Document parsed successfully",
  "format": "markdown",
  "content": "# Document Title\n\nParsed content here...",
  "metadata": {
    "file_size": 1024000
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": "Detailed error information"
}
```

## ⚙️ Configuration

### Environment Variables
```bash
# Server configuration
HOST=0.0.0.0
PORT=8000

# Docling configuration
DOCLING_OCR_ENABLED=false
DOCLING_TABLE_STRUCTURE=true
```

### Advanced Usage
```python
# Custom configuration in code
from api.main_simple import app
import uvicorn

# Run with custom config
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        workers=4  # Production setting
    )
```

## 🔐 Security Notes

- API currently has no authentication - add for production use
- File uploads are stored temporarily and automatically cleaned up
- CORS is enabled for all origins - restrict in production
- Rate limiting is not implemented

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn api.main_simple:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "api.main_simple:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
2. **Port conflicts**: Change port in start_api.py
3. **File upload fails**: Check file size limits and supported formats
4. **OCR errors**: Additional dependencies needed for some image formats

### Debug Mode
```bash
uvicorn api.main_simple:app --reload --log-level debug
```

## 📝 Version Notes

**Current Version**: Simplified (v1.0.0-simple)
- Basic document parsing functionality
- Core formats supported
- Advanced PDF options (OCR, table structure) in development

## 🔧 Development

### Project Structure
```
api/
├── main_simple.py          # Simplified API server
├── main.py                 # Full API server (with advanced options)
├── example_client.py       # Test client
└── README.md              # This documentation
```

### Adding Features
1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly
5. Submit a pull request

## 📚 API Integration Examples

### Python
```python
import requests

# Parse document from file
files = {'file': open('document.pdf', 'rb')}
response = requests.post('http://localhost:8000/upload', files=files)
result = response.json()
markdown_content = result['content']
```

### JavaScript/Frontend
```javascript
// Upload and parse file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('format', 'markdown');

fetch('http://localhost:8000/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.content));
```

### cURL Examples
```bash
# Health check
curl http://localhost:8000/health

# Parse URL
curl -X POST "http://localhost:8000/parse-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/document.pdf", "format": "json"}'

# Get supported formats
curl http://localhost:8000/supported-formats
```

## 🎯 Use Cases

- **Document Processing Pipelines**: Batch convert documents to markdown
- **RAG Applications**: Parse PDFs for vector database ingestion
- **Content Management**: Extract text from various document formats
- **Web Applications**: Add document parsing to your web app
- **Research Tools**: Parse academic papers and reports
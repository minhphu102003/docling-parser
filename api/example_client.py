#!/usr/bin/env python3
"""
Example client to test Docling Parser API
"""

import requests
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        print("✅ Health check passed:", response.json())
        return True
    except Exception as e:
        print("❌ Health check failed:", e)
        return False

def test_file_upload(file_path: str):
    """Test file upload endpoint."""
    print(f"📤 Testing file upload: {file_path}")
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'format': 'markdown',
                'enable_ocr': False,
                'enable_table_structure': True
            }
            
            response = requests.post(f"{API_BASE_URL}/upload", files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            print("✅ Upload successful!")
            print(f"   Format: {result['format']}")
            print(f"   Content length: {len(result['content'])} characters")
            print(f"   Preview: {result['content'][:200]}...")
            
            return True
            
    except Exception as e:
        print("❌ Upload failed:", e)
        return False

def test_url_parsing():
    """Test URL parsing endpoint."""
    print("🌐 Testing URL parsing...")
    
    url_data = {
        "url": "https://arxiv.org/pdf/2408.09869",
        "format": "markdown",
        "enable_ocr": False,
        "enable_table_structure": True
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/parse-url", json=url_data)
        response.raise_for_status()
        
        result = response.json()
        print("✅ URL parsing successful!")
        print(f"   Format: {result['format']}")
        print(f"   Content length: {len(result['content'])} characters")
        print(f"   Preview: {result['content'][:200]}...")
        
        return True
        
    except Exception as e:
        print("❌ URL parsing failed:", e)
        return False

def test_supported_formats():
    """Test supported formats endpoint."""
    print("📋 Testing supported formats...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/supported-formats")
        response.raise_for_status()
        
        result = response.json()
        print("✅ Supported formats retrieved!")
        print(f"   Input formats: {result['supported_formats']['input']}")
        print(f"   Output formats: {result['supported_formats']['output']}")
        
        return True
        
    except Exception as e:
        print("❌ Failed to get supported formats:", e)
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Docling Parser API")
    print("=" * 40)
    
    # Test health check first
    if not test_health():
        print("❌ API server not running. Start with: python start_api.py")
        return
    
    print()
    
    # Test supported formats
    test_supported_formats()
    print()
    
    # Test URL parsing
    test_url_parsing()
    print()
    
    # Test file upload (if sample file exists)
    sample_files = [
        "output/parsed_document.md",  # From previous run
        "README.md",  # Project readme
        "docs/usage.md"  # Documentation
    ]
    
    for file_path in sample_files:
        if Path(file_path).exists():
            test_file_upload(file_path)
            break
    else:
        print("ℹ️  No sample files found for upload test")
    
    print("\n🎉 API testing completed!")
    print("💡 Try the interactive docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

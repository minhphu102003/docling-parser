import uvicorn
import sys
import os

# Add current directory to path so we can import from api
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the FastAPI server."""
    print("🚀 Starting Docling Parser API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔄 Alternative Docs: http://localhost:8000/redoc") 
    print("⚡ API Endpoint: http://localhost:8000")
    print("\n" + "="*50)
    
    try:
         uvicorn.run(
             "api.main_simple:app",
             host="0.0.0.0",
             port=8000,
             reload=True,
             log_level="info",
             access_log=True
         )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

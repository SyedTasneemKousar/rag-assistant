"""Quick start script for RAG Assistant"""
import uvicorn
import sys
import os

if __name__ == "__main__":
    print("🚀 Starting RAG Assistant Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")
        sys.exit(0)


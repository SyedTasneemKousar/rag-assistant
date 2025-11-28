from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from app.models import QueryRequest, QueryResponse, UploadResponse
from app.rag_engine import RAGEngine
from app.rag_engine_demo import RAGEngineDemo
from app.agent import AgenticWorkflow
import os

app = FastAPI(title="RAG Assistant API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Check if we should use demo mode (no OpenAI required)
USE_DEMO_MODE = os.getenv("USE_DEMO_MODE", "false").lower() == "true"
HAS_API_KEY = bool(os.getenv("OPENAI_API_KEY"))

# Use demo mode if no API key or explicitly requested
if USE_DEMO_MODE or not HAS_API_KEY:
    print("🔓 Running in DEMO MODE (No OpenAI API required - Free!)")
    rag_engine = RAGEngineDemo()
    agent = None  # Agentic workflow requires OpenAI
else:
    print("🔐 Running in FULL MODE (OpenAI API enabled)")
    rag_engine = RAGEngine()
    agent = AgenticWorkflow(rag_engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "RAG Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    doc_count = len(rag_engine.documents) if hasattr(rag_engine, 'documents') else 0
    return {
        "status": "healthy", 
        "rag_engine_ready": doc_count > 0,
        "mode": "DEMO (Free)" if USE_DEMO_MODE or not HAS_API_KEY else "FULL (OpenAI)"
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["pdf", "txt", "docx"]:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        chunks_processed = rag_engine.process_document(file_path, file_ext)
        return UploadResponse(message=f"Document '{file.filename}' processed", document_id=file.filename, chunks_processed=chunks_processed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        # Check if documents are uploaded
        has_docs = len(rag_engine.documents) > 0 if hasattr(rag_engine, 'documents') else False
        has_vector_store = hasattr(rag_engine, 'vector_store') and rag_engine.vector_store is not None
        
        if not has_vector_store and not has_docs:
            return QueryResponse(answer="No documents uploaded yet.", sources=[], confidence=0.0)
        
        # Use agentic workflow only if available (requires OpenAI)
        if agent and not USE_DEMO_MODE:
            # Determine if query is complex
            complex_keywords = ["summarize", "compare", "analyze", "explain", "and", "also", "then", "multiple"]
            is_complex = any(keyword in question.lower() for keyword in complex_keywords) or len(question.split()) > 10
            
            if is_complex:
                result = agent.process_query(question)
            else:
                result = rag_engine.query(question)
        else:
            # Demo mode - simple RAG only
            result = rag_engine.query(question)
        
        return QueryResponse(
            answer=result["answer"], 
            sources=result.get("sources", [])[:3], 
            confidence=result.get("confidence", 0.7)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/stats")
async def get_stats():
    stats = rag_engine.get_stats()
    return {
        "total_chunks": stats["total_chunks"],
        "has_vector_store": stats.get("has_vector_store", False),
        "total_documents": stats.get("total_documents", 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from app.models import QueryRequest, QueryResponse, UploadResponse, DocumentInfo, DocumentListResponse
from datetime import datetime
from fastapi.responses import FileResponse
import json
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

# Store conversation history (simple in-memory storage)
conversation_history = {}

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

@app.get("/stats")
async def get_stats():
    stats = rag_engine.get_stats()
    return {
        "total_chunks": stats["total_chunks"],
        "has_vector_store": stats.get("has_vector_store", False),
        "total_documents": stats.get("total_documents", 0)
    }

# ==================== NEW FEATURES ====================

@app.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """List all uploaded documents"""
    try:
        documents = []
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    # Get file stats
                    stat = os.stat(file_path)
                    upload_date = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    # Count chunks for this document (simplified - count by filename match)
                    chunks = 0
                    if hasattr(rag_engine, 'chunks'):
                        chunks = len([c for c in rag_engine.chunks if filename in str(c)])
                    
                    documents.append(DocumentInfo(
                        document_id=filename,
                        filename=filename,
                        chunks=chunks if chunks > 0 else 1,  # At least 1 if file exists
                        upload_date=upload_date
                    ))
        
        return DocumentListResponse(documents=documents, total=len(documents))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a specific document"""
    try:
        file_path = os.path.join(UPLOAD_DIR, document_id)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
        
        # Delete the file
        os.remove(file_path)
        
        # Remove from RAG engine (simplified - would need document tracking for full implementation)
        # For now, just delete the file
        
        return {"message": f"Document '{document_id}' deleted successfully", "document_id": document_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents with conversation memory"""
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        # Check if documents are uploaded
        has_docs = len(rag_engine.documents) > 0 if hasattr(rag_engine, 'documents') else False
        has_vector_store = hasattr(rag_engine, 'vector_store') and rag_engine.vector_store is not None
        
        if not has_vector_store and not has_docs:
            return QueryResponse(answer="No documents uploaded yet.", sources=[], confidence=0.0)
        
        # Store user question in conversation history
        session_id = request.chat_history[0].get("session_id", "default") if request.chat_history and len(request.chat_history) > 0 else "default"
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        conversation_history[session_id].append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now().isoformat()
        })
        
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
        
        # Store assistant response in conversation history
        conversation_history[session_id].append({
            "role": "assistant",
            "content": result["answer"],
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            answer=result["answer"], 
            sources=result.get("sources", [])[:3], 
            confidence=result.get("confidence", 0.7)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str = "default"):
    """Get conversation history for a session"""
    if session_id not in conversation_history:
        return {"messages": [], "total": 0}
    
    return {
        "messages": conversation_history[session_id],
        "total": len(conversation_history[session_id])
    }

@app.get("/export/{session_id}")
async def export_conversation(session_id: str = "default"):
    """Export conversation as PDF"""
    try:
        if session_id not in conversation_history or not conversation_history[session_id]:
            raise HTTPException(status_code=404, detail="No conversation found for this session")
        
        # Create simple text export (PDF would require additional library)
        export_text = f"RAG Assistant - Conversation Export\n"
        export_text += f"Session ID: {session_id}\n"
        export_text += f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        export_text += "=" * 60 + "\n\n"
        
        for msg in conversation_history[session_id]:
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            export_text += f"[{role}] ({timestamp})\n"
            export_text += f"{content}\n\n"
            export_text += "-" * 60 + "\n\n"
        
        # Save as text file (simple export)
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        export_file = os.path.join(export_dir, f"conversation_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(export_file, "w", encoding="utf-8") as f:
            f.write(export_text)
        
        return FileResponse(
            export_file,
            media_type="text/plain",
            filename=f"conversation_{session_id}.txt"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting conversation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

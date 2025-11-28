# Backend - FastAPI RAG System

## Quick Start

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env and add OPENAI_API_KEY

# Run
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /upload` - Upload document (PDF/TXT/DOCX)
- `POST /query` - Ask questions
- `GET /stats` - Document statistics

## File Structure

- `main.py` - FastAPI application and endpoints
- `rag_engine.py` - Core RAG logic (chunking, embeddings, retrieval)
- `agent.py` - Agentic AI workflow
- `models.py` - Pydantic models for API

## Testing

```bash
# Test upload
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"

# Test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```



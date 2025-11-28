# 🆓 FREE DEMO MODE - No OpenAI Payment Required!

## How to Enable Demo Mode

### Option 1: Set Environment Variable (Recommended)

In your `.env` file, add this line:
```
USE_DEMO_MODE=true
```

Or in PowerShell:
```powershell
$env:USE_DEMO_MODE="true"
```

### Option 2: It Auto-Enables!

If you don't have a valid OpenAI API key with credits, the system **automatically** uses demo mode!

## What Works in Demo Mode

✅ **Document Upload** - Upload PDF, TXT, DOCX files
✅ **Text Extraction** - Extracts text from documents
✅ **Text Chunking** - Splits documents into chunks
✅ **Simple Search** - Finds relevant chunks using keyword matching
✅ **Query Responses** - Returns answers based on document content
✅ **Source Citations** - Shows where answers came from

## What's Different

❌ **No AI-Generated Answers** - Uses keyword matching instead of LLM
❌ **No Embeddings** - Uses simple text similarity
❌ **No Agentic AI** - Complex reasoning not available

## Demo Mode vs Full Mode

| Feature | Demo Mode (Free) | Full Mode (Paid) |
|---------|------------------|------------------|
| Document Upload | ✅ | ✅ |
| Text Extraction | ✅ | ✅ |
| Chunking | ✅ | ✅ |
| Search Method | Keyword Matching | Vector Embeddings |
| Answer Quality | Good (keyword-based) | Excellent (AI-generated) |
| Cost | **FREE** | ~$0.001-0.01 per query |

## Perfect For

- ✅ Testing the system structure
- ✅ Learning how RAG works
- ✅ Demonstrating the project
- ✅ Development without API costs
- ✅ Understanding document processing

## How to Switch Back to Full Mode

1. Remove `USE_DEMO_MODE=true` from `.env`
2. Add valid `OPENAI_API_KEY` with credits
3. Restart server

## Example Usage

1. Start server (auto-detects demo mode if no API key)
2. Upload document: `POST /upload`
3. Query: `POST /query` with question
4. Get answers based on keyword matching!

**Enjoy testing for FREE! 🎉**


# 🌐 Start the Beautiful Website Interface

## Quick Start (2 Steps!)

### Step 1: Enable Demo Mode (Free - No Payment!)

Open `C:\rag-assistant\backend\.env` and add:
```
USE_DEMO_MODE=true
```

Or just remove/comment out the API key line:
```
# OPENAI_API_KEY=sk-proj-...
```

### Step 2: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd C:\rag-assistant\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd C:\rag-assistant\frontend
npm install
npm start
```

### Step 3: Open Website

Open your browser:
👉 **http://localhost:3000**

## What You'll See

✨ **Beautiful, Clean Website** with:
- 📄 Document upload section
- 💬 Chat interface for questions
- 🎨 Modern, professional design
- 📱 Responsive (works on mobile too!)

## Features

✅ Upload PDF, TXT, DOCX files
✅ Ask questions about documents
✅ Get answers with source citations
✅ **100% FREE** in demo mode!

## Demo Mode vs Full Mode

| Feature | Demo Mode (Free) | Full Mode (Paid) |
|---------|------------------|------------------|
| Document Upload | ✅ | ✅ |
| Text Extraction | ✅ | ✅ |
| Answers | Keyword-based | AI-generated |
| Cost | **FREE** | ~$0.001/query |

Enjoy your beautiful RAG Assistant! 🎉


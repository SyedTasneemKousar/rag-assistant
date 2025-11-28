# 🤖 RAG Assistant - Intelligent Document Q&A System

A full-stack AI application that allows users to upload documents and ask intelligent questions about them using RAG (Retrieval Augmented Generation) and Agentic AI.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 📄 **Document Processing**: Upload and process PDF, TXT, and DOCX files
- 🔍 **RAG System**: Intelligent document chunking, embedding generation, and vector search
- 🤖 **Agentic AI**: Multi-step reasoning for complex queries using LangChain agents
- 💬 **Interactive Chat**: Beautiful web interface for asking questions
- 🆓 **Demo Mode**: Test the system without OpenAI API costs (keyword-based search)
- 🚀 **Production Ready**: Docker support, Azure deployment guides, comprehensive error handling

## 🏗️ Architecture

```
User → React Frontend → FastAPI Backend → RAG Engine → Vector DB (FAISS) → LLM (OpenAI)
                              ↓
                         Agentic AI (LangChain)
                              ↓
                      Multi-step Reasoning
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- (Optional) OpenAI API key for full AI features

### Option 1: Demo Mode (Free - No API Key Required)

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag-assistant.git
   cd rag-assistant
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   
   # Create .env file
   echo "USE_DEMO_MODE=true" > .env
   
   # Start server
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

3. **Setup Frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Open in browser**: http://localhost:3000

### Option 2: Full Mode (With OpenAI API)

1. **Get OpenAI API Key**: https://platform.openai.com/api-keys

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   
   # Create .env file
   echo "OPENAI_API_KEY=sk-your-key-here" > .env
   
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

3. **Setup Frontend** (same as Option 1)

## 📁 Project Structure

```
rag-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── rag_engine.py        # RAG implementation
│   │   ├── rag_engine_demo.py   # Demo mode (free)
│   │   ├── agent.py             # Agentic AI workflow
│   │   └── models.py            # API models
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── DocumentUpload.jsx
│   │       └── ChatInterface.jsx
│   ├── package.json
│   └── Dockerfile
│
├── data/
│   └── sample_document.txt      # Sample document for testing
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

## 🔧 API Endpoints

### Document Management

- `POST /upload` - Upload a document (PDF, TXT, DOCX)
- `GET /stats` - Get document statistics

### Query

- `POST /query` - Ask questions about uploaded documents
  ```json
  {
    "question": "What is this document about?",
    "chat_history": []
  }
  ```

### Health

- `GET /health` - Check server status
- `GET /` - API information

## 🎯 Demo Mode vs Full Mode

| Feature | Demo Mode (Free) | Full Mode (Paid) |
|---------|------------------|------------------|
| Document Upload | ✅ | ✅ |
| Text Extraction | ✅ | ✅ |
| Chunking | ✅ | ✅ |
| Search Method | Keyword Matching | Vector Embeddings |
| Answer Quality | Good | Excellent (AI-generated) |
| Cost | **FREE** | ~$0.001-0.01 per query |
| Agentic AI | ❌ | ✅ |

**To enable Demo Mode**: Set `USE_DEMO_MODE=true` in `backend/.env`

## 🐳 Docker Deployment

### Using Docker Compose

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Individual Containers

```bash
# Backend
cd backend
docker build -t rag-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key rag-backend

# Frontend
cd frontend
docker build -t rag-frontend .
docker run -p 3000:80 rag-frontend
```

## ☁️ Cloud Deployment

See `azure-deploy.md` for detailed Azure deployment instructions.

Supported platforms:
- Azure Container Apps
- Azure App Service
- Azure VM
- Any Docker-compatible platform

## 🧪 Testing

### Using the Web Interface

1. Start backend and frontend
2. Open http://localhost:3000
3. Upload a document
4. Ask questions!

### Using API Directly

```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST http://localhost:8000/upload \
  -F "file=@data/sample_document.txt"

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - RAG pipeline and agent orchestration
- **OpenAI** - LLM for answer generation
- **FAISS** - Vector similarity search
- **PyPDF2** - PDF processing
- **python-docx** - DOCX processing

### Frontend
- **React** - UI library
- **Axios** - HTTP client
- **CSS3** - Styling

## 📚 Documentation

- `PROJECT_EXPLANATION.md` - Detailed technical explanations
- `QUICK_START.md` - Fast setup guide
- `azure-deploy.md` - Azure deployment guide
- `GITHUB_SETUP.md` - GitHub setup instructions

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`  
**Solution**: Activate virtual environment and run `pip install -r requirements.txt`

**Problem**: `OPENAI_API_KEY not set`  
**Solution**: Create `.env` file in `backend/` with `OPENAI_API_KEY=your_key` or `USE_DEMO_MODE=true`

**Problem**: Port 8000 already in use  
**Solution**: Use different port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**Problem**: Cannot connect to backend  
**Solution**: Ensure backend is running on http://localhost:8000

**Problem**: `npm install` fails  
**Solution**: Delete `node_modules` and `package-lock.json`, then reinstall

## 📝 Environment Variables

### Backend (.env)

```env
# For Full Mode (with OpenAI)
OPENAI_API_KEY=sk-your-key-here

# For Demo Mode (free, no API needed)
USE_DEMO_MODE=true
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Future Enhancements

- [ ] Support for more file types (Excel, PowerPoint)
- [ ] User authentication and multi-user support
- [ ] Document management (list, delete, search)
- [ ] Streaming responses
- [ ] Conversation memory
- [ ] Export Q&A sessions
- [ ] Analytics dashboard

## 📄 License

This project is for educational and portfolio purposes.

## 👤 Author

Built as a portfolio project demonstrating:
- RAG system implementation
- Agentic AI workflows
- Full-stack development
- Cloud deployment

## 🙏 Acknowledgments

- LangChain team for excellent documentation
- OpenAI for GPT models
- FastAPI for the amazing framework
- React team for the frontend library

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review code comments (extensive explanations included)
3. Check documentation files in the repository

---

**Made with ❤️ for learning and portfolio purposes**

**Happy Coding! 🚀**

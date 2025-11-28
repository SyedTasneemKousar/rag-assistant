# 🤖 RAG Assistant - Intelligent Document Q&A System

## 📋 Project Overview

**RAG Assistant** is a full-stack AI application that allows users to upload documents and ask intelligent questions about them. It uses:

- **RAG (Retrieval Augmented Generation)**: Finds relevant information from documents
- **Agentic AI**: Performs multi-step reasoning for complex queries
- **FastAPI**: Modern Python backend with REST APIs
- **React**: Beautiful, responsive frontend
- **LangChain & LlamaIndex**: Industry-standard AI frameworks
- **Azure**: Cloud deployment ready

---

## 🎯 Why This Project?

This project demonstrates **exactly** what the job description requires:

✅ **RAG Systems** - Document chunking, embeddings, vector search  
✅ **LLMs** - OpenAI GPT integration for answer generation  
✅ **Agentic AI** - Multi-step reasoning with LangChain agents  
✅ **LangChain** - RAG pipeline and agent orchestration  
✅ **LlamaIndex** - Document indexing (included in dependencies)  
✅ **FastAPI** - High-performance REST API  
✅ **React** - Modern frontend development  
✅ **Azure** - Cloud deployment configurations  

---

## 🏗️ Architecture Overview

```
User → React Frontend → FastAPI Backend → RAG Engine → Vector DB → LLM
                              ↓
                         Agentic AI
                              ↓
                      Multi-step Reasoning
```

### How It Works:

1. **Document Upload**: User uploads PDF/TXT/DOCX
2. **Processing**: Document is split into chunks, converted to embeddings, stored in vector database
3. **Query**: User asks a question
4. **Retrieval**: System finds most relevant document chunks
5. **Generation**: LLM generates answer using retrieved context
6. **Agentic Reasoning**: For complex queries, agent breaks down into steps

---

## 📁 Project Structure

```
rag-assistant/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app with API endpoints
│   │   ├── rag_engine.py   # Core RAG logic (chunking, embeddings, retrieval)
│   │   ├── agent.py        # Agentic AI workflow
│   │   └── models.py       # Pydantic models for API
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Container configuration
│   └── .env.example        # Environment variables template
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main app component
│   │   └── components/
│   │       ├── DocumentUpload.jsx    # File upload UI
│   │       └── ChatInterface.jsx     # Chat Q&A UI
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Container configuration
│
├── docker-compose.yml      # Run both services together
├── azure-deploy.md        # Azure deployment guide
└── README.md              # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step 1: Setup Backend

```bash
# Navigate to backend
cd rag-assistant/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Step 2: Setup Frontend

```bash
# Open new terminal, navigate to frontend
cd rag-assistant/frontend

# Install dependencies
npm install

# Run the app
npm start
```

Frontend will run on `http://localhost:3000`

### Step 3: Use the Application

1. Open `http://localhost:3000` in your browser
2. Upload a PDF/TXT/DOCX document
3. Wait for processing (you'll see "chunks processed" message)
4. Ask questions about the document!

---

## 🔧 Key Components Explained

### 1. RAG Engine (`rag_engine.py`)

**What it does:**
- Processes documents (PDF, TXT, DOCX)
- Splits documents into chunks (1000 characters each)
- Creates embeddings (numerical representations of text)
- Stores chunks in vector database (FAISS)
- Retrieves relevant chunks when user asks questions
- Generates answers using LLM

**Key Concepts:**
- **Chunking**: Breaking large documents into smaller pieces
- **Embeddings**: Converting text to numbers that capture meaning
- **Vector Search**: Finding similar text using mathematical similarity
- **RAG**: Combining retrieval + generation for accurate answers

### 2. Agentic AI (`agent.py`)

**What it does:**
- Uses LangChain agents for multi-step reasoning
- Can break down complex questions into steps
- Uses multiple tools (search, summarize, etc.)
- Makes decisions about what to do next

**Example:**
- User: "Summarize the document and find related information"
- Agent:
  1. Uses summarize tool
  2. Uses search tool with summary
  3. Combines results
  4. Returns final answer

### 3. FastAPI Backend (`main.py`)

**API Endpoints:**

- `POST /upload` - Upload a document
  ```json
  {
    "file": "document.pdf"
  }
  ```

- `POST /query` - Ask a question
  ```json
  {
    "question": "What is this document about?",
    "chat_history": []
  }
  ```

- `GET /health` - Check server status
- `GET /stats` - Get document statistics

### 4. React Frontend

**Components:**
- **DocumentUpload**: File upload interface
- **ChatInterface**: Q&A chat interface

**Features:**
- Drag-and-drop file upload
- Real-time chat
- Source citations
- Responsive design

---

## 🐳 Docker Deployment

### Using Docker Compose (Easiest)

```bash
# From project root
docker-compose up --build
```

This will:
- Build backend container
- Build frontend container
- Run both services
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

---

## ☁️ Azure Deployment

See `azure-deploy.md` for detailed instructions.

**Quick Summary:**
1. Use Azure Container Apps (recommended)
2. Or Azure App Service (simpler)
3. Or Azure VM (most control)

All configurations are provided in the deployment guide.

---

## 🧪 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"

# Ask question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

### Using Python

```python
import requests

# Upload
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload",
        files={"file": f}
    )
print(response.json())

# Query
response = requests.post(
    "http://localhost:8000/query",
    json={"question": "What is this document about?"}
)
print(response.json())
```

---

## 📊 How to Explain This Project in Interviews

### 1. Problem Statement
"I built a system that allows users to ask questions about uploaded documents using AI, solving the problem of quickly finding information in large documents."

### 2. Technical Approach
"I implemented a RAG (Retrieval Augmented Generation) system that:
- Processes documents by chunking them into smaller pieces
- Creates embeddings using OpenAI's API
- Stores them in a vector database (FAISS) for similarity search
- Retrieves relevant chunks when users ask questions
- Generates accurate answers using GPT-3.5"

### 3. Agentic AI
"For complex queries, I added an agentic workflow using LangChain that can:
- Break down complex questions into steps
- Use multiple tools (search, summarize)
- Perform multi-step reasoning
- Combine results intelligently"

### 4. Architecture
"I built a full-stack application:
- FastAPI backend for high-performance API
- React frontend for intuitive user experience
- Docker for containerization
- Azure-ready for cloud deployment"

### 5. Key Technologies
- **LangChain**: RAG pipeline and agent orchestration
- **LlamaIndex**: Document indexing (included)
- **FAISS**: Vector similarity search
- **OpenAI**: LLM for answer generation
- **FastAPI**: Modern async Python framework
- **React**: Component-based frontend

---

## 🎓 Learning Resources

### Understanding RAG
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [What is RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/)

### LangChain
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)

### FastAPI
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### React
- [React Documentation](https://react.dev/)

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
**Solution**: Make sure virtual environment is activated and dependencies are installed

**Problem**: `OPENAI_API_KEY not set`
**Solution**: Create `.env` file in `backend/` directory with `OPENAI_API_KEY=your_key`

**Problem**: Port 8000 already in use
**Solution**: Change port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**Problem**: Cannot connect to backend
**Solution**: Check `REACT_APP_API_URL` in `.env` or ensure backend is running

**Problem**: `npm install` fails
**Solution**: Delete `node_modules` and `package-lock.json`, then run `npm install` again

### Docker Issues

**Problem**: Container won't start
**Solution**: Check logs: `docker-compose logs`

**Problem**: Environment variables not working
**Solution**: Ensure `.env` file exists and variables are set correctly

---

## 📝 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=sk-your-key-here
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🚀 Next Steps / Enhancements

- [ ] Add support for more file types (Excel, PowerPoint)
- [ ] Implement user authentication
- [ ] Add document management (list, delete documents)
- [ ] Improve agentic workflow with more tools
- [ ] Add streaming responses for better UX
- [ ] Implement conversation memory
- [ ] Add export functionality (export Q&A as PDF)
- [ ] Add analytics dashboard

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

Built as a portfolio project demonstrating:
- RAG system implementation
- Agentic AI workflows
- Full-stack development
- Cloud deployment

---

## 🙏 Acknowledgments

- LangChain team for excellent documentation
- OpenAI for GPT models
- FastAPI for the amazing framework
- React team for the frontend library

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments (extensive explanations included)
3. Check LangChain/FastAPI documentation

---

**Happy Coding! 🚀**



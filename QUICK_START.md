# ⚡ Quick Start Guide - Get Running in 10 Minutes!

## Prerequisites Check

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

---

## 🚀 Fastest Setup (Step by Step)

### 1. Setup Backend (5 minutes)

```bash
# Navigate to backend
cd rag-assistant/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env

# Edit .env file and add your API key:
# OPENAI_API_KEY=sk-your-actual-key-here

# Run server
uvicorn app.main:app --reload
```

✅ Backend running on http://localhost:8000

### 2. Setup Frontend (3 minutes)

```bash
# Open NEW terminal window
cd rag-assistant/frontend

# Install dependencies
npm install

# Run frontend
npm start
```

✅ Frontend running on http://localhost:3000

### 3. Test It! (2 minutes)

1. Open http://localhost:3000
2. Upload `data/sample_document.txt`
3. Wait for "Document processed" message
4. Ask: "What is artificial intelligence?"
5. See the magic! ✨

---

## 🐛 Common Issues & Quick Fixes

### Issue: "ModuleNotFoundError"
**Fix**: Make sure virtual environment is activated and run `pip install -r requirements.txt` again

### Issue: "OPENAI_API_KEY not set"
**Fix**: Create `.env` file in `backend/` folder with `OPENAI_API_KEY=your_key`

### Issue: Port already in use
**Fix**: 
- Backend: `uvicorn app.main:app --port 8001`
- Frontend: Create `.env` in `frontend/` with `PORT=3001`

### Issue: npm install fails
**Fix**: Delete `node_modules` folder and `package-lock.json`, then run `npm install` again

---

## 🧪 Test Without Frontend

You can test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST http://localhost:8000/upload -F "file=@data/sample_document.txt"

# Ask question
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d "{\"question\": \"What is AI?\"}"
```

---

## 📝 What to Do Next

1. ✅ Get it running (you just did!)
2. 📖 Read `PROJECT_EXPLANATION.md` to understand how it works
3. 🎨 Customize the UI (change colors, add features)
4. 🚀 Deploy to Azure (see `azure-deploy.md`)
5. 📊 Add to your resume!

---

## 💡 Pro Tips

- **First time?** Use the sample document in `data/` folder
- **No API key?** The system will work but show warnings (you can still see the structure)
- **Want to learn?** Read the code comments - everything is explained!
- **Stuck?** Check `README.md` troubleshooting section

---

**You're all set! Happy coding! 🎉**



# 🔑 OpenAI API Key Setup Guide

## Step 1: Get Your OpenAI API Key

1. **Go to OpenAI Platform:**
   - Visit: https://platform.openai.com/api-keys
   - Sign up or log in to your OpenAI account

2. **Create API Key:**
   - Click "Create new secret key"
   - Give it a name (e.g., "RAG Assistant")
   - Click "Create secret key"
   - **IMPORTANT:** Copy the key immediately (you won't see it again!)
   - It looks like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Add Credits (if needed):**
   - Go to: https://platform.openai.com/account/billing
   - Add payment method and credits
   - You need at least $5-10 to test

## Step 2: Add API Key to Project

### Option A: Edit .env File (Easiest)

1. Open `C:\rag-assistant\backend\.env` in Notepad or any text editor
2. Replace `your-api-key-here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
3. Save the file

### Option B: Set Environment Variable (Windows)

Open PowerShell and run:
```powershell
$env:OPENAI_API_KEY="sk-proj-your-actual-key-here"
```

## Step 3: Restart Server

1. Stop the current server (Press `Ctrl+C` in the server window)
2. Start it again:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

## Step 4: Test It

Run the test script:
```bash
python test_complete.py
```

You should see:
- ✅ Document uploaded successfully
- ✅ Query successful with actual answers

## 💰 Cost Estimate

- **Document Processing:** ~$0.0001 per document
- **Query:** ~$0.001-0.01 per question
- **Testing:** ~$0.10-0.50 for full testing

## 🔒 Security Note

- **Never commit** `.env` file to Git
- **Never share** your API key publicly
- The `.env` file is already in `.gitignore`

## ❓ Troubleshooting

**Error: "Invalid API key"**
- Check that you copied the full key (starts with `sk-`)
- Make sure there are no extra spaces

**Error: "Insufficient credits"**
- Add credits to your OpenAI account
- Check billing at: https://platform.openai.com/account/billing

**Error: "Rate limit exceeded"**
- You're making too many requests
- Wait a few minutes and try again


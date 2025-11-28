@echo off
echo Starting server on port 8001 (port 8000 is busy)...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
pause


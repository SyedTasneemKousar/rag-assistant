import requests
try:
    r = requests.get("http://localhost:8000/health")
    print("✅ SERVER IS RUNNING!")
    print(r.json())
except:
    print("❌ Server not running. Start it with: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")


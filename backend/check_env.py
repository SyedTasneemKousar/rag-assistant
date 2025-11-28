"""
Quick script to check if .env file is being read correctly
"""
import os
from dotenv import load_dotenv

print("=" * 60)
print("🔍 CHECKING .ENV FILE")
print("=" * 60)

# Check if .env file exists
env_path = ".env"
if os.path.exists(env_path):
    print(f"✅ .env file exists at: {os.path.abspath(env_path)}")
    
    # Read file content
    with open(env_path, 'r') as f:
        content = f.read().strip()
        print(f"📄 File content: {content[:50]}...")  # Show first 50 chars
    
    # Try loading with dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print(f"✅ API key loaded successfully!")
        print(f"🔑 Key starts with: {api_key[:10]}...")
        print(f"📏 Key length: {len(api_key)} characters")
    else:
        print("❌ API key NOT loaded from .env file")
        print("\n💡 Possible issues:")
        print("   1. Wrong format in .env file")
        print("   2. Spaces around = sign")
        print("   3. File encoding issue")
        print("\n📋 Correct format should be:")
        print("   OPENAI_API_KEY=sk-proj-your-key-here")
        print("   (NO spaces around =)")
else:
    print(f"❌ .env file NOT found at: {os.path.abspath(env_path)}")
    print(f"💡 Current directory: {os.getcwd()}")
    print(f"💡 Looking for: {os.path.abspath(env_path)}")

print("\n" + "=" * 60)


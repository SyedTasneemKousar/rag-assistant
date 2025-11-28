"""
Interactive script to help set up OpenAI API key
"""
import os

def setup_api_key():
    print("=" * 60)
    print("🔑 OpenAI API Key Setup")
    print("=" * 60)
    
    print("\n📝 Step 1: Get your API key")
    print("   1. Go to: https://platform.openai.com/api-keys")
    print("   2. Sign up/Login")
    print("   3. Click 'Create new secret key'")
    print("   4. Copy the key (starts with 'sk-')")
    
    print("\n" + "-" * 60)
    api_key = input("\n🔑 Paste your API key here: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: API key should start with 'sk-'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    # Create .env file
    env_path = ".env"
    env_content = f"# OpenAI API Key\nOPENAI_API_KEY={api_key}\n"
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"\n✅ API key saved to {env_path}")
        print("\n📋 Next steps:")
        print("   1. Restart your server (Ctrl+C, then start again)")
        print("   2. Test with: python test_complete.py")
        print("\n🔒 Security: Your .env file is in .gitignore (safe)")
    except Exception as e:
        print(f"\n❌ Error saving API key: {e}")
        print("\n💡 Manual setup:")
        print("   1. Create .env file in backend folder")
        print(f"   2. Add: OPENAI_API_KEY={api_key}")

if __name__ == "__main__":
    setup_api_key()


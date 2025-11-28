"""
Fix .env file by removing BOM and ensuring correct format
"""
import os

env_path = ".env"

if os.path.exists(env_path):
    # Read the file
    with open(env_path, 'rb') as f:
        content = f.read()
    
    # Remove BOM if present
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]  # Remove BOM
    
    # Decode and clean
    text = content.decode('utf-8').strip()
    
    # Extract API key
    if '=' in text:
        parts = text.split('=', 1)
        if len(parts) == 2:
            key_name = parts[0].strip()
            key_value = parts[1].strip()
            
            # Write back without BOM
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(f"{key_name}={key_value}\n")
            
            print("✅ Fixed .env file!")
            print(f"📄 Key: {key_name}")
            print(f"🔑 Value: {key_value[:20]}...")
            print("\n💡 Now restart your server!")
        else:
            print("❌ Invalid format in .env file")
    else:
        print("❌ No '=' found in .env file")
else:
    print("❌ .env file not found")


#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""

import os
import sys
from pathlib import Path

print("🔍 Environment Variables Debug Script")
print("=" * 50)

# Check current working directory
print(f"📁 Current working directory: {os.getcwd()}")
print(f"📁 Script location: {Path(__file__).parent}")

# Check if .env file exists
env_file = Path(".env")
if env_file.exists():
    print(f"✅ .env file found at: {env_file.absolute()}")
    print(f"📄 .env file size: {env_file.stat().st_size} bytes")
else:
    print("❌ .env file NOT found!")
    print("💡 Make sure .env is in the same directory as this script")

# Try loading dotenv
try:
    from dotenv import load_dotenv
    print("✅ python-dotenv installed successfully")
    
    # Load .env file
    result = load_dotenv()
    print(f"📋 load_dotenv() result: {result}")
    
except ImportError:
    print("❌ python-dotenv NOT installed!")
    print("💡 Install with: pip install python-dotenv")
    sys.exit(1)

# Check environment variables
print("\n🔍 Environment Variables:")
required_vars = [
    'OPENWEATHER_API_KEY',
    'AZURE_STORAGE_CONNECTION_STRING', 
    'AZURE_CONTAINER_NAME'
]

all_good = True
for var_name in required_vars:
    value = os.getenv(var_name)
    if value:
        # Mask the value for security
        if len(value) > 8:
            masked = value[:4] + '*' * (len(value) - 8) + value[-4:]
        else:
            masked = '*' * len(value)
        print(f"  ✅ {var_name}: {masked} (length: {len(value)})")
    else:
        print(f"  ❌ {var_name}: NOT SET")
        all_good = False

# Final result
print("\n" + "=" * 50)
if all_good:
    print("🎉 All environment variables are set correctly!")
    print("✅ You can now run your temperature capture script")
else:
    print("❌ Some environment variables are missing")
    print("💡 Check your .env file and make sure it's in the right location")

# Show .env file content (masked)
if env_file.exists():
    print(f"\n📄 .env file content preview:")
    try:
        with open(".env", "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines[:5], 1):  # Show first 5 lines
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    masked_value = value[:4] + '*' * max(0, len(value) - 8) + value[-4:] if len(value) > 8 else '*' * len(value)
                    print(f"  Line {i}: {key}={masked_value}")
                else:
                    print(f"  Line {i}: {line}")
    except Exception as e:
        print(f"  Error reading .env file: {e}")
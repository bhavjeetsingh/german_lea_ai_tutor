"""
Deep Debug Script - Find out exactly what's happening with API keys
Save as: backend/debug_deep.py
Run from backend folder: python debug_deep.py
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("DEEP DEBUGGING - API KEY LOADING")
print("=" * 80)
print()

# Step 1: Check working directory
print("STEP 1: Working Directory Check")
print("-" * 80)
current_dir = Path.cwd()
print(f"Current working directory: {current_dir}")
print(f"Script location: {Path(__file__).parent.absolute()}")
print()

# Step 2: Check .env file
print("STEP 2: .env File Check")
print("-" * 80)
env_file = current_dir / ".env"
print(f"Looking for .env at: {env_file}")
print(f".env exists: {env_file.exists()}")

if env_file.exists():
    print(f".env file size: {env_file.stat().st_size} bytes")
    print()
    print("First 500 characters of .env file:")
    print("-" * 80)
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content[:500])
    print("-" * 80)
    
    # Check for specific keys
    print()
    print("Checking for API keys in .env file:")
    for line in content.split('\n'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if 'API_KEY' in key or 'PROVIDER' in key:
                if 'KEY' in key:
                    print(f"  {key} = {value[:20]}... (length: {len(value)})")
                else:
                    print(f"  {key} = {value}")
else:
    print("❌ .env file NOT FOUND!")
print()

# Step 3: Check environment variables
print("STEP 3: System Environment Variables")
print("-" * 80)
env_vars = ['AI_PROVIDER', 'OPENAI_API_KEY', 'GEMINI_API_KEY', 'GROQ_API_KEY']
for var in env_vars:
    value = os.environ.get(var)
    if value:
        if 'KEY' in var:
            print(f"{var} = {value[:20]}... (from system env)")
        else:
            print(f"{var} = {value} (from system env)")
    else:
        print(f"{var} = NOT SET in system")
print()

# Step 4: Try to import and test settings
print("STEP 4: Pydantic Settings Loading")
print("-" * 80)

try:
    from src.config.settings import settings
    
    print("✓ Settings imported successfully")
    print()
    print("Settings values:")
    print(f"  ai_provider: {settings.ai_provider}")
    print(f"  openai_model: {settings.openai_model}")
    print(f"  gemini_model: {settings.gemini_model}")
    print(f"  groq_model: {settings.groq_model}")
    print()
    
    print("API Key Status (first 30 characters):")
    if settings.openai_api_key:
        print(f"  openai_api_key: {settings.openai_api_key[:30]}... (length: {len(settings.openai_api_key)})")
    else:
        print(f"  openai_api_key: EMPTY or NOT SET")
    
    if settings.gemini_api_key:
        print(f"  gemini_api_key: {settings.gemini_api_key[:30]}... (length: {len(settings.gemini_api_key)})")
    else:
        print(f"  gemini_api_key: EMPTY or NOT SET")
    
    if settings.groq_api_key:
        print(f"  groq_api_key: {settings.groq_api_key[:30]}... (length: {len(settings.groq_api_key)})")
    else:
        print(f"  groq_api_key: EMPTY or NOT SET")
    
    print()
    print("Selected Provider Analysis:")
    print(f"  Current provider: {settings.ai_provider}")
    
    if settings.ai_provider == "openai":
        if settings.openai_api_key:
            print(f"  ✓ OpenAI key is set")
            print(f"  Key starts with: {settings.openai_api_key[:7]}")
            print(f"  Key length: {len(settings.openai_api_key)} characters")
            # OpenAI keys should start with 'sk-'
            if not settings.openai_api_key.startswith('sk-'):
                print(f"  ⚠️  WARNING: OpenAI keys should start with 'sk-'")
        else:
            print(f"  ❌ OpenAI selected but key is NOT SET!")
    
    elif settings.ai_provider == "gemini":
        if settings.gemini_api_key:
            print(f"  ✓ Gemini key is set")
            print(f"  Key starts with: {settings.gemini_api_key[:7]}")
            print(f"  Key length: {len(settings.gemini_api_key)} characters")
            # Gemini keys should start with 'AIza'
            if not settings.gemini_api_key.startswith('AIza'):
                print(f"  ⚠️  WARNING: Gemini keys typically start with 'AIza'")
        else:
            print(f"  ❌ Gemini selected but key is NOT SET!")
    
    elif settings.ai_provider == "groq":
        if settings.groq_api_key:
            print(f"  ✓ Groq key is set")
            print(f"  Key starts with: {settings.groq_api_key[:7]}")
            print(f"  Key length: {len(settings.groq_api_key)} characters")
            # Groq keys should start with 'gsk_'
            if not settings.groq_api_key.startswith('gsk_'):
                print(f"  ⚠️  WARNING: Groq keys should start with 'gsk_'")
        else:
            print(f"  ❌ Groq selected but key is NOT SET!")
    
except ImportError as e:
    print(f"❌ Cannot import settings: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Step 5: Test AI Service initialization
print("STEP 5: AI Service Initialization Test")
print("-" * 80)

try:
    from src.services.ai_service import ai_service
    print("✓ AI Service imported and initialized")
    print(f"  Provider: {ai_service.provider}")
    print(f"  Model: {ai_service.model}")
    print(f"  Client type: {type(ai_service.client).__name__}")
except ValueError as e:
    print(f"❌ AI Service failed to initialize: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
print()
print("COMMON ISSUES:")
print("1. If key shows as EMPTY: .env file not being read")
print("2. If key is set but wrong prefix: Wrong API key copied")
print("3. If key is correct but still fails: API key might be expired/invalid")
print("4. If system env vars show up: They override .env file")
print()
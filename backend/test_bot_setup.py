"""
Test bot setup - cek apakah bot bisa di-create tanpa error
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Fix timezone BEFORE importing telegram
import pytz
os.environ['TZ'] = 'UTC'

try:
    import tzlocal
    original_get_localzone = tzlocal.get_localzone
    tzlocal.get_localzone = lambda: pytz.UTC
except:
    pass

load_dotenv()

def test_bot_creation():
    """Test creating bot application"""
    print("=" * 60)
    print("TEST BOT CREATION")
    print("=" * 60)
    
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    
    print("\n1. Testing imports...")
    try:
        from telegram.ext import Application
        print("   [OK] Application import successful")
    except Exception as e:
        print(f"   [ERROR] Import failed: {e}")
        return False
    
    print("\n2. Testing Application creation...")
    try:
        # Create event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Create application
        app = Application.builder().token(token).build()
        print("   [OK] Application created successfully")
        return True
    except Exception as e:
        print(f"   [ERROR] Application creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\nTesting bot setup...\n")
    success = test_bot_creation()
    
    if success:
        print("\n" + "=" * 60)
        print("[OK] Bot setup test PASSED!")
        print("=" * 60)
        print("\nBot seharusnya bisa jalan sekarang.")
        print("Run: python app.py")
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Bot setup test FAILED!")
        print("=" * 60)
        print("\nAda masalah yang perlu diperbaiki.")
    
    print()


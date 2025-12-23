"""
Check bot status - apakah bot masih running
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_bot_status():
    """Check if bot is running"""
    try:
        token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
        response = requests.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=5
        )
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                return True, bot_info.get('result', {})
        return False, None
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    print("Checking bot status...")
    is_running, info = check_bot_status()
    
    if is_running:
        print("✅ Bot is running!")
        if info:
            print(f"   Bot name: {info.get('first_name', 'N/A')}")
            print(f"   Bot username: @{info.get('username', 'N/A')}")
    else:
        print("❌ Bot is not running or cannot connect")
        if info:
            print(f"   Error: {info}")


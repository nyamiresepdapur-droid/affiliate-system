"""
Test Bot Token - Verifikasi token bot valid
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

def test_token():
    """Test bot token"""
    print("=" * 60)
    print("TEST BOT TOKEN")
    print("=" * 60)
    
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    
    if not token:
        print("[ERROR] TELEGRAM_TOKEN tidak ditemukan di .env")
        print("\nBuat file .env dengan isi:")
        print("TELEGRAM_TOKEN=your-token-here")
        return False
    
    print(f"Token: {token[:20]}...")
    print("\nTesting token...")
    
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print("\n[OK] TOKEN VALID!")
            print(f"   Bot ID: {bot_info.get('id')}")
            print(f"   Bot Name: {bot_info.get('first_name')}")
            print(f"   Bot Username: @{bot_info.get('username')}")
            print(f"   Is Bot: {bot_info.get('is_bot')}")
            return True
        else:
            print(f"\n[ERROR] TOKEN INVALID!")
            print(f"   Error: {data.get('description', 'Unknown error')}")
            print(f"   Error Code: {data.get('error_code', 'N/A')}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n[ERROR] TIMEOUT: Tidak bisa connect ke Telegram API")
        print("   Cek internet connection Anda")
        return False
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] CONNECTION ERROR: Tidak bisa connect ke Telegram API")
        print("   Cek internet connection atau firewall")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

def test_webhook():
    """Test webhook status"""
    print("\n" + "=" * 60)
    print("TEST WEBHOOK STATUS")
    print("=" * 60)
    
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            webhook_info = data['result']
            webhook_url = webhook_info.get('url', '')
            
            if webhook_url:
                print(f"[WARNING] WEBHOOK AKTIF!")
                print(f"   URL: {webhook_url}")
                print("\n   Bot menggunakan webhook, bukan polling")
                print("   Untuk development dengan polling, disable webhook dulu:")
                print(f"   https://api.telegram.org/bot{token}/deleteWebhook")
                return False
            else:
                print("[OK] Webhook tidak aktif (OK untuk polling)")
                return True
        else:
            print(f"[ERROR] Error: {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TELEGRAM BOT TOKEN TEST")
    print("=" * 60 + "\n")
    
    token_ok = test_token()
    webhook_ok = test_webhook()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if token_ok and webhook_ok:
        print("[OK] Semua test PASS!")
        print("\nBot token valid dan siap digunakan.")
        print("Langkah selanjutnya: Run 'python app.py'")
    else:
        print("[ERROR] Ada masalah yang perlu diperbaiki:")
        if not token_ok:
            print("   - Token invalid atau tidak ditemukan")
        if not webhook_ok:
            print("   - Webhook aktif, perlu disable untuk polling")
    
    print()


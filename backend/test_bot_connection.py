"""
Test koneksi bot ke Telegram API
Cek apakah bot bisa connect dan merespons
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def test_bot_api():
    """Test bot API connection"""
    print("=" * 60)
    print("TEST BOT API CONNECTION")
    print("=" * 60)
    
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    
    if not token:
        print("[ERROR] TELEGRAM_TOKEN tidak ditemukan di .env")
        return False
    
    print(f"Token: {token[:20]}...")
    print("\n1. Testing getMe API...")
    
    # Test getMe
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"   [OK] Bot Name: {bot_info.get('first_name')}")
            print(f"   [OK] Bot Username: @{bot_info.get('username')}")
            print(f"   [OK] Bot ID: {bot_info.get('id')}")
        else:
            print(f"   [ERROR] {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False
    
    print("\n2. Testing getUpdates API...")
    
    # Test getUpdates (cek apakah bot bisa terima update)
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            updates = data.get('result', [])
            print(f"   [OK] Bot bisa terima updates")
            print(f"   [INFO] Pending updates: {len(updates)}")
            
            if len(updates) > 0:
                print(f"   [WARNING] Ada {len(updates)} pending updates")
                print("   [INFO] Bot mungkin perlu process updates ini dulu")
        else:
            print(f"   [ERROR] {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False
    
    print("\n3. Testing sendMessage API...")
    
    # Test sendMessage (coba kirim message ke bot sendiri)
    # Note: Ini hanya test API, tidak akan kirim message real
    print("   [INFO] Testing sendMessage endpoint...")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Get bot info untuk chat_id
    getme_url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(getme_url, timeout=10)
        bot_data = response.json()
        if bot_data.get('ok'):
            bot_id = bot_data['result']['id']
            # Test dengan chat_id bot sendiri (tidak akan work, tapi test endpoint)
            test_data = {
                'chat_id': bot_id,
                'text': 'Test message'
            }
            response = requests.post(url, json=test_data, timeout=10)
            result = response.json()
            if result.get('ok'):
                print("   [OK] sendMessage API working")
            else:
                print(f"   [INFO] sendMessage test: {result.get('description', 'N/A')}")
                print("   [INFO] Ini normal, bot tidak bisa kirim ke dirinya sendiri")
    except Exception as e:
        print(f"   [INFO] sendMessage test: {e}")
    
    return True

def test_webhook_status():
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
                print(f"[WARNING] Webhook aktif: {webhook_url}")
                print("[WARNING] Bot menggunakan webhook, bukan polling")
                print("[INFO] Untuk development, perlu disable webhook:")
                print(f"       https://api.telegram.org/bot{token}/deleteWebhook")
                return False
            else:
                print("[OK] Webhook tidak aktif (OK untuk polling)")
                return True
        else:
            print(f"[ERROR] {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def check_pending_updates():
    """Check dan clear pending updates jika perlu"""
    print("\n" + "=" * 60)
    print("CHECK PENDING UPDATES")
    print("=" * 60)
    
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            updates = data.get('result', [])
            if len(updates) > 0:
                print(f"[WARNING] Ada {len(updates)} pending updates")
                print("[INFO] Updates ini mungkin menghalangi bot merespons")
                print("[INFO] Bot perlu process atau skip updates ini")
                
                # Get last update_id
                last_update_id = updates[-1].get('update_id')
                print(f"[INFO] Last update_id: {last_update_id}")
                print("\n[INFO] Untuk clear updates, bot perlu:")
                print("       1. Process semua updates, atau")
                print("       2. Skip dengan drop_pending_updates=True (sudah ada di code)")
                
                return False
            else:
                print("[OK] Tidak ada pending updates")
                return True
        else:
            print(f"[ERROR] {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("BOT CONNECTION TEST")
    print("=" * 60 + "\n")
    
    # Test 1: API Connection
    api_ok = test_bot_api()
    
    # Test 2: Webhook Status
    webhook_ok = test_webhook_status()
    
    # Test 3: Pending Updates
    updates_ok = check_pending_updates()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if api_ok and webhook_ok:
        print("[OK] Bot API connection: OK")
        print("[OK] Webhook status: OK")
        
        if not updates_ok:
            print("[WARNING] Ada pending updates yang perlu di-clear")
            print("[INFO] Bot akan skip updates saat start (drop_pending_updates=True)")
        
        print("\n[INFO] Jika bot masih tidak merespons:")
        print("       1. Pastikan aplikasi running: python app.py")
        print("       2. Cek console untuk error")
        print("       3. Pastikan bot thread tidak crash")
        print("       4. Test lagi dengan /start di Telegram")
    else:
        print("[ERROR] Ada masalah dengan bot API")
        if not api_ok:
            print("       - Token invalid atau bot tidak aktif")
        if not webhook_ok:
            print("       - Webhook aktif, perlu disable untuk polling")
    
    print()


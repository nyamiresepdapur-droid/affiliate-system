"""
Force Clear Webhook - Clear webhook dan pending updates
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def force_clear():
    """Force clear webhook and pending updates"""
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    
    print("=" * 60)
    print("FORCE CLEAR WEBHOOK & UPDATES")
    print("=" * 60)
    
    # 1. Delete webhook
    print("\n1. Deleting webhook...")
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    try:
        response = requests.post(url, json={'drop_pending_updates': True}, timeout=10)
        data = response.json()
        if data.get('ok'):
            print("   [OK] Webhook deleted")
        else:
            print(f"   [INFO] {data.get('description', 'N/A')}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # 2. Get updates and clear
    print("\n2. Clearing pending updates...")
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('ok'):
            updates = data.get('result', [])
            if len(updates) > 0:
                last_update_id = updates[-1].get('update_id')
                # Clear with offset
                clear_url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}"
                requests.get(clear_url, timeout=10)
                print(f"   [OK] Cleared {len(updates)} pending updates")
            else:
                print("   [OK] No pending updates")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # 3. Verify webhook status
    print("\n3. Verifying webhook status...")
    url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('ok'):
            webhook_info = data['result']
            webhook_url = webhook_info.get('url', '')
            if webhook_url:
                print(f"   [WARNING] Webhook still active: {webhook_url}")
                print("   [INFO] Trying to delete again...")
                requests.post(f"https://api.telegram.org/bot{token}/deleteWebhook", timeout=10)
            else:
                print("   [OK] Webhook not active")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print("\n" + "=" * 60)
    print("[OK] Force clear completed!")
    print("=" * 60)
    print("\nLangkah selanjutnya:")
    print("1. Pastikan TIDAK ada instance python app.py yang running")
    print("2. Run: python app.py")
    print("3. Bot seharusnya start tanpa conflict")
    print()

if __name__ == '__main__':
    force_clear()


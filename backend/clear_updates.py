"""
Script untuk clear pending updates dari bot
Jalankan script ini untuk clear semua pending updates
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def clear_pending_updates():
    """Clear semua pending updates"""
    token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
    
    print("=" * 60)
    print("CLEAR PENDING UPDATES")
    print("=" * 60)
    
    # Get updates untuk dapat last update_id
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if not data.get('ok'):
        print(f"[ERROR] {data.get('description', 'Unknown error')}")
        return False
    
    updates = data.get('result', [])
    
    if len(updates) == 0:
        print("[OK] Tidak ada pending updates")
        return True
    
    print(f"[INFO] Ditemukan {len(updates)} pending updates")
    
    # Get last update_id
    last_update_id = updates[-1].get('update_id')
    print(f"[INFO] Last update_id: {last_update_id}")
    
    # Clear updates dengan getUpdates + offset
    print("\n[INFO] Clearing updates...")
    clear_url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}"
    response = requests.get(clear_url, timeout=10)
    data = response.json()
    
    if data.get('ok'):
        print("[OK] Updates berhasil di-clear!")
        print(f"[INFO] Bot sekarang siap terima update baru")
        return True
    else:
        print(f"[ERROR] {data.get('description', 'Unknown error')}")
        return False

if __name__ == '__main__':
    print("\nClearing pending updates...\n")
    success = clear_pending_updates()
    
    if success:
        print("\n" + "=" * 60)
        print("[OK] Selesai! Bot sekarang siap digunakan.")
        print("=" * 60)
        print("\nLangkah selanjutnya:")
        print("1. Run: python app.py")
        print("2. Test /start di Telegram")
    else:
        print("\n[ERROR] Gagal clear updates")
    
    print()


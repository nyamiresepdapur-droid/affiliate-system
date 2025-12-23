"""
Script untuk set Telegram ID untuk owner
Jalankan: python set_owner_telegram.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def set_owner_telegram_id(telegram_id: str, telegram_username: str = None):
    """Set Telegram ID untuk owner"""
    with app.app_context():
        owner = User.query.filter_by(role='owner').first()
        
        if not owner:
            print("❌ Owner not found in database!")
            print("   Creating default owner...")
            from werkzeug.security import generate_password_hash
            owner = User(
                username='owner',
                email='owner@affiliate.com',
                password_hash=generate_password_hash('admin123'),
                role='owner',
                full_name='Owner',
                telegram_id=telegram_id,
                telegram_username=telegram_username
            )
            db.session.add(owner)
            db.session.commit()
            print("✅ Default owner created!")
        else:
            owner.telegram_id = str(telegram_id)
            if telegram_username:
                owner.telegram_username = telegram_username
            db.session.commit()
            print(f"✅ Owner Telegram ID updated!")
        
        print(f"\n📋 Owner Info:")
        print(f"   Username: {owner.username}")
        print(f"   Full Name: {owner.full_name}")
        print(f"   Telegram ID: {owner.telegram_id}")
        print(f"   Telegram Username: {owner.telegram_username or 'N/A'}")
        print(f"   Role: {owner.role}")
        print(f"\n✅ Sekarang Anda bisa pakai /admin di bot!")

if __name__ == '__main__':
    print("=" * 50)
    print("SET OWNER TELEGRAM ID")
    print("=" * 50)
    print("\n📱 Cara dapat Telegram ID:")
    print("   1. Buka bot: @userinfobot")
    print("   2. Ketik /start")
    print("   3. Copy ID yang dikirim bot")
    print()
    
    # Get Telegram ID from user
    telegram_id = input("Masukkan Telegram ID Anda: ").strip()
    
    if not telegram_id:
        print("❌ Telegram ID tidak boleh kosong!")
        sys.exit(1)
    
    # Optional: Get Telegram username
    telegram_username = input("Masukkan Telegram Username (optional, tekan Enter untuk skip): ").strip()
    if not telegram_username:
        telegram_username = None
    
    # Set Telegram ID
    try:
        set_owner_telegram_id(telegram_id, telegram_username)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


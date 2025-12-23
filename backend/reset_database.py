"""
Reset Database - Hapus database dan buat baru dengan schema terbaru
"""

import os
from pathlib import Path

def reset_database():
    """Delete database file"""
    db_path = Path(__file__).parent / 'affiliate_system.db'
    
    if db_path.exists():
        os.remove(db_path)
        print(f"✅ Database deleted: {db_path}")
        print("Database akan dibuat otomatis saat app.py dijalankan dengan schema baru.")
    else:
        print("Database tidak ditemukan. Akan dibuat otomatis saat app.py dijalankan.")
    
    print("\nLangkah selanjutnya:")
    print("1. Run: python app.py")
    print("2. Database akan dibuat dengan schema terbaru")

if __name__ == '__main__':
    print("=" * 60)
    print("RESET DATABASE")
    print("=" * 60)
    print()
    reset_database()
    print()


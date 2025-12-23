"""
Migration Script - Update database schema
Menambahkan field baru ke tabel yang sudah ada
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """Migrate database to new schema"""
    db_path = Path(__file__).parent / 'affiliate_system.db'
    
    if not db_path.exists():
        print("Database tidak ditemukan. Akan dibuat otomatis saat app.py dijalankan.")
        return
    
    print("=" * 60)
    print("DATABASE MIGRATION")
    print("=" * 60)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Check existing columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print("\nExisting columns in users table:")
        for col in columns:
            print(f"  - {col}")
        
        # Add new columns if they don't exist
        new_columns = {
            'whatsapp': 'VARCHAR(20)',
            'tiktok_akun': 'VARCHAR(100)',
            'wallet': 'VARCHAR(100)',
            'bank_account': 'VARCHAR(100)',
            'telegram_id': 'VARCHAR(50)',
            'telegram_username': 'VARCHAR(100)'
        }
        
        print("\nAdding new columns...")
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                    print(f"  ✅ Added column: {col_name}")
                except sqlite3.OperationalError as e:
                    print(f"  ⚠️  Column {col_name} might already exist: {e}")
            else:
                print(f"  ⏭️  Column {col_name} already exists")
        
        # Check products table
        cursor.execute("PRAGMA table_info(products)")
        product_columns = [col[1] for col in cursor.fetchall()]
        
        print("\nChecking products table...")
        if 'target_gmv' not in product_columns:
            try:
                cursor.execute("ALTER TABLE products ADD COLUMN target_gmv FLOAT DEFAULT 0")
                print("  ✅ Added column: target_gmv")
            except sqlite3.OperationalError as e:
                print(f"  ⚠️  Error: {e}")
        else:
            print("  ⏭️  Column target_gmv already exists")
        
        if 'updated_at' not in product_columns:
            try:
                cursor.execute("ALTER TABLE products ADD COLUMN updated_at DATETIME")
                print("  ✅ Added column: updated_at")
            except sqlite3.OperationalError as e:
                print(f"  ⚠️  Error: {e}")
        else:
            print("  ⏭️  Column updated_at already exists")
        
        # Check content table
        cursor.execute("PRAGMA table_info(content)")
        content_columns = [col[1] for col in cursor.fetchall()]
        
        print("\nChecking content table...")
        new_content_columns = {
            'link_video': 'VARCHAR(500)',
            'tanggal_upload': 'DATE',
            'tiktok_akun': 'VARCHAR(100)'
        }
        
        for col_name, col_type in new_content_columns.items():
            if col_name not in content_columns:
                try:
                    cursor.execute(f"ALTER TABLE content ADD COLUMN {col_name} {col_type}")
                    print(f"  ✅ Added column: {col_name}")
                except sqlite3.OperationalError as e:
                    print(f"  ⚠️  Error: {e}")
            else:
                print(f"  ⏭️  Column {col_name} already exists")
        
        # Check payments table
        cursor.execute("PRAGMA table_info(payments)")
        payment_columns = [col[1] for col in cursor.fetchall()]
        
        print("\nChecking payments table...")
        new_payment_columns = {
            'payment_method': 'VARCHAR(50)',
            'payment_detail': 'VARCHAR(200)'
        }
        
        for col_name, col_type in new_payment_columns.items():
            if col_name not in payment_columns:
                try:
                    cursor.execute(f"ALTER TABLE payments ADD COLUMN {col_name} {col_type}")
                    print(f"  ✅ Added column: {col_name}")
                except sqlite3.OperationalError as e:
                    print(f"  ⚠️  Error: {e}")
            else:
                print(f"  ⏭️  Column {col_name} already exists")
        
        # Make product_id nullable in content table (for reports)
        # SQLite doesn't support MODIFY COLUMN, so we skip this
        # It's already nullable in the model
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    print("\nStarting database migration...\n")
    migrate_database()
    print("\nMigration finished. You can now run: python app.py\n")


"""
Script to add sheet_order column to products table
Run this once to update existing database schema
"""
import sqlite3
import os
from pathlib import Path

def add_sheet_order_column():
    """Add sheet_order column to products table if it doesn't exist"""
    # Flask SQLAlchemy uses instance/ folder for database
    db_path = Path(__file__).parent / 'instance' / 'affiliate_system.db'
    # Fallback to same directory if instance folder doesn't exist
    if not db_path.exists():
        db_path = Path(__file__).parent / 'affiliate_system.db'
    
    if not db_path.exists():
        print(f"[ERROR] Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'sheet_order' in columns:
            print("[OK] Column 'sheet_order' already exists in products table")
            conn.close()
            return True
        
        # Add column
        print("Adding 'sheet_order' column to products table...")
        cursor.execute("ALTER TABLE products ADD COLUMN sheet_order INTEGER")
        conn.commit()
        
        print("[OK] Successfully added 'sheet_order' column to products table")
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error adding column: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Adding sheet_order column to products table")
    print("=" * 50)
    success = add_sheet_order_column()
    if success:
        print("\n[OK] Migration completed successfully!")
        print("You can now sync products from Google Sheets to update sheet_order values.")
    else:
        print("\n[ERROR] Migration failed. Please check the error above.")


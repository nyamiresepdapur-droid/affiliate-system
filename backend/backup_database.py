"""
Database Backup Script
Jalankan: python backup_database.py
"""

import os
import shutil
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def backup_database():
    """Backup SQLite database"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'affiliate_system.db')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        print(f"   Expected location: {db_path}")
        return False
    
    # Create backup directory if not exists
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'affiliate_system_backup_{timestamp}.db'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        # Get file size
        file_size = os.path.getsize(backup_path)
        file_size_mb = file_size / (1024 * 1024)
        
        print("✅ Database backup created successfully!")
        print(f"   Backup file: {backup_filename}")
        print(f"   Location: {backup_path}")
        print(f"   Size: {file_size_mb:.2f} MB")
        print(f"   Timestamp: {timestamp}")
        
        # Cleanup old backups (keep last 30 days)
        cleanup_old_backups(backup_dir, days=30)
        
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_old_backups(backup_dir, days=30):
    """Remove backups older than specified days"""
    try:
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        deleted_count = 0
        for filename in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, filename)
            if os.path.isfile(file_path) and filename.startswith('affiliate_system_backup_'):
                # Extract timestamp from filename
                try:
                    timestamp_str = filename.replace('affiliate_system_backup_', '').replace('.db', '')
                    file_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    
                    if file_date < cutoff_date:
                        os.remove(file_path)
                        deleted_count += 1
                except ValueError:
                    # Skip files with invalid timestamp format
                    pass
        
        if deleted_count > 0:
            print(f"   Cleaned up {deleted_count} old backup(s)")
    except Exception as e:
        print(f"   Warning: Could not cleanup old backups: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("DATABASE BACKUP")
    print("=" * 50)
    print()
    
    backup_database()
    
    print()
    print("💡 Tip: Setup automated backup dengan Task Scheduler (Windows)")
    print("   atau cron job (Linux) untuk backup harian otomatis.")


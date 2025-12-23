"""
Test script untuk sync Google Sheets
Jalankan: python test_sync.py
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from google_sheets_service import GoogleSheetsService

def test_sync():
    """Test sync dengan Flask app context"""
    with app.app_context():
        print("🔄 Testing Google Sheets sync...")
        
        gs_service = GoogleSheetsService()
        
        if not gs_service.is_available():
            print("❌ Google Sheets service tidak tersedia")
            print("   Pastikan google_credentials.json ada di folder backend/")
            return False
        
        print("✅ Google Sheets service tersedia")
        print("📊 Starting sync...")
        
        try:
            success = gs_service.sync_all_from_sheets()
            
            if success:
                print("✅ Sync berhasil!")
                
                # Show results
                from models import Product, User, Content
                product_count = Product.query.count()
                user_count = User.query.count()
                report_count = Content.query.filter(Content.link_video != None, Content.link_video != '').count()
                
                print(f"\n📈 Data di database:")
                print(f"   - Produk: {product_count}")
                print(f"   - User: {user_count}")
                print(f"   - Laporan: {report_count}")
            else:
                print("⚠️  Sync selesai dengan beberapa error")
                print("   Cek log untuk detail")
            
            return success
        except Exception as e:
            print(f"❌ Error saat sync: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_sync()


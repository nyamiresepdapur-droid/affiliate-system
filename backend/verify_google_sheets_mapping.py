"""
Script untuk verifikasi mapping kolom Google Sheets vs Dashboard
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from google_sheets_service import GoogleSheetsService
from models import db, Product
from app import app

def verify_mapping():
    """Verifikasi mapping kolom Google Sheets"""
    with app.app_context():
        gs_service = GoogleSheetsService()
        
        if not gs_service.is_available():
            print("❌ Google Sheets tidak tersedia")
            return False
        
        try:
            sheet = gs_service.spreadsheet.worksheet('produk')
            all_values = sheet.get_all_values()
            
            if len(all_values) <= 1:
                print("⚠️ Sheet 'produk' kosong (hanya header)")
                return True
            
            headers = all_values[0]
            print("\n📋 HEADER DI GOOGLE SHEETS:")
            print("=" * 80)
            for i, header in enumerate(headers):
                col_letter = chr(65 + i)  # A, B, C, ...
                print(f"{col_letter:>3} ({i:>2}): {header}")
            
            print("\n📊 STRUKTUR YANG DIHARAPKAN:")
            print("=" * 80)
            expected = [
                (0, 'A', 'tanggal'),
                (1, 'B', 'nama produk'),
                (2, 'C', 'harga produk'),
                (3, 'D', 'link produk'),
                (4, 'E', 'komisi_reguler'),
                (5, 'F', 'komisi_gmv'),
                (6, 'G', 'target_gmv'),
                (7, 'H', 'status')
            ]
            
            for idx, col, name in expected:
                if idx < len(headers):
                    actual = headers[idx].lower().strip()
                    match = actual == name.lower() or actual.replace(' ', '_') == name
                    status = "✅" if match else "❌"
                    print(f"{status} {col:>3} ({idx:>2}): Expected '{name}', Got '{actual}'")
                else:
                    print(f"❌ {col:>3} ({idx:>2}): Expected '{name}', MISSING")
            
            print("\n📦 DATA SAMPLE (Row 2):")
            print("=" * 80)
            if len(all_values) > 1:
                row = all_values[1]
                for i, val in enumerate(row):
                    col_letter = chr(65 + i)
                    header = headers[i] if i < len(headers) else f"Col {i+1}"
                    print(f"{col_letter:>3} ({header:20}): {val}")
            
            print("\n💾 DATA DI DATABASE:")
            print("=" * 80)
            products = Product.query.order_by(Product.sheet_order.asc(), Product.id.asc()).limit(3).all()
            for p in products:
                print(f"ID: {p.id}")
                print(f"  Nama: {p.product_name}")
                print(f"  Harga: Rp{p.product_price:,.0f}")
                print(f"  Link: {p.product_link[:50]}...")
                print(f"  Komisi Reguler: Rp{p.regular_commission:,.0f}")
                print(f"  Komisi GMV: Rp{p.gmv_max_commission:,.0f}")
                print(f"  Target GMV: {p.target_gmv}")
                print(f"  Status: {p.status}")
                print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("=" * 80)
    print("VERIFIKASI MAPPING GOOGLE SHEETS")
    print("=" * 80)
    verify_mapping()


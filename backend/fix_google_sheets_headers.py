"""
Fix Google Sheets Headers
Memperbaiki typo di header Google Sheets: "harga produl" dan "komisi_regul"
"""
import sys
import os
# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google_sheets_service import GoogleSheetsService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_headers():
    """Fix headers in Google Sheets"""
    print("=" * 60)
    print("FIX GOOGLE SHEETS HEADERS")
    print("=" * 60)
    print()
    
    gs_service = GoogleSheetsService()
    
    if not gs_service.is_available():
        print("[ERROR] Google Sheets service not available")
        print("        Pastikan google_credentials.json sudah dikonfigurasi")
        return False
    
    try:
        # Get the produk sheet
        sheet = gs_service.spreadsheet.worksheet('produk')
        
        # Get current headers
        headers = sheet.row_values(1)
        print(f"Current headers: {headers}")
        print()
        
        # Check if there are typos
        has_typos = False
        fixed_headers = []
        
        header_fixes = {
            'harga produl': 'harga produk',
            'komisi_regul': 'komisi_reguler'
        }
        
        for i, header in enumerate(headers):
            header_lower = header.lower().strip()
            if header_lower in header_fixes:
                print(f"[WARNING] Found typo: '{header}' -> '{header_fixes[header_lower]}'")
                fixed_headers.append(header_fixes[header_lower])
                has_typos = True
            else:
                fixed_headers.append(header)
        
        if not has_typos:
            print("[OK] No typos found. Headers are correct!")
            return True
        
        print()
        print("Fixed headers:")
        for i, (old, new) in enumerate(zip(headers, fixed_headers)):
            if old != new:
                print(f"  Column {chr(65+i)}: '{old}' → '{new}'")
            else:
                print(f"  Column {chr(65+i)}: '{old}' (OK)")
        
        print()
        confirm = input("Fix headers in Google Sheets? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("[CANCELLED] Operation cancelled")
            return False
        
        # Update headers
        print()
        print("Updating headers...")
        for i, new_header in enumerate(fixed_headers, start=1):
            sheet.update_cell(1, i, new_header)
        
        print("[OK] Headers fixed successfully!")
        print()
        print("New headers:")
        new_headers = sheet.row_values(1)
        for i, header in enumerate(new_headers, start=1):
            print(f"  Column {chr(64+i)}: {header}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_headers()
    sys.exit(0 if success else 1)


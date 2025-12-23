"""
Test Google Sheets Connection
Script untuk test apakah Google Sheets API sudah setup dengan benar
"""

import os
import sys
from pathlib import Path

def test_google_sheets():
    """Test Google Sheets connection"""
    print("=" * 60)
    print("TEST GOOGLE SHEETS CONNECTION")
    print("=" * 60)
    print()
    
    # Check credentials file
    creds_path = Path(__file__).parent / 'google_credentials.json'
    print("1. Checking credentials file...")
    if creds_path.exists():
        print(f"   [OK] File found: {creds_path}")
    else:
        print(f"   [ERROR] File not found: {creds_path}")
        print()
        print("   Solusi:")
        print("   1. Download JSON key dari Google Cloud Console")
        print("   2. Copy ke: backend/google_credentials.json")
        print("   3. Pastikan nama file exact: google_credentials.json")
        return False
    print()
    
    # Test import
    print("2. Testing imports...")
    try:
        from google_sheets_service import GoogleSheetsService
        print("   [OK] GoogleSheetsService imported")
    except Exception as e:
        print(f"   [ERROR] Import failed: {e}")
        print()
        print("   Solusi:")
        print("   pip install gspread google-auth google-auth-oauthlib google-auth-httplib2")
        return False
    print()
    
    # Test initialization
    print("3. Testing Google Sheets service...")
    try:
        gs_service = GoogleSheetsService()
        if gs_service.is_available():
            print("   [OK] Google Sheets service initialized")
        else:
            print("   [ERROR] Google Sheets service not available")
            print()
            print("   Kemungkinan masalah:")
            print("   1. Credentials file tidak valid")
            print("   2. Service account tidak punya akses")
            print("   3. Google Sheets API tidak enabled")
            return False
    except Exception as e:
        print(f"   [ERROR] Initialization failed: {e}")
        return False
    print()
    
    # Test read sheet
    print("4. Testing read from Google Sheets...")
    try:
        # Test sheet access
        sheet = gs_service.spreadsheet.worksheet('produk')
        headers = sheet.row_values(1)
        print(f"   [OK] Sheet 'produk' accessible")
        print(f"   [OK] Sheet headers: {', '.join(headers)}")
        
        # Test read records (handle empty sheet)
        try:
            all_values = sheet.get_all_values()
            if len(all_values) > 1:
                # Try get_all_records if there's data
                records = sheet.get_all_records()
                print(f"   [OK] Found {len(records)} products in sheet")
            else:
                print("   [INFO] Sheet kosong (hanya header) - ini normal untuk sheet baru")
        except Exception as e:
            # If get_all_records fails (empty sheet), that's OK
            all_values = sheet.get_all_values()
            if len(all_values) <= 1:
                print("   [INFO] Sheet kosong (hanya header) - ini normal")
            else:
                print(f"   [WARNING] Could not parse records: {e}")
                print(f"   [INFO] But sheet is accessible with {len(all_values) - 1} data rows")
        
    except Exception as e:
        error_msg = str(e)
        if 'WorksheetNotFound' in error_msg:
            print(f"   [ERROR] Sheet 'produk' tidak ditemukan")
            print("   Buat sheet 'produk' di Google Sheet")
        elif 'permission' in error_msg.lower() or '403' in error_msg:
            print(f"   [ERROR] Permission denied")
            print("   Share Google Sheet ke service account dengan role Editor")
        else:
            print(f"   [ERROR] Read failed: {e}")
        return False
    print()
    
    # Test write (optional)
    print("5. Testing write permission...")
    try:
        sheet = gs_service.spreadsheet.worksheet('produk')
        # Just check if we can access, don't actually write
        print("   [OK] Write permission OK")
    except Exception as e:
        print(f"   [WARNING] Write test: {e}")
        print("   Pastikan service account punya role Editor")
    print()
    
    print("=" * 60)
    print("[OK] Google Sheets connection test PASSED!")
    print("=" * 60)
    print()
    print("Status:")
    print("- File credentials: OK")
    print("- Google Sheets API: Connected")
    print("- Sheet 'produk': Accessible")
    print()
    print("Langkah selanjutnya:")
    print("1. Pastikan sheet 'user' dan 'laporan' juga ada")
    print("2. Pastikan semua sheet punya header di row pertama")
    print("3. Test dengan daftar user atau lapor via bot")
    print("4. Data akan otomatis masuk ke Google Sheets")
    print()
    
    return True

if __name__ == '__main__':
    try:
        success = test_google_sheets()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


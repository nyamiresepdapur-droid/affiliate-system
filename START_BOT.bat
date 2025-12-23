@echo off
chcp 65001 >nul
echo ========================================
echo    AFFILIATE SYSTEM - START BOT
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan! Pastikan Python sudah terinstall.
    pause
    exit /b 1
)
python --version
echo.

echo [2/3] Checking database migration (sheet_order column)...
python -c "import sqlite3; import os; db_path = os.path.join('instance', 'affiliate_system.db'); conn = sqlite3.connect(db_path) if os.path.exists(db_path) else None; cursor = conn.cursor() if conn else None; cursor.execute('PRAGMA table_info(products)') if cursor else None; cols = [col[1] for col in cursor.fetchall()] if cursor else []; print('OK - sheet_order column exists') if 'sheet_order' in cols else print('WARNING - sheet_order column missing, run: python add_sheet_order_column.py'); conn.close() if conn else None" 2>nul
if errorlevel 1 (
    echo [INFO] Database belum ada atau perlu migration. Akan dibuat otomatis saat start.
)
echo.

echo [3/3] Starting Flask app and Telegram bot...
echo.
echo ========================================
echo    SYSTEM FEATURES:
echo ========================================
echo    - Google Sheets Sync (auto every 5 min)
echo    - Telegram Bot Integration
echo    - Daily Commission Tracking
echo    - Video Statistics Tracking
echo    - Member Daily Summary
echo    - Date Filtering (Dashboard & Reports)
echo    - Currency Format: Rp50,000
echo    - Column Mapping: A=tanggal, B=nama produk, etc.
echo ========================================
echo.
echo Server akan berjalan di: http://localhost:5000
echo Dashboard: http://localhost:5000
echo API Docs: http://localhost:5000/api/docs
echo.
echo Press CTRL+C to stop
echo.

python app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Aplikasi error saat start!
    echo Periksa log di atas untuk detail error.
    pause
    exit /b 1
)

pause


# PowerShell script untuk start Affiliate System
# Usage: .\start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AFFILIATE SYSTEM - START BOT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptPath "backend")

# Check Python
Write-Host "[1/3] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python tidak ditemukan! Pastikan Python sudah terinstall." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check database migration
Write-Host "[2/3] Checking database migration (sheet_order column)..." -ForegroundColor Yellow
$dbPath = Join-Path "instance" "affiliate_system.db"
if (Test-Path $dbPath) {
    try {
        python -c "import sqlite3; import os; db_path = os.path.join('instance', 'affiliate_system.db'); conn = sqlite3.connect(db_path); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(products)'); cols = [col[1] for col in cursor.fetchall()]; print('OK - sheet_order column exists') if 'sheet_order' in cols else print('WARNING - sheet_order column missing, run: python add_sheet_order_column.py'); conn.close()" 2>&1
    } catch {
        Write-Host "[INFO] Database check skipped" -ForegroundColor Gray
    }
} else {
    Write-Host "[INFO] Database belum ada, akan dibuat otomatis saat start" -ForegroundColor Gray
}
Write-Host ""

# Start application
Write-Host "[3/3] Starting Flask app and Telegram bot..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    SYSTEM FEATURES:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    - Google Sheets Sync (auto every 5 min)" -ForegroundColor White
Write-Host "    - Telegram Bot Integration" -ForegroundColor White
Write-Host "    - Daily Commission Tracking" -ForegroundColor White
Write-Host "    - Video Statistics Tracking" -ForegroundColor White
Write-Host "    - Member Daily Summary" -ForegroundColor White
Write-Host "    - Date Filtering (Dashboard & Reports)" -ForegroundColor White
Write-Host "    - Currency Format: Rp50,000" -ForegroundColor White
Write-Host "    - Column Mapping: A=tanggal, B=nama produk, etc." -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server akan berjalan di: http://localhost:5000" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:5000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:5000/api/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""

try {
    python app.py
} catch {
    Write-Host ""
    Write-Host "[ERROR] Aplikasi error saat start!" -ForegroundColor Red
    Write-Host "Periksa log di atas untuk detail error." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"


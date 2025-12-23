#!/bin/bash
# Bash script untuk start Affiliate System (Linux/Mac)
# Usage: ./start.sh

echo "========================================"
echo "   AFFILIATE SYSTEM - START BOT"
echo "========================================"
echo ""

# Change to backend directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/backend"

# Check Python
echo "[1/3] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[ERROR] Python tidak ditemukan! Pastikan Python sudah terinstall."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD --version
echo ""

# Check database migration
echo "[2/3] Checking database migration (sheet_order column)..."
if [ -f "instance/affiliate_system.db" ]; then
    $PYTHON_CMD -c "
import sqlite3
import os
db_path = os.path.join('instance', 'affiliate_system.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(products)')
    cols = [col[1] for col in cursor.fetchall()]
    if 'sheet_order' in cols:
        print('OK - sheet_order column exists')
    else:
        print('WARNING - sheet_order column missing, run: python add_sheet_order_column.py')
    conn.close()
" 2>/dev/null || echo "[INFO] Database check skipped"
else
    echo "[INFO] Database belum ada, akan dibuat otomatis saat start"
fi
echo ""

# Start application
echo "[3/3] Starting Flask app and Telegram bot..."
echo ""
echo "========================================"
echo "    SYSTEM FEATURES:"
echo "========================================"
echo "    - Google Sheets Sync (auto every 5 min)"
echo "    - Telegram Bot Integration"
echo "    - Daily Commission Tracking"
echo "    - Video Statistics Tracking"
echo "    - Member Daily Summary"
echo "    - Date Filtering (Dashboard & Reports)"
echo "    - Currency Format: Rp50,000"
echo "    - Column Mapping: A=tanggal, B=nama produk, etc."
echo "========================================"
echo ""
echo "Server akan berjalan di: http://localhost:5000"
echo "Dashboard: http://localhost:5000"
echo "API Docs: http://localhost:5000/api/docs"
echo ""
echo "Press CTRL+C to stop"
echo ""

$PYTHON_CMD app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Aplikasi error saat start!"
    echo "Periksa log di atas untuk detail error."
    exit 1
fi


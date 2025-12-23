"""
Google Sheets Service
Handle sync antara Google Sheets dan Database
"""

import gspread
from gspread.exceptions import WorksheetNotFound
from google.oauth2.service_account import Credentials
import os
from datetime import datetime, timezone
from models import db, Product, User, Content
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        """Initialize Google Sheets service"""
        try:
            # Load credentials
            creds_path = os.path.join(os.path.dirname(__file__), 'google_credentials.json')
            if not os.path.exists(creds_path):
                logger.warning("Google credentials not found. Google Sheets sync disabled.")
                self.client = None
                return
            
            creds = Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.client = gspread.authorize(creds)
            self.sheet_id = '1pETKwrDqfygYrUwR68aQdf_tFLOx2USuL-jE2m0f8iY'
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            logger.info("Google Sheets service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets: {e}")
            self.client = None
    
    def is_available(self):
        """Check if Google Sheets service is available"""
        return self.client is not None
    
    def ensure_sheet_exists(self, sheet_name: str, headers: list = None):
        """Ensure sheet exists, create if not exists"""
        if not self.is_available():
            return None
        
        try:
            # First, try to get sheet directly
            try:
                sheet = self.spreadsheet.worksheet(sheet_name)
                return sheet
            except WorksheetNotFound:
                pass  # Continue to create logic
            
            # If not found, check if sheet exists with different case/spacing
            # List all worksheets to check
            try:
                all_sheets = self.spreadsheet.worksheets()
                for ws in all_sheets:
                    if ws.title.strip().lower() == sheet_name.strip().lower():
                        # Found sheet with similar name (case-insensitive)
                        logger.info(f"Found sheet '{ws.title}' (matches '{sheet_name}')")
                        return ws
            except Exception as e:
                logger.warning(f"Error listing worksheets: {e}")
            
            # Sheet doesn't exist, try to create it
            try:
                logger.info(f"Sheet '{sheet_name}' not found, creating...")
                sheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
                
                # Add headers if provided
                if headers:
                    sheet.append_row(headers)
                    logger.info(f"Sheet '{sheet_name}' created with headers: {headers}")
                else:
                    logger.info(f"Sheet '{sheet_name}' created without headers")
                
                return sheet
            except Exception as create_error:
                # If create fails because sheet already exists, try to get it again
                error_str = str(create_error)
                if 'already exists' in error_str.lower() or 'duplicate' in error_str.lower():
                    logger.warning(f"Sheet '{sheet_name}' creation failed (may already exist), trying to get it...")
                    try:
                        # Try to get it again (maybe it was just created by another process)
                        sheet = self.spreadsheet.worksheet(sheet_name)
                        logger.info(f"Successfully retrieved existing sheet '{sheet_name}'")
                        return sheet
                    except WorksheetNotFound:
                        # Still not found, try case-insensitive search again
                        all_sheets = self.spreadsheet.worksheets()
                        for ws in all_sheets:
                            if ws.title.strip().lower() == sheet_name.strip().lower():
                                logger.info(f"Found sheet '{ws.title}' after creation error")
                                return ws
                        raise create_error  # Re-raise if still not found
                else:
                    raise create_error  # Re-raise if it's a different error
                    
        except Exception as e:
            logger.error(f"Error ensuring sheet '{sheet_name}' exists: {e}")
            return None
    
    # ==================== PRODUCTS ====================
    
    def add_product_to_sheet(self, product):
        """Add product to Google Sheet 'produk'"""
        if not self.is_available():
            return False
        
        try:
            # Ensure sheet exists - sesuai dengan struktur Google Sheets
            # A=tanggal, B=nama produk, C=harga produk, D=link produk, E=komisi reguler, F=komisi gmv, G=target gmv, H=status
            headers = ['tanggal', 'nama produk', 'harga produk', 'link produk', 'komisi_reguler', 'komisi_gmv', 'target_gmv', 'status']
            sheet = self.ensure_sheet_exists('produk', headers)
            if not sheet:
                logger.warning("Sheet 'produk' tidak bisa dibuat atau diakses")
                return False
            
            # Format tanggal untuk Google Sheets (DD/MM/YYYY)
            tanggal = datetime.now().strftime('%d/%m/%Y')
            
            # Format harga dan komisi dalam bentuk rupiah (sesuai Google Sheets: Rp50,000)
            def format_rupiah(value):
                # Format: Rp50,000 (tanpa spasi, koma sebagai pemisah ribuan)
                return f"Rp{value:,.0f}"
            
            sheet.append_row([
                tanggal,  # A: tanggal
                product.product_name,  # B: nama produk
                format_rupiah(product.product_price),  # C: harga produk (rupiah) - Rp50,000
                product.product_link,  # D: link produk
                format_rupiah(product.regular_commission),  # E: komisi reguler (rupiah) - Rp5,000
                format_rupiah(product.gmv_max_commission),  # F: komisi gmv (rupiah) - Rp2,500
                int(product.target_gmv) if product.target_gmv else 0,  # G: target gmv (angka biasa, bukan rupiah) - 0
                product.status  # H: status
            ])
            logger.info(f"Product {product.product_name} added to Google Sheets")
            return True
        except Exception as e:
            logger.error(f"Error adding product to sheet: {e}")
            return False
    
    def sync_products_from_sheet(self):
        """Sync products from Google Sheets to database"""
        if not self.is_available():
            return False
        
        try:
            # Ensure sheet exists - sesuai dengan struktur Google Sheets
            # A=tanggal, B=nama produk, C=harga produk, D=link produk, E=komisi reguler, F=komisi gmv, G=target gmv, H=status
            headers = ['tanggal', 'nama produk', 'harga produk', 'link produk', 'komisi_reguler', 'komisi_gmv', 'target_gmv', 'status']
            sheet = self.ensure_sheet_exists('produk', headers)
            if not sheet:
                logger.warning("Sheet 'produk' tidak bisa dibuat atau diakses")
                return False
            # Use get_all_values to handle empty sheet better
            all_values = sheet.get_all_values()
            
            if len(all_values) <= 1:
                # Only header, no data
                logger.info("Sheet 'produk' is empty (only header)")
                return True
            
            # Get headers from first row - normalize to handle typos
            # Struktur Google Sheets: A=tanggal, B=nama produk, C=harga produk, D=link produk, E=komisi reguler, F=komisi gmv, G=target gmv, H=status
            headers_raw = all_values[0]
            
            # Map headers by position (index-based) untuk memastikan urutan sesuai Google Sheets
            # A=0: tanggal, B=1: nama produk, C=2: harga produk, D=3: link produk, E=4: komisi reguler, F=5: komisi gmv, G=6: target gmv, H=7: status
            header_mapping = {
                'tanggal': 'tanggal',
                'nama produk': 'nama_produk',
                'harga produk': 'harga_produk',
                'harga produl': 'harga_produk',  # Handle typo
                'link produk': 'link_produk',
                'komisi_reguler': 'komisi_reguler',
                'komisi reguler': 'komisi_reguler',  # Handle space
                'komisi_regul': 'komisi_reguler',  # Handle typo
                'komisi_gmv': 'komisi_gmv',
                'komisi gmv': 'komisi_gmv',  # Handle space
                'target_gmv': 'target_gmv',
                'target gmv': 'target_gmv',  # Handle space
                'status': 'status'
            }
            
            # Normalize headers dengan mapping
            normalized_headers = []
            for h in headers_raw:
                h_lower = h.lower().strip()
                normalized = header_mapping.get(h_lower, h_lower.replace(' ', '_'))
                normalized_headers.append(normalized)
            
            records = []
            row_number = 1  # Start from 1 (row 2 in sheet, after header)
            for row in all_values[1:]:
                if not any(row):  # Skip empty rows
                    row_number += 1
                    continue
                
                # Build record berdasarkan posisi kolom (index-based)
                # Pastikan urutan sesuai: A=tanggal, B=nama produk, C=harga produk, D=link produk, E=komisi reguler, F=komisi gmv, G=target gmv, H=status
                record = {}
                for i, header_normalized in enumerate(normalized_headers):
                    if i < len(row):
                        record[header_normalized] = row[i]
                
                # Fallback: jika header tidak ditemukan, gunakan posisi langsung
                # A=0: tanggal (skip), B=1: nama produk, C=2: harga produk, D=3: link produk, E=4: komisi reguler, F=5: komisi gmv, G=6: target gmv, H=7: status
                if len(row) >= 2 and 'nama_produk' not in record:
                    record['nama_produk'] = row[1] if len(row) > 1 else ''
                if len(row) >= 3 and 'harga_produk' not in record:
                    record['harga_produk'] = row[2] if len(row) > 2 else ''
                if len(row) >= 4 and 'link_produk' not in record:
                    record['link_produk'] = row[3] if len(row) > 3 else ''
                if len(row) >= 5 and 'komisi_reguler' not in record:
                    record['komisi_reguler'] = row[4] if len(row) > 4 else ''
                if len(row) >= 6 and 'komisi_gmv' not in record:
                    record['komisi_gmv'] = row[5] if len(row) > 5 else ''
                if len(row) >= 7 and 'target_gmv' not in record:
                    record['target_gmv'] = row[6] if len(row) > 6 else ''
                if len(row) >= 8 and 'status' not in record:
                    record['status'] = row[7] if len(row) > 7 else 'active'
                
                record['_row_number'] = row_number  # Store row number for ordering
                records.append(record)
                row_number += 1
            
            logger.info(f"Found {len(records)} product records to sync")
            
            for record in records:
                product_name = record.get('nama_produk', '').strip()
                if not product_name:
                    continue
                
                # Check if product exists
                product = Product.query.filter_by(product_name=product_name).first()
                
                try:
                    # Parse numeric values safely - handle various formats
                    def parse_number(value, default=0):
                        if not value:
                            return default
                        # Convert to string and clean
                        value_str = str(value).strip()
                        if not value_str:
                            return default
                        
                        # Remove currency symbols and prefixes (Rp, $, etc.)
                        import re
                        value_str = re.sub(r'^[Rp$€£¥\s]+', '', value_str, flags=re.IGNORECASE)
                        value_str = value_str.strip()
                        
                        if not value_str:
                            return default
                        
                        # Remove thousand separators (commas), keep decimal point
                        # Indonesian format: 50.000,00 -> 50000.00
                        # International format: 50,000.00 -> 50000.00
                        if ',' in value_str and '.' in value_str:
                            # Has both comma and dot - determine which is decimal
                            if value_str.rindex(',') > value_str.rindex('.'):
                                # Comma is decimal separator (Indonesian format)
                                value_str = value_str.replace('.', '').replace(',', '.')
                            else:
                                # Dot is decimal separator (International format)
                                value_str = value_str.replace(',', '')
                        elif ',' in value_str:
                            # Only comma - could be decimal or thousand separator
                            # If more than 3 digits after comma, it's probably thousand separator
                            parts = value_str.split(',')
                            if len(parts) == 2 and len(parts[1]) <= 2:
                                # Decimal separator
                                value_str = value_str.replace(',', '.')
                            else:
                                # Thousand separator
                                value_str = value_str.replace(',', '')
                        elif '.' in value_str:
                            # Only dot - could be decimal or thousand separator
                            parts = value_str.split('.')
                            if len(parts) == 2 and len(parts[1]) <= 2:
                                # Decimal separator
                                pass  # Keep as is
                            else:
                                # Thousand separator
                                value_str = value_str.replace('.', '')
                        
                        # Remove any remaining spaces and non-numeric characters except decimal point
                        value_str = re.sub(r'[^\d.]', '', value_str)
                        
                        if not value_str:
                            return default
                        try:
                            return float(value_str)
                        except (ValueError, TypeError):
                            logger.warning(f"Could not parse number: {value}, using default {default}")
                            return default
                    
                    harga_produk = parse_number(record.get('harga_produk', 0))
                    komisi_reguler = parse_number(record.get('komisi_reguler', 0))
                    komisi_gmv = parse_number(record.get('komisi_gmv', 0))
                    target_gmv = parse_number(record.get('target_gmv', 0))
                    
                    link_produk = record.get('link_produk', '').strip()
                    status = (record.get('status', 'active') or 'active').lower()
                    
                    sheet_order = record.get('_row_number', None)
                    
                    if product:
                        # Update existing
                        product.product_price = harga_produk
                        product.product_link = link_produk
                        product.regular_commission = komisi_reguler
                        product.gmv_max_commission = komisi_gmv
                        product.target_gmv = target_gmv
                        product.status = status
                        product.sheet_order = sheet_order  # Update sheet order
                        product.updated_at = datetime.now(timezone.utc)
                        logger.debug(f"Updated product: {product_name} (sheet_order={sheet_order})")
                    else:
                        # Create new
                        product = Product(
                            product_name=product_name,
                            category='General',  # Default category
                            product_link=link_produk,
                            product_price=harga_produk,
                            commission_percent=0,  # Will be calculated
                            regular_commission=komisi_reguler,
                            gmv_max_commission=komisi_gmv,
                            target_gmv=target_gmv,
                            status=status,
                            sheet_order=sheet_order  # Store sheet order
                        )
                        db.session.add(product)
                        logger.debug(f"Created new product: {product_name} (sheet_order={sheet_order})")
                except Exception as e:
                    logger.warning(f"Error processing product {product_name}: {e}", exc_info=True)
                    continue
            
            db.session.commit()
            logger.info(f"Synced {len(records)} products from Google Sheets")
            return True
        except Exception as e:
            logger.error(f"Error syncing products from sheet: {e}")
            db.session.rollback()
            return False
    
    # ==================== USERS ====================
    
    def add_user_to_sheet(self, user):
        """Add user to Google Sheet 'user'"""
        if not self.is_available():
            return False
        
        try:
            # Ensure sheet exists
            headers = ['nama', 'email', 'whatsapp', 'tiktok_akun', 'wallet', 'bank_account', 'telegram_username']
            sheet = self.ensure_sheet_exists('user', headers)
            if not sheet:
                logger.warning("Sheet 'user' tidak bisa dibuat atau diakses")
                return False
            # Check if user already exists (by name or telegram_id)
            try:
                records = sheet.get_all_records()
                for record in records:
                    if record.get('nama', '').strip() == (user.full_name or '').strip():
                        logger.info(f"User {user.full_name} already exists in sheet")
                        return True
            except:
                pass
            
            sheet.append_row([
                user.full_name or '',
                user.whatsapp or '',
                user.tiktok_akun or '',
                user.email or '',
                user.telegram_username or '',
                user.created_at.strftime('%d/%m/%Y') if user.created_at else datetime.now().strftime('%d/%m/%Y'),
                'Active'
            ])
            logger.info(f"User {user.full_name} added to Google Sheets")
            return True
        except Exception as e:
            logger.error(f"Error adding user to sheet: {e}")
            return False
    
    def sync_users_from_sheet(self):
        """Sync users from Google Sheets to database"""
        if not self.is_available():
            return False
        
        try:
            # Ensure sheet exists with headers
            headers = ['nama', 'email', 'whatsapp', 'tiktok_akun', 'wallet', 'bank_account', 'telegram_username']
            sheet = self.ensure_sheet_exists('user', headers)
            if not sheet:
                logger.warning("Sheet 'user' tidak bisa dibuat atau diakses")
                return False
            # Use get_all_values to handle empty sheet better
            all_values = sheet.get_all_values()
            
            if len(all_values) <= 1:
                # Only header, no data
                logger.info("Sheet 'user' is empty (only header)")
                return True
            
            # Get headers from first row
            headers = all_values[0]
            records = []
            for row in all_values[1:]:
                if not any(row):  # Skip empty rows
                    continue
                record = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        record[header] = row[i]
                records.append(record)
            
            for record in records:
                nama = record.get('nama', '').strip()
                if not nama:
                    continue
                
                # Check if user exists by name
                user = User.query.filter_by(full_name=nama).first()
                
                if not user:
                    # Create new user
                    user = User(
                        username=f"user_{nama.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
                        email=record.get('email', '') or f"{nama.lower().replace(' ', '_')}@telegram.local",
                        password_hash='telegram_user',
                        role='member',
                        full_name=nama,
                        whatsapp=record.get('whatsapp', ''),
                        tiktok_akun=record.get('tiktok_akun', ''),
                        telegram_username=record.get('telegram_username', '').replace('@', '') if record.get('telegram_username') else ''
                    )
                    db.session.add(user)
            
            db.session.commit()
            logger.info(f"Synced {len(records)} users from Google Sheets")
            return True
        except Exception as e:
            logger.error(f"Error syncing users from sheet: {e}", exc_info=True)
            db.session.rollback()
            return False
    
    # ==================== REPORTS ====================
    
    def add_report_to_sheet(self, content):
        """Add report/laporan to Google Sheet 'laporan'"""
        if not self.is_available():
            return False
        
        try:
            # Ensure sheet exists
            headers = ['nama_user', 'link_video', 'tanggal_upload', 'tiktok_akun', 'status', 'created_at']
            sheet = self.ensure_sheet_exists('laporan', headers)
            if not sheet:
                logger.warning("Sheet 'laporan' tidak bisa dibuat atau diakses")
                return False
            
            # Get user info
            user = User.query.get(content.creator_id)
            user_name = user.full_name if user else 'Unknown'
            tiktok_akun = content.tiktok_akun or (user.tiktok_akun if user else '')
            
            # Timestamp saat masuk ke sistem
            timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            # Match header order: ['nama_user', 'link_video', 'tanggal_upload', 'tiktok_akun', 'status', 'created_at']
            sheet.append_row([
                user_name,  # nama_user
                content.link_video or content.media_url or '',  # link_video
                content.tanggal_upload.strftime('%d/%m/%Y') if content.tanggal_upload else '',  # tanggal_upload
                tiktok_akun,  # tiktok_akun
                content.status,  # status
                timestamp  # created_at (timestamp saat masuk ke sistem)
            ])
            logger.info(f"Report added to Google Sheets for user {user_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding report to sheet: {e}")
            return False
    
    def sync_reports_from_sheet(self):
        """Sync reports from Google Sheets to database"""
        if not self.is_available():
            return False
        
        try:
            # Ensure sheet exists with headers
            headers = ['nama_user', 'link_video', 'tanggal_upload', 'tiktok_akun', 'status', 'created_at']
            sheet = self.ensure_sheet_exists('laporan', headers)
            if not sheet:
                logger.warning("Sheet 'laporan' tidak bisa dibuat atau diakses")
                return False
            # Use get_all_values to handle empty sheet better
            all_values = sheet.get_all_values()
            
            if len(all_values) <= 1:
                # Only header, no data
                logger.info("Sheet 'laporan' is empty (only header)")
                return True
            
            # Get headers from first row
            headers = all_values[0]
            records = []
            for row in all_values[1:]:
                if not any(row):  # Skip empty rows
                    continue
                record = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        record[header] = row[i]
                records.append(record)
            
            for record in records:
                nama_user = record.get('nama_user', '').strip()
                link_video = record.get('link_video', '').strip()
                
                if not nama_user or not link_video:
                    continue
                
                # Find user
                user = User.query.filter_by(full_name=nama_user).first()
                if not user:
                    continue
                
                # Check if content exists
                content = Content.query.filter_by(
                    creator_id=user.id,
                    link_video=link_video
                ).first()
                
                if not content:
                    # Create new content
                    tanggal_upload_str = record.get('tanggal_upload', '')
                    tanggal_upload = None
                    if tanggal_upload_str:
                        try:
                            tanggal_upload = datetime.strptime(tanggal_upload_str, '%d/%m/%Y').date()
                        except:
                            pass
                    
                    content = Content(
                        product_id=None,  # No product link for reports
                        creator_id=user.id,
                        title=f"Laporan dari {nama_user}",
                        description=f"Link: {link_video}",
                        link_video=link_video,
                        tanggal_upload=tanggal_upload,
                        tiktok_akun=record.get('tiktok_akun', ''),
                        status=record.get('status', 'pending').lower()
                    )
                    db.session.add(content)
            
            db.session.commit()
            logger.info(f"Synced {len(records)} reports from Google Sheets")
            return True
        except Exception as e:
            logger.error(f"Error syncing reports from sheet: {e}", exc_info=True)
            db.session.rollback()
            return False
    
    # ==================== FULL SYNC ====================
    
    def sync_all_from_sheets(self):
        """Sync all data from Google Sheets to database"""
        if not self.is_available():
            logger.warning("Google Sheets not available, skipping sync")
            return False
        
        try:
            results = {
                'products': False,
                'users': False,
                'reports': False
            }
            
            # Sync products
            try:
                results['products'] = self.sync_products_from_sheet()
                logger.info("Products sync completed")
            except Exception as e:
                logger.error(f"Error syncing products: {e}", exc_info=True)
                results['products'] = False
            
            # Sync users
            try:
                results['users'] = self.sync_users_from_sheet()
                logger.info("Users sync completed")
            except Exception as e:
                logger.error(f"Error syncing users: {e}", exc_info=True)
                results['users'] = False
            
            # Sync reports
            try:
                results['reports'] = self.sync_reports_from_sheet()
                logger.info("Reports sync completed")
            except Exception as e:
                logger.error(f"Error syncing reports: {e}", exc_info=True)
                results['reports'] = False
            
            # Return results dict
            return results
        except Exception as e:
            logger.error(f"Error in sync_all_from_sheets: {e}", exc_info=True)
            return {
                'products': False,
                'users': False,
                'reports': False
            }


"""
Telegram Bot untuk Affiliate Management System
Member bisa lapor konten via bot, Owner bisa approve via bot atau dashboard
"""

# Fix timezone issue for Python 3.13 BEFORE importing anything that uses apscheduler
import pytz
import os
# Set timezone environment before apscheduler is imported
os.environ['TZ'] = 'UTC'

# Monkey patch apscheduler.util to fix timezone issue
try:
    from apscheduler import util as apscheduler_util
    from tzlocal import get_localzone
    
    # Patch astimezone function to handle pytz
    original_astimezone = apscheduler_util.astimezone
    
    def patched_astimezone(obj):
        if obj is None:
            return pytz.UTC
        if isinstance(obj, pytz.BaseTzInfo):
            return obj
        # Try original first
        try:
            return original_astimezone(obj)
        except:
            return pytz.UTC
    
    apscheduler_util.astimezone = patched_astimezone
    
    # Also patch get_localzone
    import tzlocal
    tzlocal.get_localzone = lambda: pytz.UTC
except Exception as e:
    # If patching fails, we'll handle it in setup_bot
    pass

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.error import Conflict
from models import db, User, Product, Content, Commission, Payment, TeamMember
import logging
from dotenv import load_dotenv

load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID', '-1003342536716')
CHANNEL_CHAT_ID = os.getenv('CHANNEL_CHAT_ID', '-1003607323066')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store untuk temporary data (dalam production, pakai database atau Redis)
pending_submissions = {}  # {user_id: {product_name, link, platform}}
pending_registrations = {}  # {user_id: {step, data}}
pending_reports = {}  # {user_id: {step, links: [], waiting_date: False}}
pending_payments = {}  # {user_id: {type: 'purchase'|'upgrade', tier, amount, file_id}}
pending_upgrades = {}  # {user_id: {from_tier, to_tier, amount, file_id}}

def init_bot(app_instance, db_instance):
    """Initialize bot dengan Flask app dan database"""
    global flask_app, database
    flask_app = app_instance
    database = db_instance

# ==================== COMMAND HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_message = f"""
👋 Halo {user.first_name}!

Selamat datang di Affiliate Management Bot!

📋 **Perintah yang tersedia:**
/daftar - Daftar sebagai member baru
/lapor - Lapor kinerja (link video, tanggal upload, akun TikTok)
/komisi - Cek komisi Anda
/pembayaran - Cek pembayaran
/help - Bantuan

**Untuk member baru:**
Gunakan /daftar untuk mendaftar terlebih dahulu.

**Untuk member yang sudah terdaftar:**
Gunakan /lapor untuk melaporkan kinerja Anda.
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📖 **Bantuan Affiliate Bot**

**Untuk Member Baru:**
/daftar - Daftar sebagai member baru
/beli - Beli membership (Basic Rp 97k / VIP Rp 299k)
/upgrade - Upgrade ke VIP (dari Basic)

**Untuk Member:**
/lapor - Lapor kinerja harian
/komisi - Lihat total komisi Anda
/pembayaran - Lihat status pembayaran
/akun - Cek info akun TikTok affiliate (VIP only)

**Membership:**
- Basic Member (Rp 97k): Materi AI, Tutorial, Akses platform
- VIP Member (Rp 299k): Semua Basic + Group, TikTok Account, Bagi hasil 55%

**Catatan:**
- Bisa kirim banyak link (satu per satu atau sekaligus)
- Format tanggal: DD/MM/YYYY
- Untuk video jadwal, isi tanggal jadwal upload
- Laporan akan otomatis masuk ke sistem dengan timestamp
    """
    await update.message.reply_text(help_text)

async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /daftar command - User registration"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        # Check if user already registered
        existing_user = User.query.filter_by(telegram_id=user_id).first()
        if existing_user:
            await update.message.reply_text(
                f"✅ Anda sudah terdaftar!\n\n"
                f"Nama: {existing_user.full_name}\n"
                f"Role: {existing_user.role}\n\n"
                f"Gunakan /lapor untuk melaporkan kinerja Anda."
            )
            return
        
        # Start registration process
        pending_registrations[user_id] = {
            'step': 'waiting_name',
            'data': {}
        }
        
        await update.message.reply_text(
            "📝 **Pendaftaran Member Baru**\n\n"
            "Silakan isi data berikut:\n\n"
            "1️⃣ **Nama Lengkap:**\n"
            "Kirim nama lengkap Anda"
        )

async def report_kinerja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lapor command - User report kinerja"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        # Check if user is registered
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        if not telegram_user:
            await update.message.reply_text(
                "❌ Anda belum terdaftar!\n\n"
                "Silakan daftar terlebih dahulu dengan /daftar"
            )
            return
        
        # Set waiting for report - user bisa kirim banyak link
        pending_reports[user_id] = {
            'step': 'waiting_links',
            'user_id': telegram_user.id,
            'links': [],
            'waiting_date': False
        }
        
        await update.message.reply_text(
            "📊 **Laporan Kinerja**\n\n"
            "Kirim link video kamu hari ini.\n"
            "Bisa kirim banyak link (satu per satu atau sekaligus).\n\n"
            "**Contoh:**\n"
            "https://tiktok.com/@user/video/123\n"
            "https://tiktok.com/@user/video/456\n\n"
            "Setelah semua link dikirim, ketik 'selesai' untuk lanjut ke tanggal upload."
        )

async def submit_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /submit command - Member submit konten"""
    user = update.effective_user
    user_id = str(user.id)
    
    message = """
📝 **Submit Konten Baru**

Silakan kirim format berikut:
**Nama Produk | Link Konten | Platform**

**Contoh:**
Sarung Tangan Premium | https://tiktok.com/@user/video/123 | TikTok

**Platform:** TikTok atau Shopee
    """
    
    await update.message.reply_text(message)
    
    # Set state untuk menunggu input
    pending_submissions[user_id] = {'step': 'waiting_input'}

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages - Payment proof upload"""
    user = update.effective_user
    user_id = str(user.id)
    
    # Check if user is waiting for payment proof
    if user_id in pending_payments and pending_payments[user_id].get('status') == 'waiting_proof':
        photo = update.message.photo[-1]  # Get largest photo
        file_id = photo.file_id
        
        payment_data = pending_payments[user_id]
        payment_data['file_id'] = file_id
        payment_data['status'] = 'pending_verification'
        
        # Get file info
        file = await context.bot.get_file(file_id)
        
        await update.message.reply_text(
            "✅ **Bukti pembayaran diterima!**\n\n"
            f"📋 **Detail Pembayaran:**\n"
            f"Membership: {payment_data['membership_tier'].upper()} Member\n"
            f"Harga: Rp {payment_data['amount']:,}\n"
            f"Status: ⏳ Menunggu Verifikasi\n\n"
            f"Admin akan memverifikasi pembayaran Anda dalam 1x24 jam.\n\n"
            f"Anda akan mendapat notifikasi saat pembayaran sudah diverifikasi.\n\n"
            f"💡 **Tips:** Sambil menunggu, Anda bisa explore bot dengan /help"
        )
        
        # Notify admin
        try:
            with flask_app.app_context():
                from models import User
                admin_users = User.query.filter_by(role='owner').all()
                
                for admin in admin_users:
                    if admin.telegram_id:
                        keyboard = [
                            [
                                InlineKeyboardButton("✅ Verify", callback_data=f"verify_payment_{user_id}"),
                                InlineKeyboardButton("❌ Reject", callback_data=f"reject_payment_{user_id}")
                            ],
                            [
                                InlineKeyboardButton("👁️ Lihat Bukti", callback_data=f"view_proof_{user_id}")
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        notification_text = (
                            f"💳 **PEMBAYARAN BARU**\n\n"
                            f"👤 User: {payment_data.get('data', {}).get('full_name', 'N/A')}\n"
                            f"📱 WhatsApp: {payment_data.get('data', {}).get('whatsapp', 'N/A')}\n"
                            f"💳 Membership: {payment_data['membership_tier'].upper()} Member\n"
                            f"💰 Harga: Rp {payment_data['amount']:,}\n"
                            f"📅 Tanggal: {update.message.date.strftime('%d/%m/%Y %H:%M')}\n\n"
                            f"Pilih aksi:"
                        )
                        
                        await context.bot.send_message(
                            chat_id=admin.telegram_id,
                            text=notification_text,
                            reply_markup=reply_markup
                        )
                        
                        # Send payment proof photo to admin
                        await context.bot.send_photo(
                            chat_id=admin.telegram_id,
                            photo=file_id,
                            caption=f"Bukti pembayaran dari {payment_data.get('data', {}).get('full_name', 'User')}"
                        )
        except Exception as e:
            logger.error(f"Error notifying admin: {e}")
        
        return
    
    # If not waiting for payment proof, ignore
    await update.message.reply_text(
        "📸 Foto diterima, tapi Anda tidak sedang dalam proses pembayaran.\n\n"
        "Gunakan /beli untuk membeli membership atau /upgrade untuk upgrade."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages - Process registration, report, or submission"""
    user = update.effective_user
    user_id = str(user.id)
    message_text = update.message.text
    
    # Handle registration
    if user_id in pending_registrations:
        await handle_registration_input(update, context, message_text, user_id)
        return
    
    # Handle report
    if user_id in pending_reports:
        await handle_report_input(update, context, message_text, user_id)
        return
    
    # Check if user is in submission mode (legacy)
    if user_id in pending_submissions and pending_submissions[user_id].get('step') == 'waiting_input':
        try:
            # Parse format: "Nama Produk | Link | Platform"
            parts = [p.strip() for p in message_text.split('|')]
            
            if len(parts) < 3:
                await update.message.reply_text(
                    "❌ Format salah!\n\n"
                    "Format yang benar:\n"
                    "Nama Produk | Link Konten | Platform\n\n"
                    "Contoh:\n"
                    "Sarung Tangan Premium | https://tiktok.com/... | TikTok"
                )
                return
            
            product_name = parts[0]
            link = parts[1]
            platform = parts[2].lower()
            
            if platform not in ['tiktok', 'shopee']:
                await update.message.reply_text(
                    "❌ Platform harus 'TikTok' atau 'Shopee'"
                )
                return
            
            # Save submission
            pending_submissions[user_id] = {
                'step': 'submitted',
                'product_name': product_name,
                'link': link,
                'platform': platform,
                'user_id': user_id,
                'username': user.username or user.first_name
            }
            
            # Create content in database
            with flask_app.app_context():
                # Find product by name
                product = Product.query.filter(
                    Product.product_name.ilike(f'%{product_name}%')
                ).first()
                
                if not product:
                    await update.message.reply_text(
                        f"❌ Produk '{product_name}' tidak ditemukan di database.\n\n"
                        "Silakan hubungi admin untuk menambahkan produk terlebih dahulu."
                    )
                    del pending_submissions[user_id]
                    return
                
                # Find or create user
                telegram_user = User.query.filter_by(telegram_id=user_id).first()
                if not telegram_user:
                    telegram_user = User.query.filter_by(username=f"telegram_{user_id}").first()
                if not telegram_user:
                    telegram_user = User(
                        username=f"telegram_{user_id}",
                        email=f"telegram_{user_id}@telegram.local",
                        password_hash="telegram_user",
                        role='member',
                        full_name=user.first_name or user.username or "Telegram User",
                        telegram_id=user_id,
                        telegram_username=user.username or None
                    )
                    database.session.add(telegram_user)
                    database.session.commit()
                
                # Create content
                content = Content(
                    product_id=product.id,
                    creator_id=telegram_user.id,
                    title=f"Konten dari {user.first_name}",
                    description=f"Produk: {product_name}\nLink: {link}",
                    media_url=link,
                    platform=platform,
                    quality_score=0,
                    status='pending'
                )
                database.session.add(content)
                database.session.commit()
                
                # Send confirmation to user
                await update.message.reply_text(
                    f"✅ **Konten Berhasil Disubmit!**\n\n"
                    f"📦 Produk: {product_name}\n"
                    f"🔗 Link: {link}\n"
                    f"📱 Platform: {platform}\n\n"
                    f"Status: ⏳ Menunggu Approval\n\n"
                    f"Konten Anda sedang direview oleh admin. "
                    f"Anda akan mendapat notifikasi setelah disetujui."
                )
                
                # Send notification to owner in group
                keyboard = [
                    [
                        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{content.id}"),
                        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{content.id}")
                    ],
                    [
                        InlineKeyboardButton("📊 Lihat Detail", callback_data=f"detail_{content.id}")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                notification_text = (
                    f"📝 **Konten Baru dari Member**\n\n"
                    f"👤 Member: {user.first_name} (@{user.username or 'N/A'})\n"
                    f"📦 Produk: {product_name}\n"
                    f"🔗 Link: {link}\n"
                    f"📱 Platform: {platform}\n"
                    f"🆔 Content ID: {content.id}\n\n"
                    f"Pilih aksi:"
                )
                
                await context.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=notification_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                
                # Clear submission
                del pending_submissions[user_id]
                
        except Exception as e:
            logger.error(f"Error processing submission: {e}")
            await update.message.reply_text(
                "❌ Terjadi error saat memproses submission. Silakan coba lagi atau hubungi admin."
            )
            if user_id in pending_submissions:
                del pending_submissions[user_id]

async def handle_registration_input(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str, user_id: str):
    """Handle registration input step by step"""
    reg_data = pending_registrations[user_id]
    step = reg_data['step']
    data = reg_data['data']
    
    try:
        if step == 'waiting_name':
            data['full_name'] = message_text
            reg_data['step'] = 'waiting_whatsapp'
            await update.message.reply_text(
                "✅ Nama tersimpan!\n\n"
                "2️⃣ **Nomor WhatsApp:**\n"
                "Kirim nomor WhatsApp Anda (contoh: 081234567890)"
            )
        
        elif step == 'waiting_whatsapp':
            data['whatsapp'] = message_text
            reg_data['step'] = 'waiting_email'
            await update.message.reply_text(
                "✅ WhatsApp tersimpan!\n\n"
                "3️⃣ **Email (Optional):**\n"
                "Kirim email Anda, atau ketik 'skip' untuk melewati"
            )
        
        elif step == 'waiting_email':
            if message_text.lower() != 'skip':
                data['email'] = message_text
            reg_data['step'] = 'waiting_payment'
            await update.message.reply_text(
                "✅ Email tersimpan!\n\n"
                "4️⃣ **Metode Pembayaran:**\n"
                "Pilih metode pembayaran:\n"
                "1. Wallet (DANA/OVO/GoPay)\n"
                "2. Bank\n\n"
                "Ketik '1' untuk Wallet atau '2' untuk Bank"
            )
        
        elif step == 'waiting_payment':
            if message_text == '1':
                reg_data['step'] = 'waiting_wallet'
                await update.message.reply_text(
                    "✅ Wallet dipilih!\n\n"
                    "5️⃣ **Detail Wallet:**\n"
                    "Kirim detail wallet Anda (contoh: DANA - 081234567890)"
                )
            elif message_text == '2':
                reg_data['step'] = 'waiting_bank'
                await update.message.reply_text(
                    "✅ Bank dipilih!\n\n"
                    "5️⃣ **Detail Bank:**\n"
                    "Kirim detail bank Anda (contoh: BCA - 1234567890 - Nama Pemilik)"
                )
            else:
                await update.message.reply_text(
                    "❌ Pilihan tidak valid. Ketik '1' untuk Wallet atau '2' untuk Bank"
                )
                return
        
        elif step == 'waiting_wallet':
            data['wallet'] = message_text
            data['bank_account'] = None
            # Move to membership selection
            reg_data['step'] = 'waiting_membership'
            keyboard = [
                [
                    InlineKeyboardButton("Basic Member - Rp 97.000", callback_data="membership_basic"),
                    InlineKeyboardButton("VIP Member - Rp 299.000", callback_data="membership_vip")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "✅ Wallet tersimpan!\n\n"
                "6️⃣ **Pilih Membership:**\n\n"
                "📦 **Basic Member (Rp 97.000)**\n"
                "✅ Materi AI Content Creation\n"
                "✅ Tutorial dasar sampai upload\n"
                "✅ Akses platform\n\n"
                "👑 **VIP Member (Rp 299.000)**\n"
                "✅ Semua Basic Member\n"
                "✅ Group diskusi\n"
                "✅ Tanya jawab\n"
                "✅ Zoom meeting\n"
                "✅ Akun TikTok affiliate\n"
                "✅ Bagi hasil 55%\n\n"
                "Pilih membership yang ingin dibeli:",
                reply_markup=reply_markup
            )
        
        elif step == 'waiting_bank':
            data['bank_account'] = message_text
            data['wallet'] = None
            # Move to membership selection
            reg_data['step'] = 'waiting_membership'
            keyboard = [
                [
                    InlineKeyboardButton("Basic Member - Rp 97.000", callback_data="membership_basic"),
                    InlineKeyboardButton("VIP Member - Rp 299.000", callback_data="membership_vip")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "✅ Bank tersimpan!\n\n"
                "6️⃣ **Pilih Membership:**\n\n"
                "📦 **Basic Member (Rp 97.000)**\n"
                "✅ Materi AI Content Creation\n"
                "✅ Tutorial dasar sampai upload\n"
                "✅ Akses platform\n\n"
                "👑 **VIP Member (Rp 299.000)**\n"
                "✅ Semua Basic Member\n"
                "✅ Group diskusi\n"
                "✅ Tanya jawab\n"
                "✅ Zoom meeting\n"
                "✅ Akun TikTok affiliate\n"
                "✅ Bagi hasil 55%\n\n"
                "Pilih membership yang ingin dibeli:",
                reply_markup=reply_markup
            )
        
        elif step == 'waiting_membership':
            # This should be handled by callback, but handle text input as fallback
            if message_text.lower() in ['basic', '1']:
                data['membership_tier'] = 'basic'
                data['membership_price'] = 97000
            elif message_text.lower() in ['vip', '2']:
                data['membership_tier'] = 'vip'
                data['membership_price'] = 299000
            else:
                await update.message.reply_text(
                    "❌ Pilihan tidak valid. Pilih dari tombol di atas atau ketik 'basic' atau 'vip'"
                )
                return
            
            # Move to payment instruction
            reg_data['step'] = 'waiting_payment_proof'
            await update.message.reply_text(
                f"💳 **PEMBELIAN {data['membership_tier'].upper()} MEMBER**\n\n"
                f"Harga: Rp {data['membership_price']:,}\n\n"
                f"**Cara Pembayaran:**\n"
                f"1. Transfer ke rekening berikut:\n"
                f"   💰 BCA: 1131339351 (a.n. Andik veris febriyanto)\n"
                f"   💰 DANA: 085732740006 (a.n. Andik veris febriyanto)\n\n"
                f"2. Upload bukti pembayaran (foto/screenshot)\n"
                f"   (Kirim foto bukti transfer)\n\n"
                f"⚠️ Setelah pembayaran diverifikasi, membership akan aktif otomatis."
            )
    
    except Exception as e:
        logger.error(f"Error in registration: {e}")
        await update.message.reply_text(
            "❌ Terjadi error. Silakan coba lagi dengan /daftar"
        )
        if user_id in pending_registrations:
            del pending_registrations[user_id]

async def complete_registration(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str, data: dict):
    """Complete user registration"""
    user = update.effective_user
    
    with flask_app.app_context():
        try:
            # Create user
            new_user = User(
                username=f"telegram_{user_id}",
                email=data.get('email') or f"telegram_{user_id}@telegram.local",
                password_hash="telegram_user",
                role='member',
                full_name=data.get('full_name', user.first_name or 'User'),
                whatsapp=data.get('whatsapp', ''),
                tiktok_akun='',  # Akan diisi admin nanti
                wallet=data.get('wallet'),
                bank_account=data.get('bank_account'),
                telegram_id=user_id,
                telegram_username=user.username or None
            )
            database.session.add(new_user)
            database.session.commit()
            
            # Add to Google Sheets
            try:
                from google_sheets_service import GoogleSheetsService
                gs_service = GoogleSheetsService()
                if gs_service.is_available():
                    gs_service.add_user_to_sheet(new_user)
            except Exception as e:
                logger.warning(f"Failed to add user to Google Sheets: {e}")
            
            await update.message.reply_text(
                f"✅ **Pendaftaran Berhasil!**\n\n"
                f"👤 Nama: {new_user.full_name}\n"
                f"📱 WhatsApp: {new_user.whatsapp}\n"
                f"💳 Pembayaran: {new_user.wallet or new_user.bank_account}\n\n"
                f"Selamat! Anda sudah terdaftar sebagai member.\n"
                f"Admin akan mengatur akun TikTok Anda.\n\n"
                f"Gunakan /lapor untuk melaporkan kinerja Anda."
            )
            
            # Clear registration
            if user_id in pending_registrations:
                del pending_registrations[user_id]
        
        except Exception as e:
            logger.error(f"Error completing registration: {e}")
            database.session.rollback()
            await update.message.reply_text(
                "❌ Terjadi error saat mendaftar. Silakan coba lagi atau hubungi admin."
            )

async def handle_report_input(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str, user_id: str):
    """Handle report input - User kirim link, lalu tanggal upload"""
    try:
        report_data = pending_reports[user_id]
        step = report_data.get('step', 'waiting_links')
        links = report_data.get('links', [])
        waiting_date = report_data.get('waiting_date', False)
        
        # Check if user wants to finish adding links
        if message_text.lower().strip() == 'selesai' and step == 'waiting_links' and len(links) > 0:
            # Move to date input
            report_data['step'] = 'waiting_date'
            report_data['waiting_date'] = True
            await update.message.reply_text(
                "✅ Link sudah dikumpulkan!\n\n"
                f"Total link: {len(links)}\n\n"
                "📅 **Tanggal Upload:**\n"
                "Kirim tanggal upload untuk semua video ini.\n"
                "Format: DD/MM/YYYY\n\n"
                "**Contoh:**\n"
                "17/12/2024\n\n"
                "💡 **Tips:** Jika video dijadwalkan, isi tanggal jadwal upload."
            )
            return
        
        if step == 'waiting_links':
            # User is sending links
            # Extract all TikTok links from message
            import re
            tiktok_pattern = r'https?://(?:www\.)?(?:vm\.|vt\.)?tiktok\.com/[^\s]+'
            found_links = re.findall(tiktok_pattern, message_text, re.IGNORECASE)
            
            if found_links:
                # Add new links
                for link in found_links:
                    if link not in links:
                        links.append(link)
                
                report_data['links'] = links
                
                await update.message.reply_text(
                    f"✅ Link ditambahkan!\n\n"
                    f"Total link: {len(links)}\n\n"
                    f"Kirim link lagi atau ketik 'selesai' untuk lanjut ke tanggal upload."
                )
            else:
                # Check if user typed 'selesai' without links
                if message_text.lower().strip() == 'selesai':
                    await update.message.reply_text(
                        "❌ Belum ada link yang dikirim!\n\n"
                        "Kirim link video TikTok terlebih dahulu."
                    )
                else:
                    await update.message.reply_text(
                        "❌ Link tidak valid!\n\n"
                        "Pastikan link dari TikTok.\n"
                        "Contoh: https://tiktok.com/@user/video/123\n\n"
                        "Atau ketik 'selesai' jika sudah selesai kirim link."
                    )
            return
        
        elif step == 'waiting_date':
            # User is sending date
            try:
                from datetime import datetime
                tanggal = datetime.strptime(message_text.strip(), '%d/%m/%Y').date()
                
                # Save all links with the same date
                with flask_app.app_context():
                    creator_id = report_data['user_id']
                    user_obj = User.query.get(creator_id)
                    
                    if not user_obj:
                        await update.message.reply_text("❌ User tidak ditemukan!")
                        return
                    
                    saved_count = 0
                    for link in links:
                        # Create content/report for each link
                        content = Content(
                            product_id=None,
                            creator_id=creator_id,
                            title=f"Laporan dari {user_obj.full_name}",
                            description=f"Link: {link}\nTanggal Upload: {tanggal}",
                            link_video=link,
                            tanggal_upload=tanggal,
                            tiktok_akun=user_obj.tiktok_akun or '',  # Pakai dari user
                            status='pending'
                        )
                        database.session.add(content)
                        saved_count += 1
                    
                    database.session.commit()
                    
                    # Add to Google Sheets
                    try:
                        from google_sheets_service import GoogleSheetsService
                        gs_service = GoogleSheetsService()
                        if gs_service.is_available():
                            # Get all saved content to add to sheet
                            for link in links:
                                content = Content.query.filter_by(
                                    creator_id=creator_id,
                                    link_video=link,
                                    tanggal_upload=tanggal
                                ).order_by(Content.created_at.desc()).first()
                                if content:
                                    gs_service.add_report_to_sheet(content)
                    except Exception as e:
                        logger.warning(f"Failed to add report to Google Sheets: {e}")
                    
                    await update.message.reply_text(
                        f"✅ **Laporan Berhasil Disimpan!**\n\n"
                        f"📹 Total Video: {saved_count}\n"
                        f"📅 Tanggal Upload: {tanggal.strftime('%d/%m/%Y')}\n\n"
                        f"Status: ⏳ Menunggu Review\n\n"
                        f"Semua laporan sudah masuk ke sistem dan akan direview oleh admin."
                    )
                    
                    # Notify admin about new reports
                    try:
                        await notify_admin_new_reports(context, links, user_obj, tanggal)
                    except Exception as e:
                        logger.warning(f"Failed to notify admin: {e}")
                    
                    # Clear report
                    if user_id in pending_reports:
                        del pending_reports[user_id]
            
            except ValueError:
                await update.message.reply_text(
                    "❌ Format tanggal salah!\n\n"
                    "Format yang benar: DD/MM/YYYY\n\n"
                    "**Contoh:**\n"
                    "17/12/2024"
                )
            except Exception as e:
                logger.error(f"Error saving report: {e}")
                await update.message.reply_text(
                    "❌ Terjadi error saat menyimpan laporan. Silakan coba lagi atau hubungi admin."
                )
                if user_id in pending_reports:
                    del pending_reports[user_id]
    
    except Exception as e:
        logger.error(f"Error processing report: {e}")
        await update.message.reply_text(
            "❌ Terjadi error saat memproses laporan. Silakan coba lagi atau hubungi admin."
        )
        if user_id in pending_reports:
            del pending_reports[user_id]

async def check_commission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /komisi command - Member cek komisi"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        # Find user
        telegram_user = User.query.filter_by(username=f"telegram_{user_id}").first()
        
        if not telegram_user:
            await update.message.reply_text(
                "❌ Anda belum terdaftar. Silakan submit konten terlebih dahulu."
            )
            return
        
        # Get commissions
        commissions = Commission.query.filter_by(creator_id=telegram_user.id).all()
        
        total_commission = sum(c.team_share for c in commissions)
        pending_commissions = sum(c.team_share for c in commissions if c.status == 'pending')
        approved_commissions = sum(c.team_share for c in commissions if c.status == 'approved')
        paid_commissions = sum(c.team_share for c in commissions if c.status == 'paid')
        
        # Get pending payments
        pending_payments = Payment.query.filter_by(
            user_id=telegram_user.id,
            status='pending'
        ).all()
        total_pending_payment = sum(p.amount for p in pending_payments)
        
        message = (
            f"💰 **Komisi Anda**\n\n"
            f"📊 Total Komisi: Rp {total_commission:,.0f}\n"
            f"⏳ Pending: Rp {pending_commissions:,.0f}\n"
            f"✅ Approved: Rp {approved_commissions:,.0f}\n"
            f"💵 Sudah Dibayar: Rp {paid_commissions:,.0f}\n\n"
            f"💳 Pembayaran Pending: Rp {total_pending_payment:,.0f}\n\n"
            f"📝 Total Konten: {len(commissions)}"
        )
        
        await update.message.reply_text(message)

async def check_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pembayaran command - Member cek pembayaran"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        # Find user
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        
        if not telegram_user:
            await update.message.reply_text(
                "❌ Anda belum terdaftar. Silakan daftar dengan /daftar terlebih dahulu."
            )
            return
        
        # Check pending payments
        if user_id in pending_payments:
            payment_data = pending_payments[user_id]
            status_text = "⏳ Menunggu Verifikasi" if payment_data.get('status') == 'pending_verification' else "⏳ Menunggu Bukti"
            await update.message.reply_text(
                f"💳 **Status Pembayaran**\n\n"
                f"Tipe: {payment_data['type'].upper()}\n"
                f"Membership: {payment_data['membership_tier'].upper()} Member\n"
                f"Harga: Rp {payment_data['amount']:,}\n"
                f"Status: {status_text}\n\n"
                f"Admin akan memverifikasi dalam 1x24 jam."
            )
            return
        
        # Get payments from database (if membership system implemented)
        await update.message.reply_text(
            "💳 **Riwayat Pembayaran**\n\n"
            "Belum ada pembayaran yang tercatat.\n\n"
            "Gunakan /beli untuk membeli membership."
        )

async def purchase_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /beli command - Purchase membership"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        # Check if user already registered
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        if not telegram_user:
            await update.message.reply_text(
                "❌ Anda belum terdaftar!\n\n"
                "Silakan daftar terlebih dahulu dengan /daftar"
            )
            return
        
        # Check if already has pending payment
        if user_id in pending_payments:
            await update.message.reply_text(
                "⏳ Anda sudah ada pembayaran yang sedang diproses.\n\n"
                "Tunggu verifikasi admin atau hubungi admin jika sudah lebih dari 24 jam."
            )
            return
        
        keyboard = [
            [
                InlineKeyboardButton("Basic Member - Rp 97.000", callback_data="purchase_basic"),
                InlineKeyboardButton("VIP Member - Rp 299.000", callback_data="purchase_vip")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "💳 **BELI MEMBERSHIP**\n\n"
            "📦 **Basic Member (Rp 97.000)**\n"
            "✅ Materi AI Content Creation\n"
            "✅ Tutorial dasar sampai upload\n"
            "✅ Akses platform\n\n"
            "👑 **VIP Member (Rp 299.000)**\n"
            "✅ Semua Basic Member\n"
            "✅ Group diskusi\n"
            "✅ Tanya jawab\n"
            "✅ Zoom meeting\n"
            "✅ Akun TikTok affiliate\n"
            "✅ Bagi hasil 55%\n\n"
            "Pilih membership yang ingin dibeli:",
            reply_markup=reply_markup
        )

async def upgrade_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /upgrade command - Upgrade to VIP"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        if not telegram_user:
            await update.message.reply_text(
                "❌ Anda belum terdaftar. Silakan daftar dengan /daftar terlebih dahulu."
            )
            return
        
        # Check current membership (simplified - assume basic if no membership system yet)
        # TODO: Check actual membership from database
        
        keyboard = [
            [InlineKeyboardButton("Ya, Saya Mau Upgrade", callback_data="confirm_upgrade")],
            [InlineKeyboardButton("Batal", callback_data="cancel_upgrade")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⬆️ **UPGRADE KE VIP MEMBER**\n\n"
            "**Current Membership:** Basic Member\n"
            "**Upgrade to:** VIP Member\n\n"
            "💰 **Harga Upgrade:**\n"
            "VIP Member: Rp 299.000\n"
            "Basic Member: Rp 97.000\n"
            "─────────────────────\n"
            "Selisih: Rp 202.000\n\n"
            "📋 **Fasilitas VIP:**\n"
            "✅ Semua Basic Member\n"
            "✅ Group diskusi\n"
            "✅ Tanya jawab langsung\n"
            "✅ Zoom meeting\n"
            "✅ Akun TikTok affiliate (keranjang kuning)\n"
            "✅ Reporting & validasi\n"
            "✅ Bagi hasil 55% komisi!\n\n"
            "**Cara Pembayaran:**\n"
            "1. Transfer Rp 202.000 ke:\n"
            "   💰 BCA: 1234567890\n"
            "   💰 DANA: 081234567890\n\n"
            "2. Upload bukti pembayaran\n"
            "   (Kirim foto bukti transfer)\n\n"
            "Lanjutkan upgrade?",
            reply_markup=reply_markup
        )

async def check_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /akun command - Check TikTok affiliate account (VIP only)"""
    user = update.effective_user
    user_id = str(user.id)
    
    with flask_app.app_context():
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        if not telegram_user:
            await update.message.reply_text(
                "❌ Anda belum terdaftar. Silakan daftar dengan /daftar terlebih dahulu."
            )
            return
        
        # TODO: Check if user is VIP and has account assigned
        # For now, show placeholder
        await update.message.reply_text(
            "📱 **AKUN TIKTOK AFFILIATE**\n\n"
            "⏳ Fitur ini sedang dalam pengembangan.\n\n"
            "Akun TikTok affiliate akan di-assign oleh admin setelah Anda menjadi VIP Member.\n\n"
            "Gunakan /upgrade untuk upgrade ke VIP."
        )

# ==================== ADMIN COMMANDS ====================

def check_owner(user_id: str):
    """Check if user is owner"""
    with flask_app.app_context():
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        return telegram_user and telegram_user.role == 'owner'

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command - Hanya untuk owner"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text(
            "❌ Command ini hanya untuk admin/owner!\n\n"
            "Gunakan /help untuk melihat commands yang tersedia."
        )
        return
    
    menu = """
👨‍💼 **ADMIN MENU**

📊 **Reports:**
/pending - List pending reports
/reports - List semua reports
/approve <id> - Approve report (contoh: /approve 123)
/reject <id> <alasan> - Reject report (contoh: /reject 123 Link tidak valid)

👥 **Users:**
/users - List semua users
/user <id> - Detail user (contoh: /user 5)

📈 **Statistics:**
/stats - Statistik sistem

💡 **Tips:**
- Gunakan /pending untuk melihat reports yang perlu di-review
- Gunakan /approve atau /reject untuk quick action
    """
    
    await update.message.reply_text(menu)

async def pending_reports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pending command - List pending reports"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text("❌ Command ini hanya untuk admin!")
        return
    
    with flask_app.app_context():
        # Get pending reports
        reports = Content.query.filter(
            Content.link_video != None,
            Content.link_video != '',
            Content.status == 'pending'
        ).order_by(Content.created_at.desc()).limit(10).all()
        
        if not reports:
            await update.message.reply_text("✅ Tidak ada pending reports!")
            return
        
        message = f"⏳ **PENDING REPORTS** ({len(reports)})\n\n"
        
        for r in reports:
            creator = User.query.get(r.creator_id) if r.creator_id else None
            message += (
                f"📊 **Report #{r.id}**\n"
                f"👤 User: {creator.full_name if creator else 'N/A'}\n"
                f"🔗 Link: {r.link_video[:50]}...\n"
                f"📅 Upload: {r.tanggal_upload.strftime('%d/%m/%Y') if r.tanggal_upload else 'N/A'}\n"
                f"📅 Lapor: {r.created_at.strftime('%d/%m/%Y %H:%M') if r.created_at else 'N/A'}\n"
                f"**Action:** /approve {r.id} atau /reject {r.id}\n\n"
            )
        
        message += "💡 Gunakan /approve <id> atau /reject <id> untuk action"
        
        await update.message.reply_text(message)

async def approve_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /approve <id> command"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text("❌ Command ini hanya untuk admin!")
        return
    
    # Get report ID from command
    command_text = update.message.text.strip()
    parts = command_text.split()
    
    if len(parts) < 2:
        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "**Format:** /approve <id>\n"
            "**Contoh:** /approve 123"
        )
        return
    
    try:
        report_id = int(parts[1])
    except ValueError:
        await update.message.reply_text("❌ ID harus berupa angka!")
        return
    
    with flask_app.app_context():
        report = Content.query.get(report_id)
        
        if not report:
            await update.message.reply_text(f"❌ Report #{report_id} tidak ditemukan!")
            return
        
        if report.status != 'pending':
            await update.message.reply_text(
                f"⚠️ Report #{report_id} sudah di-{report.status}!"
            )
            return
        
        # Approve report
        report.status = 'approved'
        report.quality_score = 7.0  # Default score
        database.session.commit()
        
        # Notify creator
        creator = User.query.get(report.creator_id) if report.creator_id else None
        if creator and creator.telegram_id:
            try:
                await context.bot.send_message(
                    chat_id=creator.telegram_id,
                    text=(
                        f"✅ **Report Anda Disetujui!**\n\n"
                        f"📊 Report ID: #{report_id}\n"
                        f"🔗 Link: {report.link_video}\n"
                        f"⭐ Quality Score: {report.quality_score}\n\n"
                        f"Gunakan /komisi untuk cek komisi Anda."
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to notify creator: {e}")
        
        await update.message.reply_text(
            f"✅ **Report #{report_id} berhasil di-approve!**\n\n"
            f"👤 User: {creator.full_name if creator else 'N/A'}\n"
            f"🔗 Link: {report.link_video[:50]}...\n"
            f"⭐ Quality Score: {report.quality_score}"
        )

async def reject_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reject <id> <alasan> command"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text("❌ Command ini hanya untuk admin!")
        return
    
    # Get report ID and reason from command
    command_text = update.message.text.strip()
    parts = command_text.split(maxsplit=2)
    
    if len(parts) < 2:
        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "**Format:** /reject <id> <alasan>\n"
            "**Contoh:** /reject 123 Link tidak valid"
        )
        return
    
    try:
        report_id = int(parts[1])
    except ValueError:
        await update.message.reply_text("❌ ID harus berupa angka!")
        return
    
    reason = parts[2] if len(parts) > 2 else "Tidak memenuhi standar"
    
    with flask_app.app_context():
        report = Content.query.get(report_id)
        
        if not report:
            await update.message.reply_text(f"❌ Report #{report_id} tidak ditemukan!")
            return
        
        if report.status != 'pending':
            await update.message.reply_text(
                f"⚠️ Report #{report_id} sudah di-{report.status}!"
            )
            return
        
        # Reject report
        report.status = 'rejected'
        database.session.commit()
        
        # Notify creator
        creator = User.query.get(report.creator_id) if report.creator_id else None
        if creator and creator.telegram_id:
            try:
                await context.bot.send_message(
                    chat_id=creator.telegram_id,
                    text=(
                        f"❌ **Report Anda Ditolak**\n\n"
                        f"📊 Report ID: #{report_id}\n"
                        f"🔗 Link: {report.link_video}\n"
                        f"📝 Alasan: {reason}\n\n"
                        f"Silakan submit report baru dengan /lapor"
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to notify creator: {e}")
        
        await update.message.reply_text(
            f"❌ **Report #{report_id} berhasil di-reject!**\n\n"
            f"👤 User: {creator.full_name if creator else 'N/A'}\n"
            f"🔗 Link: {report.link_video[:50]}...\n"
            f"📝 Alasan: {reason}"
        )

async def list_reports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reports command - List all reports"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text("❌ Command ini hanya untuk admin!")
        return
    
    # Get status filter if provided
    command_text = update.message.text.strip()
    parts = command_text.split()
    status_filter = parts[1] if len(parts) > 1 else None
    
    with flask_app.app_context():
        query = Content.query.filter(
            Content.link_video != None,
            Content.link_video != ''
        )
        
        if status_filter:
            query = query.filter(Content.status == status_filter)
        
        reports = query.order_by(Content.created_at.desc()).limit(20).all()
        
        if not reports:
            await update.message.reply_text(
                f"📭 Tidak ada reports{f' dengan status {status_filter}' if status_filter else ''}!"
            )
            return
        
        message = f"📊 **ALL REPORTS** ({len(reports)})\n\n"
        
        for r in reports[:10]:  # Limit to 10 for readability
            creator = User.query.get(r.creator_id) if r.creator_id else None
            status_emoji = "✅" if r.status == 'approved' else "❌" if r.status == 'rejected' else "⏳"
            message += (
                f"{status_emoji} **#{r.id}** - {r.status}\n"
                f"👤 {creator.full_name if creator else 'N/A'}\n"
                f"🔗 {r.link_video[:40]}...\n"
                f"📅 {r.created_at.strftime('%d/%m/%Y') if r.created_at else 'N/A'}\n\n"
            )
        
        if len(reports) > 10:
            message += f"... dan {len(reports) - 10} reports lainnya\n\n"
        
        message += "💡 Gunakan /reports <status> untuk filter (pending/approved/rejected)"
        
        await update.message.reply_text(message)

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /users command - List all users"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text("❌ Command ini hanya untuk admin!")
        return
    
    with flask_app.app_context():
        users = User.query.order_by(User.created_at.desc()).limit(20).all()
        
        if not users:
            await update.message.reply_text("📭 Tidak ada users!")
            return
        
        message = f"👥 **ALL USERS** ({len(users)})\n\n"
        
        for u in users[:10]:  # Limit to 10
            role_emoji = "👑" if u.role == 'owner' else "👨‍💼" if u.role == 'manager' else "👤"
            message += (
                f"{role_emoji} **#{u.id}** - {u.full_name or u.username}\n"
                f"📧 {u.email or 'N/A'}\n"
                f"🔑 Role: {u.role}\n"
                f"📅 {u.created_at.strftime('%d/%m/%Y') if u.created_at else 'N/A'}\n\n"
            )
        
        if len(users) > 10:
            message += f"... dan {len(users) - 10} users lainnya\n\n"
        
        message += "💡 Gunakan /user <id> untuk detail user"
        
        await update.message.reply_text(message)

async def system_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - System statistics"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text("❌ Command ini hanya untuk admin!")
        return
    
    with flask_app.app_context():
        # Count users
        total_users = User.query.count()
        active_users = User.query.filter(User.role == 'member').count()
        
        # Count reports
        total_reports = Content.query.filter(
            Content.link_video != None,
            Content.link_video != ''
        ).count()
        pending_reports = Content.query.filter(
            Content.link_video != None,
            Content.link_video != '',
            Content.status == 'pending'
        ).count()
        approved_reports = Content.query.filter(
            Content.link_video != None,
            Content.link_video != '',
            Content.status == 'approved'
        ).count()
        rejected_reports = Content.query.filter(
            Content.link_video != None,
            Content.link_video != '',
            Content.status == 'rejected'
        ).count()
        
        # Count commissions
        total_commissions = Commission.query.count()
        total_commission_amount = sum(c.total_commission for c in Commission.query.all()) or 0
        
        # Count payments
        total_payments = Payment.query.count()
        pending_payments = Payment.query.filter_by(status='pending').count()
        paid_payments = Payment.query.filter_by(status='paid').count()
        
        message = (
            f"📈 **SYSTEM STATISTICS**\n\n"
            f"👥 **Users:**\n"
            f"   Total: {total_users}\n"
            f"   Active: {active_users}\n\n"
            f"📊 **Reports:**\n"
            f"   Total: {total_reports}\n"
            f"   ⏳ Pending: {pending_reports}\n"
            f"   ✅ Approved: {approved_reports}\n"
            f"   ❌ Rejected: {rejected_reports}\n\n"
            f"💰 **Commissions:**\n"
            f"   Total: {total_commissions}\n"
            f"   Amount: Rp {total_commission_amount:,.0f}\n\n"
            f"💳 **Payments:**\n"
            f"   Total: {total_payments}\n"
            f"   ⏳ Pending: {pending_payments}\n"
            f"   ✅ Paid: {paid_payments}\n"
        )
        
        await update.message.reply_text(message)

async def handle_purchase_selection(context: ContextTypes.DEFAULT_TYPE, user_id: str, tier: str, price: int, query):
    """Handle purchase selection from /beli command"""
    with flask_app.app_context():
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        if not telegram_user:
            await query.edit_message_text("❌ User tidak ditemukan.")
            return
        
        # Store payment request
        pending_payments[user_id] = {
            'type': 'purchase',
            'user_id': telegram_user.id,
            'membership_tier': tier,
            'amount': price,
            'data': {
                'full_name': telegram_user.full_name,
                'whatsapp': telegram_user.whatsapp,
                'email': telegram_user.email,
                'wallet': telegram_user.wallet,
                'bank_account': telegram_user.bank_account
            },
            'status': 'waiting_proof'
        }
        
        await query.edit_message_text(
            f"💳 **PEMBELIAN {tier.upper()} MEMBER**\n\n"
            f"Harga: Rp {price:,}\n\n"
            f"**Cara Pembayaran:**\n"
            f"1. Transfer ke rekening berikut:\n"
            f"   💰 BCA: 1234567890 (a.n. Admin)\n"
            f"   💰 DANA: 081234567890 (a.n. Admin)\n\n"
            f"2. Upload bukti pembayaran (foto/screenshot)\n"
            f"   (Kirim foto bukti transfer)\n\n"
            f"⚠️ Setelah pembayaran diverifikasi, membership akan aktif otomatis."
        )

async def handle_upgrade_confirmation(context: ContextTypes.DEFAULT_TYPE, user_id: str, query):
    """Handle upgrade confirmation"""
    with flask_app.app_context():
        telegram_user = User.query.filter_by(telegram_id=user_id).first()
        if not telegram_user:
            await query.edit_message_text("❌ User tidak ditemukan.")
            return
        
        # Store upgrade request
        pending_payments[user_id] = {
            'type': 'upgrade',
            'user_id': telegram_user.id,
            'from_tier': 'basic',
            'to_tier': 'vip',
            'membership_tier': 'vip',
            'amount': 202000,  # 299k - 97k
            'data': {
                'full_name': telegram_user.full_name,
                'whatsapp': telegram_user.whatsapp
            },
            'status': 'waiting_proof'
        }
        
        await query.edit_message_text(
            "💳 **PEMBAYARAN UPGRADE**\n\n"
            "Silakan transfer Rp 202.000 dan upload bukti pembayaran.\n\n"
            "(Kirim foto bukti transfer)"
        )

async def verify_payment(context: ContextTypes.DEFAULT_TYPE, target_user_id: str, admin_user, query=None):
    """Verify payment and activate membership"""
    with flask_app.app_context():
        if target_user_id not in pending_payments:
            if query:
                await query.edit_message_text("❌ Pembayaran tidak ditemukan.")
            else:
                await context.bot.send_message(
                    chat_id=admin_user.id,
                    text="❌ Pembayaran tidak ditemukan."
                )
            return
        
        payment_data = pending_payments[target_user_id]
        user_data = payment_data.get('data', {})
        
        try:
            # Find or create user
            telegram_user = User.query.filter_by(telegram_id=target_user_id).first()
            if not telegram_user:
                # Create user from registration data
                telegram_user = User(
                    username=f"telegram_{target_user_id}",
                    email=user_data.get('email') or f"telegram_{target_user_id}@telegram.local",
                    password_hash="telegram_user",
                    role='member',
                    full_name=user_data.get('full_name', 'User'),
                    whatsapp=user_data.get('whatsapp', ''),
                    wallet=user_data.get('wallet'),
                    bank_account=user_data.get('bank_account'),
                    telegram_id=target_user_id,
                    telegram_username=user_data.get('telegram_username')
                )
                database.session.add(telegram_user)
                database.session.flush()
            
            # TODO: Create membership record in database
            # For now, just mark as verified
            
            # Notify user
            try:
                membership_tier = payment_data['membership_tier']
                from datetime import datetime
                current_date = datetime.now().strftime('%d %B %Y')
                
                await context.bot.send_message(
                    chat_id=int(target_user_id),
                    text=(
                        f"🎉 **PEMBAYARAN DITERIMA!**\n\n"
                        f"Membership Anda sudah aktif!\n\n"
                        f"✅ **{membership_tier.upper()} Member** - Aktif\n"
                        f"📅 Aktif sejak: {current_date}\n\n"
                        f"**Fasilitas yang bisa digunakan:**\n"
                        f"{'✅ Materi AI Content Creation\n✅ Tutorial dasar sampai upload\n✅ Akses platform website\n✅ Submit report via /lapor' if membership_tier == 'basic' else '✅ Semua Basic Member\n✅ Group diskusi\n✅ Tanya jawab\n✅ Zoom meeting\n✅ Akun TikTok affiliate\n✅ Bagi hasil 55%'}\n\n"
                        f"**Perintah yang bisa digunakan:**\n"
                        f"/lapor - Lapor kinerja\n"
                        f"/komisi - Cek komisi\n"
                        f"{'/upgrade - Upgrade ke VIP (dapat 55% komisi!)' if membership_tier == 'basic' else '/akun - Cek info akun TikTok affiliate'}\n\n"
                        f"Selamat bergabung! 🎊"
                    )
                )
            except Exception as e:
                logger.error(f"Error notifying user: {e}")
            
            # Notify admin
            if query:
                await query.edit_message_text(
                    f"✅ Payment telah diverifikasi!\n\n"
                    f"User: {user_data.get('full_name', 'N/A')}\n"
                    f"Membership: {payment_data['membership_tier'].upper()} Member - Aktif\n"
                    f"Harga: Rp {payment_data['amount']:,}\n\n"
                    f"✅ User telah menjadi {payment_data['membership_tier'].upper()} Member.\n"
                    f"✅ Notifikasi telah dikirim ke user."
                )
            else:
                await context.bot.send_message(
                    chat_id=admin_user.id,
                    text=(
                        f"✅ Payment telah diverifikasi!\n\n"
                        f"User: {user_data.get('full_name', 'N/A')}\n"
                        f"Membership: {payment_data['membership_tier'].upper()} Member - Aktif"
                    )
                )
            
            # Clear pending payment
            del pending_payments[target_user_id]
            
        except Exception as e:
            logger.error(f"Error verifying payment: {e}")
            if query:
                await query.edit_message_text("❌ Error saat memverifikasi pembayaran.")
            else:
                await context.bot.send_message(
                    chat_id=admin_user.id,
                    text=f"❌ Error: {str(e)}"
                )

async def reject_payment(context: ContextTypes.DEFAULT_TYPE, target_user_id: str, admin_user, query=None, reason=""):
    """Reject payment"""
    if target_user_id not in pending_payments:
        if query:
            await query.edit_message_text("❌ Pembayaran tidak ditemukan.")
        return
    
    payment_data = pending_payments[target_user_id]
    user_data = payment_data.get('data', {})
    
    # Notify user
    try:
        await context.bot.send_message(
            chat_id=int(target_user_id),
            text=(
                f"❌ **PEMBAYARAN DITOLAK**\n\n"
                f"Payment Request\n\n"
                f"Alasan: {reason or 'Tidak disebutkan'}\n\n"
                f"Silakan upload ulang bukti pembayaran yang lebih jelas.\n\n"
                f"Gunakan /beli untuk membeli membership lagi."
            )
        )
    except Exception as e:
        logger.error(f"Error notifying user: {e}")
    
    # Notify admin
    if query:
        await query.edit_message_text(
            f"❌ Payment telah ditolak.\n\n"
            f"Alasan: {reason or 'Tidak disebutkan'}\n\n"
            f"User telah mendapat notifikasi."
        )
    
    # Clear pending payment
    del pending_payments[target_user_id]

async def pending_payments_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pending-payments command - Admin list pending payments"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text(
            "❌ Command ini hanya untuk admin/owner!"
        )
        return
    
    if not pending_payments:
        await update.message.reply_text(
            "📭 Tidak ada pembayaran yang pending."
        )
        return
    
    count = 1
    for tg_user_id, payment_data in pending_payments.items():
        if payment_data.get('status') == 'pending_verification':
            user_data = payment_data.get('data', {})
            keyboard = [
                [
                    InlineKeyboardButton("✅ Verify", callback_data=f"verify_payment_{tg_user_id}"),
                    InlineKeyboardButton("❌ Reject", callback_data=f"reject_payment_{tg_user_id}")
                ],
                [
                    InlineKeyboardButton("👁️ Lihat Bukti", callback_data=f"view_proof_{tg_user_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"{count}. {payment_data['type'].upper()} Request\n"
                f"   👤 User: {user_data.get('full_name', 'N/A')}\n"
                f"   💰 Membership: {payment_data['membership_tier'].upper()}\n"
                f"   💵 Harga: Rp {payment_data['amount']:,}\n"
                f"   📅 Status: ⏳ Pending",
                reply_markup=reply_markup
            )
            count += 1

async def verify_payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verify-payment command - Admin verify payment"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text(
            "❌ Command ini hanya untuk admin/owner!"
        )
        return
    
    # Get payment ID from command args
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Format: /verify-payment <user_telegram_id>\n\n"
            "Contoh: /verify-payment 123456789"
        )
        return
    
    target_user_id = args[0]
    await verify_payment(context, target_user_id, user, None)

async def reject_payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reject-payment command - Admin reject payment"""
    user = update.effective_user
    user_id = str(user.id)
    
    if not check_owner(user_id):
        await update.message.reply_text(
            "❌ Command ini hanya untuk admin/owner!"
        )
        return
    
    # Get payment ID and reason from command args
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "❌ Format: /reject-payment <user_telegram_id> <alasan>\n\n"
            "Contoh: /reject-payment 123456789 Bukti pembayaran tidak jelas"
        )
        return
    
    target_user_id = args[0]
    reason = ' '.join(args[1:])
    await reject_payment(context, target_user_id, user, None, reason)

async def notify_admin_new_reports(context: ContextTypes.DEFAULT_TYPE, links: list, user_obj, tanggal):
    """Notify admin about new reports"""
    with flask_app.app_context():
        # Get all owners
        owners = User.query.filter_by(role='owner').all()
        
        if not owners:
            return
        
        # Get the latest reports for these links
        reports = []
        for link in links:
            report = Content.query.filter_by(
                creator_id=user_obj.id,
                link_video=link,
                tanggal_upload=tanggal
            ).order_by(Content.created_at.desc()).first()
            if report:
                reports.append(report)
        
        if not reports:
            return
        
        # Send notification to each owner
        for owner in owners:
            if not owner.telegram_id:
                continue
            
            try:
                message = (
                    f"📊 **REPORT BARU**\n\n"
                    f"👤 User: {user_obj.full_name or user_obj.username}\n"
                    f"📹 Total Video: {len(reports)}\n"
                    f"📅 Tanggal Upload: {tanggal.strftime('%d/%m/%Y')}\n\n"
                )
                
                # Show first 3 links
                for i, report in enumerate(reports[:3], 1):
                    message += f"{i}. {report.link_video[:50]}...\n"
                
                if len(reports) > 3:
                    message += f"... dan {len(reports) - 3} video lainnya\n\n"
                
                message += (
                    f"**Quick Actions:**\n"
                    f"/pending - Lihat semua pending\n"
                    f"/approve {reports[0].id} - Approve report pertama\n"
                    f"/reject {reports[0].id} - Reject report pertama"
                )
                
                await context.bot.send_message(
                    chat_id=owner.telegram_id,
                    text=message
                )
            except Exception as e:
                logger.warning(f"Failed to notify owner {owner.id}: {e}")

# ==================== CALLBACK HANDLERS ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = query.from_user
    user_id = str(user.id)
    
    if data.startswith('approve_'):
        content_id = int(data.split('_')[1])
        await approve_content(context, content_id, user, query)
        
    elif data.startswith('reject_'):
        content_id = int(data.split('_')[1])
        await reject_content(context, content_id, user, query)
        
    elif data.startswith('detail_'):
        content_id = int(data.split('_')[1])
        await show_content_detail(context, content_id, query)
    
    elif data == 'membership_basic':
        # Handle basic membership selection
        if user_id in pending_registrations:
            reg_data = pending_registrations[user_id]
            reg_data['data']['membership_tier'] = 'basic'
            reg_data['data']['membership_price'] = 97000
            reg_data['step'] = 'waiting_payment_proof'
            
            await query.edit_message_text(
                "💳 **PEMBELIAN BASIC MEMBER**\n\n"
                "Harga: Rp 97.000\n\n"
                "**Cara Pembayaran:**\n"
                "1. Transfer ke rekening berikut:\n"
                "   💰 BCA: 1234567890 (a.n. Admin)\n"
                "   💰 DANA: 081234567890 (a.n. Admin)\n\n"
                "2. Upload bukti pembayaran (foto/screenshot)\n"
                "   (Kirim foto bukti transfer)\n\n"
                "⚠️ Setelah pembayaran diverifikasi, membership akan aktif otomatis."
            )
    
    elif data == 'membership_vip':
        # Handle VIP membership selection
        if user_id in pending_registrations:
            reg_data = pending_registrations[user_id]
            reg_data['data']['membership_tier'] = 'vip'
            reg_data['data']['membership_price'] = 299000
            reg_data['step'] = 'waiting_payment_proof'
            
            await query.edit_message_text(
                "💳 **PEMBELIAN VIP MEMBER**\n\n"
                "Harga: Rp 299.000\n\n"
                "**Cara Pembayaran:**\n"
                "1. Transfer ke rekening berikut:\n"
                "   💰 BCA: 1234567890 (a.n. Admin)\n"
                "   💰 DANA: 081234567890 (a.n. Admin)\n\n"
                "2. Upload bukti pembayaran (foto/screenshot)\n"
                "   (Kirim foto bukti transfer)\n\n"
                "⚠️ Setelah pembayaran diverifikasi, membership akan aktif otomatis."
            )
    
    elif data == 'purchase_basic':
        # Handle purchase basic from /beli command
        await handle_purchase_selection(context, user_id, 'basic', 97000, query)
    
    elif data == 'purchase_vip':
        # Handle purchase VIP from /beli command
        await handle_purchase_selection(context, user_id, 'vip', 299000, query)
    
    elif data == 'confirm_upgrade':
        # Handle upgrade confirmation
        await handle_upgrade_confirmation(context, user_id, query)
    
    elif data == 'cancel_upgrade':
        await query.edit_message_text("❌ Upgrade dibatalkan.")
    
    elif data.startswith('verify_payment_'):
        # Admin verify payment
        target_user_id = data.split('_')[2]
        await verify_payment(context, target_user_id, user, query)
    
    elif data.startswith('reject_payment_'):
        # Admin reject payment
        target_user_id = data.split('_')[2]
        await reject_payment(context, target_user_id, user, query)
    
    elif data.startswith('view_proof_'):
        # Admin view payment proof
        target_user_id = data.split('_')[2]
        if target_user_id in pending_payments:
            payment_data = pending_payments[target_user_id]
            file_id = payment_data.get('file_id')
            if file_id:
                await context.bot.send_photo(
                    chat_id=user.id,
                    photo=file_id,
                    caption=f"Bukti pembayaran dari {payment_data.get('data', {}).get('full_name', 'User')}"
                )

async def approve_content(context: ContextTypes.DEFAULT_TYPE, content_id: int, user, query=None):
    """Approve content from Telegram"""
    with flask_app.app_context():
        content = Content.query.get(content_id)
        if not content:
            await context.bot.send_message(
                chat_id=user.id,
                text="❌ Konten tidak ditemukan"
            )
            return
        
        # Check if user is owner (simple check - bisa diperbaiki dengan user management)
        # Untuk sekarang, kita anggap semua yang approve di group adalah owner
        
        content.status = 'approved'
        content.quality_score = 7.0  # Default score
        database.session.commit()
        
        # Notify creator
        creator = User.query.get(content.creator_id)
        if creator and creator.username.startswith('telegram_'):
            telegram_id = creator.username.replace('telegram_', '')
            try:
                await context.bot.send_message(
                    chat_id=telegram_id,
                    text=f"✅ **Konten Anda Disetujui!**\n\n"
                         f"Produk: {content.product.product_name}\n"
                         f"Quality Score: {content.quality_score}\n\n"
                         f"Gunakan /komisi untuk cek komisi Anda."
                )
            except:
                pass
        
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"✅ Konten ID {content_id} telah disetujui oleh {user.first_name}"
        )
        
        # Update original message if query provided
        if query:
            try:
                await context.bot.edit_message_text(
                    chat_id=GROUP_CHAT_ID,
                    message_id=query.message.message_id,
                    text=f"✅ **Konten Disetujui**\n\n"
                         f"Produk: {content.product.product_name}\n"
                         f"Member: {creator.full_name if creator else 'N/A'}\n"
                         f"Approved by: {user.first_name}"
                )
            except:
                pass

async def reject_content(context: ContextTypes.DEFAULT_TYPE, content_id: int, user, query=None):
    """Reject content from Telegram"""
    with flask_app.app_context():
        content = Content.query.get(content_id)
        if not content:
            return
        
        content.status = 'rejected'
        database.session.commit()
        
        # Notify creator
        creator = User.query.get(content.creator_id)
        if creator and creator.username.startswith('telegram_'):
            telegram_id = creator.username.replace('telegram_', '')
            try:
                await context.bot.send_message(
                    chat_id=telegram_id,
                    text=f"❌ **Konten Anda Ditolak**\n\n"
                         f"Produk: {content.product.product_name}\n\n"
                         f"Silakan submit konten baru dengan /submit"
                )
            except:
                pass
        
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"❌ Konten ID {content_id} telah ditolak oleh {user.first_name}"
        )
        
        # Update original message if query provided
        if query:
            try:
                await context.bot.edit_message_text(
                    chat_id=GROUP_CHAT_ID,
                    message_id=query.message.message_id,
                    text=f"❌ **Konten Ditolak**\n\n"
                         f"Produk: {content.product.product_name}\n"
                         f"Member: {creator.full_name if creator else 'N/A'}\n"
                         f"Rejected by: {user.first_name}"
                )
            except:
                pass

async def show_content_detail(context: ContextTypes.DEFAULT_TYPE, content_id: int, query):
    """Show content detail"""
    with flask_app.app_context():
        content = Content.query.get(content_id)
        if not content:
            await query.answer("Konten tidak ditemukan", show_alert=True)
            return
        
        creator = User.query.get(content.creator_id)
        product = Product.query.get(content.product_id)
        
        detail_text = (
            f"📋 **Detail Konten**\n\n"
            f"🆔 ID: {content.id}\n"
            f"👤 Creator: {creator.full_name if creator else 'N/A'}\n"
            f"📦 Produk: {product.product_name if product else 'N/A'}\n"
            f"🔗 Link: {content.media_url}\n"
            f"📱 Platform: {content.platform}\n"
            f"⭐ Quality Score: {content.quality_score}\n"
            f"📊 Status: {content.status}\n"
            f"📅 Created: {content.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        
        await query.edit_message_text(detail_text)

# ==================== BOT SETUP ====================

def setup_bot(app_instance, db_instance):
    """Setup and return bot application"""
    init_bot(app_instance, db_instance)
    
    # Aggressive patch for Python 3.13 timezone issue
    # Patch get_localzone BEFORE JobQueue is created
    import tzlocal
    original_get_localzone = tzlocal.get_localzone
    
    # Force return pytz.UTC
    def get_localzone_patched():
        return pytz.UTC
    
    # Patch at multiple levels
    tzlocal.get_localzone = get_localzone_patched
    if hasattr(tzlocal, '__all__'):
        for name in tzlocal.__all__:
            if name == 'get_localzone':
                setattr(tzlocal, name, get_localzone_patched)
    
    # Also patch apscheduler.util.astimezone
    try:
        from apscheduler import util as apscheduler_util
        original_astimezone = apscheduler_util.astimezone
        
        def patched_astimezone(obj):
            if obj is None:
                return pytz.UTC
            if hasattr(obj, 'zone'):  # pytz timezone
                return obj
            # If zoneinfo, return pytz.UTC
            if hasattr(obj, 'key'):  # zoneinfo timezone
                return pytz.UTC
            try:
                return original_astimezone(obj)
            except:
                return pytz.UTC
        
        apscheduler_util.astimezone = patched_astimezone
    except:
        pass
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add error handler for Conflict and other errors
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        error = context.error
        
        # Handle Conflict error (multiple bot instances)
        if isinstance(error, Conflict):
            logger.warning("⚠️ Conflict detected: Multiple bot instances running!")
            logger.warning("   Attempting to clear webhook and stop polling...")
            try:
                # Stop current polling
                if hasattr(context, 'bot') and context.bot:
                    await context.bot.delete_webhook(drop_pending_updates=True)
                    logger.info("✅ Webhook cleared")
                logger.error("❌ Please stop ALL Python instances running app.py and restart!")
            except Exception as e:
                logger.error(f"❌ Failed to clear webhook: {e}")
        else:
            logger.error(f"Exception while handling an update: {error}", exc_info=error)
    
    application.add_error_handler(error_handler)
    
    # Add handlers
    # USER COMMANDS
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("daftar", register_user))
    application.add_handler(CommandHandler("lapor", report_kinerja))
    application.add_handler(CommandHandler("submit", submit_content))  # Legacy command
    application.add_handler(CommandHandler("komisi", check_commission))
    application.add_handler(CommandHandler("pembayaran", check_payment))
    
    # ADMIN COMMANDS (role check di dalam function)
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("pending", pending_reports))
    application.add_handler(CommandHandler("pending-payments", pending_payments_command))
    application.add_handler(CommandHandler("verify-payment", verify_payment_command))
    application.add_handler(CommandHandler("reject-payment", reject_payment_command))
    application.add_handler(CommandHandler("approve", approve_report_command))
    application.add_handler(CommandHandler("reject", reject_report_command))
    application.add_handler(CommandHandler("reports", list_reports))
    application.add_handler(CommandHandler("users", list_users))
    application.add_handler(CommandHandler("stats", system_stats))
    
    # Callback and message handlers
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # Handle payment proof photos
    
    return application

# Global variables
flask_app = None
database = None


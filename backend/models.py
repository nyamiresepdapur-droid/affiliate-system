from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone

db = SQLAlchemy()

def utcnow():
    """Get current UTC datetime (replacement for deprecated datetime.utcnow())"""
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.Index('idx_user_telegram_id', 'telegram_id'),
        db.Index('idx_user_role', 'role'),
        db.Index('idx_user_username', 'username'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # Optional
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # owner, manager, member
    full_name = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))  # Nomor WhatsApp
    tiktok_akun = db.Column(db.String(100))  # Nama akun TikTok
    wallet = db.Column(db.String(100))  # Wallet (DANA, OVO, GoPay, dll)
    bank_account = db.Column(db.String(100))  # Bank & No Rekening
    telegram_id = db.Column(db.String(50))  # Telegram User ID
    telegram_username = db.Column(db.String(100))  # Telegram Username (@username)
    created_at = db.Column(db.DateTime, default=utcnow)
    
    # Relationships
    created_content = db.relationship('Content', backref='creator', lazy=True)
    managed_teams = db.relationship('Team', backref='manager', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        db.Index('idx_product_status', 'status'),
        db.Index('idx_product_category', 'category'),
        db.Index('idx_product_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)  # Nama Produk
    category = db.Column(db.String(100), nullable=False)  # Kategori TikTok
    product_link = db.Column(db.String(500), nullable=False)  # Link Produk
    product_price = db.Column(db.Float, nullable=False)  # Harga Produk
    commission_percent = db.Column(db.Float, nullable=False)  # Komisi dalam persentase
    regular_commission = db.Column(db.Float, nullable=False)  # komisi_reguler
    gmv_max_commission = db.Column(db.Float, nullable=False)  # komisi_gmv
    target_gmv = db.Column(db.Float, default=0)  # target_gmv
    item_terjual = db.Column(db.Integer, default=0)  # Jumlah item terjual
    status = db.Column(db.String(20), default='active')  # active, inactive
    sheet_order = db.Column(db.Integer, nullable=True)  # Urutan di Google Sheets (row number)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)  # Untuk sync Google Sheets
    
    # Relationships
    content = db.relationship('Content', backref='product', lazy=True)
    commissions = db.relationship('Commission', backref='product', lazy=True)

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    target_commission = db.Column(db.Float, default=0)
    manager_bonus_percent = db.Column(db.Float, default=5)  # 5-10%
    created_at = db.Column(db.DateTime, default=utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')
    manager_bonuses = db.relationship('ManagerBonus', backref='team', lazy=True)

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=utcnow)
    
    __table_args__ = (db.UniqueConstraint('team_id', 'user_id', name='unique_team_member'),)

class Content(db.Model):
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)  # Optional (bisa link manual)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    link_video = db.Column(db.String(500))  # Link video TikTok
    tanggal_upload = db.Column(db.Date)  # Tanggal upload video
    tiktok_akun = db.Column(db.String(100))  # Nama akun TikTok
    media_url = db.Column(db.String(500))  # Legacy field (backward compatibility)
    platform = db.Column(db.String(50), default='tiktok')  # tiktok, shopee
    quality_score = db.Column(db.Float, default=0)  # 0-10
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=utcnow)
    
    # Relationships
    commissions = db.relationship('Commission', backref='content', lazy=True)

class Commission(db.Model):
    __tablename__ = 'commissions'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_commission = db.Column(db.Float, nullable=False)
    owner_share = db.Column(db.Float, nullable=False)  # 40%
    team_share = db.Column(db.Float, nullable=False)  # 50%
    manager_bonus = db.Column(db.Float, default=0)  # 5-10% dari total
    status = db.Column(db.String(20), default='pending')  # pending, approved, paid
    created_at = db.Column(db.DateTime, default=utcnow)
    
    # Relationships
    manager_bonuses = db.relationship('ManagerBonus', backref='commission', lazy=True)

class ManagerBonus(db.Model):
    __tablename__ = 'manager_bonuses'
    
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    commission_id = db.Column(db.Integer, db.ForeignKey('commissions.id'), nullable=False)
    bonus_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, paid
    created_at = db.Column(db.DateTime, default=utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(50))  # commission, manager_bonus, quality_bonus
    payment_method = db.Column(db.String(50))  # wallet, bank
    payment_detail = db.Column(db.String(200))  # Detail wallet/bank
    period = db.Column(db.String(20))  # Format: '2024-01'
    status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    created_at = db.Column(db.DateTime, default=utcnow)

class DailyCommission(db.Model):
    """Mencatat komisi harian per member per tanggal"""
    __tablename__ = 'daily_commissions'
    __table_args__ = (
        db.Index('idx_daily_comm_user_date', 'user_id', 'date'),
        db.Index('idx_daily_comm_date', 'date'),
        db.UniqueConstraint('user_id', 'date', name='unique_user_date_commission'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Tanggal komisi (YYYY-MM-DD)
    commission_amount = db.Column(db.Float, nullable=False)  # Jumlah komisi harian
    notes = db.Column(db.Text)  # Catatan admin (opsional)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin yang update
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    
    # Relationships
    user_rel = db.relationship('User', foreign_keys=[user_id], backref='daily_commissions')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_daily_commissions')

class VideoStatistic(db.Model):
    """Mencatat statistik video per member dan per akun TikTok"""
    __tablename__ = 'video_statistics'
    __table_args__ = (
        db.Index('idx_video_stat_user_akun_date', 'user_id', 'tiktok_akun', 'date'),
        db.Index('idx_video_stat_date', 'date'),
        db.UniqueConstraint('user_id', 'tiktok_akun', 'date', name='unique_user_akun_date_video'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tiktok_akun = db.Column(db.String(100), nullable=False)  # Nama akun TikTok
    date = db.Column(db.Date, nullable=False)  # Tanggal upload (YYYY-MM-DD)
    video_count = db.Column(db.Integer, default=0, nullable=False)  # Jumlah video di tanggal tersebut
    total_views = db.Column(db.Integer, default=0)  # Total views (opsional, untuk future)
    total_likes = db.Column(db.Integer, default=0)  # Total likes (opsional, untuk future)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin yang update
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    
    # Relationships
    user_rel = db.relationship('User', foreign_keys=[user_id], backref='video_statistics')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_video_statistics')

class MemberDailySummary(db.Model):
    """Summary harian per member (denormalized untuk query cepat)"""
    __tablename__ = 'member_daily_summary'
    __table_args__ = (
        db.Index('idx_summary_user_date', 'user_id', 'date'),
        db.Index('idx_summary_date', 'date'),
        db.UniqueConstraint('user_id', 'date', name='unique_user_date_summary'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Tanggal (YYYY-MM-DD)
    total_commission = db.Column(db.Float, default=0, nullable=False)  # Total komisi hari ini
    total_videos = db.Column(db.Integer, default=0, nullable=False)  # Total video hari ini (semua akun)
    total_akun = db.Column(db.Integer, default=0, nullable=False)  # Jumlah akun yang upload hari ini
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    
    # Relationships
    user_rel = db.relationship('User', foreign_keys=[user_id], backref='daily_summaries')

class Notification(db.Model):
    """Notifications untuk user"""
    __tablename__ = 'notifications'
    __table_args__ = (
        db.Index('idx_notifications_user_id', 'user_id'),
        db.Index('idx_notifications_is_read', 'is_read'),
        db.Index('idx_notifications_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'report_approved', 'report_rejected', 'commission_added', 'milestone', 'reminder'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    data = db.Column(db.Text)  # JSON string untuk additional data
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')


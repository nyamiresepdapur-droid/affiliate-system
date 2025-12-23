-- Database Migration Script for Supabase PostgreSQL
-- Run this in Supabase SQL Editor

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    full_name VARCHAR(100),
    whatsapp VARCHAR(20),
    tiktok_akun VARCHAR(100),
    wallet VARCHAR(100),
    bank_account VARCHAR(100),
    telegram_id VARCHAR(50),
    telegram_username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    product_link TEXT,
    product_price DECIMAL(10, 2),
    description TEXT,
    item_terjual INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teams table
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manager_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Team Members table
CREATE TABLE IF NOT EXISTS team_members (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, user_id)
);

-- Content table
CREATE TABLE IF NOT EXISTS content (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    creator_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    description TEXT,
    media_url TEXT,
    link_video TEXT,
    platform VARCHAR(50) DEFAULT 'tiktok',
    quality_score DECIMAL(3, 1) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    tanggal_upload DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Commissions table
CREATE TABLE IF NOT EXISTS commissions (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    user_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL,
    total_commission DECIMAL(10, 2),
    team_share DECIMAL(10, 2),
    manager_share DECIMAL(10, 2),
    owner_share DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    period VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Manager Bonus table
CREATE TABLE IF NOT EXISTS manager_bonus (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL,
    period VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily Commission table
CREATE TABLE IF NOT EXISTS daily_commissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    date DATE NOT NULL,
    total_commission DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);

-- Video Statistics table
CREATE TABLE IF NOT EXISTS video_statistics (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Member Daily Summary table
CREATE TABLE IF NOT EXISTS member_daily_summary (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    date DATE NOT NULL,
    total_videos INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    total_likes INTEGER DEFAULT 0,
    total_commission DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    data JSONB,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_user_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_content_creator ON content(creator_id);
CREATE INDEX IF NOT EXISTS idx_content_status ON content(status);
CREATE INDEX IF NOT EXISTS idx_commission_user ON commissions(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_read ON notifications(is_read);

-- Create default owner (password: admin123)
-- Note: Update password hash with actual hash from your system
INSERT INTO users (username, email, password_hash, role, full_name)
SELECT 'owner', 'owner@affiliate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'owner', 'Owner'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'owner');


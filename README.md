# Affiliate Management System

Sistem manajemen affiliate dengan Telegram bot integration, web dashboard, dan automated commission tracking.

## 🚀 Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL (Supabase)
- **Deployment:**
  - Backend: Railway
  - Frontend: Vercel
  - Database: Supabase

## 📁 Structure

```
affiliate-system/
├── backend/           # Flask API
│   ├── app.py       # Main application
│   ├── models.py    # Database models
│   ├── telegram_bot.py
│   └── requirements.txt
├── frontend/        # Web dashboard
│   ├── index.html
│   ├── landing.html
│   └── register.html
└── nixpacks.toml    # Railway configuration
```

## 🔧 Setup

### Backend (Railway)
1. Set environment variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `FLASK_ENV=production`
   - `TELEGRAM_TOKEN`
   - `FRONTEND_URL`

### Frontend (Vercel)
1. Set environment variable:
   - `API_URL`

### Database (Supabase)
1. Run migration: `backend/migrations/create_tables.sql`

## 📝 Features

- User registration & authentication
- Product management
- Content reporting
- Commission tracking
- Telegram bot integration
- Membership tiers (Basic/VIP)

## 🔗 Links

- Backend: `affiliate-system-production.up.railway.app`
- Frontend: `https://affiliate-system-rho.vercel.app`

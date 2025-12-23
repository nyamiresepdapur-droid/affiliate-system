# 🚀 DEPLOYMENT GUIDE - VERCEL + RAILWAY + SUPABASE

**Tanggal:** 20 Desember 2025  
**Platform:** Vercel (Frontend) + Railway (Backend) + Supabase (Database)

---

## 📋 OVERVIEW

**Arsitektur:**
```
Frontend (Vercel) → Backend (Railway) → Database (Supabase)
```

**Total Cost:** $0-10/tahun (hanya domain jika pakai .com)

---

## 🎯 STEP 1: DEPLOY FRONTEND KE VERCEL

### **1.1. Buat Akun Vercel**

1. **Buka:** https://vercel.com
2. **Klik:** "Sign Up"
3. **Pilih:** "Continue with GitHub"
4. **Authorize** Vercel untuk akses GitHub

---

### **1.2. Import Repository**

1. **Setelah login, klik:** "Add New..." → "Project"
2. **Pilih repository:** `nyamiresepdapur-droid/affiliate-system`
3. **Configure Project:**
   - **Framework Preset:** Other
   - **Root Directory:** `frontend`
   - **Build Command:** (kosongkan - static site)
   - **Output Directory:** `frontend`
   - **Install Command:** (kosongkan)
4. **Klik:** "Deploy"

---

### **1.3. Setup Environment Variables (Opsional)**

**Jika perlu environment variables:**
1. **Project Settings** → **Environment Variables**
2. **Add:**
   - `API_URL` = `https://your-backend.railway.app/api`
   - (akan di-update setelah backend deploy)

---

### **1.4. Get Frontend URL**

**Setelah deploy selesai:**
- Vercel akan kasih URL: `https://affiliate-system-xxx.vercel.app`
- **Simpan URL ini** untuk update backend CORS

---

## 🎯 STEP 2: SETUP DATABASE DI SUPABASE

### **2.1. Buat Akun Supabase**

1. **Buka:** https://supabase.com
2. **Klik:** "Start your project"
3. **Sign up** dengan GitHub
4. **Create Organization** (jika belum ada)

---

### **2.2. Create New Project**

1. **Klik:** "New Project"
2. **Isi:**
   - **Name:** `affiliate-system`
   - **Database Password:** (buat password kuat, simpan!)
   - **Region:** Pilih terdekat (Singapore recommended)
   - **Pricing Plan:** Free
3. **Klik:** "Create new project"
4. **Tunggu** sampai project ready (2-3 menit)

---

### **2.3. Get Database Connection String**

1. **Project Settings** → **Database**
2. **Scroll ke:** "Connection string"
3. **Pilih:** "URI"
4. **Copy connection string** (contoh: `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`)
5. **Simpan** connection string ini

---

### **2.4. Run Database Migration**

**Option 1: Via Supabase SQL Editor**

1. **Buka:** SQL Editor di Supabase dashboard
2. **Klik:** "New query"
3. **Copy migration script** (lihat `backend/migrations/` atau buat dari models)
4. **Paste** dan **Run**

**Option 2: Via Python Script**

1. **Update `DATABASE_URL`** di local `.env`
2. **Run migration:**
   ```bash
   cd backend
   python migrate_database.py
   ```

---

## 🎯 STEP 3: DEPLOY BACKEND KE RAILWAY

### **3.1. Buat Akun Railway**

1. **Buka:** https://railway.app
2. **Klik:** "Start a New Project"
3. **Sign up** dengan GitHub
4. **Authorize** Railway untuk akses GitHub

---

### **3.2. Create New Project**

1. **Klik:** "New Project"
2. **Pilih:** "Deploy from GitHub repo"
3. **Pilih repository:** `nyamiresepdapur-droid/affiliate-system`
4. **Railway akan auto-detect** Python project

---

### **3.3. Configure Service**

1. **Klik service** yang sudah dibuat
2. **Settings** → **Root Directory:** `backend`
3. **Settings** → **Start Command:** `python app.py`
4. **Settings** → **Build Command:** (kosongkan atau `pip install -r requirements.txt`)

---

### **3.4. Setup Environment Variables**

**Klik:** "Variables" tab, tambahkan:

```env
# Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres

# Flask
SECRET_KEY=your-secret-key-change-this-to-random-string
JWT_SECRET_KEY=your-jwt-secret-key-change-this-to-random-string
FLASK_ENV=production

# Telegram Bot
TELEGRAM_TOKEN=your-telegram-bot-token
GROUP_CHAT_ID=your-group-chat-id
CHANNEL_CHAT_ID=your-channel-chat-id

# CORS (Frontend URL dari Vercel)
FRONTEND_URL=https://your-app.vercel.app
```

**Generate secrets:**
```bash
# Di local, jalankan:
python -c "import secrets; print(secrets.token_hex(32))"
# Copy hasil untuk SECRET_KEY dan JWT_SECRET_KEY
```

---

### **3.5. Update Backend Code untuk Production**

**File: `backend/app.py`** - Update database URL:

```python
# Ganti:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///affiliate_system.db'

# Dengan:
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///affiliate_system.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

**Update CORS:**
```python
# Ganti:
CORS(app)

# Dengan:
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
CORS(app, origins=[FRONTEND_URL, 'https://your-app.vercel.app'])
```

---

### **3.6. Deploy**

1. **Railway akan auto-deploy** setelah push ke GitHub
2. **Atau klik:** "Deploy" manual
3. **Tunggu** sampai deploy selesai
4. **Get URL:** Railway akan kasih URL (contoh: `https://affiliate-system-production.up.railway.app`)

---

## 🎯 STEP 4: UPDATE CONFIGURATION

### **4.1. Update Frontend API URL**

**File: `frontend/js/app.js` dan `frontend/js/register.js`:**

```javascript
// Ganti:
const API_URL = 'http://localhost:5000/api';

// Dengan:
const API_URL = 'https://your-backend.railway.app/api';
```

**Commit & push:**
```bash
git add frontend/js/app.js frontend/js/register.js
git commit -m "Update API URL for production"
git push
```

**Vercel akan auto-redeploy**

---

### **4.2. Update Backend CORS**

**File: `backend/app.py`:**

```python
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
CORS(app, origins=[
    FRONTEND_URL,
    'https://your-app.vercel.app',
    'https://affiliate-system-xxx.vercel.app'
])
```

**Update Railway environment variable:**
- `FRONTEND_URL` = `https://your-app.vercel.app`

---

## 🎯 STEP 5: TEST PRODUCTION

### **5.1. Test Frontend**

1. **Buka:** `https://your-app.vercel.app`
2. **Cek:** Landing page load
3. **Cek:** Register page load
4. **Test:** Submit registration

---

### **5.2. Test Backend**

1. **Buka:** `https://your-backend.railway.app/api/health` (jika ada)
2. **Test API:** Via Postman atau browser console
3. **Cek logs:** Railway dashboard → Logs

---

### **5.3. Test Database**

1. **Buka:** Supabase dashboard
2. **SQL Editor** → Run query:
   ```sql
   SELECT * FROM users LIMIT 5;
   ```
3. **Cek:** Data sudah masuk

---

## 🔧 TROUBLESHOOTING

### **Problem: Frontend tidak load**
- Cek Vercel deployment status
- Cek build logs
- Cek API_URL sudah benar

### **Problem: Backend error**
- Cek Railway logs
- Cek environment variables
- Cek database connection

### **Problem: Database connection failed**
- Cek DATABASE_URL di Railway
- Cek password sudah benar
- Cek Supabase project status

### **Problem: CORS error**
- Cek FRONTEND_URL di Railway
- Cek CORS origins di backend
- Cek frontend URL sudah benar

---

## 📋 CHECKLIST DEPLOYMENT

### **Vercel (Frontend):**
- [ ] Akun Vercel sudah dibuat
- [ ] Repository sudah di-import
- [ ] Root directory: `frontend`
- [ ] Deploy berhasil
- [ ] URL sudah didapat

### **Supabase (Database):**
- [ ] Akun Supabase sudah dibuat
- [ ] Project sudah dibuat
- [ ] Database password sudah disimpan
- [ ] Connection string sudah didapat
- [ ] Migration sudah di-run

### **Railway (Backend):**
- [ ] Akun Railway sudah dibuat
- [ ] Project sudah dibuat
- [ ] Root directory: `backend`
- [ ] Environment variables sudah di-set
- [ ] Deploy berhasil
- [ ] URL sudah didapat

### **Configuration:**
- [ ] Frontend API_URL sudah di-update
- [ ] Backend CORS sudah di-update
- [ ] DATABASE_URL sudah di-set di Railway
- [ ] Semua secrets sudah di-set

### **Testing:**
- [ ] Frontend bisa diakses
- [ ] Backend API bisa diakses
- [ ] Database connection berhasil
- [ ] Register flow berhasil
- [ ] File upload berhasil

---

## 🎯 QUICK REFERENCE

**Vercel:**
- URL: https://vercel.com
- Deploy: Auto dari GitHub
- Cost: Free

**Railway:**
- URL: https://railway.app
- Deploy: Auto dari GitHub
- Cost: Free tier ($5 credit/month)

**Supabase:**
- URL: https://supabase.com
- Database: PostgreSQL
- Cost: Free (500MB)

---

**Ready to deploy! 🚀**


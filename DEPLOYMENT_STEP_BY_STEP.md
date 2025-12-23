# 🚀 DEPLOYMENT STEP-BY-STEP (VERCEL + RAILWAY + SUPABASE)

**Panduan lengkap untuk deploy ke production**

---

## 📋 PERSIAPAN

**Yang dibutuhkan:**
- ✅ GitHub repository sudah ready
- ✅ Code sudah di-push ke GitHub
- ✅ Akun GitHub (sudah punya)

---

## 🎯 STEP 1: DEPLOY FRONTEND KE VERCEL (10 MENIT)

### **1.1. Buat Akun Vercel**

1. **Buka:** https://vercel.com
2. **Klik:** "Sign Up"
3. **Pilih:** "Continue with GitHub"
4. **Authorize** Vercel untuk akses GitHub
5. **Selesai!** Akun sudah dibuat

---

### **1.2. Import Repository**

1. **Setelah login, klik:** "Add New..." → "Project"
2. **Pilih repository:** `nyamiresepdapur-droid/affiliate-system`
3. **Jika tidak muncul, klik:** "Import Git Repository"
4. **Paste URL:** `https://github.com/nyamiresepdapur-droid/affiliate-system`
5. **Klik:** "Import"

---

### **1.3. Configure Project**

**Isi form:**

1. **Project Name:** `affiliate-system` (atau sesuai keinginan)
2. **Framework Preset:** Other (atau pilih "Other")
3. **Root Directory:** 
   - Klik "Edit" → Pilih `frontend`
4. **Build Command:** (kosongkan - static site)
5. **Output Directory:** `frontend`
6. **Install Command:** (kosongkan)

**Environment Variables (opsional, bisa diisi nanti):**
- `API_URL` = (akan di-update setelah backend deploy)

7. **Klik:** "Deploy"

---

### **1.4. Tunggu Deploy**

1. **Vercel akan:**
   - Clone repository
   - Build project
   - Deploy ke CDN
2. **Tunggu** sampai status "Ready" (1-2 menit)
3. **Setelah selesai, dapat URL:** `https://affiliate-system-xxx.vercel.app`
4. **Simpan URL ini!** (untuk update backend CORS)

---

### **1.5. Test Frontend**

1. **Buka URL** yang diberikan Vercel
2. **Cek:** Landing page load
3. **Cek:** Register page bisa diakses
4. **Jika error, cek:** Build logs di Vercel dashboard

---

## 🎯 STEP 2: SETUP DATABASE DI SUPABASE (15 MENIT)

### **2.1. Buat Akun Supabase**

1. **Buka:** https://supabase.com
2. **Klik:** "Start your project"
3. **Sign up** dengan GitHub
4. **Create Organization:**
   - Nama: `Affiliate System` (atau sesuai)
   - Klik "Create organization"

---

### **2.2. Create New Project**

1. **Klik:** "New Project"
2. **Isi form:**
   - **Name:** `affiliate-system`
   - **Database Password:** 
     - Buat password kuat (min 12 karakter)
     - **⚠️ SIMPAN PASSWORD INI!** (tidak bisa dilihat lagi)
     - Contoh: `MySecurePass123!@#`
   - **Region:** 
     - Pilih terdekat (Singapore recommended untuk Indonesia)
   - **Pricing Plan:** Free
3. **Klik:** "Create new project"
4. **Tunggu** sampai project ready (2-3 menit)

---

### **2.3. Get Database Connection String**

1. **Project Settings** → **Database**
2. **Scroll ke:** "Connection string"
3. **Pilih tab:** "URI"
4. **Copy connection string:**
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
5. **Ganti `[YOUR-PASSWORD]`** dengan password yang dibuat tadi
6. **Simpan** connection string lengkap ini

**Contoh:**
```
postgresql://postgres:MySecurePass123!@#@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

### **2.4. Run Database Migration**

**Option 1: Via Supabase SQL Editor (Recommended)**

1. **Buka:** SQL Editor di Supabase dashboard
2. **Klik:** "New query"
3. **Copy script berikut:**

```sql
-- Create tables from models.py
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
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

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_user_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_user_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_username ON users(username);

-- Create default owner
INSERT INTO users (username, email, password_hash, role, full_name)
SELECT 'owner', 'owner@affiliate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'owner', 'Owner'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'owner');
```

4. **Paste** di SQL Editor
5. **Klik:** "Run" atau tekan Ctrl+Enter
6. **Cek:** Query berhasil (harus muncul "Success. No rows returned")

**Option 2: Via Python Script (Jika punya akses local)**

1. **Update `.env`** dengan DATABASE_URL dari Supabase
2. **Run:**
   ```bash
   cd backend
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

---

## 🎯 STEP 3: DEPLOY BACKEND KE RAILWAY (20 MENIT)

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
5. **Klik:** "Deploy Now"

---

### **3.3. Configure Service**

1. **Klik service** yang sudah dibuat
2. **Settings** tab:
   - **Root Directory:** `backend`
   - **Start Command:** `python app.py`
   - **Build Command:** `pip install -r requirements.txt`

---

### **3.4. Setup Environment Variables**

**Klik:** "Variables" tab

**Generate secrets dulu (di local terminal):**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

**Tambahkan variables satu per satu:**

1. **DATABASE_URL:**
   - Key: `DATABASE_URL`
   - Value: Connection string dari Supabase (yang sudah di-save tadi)

2. **SECRET_KEY:**
   - Key: `SECRET_KEY`
   - Value: (hasil dari command di atas)

3. **JWT_SECRET_KEY:**
   - Key: `JWT_SECRET_KEY`
   - Value: (hasil dari command di atas)

4. **FLASK_ENV:**
   - Key: `FLASK_ENV`
   - Value: `production`

5. **TELEGRAM_TOKEN:**
   - Key: `TELEGRAM_TOKEN`
   - Value: Token bot Telegram Anda

6. **GROUP_CHAT_ID:**
   - Key: `GROUP_CHAT_ID`
   - Value: ID group Telegram (jika ada)

7. **CHANNEL_CHAT_ID:**
   - Key: `CHANNEL_CHAT_ID`
   - Value: ID channel Telegram (jika ada)

8. **FRONTEND_URL:**
   - Key: `FRONTEND_URL`
   - Value: URL dari Vercel (contoh: `https://affiliate-system-xxx.vercel.app`)

**Setelah semua variables di-set, Railway akan auto-redeploy**

---

### **3.5. Get Backend URL**

1. **Setelah deploy selesai, klik:** "Settings" → "Generate Domain"
2. **Atau Railway akan kasih URL otomatis:** `https://affiliate-system-production.up.railway.app`
3. **Simpan URL ini!** (untuk update frontend API_URL)

---

### **3.6. Test Backend**

1. **Buka:** `https://your-backend.railway.app/api/health` (jika ada endpoint)
2. **Atau test via Postman:**
   - `GET https://your-backend.railway.app/api/users` (harus error 401 - normal, butuh auth)
3. **Cek logs:** Railway dashboard → Logs tab

---

## 🎯 STEP 4: UPDATE CONFIGURATION

### **4.1. Update Frontend API URL**

**File: `frontend/js/app.js` dan `frontend/js/register.js`:**

**Option 1: Via Vercel Environment Variable (Recommended)**

1. **Vercel Dashboard** → Project → Settings → Environment Variables
2. **Add:**
   - Key: `API_URL`
   - Value: `https://your-backend.railway.app/api`
   - Environment: Production, Preview, Development
3. **Redeploy** (Vercel akan auto-redeploy)

**Option 2: Update Code Langsung**

1. **Edit file:** `frontend/js/app.js`
   ```javascript
   const API_URL = 'https://your-backend.railway.app/api';
   ```

2. **Edit file:** `frontend/js/register.js`
   ```javascript
   const API_URL = 'https://your-backend.railway.app/api';
   ```

3. **Commit & push:**
   ```bash
   git add frontend/js/app.js frontend/js/register.js
   git commit -m "Update API URL for production"
   git push
   ```

4. **Vercel akan auto-redeploy**

---

### **4.2. Update Backend CORS**

**File sudah di-update, tapi pastikan FRONTEND_URL di Railway sudah benar:**

1. **Railway Dashboard** → Variables
2. **Cek:** `FRONTEND_URL` sudah di-set dengan URL Vercel
3. **Jika belum, update** dan Railway akan auto-redeploy

---

## 🎯 STEP 5: TEST PRODUCTION

### **5.1. Test Frontend**

1. **Buka:** URL Vercel Anda
2. **Test:**
   - ✅ Landing page load
   - ✅ Register page bisa diakses
   - ✅ Form bisa diisi
   - ✅ Submit registration

---

### **5.2. Test Backend**

1. **Test registration:**
   - Buka register page
   - Isi form
   - Submit
   - Cek response

2. **Cek logs:**
   - Railway → Logs tab
   - Cek apakah ada error

---

### **5.3. Test Database**

1. **Buka:** Supabase dashboard
2. **SQL Editor** → Run:
   ```sql
   SELECT * FROM users ORDER BY created_at DESC LIMIT 5;
   ```
3. **Cek:** Data user sudah masuk

---

## 📋 CHECKLIST FINAL

### **Vercel:**
- [ ] Akun sudah dibuat
- [ ] Repository sudah di-import
- [ ] Root directory: `frontend`
- [ ] Deploy berhasil
- [ ] URL sudah didapat
- [ ] API_URL environment variable sudah di-set (opsional)

### **Supabase:**
- [ ] Akun sudah dibuat
- [ ] Project sudah dibuat
- [ ] Database password sudah disimpan
- [ ] Connection string sudah didapat
- [ ] Migration sudah di-run
- [ ] Tables sudah dibuat

### **Railway:**
- [ ] Akun sudah dibuat
- [ ] Project sudah dibuat
- [ ] Root directory: `backend`
- [ ] Environment variables sudah di-set:
  - [ ] DATABASE_URL
  - [ ] SECRET_KEY
  - [ ] JWT_SECRET_KEY
  - [ ] FLASK_ENV
  - [ ] TELEGRAM_TOKEN
  - [ ] FRONTEND_URL
- [ ] Deploy berhasil
- [ ] URL sudah didapat

### **Configuration:**
- [ ] Frontend API_URL sudah di-update
- [ ] Backend CORS sudah di-update
- [ ] Semua links sudah benar

### **Testing:**
- [ ] Frontend bisa diakses
- [ ] Backend API bisa diakses
- [ ] Database connection berhasil
- [ ] Register flow berhasil

---

## 🎯 QUICK COMMANDS

**Generate secrets:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Test database connection:**
```bash
# Di local, update .env dengan DATABASE_URL dari Supabase
cd backend
python -c "from app import app, db; app.app_context().push(); print('Connected!')"
```

---

## 🚨 TROUBLESHOOTING

### **Vercel: Build Failed**
- Cek build logs
- Pastikan root directory benar: `frontend`
- Pastikan tidak ada syntax error

### **Railway: Deploy Failed**
- Cek logs di Railway dashboard
- Pastikan requirements.txt ada
- Pastikan start command benar: `python app.py`

### **Database: Connection Failed**
- Cek DATABASE_URL sudah benar
- Cek password sudah benar
- Cek Supabase project status (harus "Active")

### **CORS Error**
- Cek FRONTEND_URL di Railway sudah benar
- Cek CORS origins di backend code
- Cek frontend URL sudah benar

---

**Ready to deploy! Ikuti step-by-step di atas 🚀**


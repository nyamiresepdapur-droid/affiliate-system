# 🛠️ IMPLEMENTATION GUIDE - LOW BUDGET WEBSITE

**Tanggal:** 20 Desember 2025  
**Fokus:** Step-by-step implementation dengan budget minimal

---

## 🎯 OVERVIEW

**Tujuan:** Build website untuk manage tim affiliate dengan:
- ✅ Budget minimal ($0-10/tahun)
- ✅ Hosting gratis
- ✅ Database gratis
- ✅ Fast deployment

---

## 📋 STEP 1: PREPARE CODE

### **1.1. Update Frontend Structure**

**Buat folder structure:**
```
frontend/
├── index.html (Landing page)
├── login.html (Login page)
├── register.html (Register page)
├── dashboard.html (User dashboard)
├── admin.html (Admin dashboard)
├── css/
│   ├── style.css (Main styles)
│   └── landing.css (Landing page styles)
└── js/
    ├── app.js (Main app logic)
    ├── auth.js (Authentication)
    └── admin.js (Admin functions)
```

---

### **1.2. Create Landing Page**

**File: `frontend/index.html`**

**Sections:**
1. Header (Logo, Nav, Login button)
2. Hero (Judul, deskripsi, CTA)
3. Membership Plans (Basic & VIP cards)
4. Features (List fitur)
5. FAQ (Accordion)
6. Footer (Links, contact)

**Tech:**
- HTML5
- CSS3 (Bootstrap 5 CDN)
- Vanilla JavaScript

---

### **1.3. Create Register Page**

**File: `frontend/register.html`**

**Form Fields:**
- Nama Lengkap (text)
- WhatsApp (tel)
- Email (email)
- Membership (radio: Basic/VIP)
- Payment Method (radio: Wallet/Bank)
- Payment Detail (text)
- Payment Proof (file upload)
- Submit button

**Validation:**
- Client-side validation
- Image preview
- Form submission to API

---

### **1.4. Update Backend API**

**New Endpoints:**
```
POST /api/register - Register new user
POST /api/upload-payment-proof - Upload payment proof
GET /api/payment-status/:id - Get payment status
```

---

## 📋 STEP 2: SETUP HOSTING (FREE)

### **2.1. Setup Vercel (Frontend)**

**Step 1: Create Account**
1. Buka: https://vercel.com
2. Sign up dengan GitHub
3. Connect GitHub account

**Step 2: Deploy**
1. Klik "New Project"
2. Import repository (GitHub)
3. Select folder: `frontend`
4. Build command: (kosongkan - static site)
5. Output directory: `frontend`
6. Deploy!

**Step 3: Domain (Optional)**
- Pakai subdomain: `your-app.vercel.app` (gratis)
- Atau add custom domain

---

### **2.2. Setup Railway (Backend)**

**Step 1: Create Account**
1. Buka: https://railway.app
2. Sign up dengan GitHub
3. Connect GitHub account

**Step 2: Deploy**
1. Klik "New Project"
2. Deploy from GitHub repo
3. Select folder: `backend`
4. Add environment variables:
   ```
   TELEGRAM_TOKEN=your_token
   SECRET_KEY=your_secret
   JWT_SECRET_KEY=your_jwt_secret
   DATABASE_URL=your_database_url
   ```
5. Deploy!

**Step 3: Get URL**
- Railway akan kasih URL: `your-app.railway.app`
- Update frontend API_URL ke URL ini

---

### **2.3. Setup Supabase (Database)**

**Step 1: Create Account**
1. Buka: https://supabase.com
2. Sign up (gratis)
3. Create new project

**Step 2: Setup Database**
1. Go to SQL Editor
2. Run migration script (dari `backend/migrations/`)
3. Database ready!

**Step 3: Get Connection String**
1. Go to Settings → Database
2. Copy connection string
3. Update `DATABASE_URL` di Railway

---

## 📋 STEP 3: UPDATE CODE FOR PRODUCTION

### **3.1. Update API URL**

**File: `frontend/js/app.js`**

**Change:**
```javascript
const API_URL = 'http://localhost:5000/api';
```

**To:**
```javascript
const API_URL = 'https://your-backend.railway.app/api';
```

---

### **3.2. Update CORS**

**File: `backend/app.py`**

**Add:**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://your-frontend.vercel.app'])
```

---

### **3.3. Update Database URL**

**File: `backend/app.py`**

**Change:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///affiliate_system.db'
```

**To:**
```python
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///affiliate_system.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

---

## 📋 STEP 4: DEPLOY

### **4.1. Deploy Frontend**

```bash
# Push to GitHub
git add .
git commit -m "Add landing page and register"
git push origin main

# Vercel akan auto-deploy
```

**Check:**
- Vercel dashboard → Deployments
- Tunggu sampai "Ready"
- Test URL: `https://your-app.vercel.app`

---

### **4.2. Deploy Backend**

```bash
# Push to GitHub
git add .
git commit -m "Update API for production"
git push origin main

# Railway akan auto-deploy
```

**Check:**
- Railway dashboard → Deployments
- Tunggu sampai "Active"
- Test URL: `https://your-backend.railway.app/api/health`

---

### **4.3. Setup Database**

1. **Run Migration:**
   - Go to Supabase SQL Editor
   - Run migration script
   - Check tables created

2. **Test Connection:**
   - Test API endpoint
   - Check database connection

---

## 📋 STEP 5: TEST PRODUCTION

### **5.1. Test Landing Page**
- [ ] Buka landing page
- [ ] Cek semua sections
- [ ] Test responsive (mobile/desktop)
- [ ] Test CTA buttons

### **5.2. Test Register**
- [ ] Buka register page
- [ ] Isi form
- [ ] Upload payment proof
- [ ] Submit form
- [ ] Cek payment status

### **5.3. Test Login**
- [ ] Login dengan user baru
- [ ] Cek dashboard
- [ ] Test semua fitur

### **5.4. Test Admin**
- [ ] Login sebagai admin
- [ ] Cek pending payments
- [ ] Verify payment
- [ ] Cek pending reports
- [ ] Approve report

---

## 💰 COST BREAKDOWN

### **Free Tier Limits:**

**Vercel:**
- ✅ 100GB bandwidth/month
- ✅ Unlimited deployments
- ✅ SSL included

**Railway:**
- ✅ $5 credit/month (gratis)
- ✅ 500 hours runtime
- ✅ 1GB storage

**Supabase:**
- ✅ 500MB database
- ✅ 1GB file storage
- ✅ 2GB bandwidth

**Cloudinary:**
- ✅ 25GB storage
- ✅ 25GB bandwidth/month

**Total: $0-10/tahun** (hanya domain jika pakai .com)

---

## 🚨 TROUBLESHOOTING

### **Problem: Frontend tidak load**
- Cek Vercel deployment status
- Cek build logs
- Cek API_URL sudah benar

### **Problem: Backend error**
- Cek Railway logs
- Cek environment variables
- Cek database connection

### **Problem: Database connection failed**
- Cek DATABASE_URL
- Cek Supabase connection string
- Cek firewall settings

---

## 📋 CHECKLIST FINAL

### **Pre-Launch:**
- [ ] Code sudah siap
- [ ] Database migration selesai
- [ ] Environment variables set
- [ ] Test lokal berhasil

### **Deployment:**
- [ ] Frontend deployed (Vercel)
- [ ] Backend deployed (Railway)
- [ ] Database setup (Supabase)
- [ ] All services connected

### **Post-Launch:**
- [ ] Test semua fitur
- [ ] Monitor performance
- [ ] Setup backup (opsional)
- [ ] Update documentation

---

**Ready to launch! 🚀**


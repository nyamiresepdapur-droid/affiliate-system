# ⚙️ UPDATE CONFIGURATION - INSTRUKSI LENGKAP

**Update configuration untuk connect Vercel (frontend) dan Railway (backend)**

---

## 🎯 YANG PERLU DI-UPDATE

1. **Vercel Environment Variable:** `API_URL` → Point ke Railway
2. **Railway Environment Variable:** `FRONTEND_URL` → Point ke Vercel

---

## 📋 STEP 1: DAPATKAN URLS

**Simpan URL berikut:**

### **Railway Backend:**
```
https://your-backend.railway.app
```

**API URL:**
```
https://your-backend.railway.app/api
```

### **Vercel Frontend:**
```
https://your-app.vercel.app
```

---

## 📋 STEP 2: UPDATE VERCEL (FRONTEND)

### **Option 1: Via Environment Variable (Recommended)**

1. **Buka:** Vercel Dashboard
2. **Pilih project:** `affiliate-system`
3. **Settings** → **Environment Variables**
4. **Add Variable:**
   - **Key:** `API_URL`
   - **Value:** `https://your-backend.railway.app/api`
     *(Ganti dengan URL Railway Anda)*
   - **Environment:** 
     - ✅ Production
     - ✅ Preview  
     - ✅ Development
5. **Save**
6. **Redeploy:** 
   - Go to **Deployments** tab
   - Klik **"..."** pada deployment terbaru
   - Klik **"Redeploy"**

### **Option 2: Update Code Langsung**

**Jika environment variable tidak work, update code:**

1. **Edit:** `frontend/js/app.js`
   ```javascript
   const API_URL = 'https://your-backend.railway.app/api';
   ```

2. **Edit:** `frontend/js/register.js`
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

## 📋 STEP 3: UPDATE RAILWAY (BACKEND)

1. **Buka:** Railway Dashboard
2. **Pilih service** yang sudah dibuat
3. **Tab "Variables"**
4. **Add/Update Variable:**
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://your-app.vercel.app`
     *(Ganti dengan URL Vercel Anda)*
5. **Save**
6. **Railway akan auto-redeploy**

---

## 📋 STEP 4: VERIFY CONFIGURATION

### **Test Backend Health:**
1. **Buka browser:**
   ```
   https://your-backend.railway.app/api/health
   ```
2. **Harus return:**
   ```json
   {
     "status": "healthy",
     "database": "connected",
     "timestamp": "..."
   }
   ```

### **Test Frontend:**
1. **Buka:** URL Vercel Anda
2. **Buka browser console** (F12)
3. **Test API:**
   ```javascript
   fetch('https://your-backend.railway.app/api/health')
     .then(r => r.json())
     .then(console.log)
   ```
4. **Harus return data** tanpa CORS error

### **Test Register Flow:**
1. **Buka:** Register page di Vercel
2. **Isi form** dan submit
3. **Cek:** Response berhasil atau error
4. **Cek Railway logs** untuk melihat request

---

## 🔧 TROUBLESHOOTING

### **Problem: CORS Error**

**Error:** `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solusi:**
1. **Cek FRONTEND_URL** di Railway sudah benar
2. **Cek CORS origins** di backend code
3. **Restart Railway** (redeploy)

**Cek backend code:**
```python
# Di backend/app.py, pastikan:
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
CORS(app, origins=[FRONTEND_URL, 'https://your-app.vercel.app'])
```

---

### **Problem: API calls return 404**

**Solusi:**
1. **Cek API_URL** sudah benar (harus ada `/api` di akhir)
2. **Cek backend route** sudah ada
3. **Cek Railway deployment** status (harus Active)

---

### **Problem: API calls return 500**

**Solusi:**
1. **Cek Railway logs** untuk error detail
2. **Cek DATABASE_URL** sudah benar
3. **Cek environment variables** sudah lengkap

---

## 📋 CHECKLIST

- [ ] Railway URL sudah didapat
- [ ] Vercel URL sudah didapat
- [ ] API_URL sudah di-set di Vercel (atau update code)
- [ ] FRONTEND_URL sudah di-set di Railway
- [ ] Backend health check berhasil
- [ ] Frontend bisa akses backend API
- [ ] CORS sudah bekerja
- [ ] Register flow test berhasil

---

## 🎯 QUICK REFERENCE

**Vercel:**
```
Settings → Environment Variables → Add API_URL
```

**Railway:**
```
Variables → Add FRONTEND_URL
```

**Test:**
```
Backend: https://your-backend.railway.app/api/health
Frontend: https://your-app.vercel.app
```

---

**Update configuration sekarang! 🚀**


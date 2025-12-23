# ⚙️ UPDATE CONFIGURATION - CONNECT VERCEL & RAILWAY

**Langkah update configuration untuk connect frontend dan backend**

---

## 🎯 YANG PERLU DI-UPDATE

### **1. Frontend API_URL** (Point ke Railway)
### **2. Backend FRONTEND_URL** (Allow CORS dari Vercel)

---

## 📋 STEP 1: DAPATKAN URLS

**Simpan URL berikut:**

1. **Railway Backend URL:**
   - Contoh: `https://affiliate-system-production.up.railway.app`
   - **API URL:** `https://affiliate-system-production.up.railway.app/api`

2. **Vercel Frontend URL:**
   - Contoh: `https://affiliate-system-xxx.vercel.app`

---

## 📋 STEP 2: UPDATE VERCEL ENVIRONMENT VARIABLES

### **Via Vercel Dashboard (Recommended):**

1. **Buka:** Vercel Dashboard → Project → **Settings** → **Environment Variables**
2. **Add Variable:**
   - **Key:** `API_URL`
   - **Value:** `https://your-backend.railway.app/api`
     *(Ganti dengan URL Railway Anda)*
   - **Environment:** 
     - ✅ Production
     - ✅ Preview
     - ✅ Development
3. **Save**
4. **Redeploy:** Settings → Deployments → Redeploy (atau auto-redeploy)

---

## 📋 STEP 3: UPDATE RAILWAY ENVIRONMENT VARIABLES

1. **Buka:** Railway Dashboard → Service → **Variables**
2. **Add/Update Variable:**
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://your-app.vercel.app`
     *(Ganti dengan URL Vercel Anda)*
3. **Save**
4. **Railway akan auto-redeploy**

---

## 📋 STEP 4: UPDATE CODE (ALTERNATIF)

**Jika tidak pakai environment variables, update code langsung:**

### **Update Frontend:**

**File: `frontend/js/app.js`**
```javascript
// Ganti:
const API_URL = 'http://localhost:5000/api';

// Dengan:
const API_URL = 'https://your-backend.railway.app/api';
```

**File: `frontend/js/register.js`**
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

## 📋 STEP 5: VERIFY CONFIGURATION

### **Test Frontend:**
1. **Buka:** URL Vercel Anda
2. **Test:** Register page
3. **Submit form** dan cek apakah API call berhasil

### **Test Backend:**
1. **Buka:** `https://your-backend.railway.app/api/health`
2. **Harus return:** `{"status": "healthy", "database": "connected"}`

### **Test CORS:**
1. **Buka browser console** di Vercel frontend
2. **Test API call:**
   ```javascript
   fetch('https://your-backend.railway.app/api/health')
     .then(r => r.json())
     .then(console.log)
   ```
3. **Harus return data** tanpa CORS error

---

## 🔧 TROUBLESHOOTING

### **Problem: CORS error**
- Cek FRONTEND_URL di Railway sudah benar
- Cek CORS origins di backend code
- Cek frontend URL sudah benar

### **Problem: API calls failed**
- Cek API_URL sudah benar
- Cek backend sudah running
- Cek Railway logs untuk error

### **Problem: 404 Not Found**
- Cek API endpoint sudah benar
- Cek backend route sudah ada
- Cek Railway deployment status

---

## 📋 CHECKLIST

- [ ] Railway URL sudah didapat
- [ ] Vercel URL sudah didapat
- [ ] API_URL sudah di-set di Vercel
- [ ] FRONTEND_URL sudah di-set di Railway
- [ ] Frontend bisa akses backend API
- [ ] CORS sudah bekerja
- [ ] Test register flow berhasil

---

**Update configuration sekarang! 🚀**


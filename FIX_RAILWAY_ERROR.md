# 🔧 FIX RAILWAY ERROR - "Application failed to respond"

**Railway URL:** `affiliate-system-production.up.railway.app`  
**Vercel URL:** `https://affiliate-system-rho.vercel.app/`

---

## 🚨 PROBLEM: Railway Application Failed

**Error:** "Application failed to respond"

**Kemungkinan penyebab:**
1. Environment variables belum lengkap
2. Database connection failed
3. Code error saat startup
4. Port configuration salah

---

## 🔧 STEP 1: CEK RAILWAY LOGS

1. **Buka:** Railway Dashboard
2. **Klik service** yang error
3. **Tab "Logs"**
4. **Cek error message** di logs
5. **Copy error** untuk analisis

---

## 🔧 STEP 2: CEK ENVIRONMENT VARIABLES

**Pastikan semua variables sudah di-set:**

1. **Railway** → Service → **Variables**
2. **Cek variables berikut sudah ada:**

### **Required Variables:**
- [ ] `DATABASE_URL` = `postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres`
- [ ] `SECRET_KEY` = `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`
- [ ] `JWT_SECRET_KEY` = `4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a`
- [ ] `FLASK_ENV` = `production`
- [ ] `TELEGRAM_TOKEN` = (token bot Anda)
- [ ] `FRONTEND_URL` = `https://affiliate-system-rho.vercel.app`

---

## 🔧 STEP 3: FIX DATABASE CONNECTION

**Jika error karena database:**

1. **Cek DATABASE_URL** sudah benar
2. **Cek password** sudah benar: `1Milyarberkah$`
3. **Cek Supabase project** status (harus Active)
4. **Test connection** di Supabase SQL Editor

**Jika password perlu URL-encoded:**
- Password: `1Milyarberkah$`
- URL-encoded: `1Milyarberkah%24`
- Connection string: `postgresql://postgres:1Milyarberkah%24@db.xxx.supabase.co:5432/postgres`

---

## 🔧 STEP 4: UPDATE CONFIGURATION

### **Update Vercel API_URL:**

1. **Vercel Dashboard** → Project → **Settings** → **Environment Variables**
2. **Add Variable:**
   - **Key:** `API_URL`
   - **Value:** `https://affiliate-system-production.up.railway.app/api`
   - **Environment:** Production, Preview, Development
3. **Save**
4. **Redeploy:** Deployments → ... → Redeploy

### **Update Railway FRONTEND_URL:**

1. **Railway Dashboard** → Service → **Variables**
2. **Add/Update:**
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://affiliate-system-rho.vercel.app`
3. **Save**
4. **Railway akan auto-redeploy**

---

## 🔧 STEP 5: UPDATE CODE (JIKA PERLU)

**Update frontend code untuk production:**

**File: `frontend/js/app.js`**
```javascript
const API_URL = 'https://affiliate-system-production.up.railway.app/api';
```

**File: `frontend/js/register.js`**
```javascript
const API_URL = 'https://affiliate-system-production.up.railway.app/api';
```

**Commit & push:**
```bash
git add frontend/js/app.js frontend/js/register.js
git commit -m "Update API URL to Railway production"
git push
```

---

## 🔧 STEP 6: CEK RAILWAY SETTINGS

**Pastikan settings benar:**

1. **Root Directory:** `backend`
2. **Start Command:** `python app.py`
3. **Build Command:** `pip install -r requirements.txt`
4. **Port:** Railway auto-detect (atau set `PORT` variable)

---

## 🚨 COMMON ERRORS & FIXES

### **Error: "Module not found"**
**Fix:** Pastikan `requirements.txt` ada dan lengkap

### **Error: "DATABASE_URL not set"**
**Fix:** Add `DATABASE_URL` variable di Railway

### **Error: "Connection refused"**
**Fix:** Cek database connection string sudah benar

### **Error: "Port already in use"**
**Fix:** Railway auto-handle, tidak perlu set manual

---

## 📋 CHECKLIST FIX

- [ ] Cek Railway logs untuk error detail
- [ ] Semua environment variables sudah di-set
- [ ] DATABASE_URL sudah benar (dengan password)
- [ ] FRONTEND_URL sudah di-set
- [ ] Vercel API_URL sudah di-set
- [ ] Railway settings sudah benar
- [ ] Redeploy Railway
- [ ] Test health endpoint

---

**Cek Railway logs dulu untuk lihat error detail! 🔍**


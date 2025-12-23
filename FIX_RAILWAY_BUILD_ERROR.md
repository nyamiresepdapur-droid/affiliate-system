# 🔧 FIX RAILWAY BUILD ERROR

**Error:** `failed to solve: secret FRONTEND_URL not found`

**Penyebab:** Railway mencoba resolve `FRONTEND_URL` di build time, padahal hanya perlu di runtime

---

## 🔧 FIX: UPDATE RAILWAY CONFIGURATION

### **Option 1: Remove railway.json (Recommended)**

**File `railway.json` mungkin menyebabkan masalah. Hapus atau update:**

1. **Hapus file:** `railway.json` (jika ada)
2. **Railway akan auto-detect** Python project
3. **Redeploy**

### **Option 2: Update railway.json**

**Jika perlu keep file, update:**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Jangan reference environment variables di build section!**

---

## 🔧 FIX: SET ENVIRONMENT VARIABLES DI RAILWAY

**Railway** → Service → **Variables**, pastikan:

1. **FRONTEND_URL** sudah di-set (sebagai runtime variable, bukan build secret)
2. **Semua variables** sudah di-set sebelum build

---

## 🔧 FIX: UPDATE RAILWAY SETTINGS

1. **Railway** → Service → **Settings**
2. **Root Directory:** `backend`
3. **Start Command:** `python app.py`
4. **Build Command:** `pip install -r requirements.txt`
   - Atau kosongkan (Railway auto-detect)

---

## 🚨 QUICK FIX

**Cara tercepat:**

1. **Railway** → Service → **Settings**
2. **Hapus/Update Build Command** (kosongkan atau set ke `pip install -r requirements.txt`)
3. **Pastikan Start Command:** `python app.py`
4. **Set semua environment variables** di Variables tab
5. **Redeploy**

---

## 📋 ENVIRONMENT VARIABLES CHECKLIST

**Pastikan semua sudah di-set di Railway Variables:**

- [ ] `DATABASE_URL`
- [ ] `SECRET_KEY`
- [ ] `JWT_SECRET_KEY`
- [ ] `FLASK_ENV` = `production`
- [ ] `TELEGRAM_TOKEN`
- [ ] `FRONTEND_URL` = `https://affiliate-system-rho.vercel.app`

**⚠️ Semua variables harus di-set SEBELUM build!**

---

## 🔧 ALTERNATIF: REMOVE RAILWAY.JSON

**Jika masih error, hapus railway.json:**

1. **Delete file:** `railway.json`
2. **Commit & push:**
   ```bash
   git rm railway.json
   git commit -m "Remove railway.json to fix build error"
   git push
   ```
3. **Railway akan auto-redeploy** dengan default config

---

**Fix build error sekarang! 🔧**


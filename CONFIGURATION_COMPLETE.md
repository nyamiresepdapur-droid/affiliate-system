# ✅ CONFIGURATION UPDATE - COMPLETE

**URLs:**
- **Railway Backend:** `affiliate-system-production.up.railway.app`
- **Vercel Frontend:** `https://affiliate-system-rho.vercel.app/`

---

## ✅ YANG SUDAH DI-UPDATE

### **1. Frontend Code:**
- ✅ `frontend/js/app.js` - API_URL auto-detect production
- ✅ `frontend/js/register.js` - API_URL auto-detect production
- ✅ Auto-detect: Jika bukan localhost, pakai Railway URL

### **2. Backend Code:**
- ✅ `backend/app.py` - CORS allow Vercel production URL
- ✅ Support `FRONTEND_URL` environment variable

### **3. Code sudah di-commit & push ke GitHub:**
- ✅ Vercel akan auto-redeploy
- ✅ Railway akan auto-redeploy

---

## 🔧 YANG PERLU DI-SET DI RAILWAY

**Railway** → Variables, pastikan sudah ada:

1. **DATABASE_URL**
   ```
   postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres
   ```
   **⚠️ Jika error connection, coba URL-encode password:**
   ```
   postgresql://postgres:1Milyarberkah%24@db.xxx.supabase.co:5432/postgres
   ```

2. **SECRET_KEY**
   ```
   9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f
   ```

3. **JWT_SECRET_KEY**
   ```
   4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a
   ```

4. **FLASK_ENV**
   ```
   production
   ```

5. **TELEGRAM_TOKEN**
   ```
   (token bot Anda)
   ```

6. **FRONTEND_URL**
   ```
   https://affiliate-system-rho.vercel.app
   ```

---

## 🔧 YANG PERLU DI-SET DI VERCEL (OPSIONAL)

**Vercel** → Settings → Environment Variables:

**API_URL** (opsional, karena code sudah auto-detect):
```
https://affiliate-system-production.up.railway.app/api
```

---

## 🚨 FIX RAILWAY ERROR

**Jika Railway masih error "Application failed to respond":**

### **STEP 1: Cek Logs**
1. **Railway** → Service → **Logs tab**
2. **Scroll ke error** terakhir
3. **Copy error message**

### **STEP 2: Common Fixes**

**Error: "DATABASE_URL not set"**
- Add `DATABASE_URL` variable

**Error: "Connection refused"**
- Cek DATABASE_URL sudah benar
- Coba URL-encode password: `1Milyarberkah%24`

**Error: "Module not found"**
- Railway akan auto-install dari requirements.txt

**Error: "Port already in use"**
- Railway auto-handle, tidak perlu fix

### **STEP 3: Redeploy**
1. **Railway** → Deployments → **Redeploy**
2. **Tunggu** sampai selesai
3. **Cek logs** lagi

---

## ✅ TEST SETELAH FIX

### **1. Test Backend:**
```
https://affiliate-system-production.up.railway.app/api/health
```
**Harus return:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### **2. Test Frontend:**
```
https://affiliate-system-rho.vercel.app
```
- ✅ Landing page load
- ✅ Register page bisa diakses
- ✅ Form bisa diisi

### **3. Test Integration:**
- ✅ Submit registration dari Vercel
- ✅ Cek Railway logs untuk request
- ✅ Cek database untuk data baru

---

## 📋 CHECKLIST

- [x] Frontend code updated (auto-detect production)
- [x] Backend code updated (CORS allow Vercel)
- [x] Code committed & pushed
- [ ] Railway variables sudah lengkap
- [ ] Railway error sudah di-fix
- [ ] Backend health check berhasil
- [ ] Frontend bisa akses backend
- [ ] Register flow test berhasil

---

## 🎯 NEXT STEPS

1. **Fix Railway error** (cek logs)
2. **Set semua environment variables** di Railway
3. **Test health endpoint**
4. **Test register flow** end-to-end

---

**Configuration sudah di-update! Sekarang fix Railway error dan test! 🚀**


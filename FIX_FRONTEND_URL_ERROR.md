# 🔧 FIX FRONTEND_URL ERROR - RAILWAY BUILD

**Error:** `failed to solve: secret FRONTEND_URL not found`

**Penyebab:** Railway mencoba resolve FRONTEND_URL di build time

---

## 🔧 FIX: SET FRONTEND_URL SEBELUM BUILD

**Railway mencoba resolve semua environment variables di build time.**

**Solusi:** Set FRONTEND_URL di Railway Variables **SEBELUM** build.

---

## 🎯 LANGKAH FIX

### **STEP 1: Set FRONTEND_URL di Railway**

1. **Railway Dashboard** → Service → **Variables**
2. **Add Variable:**
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://affiliate-system-rho.vercel.app`
3. **Save**

**⚠️ PENTING:** Set **SEBELUM** build/redeploy!

---

### **STEP 2: Set Semua Variables**

**Pastikan semua sudah di-set:**

1. **FRONTEND_URL** = `https://affiliate-system-rho.vercel.app` ⚠️ **SET INI DULU!**
2. **DATABASE_URL** = `postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres`
3. **SECRET_KEY** = `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`
4. **JWT_SECRET_KEY** = `4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a`
5. **FLASK_ENV** = `production`
6. **TELEGRAM_TOKEN** = (token bot Anda)

---

### **STEP 3: Redeploy**

1. **Setelah semua variables di-set**
2. **Railway** → Deployments → **Redeploy**
3. **Tunggu** sampai build selesai

---

## 🔧 ALTERNATIF: BUAT FRONTEND_URL OPTIONAL

**Jika masih error, update code untuk make FRONTEND_URL optional:**

**File: `backend/app.py`** - Sudah optional, tapi pastikan tidak error jika tidak ada.

---

## 🚨 QUICK FIX

**Cara tercepat:**

1. **Railway** → Variables
2. **Add FRONTEND_URL** = `https://affiliate-system-rho.vercel.app`
3. **Set semua variables lainnya**
4. **Redeploy**

**Railway akan build dengan semua variables yang diperlukan!**

---

## 📋 CHECKLIST

- [ ] FRONTEND_URL sudah di-set di Railway Variables
- [ ] Semua variables sudah di-set
- [ ] Redeploy Railway
- [ ] Build berhasil
- [ ] Backend health check berhasil

---

**Set FRONTEND_URL di Railway Variables sekarang, lalu redeploy! 🚀**


# 🔐 RAILWAY VARIABLES - SETUP LENGKAP

**Railway:** `affiliate-system-production.up.railway.app`  
**Vercel:** `https://affiliate-system-rho.vercel.app/`

---

## 📋 VARIABLES YANG HARUS DI-SET DI RAILWAY

**Railway** → Service → **Variables** → **Add Variable** (satu per satu):

### **1. FRONTEND_URL** ⚠️ **SET INI DULU!**
- **Key:** `FRONTEND_URL`
- **Value:** `https://affiliate-system-rho.vercel.app`
- **⚠️ PENTING:** Set ini SEBELUM build!

---

### **2. DATABASE_URL**
- **Key:** `DATABASE_URL`
- **Value:** `postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres`
- **Ganti `xxx`** dengan project reference dari Supabase
- **Jika error, coba URL-encode password:** `1Milyarberkah%24`

---

### **3. SECRET_KEY**
- **Key:** `SECRET_KEY`
- **Value:** `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`

---

### **4. JWT_SECRET_KEY**
- **Key:** `JWT_SECRET_KEY`
- **Value:** `4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a`

---

### **5. FLASK_ENV**
- **Key:** `FLASK_ENV`
- **Value:** `production`

---

### **6. TELEGRAM_TOKEN**
- **Key:** `TELEGRAM_TOKEN`
- **Value:** (token bot Telegram Anda dari BotFather)

---

### **7. GROUP_CHAT_ID** (Opsional)
- **Key:** `GROUP_CHAT_ID`
- **Value:** (ID group Telegram, jika ada)

---

### **8. CHANNEL_CHAT_ID** (Opsional)
- **Key:** `CHANNEL_CHAT_ID`
- **Value:** (ID channel Telegram, jika ada)

---

## 🎯 CARA SET DI RAILWAY

1. **Buka:** Railway Dashboard
2. **Pilih service** yang sudah dibuat
3. **Tab "Variables"**
4. **Klik "New Variable"**
5. **Isi Key dan Value**
6. **Klik "Add"**
7. **Ulangi** untuk semua variables

---

## ⚠️ PENTING

**Set FRONTEND_URL DULU sebelum variables lainnya!**

Railway akan coba resolve semua variables di build time, jadi pastikan semua sudah di-set sebelum build.

---

## 🔄 SETELAH SET SEMUA VARIABLES

1. **Railway akan auto-redeploy** setelah variables di-set
2. **Atau manual redeploy:** Deployments → ... → Redeploy
3. **Cek logs** untuk memastikan build berhasil

---

## ✅ TEST

**Setelah build berhasil:**

1. **Backend Health:**
   ```
   https://affiliate-system-production.up.railway.app/api/health
   ```

2. **Frontend:**
   ```
   https://affiliate-system-rho.vercel.app
   ```

---

**Set semua variables di Railway sekarang! 🚀**


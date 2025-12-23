# 🔐 RAILWAY ENVIRONMENT VARIABLES - LENGKAP

**Secret yang sudah di-generate:**
```
9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f
```

---

## 📋 VARIABLES YANG PERLU DI-SET DI RAILWAY

### **1. SECRET_KEY**

**Di Railway:**
- **Key:** `SECRET_KEY`
- **Value:** `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`

---

### **2. JWT_SECRET_KEY**

**Generate secret baru untuk JWT (jalankan di terminal):**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Atau pakai secret yang sama (tidak recommended, tapi bisa):**
- **Key:** `JWT_SECRET_KEY`
- **Value:** `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`

**⚠️ Lebih baik generate secret baru untuk JWT_SECRET_KEY**

---

### **3. DATABASE_URL**

**Dari Supabase:**
- **Key:** `DATABASE_URL`
- **Value:** `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`
- **Ganti `[PASSWORD]`** dengan password Supabase Anda

---

### **4. FLASK_ENV**

- **Key:** `FLASK_ENV`
- **Value:** `production`

---

### **5. TELEGRAM_TOKEN**

- **Key:** `TELEGRAM_TOKEN`
- **Value:** Token bot Telegram Anda (dari BotFather)

---

### **6. GROUP_CHAT_ID** (Opsional)

- **Key:** `GROUP_CHAT_ID`
- **Value:** ID group Telegram (jika ada)

---

### **7. CHANNEL_CHAT_ID** (Opsional)

- **Key:** `CHANNEL_CHAT_ID`
- **Value:** ID channel Telegram (jika ada)

---

### **8. FRONTEND_URL** (Update setelah Vercel deploy)

- **Key:** `FRONTEND_URL`
- **Value:** URL dari Vercel (contoh: `https://affiliate-system-xxx.vercel.app`)
- **Update nanti** setelah Vercel deploy

---

## 🎯 CARA SET DI RAILWAY

### **STEP 1: Buka Railway Service**

1. **Railway dashboard** → Klik service yang sudah dibuat
2. **Tab "Variables"**

---

### **STEP 2: Add Variables**

**Klik "New Variable" untuk setiap variable:**

1. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`
   - Klik "Add"

2. **JWT_SECRET_KEY** (generate baru atau pakai yang sama)
   - Key: `JWT_SECRET_KEY`
   - Value: (generate baru dengan command yang sama)
   - Klik "Add"

3. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: (dari Supabase, sudah ganti password)
   - Klik "Add"

4. **FLASK_ENV**
   - Key: `FLASK_ENV`
   - Value: `production`
   - Klik "Add"

5. **TELEGRAM_TOKEN**
   - Key: `TELEGRAM_TOKEN`
   - Value: (token bot Anda)
   - Klik "Add"

6. **FRONTEND_URL** (update nanti)
   - Key: `FRONTEND_URL`
   - Value: (URL Vercel, update setelah deploy)
   - Klik "Add"

---

### **STEP 3: Deploy**

**Setelah semua variables di-set:**
- Railway akan **auto-redeploy**
- Tunggu sampai status "Active"
- Cek logs untuk memastikan tidak ada error

---

## 🔄 GENERATE JWT_SECRET_KEY BARU (RECOMMENDED)

**Jalankan di terminal:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Copy hasilnya** dan gunakan sebagai `JWT_SECRET_KEY`

**Contoh output:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

---

## 📋 CHECKLIST VARIABLES

**Minimum yang diperlukan:**
- [x] SECRET_KEY = `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`
- [ ] JWT_SECRET_KEY = (generate baru)
- [ ] DATABASE_URL = (dari Supabase)
- [ ] FLASK_ENV = `production`
- [ ] TELEGRAM_TOKEN = (token bot)

**Opsional:**
- [ ] GROUP_CHAT_ID = (jika ada)
- [ ] CHANNEL_CHAT_ID = (jika ada)
- [ ] FRONTEND_URL = (update setelah Vercel)

---

**Set semua variables di Railway sekarang! 🚀**


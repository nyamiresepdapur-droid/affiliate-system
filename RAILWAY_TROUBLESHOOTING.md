# 🔧 RAILWAY TROUBLESHOOTING - BACKEND ERROR

**Error:** "Application failed to respond"  
**Frontend:** ✅ Berhasil (Vercel)  
**Backend:** ❌ Error (Railway)

---

## 🔍 STEP 1: CEK RAILWAY LOGS

**Cara cek logs:**

1. **Railway Dashboard** → Service → **Deployments**
2. **Klik deployment terbaru** (yang paling atas)
3. **Tab "Logs"** atau scroll ke bawah
4. **Cari error message** (biasanya di akhir logs)
5. **Copy error message lengkap** dan kirim ke saya

**Atau:**

1. **Railway Dashboard** → Service → **Metrics** → **Logs**
2. **Scroll** untuk melihat real-time logs
3. **Cari error** (biasanya merah atau dengan "Error", "Exception", "Traceback")

---

## 🚨 ERROR YANG MUNGKIN TERJADI

### **1. Database Connection Error**

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
connection refused
```

**Fix:**
- Cek DATABASE_URL format
- Pastikan Supabase database sudah running
- Cek firewall/network settings

---

### **2. Import Error (Google Sheets / Channel Service)**

**Error:**
```
ModuleNotFoundError: No module named 'google_sheets_service'
ImportError: cannot import name 'GoogleSheetsService'
```

**Fix:**
- File mungkin tidak ada atau path salah
- Cek apakah file ada di folder `backend`

---

### **3. Telegram Bot Error**

**Error:**
```
Error starting bot: ...
```

**Fix:**
- Bot akan crash tapi Flask app tetap jalan
- Cek TELEGRAM_TOKEN
- Bot error tidak akan crash Flask app (daemon thread)

---

### **4. Port Error**

**Error:**
```
Address already in use
```

**Fix:**
- Railway auto-handle, tidak perlu fix
- Pastikan tidak hardcode port

---

### **5. Secret Key Error**

**Error:**
```
ValueError: SECRET_KEY must be set in production
```

**Fix:**
- Pastikan SECRET_KEY dan JWT_SECRET_KEY sudah di-set
- Cek format (tidak ada spasi di awal/akhir)

---

## 🔧 QUICK FIXES

### **Fix 1: Cek Root Directory**

1. **Railway** → Settings
2. **Root Directory:** `backend`
3. **Start Command:** `python app.py`
4. **Save** → **Redeploy**

---

### **Fix 2: Cek Environment Variables**

**Pastikan semua sudah di-set:**

- [ ] DATABASE_URL
- [ ] SECRET_KEY
- [ ] JWT_SECRET_KEY
- [ ] FLASK_ENV = `production`
- [ ] TELEGRAM_TOKEN
- [ ] FRONTEND_URL

---

### **Fix 3: Redeploy**

1. **Railway** → Deployments
2. **Klik "..."** → **Redeploy**
3. **Tunggu** sampai build selesai
4. **Cek logs** lagi

---

## 📋 CHECKLIST

- [ ] Cek Railway logs untuk error detail
- [ ] Copy error message lengkap
- [ ] Cek Root Directory = `backend`
- [ ] Cek Start Command = `python app.py`
- [ ] Cek semua environment variables
- [ ] Redeploy jika perlu

---

## 🆘 JIKA MASIH ERROR

**Kirim ke saya:**
1. **Error message lengkap** dari Railway logs
2. **Screenshot** Railway logs (jika bisa)
3. **Railway Settings** screenshot (Root Directory, Start Command)

---

**Cek Railway logs sekarang dan kirim error message ke saya! 🔍**


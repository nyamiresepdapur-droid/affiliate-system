# 🔍 CHECK RAILWAY LOGS - TROUBLESHOOTING

**Status:** Backend masih error "Application failed to respond"

---

## 🔍 STEP 1: CEK RAILWAY LOGS

1. **Railway Dashboard** → Service → **Deployments**
2. **Klik build terbaru** (yang paling atas)
3. **Tab "Logs"** atau **"View Logs"**
4. **Scroll ke bawah** untuk melihat error terakhir
5. **Copy error message** dan kirim ke saya

---

## 🚨 ERROR YANG MUNGKIN TERJADI

### **1. Database Connection Error**

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Fix:**
- Cek DATABASE_URL format
- Pastikan database sudah di-migrate
- Cek Supabase connection settings

---

### **2. Port Error**

**Error:**
```
Address already in use
```

**Fix:**
- Railway auto-handle port, tidak perlu fix
- Pastikan tidak hardcode port di code

---

### **3. Module Not Found**

**Error:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Fix:**
- Pastikan `requirements.txt` lengkap
- Railway akan auto-install

---

### **4. Import Error**

**Error:**
```
ImportError: cannot import name 'xxx'
```

**Fix:**
- Cek import statements di code
- Pastikan semua dependencies ada

---

### **5. Secret Key Error**

**Error:**
```
ValueError: SECRET_KEY must be set in production
```

**Fix:**
- Pastikan SECRET_KEY dan JWT_SECRET_KEY sudah di-set
- Cek format (tidak ada spasi)

---

## 🔧 QUICK FIXES

### **Fix 1: Redeploy**

1. **Railway** → Deployments
2. **Klik "..."** → **Redeploy**
3. **Tunggu** sampai build selesai

---

### **Fix 2: Cek Root Directory**

1. **Railway** → Settings
2. **Root Directory:** `backend`
3. **Start Command:** `python app.py`
4. **Redeploy**

---

### **Fix 3: Cek Environment Variables**

1. **Railway** → Variables
2. **Pastikan semua sudah di-set:**
   - DATABASE_URL
   - SECRET_KEY
   - JWT_SECRET_KEY
   - FLASK_ENV = `production`
   - TELEGRAM_TOKEN
   - FRONTEND_URL

---

## 📋 CHECKLIST

- [ ] Cek Railway logs untuk error detail
- [ ] Copy error message
- [ ] Cek Root Directory = `backend`
- [ ] Cek Start Command = `python app.py`
- [ ] Cek semua environment variables
- [ ] Redeploy jika perlu

---

**Cek Railway logs sekarang dan kirim error message ke saya! 🔍**


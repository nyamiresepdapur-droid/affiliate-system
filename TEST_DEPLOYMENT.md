# ✅ TEST DEPLOYMENT - SETELAH VARIABLES DI-SET

**Status:** Semua variables sudah di-set di Railway ✅

---

## 🔍 CEK BUILD STATUS

1. **Railway Dashboard** → Service → **Deployments**
2. **Cek build terbaru:**
   - ✅ **Success** = Build berhasil
   - ❌ **Failed** = Cek logs untuk error

---

## 🧪 TEST BACKEND

### **1. Health Check**

**URL:**
```
https://affiliate-system-production.up.railway.app/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Jika error:**
- Cek Railway logs
- Pastikan DATABASE_URL benar
- Pastikan database sudah di-migrate

---

### **2. Test API Endpoints**

**Test Products:**
```
https://affiliate-system-production.up.railway.app/api/products
```

**Expected:** List products (atau empty array jika belum ada data)

---

## 🧪 TEST FRONTEND

**URL:**
```
https://affiliate-system-rho.vercel.app
```

**Test:**
1. ✅ Landing page load
2. ✅ Register page bisa diakses
3. ✅ Form register bisa di-submit
4. ✅ API calls ke backend berhasil

---

## 🚨 JIKA BUILD MASIH ERROR

### **Error: "FRONTEND_URL not found"**
- ✅ Sudah di-fix dengan membuat FRONTEND_URL optional
- Pastikan FRONTEND_URL sudah di-set di Railway Variables

### **Error: "DATABASE_URL not found"**
- Pastikan DATABASE_URL sudah di-set
- Cek format: `postgresql://postgres:password@host:port/dbname`

### **Error: "Module not found"**
- Railway akan auto-install dari `requirements.txt`
- Pastikan file ada di folder `backend`

### **Error: "Port already in use"**
- Railway auto-handle, tidak perlu fix

---

## 📋 CHECKLIST

- [x] Semua variables sudah di-set di Railway
- [ ] Railway build berhasil
- [ ] Backend health check berhasil
- [ ] Frontend bisa akses backend
- [ ] Register flow berhasil

---

## 🔧 NEXT STEPS

**Setelah semua test berhasil:**

1. **Database Migration:**
   - Run migration di Supabase (jika belum)
   - File: `backend/migrations/create_tables.sql`

2. **Test Full Flow:**
   - Register user baru
   - Login
   - Scrape product
   - Report content

---

**Cek Railway build status sekarang! 🚀**


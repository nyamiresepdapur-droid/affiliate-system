# ✅ DEPLOYMENT CHECKLIST

**Checklist lengkap untuk deployment**

---

## 🎯 RAILWAY (BACKEND)

### **Setup:**
- [ ] Akun Railway sudah dibuat
- [ ] Repository sudah di-import
- [ ] Root directory: `backend`
- [ ] Start command: `python app.py`
- [ ] Build command: `pip install -r requirements.txt`

### **Environment Variables:**
- [ ] `SECRET_KEY` = `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`
- [ ] `JWT_SECRET_KEY` = `4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a`
- [ ] `DATABASE_URL` = (dari Supabase, password: `1Milyarberkah$`)
- [ ] `FLASK_ENV` = `production`
- [ ] `TELEGRAM_TOKEN` = (token bot Anda)
- [ ] `FRONTEND_URL` = (URL Vercel - update setelah deploy)

### **Deploy:**
- [ ] Domain sudah di-generate
- [ ] Port sudah di-set (5000)
- [ ] Deploy berhasil
- [ ] URL Railway sudah didapat
- [ ] Backend bisa diakses (test `/api/health`)

---

## 🎯 VERCEL (FRONTEND)

### **Setup:**
- [ ] Akun Vercel sudah dibuat
- [ ] Repository sudah di-import
- [ ] Root directory: `frontend`
- [ ] Build command: (kosongkan)
- [ ] Output directory: `frontend`

### **Environment Variables:**
- [ ] `API_URL` = (URL Railway + `/api`)

### **Deploy:**
- [ ] Deploy berhasil
- [ ] URL Vercel sudah didapat
- [ ] Frontend bisa diakses
- [ ] Landing page load
- [ ] Register page bisa diakses

---

## 🎯 SUPABASE (DATABASE)

### **Setup:**
- [ ] Akun Supabase sudah dibuat
- [ ] Project sudah dibuat
- [ ] Database password: `1Milyarberkah$` (sudah diketahui)

### **Migration:**
- [ ] Connection string sudah didapat
- [ ] Migration script sudah di-run
- [ ] Tables sudah dibuat
- [ ] Default owner sudah dibuat

### **Connection:**
- [ ] DATABASE_URL sudah di-set di Railway
- [ ] Database connection berhasil
- [ ] Test query berhasil

---

## 🎯 CONFIGURATION

### **Backend:**
- [ ] CORS sudah di-update (allow Vercel URL)
- [ ] DATABASE_URL sudah di-set
- [ ] All environment variables sudah di-set

### **Frontend:**
- [ ] API_URL sudah di-update (point ke Railway)
- [ ] All links sudah benar

---

## 🎯 TESTING

### **Frontend:**
- [ ] Landing page load
- [ ] Register page load
- [ ] Form bisa diisi
- [ ] Submit registration

### **Backend:**
- [ ] Health check: `/api/health`
- [ ] API bisa diakses
- [ ] Database connection berhasil

### **Integration:**
- [ ] Register flow end-to-end
- [ ] File upload berhasil
- [ ] Data masuk ke database

---

## 📋 URLS YANG PERLU DISIMPAN

**Railway Backend:**
```
https://your-backend.railway.app
```

**Vercel Frontend:**
```
https://your-app.vercel.app
```

**Supabase:**
```
https://supabase.com/dashboard/project/xxx
```

---

## 🚀 NEXT STEPS SETELAH DEPLOY

1. **Test semua fitur** di production
2. **Setup custom domain** (opsional)
3. **Monitor logs** untuk error
4. **Setup backup** (opsional)

---

**Gunakan checklist ini untuk track progress deployment! ✅**


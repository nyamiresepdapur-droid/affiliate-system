# 🔌 RAILWAY PORT SETUP

**Port yang digunakan: 5000 (atau dari environment variable PORT)**

---

## 🎯 LANGKAH DI RAILWAY

### **STEP 1: Set Port di Generate Domain**

**Di field "Enter the port your app is listening on":**

1. **Ganti `8080` dengan:** `5000`
   - Flask app menggunakan port **5000**
   - Code sudah di-update untuk support `PORT` environment variable

2. **Klik:** "Generate Domain"

---

## 🔧 PORT CONFIGURATION

**Backend code sudah support:**
- **Environment variable `PORT`** (Railway auto-set)
- **Default:** `5000` jika PORT tidak di-set

**Railway biasanya:**
- Auto-detect port dari code
- Atau set `PORT` environment variable
- Default Railway port: `8080` (tapi kita pakai 5000)

---

## 📋 SETELAH GENERATE DOMAIN

**Anda akan dapat URL seperti:**
```
https://affiliate-system-production.up.railway.app
```

**URL ini untuk:**
1. **Update FRONTEND_URL** di Railway (setelah Vercel deploy)
2. **Update API_URL** di Vercel environment variables
3. **Test backend:** `https://your-backend.railway.app/api/health`

---

## ⚠️ CATATAN

- **Port 5000** adalah port yang benar untuk Flask
- **Railway akan auto-set PORT** environment variable
- **Code sudah di-update** untuk read PORT dari environment

---

**Set port ke 5000, lalu klik "Generate Domain"! 🚀**


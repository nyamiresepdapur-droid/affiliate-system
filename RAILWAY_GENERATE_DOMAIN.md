# 🌐 RAILWAY: GENERATE DOMAIN

**Langkah untuk generate public domain di Railway**

---

## 🎯 LANGKAH GENERATE DOMAIN

### **STEP 1: Set Port**

**Di field "Enter the port your app is listening on":**

1. **Ganti `8080` dengan:** `5000`
   - Flask default port adalah **5000**
   - Atau cek di `backend/app.py` - biasanya `app.run(port=5000)`

2. **Jika tidak yakin, cek:**
   - Buka `backend/app.py`
   - Cari: `app.run(port=...)`
   - Atau default Flask adalah 5000

---

### **STEP 2: Generate Domain**

1. **Setelah port di-set ke `5000`**
2. **Klik:** "Generate Domain" (tombol purple)
3. **Railway akan generate domain** (contoh: `affiliate-system-production.up.railway.app`)
4. **Simpan URL ini!** (untuk update FRONTEND_URL nanti)

---

## 🔧 PORT YANG BENAR

**Flask default port:**
- **Development:** `5000`
- **Production:** `5000` (atau sesuai environment variable `PORT`)

**Railway biasanya auto-detect port, tapi jika tidak:**
- **Set ke:** `5000`
- **Atau:** Cek environment variable `PORT` di Railway

---

## 📋 SETELAH DOMAIN DI-GENERATE

**Anda akan dapat URL seperti:**
```
https://affiliate-system-production.up.railway.app
```

**Update FRONTEND_URL di Railway:**
1. **Railway** → Variables
2. **Add/Update:**
   - Key: `FRONTEND_URL`
   - Value: (URL dari Vercel - update setelah Vercel deploy)
3. **Backend URL untuk frontend:**
   - Update `API_URL` di Vercel dengan: `https://affiliate-system-production.up.railway.app/api`

---

## ⚠️ CATATAN

- **Port 5000** adalah default Flask
- **Jika error, cek logs** di Railway untuk melihat port yang digunakan
- **Domain akan aktif** setelah deploy selesai

---

**Set port ke 5000, lalu klik "Generate Domain"! 🚀**


# 🔧 FIX RAILWAY ERROR - QUICK GUIDE

**Railway:** `affiliate-system-production.up.railway.app`  
**Vercel:** `https://affiliate-system-rho.vercel.app/`

---

## 🚨 PROBLEM: Application Failed to Respond

**Langkah fix:**

### **STEP 1: Cek Railway Logs**

1. **Railway Dashboard** → Service → **Logs tab**
2. **Scroll ke error** terakhir
3. **Copy error message**
4. **Cek apa error-nya**

---

### **STEP 2: Cek Environment Variables**

**Railway** → Variables, pastikan sudah ada:

1. **DATABASE_URL**
   - Value: `postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres`
   - **⚠️ Jika error, coba URL-encode password:** `1Milyarberkah%24`

2. **SECRET_KEY**
   - Value: `9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f`

3. **JWT_SECRET_KEY**
   - Value: `4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a`

4. **FLASK_ENV**
   - Value: `production`

5. **TELEGRAM_TOKEN**
   - Value: (token bot Anda)

6. **FRONTEND_URL**
   - Value: `https://affiliate-system-rho.vercel.app`

---

### **STEP 3: Fix Database Connection**

**Jika error karena database connection:**

**Option 1: URL-encode password**
- Password: `1Milyarberkah$`
- Encoded: `1Milyarberkah%24`
- Update DATABASE_URL di Railway dengan encoded password

**Option 2: Test connection di Supabase**
1. **Supabase** → SQL Editor
2. **Run:** `SELECT 1;`
3. **Jika berhasil, connection string benar**

---

### **STEP 4: Redeploy Railway**

1. **Railway** → Service → **Deployments**
2. **Klik "..."** pada deployment terbaru
3. **Klik "Redeploy"**
4. **Tunggu** sampai selesai
5. **Cek logs** untuk error

---

### **STEP 5: Update Vercel**

**Vercel** → Settings → Environment Variables:

1. **Add:**
   - Key: `API_URL`
   - Value: `https://affiliate-system-production.up.railway.app/api`
2. **Redeploy** Vercel

---

## 📋 COMMON ERRORS

### **"DATABASE_URL not set"**
- Add `DATABASE_URL` variable di Railway

### **"Connection refused"**
- Cek DATABASE_URL sudah benar
- Cek Supabase project status

### **"Module not found"**
- Cek `requirements.txt` ada
- Railway akan auto-install

### **"Port already in use"**
- Railway auto-handle, tidak perlu fix

---

## ✅ SETELAH FIX

**Test:**
1. **Backend:** `https://affiliate-system-production.up.railway.app/api/health`
2. **Frontend:** `https://affiliate-system-rho.vercel.app`
3. **Register flow:** Test submit registration

---

**Cek Railway logs dulu untuk lihat error detail! 🔍**


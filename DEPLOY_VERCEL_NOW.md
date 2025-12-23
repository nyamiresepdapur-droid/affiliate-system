# 🚀 DEPLOY VERCEL - STEP BY STEP

**Langkah deploy frontend ke Vercel**

---

## 🎯 STEP 1: BUAT AKUN VERCEL

1. **Buka:** https://vercel.com
2. **Klik:** "Sign Up"
3. **Pilih:** "Continue with GitHub"
4. **Authorize** Vercel untuk akses GitHub
5. **Selesai!** Akun sudah dibuat

---

## 🎯 STEP 2: IMPORT REPOSITORY

1. **Setelah login, klik:** "Add New..." → "Project"
2. **Atau klik:** "Import Project"
3. **Pilih repository:** `nyamiresepdapur-droid/affiliate-system`
4. **Jika tidak muncul, klik:** "Import Git Repository"
5. **Paste URL:** `https://github.com/nyamiresepdapur-droid/affiliate-system`
6. **Klik:** "Import"

---

## 🎯 STEP 3: CONFIGURE PROJECT

**Isi form yang muncul:**

1. **Project Name:**
   - Default: `affiliate-system` (bisa diubah)
   - Biarkan default atau ubah sesuai keinginan

2. **Framework Preset:**
   - Pilih: **"Other"** atau **"Vite"** (tidak masalah, kita akan override)

3. **Root Directory:**
   - **Klik "Edit"** (atau "Change")
   - **Pilih:** `frontend`
   - **Klik:** "Continue"

4. **Build and Output Settings:**
   - **Build Command:** (kosongkan - static site)
   - **Output Directory:** `frontend`
   - **Install Command:** (kosongkan)

5. **Environment Variables (opsional, bisa diisi nanti):**
   - **API_URL** = (akan di-update setelah Railway deploy)
   - Untuk sekarang bisa skip

6. **Klik:** "Deploy"

---

## 🎯 STEP 4: TUNGGU DEPLOY

1. **Vercel akan:**
   - Clone repository dari GitHub
   - Build project
   - Deploy ke CDN global

2. **Tunggu** sampai status "Ready" (1-2 menit)

3. **Setelah selesai, dapat URL:**
   - Contoh: `https://affiliate-system-xxx.vercel.app`
   - **Simpan URL ini!**

---

## 🎯 STEP 5: UPDATE API_URL (SETELAH RAILWAY DEPLOY)

**Setelah Railway sudah deploy dan dapat URL:**

1. **Vercel Dashboard** → Project → **Settings** → **Environment Variables**
2. **Add Variable:**
   - **Key:** `API_URL`
   - **Value:** `https://your-backend.railway.app/api`
     *(Ganti dengan URL Railway yang sudah di-generate)*
   - **Environment:** Production, Preview, Development (centang semua)
3. **Save**

**Atau update code langsung:**

1. **Edit:** `frontend/js/app.js` dan `frontend/js/register.js`
2. **Ganti:** `const API_URL = 'http://localhost:5000/api';`
3. **Dengan:** `const API_URL = 'https://your-backend.railway.app/api';`
4. **Commit & push:**
   ```bash
   git add frontend/js/app.js frontend/js/register.js
   git commit -m "Update API URL for production"
   git push
   ```
5. **Vercel akan auto-redeploy**

---

## 🎯 STEP 6: TEST FRONTEND

1. **Buka URL Vercel** yang diberikan
2. **Test:**
   - ✅ Landing page load
   - ✅ Register page bisa diakses
   - ✅ Form bisa diisi
   - ✅ Submit registration (jika backend sudah ready)

---

## 📋 CHECKLIST VERCEL

- [ ] Akun Vercel sudah dibuat
- [ ] Repository sudah di-import
- [ ] Root directory: `frontend`
- [ ] Build command: (kosongkan)
- [ ] Output directory: `frontend`
- [ ] Deploy berhasil
- [ ] URL sudah didapat
- [ ] API_URL sudah di-update (setelah Railway)

---

## 🚨 TROUBLESHOOTING

### **Problem: Build failed**
- Cek build logs di Vercel
- Pastikan root directory benar: `frontend`
- Pastikan tidak ada syntax error

### **Problem: Page not found**
- Cek output directory: `frontend`
- Cek file `index.html` ada di folder `frontend`

### **Problem: API calls failed**
- Cek API_URL sudah benar
- Cek CORS di backend sudah allow Vercel URL
- Cek backend sudah running di Railway

---

**Deploy Vercel sekarang! 🚀**


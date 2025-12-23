# 🔧 FIX RAILWAY FRONTEND_URL ERROR - FINAL

**Error:** `secret FRONTEND_URL not found` di build time

**Penyebab:** Railway Nixpacks mencoba resolve semua environment variables di build time

---

## 🔧 SOLUSI 1: SET FRONTEND_URL DI RAILWAY (RECOMMENDED)

**Railway** → Service → **Variables**:

1. **Pastikan FRONTEND_URL sudah ada:**
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://affiliate-system-rho.vercel.app`

2. **Set SEBELUM build/redeploy**

3. **Redeploy:**
   - Railway → Deployments → **Redeploy**

---

## 🔧 SOLUSI 2: BUAT NIXPACKS.TOML

**File `nixpacks.toml` sudah dibuat di root directory.**

**Isi:**
```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python app.py"
```

**Fungsi:** Skip environment variable resolution di build time

---

## 🔧 SOLUSI 3: UPDATE CODE (SUDAH DILAKUKAN)

**Code sudah di-update:**
- FRONTEND_URL optional di `backend/app.py`
- Tidak akan error jika FRONTEND_URL tidak ada

---

## 🎯 LANGKAH FIX

### **STEP 1: Pastikan FRONTEND_URL di Railway**

1. **Railway** → Service → **Variables**
2. **Cek apakah FRONTEND_URL ada:**
   - Jika tidak ada → **Add Variable**
   - Key: `FRONTEND_URL`
   - Value: `https://affiliate-system-rho.vercel.app`
3. **Save**

---

### **STEP 2: Push nixpacks.toml**

**File `nixpacks.toml` sudah dibuat. Push ke GitHub:**

```bash
git add nixpacks.toml
git commit -m "Add nixpacks.toml to fix FRONTEND_URL build error"
git push origin main
```

---

### **STEP 3: Redeploy Railway**

1. **Railway** → Deployments
2. **Klik "..."** → **Redeploy**
3. **Tunggu** sampai build selesai

---

## 🚨 JIKA MASIH ERROR

**Cek Railway logs untuk error detail:**

1. **Railway** → Deployments → **Klik deployment terbaru**
2. **Tab "Logs"**
3. **Copy error message** dan kirim ke saya

---

## 📋 CHECKLIST

- [ ] FRONTEND_URL sudah di-set di Railway Variables
- [ ] nixpacks.toml sudah di-push ke GitHub
- [ ] Railway redeploy
- [ ] Build berhasil
- [ ] Backend health check berhasil

---

**Set FRONTEND_URL di Railway Variables, lalu push nixpacks.toml dan redeploy! 🚀**


# 🔑 CARA GENERATE PERSONAL ACCESS TOKEN DI GITHUB

**Untuk push code ke GitHub tanpa login via desktop**

---

## 🎯 LANGKAH LENGKAP

### **STEP 1: Buka GitHub Settings**

1. **Buka browser** (Chrome, Firefox, dll)
2. **Login ke GitHub:** https://github.com/login
3. **Setelah login, buka:** https://github.com/settings/tokens
   - Atau: Klik profile picture (kanan atas) → Settings → Developer settings → Personal access tokens → Tokens (classic)

---

### **STEP 2: Generate New Token**

1. **Klik tombol:** "Generate new token" → "Generate new token (classic)"
2. **Jika diminta password, masukkan password GitHub Anda**

---

### **STEP 3: Isi Form Token**

**Isi form dengan:**

1. **Note:** `Affiliate System Push`
   - (Nama token, untuk identifikasi)

2. **Expiration:** 
   - Pilih: `90 days` (atau sesuai kebutuhan)
   - Atau: `No expiration` (jika mau permanen)

3. **Select scopes:**
   - ✅ **repo** (semua)
     - Ini akan otomatis centang semua sub-options:
       - ✅ repo:status
       - ✅ repo_deployment
       - ✅ public_repo
       - ✅ repo:invite
       - ✅ security_events

4. **Scroll ke bawah, klik:** "Generate token"

---

### **STEP 4: Copy Token**

**⚠️ PENTING: Token hanya muncul sekali!**

1. **Copy token** yang muncul (contoh: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
2. **Simpan di tempat aman** (notepad, notes, dll)
3. **Jangan share** token ke sembarang orang!

---

### **STEP 5: Gunakan Token untuk Push**

**Buka terminal/command prompt, jalankan:**

```bash
git push -u origin main
```

**Saat diminta:**
- **Username:** `nyamiresepdapur-droid`
- **Password:** **Paste token yang sudah di-copy** (bukan password GitHub!)

---

## 🎯 ALTERNATIF: Setup Token di URL

**Jika tidak mau input setiap kali, bisa setup token langsung di URL:**

```bash
# Ganti YOUR_TOKEN dengan token yang sudah di-generate
git remote set-url origin https://YOUR_TOKEN@github.com/nyamiresepdapur-droid/affiliate-system.git

# Lalu push
git push -u origin main
```

**Contoh:**
```bash
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/nyamiresepdapur-droid/affiliate-system.git
git push -u origin main
```

---

## 🔐 KEAMANAN TOKEN

### **Jangan:**
- ❌ Commit token ke GitHub
- ❌ Share token ke sembarang orang
- ❌ Post token di public place

### **Lakukan:**
- ✅ Simpan token di tempat aman
- ✅ Gunakan token hanya untuk push/pull
- ✅ Revoke token jika tidak digunakan lagi

---

## 🚨 TROUBLESHOOTING

### **Problem: "Token tidak valid"**
- Pastikan token sudah di-copy dengan benar
- Pastikan token belum expired
- Generate token baru jika perlu

### **Problem: "Permission denied"**
- Pastikan scope "repo" sudah di-centang
- Pastikan token belum di-revoke
- Generate token baru dengan permission lengkap

### **Problem: "Authentication failed"**
- Pastikan username benar: `nyamiresepdapur-droid`
- Pastikan menggunakan token (bukan password)
- Coba generate token baru

---

## 📋 CHECKLIST

**Sebelum push:**
- [ ] Token sudah di-generate
- [ ] Token sudah di-copy
- [ ] Token disimpan di tempat aman
- [ ] Remote sudah di-connect
- [ ] Ready to push!

---

## 🎯 QUICK REFERENCE

**Generate Token:**
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. Centang "repo"
4. Generate & copy

**Push:**
```bash
git push -u origin main
# Username: nyamiresepdapur-droid
# Password: [paste token]
```

---

**Generate token sekarang dan push code! 🚀**


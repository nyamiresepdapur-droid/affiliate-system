# 🚀 PUSH KE GITHUB DENGAN TOKEN

**Cara termudah untuk push tanpa login via desktop**

---

## ⚡ LANGKAH CEPAT

### **1. Generate Token (5 menit)**

1. **Buka:** https://github.com/settings/tokens
2. **Klik:** "Generate new token" → "Generate new token (classic)"
3. **Isi:**
   - Note: `Affiliate System`
   - Expiration: `90 days`
   - Scopes: ✅ **repo** (semua)
4. **Klik:** "Generate token"
5. **Copy token** (contoh: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

---

### **2. Setup Token di Git (1 menit)**

**Jalankan di terminal:**

```bash
# Ganti YOUR_TOKEN dengan token yang sudah di-copy
git remote set-url origin https://YOUR_TOKEN@github.com/nyamiresepdapur-droid/affiliate-system.git
```

**Contoh:**
```bash
git remote set-url origin https://ghp_abc123xyz456@github.com/nyamiresepdapur-droid/affiliate-system.git
```

---

### **3. Push Code (1 menit)**

```bash
git push -u origin main
```

**Selesai! ✅ Code sudah ter-push ke GitHub**

---

## 🔄 UNTUK PUSH SELANJUTNYA

**Setelah setup token di URL, push selanjutnya cukup:**

```bash
git add .
git commit -m "Pesan commit"
git push
```

**Tidak perlu input username/password lagi!**

---

## ⚠️ PENTING

**Token di URL akan tersimpan di:**
- Windows: `.git/config` (file lokal)
- Tidak akan ter-commit ke GitHub (aman)

**Tapi tetap jangan share file `.git/config` ke sembarang orang!**

---

## 🎯 ALTERNATIF: Pakai Credential Helper

**Jika tidak mau token di URL:**

```bash
# Setup credential helper
git config --global credential.helper wincred

# Push (akan minta username & token sekali)
git push -u origin main
# Username: nyamiresepdapur-droid
# Password: [paste token]
```

**Token akan tersimpan di Windows Credential Manager**

---

## 📋 VERIFIKASI

**Setelah push berhasil:**

1. **Buka:** https://github.com/nyamiresepdapur-droid/affiliate-system
2. **Cek semua file** sudah ter-upload
3. **Cek commit** sudah muncul

---

**Generate token → Setup di URL → Push! 🚀**


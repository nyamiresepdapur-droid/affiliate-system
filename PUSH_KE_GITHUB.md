# 🚀 PUSH KE GITHUB - PERINTAH LENGKAP

**Cara push ke GitHub tanpa GitHub Desktop (langsung di terminal)**

---

## 📋 PERINTAH DASAR

### **1. Cek Status**
```bash
git status
```
**Fungsi:** Lihat file yang berubah atau belum di-commit

---

### **2. Add Semua File**
```bash
git add .
```
**Fungsi:** Tambahkan semua file yang berubah ke staging area

**Atau add file tertentu:**
```bash
git add nama_file.py
```

---

### **3. Commit**
```bash
git commit -m "Pesan commit Anda"
```
**Fungsi:** Simpan perubahan dengan pesan commit

**Contoh:**
```bash
git commit -m "Fix Railway deployment error"
```

---

### **4. Push ke GitHub**
```bash
git push origin main
```
**Fungsi:** Upload perubahan ke GitHub

**Jika pertama kali:**
```bash
git push -u origin main
```

---

## 🔐 JIKA PERLU LOGIN

**GitHub akan minta username dan password/token:**

1. **Username:** GitHub username Anda
2. **Password:** Gunakan **Personal Access Token** (bukan password GitHub)

**Cara generate token:**
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token
- Copy token dan gunakan sebagai password

---

## 📝 CONTOH LENGKAP

```bash
# 1. Cek status
git status

# 2. Add semua file
git add .

# 3. Commit dengan pesan
git commit -m "Update code untuk fix Railway error"

# 4. Push ke GitHub
git push origin main
```

---

## 🚨 JIKA ERROR

### **Error: "not a git repository"**
```bash
git init
git remote add origin https://github.com/nyamiresepdapur-droid/affiliate-system.git
```

### **Error: "fatal: Authentication failed"**
- Gunakan Personal Access Token sebagai password
- Bukan password GitHub biasa

### **Error: "Updates were rejected"**
```bash
git pull origin main
git push origin main
```

---

## ✅ CHECKLIST

- [ ] `git status` - Cek file yang berubah
- [ ] `git add .` - Add semua file
- [ ] `git commit -m "pesan"` - Commit dengan pesan
- [ ] `git push origin main` - Push ke GitHub

---

**Gunakan perintah di atas untuk push ke GitHub! 🚀**


# 🚀 SETUP GITHUB REPOSITORY

**Status:** Git repository sudah di-init dan commit selesai

---

## 📋 LANGKAH PUSH KE GITHUB

### **STEP 1: Buat Repository di GitHub**

1. **Buka:** https://github.com/new
2. **Isi:**
   - Repository name: `affiliate-system` (atau nama lain)
   - Description: "Affiliate Management System dengan Telegram Bot"
   - Visibility: **Private** (recommended) atau Public
   - **Jangan** centang "Initialize with README"
3. **Klik:** "Create repository"

---

### **STEP 2: Connect Local ke GitHub**

**Setelah repository dibuat, GitHub akan kasih instruksi. Jalankan:**

```bash
git remote add origin https://github.com/USERNAME/affiliate-system.git
git branch -M main
git push -u origin main
```

**Ganti `USERNAME` dengan username GitHub Anda**

---

### **STEP 3: Push ke GitHub**

**Jika sudah setup remote, jalankan:**

```bash
git push -u origin main
```

**Atau jika sudah pernah push:**

```bash
git push
```

---

## 🔐 KEAMANAN

### **File yang TIDAK di-push (sudah di .gitignore):**

- ✅ `.env` - Environment variables (token, secrets)
- ✅ `*.db` - Database files
- ✅ `__pycache__/` - Python cache
- ✅ `venv/` - Virtual environment

### **File yang AMAN di-push:**

- ✅ Source code (`.py`, `.html`, `.css`, `.js`)
- ✅ Documentation (`.md`)
- ✅ Configuration files (tanpa secrets)

---

## 📝 COMMIT MESSAGE

**Commit yang sudah dibuat:**
```
Add landing page and documentation
- Landing page dengan hero section, membership plans, features, FAQ
- Documentation untuk setup bot, commands, upgrade flow
- Plan website low budget dengan deployment strategy
```

---

## 🔄 UNTUK PUSH SELANJUTNYA

**Setelah setup remote, untuk push perubahan:**

```bash
# 1. Cek status
git status

# 2. Add file yang berubah
git add .

# 3. Commit
git commit -m "Deskripsi perubahan"

# 4. Push
git push
```

---

## ⚠️ PENTING

**Jangan push:**
- ❌ File `.env` (berisi token & secrets)
- ❌ Database files (`.db`)
- ❌ Virtual environment (`venv/`)

**File-file ini sudah di-ignore oleh `.gitignore`**

---

## 🎯 QUICK COMMANDS

```bash
# Cek status
git status

# Add semua file
git add .

# Commit
git commit -m "Pesan commit"

# Push
git push

# Cek remote
git remote -v
```

---

**Setup remote repository di GitHub dulu, lalu push! 🚀**


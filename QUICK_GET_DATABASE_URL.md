# ⚡ QUICK: AMBIL DATABASE_URL DARI SUPABASE

**Cara cepat untuk mendapatkan connection string**

---

## 🎯 LANGKAH CEPAT (2 MENIT)

### **1. Buka Supabase Dashboard**
```
https://supabase.com → Login → Pilih project
```

### **2. Buka Settings**
```
Settings (gear icon) → Database
```

### **3. Scroll ke "Connection string"**
```
Scroll ke bawah → Tab "URI"
```

### **4. Copy Connection String**
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

### **5. Ganti Password**
```
Ganti [YOUR-PASSWORD] dengan password yang dibuat saat create project
```

### **6. Copy Lengkap**
```
postgresql://postgres:MyPassword123@db.xxx.supabase.co:5432/postgres
```

---

## 📋 UNTUK RAILWAY

**Paste connection string lengkap ke Railway:**

1. **Railway** → Service → **Variables**
2. **Add Variable:**
   - Key: `DATABASE_URL`
   - Value: `postgresql://postgres:MyPassword123@db.xxx.supabase.co:5432/postgres`
3. **Save**

---

## ⚠️ PENTING

- **Password** = Password yang dibuat saat create project Supabase
- **Ganti** `[YOUR-PASSWORD]` dengan password asli
- **Jangan share** connection string ke public

---

**Lokasi di Supabase: Settings → Database → Connection string → Tab URI**


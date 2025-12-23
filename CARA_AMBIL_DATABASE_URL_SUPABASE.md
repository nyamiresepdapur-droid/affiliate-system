# 🔗 CARA AMBIL DATABASE_URL DARI SUPABASE

**Step-by-step untuk mendapatkan connection string**

---

## 🎯 LANGKAH LENGKAP

### **STEP 1: Buka Supabase Dashboard**

1. **Buka:** https://supabase.com
2. **Login** ke akun Anda
3. **Pilih project:** `affiliate-system` (atau nama project Anda)

---

### **STEP 2: Buka Project Settings**

1. **Klik icon "Settings"** (gear icon) di sidebar kiri
   - Atau klik: **"Project Settings"** di menu
2. **Pilih:** **"Database"** di menu settings

---

### **STEP 3: Cari Connection String**

1. **Scroll ke bawah** sampai bagian **"Connection string"**
2. **Anda akan lihat beberapa tab:**
   - **URI** ← **PILIH INI!**
   - Session mode
   - Transaction
   - Pooler

3. **Klik tab "URI"**

---

### **STEP 4: Copy Connection String**

**Anda akan lihat connection string seperti ini:**

```
postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**Atau format lain:**

```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

---

### **STEP 5: Ganti Password**

**⚠️ PENTING:** Connection string yang ditampilkan masih ada placeholder `[YOUR-PASSWORD]`

**Anda perlu:**
1. **Ganti `[YOUR-PASSWORD]`** dengan password yang Anda buat saat create project
2. **Password ini** adalah password yang Anda set saat membuat project Supabase

**Contoh:**
- **Sebelum:** `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`
- **Sesudah:** `postgresql://postgres:MySecurePass123!@#@db.xxx.supabase.co:5432/postgres`

---

### **STEP 6: Copy Connection String Lengkap**

**Setelah ganti password, copy seluruh connection string:**

```
postgresql://postgres:MySecurePass123!@#@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**⚠️ INI ADALAH DATABASE_URL YANG AKAN DI-PAKAI DI RAILWAY!**

---

## 📋 ALTERNATIF: CARA LAIN

### **Option 1: Via Connection Pooling (Recommended untuk Production)**

1. **Di Supabase, pilih tab:** **"Connection pooling"**
2. **Mode:** Transaction
3. **Copy connection string** dari sana
4. **Format:** `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`

**Keuntungan:** Lebih stabil untuk production, support connection pooling

---

### **Option 2: Via Connection Info**

1. **Di bagian "Connection info"** (atas)
2. **Anda akan lihat:**
   - Host
   - Database name
   - Port
   - User
   - Password (hidden, klik "Reveal" untuk lihat)

3. **Buat connection string manual:**
   ```
   postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres
   ```

---

## 🎯 CONTOH LENGKAP

**Connection string yang benar:**

```
postgresql://postgres:MySecurePassword123!@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**Komponen:**
- `postgres` = username
- `MySecurePassword123!` = password (ganti dengan password Anda)
- `db.abcdefghijklmnop.supabase.co` = host
- `5432` = port
- `postgres` = database name

---

## ⚠️ PENTING

### **Jangan:**
- ❌ Share connection string ke public
- ❌ Commit connection string ke GitHub
- ❌ Post di public place

### **Lakukan:**
- ✅ Simpan di Railway environment variables (aman)
- ✅ Simpan di tempat aman (password manager)
- ✅ Ganti password jika ter-expose

---

## 🔧 UNTUK RAILWAY

**Setelah dapat connection string:**

1. **Buka Railway dashboard**
2. **Klik service** yang sudah dibuat
3. **Tab "Variables"**
4. **Add Variable:**
   - **Key:** `DATABASE_URL`
   - **Value:** Paste connection string lengkap (yang sudah ganti password)
5. **Save**
6. **Railway akan auto-redeploy**

---

## 🚨 TROUBLESHOOTING

### **Problem: Password tidak tahu**
- Cek email saat create project (jika ada)
- Atau reset password di Supabase settings
- Atau buat project baru dengan password yang diingat

### **Problem: Connection string tidak work**
- Pastikan password sudah benar (tidak ada spasi)
- Pastikan format sudah benar (postgresql://...)
- Cek project status (harus "Active")

### **Problem: Tidak bisa connect**
- Cek firewall settings di Supabase
- Cek project status
- Cek connection string format

---

## 📋 CHECKLIST

- [ ] Supabase project sudah dibuat
- [ ] Password database sudah diketahui
- [ ] Buka Settings → Database
- [ ] Pilih tab "URI"
- [ ] Copy connection string
- [ ] Ganti [YOUR-PASSWORD] dengan password asli
- [ ] Copy connection string lengkap
- [ ] Paste ke Railway Variables sebagai DATABASE_URL

---

**Dapatkan connection string dari Supabase, lalu paste ke Railway! 🚀**


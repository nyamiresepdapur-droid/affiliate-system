# 🔗 DATABASE_URL UNTUK RAILWAY

**Password Supabase:** `1Milyarberkah$`

---

## 🎯 FORMAT CONNECTION STRING

**Format umum:**
```
postgresql://postgres:1Milyarberkah$@db.[PROJECT-REF].supabase.co:5432/postgres
```

**Atau dengan connection pooling:**
```
postgresql://postgres.[PROJECT-REF]:1Milyarberkah$@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

---

## 📋 CARA DAPATKAN HOST DARI SUPABASE

### **STEP 1: Buka Supabase Dashboard**

1. **Buka:** https://supabase.com
2. **Login** → Pilih project `affiliate-system`

---

### **STEP 2: Buka Settings → Database**

1. **Klik:** Settings (gear icon)
2. **Pilih:** Database
3. **Scroll ke:** "Connection string"

---

### **STEP 3: Copy Connection String**

1. **Pilih tab:** "URI"
2. **Anda akan lihat:**
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnop.supabase.co:5432/postgres
   ```

3. **Ganti `[YOUR-PASSWORD]`** dengan: `1Milyarberkah$`

4. **Hasil akhir:**
   ```
   postgresql://postgres:1Milyarberkah$@db.abcdefghijklmnop.supabase.co:5432/postgres
   ```

---

## ⚠️ PENTING: ENCODE PASSWORD

**Password mengandung karakter khusus (`$`), perlu di-encode untuk URL:**

**Password:** `1Milyarberkah$`

**URL Encoded:** `1Milyarberkah%24`

**Connection string yang benar:**
```
postgresql://postgres:1Milyarberkah%24@db.xxx.supabase.co:5432/postgres
```

**Atau jika Supabase sudah handle encoding, pakai langsung:**
```
postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres
```

---

## 🎯 UNTUK RAILWAY

**Setelah dapat connection string lengkap dari Supabase:**

1. **Railway** → Service → **Variables**
2. **Add Variable:**
   - **Key:** `DATABASE_URL`
   - **Value:** `postgresql://postgres:1Milyarberkah%24@db.xxx.supabase.co:5432/postgres`
     *(Ganti `xxx` dengan project reference dari Supabase)*
3. **Save**

---

## 🔧 ALTERNATIF: PAKAI CONNECTION POOLING

**Lebih stabil untuk production:**

1. **Di Supabase, pilih tab:** "Connection pooling"
2. **Mode:** Transaction
3. **Copy connection string**
4. **Ganti password:** `1Milyarberkah$` (atau `1Milyarberkah%24` jika perlu encode)

---

## 📋 CONTOH LENGKAP

**Jika project reference Anda:** `abcdefghijklmnop`

**Connection string:**
```
postgresql://postgres:1Milyarberkah%24@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**Atau tanpa encoding (coba dulu):**
```
postgresql://postgres:1Milyarberkah$@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## 🚨 TROUBLESHOOTING

### **Problem: Connection failed**
- Coba dengan password URL-encoded: `1Milyarberkah%24`
- Atau coba tanpa encoding: `1Milyarberkah$`
- Cek project status di Supabase (harus Active)

### **Problem: Password error**
- Pastikan password benar: `1Milyarberkah$`
- Cek apakah ada typo
- Coba reset password di Supabase jika perlu

---

## ⚠️ KEAMANAN

**Password sudah ter-expose di chat ini. Untuk keamanan:**

1. **Setelah deploy berhasil, pertimbangkan reset password** di Supabase
2. **Jangan commit** connection string ke GitHub
3. **Simpan** di Railway environment variables (aman)

---

**Ambil host dari Supabase, lalu buat connection string lengkap! 🚀**


# 🚀 CARA SETUP BOT TELEGRAM (SINGKAT)

**Untuk pemula yang mau cepat setup**

---

## ⚡ LANGKAH CEPAT (5 MENIT)

### **1. Buat Bot di Telegram**

1. Buka Telegram
2. Cari: **`BotFather`** (yang ada centang biru ✅)
3. Ketik: `/newbot`
4. Isi nama bot: `Affiliate Bot`
5. Isi username: `affiliate_bot_123` (harus unik, tambahkan angka)
6. **SALIN TOKEN** yang diberikan (contoh: `1234567890:ABC...`)

---

### **2. Setup Token di Backend**

1. Buka folder **`backend`**
2. **Buat file baru** dengan nama: **`.env`**
3. **Isi file dengan:**
   ```
   TELEGRAM_TOKEN=TOKEN_YANG_DISALIN_DARI_BOTFATHER
   ```
   
   **Contoh:**
   ```
   TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

4. **Simpan file**

---

### **3. Jalankan Backend**

1. **Buka Command Prompt** atau **PowerShell**
2. **Masuk ke folder backend:**
   ```
   cd D:\affiliate-system\backend
   ```
   
   *(Ganti path sesuai lokasi folder Anda)*

3. **Jalankan:**
   ```
   python app.py
   ```

4. **Tunggu sampai muncul:**
   ```
   ✅ Telegram bot started!
   * Running on http://127.0.0.1:5000
   ```

5. **Jangan tutup window ini!** (Bot harus tetap running)

---

### **4. Test Bot**

1. **Buka Telegram**
2. **Cari bot Anda** (nama yang Anda buat tadi)
3. **Klik bot** → Klik **"START"**
4. **Ketik:** `/start`

**Jika bot membalas, berarti berhasil! ✅**

---

## 📸 CONTOH STEP-BY-STEP DENGAN GAMBAR

### **Step 1: Buka BotFather**

```
Telegram → Search → "BotFather" → Klik
```

### **Step 2: Ketik /newbot**

```
Chat dengan BotFather → Ketik: /newbot
```

### **Step 3: Isi Nama Bot**

```
BotFather: "How are we going to call it?"
Anda ketik: Affiliate Management Bot
```

### **Step 4: Isi Username**

```
BotFather: "Choose a username"
Anda ketik: affiliate_management_bot
```

### **Step 5: Salin Token**

```
BotFather: "Use this token: 1234567890:ABC..."
Anda: SALIN token tersebut
```

### **Step 6: Buat File .env**

```
Buka folder backend
Buat file baru: .env
Isi: TELEGRAM_TOKEN=1234567890:ABC...
Simpan
```

### **Step 7: Jalankan Backend**

```
Buka Command Prompt
cd D:\affiliate-system\backend
python app.py
```

### **Step 8: Test Bot**

```
Buka Telegram
Cari bot Anda
Klik START
Ketik: /start
```

---

## ⚠️ YANG PERLU DIPERHATIKAN

### **1. Token Harus Benar**
- ✅ Copy-paste langsung dari BotFather
- ❌ Jangan ada spasi
- ❌ Jangan pakai tanda kutip

### **2. File .env Harus di Folder Backend**
```
affiliate-system/
  └── backend/
      ├── .env          ← File ini harus ada di sini
      ├── app.py
      └── telegram_bot.py
```

### **3. Backend Harus Running**
- Bot tidak akan bekerja jika backend tidak running
- Jangan tutup terminal/command prompt
- Jika error, baca pesan error di terminal

---

## 🔧 JIKA ADA MASALAH

### **Bot tidak merespon?**
1. Cek backend masih running? (lihat terminal)
2. Cek token di `.env` sudah benar?
3. Restart backend (Ctrl+C, lalu `python app.py` lagi)

### **Error "Token tidak valid"?**
1. Copy ulang token dari BotFather
2. Pastikan tidak ada spasi di token
3. Restart backend

### **Bot tidak muncul di Telegram?**
1. Cari dengan username (contoh: `@affiliate_management_bot`)
2. Atau cari dengan nama bot
3. Pastikan bot sudah dibuat di BotFather

---

## ✅ CHECKLIST

Sebelum mulai, pastikan:

- [ ] Bot sudah dibuat di BotFather
- [ ] Token sudah didapat
- [ ] File `.env` sudah dibuat di folder `backend`
- [ ] Token sudah diisi di file `.env`
- [ ] Backend sudah running
- [ ] Bot sudah di-test dengan `/start`

---

## 🎯 CONTOH FILE .env LENGKAP

**Buat file `backend/.env` dengan isi:**

```env
TELEGRAM_TOKEN=8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE
GROUP_CHAT_ID=-1003342536716
CHANNEL_CHAT_ID=-1003607323066
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=jwt-secret-key-change-this
```

**Minimal yang diperlukan:**
```env
TELEGRAM_TOKEN=TOKEN_DARI_BOTFATHER
```

---

## 📞 BUTUH BANTUAN LEBIH LANJUT?

**Baca panduan lengkap di:**
- `PANDUAN_SETUP_BOT_TELEGRAM.md` - Panduan detail step-by-step

**Atau cek:**
- Error message di terminal backend
- File `.env` sudah benar
- Token sudah valid (test di browser)

---

**Selamat setup bot! 🚀**


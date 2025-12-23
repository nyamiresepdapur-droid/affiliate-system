# 🤖 PANDUAN SETUP BOT TELEGRAM (UNTUK PEMULA)

**Tanggal:** 20 Desember 2025  
**Level:** Pemula/Awam

---

## 📋 DAFTAR ISI

1. [Membuat Bot di Telegram](#1-membuat-bot-di-telegram)
2. [Mendapatkan Bot Token](#2-mendapatkan-bot-token)
3. [Setup Bot di Backend](#3-setup-bot-di-backend)
4. [Test Bot](#4-test-bot)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. MEMBUAT BOT DI TELEGRAM

### **STEP 1: Buka Telegram**

1. Buka aplikasi **Telegram** di HP atau PC
2. Pastikan Anda sudah login dengan akun Telegram

---

### **STEP 2: Cari BotFather**

1. Di search bar Telegram, ketik: **`BotFather`**
2. Pilih akun **@BotFather** (yang ada centang biru ✅)
3. Klik untuk mulai chat

**Catatan:** BotFather adalah bot resmi dari Telegram untuk membuat bot

---

### **STEP 3: Mulai Chat dengan BotFather**

1. Klik tombol **"START"** atau ketik: `/start`

**BotFather akan membalas:**
```
Hello! I'm the BotFather. I can help you create and manage bots.

Use /newbot to create a new bot.
```

---

### **STEP 4: Buat Bot Baru**

**Ketik:** `/newbot`

**BotFather akan bertanya:**
```
Alright, a new bot. How are we going to call it? Please choose a name for your bot.
```

**Anda ketik nama bot:** `Affiliate Management Bot`

*(Nama ini akan muncul di chat list, bisa diubah nanti)*

**BotFather akan bertanya lagi:**
```
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
```

**Anda ketik username bot:** `affiliate_management_bot`

*(Username harus unik, jika sudah dipakai coba nama lain)*

**Contoh username yang valid:**
- `affiliate_management_bot` ✅
- `my_affiliate_bot` ✅
- `affiliatebot123` ✅

**Contoh username yang tidak valid:**
- `affiliate bot` ❌ (ada spasi)
- `affiliatebot` ❌ (tidak ada underscore, tapi sebenarnya bisa)
- `affiliate` ❌ (tidak ada kata "bot" di akhir)

---

### **STEP 5: Dapatkan Bot Token**

**Setelah berhasil, BotFather akan membalas:**
```
Done! Congratulations on your new bot. You will find it at t.me/affiliate_management_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

**⚠️ PENTING:** Salin token yang diberikan (contoh: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Token ini seperti password bot Anda, jangan share ke sembarang orang!**

---

## 2. MENDAPATKAN BOT TOKEN

### **STEP 1: Salin Token**

1. **Highlight** token yang diberikan BotFather
2. **Copy** token tersebut (Ctrl+C atau long press di HP)
3. **Simpan** di tempat yang aman (notepad, notes, dll)

**Format token biasanya seperti ini:**
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

---

### **STEP 2: (Opsional) Set Bot Description**

**Ketik ke BotFather:** `/setdescription`

**Pilih bot Anda, lalu ketik description:**
```
Bot untuk manage affiliate system. Daftar, beli membership, dan lapor kinerja via bot ini.
```

---

### **STEP 3: (Opsional) Set Bot About**

**Ketik ke BotFather:** `/setabouttext`

**Pilih bot Anda, lalu ketik about:**
```
Affiliate Management Bot - Daftar, beli membership, dan lapor kinerja harian
```

---

## 3. SETUP BOT DI BACKEND

### **STEP 1: Buka File .env**

1. Buka folder **`backend`** di project Anda
2. Cari file **`.env`** (jika tidak ada, buat file baru dengan nama `.env`)
3. Buka file tersebut dengan text editor (Notepad, VS Code, dll)

---

### **STEP 2: Tambahkan Bot Token**

**Tambahkan baris berikut di file `.env`:**

```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Ganti `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` dengan token yang Anda dapat dari BotFather**

**Contoh:**
```env
TELEGRAM_TOKEN=8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE
```

**⚠️ PENTING:**
- Jangan ada spasi sebelum/sesudah `=`
- Jangan pakai tanda kutip (`"` atau `'`)
- Pastikan token benar (copy-paste dari BotFather)

---

### **STEP 3: (Opsional) Set Group Chat ID**

**Jika Anda punya group Telegram untuk admin:**

1. **Tambahkan bot ke group** (cari bot Anda, klik "Add to Group")
2. **Kirim pesan di group** (bisa pesan apa saja)
3. **Buka browser**, ketik URL berikut (ganti `BOT_TOKEN` dengan token Anda):
   ```
   https://api.telegram.org/botBOT_TOKEN/getUpdates
   ```

   **Contoh:**
   ```
   https://api.telegram.org/bot8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE/getUpdates
   ```

4. **Cari `"chat":{"id"`** di hasil JSON
5. **Salin ID** (biasanya angka negatif, contoh: `-1003342536716`)

6. **Tambahkan di file `.env`:**
   ```env
   GROUP_CHAT_ID=-1003342536716
   ```

**Jika tidak punya group, skip step ini**

---

### **STEP 4: Cek File .env**

**File `.env` Anda seharusnya seperti ini:**

```env
TELEGRAM_TOKEN=8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE
GROUP_CHAT_ID=-1003342536716
CHANNEL_CHAT_ID=-1003607323066
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=jwt-secret-key-change-this
```

**Minimal yang diperlukan:**
- `TELEGRAM_TOKEN` ✅ (WAJIB)

**Opsional:**
- `GROUP_CHAT_ID` (untuk notifikasi ke group)
- `CHANNEL_CHAT_ID` (untuk notifikasi ke channel)

---

## 4. TEST BOT

### **STEP 1: Pastikan Backend Running**

1. **Buka terminal/command prompt**
2. **Masuk ke folder backend:**
   ```bash
   cd backend
   ```

3. **Jalankan backend:**
   ```bash
   python app.py
   ```

**Jika berhasil, Anda akan lihat:**
```
✅ Database schema created/verified
✅ Response compression enabled
✅ Rate limiting enabled
✅ Telegram bot started!
 * Running on http://127.0.0.1:5000
```

**⚠️ Jangan tutup terminal ini!** Bot harus tetap running.

---

### **STEP 2: Test Bot di Telegram**

1. **Buka Telegram**
2. **Cari bot Anda** (nama bot yang Anda buat tadi)
3. **Klik bot** untuk mulai chat
4. **Klik "START"** atau ketik: `/start`

**Bot harus membalas:**
```
👋 Halo [Nama Anda]!

Selamat datang di Affiliate Management Bot!

📋 Perintah yang tersedia:
/daftar - Daftar sebagai member baru
/beli - Beli membership (Basic/VIP)
...
```

**✅ Jika bot membalas, berarti setup berhasil!**

---

### **STEP 3: Test Command**

**Coba beberapa command:**

1. **Ketik:** `/help`
   - Bot harus membalas dengan list commands

2. **Ketik:** `/daftar`
   - Bot harus mulai proses registrasi

**Jika bot tidak merespon:**
- Cek apakah backend masih running
- Cek token di file `.env` sudah benar
- Restart backend (Ctrl+C, lalu jalankan lagi `python app.py`)

---

## 5. TROUBLESHOOTING

### **Problem 1: Bot tidak merespon**

**Cek:**
1. ✅ Backend masih running? (lihat terminal)
2. ✅ Token di `.env` sudah benar?
3. ✅ Bot sudah di-start? (kirim `/start`)

**Solusi:**
- Restart backend: Tekan `Ctrl+C` di terminal, lalu jalankan lagi `python app.py`
- Cek token: Pastikan token di `.env` sama dengan token dari BotFather
- Test token: Buka browser, ketik:
  ```
  https://api.telegram.org/botTOKEN_ANDA/getMe
  ```
  *(Ganti TOKEN_ANDA dengan token Anda)*
  
  Jika muncul info bot, berarti token valid ✅

---

### **Problem 2: Error "Token tidak valid"**

**Penyebab:**
- Token salah
- Token sudah expired (jarang terjadi)
- Ada spasi/karakter tidak valid di token

**Solusi:**
1. **Copy ulang token** dari BotFather
2. **Hapus token lama** di file `.env`
3. **Paste token baru** (tanpa spasi)
4. **Restart backend**

---

### **Problem 3: Bot tidak muncul di Telegram**

**Cek:**
1. ✅ Bot sudah dibuat di BotFather?
2. ✅ Username bot sudah benar?

**Solusi:**
1. **Cari bot dengan username** (contoh: `@affiliate_management_bot`)
2. **Atau cari dengan nama bot** (contoh: "Affiliate Management Bot")
3. **Jika tidak ketemu**, buat bot baru di BotFather

---

### **Problem 4: Backend error saat start**

**Cek error message di terminal:**

**Jika error: "Module not found"**
```bash
pip install python-telegram-bot
```

**Jika error: "Token required"**
- Pastikan file `.env` ada di folder `backend`
- Pastikan token sudah diisi di `.env`

**Jika error lain:**
- Copy error message
- Cek apakah semua dependencies sudah terinstall:
  ```bash
  pip install -r requirements.txt
  ```

---

### **Problem 5: Bot merespon tapi command tidak bekerja**

**Cek:**
1. ✅ Backend sudah restart setelah update code?
2. ✅ File `telegram_bot.py` sudah di-update?

**Solusi:**
- **Restart backend** (Ctrl+C, lalu `python app.py` lagi)
- **Cek log di terminal** untuk melihat error

---

## 📝 CHECKLIST SETUP

**Sebelum mulai, pastikan:**

- [ ] Bot sudah dibuat di BotFather
- [ ] Token sudah didapat dari BotFather
- [ ] Token sudah ditambahkan di file `.env`
- [ ] Backend sudah running (`python app.py`)
- [ ] Bot sudah di-test dengan `/start`
- [ ] Bot merespon dengan benar

---

## 🎯 QUICK START (TL;DR)

**Untuk yang mau cepat:**

1. **Buka Telegram → Cari BotFather → Ketik `/newbot`**
2. **Isi nama bot → Isi username bot → Dapat token**
3. **Buka file `backend/.env` → Tambahkan:**
   ```
   TELEGRAM_TOKEN=TOKEN_DARI_BOTFATHER
   ```
4. **Jalankan backend:**
   ```bash
   cd backend
   python app.py
   ```
5. **Test bot di Telegram: Ketik `/start`**

**Selesai! ✅**

---

## 📞 BUTUH BANTUAN?

**Jika masih bingung:**

1. **Cek error message** di terminal backend
2. **Cek file `.env`** sudah benar
3. **Test token** di browser (lihat Problem 1)
4. **Restart backend** dan coba lagi

**Tips:**
- Jangan panik jika ada error
- Baca error message dengan teliti
- Pastikan semua step sudah dilakukan
- Bot harus tetap running di terminal

---

## 🎉 SELAMAT!

**Jika bot sudah merespon `/start`, berarti setup berhasil!**

**Lanjutkan dengan:**
- Test command `/daftar`
- Test command `/beli`
- Test sebagai admin dengan `/admin`

**Selamat menggunakan bot! 🚀**


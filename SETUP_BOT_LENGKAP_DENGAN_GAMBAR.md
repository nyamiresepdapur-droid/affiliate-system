# 📱 SETUP BOT TELEGRAM - PANDUAN LENGKAP DENGAN CONTOH

**Untuk pemula yang belum pernah setup bot**

---

## 🎯 TUJUAN

Setup bot Telegram agar bisa digunakan untuk:
- User daftar via bot
- User beli membership via bot
- User lapor kinerja via bot
- Admin verify payment via bot

---

## 📋 PERSIAPAN

**Yang dibutuhkan:**
1. ✅ Akun Telegram (sudah punya)
2. ✅ Aplikasi Telegram (HP atau PC)
3. ✅ Akses ke folder `backend` di project
4. ✅ Text editor (Notepad, VS Code, dll)

---

## 🚀 LANGKAH 1: BUAT BOT DI TELEGRAM

### **1.1. Buka Telegram**

1. Buka aplikasi **Telegram** di HP atau PC
2. Pastikan sudah login

---

### **1.2. Cari BotFather**

1. Di **search bar** Telegram (atas), ketik: **`BotFather`**
2. Pilih akun **@BotFather** yang ada **centang biru** ✅
3. Klik untuk mulai chat

**Catatan:** BotFather adalah bot resmi Telegram untuk membuat bot

---

### **1.3. Mulai Chat dengan BotFather**

1. Klik tombol **"START"** di chat BotFather
   - Atau ketik: `/start`

**BotFather akan membalas:**
```
Hello! I'm the BotFather. I can help you create and manage bots.

Use /newbot to create a new bot.
```

---

### **1.4. Buat Bot Baru**

**Ketik:** `/newbot`

*(Tidak perlu pakai tanda kutip, langsung ketik `/newbot`)*

**BotFather akan bertanya:**
```
Alright, a new bot. How are we going to call it? Please choose a name for your bot.
```

**Anda ketik nama bot:** 
```
Affiliate Management Bot
```

*(Nama ini akan muncul di chat list user, bisa diubah nanti)*

**BotFather akan bertanya lagi:**
```
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
```

**Anda ketik username bot:** 
```
affiliate_management_bot
```

**⚠️ PENTING:**
- Username harus **unik** (tidak boleh sama dengan bot lain)
- Jika sudah dipakai, coba tambahkan angka: `affiliate_bot_123`
- Username tidak bisa diubah setelah dibuat

**Contoh username yang valid:**
- ✅ `affiliate_management_bot`
- ✅ `my_affiliate_bot`
- ✅ `affiliatebot123`
- ✅ `affiliate_bot_2025`

**Contoh username yang tidak valid:**
- ❌ `affiliate bot` (ada spasi)
- ❌ `affiliate` (tidak ada kata "bot")

---

### **1.5. Dapatkan Token**

**Setelah berhasil, BotFather akan membalas:**
```
Done! Congratulations on your new bot. You will find it at t.me/affiliate_management_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

**⚠️ PENTING: SALIN TOKEN INI!**

**Cara salin:**
1. **Highlight** token (contoh: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890`)
2. **Copy** (Ctrl+C di PC, atau long press di HP → Copy)
3. **Simpan** di notepad atau notes sementara

**Token ini seperti password bot, jangan share ke sembarang orang!**

---

## 🔧 LANGKAH 2: SETUP TOKEN DI BACKEND

### **2.1. Buka Folder Backend**

1. Buka **File Explorer** (Windows Explorer)
2. Masuk ke folder project: `D:\affiliate-system\backend`
3. Atau buka dengan text editor (VS Code, Notepad++, dll)

---

### **2.2. Buat File .env**

**Cara 1: Via File Explorer**
1. Di folder `backend`, klik kanan → **New** → **Text Document**
2. **Rename** file menjadi: **`.env`**
   - **⚠️ PENTING:** Hapus ekstensi `.txt`
   - Jika Windows minta konfirmasi, klik **Yes**
3. Buka file `.env` dengan Notepad atau text editor

**Cara 2: Via VS Code**
1. Buka folder `backend` di VS Code
2. Klik icon **"New File"** (atau Ctrl+N)
3. Simpan dengan nama: **`.env`**

**Cara 3: Via Command Prompt**
1. Buka Command Prompt
2. Masuk ke folder backend:
   ```
   cd D:\affiliate-system\backend
   ```
3. Buat file:
   ```
   echo. > .env
   ```

---

### **2.3. Isi File .env**

**Buka file `.env` yang sudah dibuat, lalu isi dengan:**

```env
TELEGRAM_TOKEN=TOKEN_YANG_DISALIN_DARI_BOTFATHER
```

**Ganti `TOKEN_YANG_DISALIN_DARI_BOTFATHER` dengan token yang Anda salin dari BotFather**

**Contoh:**
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

**⚠️ PENTING:**
- Jangan ada **spasi** sebelum/sesudah `=`
- Jangan pakai **tanda kutip** (`"` atau `'`)
- **Copy-paste langsung** dari BotFather (jangan ketik manual)

**File `.env` lengkap (opsional):**
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
GROUP_CHAT_ID=-1003342536716
CHANNEL_CHAT_ID=-1003607323066
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=jwt-secret-key-change-this
```

**Minimal yang diperlukan:**
- `TELEGRAM_TOKEN` ✅ (WAJIB)

**Lainnya opsional** (bisa ditambahkan nanti)

---

### **2.4. Simpan File**

1. **Simpan file** (Ctrl+S)
2. **Pastikan nama file:** `.env` (bukan `.env.txt`)
3. **Pastikan lokasi:** Di folder `backend`

**Struktur folder seharusnya:**
```
affiliate-system/
  └── backend/
      ├── .env          ← File ini harus ada di sini
      ├── app.py
      ├── telegram_bot.py
      └── ...
```

---

## ▶️ LANGKAH 3: JALANKAN BACKEND

### **3.1. Buka Command Prompt atau PowerShell**

**Cara 1: Via Start Menu**
1. Tekan **Windows key**
2. Ketik: **"Command Prompt"** atau **"PowerShell"**
3. Klik untuk buka

**Cara 2: Via File Explorer**
1. Buka folder `backend`
2. Klik kanan di folder kosong → **Open in Terminal** (jika ada)
3. Atau ketik `cmd` di address bar, tekan Enter

---

### **3.2. Masuk ke Folder Backend**

**Di Command Prompt, ketik:**
```bash
cd D:\affiliate-system\backend
```

**Tekan Enter**

**Jika berhasil, Anda akan lihat:**
```
D:\affiliate-system\backend>
```

---

### **3.3. Jalankan Backend**

**Ketik:**
```bash
python app.py
```

**Tekan Enter**

**Jika berhasil, Anda akan lihat:**
```
✅ Database schema created/verified
✅ Response compression enabled
✅ Rate limiting enabled
✅ Telegram bot started!
 * Running on http://127.0.0.1:5000
```

**⚠️ PENTING:**
- **Jangan tutup window ini!** Bot harus tetap running
- Jika ada error, baca pesan error dan perbaiki
- Jika perlu stop, tekan `Ctrl+C`

---

### **3.4. Jika Error "python tidak dikenali"**

**Ini berarti Python belum terinstall atau belum di PATH**

**Solusi:**
1. **Install Python** dari python.org
2. Atau gunakan **Python yang sudah ada:**
   ```bash
   py app.py
   ```
   atau
   ```bash
   python3 app.py
   ```

---

## ✅ LANGKAH 4: TEST BOT

### **4.1. Buka Telegram**

1. Buka aplikasi **Telegram**
2. Pastikan masih login

---

### **4.2. Cari Bot Anda**

**Cara 1: Via Username**
1. Di search bar, ketik: **`@affiliate_management_bot`**
   *(Ganti dengan username bot yang Anda buat)*
2. Klik bot yang muncul

**Cara 2: Via Nama**
1. Di search bar, ketik: **"Affiliate Management Bot"**
   *(Ganti dengan nama bot yang Anda buat)*
2. Klik bot yang muncul

---

### **4.3. Mulai Chat dengan Bot**

1. **Klik bot** untuk mulai chat
2. **Klik tombol "START"** (jika ada)
   - Atau ketik: `/start`

**Bot harus membalas:**
```
👋 Halo [Nama Anda]!

Selamat datang di Affiliate Management Bot!

📋 Perintah yang tersedia:
/daftar - Daftar sebagai member baru
/beli - Beli membership (Basic/VIP)
/upgrade - Upgrade ke VIP
/lapor - Lapor kinerja
/komisi - Cek komisi
/pembayaran - Cek pembayaran
/akun - Cek info akun TikTok affiliate (VIP only)
/help - Bantuan
```

**✅ Jika bot membalas seperti ini, berarti setup berhasil!**

---

### **4.4. Test Command Lain**

**Coba beberapa command:**

1. **Ketik:** `/help`
   - Bot harus membalas dengan list commands

2. **Ketik:** `/daftar`
   - Bot harus mulai proses registrasi

**Jika bot tidak merespon:**
- Cek apakah backend masih running (lihat terminal)
- Cek token di file `.env` sudah benar
- Restart backend (Ctrl+C, lalu `python app.py` lagi)

---

## 🔍 VERIFIKASI SETUP

### **Checklist:**

- [ ] Bot sudah dibuat di BotFather
- [ ] Token sudah didapat dari BotFather
- [ ] File `.env` sudah dibuat di folder `backend`
- [ ] Token sudah diisi di file `.env` (tanpa spasi, tanpa tanda kutip)
- [ ] Backend sudah running (`python app.py`)
- [ ] Bot sudah di-test dengan `/start`
- [ ] Bot merespon dengan benar

**Jika semua checklist ✅, berarti setup berhasil!**

---

## ⚠️ TROUBLESHOOTING

### **Problem 1: Bot tidak merespon**

**Cek:**
1. ✅ Backend masih running? (lihat terminal, harus ada "Running on...")
2. ✅ Token di `.env` sudah benar? (copy-paste dari BotFather)
3. ✅ Bot sudah di-start? (kirim `/start`)

**Solusi:**
- **Restart backend:** Tekan `Ctrl+C` di terminal, lalu jalankan lagi `python app.py`
- **Cek token:** Buka file `.env`, pastikan token benar
- **Test token:** Buka browser, ketik:
  ```
  https://api.telegram.org/botTOKEN_ANDA/getMe
  ```
  *(Ganti TOKEN_ANDA dengan token Anda)*
  
  Jika muncul info bot, berarti token valid ✅

---

### **Problem 2: Error "Token tidak valid"**

**Penyebab:**
- Token salah (typo)
- Token sudah expired (jarang)
- Ada spasi/karakter tidak valid

**Solusi:**
1. **Copy ulang token** dari BotFather
2. **Hapus token lama** di file `.env`
3. **Paste token baru** (tanpa spasi, tanpa tanda kutip)
4. **Simpan file**
5. **Restart backend**

---

### **Problem 3: File .env tidak ditemukan**

**Cek:**
1. ✅ File `.env` ada di folder `backend`?
2. ✅ Nama file benar: `.env` (bukan `.env.txt`)?

**Solusi:**
1. **Buat file baru** dengan nama `.env`
2. **Pastikan tidak ada ekstensi** (bukan `.env.txt`)
3. **Isi dengan token**

**Cara cek:**
- Di File Explorer, klik **View** → **Show** → **File name extensions**
- Lihat apakah file bernama `.env` atau `.env.txt`

---

### **Problem 4: Backend error saat start**

**Cek error message di terminal:**

**Jika error: "Module not found: telegram"**
```bash
pip install python-telegram-bot
```

**Jika error: "TELEGRAM_TOKEN not found"**
- Pastikan file `.env` ada di folder `backend`
- Pastikan token sudah diisi di `.env`

**Jika error lain:**
- Copy error message
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

### **Problem 5: Bot tidak muncul di Telegram**

**Cek:**
1. ✅ Bot sudah dibuat di BotFather?
2. ✅ Username bot sudah benar?

**Solusi:**
1. **Cari bot dengan username** (contoh: `@affiliate_management_bot`)
2. **Atau cari dengan nama bot** (contoh: "Affiliate Management Bot")
3. **Jika tidak ketemu**, buat bot baru di BotFather

---

## 📸 CONTOH FILE .env

**File `backend/.env` harus seperti ini:**

```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

**Atau lengkap:**
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
GROUP_CHAT_ID=-1003342536716
CHANNEL_CHAT_ID=-1003607323066
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=jwt-secret-key-change-this
```

**⚠️ Jangan ada:**
- ❌ Spasi sebelum/sesudah `=`
- ❌ Tanda kutip (`"` atau `'`)
- ❌ Komentar di baris yang sama

---

## 🎯 QUICK REFERENCE

**Langkah singkat:**
1. BotFather → `/newbot` → Isi nama & username → Salin token
2. Buat file `backend/.env` → Isi `TELEGRAM_TOKEN=TOKEN`
3. Jalankan: `python app.py`
4. Test: Telegram → Cari bot → `/start`

**Selesai! ✅**

---

## 📞 BUTUH BANTUAN?

**Jika masih bingung:**

1. **Baca error message** di terminal dengan teliti
2. **Cek file `.env`** sudah benar
3. **Test token** di browser (lihat Problem 1)
4. **Restart backend** dan coba lagi

**Tips:**
- Jangan panik jika ada error
- Baca error message dengan teliti
- Pastikan semua step sudah dilakukan
- Bot harus tetap running di terminal

---

**Selamat setup bot! 🚀**


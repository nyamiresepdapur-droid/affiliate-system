# ⚙️ PANDUAN SETUP COMMANDS BOT TELEGRAM

**Tanggal:** 20 Desember 2025  
**Untuk:** Bot yang sudah running, perlu setup commands

---

## 🎯 TUJUAN

Setup commands di bot Telegram agar user bisa lihat list commands dengan mudah (muncul di menu bot)

---

## 📋 LANGKAH 1: SETUP COMMANDS DI BOTFATHER

### **STEP 1: Buka BotFather**

1. Buka Telegram
2. Cari: **`BotFather`**
3. Klik untuk mulai chat

---

### **STEP 2: Set Bot Commands**

**Ketik ke BotFather:**
```
/setcommands
```

**BotFather akan bertanya:**
```
Select a bot to change the list of commands.
```

**Pilih bot Anda** (klik nama bot yang Anda buat)

**BotFather akan bertanya:**
```
OK. Send me a list of commands for your bot. Please use this format:

command1 - Description
command2 - Description
```

---

### **STEP 3: Kirim List Commands**

**Copy-paste list commands berikut ke BotFather:**

```
start - Mulai bot dan lihat menu utama
help - Lihat bantuan dan semua commands
daftar - Daftar sebagai member baru dan beli membership
beli - Beli membership (Basic Rp 97k / VIP Rp 299k)
upgrade - Upgrade dari Basic ke VIP Member
lapor - Lapor kinerja harian (kirim link video)
komisi - Cek total komisi Anda
pembayaran - Cek status pembayaran membership
akun - Cek info akun TikTok affiliate (VIP only)
```

**⚠️ PENTING:**
- Copy-paste **persis** seperti di atas
- Jangan ubah format
- Setiap command di baris baru
- Format: `command - Description`

---

### **STEP 4: Konfirmasi**

**Setelah kirim, BotFather akan membalas:**
```
Success! The list of commands has been updated. /help
```

**✅ Commands sudah ter-setup!**

---

## 📋 LANGKAH 2: SETUP ADMIN COMMANDS (OPSIONAL)

**Jika Anda ingin admin commands juga muncul di menu:**

**Ketik ke BotFather:**
```
/setcommands
```

**Pilih bot Anda, lalu kirim:**

```
start - Mulai bot dan lihat menu utama
help - Lihat bantuan dan semua commands
daftar - Daftar sebagai member baru dan beli membership
beli - Beli membership (Basic Rp 97k / VIP Rp 299k)
upgrade - Upgrade dari Basic ke VIP Member
lapor - Lapor kinerja harian (kirim link video)
komisi - Cek total komisi Anda
pembayaran - Cek status pembayaran membership
akun - Cek info akun TikTok affiliate (VIP only)
admin - Menu admin (owner only)
pending-payments - List pending payments (admin only)
verify-payment - Verify payment (admin only)
reject-payment - Reject payment (admin only)
pending - List pending reports (admin only)
approve - Approve report (admin only)
reject - Reject report (admin only)
users - List semua users (admin only)
stats - Statistik sistem (admin only)
```

**Catatan:** Admin commands tetap bisa dipakai meskipun tidak muncul di menu (user biasa tidak akan lihat)

---

## 📋 LANGKAH 3: VERIFIKASI COMMANDS

### **STEP 1: Test di Telegram**

1. **Buka bot Anda** di Telegram
2. **Klik icon keyboard** (jika ada) atau ketik `/`
3. **List commands akan muncul** di keyboard/suggestion

**Atau:**

1. **Ketik:** `/help`
2. **Bot akan menampilkan** semua commands yang tersedia

---

### **STEP 2: Test Setiap Command**

**Test command satu per satu:**

1. **`/start`** - Harus muncul welcome message
2. **`/help`** - Harus muncul list commands
3. **`/daftar`** - Harus mulai proses registrasi
4. **`/beli`** - Harus muncul pilihan membership
5. **`/upgrade`** - Harus muncul info upgrade
6. **`/lapor`** - Harus mulai proses lapor
7. **`/komisi`** - Harus menampilkan komisi (jika sudah terdaftar)
8. **`/pembayaran`** - Harus menampilkan status pembayaran
9. **`/akun`** - Harus menampilkan info akun (VIP only)

---

## 📋 DAFTAR COMMANDS LENGKAP

### **USER COMMANDS (Untuk Semua User)**

| Command | Deskripsi | Cara Pakai |
|---------|-----------|------------|
| `/start` | Mulai bot dan lihat menu utama | Ketik: `/start` |
| `/help` | Lihat bantuan dan semua commands | Ketik: `/help` |
| `/daftar` | Daftar sebagai member baru | Ketik: `/daftar` → Isi data → Pilih membership → Upload bukti |
| `/beli` | Beli membership (Basic/VIP) | Ketik: `/beli` → Pilih membership → Upload bukti |
| `/upgrade` | Upgrade dari Basic ke VIP | Ketik: `/upgrade` → Confirm → Upload bukti |
| `/lapor` | Lapor kinerja harian | Ketik: `/lapor` → Kirim link → Ketik "selesai" → Isi tanggal & akun |
| `/komisi` | Cek total komisi | Ketik: `/komisi` |
| `/pembayaran` | Cek status pembayaran | Ketik: `/pembayaran` |
| `/akun` | Cek info akun TikTok (VIP only) | Ketik: `/akun` |

---

### **ADMIN COMMANDS (Untuk Owner/Admin)**

| Command | Deskripsi | Cara Pakai |
|---------|-----------|------------|
| `/admin` | Menu admin | Ketik: `/admin` |
| `/pending-payments` | List pending payments | Ketik: `/pending-payments` |
| `/verify-payment <id>` | Verify payment | Ketik: `/verify-payment 123456789` |
| `/reject-payment <id> <alasan>` | Reject payment | Ketik: `/reject-payment 123456789 Bukti tidak jelas` |
| `/pending` | List pending reports | Ketik: `/pending` |
| `/approve <id>` | Approve report | Ketik: `/approve 123` |
| `/reject <id> <alasan>` | Reject report | Ketik: `/reject 123 Link tidak valid` |
| `/reports` | List semua reports | Ketik: `/reports` |
| `/users` | List semua users | Ketik: `/users` |
| `/stats` | Statistik sistem | Ketik: `/stats` |

---

## 🔧 SETUP COMMANDS VIA API (ALTERNATIF)

**Jika BotFather tidak bisa, bisa setup via API:**

### **STEP 1: Dapatkan Bot Token**

- Token dari BotFather (sudah ada)

### **STEP 2: Setup Commands via Browser**

**Buka browser, ketik URL berikut (ganti `BOT_TOKEN` dengan token Anda):**

```
https://api.telegram.org/botBOT_TOKEN/setMyCommands?commands=[{"command":"start","description":"Mulai bot dan lihat menu utama"},{"command":"help","description":"Lihat bantuan dan semua commands"},{"command":"daftar","description":"Daftar sebagai member baru dan beli membership"},{"command":"beli","description":"Beli membership (Basic Rp 97k / VIP Rp 299k)"},{"command":"upgrade","description":"Upgrade dari Basic ke VIP Member"},{"command":"lapor","description":"Lapor kinerja harian (kirim link video)"},{"command":"komisi","description":"Cek total komisi Anda"},{"command":"pembayaran","description":"Cek status pembayaran membership"},{"command":"akun","description":"Cek info akun TikTok affiliate (VIP only)"}]
```

**Contoh dengan token:**
```
https://api.telegram.org/bot8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE/setMyCommands?commands=[{"command":"start","description":"Mulai bot"},{"command":"help","description":"Bantuan"}]
```

**Jika berhasil, akan muncul:**
```json
{"ok":true,"result":true}
```

---

## 📋 LANGKAH 4: SETUP BOT DESCRIPTION (OPSIONAL)

### **STEP 1: Set Description**

**Ketik ke BotFather:**
```
/setdescription
```

**Pilih bot Anda, lalu ketik description:**
```
Bot untuk manage affiliate system. Daftar, beli membership, dan lapor kinerja via bot ini.
```

---

### **STEP 2: Set About Text**

**Ketik ke BotFather:**
```
/setabouttext
```

**Pilih bot Anda, lalu ketik about:**
```
Affiliate Management Bot - Daftar, beli membership, dan lapor kinerja harian. Dapat komisi 55% untuk VIP Member!
```

---

### **STEP 3: Set Bot Picture (Opsional)**

**Ketik ke BotFather:**
```
/setuserpic
```

**Pilih bot Anda, lalu kirim foto** (logo/icon bot)

---

## 📋 LANGKAH 5: TEST SEMUA COMMANDS

### **Test User Commands:**

1. **`/start`**
   - ✅ Harus muncul welcome message

2. **`/help`**
   - ✅ Harus muncul list commands

3. **`/daftar`**
   - ✅ Harus mulai proses registrasi
   - ✅ Minta nama lengkap

4. **`/beli`**
   - ✅ Harus muncul pilihan membership
   - ✅ Ada tombol Basic & VIP

5. **`/upgrade`**
   - ✅ Harus muncul info upgrade
   - ✅ Ada tombol confirm

6. **`/lapor`**
   - ✅ Harus mulai proses lapor
   - ✅ Minta link video

7. **`/komisi`**
   - ✅ Harus menampilkan komisi (atau pesan belum terdaftar)

8. **`/pembayaran`**
   - ✅ Harus menampilkan status pembayaran

9. **`/akun`**
   - ✅ Harus menampilkan info akun (atau pesan belum VIP)

---

### **Test Admin Commands (Sebagai Owner):**

1. **`/admin`**
   - ✅ Harus muncul menu admin

2. **`/pending-payments`**
   - ✅ Harus menampilkan list pending payments

3. **`/verify-payment 123456789`**
   - ✅ Harus verify payment (jika ada)

4. **`/pending`**
   - ✅ Harus menampilkan list pending reports

5. **`/approve 123`**
   - ✅ Harus approve report (jika ada)

6. **`/users`**
   - ✅ Harus menampilkan list users

7. **`/stats`**
   - ✅ Harus menampilkan statistik

---

## 🔍 VERIFIKASI COMMANDS DI TELEGRAM

### **Cara 1: Via Keyboard**

1. **Buka bot** di Telegram
2. **Klik icon keyboard** (jika ada)
3. **List commands akan muncul**

### **Cara 2: Via Slash Command**

1. **Ketik:** `/`
2. **List commands akan muncul** di suggestion

### **Cara 3: Via /help**

1. **Ketik:** `/help`
2. **Bot akan menampilkan** semua commands

---

## ⚠️ TROUBLESHOOTING

### **Problem 1: Commands tidak muncul di menu**

**Cek:**
1. ✅ Commands sudah di-setup di BotFather?
2. ✅ Format commands sudah benar?

**Solusi:**
- Setup ulang commands di BotFather
- Pastikan format: `command - Description`
- Restart Telegram app

---

### **Problem 2: Command tidak bekerja**

**Cek:**
1. ✅ Backend masih running?
2. ✅ Command sudah terdaftar di `telegram_bot.py`?

**Solusi:**
- Restart backend
- Cek apakah command handler sudah ada di code
- Test command langsung (tidak via menu)

---

### **Problem 3: Error saat setup commands**

**Jika BotFather error:**
- Pastikan format benar
- Setiap command di baris baru
- Tidak ada karakter khusus

**Jika API error:**
- Cek token sudah benar
- Cek format JSON sudah valid
- Coba setup via BotFather dulu

---

## 📋 CHECKLIST SETUP COMMANDS

**Pastikan sudah:**

- [ ] Commands sudah di-setup di BotFather
- [ ] Format commands sudah benar
- [ ] Bot description sudah di-set (opsional)
- [ ] Bot about text sudah di-set (opsional)
- [ ] Commands sudah di-test di Telegram
- [ ] Semua commands bekerja dengan benar

---

## 🎯 QUICK REFERENCE

**Setup Commands:**
1. BotFather → `/setcommands`
2. Pilih bot
3. Copy-paste list commands
4. Selesai ✅

**Test Commands:**
1. Telegram → Buka bot
2. Ketik `/` → Lihat list commands
3. Test setiap command

---

**Selamat! Commands sudah ter-setup! 🚀**


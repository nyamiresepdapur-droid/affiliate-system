# 🤖 FLOW TRANSAKSI VIA TELEGRAM BOT

**Tanggal:** 20 Desember 2025  
**Tujuan:** Semua transaksi (daftar, pembayaran, upgrade) via Telegram Bot

---

## 📋 OVERVIEW FLOW

### **Flow 1: User Daftar & Beli Basic Member**
```
User → /start → /daftar → Isi Data → Upload Payment Proof → Admin Verify → Basic Member Active
```

### **Flow 2: User Upgrade ke VIP**
```
VIP Member → /upgrade → Upload Payment Proof → Admin Verify → VIP Member Active + Assign TikTok Account
```

### **Flow 3: Admin Verify Payment**
```
Admin → /pending-payments → List Payments → /verify-payment <id> → Auto-activate Membership
```

---

## 🔄 DETAILED FLOWS

### **FLOW 1: REGISTRATION & BASIC MEMBERSHIP PURCHASE**

#### **Step 1: User Start Bot**
```
User: /start

Bot:
👋 Halo [Nama]!

Selamat datang di Affiliate Management Bot!

📋 **Perintah yang tersedia:**
/daftar - Daftar sebagai member baru
/beli - Beli membership (Basic/VIP)
/upgrade - Upgrade ke VIP
/lapor - Lapor kinerja
/komisi - Cek komisi
/help - Bantuan

**Untuk member baru:**
Gunakan /daftar untuk mendaftar dan beli membership.
```

#### **Step 2: User Daftar**
```
User: /daftar

Bot:
📝 **PENDAFTARAN MEMBER BARU**

Silakan isi data berikut:

1️⃣ **Nama Lengkap:**
(Ketik nama lengkap Anda)
```

#### **Step 3: Input Data (Multi-step)**
```
User: John Doe

Bot:
✅ Nama: John Doe

2️⃣ **Nomor WhatsApp:**
(Contoh: 081234567890)
```

```
User: 081234567890

Bot:
✅ WhatsApp: 081234567890

3️⃣ **Akun TikTok:**
(Contoh: @johndoe)
```

```
User: @johndoe

Bot:
✅ TikTok: @johndoe

4️⃣ **Email (Opsional):**
(Ketik email atau ketik "skip" untuk lewati)
```

```
User: john@example.com

Bot:
✅ Email: john@example.com

5️⃣ **Wallet/Bank:**
(Contoh: DANA 081234567890 atau BCA 1234567890)
```

```
User: DANA 081234567890

Bot:
✅ Wallet: DANA 081234567890

📋 **Data Anda:**
Nama: John Doe
WhatsApp: 081234567890
TikTok: @johndoe
Email: john@example.com
Wallet: DANA 081234567890

✅ Data sudah lengkap!

Sekarang pilih membership yang ingin dibeli:

[Basic Member - Rp 97.000] [VIP Member - Rp 299.000]
```

#### **Step 4: Pilih Membership**
```
User: [Klik "Basic Member - Rp 97.000"]

Bot:
💳 **PEMBELIAN BASIC MEMBER**

Harga: Rp 97.000

📋 **Fasilitas:**
✅ Materi AI Content Creation
✅ Tutorial dasar sampai upload
✅ Akses platform

**Cara Pembayaran:**
1. Transfer ke rekening berikut:
   💰 BCA: 1234567890 (a.n. Admin)
   💰 DANA: 081234567890 (a.n. Admin)

2. Upload bukti pembayaran (foto/screenshot)
   (Kirim foto bukti transfer)

⚠️ Setelah pembayaran diverifikasi, membership akan aktif otomatis.
```

#### **Step 5: Upload Payment Proof**
```
User: [Kirim foto bukti transfer]

Bot:
✅ Bukti pembayaran diterima!

📋 **Detail Pembayaran:**
Membership: Basic Member
Harga: Rp 97.000
Status: ⏳ Menunggu Verifikasi

Admin akan memverifikasi pembayaran Anda dalam 1x24 jam.

Anda akan mendapat notifikasi saat pembayaran sudah diverifikasi.

💡 **Tips:** Sambil menunggu, Anda bisa explore bot dengan /help
```

#### **Step 6: Admin Verify (Auto-notification ke user)**
```
Admin: /verify-payment 123

Bot (ke Admin):
✅ Pembayaran #123 telah diverifikasi!

User: John Doe
Membership: Basic Member
Harga: Rp 97.000
Status: ✅ Aktif

User telah menjadi Basic Member.
```

```
Bot (ke User):
🎉 **PEMBAYARAN DITERIMA!**

Membership Anda sudah aktif!

✅ **Basic Member** - Aktif
📅 Aktif sejak: 20 Desember 2025

**Fasilitas yang bisa digunakan:**
✅ Materi AI Content Creation
✅ Tutorial dasar sampai upload
✅ Akses platform website
✅ Submit report via /lapor

**Perintah yang bisa digunakan:**
/lapor - Lapor kinerja
/komisi - Cek komisi
/upgrade - Upgrade ke VIP (dapat 55% komisi!)

Selamat bergabung! 🎊
```

---

### **FLOW 2: UPGRADE KE VIP**

#### **Step 1: User Request Upgrade**
```
User: /upgrade

Bot:
⬆️ **UPGRADE KE VIP MEMBER**

**Current Membership:** Basic Member
**Upgrade to:** VIP Member

💰 **Harga Upgrade:**
VIP Member: Rp 299.000
Basic Member: Rp 97.000
─────────────────────
Selisih: Rp 202.000

📋 **Fasilitas VIP:**
✅ Semua Basic Member
✅ Group diskusi
✅ Tanya jawab langsung
✅ Zoom meeting
✅ Akun TikTok affiliate (keranjang kuning)
✅ Reporting & validasi
✅ Bagi hasil 55% komisi!

**Cara Pembayaran:**
1. Transfer Rp 202.000 ke:
   💰 BCA: 1234567890
   💰 DANA: 081234567890

2. Upload bukti pembayaran
   (Kirim foto bukti transfer)

[Ya, Saya Mau Upgrade] [Batal]
```

#### **Step 2: User Confirm & Upload Payment**
```
User: [Klik "Ya, Saya Mau Upgrade"]

Bot:
💳 **PEMBAYARAN UPGRADE**

Silakan transfer Rp 202.000 dan upload bukti pembayaran.

(Kirim foto bukti transfer)
```

```
User: [Kirim foto bukti transfer]

Bot:
✅ Bukti pembayaran diterima!

📋 **Detail Upgrade:**
Dari: Basic Member
Ke: VIP Member
Harga: Rp 202.000
Status: ⏳ Menunggu Verifikasi

Admin akan memverifikasi dalam 1x24 jam.

Setelah diverifikasi, Anda akan:
✅ Menjadi VIP Member
✅ Mendapat akun TikTok affiliate
✅ Bisa dapat komisi 55%!

Anda akan mendapat notifikasi saat upgrade sudah aktif.
```

#### **Step 3: Admin Verify Upgrade**
```
Admin: /pending-payments

Bot:
📋 **PENDING PAYMENTS**

1. Upgrade Request #123
   User: John Doe
   Dari: Basic → VIP
   Harga: Rp 202.000
   [Verify] [Reject]

2. Purchase Request #124
   User: Jane Smith
   Basic Member
   Harga: Rp 97.000
   [Verify] [Reject]
```

```
Admin: /verify-payment 123

Bot (ke Admin):
✅ Upgrade #123 telah diverifikasi!

User: John Doe
Upgrade: Basic → VIP
Harga: Rp 202.000
Status: ✅ Aktif

User sekarang adalah VIP Member.
TikTok account akan di-assign segera.
```

```
Bot (ke User):
🎉 **UPGRADE BERHASIL!**

Anda sekarang adalah **VIP MEMBER**!

✅ **VIP Member** - Aktif
📅 Aktif sejak: 20 Desember 2025

**Fasilitas VIP:**
✅ Semua Basic Member
✅ Group diskusi (akan di-invite)
✅ Tanya jawab langsung
✅ Zoom meeting
✅ Akun TikTok affiliate (sedang di-assign)
✅ Reporting & validasi
✅ Bagi hasil 55% komisi!

**Akun TikTok Affiliate:**
⏳ Sedang di-assign oleh admin...
Anda akan mendapat notifikasi saat akun sudah ready.

**Perintah VIP:**
/lapor - Lapor kinerja harian
/komisi - Cek komisi (55% untuk Anda!)
/akun - Cek info akun TikTok affiliate

Selamat! 🎊
```

---

### **FLOW 3: ADMIN VERIFY PAYMENT**

#### **Step 1: Admin Check Pending Payments**
```
Admin: /pending-payments

Bot:
📋 **PENDING PAYMENTS** (3)

1️⃣ **Purchase #123**
   👤 User: John Doe (@johndoe)
   💰 Membership: Basic Member
   💵 Harga: Rp 97.000
   📅 Tanggal: 20 Des 2025 10:30
   [✅ Verify] [❌ Reject] [👁️ Detail]

2️⃣ **Upgrade #124**
   👤 User: Jane Smith (@janesmith)
   💰 Upgrade: Basic → VIP
   💵 Harga: Rp 202.000
   📅 Tanggal: 20 Des 2025 11:00
   [✅ Verify] [❌ Reject] [👁️ Detail]

3️⃣ **Purchase #125**
   👤 User: Bob Wilson (@bobwilson)
   💰 Membership: VIP Member
   💵 Harga: Rp 299.000
   📅 Tanggal: 20 Des 2025 12:00
   [✅ Verify] [❌ Reject] [👁️ Detail]
```

#### **Step 2: Admin View Detail**
```
Admin: [Klik "👁️ Detail" pada Payment #123]

Bot:
📋 **DETAIL PAYMENT #123**

👤 **User Info:**
Nama: John Doe
WhatsApp: 081234567890
TikTok: @johndoe
Email: john@example.com

💳 **Payment Info:**
Membership: Basic Member
Harga: Rp 97.000
Metode: Bank Transfer
Status: ⏳ Pending

📸 **Payment Proof:**
[Lihat Foto]

[✅ Verify Payment] [❌ Reject] [🔙 Back]
```

#### **Step 3: Admin Verify**
```
Admin: [Klik "✅ Verify Payment"]

Bot:
✅ **VERIFY PAYMENT?**

Payment #123
User: John Doe
Membership: Basic Member
Harga: Rp 97.000

Setelah diverifikasi:
✅ User akan jadi Basic Member
✅ User akan dapat notifikasi
✅ Membership akan aktif otomatis

[✅ Ya, Verify] [❌ Batal]
```

```
Admin: [Klik "✅ Ya, Verify"]

Bot (ke Admin):
✅ Payment #123 telah diverifikasi!

User: John Doe
Membership: Basic Member - Aktif
Harga: Rp 97.000

✅ User telah menjadi Basic Member.
✅ Notifikasi telah dikirim ke user.
```

```
Bot (ke User):
🎉 **PEMBAYARAN DITERIMA!**

Membership Anda sudah aktif!

✅ **Basic Member** - Aktif
📅 Aktif sejak: 20 Desember 2025

Gunakan /help untuk melihat semua perintah.
```

#### **Step 4: Admin Reject (jika perlu)**
```
Admin: [Klik "❌ Reject" pada Payment #123]

Bot:
❌ **REJECT PAYMENT?**

Payment #123
User: John Doe

Alasan penolakan:
(Ketik alasan, contoh: "Bukti pembayaran tidak jelas")
```

```
Admin: Bukti pembayaran tidak jelas

Bot (ke Admin):
❌ Payment #123 telah ditolak.

Alasan: Bukti pembayaran tidak jelas

User akan mendapat notifikasi.
```

```
Bot (ke User):
❌ **PEMBAYARAN DITOLAK**

Payment #123

Alasan: Bukti pembayaran tidak jelas

Silakan upload ulang bukti pembayaran yang lebih jelas.

Gunakan /beli untuk membeli membership lagi.
```

---

### **FLOW 4: ASSIGN TIKTOK ACCOUNT (Admin)**

#### **Step 1: Admin Assign Account**
```
Admin: /assign-account 5

Bot:
📱 **ASSIGN TIKTOK ACCOUNT**

User: John Doe
Membership: VIP Member

Pilih akun TikTok yang akan di-assign:

[Account 1: @shop1] [Account 2: @shop2]
[Account 3: @shop3] [Lihat Semua]
```

```
Admin: [Klik "Account 1: @shop1"]

Bot:
✅ **ASSIGN ACCOUNT?**

User: John Doe
Account: @shop1
Shop ID: 1234567890
Keranjang Kuning: ✅ Verified

Setelah di-assign:
✅ User akan dapat akses akun
✅ User akan dapat notifikasi
✅ User bisa mulai dapat komisi 55%

[✅ Ya, Assign] [❌ Batal]
```

```
Admin: [Klik "✅ Ya, Assign"]

Bot (ke Admin):
✅ Account @shop1 telah di-assign ke John Doe!

User: John Doe
Account: @shop1
Status: ✅ Active

User akan mendapat notifikasi.
```

```
Bot (ke User):
🎉 **AKUN TIKTOK AFFILIATE READY!**

Akun TikTok affiliate Anda sudah siap!

📱 **Account Info:**
Username: @shop1
Shop ID: 1234567890
Keranjang Kuning: ✅ Verified
Status: ✅ Active

**Selanjutnya:**
1. Gunakan akun ini untuk promosi produk
2. Submit report via /lapor setiap hari
3. Dapat komisi 55% dari setiap penjualan!

**Perintah:**
/akun - Lihat info akun
/lapor - Submit report harian
/komisi - Cek komisi Anda

Selamat! 🎊
```

---

## 📱 BOT COMMANDS

### **User Commands:**
- `/start` - Mulai bot
- `/daftar` - Daftar sebagai member baru
- `/beli` - Beli membership (Basic/VIP)
- `/upgrade` - Upgrade ke VIP
- `/lapor` - Lapor kinerja harian
- `/komisi` - Cek komisi
- `/pembayaran` - Cek status pembayaran
- `/akun` - Cek info akun TikTok affiliate (VIP only)
- `/help` - Bantuan

### **Admin Commands:**
- `/admin` - Menu admin
- `/pending-payments` - List pending payments
- `/verify-payment <id>` - Verify payment
- `/reject-payment <id> <alasan>` - Reject payment
- `/assign-account <user_id>` - Assign TikTok account
- `/accounts` - List semua accounts
- `/users` - List semua users
- `/stats` - Statistik sistem

---

## 🗄️ DATABASE UPDATES

### **Payment Proof Storage:**
```sql
-- Add to upgrade_requests table
ALTER TABLE upgrade_requests ADD COLUMN payment_proof_file_id VARCHAR(200);  -- Telegram file_id
ALTER TABLE upgrade_requests ADD COLUMN payment_proof_url TEXT;  -- URL jika di-upload ke server

-- Add to user_memberships table (untuk purchase)
ALTER TABLE user_memberships ADD COLUMN payment_proof_file_id VARCHAR(200);
ALTER TABLE user_memberships ADD COLUMN payment_proof_url TEXT;
```

---

## 🔄 STATE MANAGEMENT

### **Pending States:**
```python
# Di telegram_bot.py
pending_registrations = {}  # {user_id: {step, data}}
pending_payments = {}  # {user_id: {type, membership_tier, amount, file_id}}
pending_upgrades = {}  # {user_id: {from_tier, to_tier, amount, file_id}}
```

---

## 🎯 IMPLEMENTATION CHECKLIST

### **Phase 1: Registration & Purchase Flow**
- [ ] Update `/daftar` command dengan membership selection
- [ ] Add payment proof upload handler
- [ ] Create payment request record
- [ ] Add `/pending-payments` command (admin)
- [ ] Add `/verify-payment` command (admin)
- [ ] Auto-activate membership setelah verify
- [ ] Send notification ke user

### **Phase 2: Upgrade Flow**
- [ ] Add `/upgrade` command
- [ ] Calculate upgrade price
- [ ] Add payment proof upload untuk upgrade
- [ ] Create upgrade request record
- [ ] Admin verify upgrade
- [ ] Auto-upgrade membership
- [ ] Send notification ke user

### **Phase 3: Account Assignment**
- [ ] Add `/assign-account` command (admin)
- [ ] List available accounts
- [ ] Assign account ke VIP user
- [ ] Send notification ke user
- [ ] Update affiliate_accounts table

### **Phase 4: Payment Proof Management**
- [ ] Store payment proof (file_id atau URL)
- [ ] Admin bisa lihat payment proof
- [ ] Reject dengan alasan
- [ ] User bisa re-upload jika ditolak

---

## 💡 FEATURES

### **1. Inline Keyboard Buttons**
- Pilih membership tier
- Verify/Reject payment
- View payment proof
- Assign account

### **2. Photo Handler**
- Auto-detect payment proof upload
- Validate file type (image)
- Store file_id atau upload ke server

### **3. Notifications**
- User dapat notifikasi saat payment verified
- User dapat notifikasi saat upgrade aktif
- User dapat notifikasi saat account assigned
- Admin dapat notifikasi saat ada payment baru

### **4. State Management**
- Multi-step registration
- Payment proof upload state
- Upgrade confirmation state

---

## 🚀 NEXT STEPS

1. **Review flow** - Pastikan sesuai kebutuhan
2. **Start implementation** - Update telegram_bot.py
3. **Test flow** - Test end-to-end
4. **Deploy** - Launch ke production

---

**Ready to implement?** 🚀


# 🔄 FLOW WEBSITE LOW BUDGET - DETAIL

**Tanggal:** 20 Desember 2025  
**Fokus:** Flow lengkap untuk manage tim dengan budget minimal

---

## 🎯 FLOW UTAMA

### **FLOW 1: VISITOR → MEMBER (Via Website)**

```
┌─────────────────────────────────────────┐
│  1. VISITOR BUKA WEBSITE                 │
│     URL: your-domain.com                  │
│     Halaman: Landing Page                 │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. LANDING PAGE                         │
│     - Hero: "Daftar Sekarang"            │
│     - Membership Plans (Basic/VIP)       │
│     - Features                           │
│     - FAQ                                 │
│     [Klik: "Daftar Sekarang"]            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. REGISTER PAGE                        │
│     Form:                                 │
│     - Nama Lengkap                        │
│     - WhatsApp                            │
│     - Email                               │
│     - Pilih Membership (Basic/VIP)       │
│     - Payment Method (Wallet/Bank)       │
│     - Detail Payment                      │
│     [Submit]                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  4. PAYMENT INSTRUCTION                  │
│     - Rekening tujuan                     │
│     - Jumlah transfer                     │
│     - Upload bukti pembayaran             │
│     [Upload Foto Bukti]                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  5. PAYMENT PENDING                      │
│     Status: ⏳ Menunggu Verifikasi       │
│     Message: "Admin akan verify 1x24 jam"│
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  6. ADMIN VERIFY (Di Admin Panel)       │
│     - Lihat payment request              │
│     - Lihat bukti pembayaran             │
│     - Verify payment                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  7. MEMBERSHIP AKTIF                    │
│     - User dapat email/notifikasi        │
│     - User bisa login                    │
│     - Membership status: Active          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  8. USER LOGIN                          │
│     - Username/Email + Password          │
│     - Masuk ke Dashboard                 │
└─────────────────────────────────────────┘
```

---

### **FLOW 2: MEMBER → SUBMIT REPORT**

```
┌─────────────────────────────────────────┐
│  1. MEMBER LOGIN                         │
│     Masuk ke Dashboard                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. DASHBOARD                           │
│     - Welcome message                    │
│     - Membership status                  │
│     - Quick stats                        │
│     [Klik: "My Reports"]                 │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. MY REPORTS PAGE                     │
│     - List reports (jika ada)           │
│     [Klik: "Submit New Report"]         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  4. SUBMIT REPORT FORM                   │
│     Form:                                 │
│     - Link Video (bisa banyak)           │
│     - Tanggal Upload                     │
│     - Akun TikTok                        │
│     [Submit]                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  5. REPORT SUBMITTED                     │
│     Status: ⏳ Pending                   │
│     Message: "Menunggu approval admin"   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  6. ADMIN APPROVE (Di Admin Panel)       │
│     - Lihat report                       │
│     - Approve report                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  7. REPORT APPROVED                     │
│     - User dapat notifikasi              │
│     - Commission calculated              │
│     - Status: ✅ Approved                 │
└─────────────────────────────────────────┘
```

---

### **FLOW 3: MEMBER → UPGRADE KE VIP**

```
┌─────────────────────────────────────────┐
│  1. MEMBER (Basic) LOGIN                 │
│     Masuk ke Dashboard                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. DASHBOARD                           │
│     - Membership: Basic Member           │
│     [Klik: "Upgrade to VIP"]             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. UPGRADE PAGE                        │
│     - Info upgrade (Basic → VIP)        │
│     - Harga: Rp 202.000                 │
│     - Fasilitas VIP                      │
│     [Klik: "Ya, Saya Mau Upgrade"]       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  4. PAYMENT INSTRUCTION                 │
│     - Transfer Rp 202.000               │
│     - Rekening tujuan                    │
│     - Upload bukti pembayaran            │
│     [Upload Foto Bukti]                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  5. PAYMENT PENDING                     │
│     Status: ⏳ Menunggu Verifikasi       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  6. ADMIN VERIFY                        │
│     - Verify payment                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  7. UPGRADE BERHASIL                    │
│     - User jadi VIP Member               │
│     - Dapat notifikasi                   │
│     - Akun TikTok di-assign (jika perlu) │
└─────────────────────────────────────────┘
```

---

### **FLOW 4: ADMIN → MANAGE TIM**

```
┌─────────────────────────────────────────┐
│  1. ADMIN LOGIN                         │
│     Role: Owner/Admin                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. ADMIN DASHBOARD                     │
│     - Overview statistics                │
│     - Pending payments                   │
│     - Pending reports                    │
│     - Quick actions                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. PENDING PAYMENTS                    │
│     List:                                │
│     - User | Type | Amount | Status     │
│     [Klik: Payment untuk detail]         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  4. PAYMENT DETAIL                      │
│     - User info                          │
│     - Payment info                       │
│     - Bukti pembayaran (foto)            │
│     [Klik: "Verify"] atau [Reject]       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  5. VERIFY PAYMENT                      │
│     - Confirm verify                     │
│     - User jadi member (otomatis)        │
│     - User dapat notifikasi              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  6. PENDING REPORTS                     │
│     List:                                │
│     - User | Link | Tanggal | Status    │
│     [Klik: Report untuk detail]         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  7. REPORT DETAIL                       │
│     - User info                          │
│     - Video links                        │
│     - Tanggal upload                     │
│     [Klik: "Approve"] atau [Reject]      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  8. APPROVE REPORT                      │
│     - Report approved                    │
│     - Commission calculated               │
│     - User dapat notifikasi              │
└─────────────────────────────────────────┘
```

---

## 📱 INTEGRASI TELEGRAM BOT

### **Website ↔ Telegram Bot**

```
┌─────────────────────────────────────────┐
│  WEBSITE                                │
│  - User daftar via website              │
│  - User submit report via website       │
│  - Admin manage via website             │
└─────────────────────────────────────────┘
              ↕ Sync Data
┌─────────────────────────────────────────┐
│  TELEGRAM BOT                           │
│  - User daftar via bot                  │
│  - User submit report via bot           │
│  - Admin manage via bot                 │
└─────────────────────────────────────────┘
              ↕
┌─────────────────────────────────────────┐
│  DATABASE (Shared)                      │
│  - Users                                 │
│  - Reports                               │
│  - Payments                              │
│  - Commissions                           │
└─────────────────────────────────────────┘
```

**Kedua platform (Website & Bot) pakai database yang sama!**

---

## 🎨 STRUKTUR HALAMAN

### **1. LANDING PAGE (`/`)**

**Sections:**
1. **Header**
   - Logo
   - Navigation (Home, Features, Pricing, FAQ)
   - Login Button

2. **Hero Section**
   - Judul besar: "Affiliate Management System"
   - Deskripsi singkat
   - CTA Button: "Daftar Sekarang"

3. **Membership Plans**
   - Basic Member (Rp 97.000)
   - VIP Member (Rp 299.000)
   - Compare features

4. **Features**
   - List fitur utama
   - Icons & descriptions

5. **FAQ**
   - Pertanyaan umum
   - Accordion style

6. **Footer**
   - Links
   - Contact
   - Social media

---

### **2. REGISTER PAGE (`/register`)**

**Form Sections:**
1. **Personal Info**
   - Nama Lengkap
   - WhatsApp
   - Email

2. **Membership Selection**
   - Radio buttons: Basic / VIP
   - Harga display

3. **Payment Method**
   - Radio buttons: Wallet / Bank
   - Detail input (Wallet number / Bank account)

4. **Payment Proof**
   - File upload (image)
   - Preview image

5. **Submit Button**

---

### **3. LOGIN PAGE (`/login`)**

**Simple Form:**
- Username/Email input
- Password input
- Login button
- Link: "Belum punya akun? Daftar"

---

### **4. USER DASHBOARD (`/dashboard`)**

**Layout:**
```
┌─────────────────────────────────────┐
│  Header                             │
│  [Logo] [User Menu] [Notifications]  │
├──────────┬──────────────────────────┤
│ Sidebar  │  Main Content            │
│          │                          │
│ - Home   │  Welcome Section         │
│ - Reports│  Stats Cards             │
│ - Komisi │  Quick Actions           │
│ - Payment│                          │
│ - Akun   │                          │
│ - Profile│                          │
└──────────┴──────────────────────────┘
```

---

### **5. MY REPORTS (`/my-reports`)**

**Sections:**
1. **Header**
   - Title: "My Reports"
   - Button: "Submit New Report"

2. **Reports List**
   - Table: No | Link | Tanggal | Status | Actions
   - Filter & Search
   - Pagination

3. **Submit Report Modal**
   - Form: Link video, Tanggal, Akun TikTok
   - Submit button

---

### **6. ADMIN - PENDING PAYMENTS (`/admin/payments`)**

**Sections:**
1. **Header**
   - Title: "Pending Payments"
   - Filter & Export buttons

2. **Payments List**
   - Table: User | Type | Amount | Status | Actions
   - Actions: View | Verify | Reject

3. **Payment Detail Modal**
   - User info
   - Payment info
   - Bukti pembayaran (image)
   - Verify/Reject buttons

---

## 💰 BUDGET BREAKDOWN

### **Option 1: FULL FREE**

| Item | Service | Cost |
|------|---------|------|
| Frontend Hosting | Vercel | $0 |
| Backend Hosting | Railway | $0 |
| Database | Supabase | $0 |
| CDN | Cloudflare | $0 |
| Storage | Cloudinary | $0 |
| Domain | Freenom (.tk) | $0 |
| **TOTAL** | | **$0/tahun** |

---

### **Option 2: SEMI-PRO (Recommended)**

| Item | Service | Cost |
|------|---------|------|
| Frontend Hosting | Vercel | $0 |
| Backend Hosting | Railway | $0 |
| Database | Supabase | $0 |
| CDN | Cloudflare | $0 |
| Storage | Cloudinary | $0 |
| Domain | Namecheap (.com) | $10/tahun |
| **TOTAL** | | **$10/tahun** |

---

## 🚀 DEPLOYMENT CHECKLIST

### **Pre-Deployment:**
- [ ] Code sudah siap
- [ ] Database migration siap
- [ ] Environment variables siap
- [ ] Test semua fitur lokal

### **Deployment:**
- [ ] Setup Vercel account
- [ ] Deploy frontend
- [ ] Setup Railway account
- [ ] Deploy backend
- [ ] Setup Supabase database
- [ ] Connect semua services
- [ ] Test di production

### **Post-Deployment:**
- [ ] Setup domain (jika ada)
- [ ] Configure SSL (auto dari Vercel)
- [ ] Test semua fitur
- [ ] Monitor performance
- [ ] Setup backup (opsional)

---

## 📋 ACTION PLAN (6 MINGGU)

### **Week 1: Landing Page**
- [ ] Design landing page
- [ ] HTML structure
- [ ] CSS styling
- [ ] Responsive design
- [ ] Deploy ke Vercel

### **Week 2: Authentication**
- [ ] Register page
- [ ] Login page
- [ ] JWT integration
- [ ] Session management
- [ ] Test flow

### **Week 3: User Dashboard**
- [ ] Dashboard layout
- [ ] My Reports page
- [ ] Submit report form
- [ ] My Commissions page
- [ ] My Payments page

### **Week 4: Admin Dashboard**
- [ ] Admin layout
- [ ] Pending Payments page
- [ ] Payment verification
- [ ] Pending Reports page
- [ ] Report approval

### **Week 5: Membership & Polish**
- [ ] Membership status
- [ ] Upgrade flow
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Testing

### **Week 6: Deployment**
- [ ] Setup hosting
- [ ] Deploy frontend
- [ ] Deploy backend
- [ ] Setup database
- [ ] Production testing

---

## 🎯 PRIORITAS FITUR

### **Must Have (MVP):**
1. ✅ Landing page
2. ✅ Register & Login
3. ✅ User dashboard
4. ✅ Submit report
5. ✅ Admin verify payment
6. ✅ Admin approve report

### **Should Have:**
7. ✅ My Reports (list & edit)
8. ✅ My Commissions
9. ✅ Payment status
10. ✅ Notifications

### **Nice to Have:**
11. ✅ Charts & analytics
12. ✅ Export data
13. ✅ Advanced filters
14. ✅ Mobile app (PWA)

---

**Ready to build! 🚀**


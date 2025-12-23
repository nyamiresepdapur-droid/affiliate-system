# 💰 PLAN WEBSITE LOW BUDGET UNTUK MENGELOLA TIM

**Tanggal:** 20 Desember 2025  
**Budget:** Low Budget (Minimal Cost)  
**Tujuan:** Website untuk manage tim affiliate dengan biaya minimal

---

## 🎯 KONSEP WEBSITE

### **Tujuan:**
- Manage tim affiliate secara efisien
- User bisa daftar, beli membership, lapor via website
- Admin bisa manage semua dari website
- **Low budget** - pakai hosting gratis/murah

---

## 💰 STRATEGI LOW BUDGET

### **1. Hosting Gratis/Murah**
- ✅ **Vercel** (Gratis) - Untuk frontend
- ✅ **Railway** (Gratis tier) - Untuk backend
- ✅ **Render** (Gratis tier) - Alternatif backend
- ✅ **Supabase** (Gratis tier) - Database PostgreSQL gratis

### **2. Database**
- ✅ **SQLite** (Gratis) - Untuk development
- ✅ **Supabase PostgreSQL** (Gratis) - Untuk production
- ✅ **PlanetScale** (Gratis tier) - Alternatif MySQL

### **3. Domain**
- ✅ **Freenom** (Gratis) - Domain .tk, .ml, .ga
- ✅ **Namecheap** (Murah) - Domain .com ~$10/tahun
- ✅ **Cloudflare** (Murah) - Domain + DNS gratis

### **4. CDN & Storage**
- ✅ **Cloudflare** (Gratis) - CDN & DDoS protection
- ✅ **Cloudinary** (Gratis tier) - Image storage
- ✅ **GitHub Pages** (Gratis) - Static hosting

---

## 🏗️ ARSITEKTUR LOW BUDGET

```
┌─────────────────────────────────────────┐
│         FRONTEND (Vercel - Gratis)      │
│  ┌──────────────┐  ┌──────────────┐    │
│  │   Landing    │  │   Dashboard  │    │
│  │    Page      │  │   (User)     │    │
│  └──────────────┘  └──────────────┘    │
│  ┌──────────────┐  ┌──────────────┐    │
│  │   Register   │  │   Admin      │    │
│  │   & Payment  │  │   Panel     │    │
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
                  │
                  │ API Calls
                  │
┌─────────────────────────────────────────┐
│      BACKEND (Railway - Gratis)         │
│  ┌──────────────┐  ┌──────────────┐    │
│  │   Flask API  │  │  Telegram    │    │
│  │   (Python)   │  │     Bot      │    │
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
                  │
                  │ SQLAlchemy ORM
                  │
┌─────────────────────────────────────────┐
│   DATABASE (Supabase - Gratis)          │
│  ┌──────────────┐  ┌──────────────┐    │
│  │  PostgreSQL  │  │   Storage    │    │
│  │   (Free)     │  │   (Images)   │    │
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
```

**Total Cost: $0-10/tahun** (hanya domain jika pakai .com)

---

## 📋 FITUR WEBSITE

### **1. LANDING PAGE (Public)**

**Fitur:**
- ✅ Hero section (judul, deskripsi, CTA)
- ✅ Fitur membership (Basic & VIP)
- ✅ Harga & paket
- ✅ Testimoni (opsional)
- ✅ FAQ
- ✅ Footer (contact, social media)

**Tujuan:** Convert visitor jadi member

---

### **2. REGISTRATION & PAYMENT PAGE**

**Fitur:**
- ✅ Form registrasi (nama, WhatsApp, email, dll)
- ✅ Pilih membership (Basic/VIP)
- ✅ Payment method selection
- ✅ Upload payment proof
- ✅ Status tracking

**Tujuan:** User bisa daftar & bayar via website

---

### **3. USER DASHBOARD**

**Fitur:**
- ✅ Profile info
- ✅ Membership status
- ✅ My Reports (list & submit)
- ✅ My Commissions
- ✅ My Payments
- ✅ Account info (VIP only)
- ✅ Notifications

**Tujuan:** User manage semua dari satu tempat

---

### **4. ADMIN DASHBOARD**

**Fitur:**
- ✅ Overview statistics
- ✅ Pending Payments (verify/reject)
- ✅ Pending Reports (approve/reject)
- ✅ User Management
- ✅ Affiliate Account Management
- ✅ Commission Management
- ✅ Leader Management

**Tujuan:** Admin manage semua dari website

---

## 🔄 FLOW WEBSITE

### **FLOW 1: VISITOR → MEMBER**

```
1. Visitor buka website
   ↓
2. Lihat landing page (info membership)
   ↓
3. Klik "Daftar Sekarang" atau "Beli Membership"
   ↓
4. Register (isi data)
   ↓
5. Pilih membership (Basic/VIP)
   ↓
6. Upload payment proof
   ↓
7. Tunggu admin verify
   ↓
8. Membership aktif → Login dashboard
```

---

### **FLOW 2: MEMBER → SUBMIT REPORT**

```
1. Member login
   ↓
2. Buka "My Reports"
   ↓
3. Klik "Submit New Report"
   ↓
4. Isi form (link video, tanggal, akun TikTok)
   ↓
5. Submit report
   ↓
6. Status: Pending
   ↓
7. Admin approve → Status: Approved
   ↓
8. Commission calculated (55% untuk VIP)
```

---

### **FLOW 3: ADMIN → VERIFY PAYMENT**

```
1. Admin login
   ↓
2. Buka "Pending Payments"
   ↓
3. Lihat list payments
   ↓
4. Klik payment → Lihat detail & bukti
   ↓
5. Verify payment
   ↓
6. User otomatis jadi member
   ↓
7. User dapat notifikasi
```

---

## 🎨 DESAIN WEBSITE

### **Warna & Style:**
- **Primary:** Purple/Gradient (sesuai existing)
- **Secondary:** Green (success), Red (danger), Blue (info)
- **Style:** Modern, Clean, Professional
- **Responsive:** Mobile-first design

### **Layout:**
- **Header:** Logo, Navigation, User menu, Notifications
- **Sidebar:** (untuk dashboard) - Navigation menu
- **Content:** Main content area
- **Footer:** Links, contact, copyright

---

## 📐 STRUKTUR HALAMAN

### **1. Landing Page (`/`)**
```
┌─────────────────────────────────────┐
│  Header (Logo, Nav, Login)          │
├─────────────────────────────────────┤
│  Hero Section                       │
│  - Judul besar                      │
│  - Deskripsi                        │
│  - CTA Button (Daftar Sekarang)     │
├─────────────────────────────────────┤
│  Membership Plans                   │
│  ┌──────────┐  ┌──────────┐        │
│  │  Basic   │  │   VIP    │        │
│  │ 97.000   │  │ 299.000  │        │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│  Features                           │
│  - List fitur                       │
├─────────────────────────────────────┤
│  FAQ                                │
│  - Pertanyaan umum                  │
├─────────────────────────────────────┤
│  Footer                             │
└─────────────────────────────────────┘
```

---

### **2. Register Page (`/register`)**
```
┌─────────────────────────────────────┐
│  Header                             │
├─────────────────────────────────────┤
│  Registration Form                  │
│  - Nama Lengkap                     │
│  - WhatsApp                         │
│  - Email                            │
│  - Wallet/Bank                      │
│  - Pilih Membership                 │
│  - Upload Payment Proof             │
│  - Submit Button                    │
└─────────────────────────────────────┘
```

---

### **3. Login Page (`/login`)**
```
┌─────────────────────────────────────┐
│  Login Form                         │
│  - Username/Email                   │
│  - Password                         │
│  - Login Button                     │
│  - Link: Belum punya akun? Daftar  │
└─────────────────────────────────────┘
```

---

### **4. User Dashboard (`/dashboard`)**
```
┌─────────────────────────────────────┐
│  Header (Logo, User Menu, Notif)    │
├──────────┬──────────────────────────┤
│ Sidebar  │  Main Content            │
│ - Home   │  ┌────────────────────┐  │
│ - Reports│  │  Welcome, [Nama]!  │  │
│ - Komisi │  │  Membership: VIP   │  │
│ - Payment│  │  ┌──────┐ ┌──────┐ │  │
│ - Akun   │  │  │Stats │ │Stats │ │  │
│ - Profile│  │  └──────┘ └──────┘ │  │
│          │  └────────────────────┘  │
└──────────┴──────────────────────────┘
```

---

### **5. My Reports Page (`/my-reports`)**
```
┌─────────────────────────────────────┐
│  Header                             │
├─────────────────────────────────────┤
│  My Reports                         │
│  [Submit New Report] [Filter]        │
├─────────────────────────────────────┤
│  Reports Table                      │
│  - No | Link | Tanggal | Status    │
│  - [Edit] [Delete] (jika pending)   │
├─────────────────────────────────────┤
│  Pagination                         │
└─────────────────────────────────────┘
```

---

### **6. Admin - Pending Payments (`/admin/payments`)**
```
┌─────────────────────────────────────┐
│  Admin Header                       │
├─────────────────────────────────────┤
│  Pending Payments                   │
│  [Filter] [Export]                  │
├─────────────────────────────────────┤
│  Payments List                       │
│  - User | Type | Amount | Status    │
│  - [View Proof] [Verify] [Reject]   │
├─────────────────────────────────────┤
│  Pagination                         │
└─────────────────────────────────────┘
```

---

## 💻 TEKNOLOGI STACK (LOW BUDGET)

### **Frontend:**
- ✅ **HTML/CSS/JavaScript** (Vanilla) - Gratis
- ✅ **Bootstrap 5** (CDN) - Gratis
- ✅ **Chart.js** (CDN) - Gratis untuk charts
- ✅ **No framework** - Lebih ringan, lebih cepat

### **Backend:**
- ✅ **Flask** (Python) - Sudah ada
- ✅ **SQLite** (Development) - Gratis
- ✅ **PostgreSQL** (Production - Supabase) - Gratis

### **Hosting:**
- ✅ **Vercel** (Frontend) - Gratis
- ✅ **Railway** (Backend) - Gratis tier
- ✅ **Cloudflare** (CDN) - Gratis

### **Database:**
- ✅ **Supabase** (PostgreSQL) - Gratis 500MB
- ✅ **PlanetScale** (MySQL) - Alternatif gratis

### **Storage:**
- ✅ **Cloudinary** (Images) - Gratis 25GB
- ✅ **Supabase Storage** - Gratis 1GB

**Total Cost: $0-10/tahun** (hanya domain)

---

## 📋 IMPLEMENTATION PLAN

### **PHASE 1: LANDING PAGE (Week 1)**

**Day 1-2: Design & HTML**
- [ ] Buat landing page HTML
- [ ] Hero section
- [ ] Membership plans section
- [ ] Features section
- [ ] FAQ section
- [ ] Footer

**Day 3-4: Styling**
- [ ] CSS styling (modern & responsive)
- [ ] Mobile responsive
- [ ] Animations (opsional)

**Day 5: Integration**
- [ ] Connect dengan backend
- [ ] CTA buttons link ke register
- [ ] Test di berbagai device

---

### **PHASE 2: AUTHENTICATION (Week 2)**

**Day 1-2: Login/Register**
- [ ] Login page
- [ ] Register page
- [ ] JWT authentication
- [ ] Session management

**Day 3-4: User Management**
- [ ] User profile page
- [ ] Edit profile
- [ ] Change password
- [ ] Logout

**Day 5: Testing**
- [ ] Test login/register flow
- [ ] Test session persistence
- [ ] Test security

---

### **PHASE 3: USER DASHBOARD (Week 3)**

**Day 1-2: Dashboard Home**
- [ ] Welcome section
- [ ] Statistics cards
- [ ] Quick actions
- [ ] Recent activity

**Day 3-4: My Reports**
- [ ] List reports
- [ ] Submit report form
- [ ] Edit/Delete report
- [ ] Filter & search

**Day 5: My Commissions & Payments**
- [ ] Commission list
- [ ] Payment history
- [ ] Statistics

---

### **PHASE 4: ADMIN DASHBOARD (Week 4)**

**Day 1-2: Admin Overview**
- [ ] Statistics dashboard
- [ ] Charts & graphs
- [ ] Quick actions

**Day 3-4: Payment Management**
- [ ] Pending payments list
- [ ] View payment proof
- [ ] Verify/Reject payment
- [ ] Payment history

**Day 5: Report Management**
- [ ] Pending reports list
- [ ] Approve/Reject reports
- [ ] Report details

---

### **PHASE 5: MEMBERSHIP & ACCOUNT (Week 5)**

**Day 1-2: Membership System**
- [ ] Membership status display
- [ ] Upgrade flow
- [ ] Payment integration

**Day 3-4: Affiliate Account**
- [ ] Account assignment (admin)
- [ ] Account info display (user)
- [ ] Account status tracking

**Day 5: Testing & Polish**
- [ ] End-to-end testing
- [ ] UI/UX improvements
- [ ] Performance optimization

---

### **PHASE 6: DEPLOYMENT (Week 6)**

**Day 1-2: Setup Hosting**
- [ ] Deploy frontend ke Vercel
- [ ] Deploy backend ke Railway
- [ ] Setup database (Supabase)

**Day 3-4: Domain & DNS**
- [ ] Setup domain (jika ada)
- [ ] Configure DNS
- [ ] SSL certificate (auto dari Vercel)

**Day 5: Testing Production**
- [ ] Test semua fitur di production
- [ ] Performance testing
- [ ] Security check

---

## 💰 ESTIMASI BIAYA

### **Gratis (Recommended):**
- ✅ Hosting: Vercel (Gratis)
- ✅ Backend: Railway (Gratis tier)
- ✅ Database: Supabase (Gratis 500MB)
- ✅ CDN: Cloudflare (Gratis)
- ✅ Storage: Cloudinary (Gratis 25GB)
- ✅ Domain: Freenom (.tk, .ml) - Gratis

**Total: $0/tahun**

---

### **Murah (Jika Mau Lebih Profesional):**
- ✅ Domain .com: Namecheap ($10/tahun)
- ✅ Hosting: Vercel (Gratis)
- ✅ Backend: Railway (Gratis tier)
- ✅ Database: Supabase (Gratis)

**Total: $10/tahun**

---

## 🚀 DEPLOYMENT STRATEGY

### **Option 1: Full Free (Recommended)**

**Frontend:**
- Deploy ke **Vercel** (gratis)
- Connect dengan GitHub
- Auto-deploy saat push

**Backend:**
- Deploy ke **Railway** (gratis tier)
- Connect dengan GitHub
- Auto-deploy saat push

**Database:**
- **Supabase PostgreSQL** (gratis 500MB)
- Cukup untuk ribuan user

**Domain:**
- Pakai subdomain Vercel: `your-app.vercel.app`
- Atau domain gratis: `.tk`, `.ml`

---

### **Option 2: Semi-Pro (Murah)**

**Frontend:**
- Vercel (gratis)

**Backend:**
- Railway (gratis tier)

**Database:**
- Supabase (gratis)

**Domain:**
- Namecheap .com ($10/tahun)
- Cloudflare DNS (gratis)

**Total: $10/tahun**

---

## 📋 CHECKLIST SETUP

### **Pre-Deployment:**
- [ ] Code sudah siap
- [ ] Database migration siap
- [ ] Environment variables siap
- [ ] Test semua fitur

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
- [ ] Configure SSL
- [ ] Test semua fitur
- [ ] Monitor performance

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

## 📊 TIMELINE

### **Week 1-2: Foundation**
- Landing page
- Authentication
- Basic dashboard

### **Week 3-4: Core Features**
- User reports
- Admin management
- Payment system

### **Week 5: Polish**
- UI/UX improvements
- Performance
- Testing

### **Week 6: Deployment**
- Setup hosting
- Deploy
- Testing production

**Total: 6 minggu untuk MVP**

---

## 💡 TIPS LOW BUDGET

1. **Pakai hosting gratis** - Vercel, Railway, Supabase
2. **Pakai CDN gratis** - Cloudflare
3. **Optimize images** - Compress sebelum upload
4. **Minimize dependencies** - Pakai vanilla JS jika bisa
5. **Cache static files** - Kurangi server load
6. **Monitor usage** - Jangan exceed free tier limits

---

## 🚀 NEXT STEPS

1. **Review plan** - Pastikan sesuai kebutuhan
2. **Pilih hosting** - Vercel + Railway (gratis)
3. **Setup database** - Supabase (gratis)
4. **Start development** - Phase 1 (Landing page)
5. **Deploy incrementally** - Deploy setiap phase

---

**Ready to start? 🚀**


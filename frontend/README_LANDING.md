# 🎨 LANDING PAGE - INSTRUKSI PENGGUNAAN

**File yang dibuat:**
- `landing.html` - Landing page utama
- `css/landing.css` - Styles untuk landing page
- `js/landing.js` - JavaScript untuk landing page

---

## 📋 CARA MENGGUNAKAN

### **1. Buka Landing Page**

**Option 1: Langsung buka file**
```
Buka: frontend/landing.html di browser
```

**Option 2: Via local server**
```bash
cd frontend
python -m http.server 8000
# Buka: http://localhost:8000/landing.html
```

---

## 🎯 FITUR LANDING PAGE

### **Sections:**
1. **Navigation Bar**
   - Logo & brand name
   - Menu: Home, Paket, Fitur, FAQ
   - Login button

2. **Hero Section**
   - Judul besar dengan gradient text
   - Deskripsi
   - CTA buttons (Daftar Sekarang, Lihat Paket)
   - Statistics (500+ Members, 10K+ Reports, 55% Commission)

3. **Membership Plans**
   - Basic Member (Rp 97.000)
   - VIP Member (Rp 299.000) - dengan badge "POPULER"
   - Compare features
   - CTA buttons

4. **Features Section**
   - 6 feature cards dengan icons
   - Analytics Dashboard
   - Submit Report
   - Commission Tracking
   - Team Management
   - Real-time Notifications
   - Telegram Bot Integration

5. **FAQ Section**
   - Accordion style
   - 6 pertanyaan umum
   - Expandable answers

6. **CTA Section**
   - Call-to-action untuk daftar
   - Link ke register page

7. **Footer**
   - Company info
   - Quick links
   - Contact info

---

## 🔗 INTEGRASI

### **Link ke Register Page:**
Landing page sudah link ke `register.html` (akan dibuat nanti)

**Saat ini:**
- CTA buttons link ke `#register` (scroll ke CTA section)
- Plan buttons link ke `register.html`

### **Link ke Login:**
Navigation bar sudah link ke `index.html` (dashboard/login)

---

## 🎨 CUSTOMIZATION

### **Update Warna:**
Edit `css/landing.css`:
```css
:root {
    --primary-color: #667eea;      /* Warna utama */
    --secondary-color: #764ba2;    /* Warna sekunder */
    --accent-color: #f093fb;       /* Warna aksen */
}
```

### **Update Konten:**
Edit `landing.html`:
- Hero title & description
- Statistics numbers
- Features list
- FAQ questions
- Footer info

### **Update Rekening:**
Edit `landing.html` - cari section payment (akan ada di register page)

---

## 📱 RESPONSIVE

Landing page sudah **fully responsive**:
- ✅ Desktop (1920px+)
- ✅ Laptop (1024px+)
- ✅ Tablet (768px+)
- ✅ Mobile (320px+)

**Test di berbagai device atau gunakan browser DevTools**

---

## 🚀 DEPLOYMENT

### **Untuk Production:**

1. **Update Links:**
   - Pastikan semua link sudah benar
   - Update API URLs jika perlu

2. **Optimize:**
   - Minify CSS & JS (opsional)
   - Optimize images (jika ada)

3. **Deploy:**
   - Upload ke Vercel/Netlify
   - Atau hosting lainnya

---

## ✅ CHECKLIST

**Sebelum launch:**
- [ ] Test semua links
- [ ] Test responsive di berbagai device
- [ ] Update konten (statistics, features, FAQ)
- [ ] Update contact info di footer
- [ ] Test CTA buttons
- [ ] Test smooth scroll
- [ ] Test animations

---

## 🎯 NEXT STEPS

1. **Buat Register Page** (`register.html`)
   - Form registrasi
   - Payment proof upload
   - Integration dengan backend

2. **Update Navigation**
   - Pastikan semua links bekerja
   - Update login/register flow

3. **Deploy**
   - Setup hosting
   - Deploy landing page
   - Test production

---

**Landing page siap digunakan! 🎉**


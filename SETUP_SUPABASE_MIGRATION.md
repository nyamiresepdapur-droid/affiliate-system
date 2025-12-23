# 🗄️ SETUP SUPABASE DATABASE MIGRATION

**Langkah run migration di Supabase**

---

## 🎯 STEP 1: BUKA SUPABASE SQL EDITOR

1. **Buka:** https://supabase.com
2. **Login** → Pilih project `affiliate-system`
3. **Klik:** "SQL Editor" di sidebar kiri
4. **Klik:** "New query"

---

## 🎯 STEP 2: COPY MIGRATION SCRIPT

**Buka file:** `backend/migrations/create_tables.sql`

**Copy semua isinya** (atau buka file tersebut dan copy)

---

## 🎯 STEP 3: PASTE & RUN DI SUPABASE

1. **Paste** script migration ke SQL Editor
2. **Review** script (pastikan tidak ada error)
3. **Klik:** "Run" (atau tekan Ctrl+Enter / Cmd+Enter)
4. **Tunggu** sampai selesai
5. **Cek:** Harus muncul "Success. No rows returned" atau "Success"

---

## 🎯 STEP 4: VERIFY TABLES

**Run query untuk verify:**

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

**Harus muncul tables:**
- users
- products
- teams
- team_members
- content
- commissions
- payments
- manager_bonus
- daily_commissions
- video_statistics
- member_daily_summary
- notifications

---

## 🎯 STEP 5: VERIFY DEFAULT OWNER

**Run query:**

```sql
SELECT * FROM users WHERE username = 'owner';
```

**Harus ada 1 row** dengan role 'owner'

---

## 📋 CHECKLIST SUPABASE

- [ ] SQL Editor sudah dibuka
- [ ] Migration script sudah di-copy
- [ ] Script sudah di-paste ke SQL Editor
- [ ] Script sudah di-run
- [ ] Query berhasil (Success)
- [ ] Tables sudah dibuat (verify dengan query)
- [ ] Default owner sudah dibuat

---

## 🚨 TROUBLESHOOTING

### **Problem: "relation already exists"**
- Tables sudah ada (tidak masalah)
- Skip error atau drop tables dulu jika perlu

### **Problem: "permission denied"**
- Pastikan login sebagai project owner
- Cek project status (harus Active)

### **Problem: Syntax error**
- Cek script sudah lengkap
- Cek tidak ada typo
- Cek semua quotes sudah benar

---

**Run migration di Supabase sekarang! 🚀**


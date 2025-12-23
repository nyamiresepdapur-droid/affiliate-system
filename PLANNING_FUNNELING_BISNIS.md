# 📋 PLANNING MODEL BISNIS FUNNELING

**Tanggal:** 20 Desember 2025  
**Model:** 2-Tier Membership dengan Funnelling

---

## 🎯 OVERVIEW MODEL BISNIS

### **Tier 1: BASIC MEMBER (Rp 97.000)**
**Fasilitas:**
- ✅ Materi cara membuat konten dengan AI
- ✅ Tutorial dari dasar sampai upload konten
- ✅ Akses ke platform (website)
- ✅ Bisa submit report (tapi belum dapat komisi)

**Target:** User yang baru belajar, belum punya akun TikTok affiliate

---

### **Tier 2: VIP MEMBER (Rp 299.000)**
**Fasilitas:**
- ✅ Semua fasilitas Basic Member
- ✅ Group diskusi (Telegram/WhatsApp)
- ✅ Tanya jawab langsung dengan admin
- ✅ Zoom meeting (weekly/monthly)
- ✅ **Akun affiliate TikTok yang sudah jadi** (ada keranjang kuning)
- ✅ Reporting pekerjaan harian (divalidasi admin)
- ✅ **Sistem bagi hasil:**
  - User: **55%**
  - Leader (Sub ID): **5%**
  - Owner: **40%**

**Target:** User yang serius, sudah siap untuk monetize

---

## 💰 STRUKTUR BAGI HASIL

### **Commission Split:**
```
Total Commission: 100%
├── User (VIP Member): 55%
├── Leader (Sub ID): 5%
└── Owner: 40%
```

**Contoh:**
- Total komisi: Rp 100.000
- User dapat: Rp 55.000
- Leader dapat: Rp 5.000
- Owner dapat: Rp 40.000

---

## 🗄️ DATABASE SCHEMA

### **1. Membership Tiers Table**

```sql
CREATE TABLE membership_tiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_code VARCHAR(20) NOT NULL UNIQUE,  -- 'basic', 'vip'
    tier_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    features JSON,  -- List of features
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Data awal
INSERT INTO membership_tiers (tier_code, tier_name, price, description, features) VALUES
('basic', 'Basic Member', 97000, 'Materi AI Content Creation', '["Materi AI Content Creation", "Tutorial dasar sampai upload", "Akses platform"]'),
('vip', 'VIP Member', 299000, 'Full access dengan affiliate account', '["Semua Basic", "Group diskusi", "Tanya jawab", "Zoom meeting", "Akun TikTok affiliate", "Reporting & validasi", "Bagi hasil 55%"]');
```

---

### **2. User Memberships Table**

```sql
CREATE TABLE user_memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tier_code VARCHAR(20) NOT NULL,  -- 'basic', 'vip'
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'expired', 'cancelled'
    purchased_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,  -- NULL = lifetime
    payment_method VARCHAR(50),  -- 'bank_transfer', 'e_wallet', etc.
    payment_proof TEXT,  -- URL to payment proof image
    verified_by INTEGER,  -- Admin user_id yang verify
    verified_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tier_code) REFERENCES membership_tiers(tier_code),
    FOREIGN KEY (verified_by) REFERENCES users(id)
);

CREATE INDEX idx_user_memberships_user_id ON user_memberships(user_id);
CREATE INDEX idx_user_memberships_status ON user_memberships(status);
```

---

### **3. Upgrade Requests Table**

```sql
CREATE TABLE upgrade_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    from_tier VARCHAR(20),  -- Current tier
    to_tier VARCHAR(20) NOT NULL,  -- Target tier
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    payment_proof TEXT,  -- URL to payment proof
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'approved', 'rejected'
    notes TEXT,
    processed_by INTEGER,  -- Admin user_id
    processed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (processed_by) REFERENCES users(id)
);

CREATE INDEX idx_upgrade_requests_user_id ON upgrade_requests(user_id);
CREATE INDEX idx_upgrade_requests_status ON upgrade_requests(status);
```

---

### **4. Affiliate Accounts Table**

```sql
CREATE TABLE affiliate_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,  -- One account per VIP user
    tiktok_username VARCHAR(100) NOT NULL,
    tiktok_account_id VARCHAR(100),  -- TikTok account ID
    shop_id VARCHAR(100),  -- TikTok Shop ID
    shop_name VARCHAR(200),
    shop_status VARCHAR(20) DEFAULT 'active',  -- 'active', 'suspended', 'inactive'
    keranjang_kuning BOOLEAN DEFAULT 0,  -- Yellow cart status
    keranjang_kuning_verified_at DATETIME,
    credentials_encrypted TEXT,  -- Encrypted credentials (if needed)
    notes TEXT,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER,  -- Admin user_id
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE),
    FOREIGN KEY (assigned_by) REFERENCES users(id)
);

CREATE INDEX idx_affiliate_accounts_user_id ON affiliate_accounts(user_id);
CREATE INDEX idx_affiliate_accounts_shop_status ON affiliate_accounts(shop_status);
```

---

### **5. Commission Structure Table**

```sql
CREATE TABLE commission_structures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_code VARCHAR(20) NOT NULL,  -- 'basic', 'vip'
    user_percent DECIMAL(5, 2) NOT NULL,  -- 55.00
    leader_percent DECIMAL(5, 2) NOT NULL,  -- 5.00
    owner_percent DECIMAL(5, 2) NOT NULL,  -- 40.00
    is_active BOOLEAN DEFAULT 1,
    effective_from DATE NOT NULL,
    effective_to DATE,  -- NULL = ongoing
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tier_code) REFERENCES membership_tiers(tier_code)
);

-- Data awal untuk VIP
INSERT INTO commission_structures (tier_code, user_percent, leader_percent, owner_percent, effective_from) VALUES
('vip', 55.00, 5.00, 40.00, '2025-12-20');
```

---

### **6. User Hierarchy (Leader-Sub) Table**

```sql
CREATE TABLE user_hierarchy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    leader_id INTEGER NOT NULL,  -- User yang jadi leader
    sub_id INTEGER NOT NULL,  -- User yang di-bawahi
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'inactive'
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leader_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (sub_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(leader_id, sub_id)
);

CREATE INDEX idx_user_hierarchy_leader_id ON user_hierarchy(leader_id);
CREATE INDEX idx_user_hierarchy_sub_id ON user_hierarchy(sub_id);
```

---

### **7. Update Commission Table**

**Modifikasi existing `commissions` table:**
```sql
-- Add new columns
ALTER TABLE commissions ADD COLUMN tier_code VARCHAR(20);
ALTER TABLE commissions ADD COLUMN leader_id INTEGER;
ALTER TABLE commissions ADD COLUMN user_share DECIMAL(10, 2);
ALTER TABLE commissions ADD COLUMN leader_share DECIMAL(10, 2);
ALTER TABLE commissions ADD COLUMN owner_share DECIMAL(10, 2);

-- Update existing data
UPDATE commissions SET tier_code = 'vip' WHERE tier_code IS NULL;
```

---

## 🏗️ ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────┐
│              USER REGISTRATION & PAYMENT                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Basic Member │→ │  Upgrade     │→ │  VIP Member  │ │
│  │  Rp 97.000   │  │  Request     │  │  Rp 299.000  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────────────────────────────────────┐
│              VIP MEMBER ACTIVATION                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Assign TikTok│→ │  Assign Group │→ │  Activate    │ │
│  │  Account     │  │  Access      │  │  Commission  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────────────────────────────────────┐
│              COMMISSION CALCULATION                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ User Report  │→ │  Admin       │→ │  Calculate   │ │
│  │  Submission  │  │  Validation  │  │  Commission  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                          │                              │
│                          ↓                              │
│              ┌───────────────────────┐                  │
│              │ Split: 55% / 5% / 40% │                  │
│              └───────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 IMPLEMENTATION PLAN

### **PHASE 1: MEMBERSHIP SYSTEM (Week 1-2)**

#### **Week 1: Database & Models**
- [ ] Create membership_tiers table
- [ ] Create user_memberships table
- [ ] Create upgrade_requests table
- [ ] Create affiliate_accounts table
- [ ] Create commission_structures table
- [ ] Create user_hierarchy table
- [ ] Update Commission model dengan tier_code, leader_id, shares
- [ ] Add models ke `models.py`

#### **Week 2: Backend API**
- [ ] `GET /api/membership/tiers` - List semua tiers
- [ ] `GET /api/membership/my-membership` - Get current user membership
- [ ] `POST /api/membership/purchase` - Purchase membership
- [ ] `POST /api/membership/upgrade` - Request upgrade
- [ ] `GET /api/membership/upgrade-requests` - List upgrade requests (admin)
- [ ] `POST /api/membership/upgrade-requests/:id/approve` - Approve upgrade
- [ ] `POST /api/membership/upgrade-requests/:id/reject` - Reject upgrade
- [ ] `GET /api/affiliate-accounts` - List affiliate accounts (admin)
- [ ] `POST /api/affiliate-accounts/assign` - Assign account ke user
- [ ] `PUT /api/affiliate-accounts/:id` - Update account info

---

### **PHASE 2: PAYMENT & UPGRADE FLOW (Week 3-4)**

#### **Week 3: Payment Integration**
- [ ] Payment method selection (Bank Transfer, E-Wallet)
- [ ] Payment proof upload
- [ ] Payment verification by admin
- [ ] Auto-activate membership setelah verified
- [ ] Email/Telegram notification saat payment verified

#### **Week 4: Upgrade Flow**
- [ ] Upgrade request form
- [ ] Calculate upgrade price (299k - 97k = 202k)
- [ ] Payment proof upload untuk upgrade
- [ ] Admin approve/reject upgrade
- [ ] Auto-upgrade membership setelah verified
- [ ] Notification ke user

---

### **PHASE 3: AFFILIATE ACCOUNT MANAGEMENT (Week 5-6)**

#### **Week 5: Account Assignment**
- [ ] Admin interface untuk manage affiliate accounts
- [ ] Assign account ke VIP user
- [ ] Track account status (active, suspended)
- [ ] Verify keranjang kuning status
- [ ] Account credentials management (encrypted)

#### **Week 6: Account Monitoring**
- [ ] Dashboard untuk monitor semua accounts
- [ ] Account health check
- [ ] Alert jika account suspended
- [ ] Account performance tracking

---

### **PHASE 4: COMMISSION SYSTEM UPDATE (Week 7-8)**

#### **Week 7: Commission Calculation**
- [ ] Update commission calculation logic
- [ ] Check user tier (Basic = no commission, VIP = 55%)
- [ ] Find leader (Sub ID) untuk VIP user
- [ ] Calculate: User 55%, Leader 5%, Owner 40%
- [ ] Store breakdown di commission table

#### **Week 8: Leader System**
- [ ] Leader assignment (manual atau auto)
- [ ] Leader dashboard (lihat semua subs)
- [ ] Leader commission tracking
- [ ] Leader performance report

---

### **PHASE 5: REPORTING & VALIDATION (Week 9-10)**

#### **Week 9: VIP Reporting**
- [ ] Daily reporting untuk VIP members
- [ ] Report validation by admin
- [ ] Report status tracking
- [ ] Commission calculation dari validated reports

#### **Week 10: Admin Validation**
- [ ] Admin interface untuk validate reports
- [ ] Bulk validation
- [ ] Validation history
- [ ] Auto-calculate commission setelah validation

---

### **PHASE 6: GROUP & COMMUNITY (Week 11-12)**

#### **Week 11: Group Management**
- [ ] Telegram/WhatsApp group integration
- [ ] Auto-add VIP members ke group
- [ ] Group member list di dashboard
- [ ] Group activity tracking

#### **Week 12: Community Features**
- [ ] Q&A system
- [ ] Zoom meeting scheduler
- [ ] Meeting attendance tracking
- [ ] Community announcements

---

## 🎨 FRONTEND FEATURES

### **1. Membership Purchase Page**
```
┌─────────────────────────────────────┐
│  🎯 Pilih Membership Plan           │
├─────────────────────────────────────┤
│  [Basic Member]  [VIP Member]      │
│  Rp 97.000       Rp 299.000        │
│  ✅ Materi AI    ✅ Semua Basic     │
│  ✅ Tutorial     ✅ Group Diskusi   │
│                   ✅ TikTok Account │
│                   ✅ Bagi Hasil 55% │
│  [Beli Sekarang] [Upgrade ke VIP]   │
└─────────────────────────────────────┘
```

### **2. Upgrade Request Form**
```
┌─────────────────────────────────────┐
│  ⬆️ Upgrade ke VIP Member           │
├─────────────────────────────────────┤
│  Current: Basic Member              │
│  Upgrade to: VIP Member             │
│  Price: Rp 202.000 (299k - 97k)     │
│                                      │
│  Payment Method: [Select]            │
│  Payment Proof: [Upload Image]      │
│                                      │
│  [Submit Request]                    │
└─────────────────────────────────────┘
```

### **3. VIP Dashboard**
```
┌─────────────────────────────────────┐
│  👑 VIP Member Dashboard            │
├─────────────────────────────────────┤
│  ✅ TikTok Account: @username       │
│  ✅ Keranjang Kuning: Verified      │
│  ✅ Group Access: Active            │
│                                      │
│  📊 My Performance                  │
│  Total Commission: Rp 5.000.000    │
│  My Share (55%): Rp 2.750.000      │
│  Pending: Rp 500.000               │
│                                      │
│  📝 Daily Report                    │
│  [Submit Report]                    │
└─────────────────────────────────────┘
```

### **4. Admin - Affiliate Account Management**
```
┌─────────────────────────────────────┐
│  📱 Affiliate Accounts              │
├─────────────────────────────────────┤
│  [Add Account] [Import CSV]         │
│                                      │
│  Account List:                      │
│  ┌──────────────────────────────┐  │
│  │ @username1 | Available |     │  │
│  │ [Assign to User]              │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ @username2 | Assigned |      │  │
│  │ User: John Doe               │  │
│  │ [View Details] [Unassign]    │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 💰 COMMISSION CALCULATION LOGIC

### **Flow:**
```python
def calculate_commission(report_id, total_commission):
    # 1. Get report
    report = Content.query.get(report_id)
    user = User.query.get(report.creator_id)
    
    # 2. Check user membership
    membership = get_active_membership(user.id)
    if membership.tier_code != 'vip':
        # Basic member tidak dapat komisi
        return None
    
    # 3. Get commission structure
    commission_structure = get_commission_structure('vip')
    
    # 4. Find leader (Sub ID)
    leader = get_leader(user.id)
    
    # 5. Calculate shares
    user_share = total_commission * (commission_structure.user_percent / 100)      # 55%
    leader_share = total_commission * (commission_structure.leader_percent / 100) if leader else 0  # 5%
    owner_share = total_commission * (commission_structure.owner_percent / 100)    # 40%
    
    # 6. Create commission record
    commission = Commission(
        content_id=report_id,
        creator_id=user.id,
        tier_code='vip',
        leader_id=leader.id if leader else None,
        total_commission=total_commission,
        user_share=user_share,
        leader_share=leader_share,
        owner_share=owner_share,
        status='pending'
    )
    
    return commission
```

---

## 🔄 USER FLOW

### **Flow 1: New User → Basic Member**
```
1. User register
2. User pilih "Basic Member" (Rp 97.000)
3. User upload payment proof
4. Admin verify payment
5. User jadi Basic Member
6. User dapat akses materi AI
```

### **Flow 2: Basic → VIP Upgrade**
```
1. Basic Member klik "Upgrade ke VIP"
2. System calculate: 299k - 97k = 202k
3. User upload payment proof untuk 202k
4. Admin verify payment
5. User jadi VIP Member
6. Admin assign TikTok account
7. User dapat akses semua VIP features
8. User mulai dapat komisi 55%
```

### **Flow 3: VIP Member Report & Commission**
```
1. VIP Member submit daily report
2. Admin validate report
3. System calculate commission
4. Commission split:
   - User: 55%
   - Leader: 5% (jika ada)
   - Owner: 40%
5. User dapat notification
6. Commission masuk ke balance
```

---

## 📊 ADMIN DASHBOARD ADDITIONS

### **New Sections:**
1. **Membership Management**
   - List semua memberships
   - Filter by tier
   - View payment proofs
   - Approve/reject payments

2. **Upgrade Requests**
   - List semua upgrade requests
   - View payment proofs
   - Approve/reject upgrades
   - Auto-upgrade setelah approve

3. **Affiliate Accounts**
   - List semua accounts
   - Assign/unassign accounts
   - Track account status
   - Monitor account health

4. **Leader Management**
   - Assign leaders
   - View leader hierarchy
   - Leader performance
   - Leader commission tracking

---

## 🎯 PRIORITY IMPLEMENTATION ORDER

### **Must Have (MVP):**
1. ✅ Membership tiers (Basic & VIP)
2. ✅ Payment & upgrade flow
3. ✅ Commission calculation (55/5/40)
4. ✅ VIP reporting system

### **Should Have:**
5. ✅ Affiliate account assignment
6. ✅ Leader system
7. ✅ Group access management

### **Nice to Have:**
8. ✅ Q&A system
9. ✅ Zoom meeting scheduler
10. ✅ Advanced analytics

---

## 📈 SUCCESS METRICS

**Track:**
- Conversion rate: Basic → VIP
- Average time to upgrade
- VIP member retention
- Commission payout rate
- Leader performance
- Account utilization rate

**Target:**
- 30% Basic → VIP conversion
- 80% VIP retention rate
- 90% commission payout accuracy

---

## 🚀 NEXT STEPS

1. **Review planning** - Pastikan sesuai kebutuhan
2. **Start Phase 1** - Database & models
3. **Test payment flow** - Pastikan payment verification works
4. **Deploy MVP** - Launch Basic & VIP membership
5. **Iterate** - Based on user feedback

---

**Ready to start implementation?** 🚀


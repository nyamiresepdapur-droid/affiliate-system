# 🔧 CONFIGURATION VALUES - TEMPLATE

**Template untuk update configuration**

---

## 📋 RAILWAY BACKEND URL

**Format:**
```
https://your-service-name.up.railway.app
```

**API URL:**
```
https://your-service-name.up.railway.app/api
```

**Contoh:**
```
https://affiliate-system-production.up.railway.app
https://affiliate-system-production.up.railway.app/api
```

---

## 📋 VERCEL FRONTEND URL

**Format:**
```
https://your-project-name.vercel.app
```

**Contoh:**
```
https://affiliate-system-xxx.vercel.app
```

---

## 📋 ENVIRONMENT VARIABLES

### **Vercel:**
```env
API_URL=https://your-backend.railway.app/api
```

### **Railway:**
```env
DATABASE_URL=postgresql://postgres:1Milyarberkah$@db.xxx.supabase.co:5432/postgres
SECRET_KEY=9b678373c6c215507d36689ad6b2aa57afce8103ad94fabfc1adb1017f329f6f
JWT_SECRET_KEY=4d06d8665369ccb52dc30557f20f4613c5d97c0eb618665f2151b226328c8a4a
FLASK_ENV=production
TELEGRAM_TOKEN=your-telegram-token
FRONTEND_URL=https://your-app.vercel.app
```

---

## 🎯 QUICK UPDATE

**1. Vercel:**
- Settings → Environment Variables → Add `API_URL`

**2. Railway:**
- Variables → Add/Update `FRONTEND_URL`

**3. Test:**
- Frontend → Test API call
- Backend → Test health endpoint

---

**Ganti URL dengan URL asli Anda! 🚀**


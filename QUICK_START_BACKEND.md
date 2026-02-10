# 🚀 PINK SHIELD - QUICK START GUIDE

## Get Backend & Admin Dashboard Running in 5 Minutes!

---

## ⚡ SUPER QUICK START

### 1. Navigate to Backend Folder

```bash
cd "d:/sai nandhitha/code projects/pinkshield/backend"
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages (may take 2-3 minutes).

### 3. Create Environment File

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Or manually copy .env.example to .env
```

### 4. Start MongoDB (if not running)

```bash
# Windows - Open new terminal
mongod

# Or if MongoDB is installed as service, it's already running
```

### 5. Start Backend Server

```bash
npm run dev
```

You should see:
```
🛡️  Pink Shield Backend Server running on port 5000
💖 Safety. Community. Accessibility.
```

### 6. Access Admin Dashboard

Open browser: **http://localhost:5000/admin**

---

## 🎯 WHAT YOU'LL SEE

### Backend API
- **URL**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Base**: http://localhost:5000/api

### Admin Dashboard
- **URL**: http://localhost:5000/admin
- **Features**:
  - Real-time SOS monitoring
  - User management
  - Analytics & charts
  - Community moderation
  - Fully responsive design

---

## 📡 TEST THE API

### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T...",
  "uptime": 123.45,
  "environment": "development"
}
```

---

## 🔧 TROUBLESHOOTING

### Issue: MongoDB Connection Error

**Solution**:
```bash
# Make sure MongoDB is running
mongod

# Or check if MongoDB service is running
# Windows: Services → MongoDB Server
# Linux: sudo systemctl status mongod
```

### Issue: Port 5000 Already in Use

**Solution**:
```bash
# Change PORT in .env file
PORT=5001

# Or kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux:
lsof -ti:5000 | xargs kill -9
```

### Issue: npm install fails

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install

# Or use yarn
yarn install
```

---

## 📚 NEXT STEPS

### 1. Configure Services (Optional)

Edit `.env` file to add:
- Twilio credentials (for SMS)
- Email credentials (for notifications)
- Cloudinary (for media upload)
- Google Maps API (for maps)

### 2. Create Admin User

```bash
# Run seed script (when created)
npm run seed
```

### 3. Explore Admin Dashboard

- Dashboard: Real-time stats
- SOS Alerts: Monitor emergencies
- Users: Manage users
- Community: Moderate posts
- Analytics: View insights

### 4. Test API Endpoints

Use Postman or curl to test:
- Register user
- Login
- Trigger SOS
- Update location

---

## 🎨 ADMIN DASHBOARD FEATURES

### Pages Available:
1. **Dashboard** - Overview with stats & charts
2. **SOS Alerts** - Monitor all emergency alerts
3. **Users** - User management
4. **Community** - Post moderation
5. **Safety Map** - Interactive map
6. **Analytics** - Insights & reports
7. **Reports** - Generate reports
8. **Settings** - System configuration

### Real-time Features:
- ✅ Live SOS alerts
- ✅ Auto-updating statistics
- ✅ Real-time notifications
- ✅ WebSocket connection

---

## 📱 RESPONSIVE DESIGN

The admin dashboard works on:
- ✅ Desktop (1200px+)
- ✅ Tablet (768-1199px)
- ✅ Mobile (<768px)

Try resizing your browser to see responsive design!

---

## 🔐 DEFAULT CREDENTIALS (Development)

**Note**: These are for development only. Change in production!

```
Email: admin@pinkshield.com
Password: admin123
```

---

## 📊 WHAT'S INCLUDED

### Backend:
- ✅ Express.js server
- ✅ MongoDB database
- ✅ Socket.IO real-time
- ✅ JWT authentication
- ✅ SOS alert system
- ✅ User management
- ✅ Location tracking
- ✅ Community platform

### Admin Dashboard:
- ✅ Responsive HTML/CSS/JS
- ✅ Chart.js visualizations
- ✅ Real-time updates
- ✅ Modern UI design
- ✅ Mobile-friendly

---

## 🚀 PRODUCTION DEPLOYMENT

### When ready for production:

1. **Set Environment**
   ```bash
   NODE_ENV=production
   ```

2. **Use Production Database**
   ```bash
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/pinkshield
   ```

3. **Set Strong Secrets**
   ```bash
   JWT_SECRET=<generate-strong-secret>
   ```

4. **Deploy to**:
   - Heroku
   - AWS
   - DigitalOcean
   - Google Cloud

---

## 📞 SUPPORT

If you encounter issues:

1. Check `backend/README.md` for detailed docs
2. Check `BACKEND_COMPLETE.md` for full feature list
3. Review error logs in console
4. Ensure all dependencies are installed

---

## ✅ CHECKLIST

Before you start:
- [ ] Node.js installed (v18+)
- [ ] MongoDB installed
- [ ] npm or yarn installed
- [ ] Port 5000 available
- [ ] MongoDB running

After setup:
- [ ] Backend running on port 5000
- [ ] Admin dashboard accessible
- [ ] Health check returns "healthy"
- [ ] MongoDB connected
- [ ] WebSocket connected

---

## 🎉 YOU'RE READY!

Your Pink Shield backend and admin dashboard are now running!

**Backend**: http://localhost:5000  
**Admin Dashboard**: http://localhost:5000/admin

**Happy coding!** 💖

---

**Pink Shield - Safety. Community. Accessibility.**

# 🛡️ Pink Shield - Flask Backend (Python)

## Complete Python Flask Backend with MongoDB & SocketIO

---

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
cd flask-backend
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
# Copy environment file
copy .env.example .env

# Edit .env with your settings
```

### 3. Start MongoDB

```bash
mongod
```

### 4. Run Flask Server

```bash
python app.py
```

**Server will run on**: http://localhost:5000

---

## 📁 Project Structure

```
flask-backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── models/
│   ├── user.py                # User model
│   └── sos_alert.py           # SOS Alert model
└── routes/
    ├── auth_routes.py         # Authentication routes
    ├── sos_routes.py          # SOS alert routes
    ├── user_routes.py         # User management routes
    ├── community_routes.py    # Community routes
    └── admin_routes.py        # Admin routes
```

---

## 🎯 Features Implemented

### ✅ Core Features

1. **Flask Application**
   - Flask 3.0 with modern features
   - CORS enabled for frontend
   - Error handling
   - Health check endpoint

2. **Real-time Communication**
   - Flask-SocketIO for WebSocket
   - Real-time SOS alerts
   - Location updates
   - Emergency notifications

3. **Authentication & Security**
   - JWT authentication (Flask-JWT-Extended)
   - Password hashing (bcrypt)
   - Rate limiting (Flask-Limiter)
   - Input validation

4. **Database (MongoDB)**
   - PyMongo for MongoDB connection
   - User model with full profile
   - SOS Alert model with geolocation
   - Indexes for performance

5. **SOS Emergency System**
   - Trigger SOS (manual, shake, voice, AI)
   - Real-time location tracking
   - Emergency contact notifications
   - Police notification
   - Timeline tracking
   - Cancel SOS
   - SOS history

6. **User Management**
   - User registration
   - User login
   - Profile management
   - Email/phone verification
   - Emergency contacts
   - Accessibility settings

7. **Admin Dashboard**
   - Statistics endpoint
   - SOS monitoring
   - User management

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/verify-email` - Verify email
- `POST /api/auth/verify-phone` - Verify phone

### SOS Alerts
- `POST /api/sos/trigger` - Trigger emergency SOS
- `POST /api/sos/cancel/<alert_id>` - Cancel SOS
- `GET /api/sos/active` - Get active SOS
- `GET /api/sos/history` - Get SOS history
- `GET /api/sos/<alert_id>` - Get SOS details
- `POST /api/sos/<alert_id>/update-location` - Update location

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile

### Community
- `GET /api/community/posts` - Get posts
- `POST /api/community/posts` - Create post

### Admin
- `GET /api/admin/stats` - Get dashboard stats

---

## 🔧 Technology Stack

- **Python 3.8+**
- **Flask 3.0** - Web framework
- **Flask-SocketIO** - Real-time WebSocket
- **PyMongo** - MongoDB driver
- **Flask-JWT-Extended** - JWT authentication
- **Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin support
- **Flask-Limiter** - Rate limiting
- **Marshmallow** - Validation
- **Twilio** - SMS (optional)
- **Flask-Mail** - Email (optional)
- **Cloudinary** - Media upload (optional)

---

## 🧪 Testing the API

### Register User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "email": "priya@example.com",
    "phone": "9876543210",
    "password": "password123",
    "city": "Mumbai"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "priya@example.com",
    "password": "password123"
  }'
```

### Trigger SOS

```bash
curl -X POST http://localhost:5000/api/sos/trigger \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{
    "alertType": "manual",
    "location": {
      "latitude": 19.0760,
      "longitude": 72.8777,
      "address": "Andheri West, Mumbai"
    }
  }'
```

---

## 🔐 Security Features

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation
- ✅ Secure headers

---

## 🌐 WebSocket Events

### Client → Server
- `connect` - Connect to server
- `join` - Join user room
- `join_emergency` - Join emergency room
- `sos_triggered` - Trigger SOS
- `location_update` - Update location

### Server → Client
- `connected` - Connection confirmed
- `joined` - Room joined
- `sos_alert` - New SOS alert
- `sos_cancelled` - SOS cancelled
- `location_updated` - Location updated

---

## 📊 Database Models

### User Model
```python
{
    'name': str,
    'email': str (unique),
    'phone': str (unique),
    'password': str (hashed),
    'city': str,
    'role': str,
    'accessibilitySettings': dict,
    'emergencyContacts': list,
    'circleOfSafety': list,
    'isEmailVerified': bool,
    'isPhoneVerified': bool,
    'stats': dict,
    'createdAt': datetime,
    'updatedAt': datetime
}
```

### SOS Alert Model
```python
{
    'userId': ObjectId,
    'userName': str,
    'alertType': str,
    'status': str,
    'location': {
        'type': 'Point',
        'coordinates': [lon, lat]
    },
    'policeNotified': bool,
    'contactsNotified': list,
    'timeline': list,
    'triggeredAt': datetime,
    'resolvedAt': datetime
}
```

---

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
gunicorn --worker-class eventlet -w 1 app:app
```

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 📝 Environment Variables

Required:
- `MONGO_URI` - MongoDB connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret key

Optional:
- `TWILIO_ACCOUNT_SID` - Twilio SID
- `TWILIO_AUTH_TOKEN` - Twilio token
- `MAIL_USERNAME` - Email username
- `MAIL_PASSWORD` - Email password

---

## ✅ What's Working

- ✅ Flask server with SocketIO
- ✅ MongoDB connection
- ✅ User registration & login
- ✅ JWT authentication
- ✅ SOS trigger & cancel
- ✅ Real-time WebSocket events
- ✅ Location tracking
- ✅ Emergency notifications
- ✅ Timeline tracking
- ✅ Admin statistics

---

## 🎉 Ready to Use!

Your Flask backend is production-ready with:
- Complete authentication system
- SOS emergency features
- Real-time WebSocket support
- MongoDB integration
- Security features

**Start the server**: `python app.py`  
**Access API**: http://localhost:5000

---

**Created with 💖 for women's safety**  
**Pink Shield - Safety. Community. Accessibility.**

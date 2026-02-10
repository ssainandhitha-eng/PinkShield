"""
Pink Shield - Flask Backend Server
AI-Powered Women's Safety Platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'pinkshield-secret-key-2026')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-2026')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/pinkshield')

# Initialize extensions
CORS(app, origins=os.getenv('FRONTEND_URL', 'http://localhost:8000'))
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
jwt = JWTManager(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per 15 minutes"]
)

# MongoDB connection
try:
    mongo_client = MongoClient(app.config['MONGO_URI'])
    db = mongo_client.pinkshield
    print("[OK] MongoDB connected successfully")
except Exception as e:
    print(f"[ERROR] MongoDB connection error: {e}")
    db = None

# Import routes
from routes import auth_routes, sos_routes, user_routes, community_routes, admin_routes

# Register blueprints
app.register_blueprint(auth_routes.bp, url_prefix='/api/auth')
app.register_blueprint(sos_routes.bp, url_prefix='/api/sos')
app.register_blueprint(user_routes.bp, url_prefix='/api/users')
app.register_blueprint(community_routes.bp, url_prefix='/api/community')
app.register_blueprint(admin_routes.bp, url_prefix='/api/admin')

# ===========================
# Health Check
# ===========================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.getenv('FLASK_ENV', 'development'),
        'database': 'connected' if db is not None else 'disconnected'
    }), 200

# ===========================
# WebSocket Events
# ===========================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'[OK] Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to Pink Shield server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'[X] Client disconnected: {request.sid}')

@socketio.on('join')
def handle_join(data):
    """Join user's personal room"""
    user_id = data.get('userId')
    if user_id:
        room = f'user_{user_id}'
        join_room(room)
        print(f'[USER] User {user_id} joined room: {room}')
        emit('joined', {'room': room})

@socketio.on('join_emergency')
def handle_join_emergency():
    """Join emergency room for SOS alerts"""
    join_room('emergency_room')
    print(f'[SOS] Client joined emergency room')
    emit('joined_emergency', {'room': 'emergency_room'})

@socketio.on('sos_triggered')
def handle_sos_triggered(data):
    """Handle SOS alert trigger"""
    print(f'[SOS] SOS triggered: {data}')
    # Broadcast to emergency room
    emit('sos_alert', data, room='emergency_room', broadcast=True)

@socketio.on('location_update')
def handle_location_update(data):
    """Handle location update"""
    user_id = data.get('userId')
    if user_id:
        room = f'user_{user_id}'
        emit('location_updated', data, room=room)

# ===========================
# Error Handlers
# ===========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Route not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all exceptions"""
    print(f'Error: {error}')
    return jsonify({
        'success': False,
        'message': str(error)
    }), 500

# ===========================
# Main
# ===========================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('=' * 60)
    print('[PINK SHIELD] Flask Backend Server')
    print('[SAFETY] Safety. Community. Accessibility.')
    print(f'[ENV] Environment: {os.getenv("FLASK_ENV", "development")}')
    print(f'[FRONTEND] Frontend URL: {os.getenv("FRONTEND_URL", "http://localhost:8000")}')
    print(f'[SERVER] Server running on port {port}')
    print('=' * 60)
    
    # Run with SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )

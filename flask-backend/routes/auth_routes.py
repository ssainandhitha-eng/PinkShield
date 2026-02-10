"""
Authentication Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from datetime import timedelta
import re

bp = Blueprint('auth', __name__)

def get_db():
    """Get database instance"""
    from app import db
    return db

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'email', 'phone', 'password', 'city']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Validate email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data['email']):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate phone
        phone_regex = r'^\d{10}$'
        if not re.match(phone_regex, data['phone']):
            return jsonify({
                'success': False,
                'message': 'Phone must be 10 digits'
            }), 400
        
        # Validate password
        if len(data['password']) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters'
            }), 400
        
        # Check if user exists
        user_model = User(get_db())
        
        if user_model.find_by_email(data['email']):
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 400
        
        if user_model.find_by_phone(data['phone']):
            return jsonify({
                'success': False,
                'message': 'Phone already registered'
            }), 400
        
        # Create user
        user = user_model.create_user(data)
        
        # Generate token
        access_token = create_access_token(
            identity=str(user['_id']),
            expires_delta=timedelta(days=7)
        )
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'userId': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'token': access_token
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user_model = User(get_db())
        user = user_model.find_by_email(data['email'])
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Verify password
        if not user_model.verify_password(user, data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Check if account is active
        if not user.get('isActive'):
            return jsonify({
                'success': False,
                'message': 'Account is deactivated'
            }), 403
        
        if user.get('isBanned'):
            return jsonify({
                'success': False,
                'message': 'Account is banned'
            }), 403
        
        # Update last login
        from datetime import datetime
        user_model.update_user(str(user['_id']), {'lastLogin': datetime.utcnow()})
        
        # Generate token
        access_token = create_access_token(
            identity=str(user['_id']),
            expires_delta=timedelta(days=7)
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'userId': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'token': access_token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/verify-email', methods=['POST'])
@jwt_required()
def verify_email():
    """Verify user email"""
    try:
        user_id = get_jwt_identity()
        user_model = User(get_db())
        
        # Update verification status
        user_model.update_user(user_id, {'isEmailVerified': True})
        
        return jsonify({
            'success': True,
            'message': 'Email verified successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/verify-phone', methods=['POST'])
@jwt_required()
def verify_phone():
    """Verify user phone"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # In production, verify OTP here
        otp = data.get('otp')
        
        user_model = User(get_db())
        user_model.update_user(user_id, {'isPhoneVerified': True})
        
        return jsonify({
            'success': True,
            'message': 'Phone verified successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

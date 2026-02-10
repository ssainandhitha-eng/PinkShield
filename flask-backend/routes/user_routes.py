"""User Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

bp = Blueprint('users', __name__)

def get_db():
    from app import db
    return db

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user_model = User(get_db())
        user = user_model.find_by_id(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Remove sensitive data
        user.pop('password', None)
        user['_id'] = str(user['_id'])
        
        return jsonify({'success': True, 'data': user}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Remove fields that shouldn't be updated this way
        data.pop('password', None)
        data.pop('email', None)
        data.pop('phone', None)
        
        user_model = User(get_db())
        user_model.update_user(user_id, data)
        
        return jsonify({'success': True, 'message': 'Profile updated'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

"""Community Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('community', __name__)

@bp.route('/posts', methods=['GET'])
def get_posts():
    """Get community posts"""
    return jsonify({'success': True, 'data': [], 'message': 'Community posts'}), 200

@bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create community post"""
    return jsonify({'success': True, 'message': 'Post created'}), 201

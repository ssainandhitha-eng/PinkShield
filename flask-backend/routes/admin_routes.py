"""Admin Routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.sos_alert import SOSAlert
from models.user import User

bp = Blueprint('admin', __name__)

def get_db():
    from app import db
    return db

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get dashboard statistics"""
    try:
        sos_model = SOSAlert(get_db())
        stats = sos_model.get_statistics()
        
        user_model = User(get_db())
        total_users = user_model.collection.count_documents({})
        
        return jsonify({
            'success': True,
            'data': {
                'activeSOS': stats['active'],
                'totalUsers': total_users,
                'resolvedToday': stats['resolved'],
                'avgResponse': 87  # Simulated
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

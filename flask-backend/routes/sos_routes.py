"""
SOS Alert Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit
from models.sos_alert import SOSAlert
from models.user import User
from datetime import datetime

bp = Blueprint('sos', __name__)

def get_db():
    """Get database instance"""
    from app import db
    return db

def get_socketio():
    """Get SocketIO instance"""
    from app import socketio
    return socketio

@bp.route('/trigger', methods=['POST'])
@jwt_required()
def trigger_sos():
    """Trigger emergency SOS"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get user details
        user_model = User(get_db())
        user = user_model.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Validate location
        if not data.get('location') or not data['location'].get('latitude') or not data['location'].get('longitude'):
            return jsonify({
                'success': False,
                'message': 'Location is required'
            }), 400
        
        # Create SOS alert
        sos_model = SOSAlert(get_db())
        alert_data = {
            'userId': user_id,
            'userName': user['name'],
            'userPhone': user['phone'],
            'alertType': data.get('alertType', 'manual'),
            'location': data['location'],
            'deviceInfo': data.get('deviceInfo', {}),
            'aiAnalysis': data.get('aiAnalysis', {})
        }
        
        alert = sos_model.create_alert(alert_data)
        
        # Notify emergency contacts (simulated)
        contacts_notified = []
        for contact in user.get('emergencyContacts', []):
            contact_data = {
                'name': contact['name'],
                'phone': contact['phone'],
                'notifiedAt': datetime.utcnow(),
                'notificationMethod': 'sms',
                'acknowledged': False
            }
            sos_model.add_contact_notified(str(alert['_id']), contact_data)
            contacts_notified.append(contact_data)
            
            # Simulate SMS (in production, use Twilio)
            print(f"📱 SMS to {contact['phone']}: 🆘 EMERGENCY! {user['name']} needs help!")
        
        # Mark police notified (simulated)
        sos_model.mark_police_notified(str(alert['_id']))
        sos_model.add_timeline_event(
            str(alert['_id']),
            'Police Notified',
            'Local police station notified',
            'system'
        )
        
        # Increment user stats
        user_model.increment_stat(user_id, 'sosTriggered')
        
        # Emit real-time event
        socketio = get_socketio()
        socketio.emit('sos_alert', {
            'alertId': str(alert['_id']),
            'userId': user_id,
            'userName': user['name'],
            'location': data['location'],
            'severity': 'critical',
            'timestamp': datetime.utcnow().isoformat()
        }, room='emergency_room')
        
        print(f"🆘 SOS triggered by user {user_id} - Alert ID: {alert['_id']}")
        
        return jsonify({
            'success': True,
            'message': 'SOS alert triggered successfully',
            'data': {
                'alertId': str(alert['_id']),
                'status': alert['status'],
                'policeNotified': alert['policeNotified'],
                'contactsNotified': len(contacts_notified),
                'triggeredAt': alert['triggeredAt'].isoformat()
            }
        }), 201
        
    except Exception as e:
        print(f"Error triggering SOS: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/cancel/<alert_id>', methods=['POST'])
@jwt_required()
def cancel_sos(alert_id):
    """Cancel active SOS"""
    try:
        user_id = get_jwt_identity()
        
        # Find alert
        sos_model = SOSAlert(get_db())
        alert = sos_model.find_by_id(alert_id)
        
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        # Verify ownership
        if str(alert['userId']) != user_id:
            return jsonify({
                'success': False,
                'message': 'Not authorized'
            }), 403
        
        # Check if active
        if alert['status'] != 'active':
            return jsonify({
                'success': False,
                'message': 'Alert is not active'
            }), 400
        
        # Update status
        sos_model.update_status(alert_id, 'cancelled')
        sos_model.add_timeline_event(
            alert_id,
            'SOS Cancelled',
            'User cancelled the alert',
            alert['userName']
        )
        
        # Emit real-time event
        socketio = get_socketio()
        socketio.emit('sos_cancelled', {
            'alertId': alert_id,
            'userId': user_id,
            'userName': alert['userName']
        }, room='emergency_room')
        
        print(f"✅ SOS cancelled by user {user_id} - Alert ID: {alert_id}")
        
        return jsonify({
            'success': True,
            'message': 'SOS alert cancelled successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/active', methods=['GET'])
@jwt_required()
def get_active_sos():
    """Get active SOS alerts for user"""
    try:
        user_id = get_jwt_identity()
        
        sos_model = SOSAlert(get_db())
        alerts = sos_model.find_active_by_user(user_id)
        
        # Convert ObjectId to string
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            alert['userId'] = str(alert['userId'])
        
        return jsonify({
            'success': True,
            'count': len(alerts),
            'data': alerts
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_sos_history():
    """Get SOS history for user"""
    try:
        user_id = get_jwt_identity()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        sos_model = SOSAlert(get_db())
        alerts = sos_model.find_by_user(user_id, limit, skip)
        
        # Convert ObjectId to string
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            alert['userId'] = str(alert['userId'])
        
        return jsonify({
            'success': True,
            'data': alerts,
            'pagination': {
                'page': page,
                'limit': limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/<alert_id>', methods=['GET'])
@jwt_required()
def get_sos_details(alert_id):
    """Get specific SOS alert details"""
    try:
        user_id = get_jwt_identity()
        
        sos_model = SOSAlert(get_db())
        alert = sos_model.find_by_id(alert_id)
        
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        # Verify ownership
        if str(alert['userId']) != user_id:
            return jsonify({
                'success': False,
                'message': 'Not authorized'
            }), 403
        
        # Convert ObjectId to string
        alert['_id'] = str(alert['_id'])
        alert['userId'] = str(alert['userId'])
        
        return jsonify({
            'success': True,
            'data': alert
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/<alert_id>/update-location', methods=['POST'])
@jwt_required()
def update_location(alert_id):
    """Update location during active SOS"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Find alert
        sos_model = SOSAlert(get_db())
        alert = sos_model.find_by_id(alert_id)
        
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        # Verify ownership
        if str(alert['userId']) != user_id:
            return jsonify({
                'success': False,
                'message': 'Not authorized'
            }), 403
        
        # Update location
        location = {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'accuracy': data.get('accuracy'),
            'address': data.get('address')
        }
        
        sos_model.update_location(alert_id, location)
        sos_model.add_timeline_event(
            alert_id,
            'Location Updated',
            f"New location: {location.get('address', 'Unknown')}"
        )
        
        # Emit real-time update
        socketio = get_socketio()
        socketio.emit('sos_location_update', {
            'alertId': alert_id,
            'location': location
        }, room='emergency_room')
        
        return jsonify({
            'success': True,
            'message': 'Location updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

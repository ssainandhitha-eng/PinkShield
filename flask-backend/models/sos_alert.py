"""
SOS Alert Model
"""

from datetime import datetime
from bson import ObjectId

class SOSAlert:
    """SOS Alert model for emergency situations"""
    
    def __init__(self, db):
        self.collection = db.sos_alerts
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        self.collection.create_index('userId')
        self.collection.create_index('status')
        self.collection.create_index('triggeredAt')
        self.collection.create_index([('location', '2dsphere')])
    
    def create_alert(self, data):
        """Create a new SOS alert"""
        alert = {
            'userId': ObjectId(data['userId']),
            'userName': data.get('userName'),
            'userPhone': data.get('userPhone'),
            
            # Alert Details
            'alertType': data.get('alertType', 'manual'),
            'status': 'active',
            'severity': data.get('severity', 'critical'),
            
            # Location (GeoJSON)
            'location': {
                'type': 'Point',
                'coordinates': [
                    data['location']['longitude'],
                    data['location']['latitude']
                ],
                'address': data['location'].get('address'),
                'city': data['location'].get('city'),
                'state': data['location'].get('state'),
                'accuracy': data['location'].get('accuracy')
            },
            
            # Device Information
            'deviceInfo': data.get('deviceInfo', {}),
            
            # Emergency Response
            'policeNotified': False,
            'policeNotifiedAt': None,
            'policeStationId': None,
            'policeResponse': {},
            
            # Contacts Notified
            'contactsNotified': [],
            
            # Recording & Evidence
            'recording': {
                'audio': None,
                'video': None,
                'photos': []
            },
            
            # AI Analysis
            'aiAnalysis': data.get('aiAnalysis', {}),
            
            # Timeline
            'timeline': [{
                'timestamp': datetime.utcnow(),
                'event': 'SOS Triggered',
                'details': f'Alert triggered via {data.get("alertType", "manual")}',
                'performedBy': data.get('userName', 'User')
            }],
            
            # Timestamps
            'triggeredAt': datetime.utcnow(),
            'resolvedAt': None,
            'cancelledAt': None,
            
            # Resolution
            'resolvedBy': None,
            'resolutionNotes': None,
            'outcome': None,
            
            # Additional
            'notes': None,
            'tags': []
        }
        
        result = self.collection.insert_one(alert)
        alert['_id'] = result.inserted_id
        return alert
    
    def find_by_id(self, alert_id):
        """Find alert by ID"""
        return self.collection.find_one({'_id': ObjectId(alert_id)})
    
    def find_active_by_user(self, user_id):
        """Find active alerts for user"""
        return list(self.collection.find({
            'userId': ObjectId(user_id),
            'status': 'active'
        }).sort('triggeredAt', -1))
    
    def find_by_user(self, user_id, limit=20, skip=0):
        """Find all alerts for user"""
        return list(self.collection.find({
            'userId': ObjectId(user_id)
        }).sort('triggeredAt', -1).skip(skip).limit(limit))
    
    def update_status(self, alert_id, status):
        """Update alert status"""
        update_data = {
            'status': status,
            'updatedAt': datetime.utcnow()
        }
        
        if status == 'cancelled':
            update_data['cancelledAt'] = datetime.utcnow()
        elif status == 'resolved':
            update_data['resolvedAt'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def update_location(self, alert_id, location):
        """Update alert location"""
        result = self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {
                '$set': {
                    'location.coordinates': [
                        location['longitude'],
                        location['latitude']
                    ],
                    'location.accuracy': location.get('accuracy'),
                    'location.address': location.get('address')
                }
            }
        )
        return result.modified_count > 0
    
    def add_timeline_event(self, alert_id, event, details, performed_by='system'):
        """Add event to timeline"""
        timeline_event = {
            'timestamp': datetime.utcnow(),
            'event': event,
            'details': details,
            'performedBy': performed_by
        }
        
        result = self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {'$push': {'timeline': timeline_event}}
        )
        return result.modified_count > 0
    
    def add_contact_notified(self, alert_id, contact):
        """Add notified contact"""
        result = self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {'$push': {'contactsNotified': contact}}
        )
        return result.modified_count > 0
    
    def mark_police_notified(self, alert_id):
        """Mark police as notified"""
        result = self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {
                '$set': {
                    'policeNotified': True,
                    'policeNotifiedAt': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    def add_evidence(self, alert_id, evidence_type, evidence_data):
        """Add audio/video evidence"""
        field = f'recording.{evidence_type}'
        result = self.collection.update_one(
            {'_id': ObjectId(alert_id)},
            {'$set': {field: evidence_data}}
        )
        return result.modified_count > 0
    
    def get_statistics(self):
        """Get SOS statistics"""
        total = self.collection.count_documents({})
        active = self.collection.count_documents({'status': 'active'})
        resolved = self.collection.count_documents({'status': 'resolved'})
        cancelled = self.collection.count_documents({'status': 'cancelled'})
        
        return {
            'total': total,
            'active': active,
            'resolved': resolved,
            'cancelled': cancelled
        }

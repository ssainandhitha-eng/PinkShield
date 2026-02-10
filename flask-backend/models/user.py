"""
User Model
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

class User:
    """User model for Pink Shield"""
    
    def __init__(self, db):
        self.collection = db.users
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        self.collection.create_index('email', unique=True)
        self.collection.create_index('phone', unique=True)
        self.collection.create_index('createdAt')
    
    def create_user(self, data):
        """Create a new user"""
        user = {
            'name': data.get('name'),
            'email': data.get('email').lower(),
            'phone': data.get('phone'),
            'password': generate_password_hash(data.get('password')),
            'gender': data.get('gender', 'prefer-not-to-say'),
            'city': data.get('city'),
            'district': data.get('district'),
            'state': data.get('state'),
            'country': data.get('country', 'India'),
            'role': data.get('role', 'viewer'),
            
            # Accessibility Settings
            'accessibilitySettings': {
                'voiceNavigation': data.get('voiceNavigation', False),
                'vibrationAlerts': data.get('vibrationAlerts', False),
                'tapPatternSOS': data.get('tapPatternSOS', False),
                'largeIconsMode': data.get('largeIconsMode', False),
                'screenReader': False,
                'highContrast': False,
                'reducedMotion': False
            },
            
            # Emergency Contacts
            'emergencyContacts': [],
            'circleOfSafety': [],
            
            # Location Settings
            'locationSettings': {
                'shareLocation': False,
                'trackingEnabled': False,
                'lastKnownLocation': None
            },
            
            # Verification
            'isEmailVerified': False,
            'isPhoneVerified': False,
            
            # Account Status
            'isActive': True,
            'isBanned': False,
            
            # Statistics
            'stats': {
                'sosTriggered': 0,
                'postsCreated': 0,
                'incidentsReported': 0,
                'helpfulVotes': 0
            },
            
            # Preferences
            'preferences': {
                'language': data.get('language', 'en'),
                'notifications': {
                    'email': True,
                    'sms': True,
                    'push': True
                },
                'theme': 'light'
            },
            
            # Timestamps
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'lastLogin': None
        }
        
        result = self.collection.insert_one(user)
        user['_id'] = result.inserted_id
        return user
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email.lower()})
    
    def find_by_phone(self, phone):
        """Find user by phone"""
        return self.collection.find_one({'phone': phone})
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def verify_password(self, user, password):
        """Verify user password"""
        return check_password_hash(user['password'], password)
    
    def update_user(self, user_id, data):
        """Update user"""
        data['updatedAt'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    def add_emergency_contact(self, user_id, contact):
        """Add emergency contact"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$push': {'emergencyContacts': contact},
                '$set': {'updatedAt': datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    def increment_stat(self, user_id, stat_name):
        """Increment user statistic"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$inc': {f'stats.{stat_name}': 1},
                '$set': {'updatedAt': datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    def get_public_profile(self, user):
        """Get public user profile"""
        return {
            'id': str(user['_id']),
            'name': user['name'],
            'city': user['city'],
            'role': user['role'],
            'stats': user['stats'],
            'createdAt': user['createdAt'].isoformat()
        }

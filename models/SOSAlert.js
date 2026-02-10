// ===========================
// SOS Alert Model
// ===========================

const mongoose = require('mongoose');

const sosAlertSchema = new mongoose.Schema({
    // User Information
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
        index: true
    },
    userName: String,
    userPhone: String,

    // Alert Details
    alertType: {
        type: String,
        enum: ['manual', 'shake', 'power-button', 'voice', 'scream', 'fall', 'auto-ai'],
        required: true
    },
    status: {
        type: String,
        enum: ['active', 'resolved', 'cancelled', 'false-alarm'],
        default: 'active',
        index: true
    },
    severity: {
        type: String,
        enum: ['critical', 'high', 'medium', 'low'],
        default: 'critical'
    },

    // Location Information
    location: {
        type: {
            type: String,
            enum: ['Point'],
            default: 'Point'
        },
        coordinates: {
            type: [Number], // [longitude, latitude]
            required: true
        },
        address: String,
        city: String,
        state: String,
        accuracy: Number
    },

    // Device Information
    deviceInfo: {
        batteryLevel: Number,
        networkType: String,
        deviceModel: String,
        osVersion: String
    },

    // Emergency Response
    policeNotified: {
        type: Boolean,
        default: false
    },
    policeNotifiedAt: Date,
    policeStationId: String,
    policeStationName: String,
    policeResponse: {
        status: String,
        officerId: String,
        eta: Number,
        arrivedAt: Date
    },

    // Emergency Contacts Notified
    contactsNotified: [{
        contactId: mongoose.Schema.Types.ObjectId,
        name: String,
        phone: String,
        notifiedAt: Date,
        notificationMethod: {
            type: String,
            enum: ['sms', 'call', 'app', 'email']
        },
        acknowledged: Boolean,
        acknowledgedAt: Date
    }],

    // Recording & Evidence
    recording: {
        audio: {
            url: String,
            duration: Number,
            startedAt: Date
        },
        video: {
            url: String,
            duration: Number,
            startedAt: Date
        },
        photos: [{
            url: String,
            timestamp: Date
        }]
    },

    // AI Analysis
    aiAnalysis: {
        threatLevel: Number,
        detectedThreats: [String],
        audioAnalysis: {
            screamDetected: Boolean,
            distressLevel: Number
        },
        movementAnalysis: {
            rapidMovement: Boolean,
            fallDetected: Boolean,
            abnormalPattern: Boolean
        },
        confidence: Number
    },

    // Timeline
    timeline: [{
        timestamp: Date,
        event: String,
        details: String,
        performedBy: String
    }],

    // Resolution
    resolvedAt: Date,
    resolvedBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    resolutionNotes: String,
    outcome: {
        type: String,
        enum: ['safe', 'assisted', 'hospitalized', 'false-alarm', 'other']
    },

    // Timestamps
    triggeredAt: {
        type: Date,
        default: Date.now,
        index: true
    },
    cancelledAt: Date,

    // Additional Notes
    notes: String,
    tags: [String]
}, {
    timestamps: true
});

// Geospatial index for location-based queries
sosAlertSchema.index({ location: '2dsphere' });

// Compound indexes
sosAlertSchema.index({ userId: 1, triggeredAt: -1 });
sosAlertSchema.index({ status: 1, triggeredAt: -1 });

// Add event to timeline
sosAlertSchema.methods.addTimelineEvent = function (event, details, performedBy = 'system') {
    this.timeline.push({
        timestamp: new Date(),
        event,
        details,
        performedBy
    });
};

// Calculate response time
sosAlertSchema.methods.getResponseTime = function () {
    if (!this.policeResponse || !this.policeResponse.arrivedAt) {
        return null;
    }
    return this.policeResponse.arrivedAt - this.triggeredAt;
};

module.exports = mongoose.model('SOSAlert', sosAlertSchema);

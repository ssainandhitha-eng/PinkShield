// ===========================
// User Model
// ===========================

const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
    // Personal Information
    name: {
        type: String,
        required: [true, 'Name is required'],
        trim: true,
        maxlength: [100, 'Name cannot exceed 100 characters']
    },
    email: {
        type: String,
        required: [true, 'Email is required'],
        unique: true,
        lowercase: true,
        trim: true,
        match: [/^\S+@\S+\.\S+$/, 'Please provide a valid email']
    },
    phone: {
        type: String,
        required: [true, 'Phone number is required'],
        unique: true,
        match: [/^[0-9]{10}$/, 'Please provide a valid 10-digit phone number']
    },
    password: {
        type: String,
        required: [true, 'Password is required'],
        minlength: [8, 'Password must be at least 8 characters'],
        select: false
    },

    // Profile Information
    gender: {
        type: String,
        enum: ['female', 'male', 'other', 'prefer-not-to-say'],
        default: 'prefer-not-to-say'
    },
    city: {
        type: String,
        required: true
    },
    district: String,
    state: String,
    country: {
        type: String,
        default: 'India'
    },

    // Community Role
    role: {
        type: String,
        enum: ['viewer', 'writer', 'author', 'admin'],
        default: 'viewer'
    },

    // Accessibility Settings
    accessibilitySettings: {
        voiceNavigation: { type: Boolean, default: false },
        vibrationAlerts: { type: Boolean, default: false },
        tapPatternSOS: { type: Boolean, default: false },
        largeIconsMode: { type: Boolean, default: false },
        screenReader: { type: Boolean, default: false },
        highContrast: { type: Boolean, default: false },
        reducedMotion: { type: Boolean, default: false }
    },

    // Emergency Contacts
    emergencyContacts: [{
        name: String,
        phone: String,
        relationship: String,
        priority: Number
    }],

    // Circle of Safety
    circleOfSafety: [{
        userId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User'
        },
        name: String,
        phone: String,
        addedAt: {
            type: Date,
            default: Date.now
        }
    }],

    // Location Settings
    locationSettings: {
        shareLocation: { type: Boolean, default: false },
        trackingEnabled: { type: Boolean, default: false },
        lastKnownLocation: {
            latitude: Number,
            longitude: Number,
            timestamp: Date,
            accuracy: Number
        }
    },

    // Verification
    isEmailVerified: {
        type: Boolean,
        default: false
    },
    isPhoneVerified: {
        type: Boolean,
        default: false
    },
    emailVerificationToken: String,
    phoneVerificationOTP: String,
    otpExpiry: Date,

    // Password Reset
    resetPasswordToken: String,
    resetPasswordExpiry: Date,

    // Account Status
    isActive: {
        type: Boolean,
        default: true
    },
    isBanned: {
        type: Boolean,
        default: false
    },
    banReason: String,

    // Statistics
    stats: {
        sosTriggered: { type: Number, default: 0 },
        postsCreated: { type: Number, default: 0 },
        incidentsReported: { type: Number, default: 0 },
        helpfulVotes: { type: Number, default: 0 }
    },

    // Preferences
    preferences: {
        language: {
            type: String,
            enum: ['en', 'ta', 'hi', 'ml', 'te', 'kn'],
            default: 'en'
        },
        notifications: {
            email: { type: Boolean, default: true },
            sms: { type: Boolean, default: true },
            push: { type: Boolean, default: true }
        },
        theme: {
            type: String,
            enum: ['light', 'dark', 'auto'],
            default: 'light'
        }
    },

    // Timestamps
    lastLogin: Date,
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

// Indexes
userSchema.index({ email: 1 });
userSchema.index({ phone: 1 });
userSchema.index({ city: 1 });
userSchema.index({ createdAt: -1 });

// Hash password before saving
userSchema.pre('save', async function (next) {
    if (!this.isModified('password')) {
        return next();
    }

    try {
        const salt = await bcrypt.genSalt(10);
        this.password = await bcrypt.hash(this.password, salt);
        next();
    } catch (error) {
        next(error);
    }
});

// Compare password method
userSchema.methods.comparePassword = async function (candidatePassword) {
    try {
        return await bcrypt.compare(candidatePassword, this.password);
    } catch (error) {
        throw new Error('Password comparison failed');
    }
};

// Get public profile
userSchema.methods.getPublicProfile = function () {
    return {
        id: this._id,
        name: this.name,
        city: this.city,
        role: this.role,
        stats: this.stats,
        createdAt: this.createdAt
    };
};

module.exports = mongoose.model('User', userSchema);

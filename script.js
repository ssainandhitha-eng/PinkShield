// ===========================
// Pink Shield - Complete Website JavaScript
// ===========================

// ===========================
// Global State
// ===========================

let currentSection = 'home';
let sosActive = false;
let companionModeActive = false;
let currentLocation = { lat: 19.0760, lng: 72.8777 }; // Mumbai coordinates
let emergencyContacts = [];
let userSettings = {
    voiceNavigation: false,
    vibrationAlerts: false,
    tapPatternSOS: false,
    largeIconsMode: false
};

// ===========================
// Section Navigation
// ===========================

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
        currentSection = sectionId;
    }

    // Update nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === `#${sectionId}`) {
            link.classList.add('active');
        }
    });

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Update URL hash
    window.location.hash = sectionId;

    // Announce to screen readers
    announceToScreenReader(`Navigated to ${sectionId} section`);
}

// ===========================
// Emergency SOS Functions
// ===========================

function triggerEmergencySOS() {
    if (sosActive) {
        alert('SOS already active! Help is on the way.');
        return;
    }

    const confirmed = confirm(
        '🆘 EMERGENCY SOS\n\n' +
        'This will immediately:\n' +
        '• Alert Police (100/112)\n' +
        '• Notify your emergency contacts\n' +
        '• Share your live location\n' +
        '• Start audio/video recording\n' +
        '• Send SMS with GPS coordinates\n\n' +
        'Press OK to activate emergency SOS'
    );

    if (confirmed) {
        activateSOS();
    }
}

function activateSOS() {
    sosActive = true;

    // Show SOS overlay
    const overlay = document.getElementById('sos-overlay');
    if (overlay) {
        overlay.classList.add('active');
    }

    // Start countdown timer
    startHelpTimer();

    // Simulate emergency actions
    setTimeout(() => {
        console.log('✓ Location shared with emergency contacts');
        console.log('✓ Police (100/112) alerted');
        console.log('✓ SMS sent to trusted network');
        console.log('✓ Audio/Video recording started');
        console.log('✓ Live tracking enabled');
    }, 500);

    // Play alarm sound (in real app)
    console.log('🚨 Panic alarm activated');

    // Vibrate device (if supported)
    if (navigator.vibrate) {
        navigator.vibrate([200, 100, 200, 100, 200]);
    }

    // Send notifications
    sendEmergencyNotifications();

    announceToScreenReader('Emergency SOS activated. Help is on the way.');
}

function cancelSOS() {
    const confirmed = confirm('Are you sure you want to cancel the emergency SOS?');

    if (confirmed) {
        sosActive = false;
        const overlay = document.getElementById('sos-overlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
        alert('Emergency SOS cancelled. Stay safe!');
        announceToScreenReader('Emergency SOS cancelled');
    }
}

function startHelpTimer() {
    let seconds = 180; // 3 minutes
    const timerElement = document.getElementById('help-timer');

    const interval = setInterval(() => {
        if (!sosActive) {
            clearInterval(interval);
            return;
        }

        seconds--;
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        if (timerElement) {
            timerElement.textContent = `${minutes}:${secs.toString().padStart(2, '0')}`;
        }

        if (seconds <= 0) {
            clearInterval(interval);
            if (timerElement) {
                timerElement.textContent = 'Help arriving now!';
            }
        }
    }, 1000);
}

function sendEmergencyNotifications() {
    // Simulate sending notifications
    const notifications = [
        {
            type: 'SMS',
            recipient: 'Emergency Contacts',
            message: '🆘 EMERGENCY! I need help. My location: [GPS coordinates]. Battery: 85%. Time: ' + new Date().toLocaleTimeString()
        },
        {
            type: 'Police Alert',
            recipient: 'Local Police Station',
            message: 'Emergency SOS triggered. Location shared. Immediate assistance required.'
        },
        {
            type: 'Push Notification',
            recipient: 'Circle of Safety',
            message: 'Emergency alert from Pink Shield user. Live location tracking active.'
        }
    ];

    notifications.forEach((notif, index) => {
        setTimeout(() => {
            console.log(`📤 ${notif.type} sent to ${notif.recipient}`);
        }, index * 500);
    });
}

// ===========================
// Quick Emergency Actions
// ===========================

function quickCall(number) {
    const numbers = {
        '100': 'Police',
        '108': 'Ambulance',
        '1091': 'Women Helpline',
        '112': 'All Emergencies'
    };

    const confirmed = confirm(
        `📞 Call ${numbers[number]}?\n\n` +
        `This will dial ${number} for ${numbers[number]}.\n\n` +
        `Your location will be automatically shared.`
    );

    if (confirmed) {
        alert(
            `✅ Calling ${numbers[number]} (${number})\n\n` +
            `📍 Location shared\n` +
            `🔋 Battery: 85%\n` +
            `⏰ Time: ${new Date().toLocaleTimeString()}\n\n` +
            `Stay on the line and describe your emergency.`
        );
        console.log(`Calling ${number} - ${numbers[number]}`);
    }
}

function shareLocation() {
    alert(
        '📍 LOCATION SHARING ACTIVATED\n\n' +
        'Your live location is now being shared with:\n' +
        '• All emergency contacts (5)\n' +
        '• Circle of Safety members (10)\n\n' +
        'Location: Mumbai, Maharashtra\n' +
        'Coordinates: 19.0760°N, 72.8777°E\n' +
        'Accuracy: ±5 meters\n' +
        'Battery: 85%\n\n' +
        'Sharing will continue until you stop it.'
    );
    console.log('Location sharing activated');
}

// ===========================
// Feature Filtering
// ===========================

function filterFeatures(category) {
    const cards = document.querySelectorAll('.feature-card');
    const buttons = document.querySelectorAll('.category-btn');

    // Update active button
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase().includes(category) || category === 'all') {
            btn.classList.add('active');
        }
    });

    // Filter cards
    cards.forEach(card => {
        if (category === 'all') {
            card.style.display = 'block';
        } else {
            const cardCategory = card.getAttribute('data-category');
            card.style.display = cardCategory === category ? 'block' : 'none';
        }
    });
}

function showFeatureDemo(feature) {
    const demos = {
        'sos': 'One-Tap SOS Demo:\n\n1. Tap the SOS button\n2. Instant alert sent (<100ms)\n3. Location shared with contacts\n4. Police notified automatically\n5. Recording starts\n\nTry the main SOS button on the home page!',
        'auto-trigger': 'Auto-Trigger SOS Methods:\n\n• Shake phone 3-4 times\n• Press power button 3 times\n• Scream detection (AI)\n• Tap pattern: tap-tap-pause-tap\n\nAll methods work even when phone is locked!',
        'calling': 'Emergency Numbers:\n\n🚓 Police: 100 / 112\n🚑 Ambulance: 108\n👩 Women Helpline: 1091\n🏠 Domestic Abuse: 181\n👶 Child Helpline: 1098\n\nAll calls share your location automatically.',
        'ai-threat': 'AI Threat Detection:\n\n• Accelerometer monitors sudden movements\n• Microphone detects screams/distress\n• GPS tracks unusual route changes\n• Multi-sensor fusion for accuracy\n\nAuto-triggers SOS when threat detected.',
        'voice': 'Voice Commands:\n\n"Help me" - Triggers SOS\n"SOS" - Emergency alert\n"Guide me home" - Safe navigation\n"Where am I" - Location info\n\nWorks offline with on-device AI!',
        'companion': 'Companion Mode:\n\n1. Set your destination\n2. AI monitors your journey\n3. Alerts if route changes\n4. Detects abrupt stops\n5. Auto-SOS if off-route >5 min\n\nPerfect for late-night travel!',
        'tracking': 'Live Tracking Features:\n\n• Real-time GPS updates\n• Battery % monitoring\n• Timestamp on every update\n• Shared with trusted contacts\n• Works until help arrives\n\nAccuracy: ±5 meters',
        'fake-screen': 'Fake Screen Mode:\n\nApp disguises as:\n• Calculator\n• Gallery\n• Notes app\n\nWhile secretly:\n• Tracking location\n• Recording audio\n• Monitoring threats\n\nActivate from settings!',
        'recording': 'Hidden Recording:\n\n• Auto-starts during SOS\n• Silent operation\n• Uploads to secure cloud\n• End-to-end encrypted\n• Evidence preservation\n\nCannot be detected or stopped.',
        'alarm': 'Panic Alarm:\n\n• 120dB loud siren\n• Flashlight strobe\n• Vibration alert\n• Cannot be silenced remotely\n\nScares attackers, attracts help!',
        'circle': 'Circle of Safety:\n\n• Add 5-10 trusted contacts\n• Real-time location sharing\n• Instant SOS notifications\n• Two-way communication\n• Emergency status updates\n\nYour personal safety network!'
    };

    alert(demos[feature] || 'Feature demo coming soon!');
}

// ===========================
// Map Functions
// ===========================

function findSafeRoute() {
    const from = document.getElementById('route-from').value;
    const to = document.getElementById('route-to').value;

    if (!to) {
        alert('Please enter a destination');
        return;
    }

    alert(
        '🛡️ SAFE ROUTE FOUND\n\n' +
        `From: ${from}\n` +
        `To: ${to}\n\n` +
        'Route Details:\n' +
        '• Distance: 2.3 km\n' +
        '• Est. Time: 15 minutes\n' +
        '• Safety Score: 95% ✓\n\n' +
        'Route Features:\n' +
        '✓ Well-lit streets\n' +
        '✓ CCTV coverage\n' +
        '✓ Crowded areas\n' +
        '✓ Police patrol route\n' +
        '✓ 3 help centers nearby\n\n' +
        'Avoiding 2 danger zones'
    );
}

function showOnMap(locationId) {
    const locations = {
        'police1': 'City Police Station - 0.5 km away',
        'hospital1': 'General Hospital - 1.2 km away',
        'ngo1': 'Women\'s Safety NGO - 2.1 km away',
        'safe1': 'Safe Haven Store - 0.8 km away'
    };

    alert(`📍 Showing on map:\n\n${locations[locationId]}\n\nNavigating...`);
}

function toggleMapLayer(layer) {
    console.log(`Map layer toggled: ${layer}`);
    announceToScreenReader(`${layer} layer toggled`);
}

function startCompanionMode() {
    if (companionModeActive) {
        alert('Companion Mode is already active!');
        return;
    }

    const confirmed = confirm(
        '🛡️ START COMPANION MODE?\n\n' +
        'AI will monitor your journey and:\n' +
        '• Track your route\n' +
        '• Detect deviations\n' +
        '• Alert on abrupt stops\n' +
        '• Auto-SOS if off-route >5 min\n\n' +
        'Start Companion Mode?'
    );

    if (confirmed) {
        companionModeActive = true;
        alert(
            '✅ COMPANION MODE ACTIVE\n\n' +
            '🛡️ AI is now monitoring your journey\n' +
            '📍 Location tracking: ON\n' +
            '🤖 Threat detection: ACTIVE\n' +
            '👥 Contacts notified: 5\n\n' +
            'Stay safe! We\'re watching over you.'
        );
        console.log('Companion Mode activated');
    }
}

function shareCurrentLocation() {
    shareLocation();
}

function reportIncident() {
    alert(
        '⚠️ REPORT UNSAFE AREA\n\n' +
        'Your report will:\n' +
        '• Mark this location on the map\n' +
        '• Notify nearby users\n' +
        '• Alert local authorities\n' +
        '• Update safety zones\n\n' +
        'Thank you for keeping the community safe!'
    );
}

function findNearestPolice() {
    alert(
        '🚓 NEAREST POLICE STATION\n\n' +
        'City Police Station\n' +
        'Distance: 0.5 km\n' +
        'Status: Open 24/7\n' +
        'Phone: 100 / 112\n\n' +
        'Estimated arrival: 3 minutes\n\n' +
        'Navigate now?'
    );
}

// ===========================
// Community Functions
// ===========================

function createPost() {
    alert(
        '✍️ CREATE POST\n\n' +
        'Share with the community:\n' +
        '• Safety tips\n' +
        '• Personal experiences\n' +
        '• Safety alerts\n' +
        '• Event announcements\n\n' +
        'Your post will be reviewed and published within 24 hours.'
    );
}

function shareExperience() {
    alert(
        '💬 SHARE YOUR EXPERIENCE\n\n' +
        'Help others by sharing:\n' +
        '• How Pink Shield helped you\n' +
        '• Safety tips you learned\n' +
        '• Areas to avoid\n' +
        '• Positive experiences\n\n' +
        'Your story can save lives!'
    );
}

// ===========================
// Accessibility Functions
// ===========================

function enableVoiceMode() {
    userSettings.voiceNavigation = true;
    alert(
        '🗣️ VOICE MODE ACTIVATED\n\n' +
        'Features enabled:\n' +
        '✓ Full voice navigation\n' +
        '✓ Audio descriptions\n' +
        '✓ Voice command SOS\n' +
        '✓ Screen reader optimization\n\n' +
        'Say "Help me" to trigger SOS'
    );
}

function enableVisualMode() {
    userSettings.vibrationAlerts = true;
    alert(
        '👁️ VISUAL MODE ACTIVATED\n\n' +
        'Features enabled:\n' +
        '✓ Vibration alerts\n' +
        '✓ Flashlight signals\n' +
        '✓ On-screen captions\n' +
        '✓ Visual SOS indicators\n\n' +
        'Optimized for deaf users'
    );
}

function enableSilentMode() {
    userSettings.tapPatternSOS = true;
    alert(
        '🤐 SILENT MODE ACTIVATED\n\n' +
        'Features enabled:\n' +
        '✓ Tap-pattern SOS\n' +
        '✓ Gesture triggers\n' +
        '✓ Pre-recorded messages\n' +
        '✓ Silent operation\n\n' +
        'Tap pattern: tap-tap-pause-tap'
    );
}

function enableAssistiveMode() {
    alert(
        '♿ ASSISTIVE MODE ACTIVATED\n\n' +
        'Features enabled:\n' +
        '✓ Eye-control SOS\n' +
        '✓ Auto-SOS on device drop\n' +
        '✓ Tilt-based activation\n' +
        '✓ Voice-only operation\n\n' +
        'Optimized for physical disabilities'
    );
}

function enableElderlyMode() {
    userSettings.largeIconsMode = true;
    alert(
        '👵 ELDERLY MODE ACTIVATED\n\n' +
        'Features enabled:\n' +
        '✓ Simplified UI\n' +
        '✓ Large buttons\n' +
        '✓ Auto check-in\n' +
        '✓ One-button emergency\n\n' +
        'Easy to use, always safe'
    );
}

function enableCalmMode() {
    alert(
        '🧠 CALM MODE ACTIVATED\n\n' +
        'Features enabled:\n' +
        '✓ Minimal stimulation\n' +
        '✓ Reduced motion\n' +
        '✓ Clear language\n' +
        '✓ Focus mode\n\n' +
        'Optimized for neurodivergent users'
    );
}

// ===========================
// Form Handling
// ===========================

function sendOTP() {
    const phone = document.getElementById('signup-phone').value;
    if (!phone) {
        alert('Please enter your phone number');
        return;
    }

    alert(
        '📱 OTP SENT!\n\n' +
        `A 6-digit code has been sent to ${phone}\n\n` +
        'Please enter the code to verify your number.\n\n' +
        'Code expires in 10 minutes.'
    );
}

function showLogin() {
    alert('Login feature coming soon!\n\nFor now, you can create a new account.');
}

// ===========================
// Accessibility Helper
// ===========================

function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.style.width = '1px';
    announcement.style.height = '1px';
    announcement.style.overflow = 'hidden';
    announcement.textContent = message;
    document.body.appendChild(announcement);

    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// ===========================
// Initialization
// ===========================

document.addEventListener('DOMContentLoaded', function () {
    // Handle signup form submission
    const signupForm = document.getElementById('main-signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const name = document.getElementById('signup-name').value;
            const phone = document.getElementById('signup-phone').value;
            const email = document.getElementById('signup-email').value;

            alert(
                '✅ REGISTRATION SUCCESSFUL!\n\n' +
                `Welcome to Pink Shield, ${name}!\n\n` +
                'Account created:\n' +
                `📧 ${email}\n` +
                `📱 ${phone}\n\n` +
                'Next steps:\n' +
                '1. Verify your email\n' +
                '2. Add emergency contacts\n' +
                '3. Set up accessibility features\n' +
                '4. Download mobile app\n\n' +
                'You\'re now protected by Pink Shield!'
            );

            console.log('New user registered:', { name, phone, email });
        });
    }

    // Handle hash navigation on page load
    const hash = window.location.hash.substring(1);
    if (hash) {
        showSection(hash);
    } else {
        showSection('home');
    }

    // Handle browser back/forward
    window.addEventListener('hashchange', function () {
        const hash = window.location.hash.substring(1);
        if (hash) {
            showSection(hash);
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function (e) {
        // Ctrl+E for Emergency SOS
        if (e.ctrlKey && e.key === 'e') {
            e.preventDefault();
            triggerEmergencySOS();
        }

        // Escape to cancel SOS
        if (e.key === 'Escape' && sosActive) {
            cancelSOS();
        }
    });

    // Shake detection (if supported)
    if (window.DeviceMotionEvent) {
        let lastShake = 0;
        let shakeCount = 0;

        window.addEventListener('devicemotion', function (e) {
            const acceleration = e.accelerationIncludingGravity;
            const threshold = 15;

            if (acceleration.x > threshold || acceleration.y > threshold || acceleration.z > threshold) {
                const now = Date.now();
                if (now - lastShake > 500) {
                    shakeCount++;
                    lastShake = now;

                    if (shakeCount >= 3) {
                        console.log('Shake detected - triggering SOS');
                        triggerEmergencySOS();
                        shakeCount = 0;
                    }
                }
            }
        });
    }

    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    const animatedElements = document.querySelectorAll('.feature-card, .post-card-large, .stat-item, .accessibility-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    console.log('🛡️ Pink Shield Website Loaded');
    console.log('💖 Safety. Community. Accessibility.');
    console.log('⌨️  Press Ctrl+E for Emergency SOS');
    console.log('📱 Shake phone 3x to trigger SOS (mobile)');
});

// ===========================
// Export for testing
// ===========================

window.PinkShield = {
    showSection,
    triggerEmergencySOS,
    cancelSOS,
    quickCall,
    shareLocation,
    filterFeatures,
    showFeatureDemo,
    findSafeRoute,
    startCompanionMode,
    reportIncident,
    createPost,
    enableVoiceMode,
    enableVisualMode,
    enableSilentMode,
    userSettings
};

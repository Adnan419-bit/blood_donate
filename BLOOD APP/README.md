# BloodConnect - Blood Donation Platform

A comprehensive blood donation platform built with Flask (web) and Android (mobile) to connect blood donors with recipients and save lives.

## 🩸 Features

### Web Application (Flask)
- **Beautiful Splash Screen**: SECDET-branded loading screen with animations
- **Donor Registration**: Complete donor profile management
- **Recipient Registration**: Blood request system
- **Smart Search**: Location-based donor matching with blood type compatibility
- **Emergency Requests**: Urgent blood request system
- **Responsive Design**: Works on desktop and mobile browsers
- **Session Management**: Splash screen shows on first visit

### Android Application
- **Native Android App**: Complete mobile experience
- **Splash Screen**: Beautiful opening screen with SECDET branding and animations
- **Material Design**: Modern UI with proper styling
- **API Integration**: Connects to Flask backend
- **Default Fonts**: Uses standard Android fonts (no custom font dependencies)

## 🚀 Quick Start

### Web Application
```bash
cd "BLOOD APP"
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000

### Android Application
```bash
cd BloodConnect_Android
./gradlew build
```

## 📱 Project Structure

### Web Application
```
BLOOD APP/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── splash.html       # Splash screen (SECDET branded)
│   ├── index.html        # Homepage
│   ├── register_donor.html
│   ├── register_recipient.html
│   ├── search_donors.html
│   ├── emergency.html
│   └── about.html
├── static/
│   ├── css/style.css     # Custom styling
│   └── js/script.js      # JavaScript functionality
└── blood_connect.db      # SQLite database
```

### Android Application
```
BloodConnect_Android/
├── app/
│   ├── src/main/
│   │   ├── java/com/bloodconnect/app/
│   │   │   ├── activities/
│   │   │   │   ├── SplashActivity.java    # Splash screen activity
│   │   │   │   ├── MainActivity.java      # Main activity
│   │   │   │   └── LoginActivity.java     # Login activity
│   │   │   └── utils/
│   │   │       ├── ApiClient.java         # API communication
│   │   │       └── SharedPrefsManager.java
│   │   ├── res/
│   │   │   ├── layout/                    # XML layouts
│   │   │   ├── drawable/                  # Icons and graphics
│   │   │   ├── values/
│   │   │   │   ├── strings.xml           # String resources
│   │   │   │   ├── colors.xml            # Color definitions
│   │   │   │   └── styles.xml            # UI styles
│   │   │   └── AndroidManifest.xml       # App configuration
│   │   └── build.gradle                  # Build configuration
├── build.gradle                          # Project build file
└── settings.gradle                       # Gradle settings
```

## 🎨 Design Features

### Splash Screen
- **SECDET Branding**: Professional developer attribution
- **Animated Logo**: Blood drop with heartbeat animation
- **Progress Bar**: Custom animated loading bar
- **Medical Theme**: Red gradient background with floating elements
- **Auto-Redirect**: Seamless transition to main app

### UI/UX
- **Medical Theme**: Red color scheme representing blood donation
- **Responsive Design**: Works on all screen sizes
- **Modern Typography**: Clean, readable fonts
- **Intuitive Navigation**: Easy-to-use interface
- **Accessibility**: Proper contrast and font sizes

## 🔧 Technical Details

### Backend (Flask)
- **Framework**: Flask with SQLite database
- **Features**: Session management, form handling, API endpoints
- **Security**: Input validation and secure data handling
- **Compatibility**: Blood type matching algorithm

### Frontend (Web)
- **Technologies**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Responsive**: Mobile-first design approach
- **Animations**: CSS animations and transitions
- **Icons**: Font Awesome icons

### Mobile (Android)
- **Language**: Java
- **UI**: XML layouts with Material Design principles
- **Fonts**: Standard Android fonts (sans-serif, sans-serif-medium)
- **API**: RESTful communication with Flask backend
- **Build**: Gradle build system

## 🩺 Blood Type Compatibility

The system implements proper blood type compatibility:
- **A+**: Can receive from A+, A-, O+, O-
- **A-**: Can receive from A-, O-
- **B+**: Can receive from B+, B-, O+, O-
- **B-**: Can receive from B-, O-
- **AB+**: Universal recipient (all types)
- **AB-**: Can receive from A-, B-, AB-, O-
- **O+**: Can receive from O+, O-
- **O-**: Can only receive from O- (universal donor)

## 🚨 Emergency Features

- **24/7 Support**: Round-the-clock emergency system
- **Instant Notifications**: Immediate alerts to compatible donors
- **Location-Based**: Finds nearest available donors
- **Priority Handling**: Emergency requests get highest priority

## 👨‍💻 Developer Information

**Developed by SECDET**
- Security & Development Team
- Version 1.0.0
- Professional medical-themed application
- Cross-platform compatibility

## 📞 Contact Information

- **Emergency**: +1-800-BLOOD-HELP
- **Email**: emergency@bloodconnect.org
- **Availability**: 24/7

## 🔒 Security Features

- **Data Protection**: Secure handling of personal information
- **Input Validation**: Prevents malicious data entry
- **Session Management**: Secure user sessions
- **Privacy**: GDPR-compliant data handling

## 🌟 Key Achievements

✅ **Complete Cross-Platform Solution**: Web + Android
✅ **Professional Splash Screens**: SECDET branding on both platforms
✅ **No Font Errors**: Uses only default system fonts
✅ **Build Success**: Both platforms compile without errors
✅ **Responsive Design**: Works on all devices
✅ **Medical Compliance**: Proper blood type matching
✅ **Emergency Ready**: 24/7 emergency blood request system

## 🎯 Mission

"To create a world where no life is lost due to blood shortage by building the largest, most efficient blood donation network."

---

**Made with ❤️ to save lives**
© 2024 BloodConnect. All rights reserved.
# blood_donate
# blood_donate

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import json
import os
import requests
import sqlite3
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'blood_donation_secret_key_2024'

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8034254176:AAH4uhZ8NEORGbZjyLqXkns5k4bQSTX7Mlk"  # Replace with your actual bot token
TELEGRAM_CHAT_ID = " 6603815140"     # Replace with your chat ID

# Database file
DATABASE = 'blood_connect.db'

# Blood types
BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

# Bangladeshi Cities
BANGLADESHI_CITIES = [
    'ঢাকা (Dhaka)', 'চট্টগ্রাম (Chittagong)', 'সিলেট (Sylhet)', 'রাজশাহী (Rajshahi)',
    'খুলনা (Khulna)', 'বরিশাল (Barisal)', 'রংপুর (Rangpur)', 'ময়মনসিংহ (Mymensingh)',
    'কুমিল্লা (Comilla)', 'নারায়ণগঞ্জ (Narayanganj)', 'গাজীপুর (Gazipur)', 'টাঙ্গাইল (Tangail)',
    'যশোর (Jessore)', 'বগুড়া (Bogra)', 'পাবনা (Pabna)', 'নাটোর (Natore)',
    'সাভার (Savar)', 'কক্সবাজার (Cox\'s Bazar)', 'ফরিদপুর (Faridpur)', 'মাদারীপুর (Madaripur)'
]

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            created_date TEXT NOT NULL
        )
    ''')
    
    # Create donors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            city TEXT NOT NULL,
            address TEXT,
            last_donation TEXT,
            available BOOLEAN DEFAULT 1,
            registered_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create recipients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            city TEXT NOT NULL,
            hospital TEXT NOT NULL,
            urgency TEXT NOT NULL,
            registered_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create blood_requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            contact_person TEXT NOT NULL,
            phone TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            units_needed TEXT,
            hospital TEXT NOT NULL,
            city TEXT NOT NULL,
            urgency TEXT NOT NULL,
            details TEXT,
            created_date TEXT NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    ''')
    
    conn.commit()
    conn.close()

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def send_telegram_message(message):
    """Send message to Telegram bot"""
    try:
        if TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE" and TELEGRAM_CHAT_ID != "6603815140":
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data)
            return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
    return False

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database on startup
init_db()

@app.route('/')
def index():
    # Check if user has seen splash screen
    if 'splash_seen' not in session:
        return redirect(url_for('splash'))
    return render_template('index.html')

@app.route('/splash')
def splash():
    # Mark that user has seen splash screen
    session['splash_seen'] = True
    return render_template('splash.html')

@app.route('/home')
def home():
    # Direct route to home page (bypassing splash)
    session['splash_seen'] = True
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, hashed_password)
        ).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_type'] = user['user_type']
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    user_data = None
    
    if session['user_type'] == 'donor':
        user_data = conn.execute(
            'SELECT * FROM donors WHERE user_id = ?',
            (session['user_id'],)
        ).fetchone()
    elif session['user_type'] == 'recipient':
        user_data = conn.execute(
            'SELECT * FROM recipients WHERE user_id = ?',
            (session['user_id'],)
        ).fetchone()
    
    conn.close()
    return render_template('profile.html', user_data=user_data, user_type=session['user_type'])

@app.route('/register_donor', methods=['GET', 'POST'])
def register_donor():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()
        
        if existing_user:
            flash('Email already registered. Please login instead.', 'warning')
            conn.close()
            return redirect(url_for('login'))
        
        # Create user account
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, password, user_type, created_date) VALUES (?, ?, ?, ?)',
            (email, hashed_password, 'donor', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        user_id = cursor.lastrowid
        
        # Create donor profile
        cursor.execute('''
            INSERT INTO donors (user_id, name, email, phone, blood_type, age, weight, city, address, last_donation, registered_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            request.form['name'],
            email,
            request.form['phone'],
            request.form['blood_type'],
            request.form['age'],
            request.form['weight'],
            request.form['city'],
            request.form['address'],
            request.form['last_donation'] if request.form['last_donation'] else None,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        
        # Send Telegram notification
        telegram_message = f"""
🩸 <b>New Donor Registration</b> 🩸

👤 <b>Name:</b> {request.form['name']}
📧 <b>Email:</b> {email}
📱 <b>Phone:</b> {request.form['phone']}
🩸 <b>Blood Type:</b> {request.form['blood_type']}
🎂 <b>Age:</b> {request.form['age']}
⚖️ <b>Weight:</b> {request.form['weight']} kg
🏙️ <b>City:</b> {request.form['city']}
📅 <b>Registered:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#BloodDonor #LifeSaver #BloodConnect
        """
        send_telegram_message(telegram_message)
        
        # Auto login the user
        session['user_id'] = user_id
        session['user_email'] = email
        session['user_type'] = 'donor'
        
        flash('Donor registration successful! Thank you for your willingness to save lives.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('register_donor.html', blood_types=BLOOD_TYPES)

@app.route('/register_recipient', methods=['GET', 'POST'])
def register_recipient():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()
        
        if existing_user:
            flash('Email already registered. Please login instead.', 'warning')
            conn.close()
            return redirect(url_for('login'))
        
        # Create user account
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, password, user_type, created_date) VALUES (?, ?, ?, ?)',
            (email, hashed_password, 'recipient', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        user_id = cursor.lastrowid
        
        # Create recipient profile
        cursor.execute('''
            INSERT INTO recipients (user_id, name, email, phone, blood_type, city, hospital, urgency, registered_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            request.form['name'],
            email,
            request.form['phone'],
            request.form['blood_type'],
            request.form['city'],
            request.form['hospital'],
            request.form['urgency'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        
        # Send Telegram notification
        telegram_message = f"""
🆘 <b>New Recipient Registration</b> 🆘

👤 <b>Name:</b> {request.form['name']}
📧 <b>Email:</b> {email}
📱 <b>Phone:</b> {request.form['phone']}
🩸 <b>Blood Type Needed:</b> {request.form['blood_type']}
🏙️ <b>City:</b> {request.form['city']}
🏥 <b>Hospital:</b> {request.form['hospital']}
⚡ <b>Urgency:</b> {request.form['urgency']}
📅 <b>Registered:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#BloodRecipient #UrgentNeed #BloodConnect
        """
        send_telegram_message(telegram_message)
        
        # Auto login the user
        session['user_id'] = user_id
        session['user_email'] = email
        session['user_type'] = 'recipient'
        
        flash('Recipient registration successful! We will help you find donors.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('register_recipient.html', blood_types=BLOOD_TYPES)

@app.route('/search_donors', methods=['GET', 'POST'])
def search_donors():
    found_donors = []
    if request.method == 'POST':
        blood_type = request.form['blood_type']
        city = request.form['city'].lower()
        
        # Compatible blood types for each blood type
        compatibility = {
            'A+': ['A+', 'A-', 'O+', 'O-'],
            'A-': ['A-', 'O-'],
            'B+': ['B+', 'B-', 'O+', 'O-'],
            'B-': ['B-', 'O-'],
            'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
            'AB-': ['A-', 'B-', 'AB-', 'O-'],
            'O+': ['O+', 'O-'],
            'O-': ['O-']
        }
        
        compatible_types = compatibility.get(blood_type, [])
        
        conn = get_db_connection()
        placeholders = ','.join('?' * len(compatible_types))
        query = f'''
            SELECT * FROM donors 
            WHERE blood_type IN ({placeholders}) 
            AND LOWER(city) LIKE ? 
            AND available = 1
            ORDER BY registered_date DESC
        '''
        found_donors = conn.execute(query, compatible_types + [f'%{city}%']).fetchall()
        conn.close()
    
    return render_template('search_donors.html', blood_types=BLOOD_TYPES, donors=found_donors)

@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO blood_requests (patient_name, contact_person, phone, blood_type, units_needed, hospital, city, urgency, details, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['patient_name'],
            request.form['contact_person'],
            request.form['phone'],
            request.form['blood_type'],
            request.form['units_needed'],
            request.form['hospital'],
            request.form['city'],
            'Emergency',
            request.form['details'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        
        # Send Emergency Telegram notification
        telegram_message = f"""
🚨 <b>EMERGENCY BLOOD REQUEST</b> 🚨

🆘 <b>Patient:</b> {request.form['patient_name']}
👤 <b>Contact Person:</b> {request.form['contact_person']}
📱 <b>Phone:</b> {request.form['phone']}
🩸 <b>Blood Type:</b> {request.form['blood_type']}
💉 <b>Units Needed:</b> {request.form['units_needed']}
🏥 <b>Hospital:</b> {request.form['hospital']}
🏙️ <b>City:</b> {request.form['city']}
📝 <b>Details:</b> {request.form['details']}
⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>URGENT: Please contact immediately if you can help!</b>

#EmergencyBlood #LifeOrDeath #BloodConnect
        """
        send_telegram_message(telegram_message)
        
        flash('Emergency request submitted! We will notify nearby donors immediately.', 'success')
        return redirect(url_for('index'))
    
    return render_template('emergency.html', blood_types=BLOOD_TYPES)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/stats')
def api_stats():
    conn = get_db_connection()
    
    total_donors = conn.execute('SELECT COUNT(*) as count FROM donors').fetchone()['count']
    total_recipients = conn.execute('SELECT COUNT(*) as count FROM recipients').fetchone()['count']
    active_requests = conn.execute('SELECT COUNT(*) as count FROM blood_requests WHERE status = "Active"').fetchone()['count']
    
    # Blood type distribution
    blood_type_distribution = {}
    for blood_type in BLOOD_TYPES:
        count = conn.execute('SELECT COUNT(*) as count FROM donors WHERE blood_type = ?', (blood_type,)).fetchone()['count']
        blood_type_distribution[blood_type] = count
    
    conn.close()
    
    stats = {
        'total_donors': total_donors,
        'total_recipients': total_recipients,
        'active_requests': active_requests,
        'blood_type_distribution': blood_type_distribution
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

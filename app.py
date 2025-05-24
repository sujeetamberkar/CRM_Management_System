from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
from datetime import datetime, date

# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

def verify_password(password, hashed):
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


# MongoDB connection - MAKE SURE THIS MATCHES YOUR WORKING CONNECTION
uri = "mongodb+srv://maku:abcd@cluster0.nv8kq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Get database and collections
db = client['suj_CRM']
login_collection = db['login']
datasheet_collection = db['datasheet']

# Test connection
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

def add_status_to_records(records):
    """Add expiry status to each record and update in database"""
    current_date = date.today()
    
    for record in records:
        expiry_date_str = record.get('Expiry date', '')
        
        if expiry_date_str and expiry_date_str != 'N/A':
            try:
                # Handle different date formats
                if isinstance(expiry_date_str, str):
                    # Remove time part if present (e.g., "2026-11-07 00:00:00" -> "2026-11-07")
                    if ' ' in expiry_date_str:
                        expiry_date_str = expiry_date_str.split(' ')[0]
                    
                    # Parse the date string
                    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                elif hasattr(expiry_date_str, 'date'):
                    # If it's already a datetime object
                    expiry_date = expiry_date_str.date()
                else:
                    # If it's already a date object
                    expiry_date = expiry_date_str
                
                # Compare with current date
                if expiry_date < current_date:
                    record['Status'] = 'EXPIRED'
                    record['status_class'] = 'status-expired'
                else:
                    record['Status'] = 'ACTIVE'
                    record['status_class'] = 'status-active'
                    
            except (ValueError, TypeError) as e:
                print(f"⚠️  Date parsing error for {expiry_date_str}: {e}")
                record['Status'] = 'UNKNOWN'
                record['status_class'] = 'status-unknown'
        else:
            record['Status'] = 'NO DATE'
            record['status_class'] = 'status-unknown'
    
    return records

def update_status_in_database(records):
    """Update status in MongoDB for all records"""
    try:
        for record in records:
            lab_code = record.get('Lab Code')
            status = record.get('Status')
            
            if lab_code and status:
                # Update the record in database with the new status
                datasheet_collection.update_one(
                    {'Lab Code': lab_code},
                    {'$set': {'Status': status, '_status_updated': datetime.now()}}
                )
        
        print(f"✅ Updated status for {len(records)} records in database")
        
    except Exception as e:
        print(f"❌ Error updating status in database: {e}")
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def authenticate_user(username, password):
    """Authenticate a user against MongoDB"""
    try:
        print(f"🔍 Looking for user: {username}")
        user = login_collection.find_one({"username": username, "active": True})
        
        if user:
            print(f"✅ User found: {username}")
            print(f"🔐 Verifying password...")
            
            password_valid = verify_password(password, user["password_hash"])
            print(f"🔐 Password valid: {password_valid}")
            
            if password_valid:
                # Update last login
                login_collection.update_one(
                    {"username": username},
                    {"$set": {"last_login": datetime.now()}}
                )
                print(f"✅ Authentication successful for {username}")
                return user
            else:
                print(f"❌ Password verification failed for {username}")
        else:
            print(f"❌ User not found or not active: {username}")
            
            # Check if user exists but inactive
            inactive_user = login_collection.find_one({"username": username})
            if inactive_user:
                print(f"⚠️  User exists but active={inactive_user.get('active', 'MISSING')}")
        
        return None
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

# Route for login page (root)
@app.route('/')
def login():
    # If user is already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    print(f"🔐 Login attempt: username='{username}', password='{password}'")
    
    # Authenticate user
    user = authenticate_user(username, password)
    
    if user:
        # Login successful - store user in session
        session['username'] = user['username']
        session['role'] = user.get('role', 'user')
        flash(f'Welcome back, {username}!', 'success')
        print(f"✅ Login successful for {username}")
        return redirect(url_for('home'))
    else:
        # Login failed
        flash('Invalid username or password', 'error')
        print(f"❌ Login failed for {username}")
        return redirect(url_for('login'))

# Route for home page (after login) - shows all data
@app.route('/home')
def home():
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))
    
    username = session['username']
    
    try:
        # Debug: Test connection
        print("🔍 Testing database connection...")
        client.admin.command('ping')
        print("✅ Database connection successful")
        
        # Debug: Check collection
        total_records = datasheet_collection.count_documents({})
        print(f"📊 Total records in database: {total_records}")
        
        # Get all data from datasheet (limit to 100 for performance)
        all_records = list(datasheet_collection.find({}, {'_id': 0}).limit(100))
        print(f"📋 Records fetched: {len(all_records)}")
        
        # Add status to records based on expiry date
        all_records = add_status_to_records(all_records)
        
        # Update status in database at every login
        update_status_in_database(all_records)
        
        if all_records:
            print(f"🔬 Sample record keys: {list(all_records[0].keys())}")
            print(f"🧪 First Lab Code: {all_records[0].get('Lab Code', 'MISSING')}")
            print(f"📅 First Status: {all_records[0].get('Status', 'MISSING')}")
            print(f"📆 First Expiry: {all_records[0].get('Expiry date', 'MISSING')}")
        
        return render_template('home.html', 
                             username=username,
                             records=all_records,
                             total_records=total_records)
    
    except Exception as e:
        print(f"❌ Database error: {e}")
        flash(f'Database error: {str(e)}', 'error')
        return render_template('home.html', 
                             username=username,
                             records=[],
                             total_records=0)

# Route for logout
@app.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True, host='0.0.0.0', port=8010)
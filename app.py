from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
from datetime import datetime, date
from functools import wraps
import pandas as pd
# Create Flask application instance
app = Flask(__name__)

# Set a secret key for session management - FIXED: was missing 'key'
app.secret_key = 'your_secret_key_here_make_it_secure_in_production'

# MongoDB connection - MAKE SURE THIS MATCHES YOUR WORKING CONNECTION
uri = "mongodb+srv://maku:abcd@cluster0.nv8kq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['suj_CRM']
login_collection = db['login']
datasheet_collection = db['noGPT']

try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection failed:", e)

def verify_password(password, hashed):
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

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route for login page (root)
@app.route('/')
def login():
    # If user is already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

# Route to handle login form submission - THIS WAS MISSING
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('Please enter both username and password.', 'error')
        return redirect(url_for('login'))
    
    # Authenticate user
    user = authenticate_user(username, password)
    
    if user:
        # Store user info in session
        session['username'] = user['username']
        session['user_id'] = str(user['_id'])
        session['role'] = user.get('role', 'user')
        
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))

# Home route - redirect to home.html after login
@app.route('/home')
@login_required
def home():
    username = session.get('username', 'User')
    datasheet_df = pd.DataFrame(list(datasheet_collection.find()))
    datasheet_df['Expiry date'] = pd.to_datetime(datasheet_df['Expiry date'], errors='coerce')
    today = pd.Timestamp.today().normalize()
    datasheet_df['Status'] = datasheet_df['Expiry date'].apply(lambda x: 'Expired' if x < today else 'Active')
    
    # Remove _id column and reorder columns with Status first
    if '_id' in datasheet_df.columns:
        datasheet_df = datasheet_df.drop('_id', axis=1)
    
    # Reorder columns to put Status first
    other_columns = [col for col in datasheet_df.columns if col != 'Status']
    if 'Status' in datasheet_df.columns:
        ordered_columns = ['Status'] + other_columns
        datasheet_df = datasheet_df[ordered_columns]
    
    # Get unique values for dropdowns
    unique_sections = ['All Sections'] + sorted(datasheet_df['Section'].dropna().unique().tolist())
    unique_status = ['All Status'] + sorted(datasheet_df['Status'].dropna().unique().tolist())
    
    # Calculate expiring in 3 months
    three_months_from_now = today + pd.DateOffset(months=3)
    expiring_soon = datasheet_df[
        (datasheet_df['Expiry date'] >= today) & 
        (datasheet_df['Expiry date'] <= three_months_from_now)
    ]
    expiring_count = len(expiring_soon)
    
    # Convert DataFrame to HTML table or pass data to template
    table_data = datasheet_df.to_dict('records')  # Convert to list of dictionaries
    columns = datasheet_df.columns.tolist()  # Get column names
    
    return render_template('home.html', 
                         username=username,
                         table_data=table_data, 
                         columns=columns,
                         unique_sections=unique_sections,
                         unique_status=unique_status,
                         total_records=len(datasheet_df),
                         expiring_count=expiring_count)


# Logout route - THIS WAS MISSING
@app.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/create_crm', methods=['GET', 'POST'])
@login_required
def create_crm():
    """Route to display and handle the Create CRM form"""
    if request.method == 'POST':
        # Handle form submission
        form_data = {
            'Name': request.form.get('name_of_standard'),
            'Lab Code': request.form.get('lab_code'),
            'Expiry date': pd.to_datetime(request.form.get('expiry_date')),
            'Make': request.form.get('make') or 'NA',
            'Quantity': request.form.get('quantity') or 'NA',
            'Purity': request.form.get('purity') or 'NA',
            'Product Code': request.form.get('product_code') or 'NA',
            'CAS no.': request.form.get('cas_no') or 'NA',
            'Section': request.form.get('section'),
            'Location': request.form.get('location') or 'NA',
            'Box No.': request.form.get('box_no') or 'NA',
            'Remarks': request.form.get('remarks') or 'NA',
            'Status': 'Active'  # Default status for new entries
        }
        
        # Validate Lab Code is not empty and unique
        lab_code = form_data['Lab Code']
        if not lab_code or lab_code.strip() == '':
            flash('Lab Code cannot be empty!', 'error')
            return redirect(url_for('create_crm'))
            
        # Check if Lab Code already exists
        if datasheet_collection.find_one({'Lab Code': lab_code}):
            flash('Lab Code already exists! Please use a different code.', 'error')
            return redirect(url_for('create_crm'))
        
        # Insert into MongoDB
        try:
            datasheet_collection.insert_one(form_data)
            flash('CRM entry created successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error creating entry: {str(e)}', 'error')
            return redirect(url_for('create_crm'))
    
    # GET request - display form
    # Get existing data for dropdowns
    datasheet_df = pd.DataFrame(list(datasheet_collection.find()))
    
    # Get unique values for dropdowns
    unique_names = sorted(datasheet_df['Name'].dropna().unique().tolist()) if not datasheet_df.empty else []
    unique_sections = sorted(datasheet_df['Section'].dropna().unique().tolist()) if not datasheet_df.empty else []
    
    # Get existing lab codes for suggestion logic
    existing_lab_codes = datasheet_df['Lab Code'].dropna().tolist() if not datasheet_df.empty else []
    
    # Create name to CAS mapping
    name_cas_mapping = {}
    if not datasheet_df.empty:
        for _, row in datasheet_df.iterrows():
            if pd.notna(row['Name']) and pd.notna(row['CAS no.']):
                name_cas_mapping[row['Name']] = row['CAS no.']
    
    return render_template('create_crm.html',
                         unique_names=unique_names,
                         unique_sections=unique_sections,
                         existing_lab_codes=existing_lab_codes,
                         name_cas_mapping=name_cas_mapping)


if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True, host='0.0.0.0', port=8000)
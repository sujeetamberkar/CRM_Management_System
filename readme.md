# 🧪 CRM Management System for Laboratory Standards

A comprehensive web-based Chemical Reference Material (CRM) management system designed for laboratories to track, manage, and monitor their chemical standards inventory. Built with Flask and MongoDB, this system provides complete CRUD operations with an intuitive user interface.

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

## ✨ Features

### 🔐 **Authentication System**
- Secure user login with bcrypt password hashing
- Session management
- Protected routes with login requirements

### 📊 **Dashboard & Overview**
- **Welcome dashboard** with user-specific greetings
- **Real-time statistics** showing total records and expiring items
- **Three main views:**
  - **All CRMs**: Complete inventory overview
  - **Expiring in 3 Months**: Items requiring attention (excludes consumed items)
  - **Consumed CRMs**: Items marked as consumed/used

### 🔍 **Advanced Search & Filtering**
- **Real-time search** across all fields (case-insensitive)
- **Section-based filtering** with dynamic dropdowns
- **Status-based filtering** (Active, Expired, Consumed)
- **Combined filtering** - all filters work together seamlessly

### ➕ **Create New CRM Entries**
- **Comprehensive form** with all necessary fields:
  - Name of Standard (with existing options + "Add New Standard")
  - Lab Code with intelligent suggestion system
  - Expiry Date with calendar picker
  - Make, Quantity, Purity, Product Code
  - CAS Number (auto-filled for existing standards)
  - Section, Location, Box Number, Remarks
- **Smart Lab Code Suggestions:**
  - For existing standards: Creates sequential codes (H-74 A, H-74 B, etc.)
  - For new standards: Starts from H-102 and increments
  - Prevents duplicate codes

### ✏️ **Edit Existing Records**
- **Pre-filled forms** with current data
- **Lab Code protection** (read-only during editing to maintain uniqueness)
- **All fields editable** except Lab Code
- **Auto-save validation** with user feedback

### 🗑️ **Delete Records**
- **Confirmation dialogs** to prevent accidental deletions
- **Safe deletion** with user feedback
- **Immediate UI updates** after deletion

### 🔄 **Consumption Tracking**
- **Mark as Consumed/Not Consumed** toggle functionality
- **Status priority logic**: Consumed → Expired → Active
- **Consumption status** affects filtering and display
- **Visual indicators** with color-coded badges

### 📈 **Intelligent Status Management**
- **Automatic status calculation** based on expiry dates and consumption
- **Three status types:**
  - 🟢 **Active**: Not expired and not consumed
  - 🔴 **Expired**: Past expiry date and not consumed
  - 🟠 **Consumed**: Manually marked as consumed (overrides expiry status)

### 🎨 **Modern User Interface**
- **Responsive design** that works on desktop, tablet, and mobile
- **Professional styling** with gradients and modern components
- **Color-coded status badges** for easy visual identification
- **Sticky headers** and smooth animations
- **Intuitive navigation** with breadcrumbs and clear actions

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: MongoDB with PyMongo driver
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: bcrypt for password hashing
- **Data Processing**: Pandas for data manipulation
- **File Handling**: openpyxl for Excel file support
- **Styling**: Custom CSS with modern design principles

## 📁 Project Structure

```
CRM_Management_System/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── templates/                  # HTML templates
│   ├── login.html             # Login page
│   ├── home.html              # Main dashboard
│   ├── create_crm.html        # Create new CRM entry
│   └── edit_crm.html          # Edit existing CRM entry
└── static/                     # Static assets
    ├── css/
    │   └── style.css          # Main stylesheet
    └── images/
        └── logo.png           # Company logo
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- MongoDB Atlas account or local MongoDB installation
- Git (for cloning the repository)

### Method 1: Using Virtual Environment (venv)

#### On Windows:
```bash
# Clone the repository
git clone https://github.com/sujeetamberkar/CRM_Management_System
cd CRM_Management_System

# Create virtual environment
python3 -m venv virtual

# Activate virtual environment
virtual\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

#### On Linux/macOS:
```bash
# Clone the repository
git clone https://github.com/sujeetamberkar/CRM_Management_System
cd CRM_Management_System

# Create virtual environment
python3 -m venv virtual

# Activate virtual environment
source virtual/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Method 2: Using Conda

#### On Windows:
```bash
# Clone the repository
git clone https://github.com/sujeetamberkar/CRM_Management_System
cd CRM_Management_System

# Create conda environment
conda create --name crm-env python=3.9

# Activate environment
conda activate crm-env

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

#### On Linux/macOS:
```bash
# Clone the repository
git clone https://github.com/sujeetamberkar/CRM_Management_System
cd CRM_Management_System

# Create conda environment
conda create --name crm-env python=3.9

# Activate environment
conda activate crm-env

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 📊 Bulk Data Import

If you have existing CRM data in Excel format, you can bulk upload it using the following script:

### Prerequisites for Data Import
- Excel file with CRM data (`data.xlsx`)
- Pandas and pymongo installed
- Valid MongoDB connection

### Data Upload Script

Create a new Python file (e.g., `upload_data.py`) and run this script:

```python
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Read the Excel file
df = pd.read_excel('data.xlsx')

# Clean and validate expiry dates
# Keep only rows where Expiry date can be converted to datetime
df['Expiry date_temp'] = pd.to_datetime(df['Expiry date'], errors='coerce')

# Remove rows where conversion failed (NaT values)
df = df.dropna(subset=['Expiry date_temp'])

# Convert to datetime objects (not strings) to match manual entry format
df['Expiry date'] = df['Expiry date_temp']

# Drop the temporary column
df = df.drop('Expiry date_temp', axis=1)

# Ensure consistent data formatting to match manual entry system
def clean_data_format(df):
    """
    Clean and format data to match the manual entry system format
    """
    # Handle missing values consistently with manual entry system
    for col in ['Make', 'Quantity', 'Purity', 'Product Code', 'CAS no.', 'Location', 'Box No.', 'Remarks']:
        if col in df.columns:
            df[col] = df[col].fillna('NA')
            # Convert empty strings to 'NA'
            df[col] = df[col].replace('', 'NA')
    
    # Initialize Consumed column (default: not consumed)
    df['Consumed'] = 0
    
    # Calculate Status based on expiry date (same logic as manual entry)
    today = pd.Timestamp.now().normalize()
    
    def calculate_status(row):
        # Same logic as in the main application
        if row.get('Consumed', 0) == 1:
            return 'Consumed'
        elif pd.notna(row['Expiry date']) and row['Expiry date'] < today:
            return 'Expired'
        else:
            return 'Active'
    
    df['Status'] = df.apply(calculate_status, axis=1)
    
    # Ensure all required columns exist
    required_columns = [
        'Lab Code', 'Name', 'Expiry date', 'Make', 'Quantity', 
        'Purity', 'Product Code', 'CAS no.', 'Section', 'Location', 
        'Box No.', 'Remarks', 'Consumed', 'Status'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            if col == 'Consumed':
                df[col] = 0
            elif col == 'Status':
                df[col] = 'Active'
            else:
                df[col] = 'NA'
    
    # Reorder columns to match the application structure
    df = df[required_columns]
    
    return df

# Clean and format the data
df = clean_data_format(df)

print(f"Remaining rows after cleanup: {len(df)}")
print("Sample of formatted data:")
print(df.head())

# MongoDB connection - UPDATE WITH YOUR CONNECTION STRING
uri = "mongodb+srv://maku:abcd@cluster0.nv8kq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Get database and collections (use same names as main application)
db = client['suj_CRM']
datasheet_collection = db['noGPT']

print("🚀 Starting upload...")

# Convert to dictionary format that matches manual entry structure
records = df.to_dict('records')

# Insert data into MongoDB
datasheet_collection.insert_many(records)

print("✅ Data uploaded successfully!")
print(f"📊 Uploaded {len(records)} records")

# Create unique index on Lab Code to prevent duplicates
try:
    datasheet_collection.create_index("Lab Code", unique=True)
    print("🔒 Unique index created on Lab Code")
except Exception as e:
    print(f"ℹ️  Index might already exist: {e}")

# Verify the upload by checking a few records
print("\n🔍 Verification - Sample uploaded records:")
sample_records = list(datasheet_collection.find().limit(3))
for record in sample_records:
    print(f"  Lab Code: {record['Lab Code']}, Status: {record['Status']}, Consumed: {record['Consumed']}")
```

### Expected Excel Format

Your Excel file should have the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| **Lab Code** | Unique identifier | H-1 A |
| **Name** | Standard name | Acesulfame Potassium |
| **Expiry date** | Expiry date | 2026-11-07 |
| **Make** | Manufacturer | Dr.Ehrenstorfer |
| **Quantity** | Amount | 250 mg |
| **Purity** | Purity percentage | 99.84 |
| **Product Code** | Manufacturer code | DRE-C10010800 |
| **CAS no.** | CAS Registry Number | 55589-62-3 |
| **Section** | Lab section | HPLC |
| **Location** | Storage location | EL-Deepfreezer-02 |
| **Box No.** | Storage box | HPLC BOX |
| **Remarks** | Additional notes | Y |

### Running the Upload Script

```bash
# Make sure you're in your project directory
cd CRM_Management_System

# Activate your virtual environment
# For venv:
source virtual/bin/activate  # Linux/macOS
# OR
virtual\Scripts\activate     # Windows

# For conda:
conda activate crm-env

# Place your data.xlsx file in the project directory
# Run the upload script
python upload_data.py
```

### Important Notes

⚠️ **Before Running the Script:**
1. **Backup your database** - The script will add new records
2. **Check your Excel format** - Ensure columns match expected format
3. **Validate dates** - Invalid dates will be automatically removed
4. **Update connection string** - Use your actual MongoDB connection details

✅ **What the Script Does:**
- Reads Excel file and validates data
- **Maintains datetime format** for expiry dates (same as manual entry)
- **Adds Consumed column** with default value 0 (not consumed)
- **Calculates Status automatically** using same logic as application
- **Fills missing values with 'NA'** to match manual entry behavior
- **Ensures all required columns exist** with proper defaults
- **Reorders columns** to match application structure
- Uploads data to MongoDB with verification
- Creates unique index on Lab Code to prevent duplicates
- Provides progress feedback and sample verification

🔄 **Automatic Features:**
- **Date consistency** - Maintains datetime objects like manual entry
- **Status calculation** - Uses exact same logic as the application
- **Consumed tracking** - Initializes consumption status properly
- **Missing value handling** - Converts empty/null to 'NA' consistently
- **Column standardization** - Ensures all required fields exist
- **Duplicate prevention** - Lab Code uniqueness is enforced
- **Data verification** - Shows sample records after upload
- **Progress tracking** - Shows upload status and row counts

### Troubleshooting Data Upload

**Common Issues:**

**Excel File Not Found**
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'data.xlsx'
```
- Ensure `data.xlsx` is in the same directory as your script
- Check the file name spelling

**Date Format Issues**
```bash
# Invalid dates will be automatically removed
# Check your Excel date format - should be recognizable date format
```

**Duplicate Lab Codes**
```bash
pymongo.errors.DuplicateKeyError
```
- Each Lab Code must be unique
- Check for duplicate entries in your Excel file
- Existing records with same Lab Code will cause conflicts

**Connection Issues**
- Verify your MongoDB connection string
- Check internet connectivity
- Ensure MongoDB Atlas IP whitelist includes your IP

### MongoDB Atlas (Recommended)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Create a database user with read/write permissions
4. Get your connection string
5. Update the connection string in `app.py`:

```python
# Replace with your MongoDB Atlas connection string
# Example: mongodb+srv://maku:abcd@cluster.mongodb.net/
client = MongoClient("mongodb+srv://username:password@cluster.mongodb.net/")
```

### Local MongoDB
1. Install MongoDB locally
2. Start MongoDB service
3. Update the connection string in `app.py`:

```python
# For local MongoDB
client = MongoClient("mongodb://localhost:27017/")
```

### Database Collections
The application will automatically create the following collections:
- `users` - User authentication data
- `datasheet` - CRM inventory records

## 🖥️ Usage

### First-Time Setup
1. Start the application: `python app.py`
2. Open your browser and navigate to `http://127.0.0.1:8000`
3. The application will create default admin credentials:
   - **Username**: `admin`
   - **Password**: `abcd`
4. Login and start adding your CRM inventory

### Adding CRM Records
1. Click **"Create New CRM Entry"**
2. Fill in all required fields:
   - Select existing standard or add new one
   - Use **"Suggest Code"** for automatic Lab Code generation
   - Set expiry date using the calendar picker
   - Fill in technical details (Make, Quantity, Purity, etc.)
   - Select appropriate Section and Location
3. Click **"Create"** to save

### Managing Records
- **Search**: Use the search bar to find records across all fields
- **Filter**: Use dropdown filters for Section and Status
- **Edit**: Click the "Edit" button in the Actions column
- **Delete**: Click "Delete" and confirm the action
- **Mark Consumed**: Use consumption toggle in Actions column

### Viewing Different Categories
- **All CRMs**: Complete inventory overview
- **Expiring in 3 Months**: Items needing attention (active items only)
- **Consumed CRMs**: Items marked as consumed/used

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Login page (redirects to home if authenticated) |
| POST | `/login` | User authentication |
| GET | `/logout` | User logout |
| GET | `/home` | Main dashboard |
| GET/POST | `/create_crm` | Create new CRM entry |
| GET/POST | `/edit_crm/<crm_id>` | Edit existing CRM entry |
| POST | `/delete_crm/<crm_id>` | Delete CRM entry |
| POST | `/toggle_consumed/<crm_id>` | Toggle consumption status |

## 📱 Features in Detail

### Smart Lab Code System
- **Existing Standards**: Automatically suggests next available letter suffix (H-74 A, H-74 B)
- **New Standards**: Starts from H-102 and increments sequentially
- **Duplicate Prevention**: Validates uniqueness before saving
- **Manual Override**: Allows custom codes while maintaining validation

### Status Management
The system uses intelligent status calculation:
1. **Consumed Check**: If marked as consumed → Status = "Consumed"
2. **Expiry Check**: If past expiry date → Status = "Expired"
3. **Default**: Otherwise → Status = "Active"

### Search Functionality
- **Global Search**: Searches across all visible columns
- **Case Insensitive**: Works regardless of letter case
- **Real-time**: Updates results as you type
- **Combined Filters**: Works with dropdown filters

### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Tablet Support**: Clean layout on tablet screens
- **Desktop Enhancement**: Full features on desktop
- **Touch-Friendly**: Large buttons and touch targets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Error**
- Verify your connection string is correct
- Check if your IP is whitelisted in MongoDB Atlas
- Ensure MongoDB service is running (for local installations)

**Dependencies Installation Error**
- Make sure you're using Python 3.7+
- Try upgrading pip: `pip install --upgrade pip`
- Use virtual environment to avoid conflicts

**Application Won't Start**
- Check if port 8000 is available
- Verify all dependencies are installed
- Check MongoDB connection

**Login Issues**
- Use default credentials: admin/abcd
- Check if users collection was created properly
- Verify bcrypt is working correctly

# Author 
Sujeet Sanjay Amberkar
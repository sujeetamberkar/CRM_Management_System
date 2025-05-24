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
- Username : admin
- Password : abcd 

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
crm-management-system/
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
git clone <repository-url>
cd crm-management-system

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
git clone <repository-url>
cd crm-management-system

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
git clone <repository-url>
cd crm-management-system

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
git clone <repository-url>
cd crm-management-system

# Create conda environment
conda create --name crm-env python=3.9

# Activate environment
conda activate crm-env

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🗄️ Database Setup

### MongoDB Atlas (Recommended)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Create a database user with read/write permissions
4. Get your connection string
5. Update the connection string in `app.py`:

```python
# Replace with your MongoDB Atlas connection string
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
   - **Password**: `admin123`
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

## 📄 License

Sujeet Sanjay Amberkar
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
- Use default credentials: admin/admin123
- Check if users collection was created properly
- Verify bcrypt is working correctly


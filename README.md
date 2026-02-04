

# Chemical Equipment Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive hybrid application combining a Web app (React) and Desktop app (PyQt5) with a unified Django REST backend for chemical equipment data visualization and analytics.

## 🚀 Overview

The Chemical Equipment Analyzer is designed to streamline the analysis of chemical equipment parameters through intuitive interfaces. Whether you prefer web-based access or desktop applications, this tool provides consistent functionality across platforms with powerful data processing capabilities.

### ✨ Key Features

- **📊 CSV Upload & Processing**: Seamlessly upload CSV files containing chemical equipment parameters
- **📈 Advanced Analytics**: Automatic computation of comprehensive statistics:
  - Total equipment count and distribution
  - Average flowrate, pressure, and temperature calculations
  - Equipment type categorization and analysis
- **🎨 Interactive Visualizations**: Dynamic charts and graphs in both Web and Desktop interfaces
- **📝 History Management**: Store and retrieve the last 5 uploaded datasets with detailed metadata
- **📄 PDF Report Generation**: Create professional downloadable PDF summary reports
- **🔐 Secure Authentication**: Token-based authentication system for data protection
- **🌐 Cross-Platform Support**: Web and desktop applications with unified backend

## 📁 Project Architecture

```
Chemical Equipment Analyzer/
├── 🗄️ backend/                 # Django REST API
│   ├── equipment_analyzer/     # Django project settings
│   ├── api/                    # API app with models, views, serializers
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data serialization
│   │   └── urls.py            # URL routing
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
├── 🌐 web/                    # React web application
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── CSVUpload.js
│   │   │   ├── Dashboard.js
│   │   │   ├── DataVisualization.js
│   │   │   └── History.js
│   │   ├── pages/           # Page components
│   │   ├── utils/           # API client and auth utilities
│   │   └── App.js          # Main application component
│   └── package.json         # Node.js dependencies
├── 💻 desktop/               # PyQt5 desktop application
│   ├── app/
│   │   ├── api_client.py    # API client
│   │   ├── main_window.py   # Main application window
│   │   ├── login_dialog.py  # Login/Register dialog
│   │   └── history_widget.py # History management
│   ├── main.py             # Desktop app entry point
│   └── requirements.txt    # Python dependencies
├── 📄 sample_data.csv       # Sample CSV for testing
├── 📋 PROJECT_SUMMARY.md    # Detailed project documentation
├── 🚀 QUICKSTART.md        # Quick setup guide
└── 📖 README.md            # This file
```

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+ and npm** - [Download Node.js](https://nodejs.org/)
- **pip** - Python package manager (included with Python)
- **Git** - For version control (optional but recommended)

## 🚀 Quick Start

Choose your preferred interface or set up all components:

### Option 1: Web Application Only
```bash
# 1. Start Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# 2. Start Web App (in new terminal)
cd web
npm install
npm start
```

### Option 2: Desktop Application Only
```bash
# 1. Start Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# 2. Start Desktop App (in new terminal)
cd desktop
pip install -r requirements.txt
python main.py
```

### Option 3: Full Setup (Recommended)
Follow the detailed setup instructions below.

## 📋 Detailed Setup Instructions

### 1. 🗄️ Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**🌐 Backend URL:** `http://localhost:8000`
**🔧 Admin Panel:** `http://localhost:8000/admin/`

### 2. 🌐 Web Application Setup (React)

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Start development server
npm start
```

**🌐 Web App URL:** `http://localhost:3000`

### 3. 💻 Desktop Application Setup (PyQt5)

```bash
# Navigate to desktop directory
cd desktop

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

**💻 Desktop App:** Launches as a native application window

## 📄 CSV File Format

The application accepts CSV files with the following required columns (case-insensitive):

| Column | Description | Data Type | Example |
|--------|-------------|-----------|---------|
| **Equipment Name** | Unique identifier for each equipment | String | "Reactor A" |
| **Type** | Category/type of equipment | String | "Reactor" |
| **Flowrate** | Flow rate measurement | Numeric | 150.5 |
| **Pressure** | Pressure measurement | Numeric | 25.3 |
| **Temperature** | Temperature measurement | Numeric | 180.2 |

### 📋 Sample CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,25.3,180.2
Distillation Column B,Distillation,200.0,30.1,200.5
Heat Exchanger C,Heat Exchanger,175.8,22.7,150.0
Pump D,Pump,85.2,18.9,75.3
Compressor E,Compressor,120.0,35.6,220.1
```

### ⚠️ Important Notes

- **Column Headers**: Must match exactly (case-insensitive)
- **Data Types**: Flowrate, Pressure, and Temperature must be numeric
- **Empty Rows**: Will be automatically skipped
- **Invalid Data**: Rows with missing or invalid data will be excluded from analysis

## 🔌 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/register/` | Register new user | None |
| POST | `/api/login/` | Login and get token | None |

### Data Management Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/upload/` | Upload and analyze CSV | Required |
| GET | `/api/history/` | Get upload history | Required |
| GET | `/api/summary/<id>/` | Get dataset summary | Required |
| GET | `/api/summary/<id>/pdf/` | Download PDF report | Required |

### 📡 API Response Format

```json
{
  "id": 1,
  "filename": "equipment_data.csv",
  "upload_date": "2024-01-15T10:30:00Z",
  "total_equipment": 25,
  "avg_flowrate": 145.7,
  "avg_pressure": 28.4,
  "avg_temperature": 185.2,
  "equipment_types": {
    "Reactor": 8,
    "Pump": 12,
    "Heat Exchanger": 5
  }
}
```

## 🎯 User Guide

### 🌐 Web Application Usage

1. **🚀 Launch**: Open `http://localhost:3000` in your browser
2. **👤 Authentication**: Register a new account or login with existing credentials
3. **📊 Upload Data**: Navigate to "Upload CSV" tab and select your CSV file
4. **📈 View Analytics**: Check the "Visualization" tab for interactive charts
5. **📝 History**: Access the "History" tab to view previous uploads
6. **📄 Download Reports**: Generate PDF reports from history or visualization views

### 💻 Desktop Application Usage

1. **🚀 Launch**: Run `python main.py` from the desktop directory
2. **👤 Login**: Use the login dialog to authenticate or register
3. **📊 Upload**: Click "Select CSV File" button to upload your data
4. **📈 Analyze**: Switch to "Visualization" tab for charts and graphs
5. **📝 History**: Use "History" tab to view previous analyses
6. **🔍 Details**: Double-click history items to view detailed information
7. **📄 Export**: Download PDF reports directly from the visualization view

## 🛠️ Technology Stack

### 🗄️ Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 4.2.7 | Web framework and API backend |
| **Django REST Framework** | 3.14.0 | RESTful API development |
| **Pandas** | 2.1.3 | Data processing and analysis |
| **ReportLab** | 4.0.7 | PDF report generation |
| **SQLite** | Built-in | Default database storage |

### 🌐 Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | Web application framework |
| **Chart.js** | 4.4.0 | Data visualization and charts |
| **Axios** | 1.6.2 | HTTP client for API calls |
| **CSS3** | Latest | Styling and responsive design |

### 💻 Desktop Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **PyQt5** | 5.15.10 | Desktop GUI framework |
| **Matplotlib** | 3.8.2 | Data visualization for desktop |
| **Requests** | 2.31.0 | HTTP client for API communication |

## 🔧 Development & Architecture

### 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │  Desktop Client │    │   Mobile Client │
│   (React)       │    │   (PyQt5)       │    │   (Future)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Django REST API         │
                    │   (Backend Server)        │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   SQLite Database         │
                    │   (Data Storage)          │
                    └───────────────────────────┘
```

### 🔐 Security Features

- **Token-Based Authentication**: Secure JWT tokens for API access
- **Input Validation**: Comprehensive data validation on all inputs
- **CORS Protection**: Cross-Origin Resource Sharing configuration
- **SQL Injection Prevention**: Django ORM protection
- **File Upload Security**: CSV file validation and processing

### 📊 Data Processing Pipeline

1. **Upload**: CSV file received via multipart form data
2. **Validation**: Column headers and data types validated
3. **Processing**: Pandas DataFrame creation and analysis
4. **Storage**: Results stored in SQLite database
5. **Visualization**: Charts generated using Chart.js/Matplotlib
6. **Reporting**: PDF reports created with ReportLab

## 🚨 Error Handling & Troubleshooting

### ⚠️ Common Issues & Solutions

#### Backend Issues
| Problem | Solution |
|---------|----------|
| **Port 8000 already in use** | Change port: `python manage.py runserver 8001` |
| **Migration errors** | Delete `db.sqlite3` and re-run migrations |
| **Permission denied** | Check database file permissions |
| **Module not found** | Activate virtual environment and install requirements |

#### Web Application Issues
| Problem | Solution |
|---------|----------|
| **CORS errors** | Ensure backend is running and CORS is configured |
| **API connection failed** | Check backend URL in `src/utils/api.js` |
| **Authentication issues** | Clear browser localStorage and re-login |
| **Build failures** | Delete `node_modules` and run `npm install` |

#### Desktop Application Issues
| Problem | Solution |
|---------|----------|
| **PyQt5 import error** | Install PyQt5: `pip install PyQt5` |
| **Window not showing** | Check Python version (3.8+ required) |
| **API connection timeout** | Verify backend is accessible from desktop app |
| **Memory issues** | Close unused applications for large datasets |

### 🐛 Debug Mode

Enable debug mode by setting `DEBUG = True` in `backend/equipment_analyzer/settings.py`

## 📈 Performance Considerations

### 🚀 Optimization Tips

- **Large Files**: Process CSV files in chunks for datasets > 10,000 rows
- **Memory Usage**: Monitor memory consumption during data processing
- **Database**: Regular database cleanup for optimal performance
- **Caching**: Implement Redis caching for frequently accessed data
- **CDN**: Use CDN for static assets in production

### 📊 Scalability

- **Current Limit**: 5 datasets per user (configurable)
- **File Size**: Recommended max 10MB per CSV file
- **Concurrent Users**: Supports multiple simultaneous users
- **Database**: SQLite for development, PostgreSQL recommended for production

## 🔄 Version Control & Deployment

### 📋 Development Workflow

```bash
# Clone repository
git clone https://github.com/VinayakKamankar1/Chemical-Equipment-Analyzer.git
cd Chemical-Equipment-Analyzer

# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

### 🚀 Production Deployment

#### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn equipment_analyzer.wsgi:application
```

#### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy build/ folder to web server
```

## 🤝 Contributing Guidelines

### 📝 How to Contribute

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### 📋 Code Standards

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Use ES6+ and consistent formatting
- **CSS**: Use BEM methodology for class names
- **Commits**: Use conventional commit messages

## 📄 License & Legal

### 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### ⚖️ Disclaimer

This software is provided "as-is" for educational and demonstration purposes. The authors are not responsible for any damages arising from the use of this software.

## 📞 Support & Contact

### 🆘 Getting Help

- **Documentation**: Check this README and `PROJECT_SUMMARY.md`
- **Issues**: Report bugs on GitHub Issues
- **Features**: Request features via GitHub Discussions
- **Email**: [Your email for support]

### 🔗 Useful Links

- **GitHub Repository**: https://github.com/VinayakKamankar1/Chemical-Equipment-Analyzer
- **Django Documentation**: https://docs.djangoproject.com/
- **React Documentation**: https://reactjs.org/docs/
- **PyQt5 Documentation**: https://doc.qt.io/qtforpython/

---

## 🎉 Acknowledgments

Thank you to all contributors and the open-source community for making this project possible!

**Built with ❤️ for the Chemical Engineering Community**


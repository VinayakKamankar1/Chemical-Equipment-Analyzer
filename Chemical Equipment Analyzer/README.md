# Chemical Equipment Analyzer

A hybrid application consisting of a Web app (React) and a Desktop app (PyQt5) connected to a common Django REST backend for chemical equipment data visualization and analytics.

## Features

- **CSV Upload**: Upload CSV files containing chemical equipment parameters
- **Data Analytics**: Automatic computation of summary statistics:
  - Total equipment count
  - Average flowrate, pressure, and temperature
  - Equipment type distribution
- **Data Visualization**: Interactive charts in both Web and Desktop interfaces
- **History Management**: Store and view the last 5 uploaded datasets
- **PDF Reports**: Generate downloadable PDF summary reports
- **Authentication**: Secure token-based authentication

## Project Structure

```
Chemical Equipment Analyzer/
├── backend/                 # Django REST API
│   ├── equipment_analyzer/ # Django project settings
│   ├── api/                # API app with models, views, serializers
│   ├── manage.py
│   └── requirements.txt
├── web/                    # React web application
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── utils/          # API client and auth utilities
│   │   └── App.js
│   └── package.json
├── desktop/                # PyQt5 desktop application
│   ├── app/
│   │   ├── api_client.py   # API client
│   │   ├── main_window.py  # Main application window
│   │   ├── login_dialog.py # Login/Register dialog
│   │   └── history_widget.py
│   ├── main.py
│   └── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- pip (Python package manager)

## Setup Instructions

### 1. Backend Setup (Django)

```bash
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

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 2. Web Application Setup (React)

```bash
cd web

# Install dependencies
npm install

# Start development server
npm start
```

The web app will be available at `http://localhost:3000`

### 3. Desktop Application Setup (PyQt5)

```bash
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

## CSV File Format

The CSV files must contain the following columns (case-insensitive):

- **Equipment Name**: Name of the equipment
- **Type**: Type/category of equipment
- **Flowrate**: Flow rate value (numeric)
- **Pressure**: Pressure value (numeric)
- **Temperature**: Temperature value (numeric)

Example CSV:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,25.3,180.2
Distillation Column B,Distillation,200.0,30.1,200.5
Heat Exchanger C,Heat Exchanger,175.8,22.7,150.0
```

## API Endpoints

### Authentication
- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login and get authentication token

### Data Operations
- `POST /api/upload/` - Upload and analyze CSV file (requires authentication)
- `GET /api/history/` - Get upload history (last 5 datasets)
- `GET /api/summary/<id>/` - Get detailed summary of a dataset
- `GET /api/summary/<id>/pdf/` - Download PDF report

## Usage

### Web Application

1. Open `http://localhost:3000` in your browser
2. Register a new account or login
3. Navigate to "Upload CSV" tab
4. Select and upload a CSV file
5. View visualizations in the "Visualization" tab
6. Check upload history in the "History" tab
7. Download PDF reports from the history or visualization views

### Desktop Application

1. Run `python main.py` from the desktop directory
2. Login or register a new account
3. Use "Select CSV File" button to upload a file
4. View visualizations in the "Visualization" tab
5. Check history in the "History" tab
6. Double-click history items to view details
7. Download PDF reports from the visualization view

## Technologies Used

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Pandas 2.1.3
- ReportLab 4.0.7
- SQLite (default database)

### Web Frontend
- React 18.2.0
- Chart.js 4.4.0
- Axios 1.6.2

### Desktop Frontend
- PyQt5 5.15.10
- Matplotlib 3.8.2
- Requests 2.31.0

## Error Handling

The application includes comprehensive error handling for:
- Invalid CSV files (missing columns, wrong format)
- Authentication failures
- Network errors
- Invalid data types
- Empty files

## Development Notes

- The backend stores only the last 5 datasets per user
- CSV files are processed in-memory (not stored on disk)
- Authentication tokens are stored in localStorage (web) and memory (desktop)
- PDF reports are generated on-demand using ReportLab

## Troubleshooting

### Backend Issues
- Ensure Django server is running on port 8000
- Check that migrations have been applied
- Verify database file (db.sqlite3) is writable

### Web App Issues
- Ensure backend is running before starting web app
- Check CORS settings if API calls fail
- Clear browser cache if authentication issues occur

### Desktop App Issues
- Ensure backend is running before starting desktop app
- Check Python version (3.8+ required)
- Verify all dependencies are installed

## License

This project is provided as-is for educational and demonstration purposes.


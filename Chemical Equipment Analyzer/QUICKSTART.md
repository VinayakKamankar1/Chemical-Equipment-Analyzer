# Quick Start Guide

## Step-by-Step Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database and run migrations
python manage.py makemigrations
python manage.py migrate

# (Optional) Create admin user
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### 2. Web Application Setup

Open a new terminal:

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Start the development server
npm start
```

The web app will open automatically at `http://localhost:3000`

### 3. Desktop Application Setup

Open a new terminal:

```bash
# Navigate to desktop directory
cd desktop

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Testing the Application

1. **Register/Login**: Use either the web or desktop app to create an account
2. **Upload CSV**: Use the provided `sample_data.csv` file to test the upload functionality
3. **View Visualizations**: Check the charts and statistics after uploading
4. **Check History**: View your upload history (last 5 datasets)
5. **Download PDF**: Generate and download PDF reports

## Sample CSV Format

The CSV file should have these columns (case-insensitive):
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

See `sample_data.csv` in the root directory for an example.

## Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check that all dependencies are installed
- Verify migrations have been run

### Web app can't connect to backend
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API_BASE_URL in `web/src/utils/api.js`

### Desktop app can't connect
- Ensure backend is running on port 8000
- Check that API_BASE_URL in `desktop/app/api_client.py` is correct
- Verify all Python dependencies are installed

### CSV upload fails
- Check that CSV has all required columns
- Ensure column names match (case-insensitive)
- Verify numeric columns contain valid numbers


"""
Configuration settings for the Flask application.
Change these values to match your local MySQL setup.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# MySQL database connection settings
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Ayush11#'),
    'database': os.getenv('DB_NAME', 'academic_results'),
}

# Flask secret key for sessions (change in production)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Folder paths for uploads and PDF reports
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
REPORTS_FOLDER = os.path.join(os.path.dirname(__file__), 'reports')

# Allowed file types for CSV upload
ALLOWED_EXTENSIONS = {'csv'}

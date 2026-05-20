"""
Cloud-Enabled Academic Result Automation System
Main Flask application entry point.

Run locally: python app.py
Then open: http://127.0.0.1:5000
"""

import os
from flask import Flask
from flask_login import LoginManager
from config import SECRET_KEY, UPLOAD_FOLDER, REPORTS_FOLDER
from models.user import User

# Import route blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.teacher import teacher_bp
from routes.student import student_bp


def create_app():
    """Application factory - creates and configures the Flask app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['REPORTS_FOLDER'] = REPORTS_FOLDER

    # Create upload and reports folders if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(REPORTS_FOLDER, exist_ok=True)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    # Register blueprints (modular routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    # Run development server (local only)
    print("=" * 50)
    print("Academic Result Automation System")
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)

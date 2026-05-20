"""
User model for Flask-Login authentication.
Wraps database user row for session management.
"""

from flask_login import UserMixin
from models.db import execute_query


class User(UserMixin):
    """Represents a logged-in user."""

    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.role = user_data['role']
        self.password_hash = user_data.get('password', '')

    @staticmethod
    def get_by_id(user_id):
        """Load user from database by ID."""
        data = execute_query(
            "SELECT id, username, password, role FROM users WHERE id = %s",
            (user_id,),
            fetch_one=True
        )
        return User(data) if data else None

    @staticmethod
    def get_by_username(username):
        """Load user from database by username."""
        data = execute_query(
            "SELECT id, username, password, role FROM users WHERE username = %s",
            (username,),
            fetch_one=True
        )
        return User(data) if data else None

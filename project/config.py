"""
Configuration settings for the Flask application.
Supports Supabase/PostgreSQL via DATABASE_URL or separate DB_* variables.
"""

import os
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-in-production"
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
REPORTS_FOLDER = os.path.join(os.path.dirname(__file__), 'reports')
ALLOWED_EXTENSIONS = {'csv'}


def _build_db_config():
    """
    Build psycopg connection kwargs.
    Important: decode URL-encoded password (e.g. %23 -> #) for Supabase.
    """
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Remove query string (pgbouncer=true breaks psycopg URI connect)
        if "?" in database_url:
            database_url = database_url.split("?", 1)[0]

        parsed = urlparse(database_url)
        return {
            "host": parsed.hostname,
            "port": parsed.port or 5432,
            "user": parsed.username,
            "password": unquote(parsed.password or ""),
            "dbname": (parsed.path or "/postgres").lstrip("/") or "postgres",
            "sslmode": "require",
        }

    # Fallback: local PostgreSQL from separate env vars
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "dbname": os.getenv("DB_NAME", "academic_results"),
    }


DB_CONFIG = _build_db_config()

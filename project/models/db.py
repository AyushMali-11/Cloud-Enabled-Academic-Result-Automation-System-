"""
Database connection helper.
Provides a simple function to get a PostgreSQL connection.
"""

import psycopg
from psycopg.rows import dict_row
from config import DB_CONFIG


def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    Returns None if connection fails.
    """
    try:
        connection = psycopg.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Run a SQL query and optionally return results.
    - fetch_one: return single row as dict
    - fetch_all: return list of dicts
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query_to_run = query
        # Beginner-friendly helper:
        # If this is an INSERT without RETURNING, append "RETURNING id"
        # so existing code can still receive the inserted row id.
        if (
            not fetch_one
            and not fetch_all
            and query.strip().lower().startswith("insert into")
            and "returning" not in query.lower()
        ):
            query_to_run = f"{query.rstrip().rstrip(';')} RETURNING id"

        cursor.execute(query_to_run, params or ())

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            inserted = cursor.fetchone() if cursor.description else None
            conn.commit()
            result = inserted["id"] if inserted and "id" in inserted else True

        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Query error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

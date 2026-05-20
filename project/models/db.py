"""
Database connection helper.
Provides a simple function to get a MySQL connection.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_db_connection():
    """
    Create and return a MySQL database connection.
    Returns None if connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
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
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid

        cursor.close()
        conn.close()
        return result
    except Error as e:
        print(f"Query error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

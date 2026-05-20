"""
Database initialization script.
Creates sample users with properly hashed passwords.

Run once after creating the database schema:
    python init_db.py
"""

from werkzeug.security import generate_password_hash
from models.db import get_db_connection, execute_query

# Default password for all demo accounts
DEFAULT_PASSWORD = 'password123'


def init_users():
    """Insert demo users if they don't exist."""
    users = [
        ('admin', 'admin'),
        ('teacher1', 'teacher'),
        ('student1', 'student'),
        ('student2', 'student'),
    ]

    pwd_hash = generate_password_hash(DEFAULT_PASSWORD)

    for username, role in users:
        existing = execute_query(
            "SELECT id FROM users WHERE username = %s",
            (username,),
            fetch_one=True
        )
        if not existing:
            execute_query(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, pwd_hash, role)
            )
            print(f"Created user: {username} ({role})")
        else:
            # Update password to known demo password
            execute_query(
                "UPDATE users SET password = %s WHERE username = %s",
                (pwd_hash, username)
            )
            print(f"Updated password for: {username}")


def init_profiles():
    """Insert teacher and student profiles linked to users."""
    # Teacher profile
    teacher_user = execute_query(
        "SELECT id FROM users WHERE username = 'teacher1'",
        fetch_one=True
    )
    if teacher_user:
        existing = execute_query(
            "SELECT id FROM teachers WHERE user_id = %s",
            (teacher_user['id'],),
            fetch_one=True
        )
        if not existing:
            execute_query(
                """INSERT INTO teachers (user_id, full_name, department, email)
                   VALUES (%s, %s, %s, %s)""",
                (teacher_user['id'], 'Dr. Sarah Johnson', 'Computer Science', 'sarah.j@college.edu')
            )
            print("Created teacher profile")

    # Student profiles
    students_data = [
        ('student1', 'CS2024001', 'John Doe', 'B.Tech CS - Year 2', 'john.doe@student.edu'),
        ('student2', 'CS2024002', 'Jane Smith', 'B.Tech CS - Year 2', 'jane.smith@student.edu'),
    ]
    for username, roll, name, cls, email in students_data:
        user = execute_query(
            "SELECT id FROM users WHERE username = %s",
            (username,),
            fetch_one=True
        )
        if user:
            existing = execute_query(
                "SELECT id FROM students WHERE user_id = %s",
                (user['id'],),
                fetch_one=True
            )
            if not existing:
                execute_query(
                    """INSERT INTO students (user_id, roll_number, full_name, class_name, email)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (user['id'], roll, name, cls, email)
                )
                print(f"Created student: {name}")


def init_subjects_exams():
    """Insert sample subjects and exams if empty."""
    subjects = execute_query("SELECT COUNT(*) as c FROM subjects", fetch_one=True)
    if subjects and subjects['c'] == 0:
        execute_query(
            "INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES (%s, %s, %s)",
            ('CS101', 'Programming Fundamentals', 100)
        )
        execute_query(
            "INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES (%s, %s, %s)",
            ('CS102', 'Data Structures', 100)
        )
        execute_query(
            "INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES (%s, %s, %s)",
            ('MA101', 'Engineering Mathematics', 100)
        )
        print("Created sample subjects")

    teacher = execute_query("SELECT id FROM teachers LIMIT 1", fetch_one=True)
    subject = execute_query("SELECT id FROM subjects LIMIT 1", fetch_one=True)
    exams = execute_query("SELECT COUNT(*) as c FROM exams", fetch_one=True)

    if teacher and subject and exams and exams['c'] == 0:
        execute_query(
            """INSERT INTO exams (exam_name, exam_date, subject_id, teacher_id)
               VALUES (%s, %s, %s, %s)""",
            ('Mid-Term Exam', '2025-03-15', subject['id'], teacher['id'])
        )
        print("Created sample exam")


if __name__ == '__main__':
    conn = get_db_connection()
    if not conn:
        print("ERROR: Cannot connect to PostgreSQL. Check config.py and .env settings.")
        exit(1)
    conn.close()

    print("Initializing database with sample data...")
    init_users()
    init_profiles()
    init_subjects_exams()
    print("\nDone! Login credentials:")
    print("  Admin:   admin / password123")
    print("  Teacher: teacher1 / password123")
    print("  Student: student1 / password123")

"""
Admin dashboard routes.
Admin can view all users, students, teachers, subjects, and system stats.
"""

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.security import generate_password_hash
from models.db import execute_query

# Default password for new accounts if admin leaves password blank
DEFAULT_NEW_PASSWORD = 'password123'

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator: only admin role can access."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with overview statistics."""
    def _count(table):
        row = execute_query(f"SELECT COUNT(*) as c FROM {table}", fetch_one=True)
        return row['c'] if row else 0

    stats = {
        'users': _count('users'),
        'students': _count('students'),
        'teachers': _count('teachers'),
        'subjects': _count('subjects'),
        'exams': _count('exams'),
        'results': _count('results'),
    }

    students = execute_query(
        """SELECT s.id, s.user_id, s.roll_number, s.full_name, s.class_name, s.email, u.username
           FROM students s JOIN users u ON s.user_id = u.id
           ORDER BY s.roll_number""",
        fetch_all=True
    ) or []

    teachers = execute_query(
        """SELECT t.id, t.user_id, t.full_name, t.department, t.email, u.username
           FROM teachers t JOIN users u ON t.user_id = u.id
           ORDER BY t.full_name""",
        fetch_all=True
    ) or []

    subjects = execute_query("SELECT * FROM subjects", fetch_all=True) or []

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        students=students,
        teachers=teachers,
        subjects=subjects
    )


@admin_bp.route('/add-subject', methods=['POST'])
@login_required
@admin_required
def add_subject():
    """Add a new subject."""
    code = request.form.get('subject_code', '').strip()
    name = request.form.get('subject_name', '').strip()
    max_marks = request.form.get('max_marks', 100)

    if code and name:
        execute_query(
            "INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES (%s, %s, %s)",
            (code, name, int(max_marks))
        )
        flash('Subject added successfully.', 'success')
    else:
        flash('Please fill all subject fields.', 'warning')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/add-student', methods=['POST'])
@login_required
@admin_required
def add_student():
    """Add a new student (creates login user + student profile)."""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip() or DEFAULT_NEW_PASSWORD
    roll_number = request.form.get('roll_number', '').strip()
    full_name = request.form.get('full_name', '').strip()
    class_name = request.form.get('class_name', '').strip()
    email = request.form.get('email', '').strip()

    if not all([username, roll_number, full_name]):
        flash('Username, roll number, and full name are required.', 'warning')
        return redirect(url_for('admin.dashboard'))

    if execute_query("SELECT id FROM users WHERE username = %s", (username,), fetch_one=True):
        flash(f'Username "{username}" already exists.', 'danger')
        return redirect(url_for('admin.dashboard'))

    if execute_query("SELECT id FROM students WHERE roll_number = %s", (roll_number,), fetch_one=True):
        flash(f'Roll number "{roll_number}" already exists.', 'danger')
        return redirect(url_for('admin.dashboard'))

    pwd_hash = generate_password_hash(password)
    user_id = execute_query(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, 'student')",
        (username, pwd_hash)
    )

    if user_id:
        execute_query(
            """INSERT INTO students (user_id, roll_number, full_name, class_name, email)
               VALUES (%s, %s, %s, %s, %s)""",
            (user_id, roll_number, full_name, class_name or None, email or None)
        )
        flash(f'Student "{full_name}" added. Login: {username} / {password}', 'success')
    else:
        flash('Failed to add student.', 'danger')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete-student/<int:student_id>', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    """Delete a student and their login account."""
    student = execute_query(
        "SELECT id, user_id, full_name FROM students WHERE id = %s",
        (student_id,),
        fetch_one=True
    )
    if not student:
        flash('Student not found.', 'warning')
        return redirect(url_for('admin.dashboard'))

    # Delete user first; CASCADE removes student, marks, and results
    execute_query("DELETE FROM users WHERE id = %s", (student['user_id'],))
    flash(f'Student "{student["full_name"]}" deleted.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/add-teacher', methods=['POST'])
@login_required
@admin_required
def add_teacher():
    """Add a new teacher (creates login user + teacher profile)."""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip() or DEFAULT_NEW_PASSWORD
    full_name = request.form.get('full_name', '').strip()
    department = request.form.get('department', '').strip()
    email = request.form.get('email', '').strip()

    if not all([username, full_name]):
        flash('Username and full name are required.', 'warning')
        return redirect(url_for('admin.dashboard'))

    if execute_query("SELECT id FROM users WHERE username = %s", (username,), fetch_one=True):
        flash(f'Username "{username}" already exists.', 'danger')
        return redirect(url_for('admin.dashboard'))

    pwd_hash = generate_password_hash(password)
    user_id = execute_query(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, 'teacher')",
        (username, pwd_hash)
    )

    if user_id:
        execute_query(
            """INSERT INTO teachers (user_id, full_name, department, email)
               VALUES (%s, %s, %s, %s)""",
            (user_id, full_name, department or None, email or None)
        )
        flash(f'Teacher "{full_name}" added. Login: {username} / {password}', 'success')
    else:
        flash('Failed to add teacher.', 'danger')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete-teacher/<int:teacher_id>', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    """Delete a teacher and their login account."""
    teacher = execute_query(
        "SELECT id, user_id, full_name FROM teachers WHERE id = %s",
        (teacher_id,),
        fetch_one=True
    )
    if not teacher:
        flash('Teacher not found.', 'warning')
        return redirect(url_for('admin.dashboard'))

    execute_query("DELETE FROM users WHERE id = %s", (teacher['user_id'],))
    flash(f'Teacher "{teacher["full_name"]}" deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

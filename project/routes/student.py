"""
Student dashboard routes.
Students can view their marks, results, and download PDF reports.
"""

import os
from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from functools import wraps
from models.db import execute_query
from utils.pdf_generator import generate_result_pdf
from config import REPORTS_FOLDER

student_bp = Blueprint('student', __name__, url_prefix='/student')


def student_required(f):
    """Decorator: only student role can access."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Access denied. Students only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_student_profile():
    """Get student profile for logged-in user."""
    return execute_query(
        """SELECT s.id, s.roll_number, s.full_name, s.class_name, s.email
           FROM students s WHERE s.user_id = %s""",
        (current_user.id,),
        fetch_one=True
    )


@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard: view marks and results."""
    profile = get_student_profile()
    if not profile:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('auth.logout'))

    results = execute_query(
        """SELECT r.total_marks, r.max_marks, r.percentage, r.grade,
                  e.exam_name, s.subject_name, s.subject_code, r.generated_at
           FROM results r
           JOIN exams e ON r.exam_id = e.id
           JOIN subjects s ON e.subject_id = s.id
           WHERE r.student_id = %s
           ORDER BY r.generated_at DESC""",
        (profile['id'],),
        fetch_all=True
    ) or []

    marks = execute_query(
        """SELECT m.marks_obtained, e.exam_name, s.subject_name
           FROM marks m
           JOIN exams e ON m.exam_id = e.id
           JOIN subjects s ON e.subject_id = s.id
           WHERE m.student_id = %s""",
        (profile['id'],),
        fetch_all=True
    ) or []

    return render_template(
        'student/dashboard.html',
        profile=profile,
        results=results,
        marks=marks
    )


@student_bp.route('/download-pdf')
@login_required
@student_required
def download_pdf():
    """Generate and download PDF result report."""
    profile = get_student_profile()
    if not profile:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('student.dashboard'))

    results = execute_query(
        """SELECT r.total_marks, r.max_marks, r.percentage, r.grade,
                  e.exam_name, s.subject_name
           FROM results r
           JOIN exams e ON r.exam_id = e.id
           JOIN subjects s ON e.subject_id = s.id
           WHERE r.student_id = %s""",
        (profile['id'],),
        fetch_all=True
    ) or []

    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    filename = f"result_{profile['roll_number']}.pdf"
    filepath = os.path.join(REPORTS_FOLDER, filename)

    try:
        generate_result_pdf(profile, results, filepath)
    except Exception as e:
        flash(f'Could not generate PDF: {e}', 'danger')
        return redirect(url_for('student.dashboard'))

    return send_file(filepath, as_attachment=True, download_name=filename)

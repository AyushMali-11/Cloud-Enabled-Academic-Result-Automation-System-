"""
Teacher dashboard routes.
Teachers can upload CSV marks, create exams, and generate results.
"""

import os
import csv
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
from models.db import execute_query
from utils.result_service import process_marks_for_exam
from config import ALLOWED_EXTENSIONS

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')


def teacher_required(f):
    """Decorator: only teacher role can access."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('Access denied. Teachers only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_teacher_id():
    """Get teacher profile ID for logged-in user."""
    row = execute_query(
        "SELECT id FROM teachers WHERE user_id = %s",
        (current_user.id,),
        fetch_one=True
    )
    return row['id'] if row else None


@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Teacher dashboard: exams, upload CSV, view marks."""
    teacher_id = get_teacher_id()
    exams = execute_query(
        """SELECT e.id, e.exam_name, e.exam_date, s.subject_name, s.subject_code
           FROM exams e
           JOIN subjects s ON e.subject_id = s.id
           WHERE e.teacher_id = %s OR e.teacher_id IS NULL
           ORDER BY e.exam_date DESC""",
        (teacher_id,),
        fetch_all=True
    ) or []

    subjects = execute_query("SELECT id, subject_code, subject_name FROM subjects", fetch_all=True) or []

    marks_summary = execute_query(
        """SELECT e.exam_name, COUNT(m.id) as mark_count
           FROM exams e
           LEFT JOIN marks m ON e.id = m.exam_id
           GROUP BY e.id, e.exam_name""",
        fetch_all=True
    ) or []

    return render_template(
        'teacher/dashboard.html',
        exams=exams,
        subjects=subjects,
        marks_summary=marks_summary
    )


@teacher_bp.route('/create-exam', methods=['POST'])
@login_required
@teacher_required
def create_exam():
    """Create a new exam for a subject."""
    exam_name = request.form.get('exam_name', '').strip()
    exam_date = request.form.get('exam_date') or None
    subject_id = request.form.get('subject_id')
    teacher_id = get_teacher_id()

    if exam_name and subject_id:
        execute_query(
            "INSERT INTO exams (exam_name, exam_date, subject_id, teacher_id) VALUES (%s, %s, %s, %s)",
            (exam_name, exam_date, subject_id, teacher_id)
        )
        flash('Exam created successfully.', 'success')
    else:
        flash('Please fill exam name and subject.', 'warning')

    return redirect(url_for('teacher.dashboard'))


@teacher_bp.route('/upload-csv', methods=['POST'])
@login_required
@teacher_required
def upload_csv():
    """
    Upload CSV file with marks.
    Expected CSV format: roll_number, marks_obtained
    Example:
        CS2024001,85
        CS2024002,92
    """
    exam_id = request.form.get('exam_id')
    if not exam_id:
        flash('Please select an exam.', 'warning')
        return redirect(url_for('teacher.dashboard'))

    if 'csv_file' not in request.files:
        flash('No file selected.', 'warning')
        return redirect(url_for('teacher.dashboard'))

    file = request.files['csv_file']
    if file.filename == '' or not allowed_file(file.filename):
        flash('Please upload a valid CSV file.', 'warning')
        return redirect(url_for('teacher.dashboard'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Parse CSV and insert marks
    success_count = 0
    error_rows = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader, start=1):
                if len(row) < 2:
                    continue
                # Skip header row if present
                if row_num == 1 and not str(row[1]).replace('.', '').isdigit():
                    if 'roll' in row[0].lower() or 'marks' in str(row[1]).lower():
                        continue

                roll_number = row[0].strip()
                try:
                    marks_obtained = float(row[1].strip())
                except ValueError:
                    error_rows.append(f"Row {row_num}: invalid marks")
                    continue

                student = execute_query(
                    "SELECT id FROM students WHERE roll_number = %s",
                    (roll_number,),
                    fetch_one=True
                )
                if not student:
                    error_rows.append(f"Row {row_num}: student {roll_number} not found")
                    continue

                execute_query(
                    """INSERT INTO marks (student_id, exam_id, marks_obtained)
                       VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE marks_obtained = VALUES(marks_obtained)""",
                    (student['id'], exam_id, marks_obtained)
                )
                success_count += 1

        # Auto-generate results after upload
        process_marks_for_exam(int(exam_id))
        flash(f'Uploaded {success_count} marks. Results generated automatically.', 'success')

        if error_rows:
            flash(f'Some rows skipped: {"; ".join(error_rows[:5])}', 'warning')

    except Exception as e:
        flash(f'Error reading CSV: {str(e)}', 'danger')
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return redirect(url_for('teacher.dashboard'))


@teacher_bp.route('/generate-results/<int:exam_id>')
@login_required
@teacher_required
def generate_results(exam_id):
    """Manually trigger result generation for an exam."""
    if process_marks_for_exam(exam_id):
        flash('Results generated successfully.', 'success')
    else:
        flash('Could not generate results.', 'danger')
    return redirect(url_for('teacher.dashboard'))

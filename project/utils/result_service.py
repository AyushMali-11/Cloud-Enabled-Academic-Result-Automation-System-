"""
Result generation service.
Processes marks and stores calculated results in the database.
"""

from models.db import execute_query
from utils.grade_calculator import generate_result


def process_marks_for_exam(exam_id):
    """
    For a given exam, read all marks and generate/update results.
    Called after CSV upload or manual mark entry.
    """
    # Get exam and subject max marks
    exam = execute_query(
        """SELECT e.id, s.max_marks, s.subject_name, e.exam_name
           FROM exams e
           JOIN subjects s ON e.subject_id = s.id
           WHERE e.id = %s""",
        (exam_id,),
        fetch_one=True
    )
    if not exam:
        return False

    max_marks = exam['max_marks']

    # Get all marks for this exam
    marks_list = execute_query(
        "SELECT id, student_id, marks_obtained FROM marks WHERE exam_id = %s",
        (exam_id,),
        fetch_all=True
    )
    if not marks_list:
        return True

    for mark in marks_list:
        obtained = float(mark['marks_obtained'])
        percentage, grade = generate_result(obtained, max_marks)

        # Insert or update result
        execute_query(
            """INSERT INTO results (student_id, exam_id, total_marks, max_marks, percentage, grade)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (student_id, exam_id) DO UPDATE SET
               total_marks = EXCLUDED.total_marks,
               max_marks = EXCLUDED.max_marks,
               percentage = EXCLUDED.percentage,
               grade = EXCLUDED.grade,
               generated_at = CURRENT_TIMESTAMP""",
            (mark['student_id'], exam_id, obtained, max_marks, percentage, grade)
        )

    return True

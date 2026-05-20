"""
PDF report generation using ReportLab.
Creates a simple student result report.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_result_pdf(student_info, results_list, output_path):
    """
    Generate a PDF report for a student's exam results.

    student_info: dict with full_name, roll_number, class_name
    results_list: list of dicts with exam_name, subject_name, percentage, grade
    output_path: full path where PDF will be saved
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph(
        "<b>Academic Result Report</b>",
        styles['Title']
    )
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Student details
    student_text = (
        f"<b>Name:</b> {student_info.get('full_name', 'N/A')}<br/>"
        f"<b>Roll Number:</b> {student_info.get('roll_number', 'N/A')}<br/>"
        f"<b>Class:</b> {student_info.get('class_name', 'N/A')}<br/>"
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    elements.append(Paragraph(student_text, styles['Normal']))
    elements.append(Spacer(1, 30))

    # Results table
    if results_list:
        table_data = [['Exam', 'Subject', 'Marks', 'Max', 'Percentage', 'Grade']]
        for r in results_list:
            pct = r.get('percentage', 0)
            table_data.append([
                str(r.get('exam_name', '') or ''),
                str(r.get('subject_name', '') or ''),
                str(r.get('total_marks', '')),
                str(r.get('max_marks', '')),
                f"{float(pct):.1f}%",
                str(r.get('grade', '') or ''),
            ])

        # TableStyle format: (COMMAND, (col0, row0), (col1, row1), value)
        table = Table(table_data, colWidths=[80, 100, 50, 50, 70, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No results available.", styles['Normal']))

    doc.build(elements)
    return output_path

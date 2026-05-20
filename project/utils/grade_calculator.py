"""
Grade and percentage calculation utilities.
Beginner-friendly logic for academic grading.
"""


def calculate_percentage(obtained, maximum):
    """Calculate percentage from marks obtained and max marks."""
    if maximum <= 0:
        return 0.0
    return round((obtained / maximum) * 100, 2)


def calculate_grade(percentage):
    """
    Convert percentage to letter grade.
    Standard grading scale used in many colleges.
    """
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'


def generate_result(obtained, maximum):
    """
    Generate percentage and grade from marks.
    Returns a tuple: (percentage, grade)
    """
    percentage = calculate_percentage(obtained, maximum)
    grade = calculate_grade(percentage)
    return percentage, grade

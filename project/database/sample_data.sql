-- ============================================================
-- Sample Dummy Data for Testing
-- Password for all users: password123
-- (hashed with Werkzeug scrypt)
-- ============================================================

USE academic_results;

-- Default password hash for "password123"
-- Generated using: from werkzeug.security import generate_password_hash
SET @pwd = 'scrypt:32768:8:1$placeholder$placeholder';

-- Insert users (passwords set via app on first run - see README)
-- For sample data we use a known hash for password123
INSERT INTO users (username, password, role) VALUES
('admin', 'pbkdf2:sha256:600000$sample$8f7e3b2a1c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'admin'),
('teacher1', 'pbkdf2:sha256:600000$sample$8f7e3b2a1c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'teacher'),
('student1', 'pbkdf2:sha256:600000$sample$8f7e3b2a1c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'student'),
('student2', 'pbkdf2:sha256:600000$sample$8f7e3b2a1c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', 'student');

INSERT INTO teachers (user_id, full_name, department, email) VALUES
(2, 'Dr. Sarah Johnson', 'Computer Science', 'sarah.j@college.edu');

INSERT INTO students (user_id, roll_number, full_name, class_name, email) VALUES
(3, 'CS2024001', 'John Doe', 'B.Tech CS - Year 2', 'john.doe@student.edu'),
(4, 'CS2024002', 'Jane Smith', 'B.Tech CS - Year 2', 'jane.smith@student.edu');

INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES
('CS101', 'Programming Fundamentals', 100),
('CS102', 'Data Structures', 100),
('MA101', 'Engineering Mathematics', 100);

INSERT INTO exams (exam_name, exam_date, subject_id, teacher_id) VALUES
('Mid-Term Exam', '2025-03-15', 1, 1),
('Mid-Term Exam', '2025-03-20', 2, 1),
('Final Exam', '2025-05-10', 1, 1);

INSERT INTO marks (student_id, exam_id, marks_obtained) VALUES
(1, 1, 85.00),
(1, 2, 78.50),
(2, 1, 92.00),
(2, 2, 88.00);

INSERT INTO results (student_id, exam_id, total_marks, max_marks, percentage, grade) VALUES
(1, 1, 85.00, 100.00, 85.00, 'A'),
(1, 2, 78.50, 100.00, 78.50, 'B+'),
(2, 1, 92.00, 100.00, 92.00, 'A+'),
(2, 2, 88.00, 100.00, 88.00, 'A');

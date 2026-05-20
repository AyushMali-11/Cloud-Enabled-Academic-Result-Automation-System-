-- ============================================================
-- Academic Result System — Supabase SQL Editor
-- Paste this in: Supabase Dashboard → SQL → New query → Run
-- ============================================================
-- Do NOT use CREATE DATABASE or \connect (Supabase manages that).
-- Tables are created in schema: public
-- ============================================================

-- Optional: reset tables (run only if you want a clean reinstall)
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS marks CASCADE;
DROP TABLE IF EXISTS exams CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ------------------------------------------------------------
-- 1) users — login for admin, teacher, student
-- ------------------------------------------------------------
CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- 2) teachers
-- ------------------------------------------------------------
CREATE TABLE teachers (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    email VARCHAR(100)
);

-- ------------------------------------------------------------
-- 3) students
-- ------------------------------------------------------------
CREATE TABLE students (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(50),
    email VARCHAR(100)
);

-- ------------------------------------------------------------
-- 4) subjects
-- ------------------------------------------------------------
CREATE TABLE subjects (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    max_marks INT DEFAULT 100
);

-- ------------------------------------------------------------
-- 5) exams
-- ------------------------------------------------------------
CREATE TABLE exams (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exam_name VARCHAR(100) NOT NULL,
    exam_date DATE,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES teachers(id) ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- 6) marks (CSV upload stores here)
-- ------------------------------------------------------------
CREATE TABLE marks (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    exam_id INT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    marks_obtained DECIMAL(5,2) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_exam UNIQUE (student_id, exam_id)
);

-- ------------------------------------------------------------
-- 7) results (auto-calculated percentage & grade)
-- ------------------------------------------------------------
CREATE TABLE results (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    exam_id INT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    total_marks DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_exam_result UNIQUE (student_id, exam_id)
);

-- ============================================================
-- SAMPLE DATA (optional)
-- Login passwords in sample_data.sql are placeholders.
-- Recommended: after tables exist, run locally:
--   .\venv\Scripts\python init_db.py
-- with .env pointing to your Supabase connection.
-- ============================================================

-- Example: insert subjects only (safe to run in Supabase)
/*
INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES
('CS101', 'Programming Fundamentals', 100),
('CS102', 'Data Structures', 100),
('MA101', 'Engineering Mathematics', 100);
*/

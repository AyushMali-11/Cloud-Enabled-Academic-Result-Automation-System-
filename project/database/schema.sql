-- ============================================================
-- Cloud-Enabled Academic Result Automation System
-- PostgreSQL Database Schema
-- Run:
--   psql -U postgres -d postgres -f database/schema.sql
-- ============================================================

DROP DATABASE IF EXISTS academic_results;
CREATE DATABASE academic_results;
\connect academic_results;

-- Users table: login credentials for all roles
CREATE TABLE IF NOT EXISTS users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teachers table: teacher profile linked to users
CREATE TABLE IF NOT EXISTS teachers (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    email VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Students table: student profile linked to users
CREATE TABLE IF NOT EXISTS students (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(50),
    email VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    max_marks INT DEFAULT 100
);

-- Exams table
CREATE TABLE IF NOT EXISTS exams (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exam_name VARCHAR(100) NOT NULL,
    exam_date DATE,
    subject_id INT NOT NULL,
    teacher_id INT,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
);

-- Marks table: raw marks per student per exam
CREATE TABLE IF NOT EXISTS marks (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    marks_obtained DECIMAL(5,2) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_exam UNIQUE (student_id, exam_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
);

-- Results table: calculated percentage and grade
CREATE TABLE IF NOT EXISTS results (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    total_marks DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_exam_result UNIQUE (student_id, exam_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
);

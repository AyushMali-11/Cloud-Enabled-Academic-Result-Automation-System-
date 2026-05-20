# Cloud-Enabled Academic Result Automation System

A beginner-friendly full-stack web application for managing academic results with role-based access, CSV mark upload, automatic grade calculation, and PDF report generation.

## Tech Stack

| Layer      | Technology        |
|-----------|-------------------|
| Backend   | Python Flask      |
| Database  | MySQL             |
| Frontend  | HTML, CSS, Bootstrap 5, JavaScript |
| PDF       | ReportLab         |

## Project Structure

```
project/
├── app.py                 # Main Flask entry point
├── config.py              # Database & app settings
├── init_db.py             # Sample users & data setup
├── requirements.txt       # Python dependencies
├── routes/                # URL routes (modular)
│   ├── auth.py            # Login / logout
│   ├── admin.py           # Admin dashboard
│   ├── teacher.py         # Teacher + CSV upload
│   └── student.py         # Student + PDF download
├── models/                # Database & user models
├── utils/                 # Grade calc, PDF, results
├── templates/             # HTML pages (Jinja2)
├── static/                # CSS & JavaScript
├── database/              # SQL schema & sample data
├── uploads/               # Temporary CSV uploads
└── reports/               # Generated PDF files
```

## Features

1. **Login system** – Secure login with hashed passwords
2. **Admin dashboard** – View stats, add/delete students & teachers, add subjects
3. **Teacher dashboard** – Create exams, upload CSV marks
4. **Student dashboard** – View results, download PDF
5. **RBAC** – Admin, Teacher, Student roles with route protection
6. **CSV upload** – Bulk marks import (`roll_number, marks_obtained`)
7. **Auto result generation** – Percentage & grade calculated automatically
8. **PDF reports** – Downloadable result report per student

## Step-by-Step Setup (Local)

### Prerequisites

- Python 3.9+
- MySQL Server (e.g. MySQL 8.0 or XAMPP/WAMP)
- pip

### Step 1: Clone / Open Project

```bash
cd project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL

1. Start MySQL service.
2. Copy environment file and edit your password:

```bash
copy .env.example .env
```

Edit `.env`:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=academic_results
SECRET_KEY=any-random-secret-string
```

### Step 5: Create Database

**Option A – MySQL command line:**

```bash
mysql -u root -p < database/schema.sql
```

**Option B – MySQL Workbench:**

Open `database/schema.sql` and run the script.

### Step 6: Initialize Sample Data

```bash
python init_db.py
```

This creates demo users and sample subjects/exams.

### Step 7: Run the Application

```bash
python app.py
```

Open in browser: **http://127.0.0.1:5000**

## Demo Login Credentials

| Role    | Username  | Password      |
|---------|-----------|---------------|
| Admin   | admin     | password123   |
| Teacher | teacher1  | password123   |
| Student | student1  | password123   |

## CSV Upload Format

Teachers can upload a CSV file with this format:

```csv
roll_number,marks_obtained
CS2024001,85
CS2024002,92
```

A sample file is included: `uploads/sample_marks.csv`

After upload, results are **automatically generated** (percentage + grade).

## Grading Scale

| Percentage | Grade |
|-----------|-------|
| 90+       | A+    |
| 80–89     | A     |
| 70–79     | B+    |
| 60–69     | B     |
| 50–59     | C     |
| 40–49     | D     |
| Below 40  | F     |

## Module Overview

| Module | Purpose |
|--------|---------|
| `app.py` | Starts Flask, registers blueprints |
| `config.py` | DB credentials from `.env` |
| `models/db.py` | MySQL connection helper |
| `models/user.py` | Flask-Login user object |
| `routes/auth.py` | Login, logout, role redirect |
| `routes/admin.py` | Admin-only pages |
| `routes/teacher.py` | CSV upload, exam creation |
| `routes/student.py` | View results, PDF download |
| `utils/grade_calculator.py` | Percentage & grade logic |
| `utils/result_service.py` | Saves results to DB |
| `utils/pdf_generator.py` | Creates PDF reports |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Database connection error | Check MySQL is running and `.env` credentials |
| Login fails | Run `python init_db.py` again to reset passwords |
| CSV upload fails | Ensure roll numbers exist in `students` table |
| PDF download empty | Upload marks and generate results first |

## Future: Cloud Deployment

This project is designed to run **locally first**. For cloud deployment later, consider:

- Host Flask on **PythonAnywhere**, **Render**, or **AWS Elastic Beanstalk**
- Use **Amazon RDS** or **PlanetScale** for managed MySQL
- Store uploads in **S3** instead of local `uploads/` folder

---

Built for learning. Keep code simple, read comments in each file, and experiment!

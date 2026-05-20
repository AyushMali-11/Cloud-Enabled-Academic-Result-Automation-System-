"""
Authentication routes: login, logout, role-based redirect.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models.db import execute_query

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Home page - redirect to login or dashboard based on role."""
    if current_user.is_authenticated:
        return redirect(_dashboard_for_role(current_user.role))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - validates username and password."""
    if current_user.is_authenticated:
        return redirect(_dashboard_for_role(current_user.role))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.get_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(_dashboard_for_role(user.role))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Allow any logged-in user (admin, teacher, student) to change password."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not current_password or not new_password:
            flash('Please fill in all password fields.', 'warning')
            return redirect(url_for('auth.change_password'))

        if len(new_password) < 6:
            flash('New password must be at least 6 characters.', 'warning')
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('auth.change_password'))

        user = User.get_by_id(current_user.id)
        if not user or not check_password_hash(user.password_hash, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('auth.change_password'))

        new_hash = generate_password_hash(new_password)
        execute_query(
            "UPDATE users SET password = %s WHERE id = %s",
            (new_hash, current_user.id)
        )
        flash('Password changed successfully.', 'success')
        return redirect(_dashboard_for_role(current_user.role))

    return render_template('change_password.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


def _dashboard_for_role(role):
    """Return the correct dashboard URL for each role (RBAC)."""
    if role == 'admin':
        return url_for('admin.dashboard')
    elif role == 'teacher':
        return url_for('teacher.dashboard')
    elif role == 'student':
        return url_for('student.dashboard')
    return url_for('auth.login')

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

# FIX: Import db from extensions.py, and models from models.py
from .extensions import db
from .models import Student_Table, Staff_Table, Admin_Table
from .forms import StudentLoginForm, InstructorLoginForm, AdminLoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/')

auth_bp = Blueprint('auth', __name__, url_prefix='/')

def attempt_login(form, UserClass, email_field):
    """Generic function to attempt login for any user type."""
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Use getattr to dynamically find the correct email column if needed, 
        # but here we assume 'Email' is the column name for simplicity and consistency
        user = UserClass.query.filter_by(Email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Login successful. Welcome, {user.get_id().split('_')[0]}!", 'text-green-600')

            # Determine where to redirect based on the user type
            if isinstance(user, Student_Table):
                return redirect(url_for('dashboards.student_dashboard'))
            elif isinstance(user, Staff_Table):
                return redirect(url_for('dashboards.instructor_dashboard'))
            elif isinstance(user, Admin_Table):
                return redirect(url_for('dashboards.admin_dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'text-red-600')
    return None # Return None if validation fails or redirect doesn't happen

# --- Routes ---

@auth_bp.route('/')
def index():
    """Home page with login links."""
    return render_template('index.html')

@auth_bp.route('/student_login', methods=['GET', 'POST'])
def student_login():
    """Handle Student Login."""
    form = StudentLoginForm()
    
    # Attempt login using the helper function
    redirect_response = attempt_login(form, Student_Table, 'Email')
    if redirect_response:
        return redirect_response

    return render_template('student_login.html', form=form)

@auth_bp.route('/instructor_login', methods=['GET', 'POST'])
def instructor_login():
    """Handle Instructor/Staff Login."""
    form = InstructorLoginForm()

    # Attempt login using the helper function
    redirect_response = attempt_login(form, Staff_Table, 'Email')
    if redirect_response:
        return redirect_response

    return render_template('instructor_login.html', form=form)


@auth_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Handle Admin Login."""
    form = AdminLoginForm()

    # Attempt login using the helper function
    redirect_response = attempt_login(form, Admin_Table, 'Email')
    if redirect_response:
        return redirect_response

    return render_template('admin_login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'text-green-600')
    return redirect(url_for('auth.index'))

@auth_bp.route('/register')
def register():
    """Placeholder for student registration page (if implemented)."""
    # Assuming registration form is also in forms.py, but not provided yet.
    # For now, we'll just show a simple page.
    return render_template('register.html')
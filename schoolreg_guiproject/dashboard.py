from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func

# FIX: Import db from extensions.py
from .extensions import db
# FIX: Import all models from the new models.py file
from .models import Student_Table, Staff_Table, Admin_Table, Enrollment_Table, Class_Sections, Courses_Table

dashboards_bp = Blueprint('dashboards', __name__, url_prefix='/')

@dashboards_bp.route('/student/dashboard')
@login_required
def student_dashboard():
    """Student Dashboard: Displays schedule and basic info."""
    if not isinstance(current_user, Student_Table):
        flash("Access denied. Please log in as a Student.", 'text-red-600')
        return redirect(url_for('auth.logout'))
        
    # --- Data Fetching ---
    student_id = current_user.Student_ID
    
    schedule_data = db.session.query(
        Class_Sections.Section_ID,
        Courses_Table.Course_Name,
        Class_Sections.Meeting_Time,
        Class_Sections.Room_Number
    ).join(Enrollment_Table, Enrollment_Table.Section_ID == Class_Sections.Section_ID
    ).join(Courses_Table, Courses_Table.Course_ID == Class_Sections.Course_ID
    ).filter(Enrollment_Table.Student_ID == student_id
    ).all()
    # ---------------------
    
    return render_template('student_dashboard.html', schedule=schedule_data)

@dashboards_bp.route('/instructor/dashboard')
@login_required
def instructor_dashboard():
    """Instructor Dashboard: Displays assigned courses and roster counts."""
    if not isinstance(current_user, Staff_Table):
        flash("Access denied. Please log in as an Instructor.", 'text-red-600')
        return redirect(url_for('auth.logout'))

    # --- Data Fetching ---
    staff_id = current_user.Staff_ID
    
    assigned_classes = db.session.query(
        Class_Sections.Section_ID,
        Courses_Table.Course_Name,
        Class_Sections.Meeting_Time,
        func.count(Enrollment_Table.Student_ID).label('student_count')
    ).join(Courses_Table, Courses_Table.Course_ID == Class_Sections.Course_ID
    ).outerjoin(Enrollment_Table, Enrollment_Table.Section_ID == Class_Sections.Section_ID
    ).filter(Class_Sections.Staff_ID == staff_id
    ).group_by(
        Class_Sections.Section_ID, 
        Courses_Table.Course_Name, 
        Class_Sections.Meeting_Time, 
        Class_Sections.Room_Number
    ).all()
    # ---------------------

    return render_template('instructor_dashboard.html', assigned_classes=assigned_classes)

@dashboards_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin Dashboard (Placeholder for system-wide functions)."""
    if not isinstance(current_user, Admin_Table):
        flash("Access denied. Please log in as an Administrator.", 'text-red-600')
        return redirect(url_for('auth.logout'))

    # Simple aggregated counts for admin dashboard (placeholder)
    stats = {
        'total_students': Student_Table.query.count(),
        'total_staff': Staff_Table.query.count(),
        'total_courses': Courses_Table.query.count(),
    }
    
    return render_template('admin_dashboard.html', stats=stats)
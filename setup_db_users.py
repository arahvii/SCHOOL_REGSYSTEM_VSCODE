from schoolreg_guiproject import create_app
from schoolreg_guiproject.models import Student_Table, Staff_Table, Admin_Table # Import models from the dedicated models file
from schoolreg_guiproject.extensions import db # Import db from the dedicated extensions file
from werkzeug.security import generate_password_hash
import sys

# --- Script Configuration ---
DEFAULT_PASSWORD = "password"
ADMIN_EMAIL = "admin@regsystem.edu"
ADMIN_NAME = "Lyka Yoshimura (Admin)"
# ----------------------------

print("--- STARTING USER PASSWORD SETUP SCRIPT ---")

try:
    app = create_app()
except Exception as e:
    print(f"ERROR: Could not create Flask app. Check __init__.py.")
    print(f"Details: {e}")
    # If the app fails to be created, we exit the script
    sys.exit(1)

with app.app_context():
    print(f"Current database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    try:
        # 1. Ensure all tables/columns are present (will create Admin_Table)
        print("Checking/creating database schema...")
        db.create_all()

        # 2. Add or update the Admin user
        admin_user = Admin_Table.query.filter_by(Email=ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = Admin_Table(Admin_Name=ADMIN_NAME, Email=ADMIN_EMAIL)
            db.session.add(admin_user)
            print(f"   ✓ Admin: Created new Admin user {ADMIN_EMAIL}.")
        
        # Set password for Admin
        admin_user.set_password(DEFAULT_PASSWORD)
        print(f"   ✓ Admin: Set password for Admin user.")


        # 3. Add Passwords to Existing Students (if necessary)
        student_count = 0
        students = Student_Table.query.all()
        for student in students:
            # We use the check_password method to avoid hashing if the password is already set to the default
            if not student.PasswordHash or not student.check_password(DEFAULT_PASSWORD): 
                student.set_password(DEFAULT_PASSWORD)
                print(f"   ✓ Student: Set password for {student.Email}")
                student_count += 1

        # 4. Add Passwords to Existing Staff (if necessary)
        staff_count = 0
        staff_members = Staff_Table.query.all()
        for staff in staff_members:
            if not staff.PasswordHash or not staff.check_password(DEFAULT_PASSWORD):
                staff.set_password(DEFAULT_PASSWORD)
                print(f"   ✓ Staff: Set password for {staff.Email}")
                staff_count += 1
            
        # 5. Commit all changes
        db.session.commit()
        print("\n--- SUCCESS: Database setup complete. ---")
        print(f"Default login password for all users is: '{DEFAULT_PASSWORD}'")
        print(f"Admin Login: {ADMIN_EMAIL}")

    except Exception as e:
        db.session.rollback()
        print("\n--- CRITICAL DATABASE ERROR ---")
        print("Possible causes: Incorrect database URI, MySQL service is not running, or schema mismatch (check for missing columns).")
        print(f"Full Error: {e}")
        sys.exit(1)

print("--- SCRIPT FINISHED ---")

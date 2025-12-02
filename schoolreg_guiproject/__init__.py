from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager
from flask_login import UserMixin

# IMPORTANT: We must import the models here so the user loader can find them.
from .models import Student_Table, Staff_Table, Admin_Table

# NOTE: Using a static path is generally not recommended in production, 
# but fine for development.
# DATABASE_URI = 'mysql+pymysql://root:YourPassWord@localhost:3306/db_name'
DATABASE_URI = 'mysql+pymysql://root:YourPassWord@127.0.0.1:3306/db_name'
# --- Application Factory ---

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-very-secret-key-for-session' 
    
    # *** CACHE FIX: Explicitly disable Jinja template caching ***
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.index'
    login_manager.login_message_category = 'info'
    
    # --- Register Blueprints Here (MUST be after db.init_app and login_manager.init_app) ---
    
    # Importing blueprints here prevents the circular dependency linter warning
    # by ensuring all global objects (.db, .login_manager) are initialized first.
    from .auth import auth_bp
    from .dashboard import dashboards_bp # <--- CHANGED FROM .dashboards TO .dashboard
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboards_bp)
    
    # --- End Register Blueprints ---
    
    return app

# --- Flask-Login User Loader ---
@login_manager.user_loader
def load_user(user_id_string):
    """Loads the user object based on the prefixed ID string."""
    parts = user_id_string.split('_')
    if len(parts) != 2:
        return None
        
    user_type, user_id = parts
    
    try:
        user_id = int(user_id)
    except ValueError:
        return None

    if user_type == 'student':
        # Use query.get() for primary key lookups
        return Student_Table.query.get(user_id)
    elif user_type == 'staff':
        return Staff_Table.query.get(user_id)
    elif user_type == 'admin':
        return Admin_Table.query.get(user_id)
        

    return None

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize these objects without an app instance
db = SQLAlchemy()
login_manager = LoginManager()
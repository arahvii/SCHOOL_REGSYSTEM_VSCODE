from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db # Need db instance for model definition

# --- Database Models (Mapped to your SQL schema) ---
class Student_Table(UserMixin, db.Model):
    __tablename__ = 'Student_Table'
    Student_ID = db.Column(db.Integer, primary_key=True)
    Student_FirstName = db.Column(db.String(50), nullable=False)
    Student_LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Enrollment_Status = db.Column(db.String(20), default='Active')
    PasswordHash = db.Column(db.String(255))
    
    @property
    def is_admin(self):
        return False
    @property
    def is_instructor(self):
        return False

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)
    def get_id(self):
        return f"student_{self.Student_ID}" 

class Staff_Table(UserMixin, db.Model):
    __tablename__ = 'Staff_Table'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FirstName = db.Column(db.String(50), nullable=False)
    Staff_LastName = db.Column(db.String(50), nullable=False)
    Title = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(50), nullable=True) 
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255))
    
    @property
    def is_admin(self):
        return False
    @property
    def is_instructor(self):
        return True

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)
    def get_id(self):
        return f"staff_{self.Staff_ID}" 
        
class Admin_Table(UserMixin, db.Model):
    __tablename__ = 'Admin_Table'
    Admin_ID = db.Column(db.Integer, primary_key=True)
    Admin_Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255))
    Role = db.Column(db.String(50), default='Admin')
    
    @property
    def is_admin(self):
        return True
    @property
    def is_instructor(self):
        return False 

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)
    def get_id(self):
        return f"admin_{self.Admin_ID}" 
        
# Tables needed for Dashboard queries (No UserMixin needed here)
class Class_Sections(db.Model):
    __tablename__ = 'Class_Sections'
    Section_ID = db.Column(db.String(20), primary_key=True)
    Course_ID = db.Column(db.String(20))
    Staff_ID = db.Column(db.Integer)
    Meeting_Time = db.Column(db.String(50)) 
    Room_Number = db.Column(db.String(20)) 

class Enrollment_Table(db.Model):
    __tablename__ = 'Enrollment_Table'
    Enrollment_ID = db.Column(db.String(20), primary_key=True)
    Student_ID = db.Column(db.Integer)
    Section_ID = db.Column(db.String(20))
    Status = db.Column(db.String(20), default='ENROLLED')

class Courses_Table(db.Model):
    __tablename__ = 'Courses_Table'
    Course_ID = db.Column(db.String(20), primary_key=True)
    Course_Name = db.Column(db.String(100))
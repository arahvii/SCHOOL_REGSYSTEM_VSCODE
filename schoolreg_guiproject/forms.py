from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# --- Login Forms ---

class StudentLoginForm(FlaskForm):
    """Form for Students to log in."""
    email = StringField('Student Email', validators=[
        DataRequired(), 
        Email(message="Must be a valid email address."),
        Length(min=6, max=100)
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In as Student')

class InstructorLoginForm(FlaskForm):
    """Form for Instructors/Staff to log in."""
    email = StringField('Staff Email', validators=[
        DataRequired(), 
        Email(message="Must be a valid email address."),
        Length(min=6, max=100)
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In as Instructor/Staff')

class AdminLoginForm(FlaskForm):
    """Form for Administrators to log in."""
    email = StringField('Admin Email', validators=[
        DataRequired(), 
        Email(message="Must be a valid email address."),
        Length(min=6, max=100)
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In as Admin')
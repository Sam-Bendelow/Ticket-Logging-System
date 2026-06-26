from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from service_desk_app.app.models import User
import re

# Password validator to enforce complexity
def validate_password_complexity(form, field):
    password = field.data
    if (len(password) < 8 or
        not re.search(r'[A-Z]', password) or
        not re.search(r'[a-z]', password) or
        not re.search(r'[@$!%*?&]', password)):
        raise ValidationError('Password does not meet complexity requirements. Password must be at least 8 charcters long, contain one upper case and lower case letter, and a special character.')

# Form for user registration
class RegistrationForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=120)]
        )
    password = PasswordField('Password', validators=[DataRequired(), validate_password_complexity])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Select Role', choices=[('user', 'Standard User')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account already exists with this email. Please register with a different email address, or sign in.')

# Form for user login    
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=120)]
        )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for submitting tickets
class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    category = SelectField(
        "Category",
        choices=[
            ("Application/Software", "Application/Software"),
            ("Network", "Network"),
            ("Hardware", "Hardware"),
            ("Telephony", "Telephony"),
            ("User Account", "User Account"),
            ("Email", "Email"),
            ("File & Print", "File & Print"),
        ],
        validators=[DataRequired()],
    )
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    status = SelectField('Status', choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')])
    assigned_to = SelectField('Assigned Analyst', coerce=int)
    notes = TextAreaField('Additional Notes')
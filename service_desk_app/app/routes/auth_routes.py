import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from service_desk_app.app import db, login_manager, csrf
from service_desk_app.app.models import User
from service_desk_app.app.forms import RegistrationForm, LoginForm
from wtforms.validators import Email, ValidationError

# Authentication-related routes blueprint
auth_bp = Blueprint('auth', __name__)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    
    form = RegistrationForm()

    print("Form submitted:", form.is_submitted())
    print("Form validated:", form.validate_on_submit())

    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account already exists with this email. Please login or register with a new email.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Proceed with user registration
        user = User(
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        print("User registered:", user.email)

        flash('You have successfully registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

# Route to check if email already exists 
@csrf.exempt
@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    try:
        data = request.get_json(force=True)
        email = data.get('email')

        # Validates email format
        email_validator = Email()
        email_validator (None, type('obj', (object,), {'data': email}))
        
        # Check if email already exists in database
        user = User.query.filter_by(email=email).first()
        return jsonify({'exists': user is not None})
    except ValidationError:
        return jsonify({'error': 'Invalid email format'}), 400
    except Exception as e:
        print("Error in /check-email:", e)
        return jsonify({'error': 'Server error'}), 500

# Route to login to system
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Checks is email is registered in database
        if user is None:
            flash('An account with this email address does not exist. Please register first.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Checks password is correct
        if not user.check_password(form.password.data):
            flash('Password is incorrect. Please try again or sign in with another account.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Login user
        login_user(user)
        flash('Login successful!', 'success')

        # Redirect user based on role
        if user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif user.role == 'analyst':
            return redirect(url_for('analyst.analyst_dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    return render_template('login.html', form=form)

# Route to logout of system
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'info')
    return redirect(url_for('auth.login'))

# Home route which directs users based on role 
@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    return redirect(url_for('auth.login'))

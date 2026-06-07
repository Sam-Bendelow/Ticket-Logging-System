from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from service_desk_app.app import db
from service_desk_app.app.models import Ticket, User, Note
from service_desk_app.app.forms import TicketForm, RegistrationForm
from functools import wraps
from collections import Counter

admin_bp = Blueprint('admin', __name__)

# Defines Admin access requirement
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Administrator access is required.", "danger")

            if current_user.role == 'analyst':
                return redirect(url_for('analyst.analyst_dashboard'))
            
            else:
                return redirect(url_for('user.dashboard'))

        return f(*args, **kwargs)
    return decorated_function

# Admin dashboard route
@admin_bp.route('/admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    tickets = Ticket.query.all()
    users = User.query.all()
    return render_template('dashboard_admin.html', tickets=tickets, users=users)

# Admin API route showing tickets by category & user
@admin_bp.route('/api/ticket-stats')
@login_required
@admin_required
def ticket_stats():
    tickets = Ticket.query.all()
    category_counts = Counter(ticket.category for ticket in tickets)
    user_counts = Counter(ticket.user.email for ticket in tickets)

    categories = [{'category': k, 'count': v} for k, v in category_counts.items()]
    users = [{'user': k, 'count': v} for k, v in user_counts.items()]

    return jsonify({'categories': categories, 'users': users})

# Admin view all tickets route
@admin_bp.route('/admin/tickets')
@login_required
@admin_required
def all_tickets():
    tickets = Ticket.query.all()
    return render_template('view_all_tickets_admin.html', tickets=tickets)

# Admin view all users route
@admin_bp.route('/admin/users')
@login_required
@admin_required
def all_users():
    users = User.query.all()
    return render_template('view_all_users_admin.html', users=users)


# Admin view specific ticket route
@admin_bp.route('/view_ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):

    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role == 'user' and ticket.user_id != current_user.id:
        flash("You do not have permission to view this ticket.", "danger")
        return redirect(url_for('user.dashboard'))
    
    return render_template('view_ticket.html', ticket=ticket)


# Admin delete ticket route
@admin_bp.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
@admin_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket has been deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))


# Admin update ticket route
@admin_bp.route('/admin/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):

    ticket = Ticket.query.get_or_404(ticket_id)
    
    if current_user.role == 'user' and ticket.user_id != current_user.id:
        flash("You do not have permission to update this ticket.", "danger")
        return redirect(url_for('user.dashboard'))

    form = TicketForm()

    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.category = form.category.data
        ticket.priority = form.priority.data
        ticket.status = form.status.data

        if form.notes.data:
            note = Note(content=form.notes.data, ticket=ticket)
            db.session.add(note)

        db.session.commit()
        flash('Ticket has been updated.', 'success')

        if current_user.role == 'analyst':
            return redirect(url_for('analyst.analyst_all_tickets'))
        else:
            return redirect(url_for('admin.all_tickets'))

    if request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.category.data = ticket.category
        form.priority.data = ticket.priority
        form.status.data = ticket.status

    return render_template('update_ticket_admin.html', form=form, ticket=ticket)


# Admin edit user details route
@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):

    if current_user.role not in ['admin', 'analyst']:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('user.dashboard'))

    user = User.query.get_or_404(user_id)

    if current_user.role == 'analyst' and user.role == 'admin':
        flash("Only administrators can edit administrator accounts.", "danger")
        return redirect(url_for('analyst.analyst_all_users'))

    is_view_only = request.args.get('view') == 'true'

    if request.method == 'POST' and not is_view_only:
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        if new_email:
            user.email = new_email
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash('User details updated successfully.', 'success')
        if current_user.role == 'analyst':
            return redirect(url_for('analyst.analyst_all_users'))
        else:
            return redirect(url_for('admin.all_users'))


    return render_template('edit_user_admin.html', user=user, is_view_only=is_view_only)


# Admin delete user route
@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been successfully deleted.', 'success')
    return redirect(url_for('admin.all_users'))


# Admin create new user route
@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():

    if current_user.role not in ['admin', 'analyst']:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('user.dashboard'))

    form = RegistrationForm()

    if current_user.role == 'admin':
        form.role.choices = [
            ('user', 'Standard User'),
            ('analyst', 'Analyst'),
            ('admin', 'Admin')
        ]
    elif current_user.role == 'analyst':
        form.role.choices = [
            ('user', 'Standard User')
        ]

    if form.validate_on_submit():

        if current_user.role == 'analyst' and form.role.data != 'user':
            flash('You do not have permission to assign this role.', 'danger')
            return redirect(url_for('admin.create_user'))

        new_user = User(
            email=form.email.data,
            role=form.role.data
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('New user has been successfully created!', 'success')

        
        if current_user.role == 'analyst':
            return redirect(url_for('analyst.analyst_all_users'))
        else:
            return redirect(url_for('admin.all_users'))

    return render_template('create_user.html', form=form)
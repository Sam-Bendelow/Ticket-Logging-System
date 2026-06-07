from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from service_desk_app.app import db
from service_desk_app.app.models import Ticket, Note
from service_desk_app.app.forms import TicketForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard_user.html', tickets=tickets)

@user_bp.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    form.status.data = 'Open'

    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created.', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('create_ticket.html', form=form)

@user_bp.route('/user/view_ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.user_id != current_user.id and not current_user.is_admin:
        flash('You cannot view this ticket.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    form = TicketForm(obj=ticket)

    return render_template('view_ticket.html', ticket=ticket, form=form)

@user_bp.route('/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        flash('You do not have access to update this ticket.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    form = TicketForm(obj=ticket)

    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.category = form.category.data
        ticket.priority = form.priority.data

        if current_user.is_admin:
            ticket.status = form.status.data
        
        if form.notes.data:
            note = Note(content=form.notes.data, ticket=ticket)
            db.session.add(note)

        db.session.commit()
        flash('Ticket has been updated.', 'success')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.category.data = ticket.category
        form.priority.data = ticket.priority
        form.status.data = ticket.status

    return render_template('update_ticket.html', form=form, ticket=ticket)

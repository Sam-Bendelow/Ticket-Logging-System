from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from service_desk_app.app.models import Ticket

analyst_bp = Blueprint('analyst', __name__)

# Analyst dashboard route
@analyst_bp.route('/analyst_dashboard')
@login_required
def analyst_dashboard():
    if current_user.role != 'analyst':
        abort(403)

    tickets = Ticket.query.filter_by(assigned_to=current_user.id).all()

    return render_template('dashboard_analyst.html', tickets=tickets)

# Analyst view tickets assigned to me route
@analyst_bp.route('/my_queue')
@login_required
def my_queue():
    if current_user.role != 'analyst':
        abort(403)

    tickets = Ticket.query.filter_by(assigned_to=current_user.id).all()

    return render_template('analyst_queue.html', tickets=tickets)

# Analyst view all tickets route
@analyst_bp.route('/analyst_all_tickets')
@login_required
def analyst_all_tickets():
    if current_user.role != 'analyst':
        abort(403)

    tickets = Ticket.query.all()

    return render_template('analyst_all_tickets.html', tickets=tickets)

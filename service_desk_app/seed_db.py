from service_desk_app.app import app, db
from service_desk_app.app.models import User, Ticket
import random
from datetime import datetime, timedelta

# Reset database with new records
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create users from a list of predefined emails and roles
    users = [
        User(email='Adam@microsoft.com', role='user'),
        User(email='Becky@microsoft.com', role='user'),
        User(email='Charlie@microsoft.com', role='user'),
        User(email='Danny@microsoft.com', role='user'),
        User(email='Elvis@microsoft.com', role='user'),
        User(email='Francesca@microsoft.com', role='user'),
        User(email='George@microsoft.com', role='user'),
        User(email='Hannah@microsoft.com', role='user'),
        User(email='Analyst1@microsoft.com', role='analyst'),
        User(email='Analyst2@microsoft.com', role='analyst'),
        User(email='Analyst3@microsoft.com', role='analyst'),
        User(email='Admin1@microsoft.com', role='admin'),
        User(email='Admin2@microsoft.com', role='admin')
    ]

    # Sets a standardised password for all users
    for user in users:
        user.set_password('Password123!')
        db.session.add(user)

    # Commits users to database
    db.session.commit()

    # Define ticket categories, statuses and priorities
    categories = ['Application/Software', 'Network', 'Hardware', 'Telephony', 'User Account', 'Email', 'File & Print']
    priorities = ['Low', 'Medium', 'High']
    statuses = ['Open', 'In Progress', 'Resolved']

    # Defines sample titles for each ticket category
    category_titles = {
        'Application/Software': [
            'Application crashing on startup',
            'Software access request',
            'Software update failure',
            'Licensing issue'
        ],
        'Hardware': [
            'Laptop will not turn on',
            'Monitor flickering',
            'USB port not working',
            'Keyboard malfunctioning'
        ],
        'Network': [
            'Unable to connect to Wi-Fi',
            'Slow internet speed',
            'Cannot connect to network printer',
            'Unable to connect to VPN'
        ],
        'Email': [
            'Shared mailbox access',
            'Unable to login to email account',
            'Need access to a distribution list',
            'Emails not syncing on mobile device'
        ],
        'User Account': [
            'Admin rights required',
            'Account locked out',
            'Password reset required',
            'Two-factor authentication issue'
        ],
        'Telephony': [
            'Poor call quality',
            'Headset not working',
            'Unable to receive inbound calls',
            'People cannot hear me on outbound calls'
        ],
        'File & Print': [
            'Printer is not working',
            'Missing files on network drive',
            'Cannot access shared drive',
            'Folder permissions need updating'
        ],
    }

    # Generate sample tickets for standard users only
    all_tickets = []
    for user in [u for u in users if u.role == 'user']:
        for _ in range(random.randint(1, 2)):
            days_ago = random.randint(0, 60)
            random_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))

            # Creates a ticket based on random title and category
            category = random.choice(categories)
            title = random.choice(category_titles[category])

            # Creates new ticket instance
            ticket = Ticket(
                title=title,
                description='This is a sample ticket description.',
                category=category,
                priority=random.choice(priorities),
                status=random.choice(statuses),
                created_at=random_date,
                user_id=user.id,
                assigned_to=random.choice([u.id for u in users if u.role == 'analyst'])
            )
            all_tickets.append(ticket)

    # Sort tickets by created_at to ensure ticket IDs follow chronological order
    all_tickets.sort(key=lambda x: x.created_at)

    for ticket in all_tickets:
        db.session.add(ticket)

    # Commits tickets to database and prints number of tickets created
    db.session.commit() 
    print(f" Created {len(all_tickets)} tickets.")
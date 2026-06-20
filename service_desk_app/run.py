from service_desk_app.app import app as application, db
from flask_migrate import Migrate
import os

migrate = Migrate(application, db)

# Tempt: Seed database on startup
with appplication.app_context():
    if os.environ.get("RENDER"): # only run on Render
        from service_desk_app.seed_db import db # Triggers seed script

# Create database tables
from service_desk_app.app.models import User, Ticket, Note

with application.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
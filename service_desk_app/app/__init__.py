from flask import Flask, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_migrate import Migrate

# Initialise Flask app, load config
app = Flask(__name__)
app.config.from_object('service_desk_app.config.Config')

# Enables CSRF Protection
csrf = CSRFProtect(app)

# Initialise login manager and database
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Register blueprints for route organisation
from service_desk_app.app.routes.auth_routes import auth_bp
from service_desk_app.app.routes.user_routes import user_bp
from service_desk_app.app.routes.admin_routes import admin_bp
from service_desk_app.app.routes.auth_routes import analyst_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(analyst_bp)

# Imports models ensuring they are registered with SQLAlchemy
from service_desk_app.app import models
__all__ = ['app', 'db', 'login_manager', 'csrf']

# Inject CSRF token into all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())
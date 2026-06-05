from service_desk_app.app import app as application, db
from flask_migrate import Migrate

migrate = Migrate(application, db)

if __name__ == '__main__':
    application.run(debug=True)
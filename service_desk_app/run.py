from service_desk_app.app import app as application, db
from flask_migrate import Migrate
import os

migrate = Migrate(application, db)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ('erfhviueviueb')
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Get database URL from Render environment
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        database_url = database_url.replace("postgres://", "postgresql+psycopg2://")
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'instance', 'service_desk.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
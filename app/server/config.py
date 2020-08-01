from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(dotenv_path=basedir)

class Config:
    """Set Flask configuration from mail.cfg file."""

    # General Config
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get("SECRET_KEY")
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS=environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL=environ.get('MAIL_USE_SSL')
    SECURITY_PASSWORD_SALT = environ.get("SECURITY_PASSWORD_SALT")
    MAIL_USERNAME=environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=environ.get('MAIL_DEFAULT_SENDER')
    STRIPE_SECRET_KEY=environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY=environ.get('STRIPE_PUBLISHABLE_KEY')

if __name__ == "__main__":
    print("base dir is " + basedir)
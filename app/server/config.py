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
    SENDGRID_API_KEY = environ.get('SENDGRID_API_KEY')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SERVER_NAME = environ.get('SERVER_NAME')
    LOCAL_BASE_URL = environ.get('LOCAL_BASE_URL')


if __name__ == "__main__":
    print("base dir is " + basedir)
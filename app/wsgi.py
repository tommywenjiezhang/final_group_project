from server import create_app
from server.model import db
from flask_script import Manager,  Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    try:
        db.create_all()
    except:
        raise Exception("Data cannot be created")

@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

def create_db(app):
    with app.app_context():
        db.create_all()

@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        email="ad@min.com",
        password="admin",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now())
    )
    db.session.commit()

manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
if __name__ == "__main__":
    manager.run()
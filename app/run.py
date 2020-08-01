from server import create_app
app = create_app()
from server.model import db


def create_db():
    with app.app_context():
        db.init_app(app)
        db.create_all()
if __name__ == "__main__":
    create_db()

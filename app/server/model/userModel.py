from . import db
from marshmallow import Schema, fields
import json

class UserModel(db.Model):
    __tablename__ = 'User'

    id = db.Column("UserID", db.Integer, primary_key=True)
    username = db.Column("username",db.String(80))
    password = db.Column("password",db.String(80))
    name = db.Column("name",db.String(20))
    email = db.Column("email",db.String(80))
    phone = db.Column("phone", db.Integer)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    password_reset_token = db.Column(db.String(255), nullable=True)
    datasets = db.relationship('DatasetModel', backref='User', lazy=True)


    def __init__(self, username, password,name,email,phone,confirmed,
                 admin=False, confirmed_on=None,
                 password_reset_token=None):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.name = name
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.password_reset_token = password_reset_token


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    @classmethod
    def find_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()

    def json(self):
        schema = UserSchema()
        return json.dumps(schema.dump(self))

    def profile(self):
        return {'name':self.name, 'username':self.username,'phone':self.phone, 'email':self.email}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.String()
    phone = fields.Integer()
    name = fields.String()

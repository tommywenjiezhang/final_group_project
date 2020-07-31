from .. import db
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
    datasets = db.relationship('DatasetModel', backref='User', lazy=True)


    def __init__(self, username, password,name,email,phone):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.name = name


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def json(self):
        schema = UserSchema()
        return json.dumps(schema.dump(self))

    def profile(self):
        return {'name':self.name, 'username':self.username,'phone':self.phone, 'email':self.email}

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.String()
    phone = fields.Integer()
    name = fields.String()

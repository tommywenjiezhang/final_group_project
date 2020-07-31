from .. import db
from marshmallow import Schema, fields
import json
from server.redis import RedisClient
from server.util import hashIdandTitle
import struct
class DatasetModel(db.Model):
    __tablename__ = "Dataset"
    id = db.Column('id',db.Integer,primary_key=True)
    title = db.Column("title", db.String(30))
    description = db.Column("description", db.String)
    created_at = db.Column("created_at", db.DateTime)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('User.UserID'))


    def __init__(self,title,description,created_at,user_id):
        self.title = title
        self.description = description
        self.created_at = created_at
        self.user_id = user_id

    @classmethod
    def findById(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def findByTitle(cls, title, user_id):
        return cls.query.filter_by(title=title,user_id=user_id).first()

    def json(self):
        dataObj = {
            "title":self.title,
            "description":self.description,
            "created_at":self.created_at,
            "user_id":self.user_id
            }
        return json.dumps(dataObj)

    def save_to_db(self,values=None):
        db.session.add(self)
        id = None
        if values is not None:
            db.session.flush()
            id = self.id
            title = self.title
            hashValue = hashIdandTitle(title,id)
            client = RedisClient()
            client.saveToRedis(hashValue, *values)
        db.session.commit()
        return id

    def getDataSet(self):
        print(self.title)
        print(self.id)
        hashValue = hashIdandTitle(self.title, self.id)
        client = RedisClient()
        dataset = client.getFullList(hashValue)
        newLst = [float(i.decode('utf-8')) for i in dataset]
        return newLst

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class DatasetSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    user_id = fields.Integer()


def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict
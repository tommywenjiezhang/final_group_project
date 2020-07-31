from flask_restful import Resource, reqparse
from flask import Response
import json

class IndexRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    def get(self):
        client.publish("messsage","hello world")
        if client.get('value'):
            obj = client.get("value")
            return Response(response=obj, status=200)
        return "hello world"
    def post(self):
        data = IndexRoute.parser.parse_args()
        client.set("value",data['name'])
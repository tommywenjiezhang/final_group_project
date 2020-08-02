from flask_restful import Resource, reqparse
from flask import Response, jsonify,render_template, make_response
import json
from flask_jwt_extended import jwt_required , get_jwt_identity

class IndexRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')

    def get(self):
        html = render_template('index.html')
        headers = {'Content-Type': 'text/html'}
        return make_response(html,200,headers)


class SecreteRoute(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user)

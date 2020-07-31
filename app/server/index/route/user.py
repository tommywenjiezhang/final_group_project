from flask_restful import Resource, reqparse
from server.model.userModel import UserModel
from werkzeug.security import generate_password_hash
from flask_jwt import jwt_required
from flask import Response
import json

class UserRegisterRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True,help="This field cannot be blank.")
    parser.add_argument('name')
    parser.add_argument('email')
    parser.add_argument('phone', type=int)

    def post(self):
        data = UserRegisterRoute.parser.parse_args()
        if(UserModel.find_by_username(data['username'])):
            return {"message": "A user with that username already exists"}
        user = UserModel(username=data['username'],
                         password= generate_password_hash(data['password']),
                         name=data['name'],
                         email=data['email'],
                         phone=data['phone']
                         )
        user.save_to_db()
        return {"message": "User created successfully."}

class UserLoginRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True,
                        help="This field cannot be blank.")
    @jwt_required()
    def post(self):
        data = UserLoginRoute.parser.parse_args()
        print(data['user_id'])
        user = UserModel.find_by_id(data['user_id'])
        userProfile = user.profile()
        message = {'msg':'User login successful'}
        mergeobj = {**message, **userProfile}
        return Response(response=json.dumps(mergeobj), status=200, mimetype="application/json")









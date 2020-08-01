from flask_restful import Resource, reqparse
from server.model.userModel import UserModel
from werkzeug.security import generate_password_hash
from flask import Response, session, jsonify
import json
from server.auth import authenicate
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
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
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password', type=str,  required=True,
                        help="This field cannot be blank.")
    def post(self):
        data = UserLoginRoute.parser.parse_args()
        user = authenicate(username=data['username'],password=data['password'])
        if not user:
            return json.dumps({"msg":"username or password is incorrect"}), 401
        userObj = {
            'username': data['username'],
            'user_id' : user.id
        }
        access_token = create_access_token(identity=userObj)
        session['username'] = data['username']
        session['loggedin'] = True
        jsonResponse = jsonify(access_token=access_token)
        return jsonResponse









from flask_restful import Resource, reqparse
from server.model.userModel import UserModel
from werkzeug.security import generate_password_hash
from flask import Response, session, jsonify, flash, render_template, url_for
import json
from server.auth import authenicate
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from datetime import datetime
from server.mail.email_token import confirm_token, generate_confirmation_token
from flask_login import login_user, logout_user, \
    login_required, current_user
from server.mail import send_email

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
                         phone=data['phone'],
                         confirmed=False
                         )
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('index_bp.userconfirmemailroute', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        login_user(user)
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
        login_user(user)
        jsonResponse = jsonify(access_token=access_token)
        return jsonResponse

class UserConfirmEmailRoute(Resource):
    @login_required
    def get(self,token):
        if current_user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        email = confirm_token(token)
        user = UserModel.find_by_email(email=current_user.email).first_or_404()
        if user.email == email:
            user.confirmed = True
            user.confirmed_on = datetime.now()
            user.save_to_db()
            return jsonify({'success':  'You have confirmed your account. Thanks!'})
        else:
            return jsonify({'error': 'The confirmation link is invalid or has expired.'})

class ResendConfirmationRoute(Resource):
    @login_required
    def get(self):
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('indexApi.UserConfirmEmailRoute', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(current_user.email, subject, html)
        flash('A new confirmation email has been sent.', 'success')

















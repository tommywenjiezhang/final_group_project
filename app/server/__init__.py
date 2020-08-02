from flask import Flask
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_login import LoginManager
from server.model.userModel import UserModel as User
from server.model import db

login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('server.config.Config')
    app.secret_key = "zhang"
    if test_config == None:
        app.config.from_object('server.config.Config')
    else:
        app.config.update(test_config)

    with app.app_context():
        login_manager.init_app(app)
        db.init_app(app)
        from .index import index_bp
        app.register_blueprint(index_bp)
        from .calculator import calculator_bp
        app.register_blueprint(calculator_bp, url_prefix="/calculator")
        from .auth import authenicate, identity
        app.config['JWT_SECRET_KEY'] = 'super-secret'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=18000)
        jwt = JWTManager(app)

        @login_manager.user_loader
        def load_user(user_id):
            print("load_user function callback +++++++++++++++++++++++++")
            print(user_id)
            return User.query.filter(User.username == user_id).first()


        @jwt.invalid_token_loader
        def invalid_token_callback(invalid_token):
            return jsonify({
                'status': 401,
                'msg': 'The request does not provide a token'
            })

        @jwt.expired_token_loader
        def expired_token_loader():
            return  jsonify({
                'status': 401,
                'msg': 'token has expired please login again'
            })

    return app


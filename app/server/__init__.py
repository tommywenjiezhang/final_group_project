from flask import Flask
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from datetime import timedelta
from flask import Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('server.config.Config')
    app.secret_key = "zhang"
    if test_config == None:
        app.config.from_object('server.config.Config')
    else:
        app.config.update(test_config)
    db.init_app(app)
    with app.app_context():
        from .index import index_bp
        app.register_blueprint(index_bp, url_prefix="/")
        from .calculator import calculator_bp
        app.register_blueprint(calculator_bp, url_prefix="/calculator")
        from .auth import authenicate, identity
        app.config['JWT_SECRET_KEY'] = 'super-secret'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=18000)
        jwt = JWTManager(app)


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


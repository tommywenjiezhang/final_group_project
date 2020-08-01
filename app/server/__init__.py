from flask import Flask, render_template
import os
from flask.json import jsonify
from datetime import timedelta
from flask_mail import Mail
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_login import LoginManager
from server.model.userModel import UserModel as User



mail = Mail()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = "zhang"
    if test_config == None:
        app.config.from_object('server.config.Config')
    else:
        app.config.update(test_config)
    with app.app_context():
        mail.init_app(app)
        login_manager.init_app(app)
        from server.model import db
        db.init_app(app)
        from .index import index_bp
        app.register_blueprint(index_bp, url_prefix="/")
        from .calculator import calculator_bp
        app.register_blueprint(calculator_bp, url_prefix="/calculator")
        from .auth import authenicate, identity
        app.config['JWT_SECRET_KEY'] = 'super-secret'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=18000)
        jwt = JWTManager(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.find_by_id(id=user_id)

        @app.errorhandler(404)
        def page_not_found(error):
            return render_template("errors/404.html"), 404

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


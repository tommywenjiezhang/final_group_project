from flask import Blueprint, Response, render_template
from flask_restful import Api, Resource
from .route import UserRegisterRoute, UserLoginRoute



auth_bp = Blueprint('auth_bp',__name__)
authApi = Api(auth_bp)


authApi.add_resource(UserRegisterRoute,'/register')
authApi.add_resource(UserLoginRoute, '/login')
authApi.add_resource(SecreteRoute, '/secret')

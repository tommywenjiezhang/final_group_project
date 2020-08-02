from flask import Blueprint, Response, render_template
from flask_restful import Api, Resource
from .route.home import IndexRoute, SecreteRoute
from .route.user import UserRegisterRoute, UserLoginRoute,\
    UserConfirmEmailRoute,UnConfirmed, \
    resend_confirmation, Profile, Logout, Forgetpassword,ResetPassword




index_bp = Blueprint('index_bp',__name__, template_folder='templates', static_folder='static')
indexApi = Api(index_bp)


indexApi.add_resource(IndexRoute,"/")
indexApi.add_resource(UserRegisterRoute,'/register')
indexApi.add_resource(UserLoginRoute, '/login')
indexApi.add_resource(SecreteRoute, '/secret')
indexApi.add_resource(UserConfirmEmailRoute, "/confirm/<string:token>")
indexApi.add_resource(UnConfirmed, '/unconfirmed')
indexApi.add_resource(resend_confirmation, '/resend')
indexApi.add_resource(Profile, '/profile')
indexApi.add_resource(Logout, '/logout')
indexApi.add_resource(Forgetpassword, '/forget')
indexApi.add_resource(ResetPassword,'/reset','/reset/<string:token>')


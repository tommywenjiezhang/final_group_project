from flask import Blueprint, Response, render_template
from flask_restful import Api, Resource
from .route.home import IndexRoute, SecreteRoute
from .route.user import UserRegisterRoute, UserLoginRoute



index_bp = Blueprint('index_bp',__name__, template_folder='templates')
indexApi = Api(index_bp)
@index_bp.route("/")
def index():
    return render_template("index.html")




indexApi.add_resource(UserRegisterRoute,'/register')
indexApi.add_resource(UserLoginRoute, '/login')
indexApi.add_resource(SecreteRoute, '/secret')



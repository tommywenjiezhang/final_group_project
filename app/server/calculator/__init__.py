from flask import Blueprint, Response
from flask_restful import Api, Resource
from .route import IndexRoute, CalculationRoute, NewRoute



calculator_bp = Blueprint('calculator_bp',__name__,template_folder='templates')
calculatorApi = Api(calculator_bp)
calculatorApi.add_resource(IndexRoute, '/')
calculatorApi.add_resource(CalculationRoute, '/<int:id>')
calculatorApi.add_resource(NewRoute, '/new')
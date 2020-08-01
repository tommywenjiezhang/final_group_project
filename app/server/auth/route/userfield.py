from flask_restful import fields
user_register_fields = {
    'username': fields.String,
    'password': fields.String,
    'name': fields.String,
    'email':fields.String,
    'phone': fields.Integer
}

user_login_fields = {
    'username': fields.String,
    'password': fields.String
}


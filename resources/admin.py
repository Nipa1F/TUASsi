from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus


from models.admin import Admin
from utils import hash_password

class AdminListResource(Resource):
    def post(self):

        json_data =request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')



        if Admin.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if Admin.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        admin = Admin(
            username=username,
            email=email,
            password=password


        )

        admin.save()

        data = {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'password': admin.password

        }

        return data, HTTPStatus.OK

class AdminResource(Resource):

    @jwt_optional
    def get(self, username):

        admin = Admin.get_by_username(username=username)

        if admin is None:
            return {'message': 'admin not found'}, HTTPStatus.NOT_FOUND

        current_admin = get_jwt_identity()

        if current_admin == admin.id:
            data = {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email,
                'password': admin.password
            }

        else:
            data = {
                'id': admin.id,
                'username': admin.username,
            }

        return data, HTTPStatus.OK
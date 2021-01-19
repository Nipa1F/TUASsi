from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus


from models.client import Client
from utils import hash_password

class ClientListResource(Resource):
    def post(self):

        json_data =request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')



        if Client.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if Client.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        client = Client(
            username=username,
            email=email,
            password=password


        )

        client.save()

        data = {
            'id': client.id,
            'username': client.username,
            'email': client.email,
            'password': client.password

        }

        return data, HTTPStatus.OK

class ClientResource(Resource):

    @jwt_optional
    def get(self, username):

        client = Client.get_by_username(username=username)

        if client is None:
            return {'message': 'client not found'}, HTTPStatus.NOT_FOUND

        current_client = get_jwt_identity()

        if current_client == client.id:
            data = {
                'id': client.id,
                'username': client.username,
                'email': client.email,
                'password': client.password
            }

        else:
            data = {
                'id': client.id,
                'username': client.username,
            }

        return data, HTTPStatus.OK

    @jwt_required
    def put(self, username):

        json_data = request.get_json()

        client = Client.get_by_username(username=username)

        if client is None:
            return {'message': 'Client not found'}, HTTPStatus.NOT_FOUND

        username = json_data['username']
        email = json_data['email']
        password = json_data['password']



        client = Client(
            username=username,
            email=email,
            password=password

        )

        client.save()






        return json_data, HTTPStatus.OK

    def delete(self, username):

        client = Client.get_by_username(username=username)

        if client is None:
            return {'message': 'Client not found'}, HTTPStatus.NOT_FOUND


        client.delete()

        return {'message': 'deleted'}, HTTPStatus.OK
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from utils import check_password
from models.client import Client
from models.admin import Admin

black_list = set()

class TokenUserResource(Resource):
    def post(self):

        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        client = Client.get_by_email(email=email)

        if not client or not check_password(password, client.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=client.id, fresh=True)
        refresh_token = create_refresh_token(identity=client.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

class TokenAdminResource(Resource):
    def post(self):

        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        admin = Admin.get_by_email(email=email)

        if not admin or not check_password(password, admin.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=admin.id, fresh=True)
        refresh_token = create_refresh_token(identity=admin.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

class RefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_client = get_jwt_identity()

        token = create_access_token(identity=current_client, fresh=False)

        return {'token': token}, HTTPStatus.OK

class RevokeResource(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']

        black_list.add(jti)

        return {'message': 'Successfully logged out'}, HTTPStatus.OK
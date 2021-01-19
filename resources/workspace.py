from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus

from models.workspace import Workspace
from models.client import Client
from models.admin import Admin


class WorkspaceListResource(Resource):

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_client = Client.id


        if current_client == Client.id:
            Roomname = json_data.get('Roomname')
            restime = json_data.get('restime')

            workspace = Workspace(

                Roomname=Roomname,
                restime=restime,

            )

            workspace.save()

            data = {

               'id': workspace.id,
                'Roomname': workspace.Roomname,
                'restime': workspace.restime,

            }

            return data, HTTPStatus.OK

        else:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN



class WorkspaceResource(Resource):

    #@jwt_optional
    def get(self):

        workspace = get_jwt_identity()

        data = {

            'id': workspace.id,
            'Roomname': workspace.Roomname,
            'restime': workspace.restime,

        }

        return data, HTTPStatus.OK
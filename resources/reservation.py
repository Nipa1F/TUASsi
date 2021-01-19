from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus

from models.reservation import Reservation


class ReservationListResource(Resource):

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_client = get_jwt_identity()

        client_id = json_data.get('client_id')
        workspace_id = json_data.get('workspace_id')

        if Reservation.get_by_workspace(workspace_id):
            return {'message': 'time already used'}, HTTPStatus.BAD_REQUEST

       # if Reservation.get_by_id(workspace_id):
        #    return {'message': 'invalid time'}, HTTPStatus.BAD_REQUEST


        reservation = Reservation(

            client_id=client_id,
            workspace_id = workspace_id,


        )

        reservation.save()

        data = {

            'id': reservation.id,
            'client_id': reservation.client_id,
            'workspace_id': reservation.workspace_id,


        }

        return data, HTTPStatus.OK


class ReservationResource(Resource):

    @jwt_required
    def get(self, client_id):

        reservation = Reservation.get_by_client(client_id=client_id)

        if reservation is None:
            return {'message': 'reservations not found'}, HTTPStatus.NOT_FOUND

        current_client = get_jwt_identity()

        if reservation.client_id != current_client:
            return {'message': 'wrong client'}, HTTPStatus.FORBIDDEN



        else:
            data = {

                'id': reservation.id,
                'client_id': reservation.client_id,
                'workspace_id': reservation.workspace_id,


            }

            return data, HTTPStatus.OK



    #@jwt_required
    def put(self, reservation_id):

        json_data = request.get_json()

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_client = get_jwt_identity()

        if current_client != Reservation.client_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.client_id = json_data['client_id']
        reservation.workspace_id = json_data['workspace_id']

        reservation.save()
        reservation.save()

        return reservation.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, reservation_id):

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_client = get_jwt_identity()

        if current_client != reservation.client_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.delete()

        return {'message': 'deleted'}, HTTPStatus.OK
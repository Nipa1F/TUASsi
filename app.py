from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt

from resources.client import ClientListResource, ClientResource
from resources.reservation import ReservationListResource, ReservationResource
from resources.workspace import WorkspaceListResource, WorkspaceResource
from resources.admin import AdminListResource
from resources.token import TokenUserResource, RefreshResource, RevokeResource, black_list
from resources.token import TokenAdminResource
def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.app_context().push
    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list

def register_resources(app):
    api = Api(app)

    api.add_resource(ClientListResource, '/clients')
    api.add_resource(ClientResource, '/clients/<string:username>')

    api.add_resource(ReservationListResource, '/res')
    api.add_resource(ReservationResource, '/res/<int:reservation_id>')


    api.add_resource(WorkspaceListResource, '/workspace')
    api.add_resource(WorkspaceResource, '/getworkspaces')


    api.add_resource(AdminListResource, '/admin')

    api.add_resource(TokenUserResource, '/token')
    api.add_resource(TokenAdminResource, '/admintoken')




if __name__ == '__main__':
    app = create_app()
    app.run()

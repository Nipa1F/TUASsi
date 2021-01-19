from extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer(), db.ForeignKey("client.id"))
    workspace_id = db.Column(db.Integer(), db.ForeignKey("workspace.id"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_all_by_client(cls, client_id):
        return cls.query.filter_by(client_id=client_id).all()

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.filter_by(id=reservation_id).first()

    @classmethod
    def get_by_client(cls, client_id):
        return cls.query.filter_by(client_id=client_id).first()

    @classmethod
    def get_by_workspace(cls, workspace_id):
        return cls.query.filter_by(workspace_id=workspace_id).first()



    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


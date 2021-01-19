from extensions import db


class Workspace(db.Model):
    __tablename__ = 'workspace'

    id = db.Column(db.Integer, primary_key=True)
    Roomname = db.Column(db.String(100), nullable=False)
    restime = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_stats(cls, id, Roomname):
        return cls.query.filter_by(id=id, Roomname=Roomname).first()



    def save(self):
        db.session.add(self)
        db.session.commit()

from flask import current_app
from . import db
from sqlalchemy.exc import SQLAlchemyError
from models.user import UsersModel
import time



class KeshiModel(db.Model):
    __tablename__ = 'keshi'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    type = db.Column(db.Boolean) # 0-res, 1-man

    # TODO 科室被删了，user的科室信息修改

    def __init__(self, name, manager, type):
        self.name = name
        self.manager = manager
        self.type = type

    def __str__(self):
        return "Keshi(name='%s')" % self.name

    # def paginate(self, page, per_page):
    #     return self.query.paginate(page=page, per_page=per_page, error_out=False)

    # def filter_by_username(self, username):
    #     return self.query.filter(self.username.like("%" + username + "%") ).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, research):
        db.session.add(research)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        # self.query.filter(self.id.in_(ids)).delete(synchronize_session=False)
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.info(e)
        return reason
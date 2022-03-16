from flask import current_app
from . import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import time



class ResearchModel(db.Model):
    __tablename__ = 'research'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(250), nullable=False, unique=True,) # 所级项目编号
    name = db.Column(db.String(250), nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('users.id'))
    isBig = db.Column(db.Boolean, nullable=False)
    state = db.Column(db.String(250), nullable=False)

    def __init__(self, number, name, manager, isBig, state):
        self.number = number
        self.name = name
        self.manager = manager
        self.isBig = isBig
        self.state = state

    def __str__(self):
        return "Users(id='%s')" % self.id

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

    def delete(self, ids):
        # self.query.filter_by(id=id).delete()
        self.query.filter(self.id.in_(ids)).delete(synchronize_session=False)
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.info(e)
        return reason
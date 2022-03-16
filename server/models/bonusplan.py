from flask import current_app
from . import db
from sqlalchemy.exc import SQLAlchemyError



class BonusPlanModel(db.Model):
    __tablename__ = 'bonus_plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.String(250), nullable=False)
    quarter = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    description_man = db.Column(db.String(250))
    description_res = db.Column(db.String(250))

    def __init__(self, name, year, quarter, state):
        self.name = name
        self.year = year
        self.quarter = quarter
        self.state = state

    def __str__(self):
        return "Bonus Plan (name='%s')" % self.name

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
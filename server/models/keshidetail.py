from flask import current_app
from . import db
from sqlalchemy.exc import SQLAlchemyError



class KeshiDetailModel(db.Model):
    __tablename__ = 'keshi_detail'
    id = db.Column(db.Integer, primary_key=True)
    planId = db.Column(db.Integer, db.ForeignKey('bonus_plan.id'))
    projectId = db.Column(db.Integer, nullable=False)
    projectType = db.Column(db.Integer, nullable=False) # 0-res, 1-man
    keshiId = db.Column(db.Integer, db.ForeignKey('keshi.id'))
    amount = db.Column(db.DECIMAL(10,2), nullable=False)
    amount_zhan = db.Column(db.DECIMAL(10,2), default=0.0)
    amount_buzhan = db.Column(db.DECIMAL(10,2), default=0.0)

    def __init__(self, planId, projectId, projectType, keshiId, amount):
        self.planId = planId
        self.projectId = projectId
        self.projectType = projectType
        self.amount = amount
        self.keshiId = keshiId

    def __str__(self):
        return "Bonus Detail (id='%s')" % self.id

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
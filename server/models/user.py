from flask import current_app
from . import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from models.research import ResearchModel

class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(250), nullable=False) #null
    keshi = db.Column(db.Integer, nullable=False) #null
    username  = db.Column(db.String(250), nullable=False) #null
    worknum  = db.Column(db.String(250),  unique=True, nullable=False) #null
    idnum  = db.Column(db.String(250),  unique=True, nullable=False) #null
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    wage_category = db.Column(db.String(250), nullable=False) #null
    job = db.Column(db.String(250))
    position = db.Column(db.String(250))
    remarks = db.Column(db.String(250))
    bonus_category = db.Column(db.String(250), nullable=False) #null

    password  = db.Column(db.String(250), nullable=False)
    session   = db.Column(db.String(250))

    my_research  = db.relationship(ResearchModel,backref='user')
    
    def __init__(self):
        pass
    
    def __init__(self, username ,  password):
        self.username = username
        self.password = password

    def __str__(self):
        return "Users(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_username(self, username):
        return self.query.filter(self.username.like("%" + username + "%") ).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, user):
        db.session.add(user)
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
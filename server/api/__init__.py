from flask import Blueprint
from functools import wraps
from flask import g, abort, jsonify, request, session
from models.user import UsersModel
from utils.response_code import RET

user_blue = Blueprint("user", __name__)
planning_blue = Blueprint("planning", __name__)
general_blue = Blueprint("general", __name__)
detail_blue = Blueprint("detail", __name__)
project_blue = Blueprint("project", __name__)
group_blue = Blueprint("group", __name__)

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        userId = session.get('userid')
        id = session.get('id')
        userInfo = UsersModel.query.get(userId)
        if(id!=userInfo.session): 
            return jsonify(code=RET.SESSIONERR, flag=True , message='登录失效' )
        return f(*args, **kws)

    return decorated_function


from server.api import user
from server.api import planning
from server.api import general
from server.api import detail
from server.api import project
from server.api import group
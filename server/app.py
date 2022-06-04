# -*- coding: utf-8
from flask import Flask, request, session
from flask_session import Session
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
from config_old import APP_ENV, config
from models import db
from flask.json import JSONEncoder
import decimal

app = Flask(__name__)
# CORS(app, supports_credentials=True)
app.config.from_object(config[APP_ENV])

app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

# json解析Decimal的问题
class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(float(obj))
        return JSONEncoder.default(self, obj)

app.json_encoder = JsonEncoder

#注册 api 蓝图
from server.api import user_blue, planning_blue, detail_blue, general_blue, project_blue, group_blue
app.register_blueprint(user_blue)
app.register_blueprint(planning_blue, url_prefix='/planning')
app.register_blueprint(general_blue, url_prefix='/general')
app.register_blueprint(detail_blue, url_prefix='/detail')
app.register_blueprint(project_blue, url_prefix='/project')
app.register_blueprint(group_blue, url_prefix='/group')


#跨域
CORS(app, resources=r'/*')


if __name__ == "__main__":
    db.init_app(app)
    db.app = app

    # print(app.url_map)
    # db.drop_all() 
    db.create_all()

    from waitress import serve
    from paste.translogger import TransLogger
    serve(TransLogger(app),port=5000)


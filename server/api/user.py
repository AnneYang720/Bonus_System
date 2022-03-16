from flask import g, abort, jsonify, request, session

from utils.response_code import RET

from . import user_blue
from . import authorize
from models.user import UsersModel
from models.role import RolesModel
from models.keshi import KeshiModel
from models.category import CategoryModel
from models.research import ResearchModel
import uuid

from functools import wraps
import csv


# 用户注册接口
@user_blue.route('/signup', methods=['POST'])
def signup():
    username =request.json.get('username')
    password =request.json.get('password')

    user = UsersModel(username=username, password=UsersModel.set_password(UsersModel, password))
    result = UsersModel.add(UsersModel, user)
    if user.id:
        return jsonify(code=RET.OK, flag=True, message='注册成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='用户注册失败(用户名或邮箱已存在)')

# 用户登录
@user_blue.route('/login', methods=['POST'])
def login():
    worknum =request.json.get('worknum')
    password =request.json.get('password')

    userInfo = UsersModel.query.filter_by(worknum=worknum).first()
    if (userInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='找不到用户')
    else:
        if (UsersModel.check_password(UsersModel, userInfo.password, password)):
            random_id = uuid.uuid4().hex

            session['userid'] = userInfo.id
            session['worknum'] = worknum
            session['id'] = random_id
            userInfo.session = random_id
            userInfo.update()
            return jsonify(code=RET.OK, flag=True, message='登录成功')
        else:
            return jsonify(code=RET.PARAMERR, flag=False, message='密码错误')

@user_blue.route('/changepwd', methods=['POST'])
@authorize
def changePwd():
    userId = session.get('userid')
    newPwd =request.json.get('password')

    userInfo = UsersModel.query.get(userId)
    if (userInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='找不到用户')
    
    userInfo.password = userInfo.set_password(newPwd)
    userInfo.update()
    return jsonify(code=RET.OK, flag=True, message='修改密码成功')


# 获取用户信息
@user_blue.route('/userinfo', methods=['GET'])
def getInfo():
    userId = session.get('userid')

    userInfo = UsersModel.query.get(userId)
    roles = RolesModel.query.filter_by(userId=userId).all()

    roleslist = []
    for role in roles: roleslist.append(role.role)

    return jsonify(code=RET.OK, flag=True, message='获取用户信息成功', data={"id":userInfo.id,"username":userInfo.username,"roles":roleslist})


@user_blue.route('/addfile', methods=['POST'])
def AddUsers():
    import os
    # print(os.getcwd())
    f = csv.reader(open('../new4.csv','r',encoding='utf-8'))
    for i in f:
        idnum =  i[4]
        username   =  i[2]
        department = i[0]
        keshi = i[1]
        category = i[5]
        wage_category = i[6]
        job = i[7]
        position = i[8]
        remarks = i[9]
        worknum  = i[3]
        bonus_category = i[10]

        userInfo = UsersModel.query.filter_by(worknum=worknum).first()
        if (userInfo):
            return jsonify(code=RET.NODATA, flag=False, message='工号已存在')
    
        # 设置密码初始为工号
        password = worknum
        user = UsersModel(username=username,password=UsersModel.set_password(UsersModel, password))
        user.department = department
        user.idnum = idnum
        user.wage_category = wage_category
        user.job = job
        user.position = position
        user.remarks = remarks
        user.bonus_category = bonus_category
        user.worknum = worknum
        user.keshi = KeshiModel.query.filter_by(name=keshi).first().id
        user.category = CategoryModel.query.filter_by(name=category).first().id
        # 添加用户
        result = UsersModel.add(UsersModel, user)

        # 添加角色
        role = RolesModel(userId=user.id,role="user")
        result = RolesModel.add(RolesModel, role)

        if (user.id is None):
            return jsonify(code=RET.DBERR, flag=False, message='添加用户失败')
    return jsonify(code=RET.OK, flag=True, message='添加用户成功')


@user_blue.route('/addprojects', methods=['POST'])
def AddProjects():
    import os
    # print(os.getcwd())
    f = csv.reader(open('../newpro2.csv','r',encoding='utf-8'))
    for i in f:
        number = i[0]
        name = i[1]
        manager_name = i[2]

        userInfo = UsersModel.query.filter_by(username=manager_name).first()
        if (userInfo is None):
            return jsonify(code=RET.NODATA, flag=False, message=name)
        

        # 添加
        research = ResearchModel(number=number,name=name, manager=userInfo.id, isBig=False, state="进行中")
        result = ResearchModel.add(ResearchModel, research)

        # 添加角色
        roleInfo = RolesModel.query.filter_by(userId=userInfo.id,role="manager_prok").first()
        if(roleInfo is None):
            role = RolesModel(userId=userInfo.id,role="manager_prok")
            result = RolesModel.add(RolesModel, role)

        if (research.id is None):
            return jsonify(code=RET.DBERR, flag=False, message='添加用户失败')
    return jsonify(code=RET.OK, flag=True, message='添加用户成功')




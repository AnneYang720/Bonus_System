from flask import g, current_app, jsonify, request, session
from server.utils.response_code import RET

from . import planning_blue
from server.models import db
from . import authorize
from models.user import UsersModel
from models.research import ResearchModel
from models.keshi import KeshiModel
from models.role import RolesModel
from sqlalchemy import func

# 获取所有项目的信息
@planning_blue.route('/getprojectlist/<int:page>/<int:size>', methods=['GET'])
@authorize
def getProjectList(page,size): 
    total = db.session.query(db.func.count(ResearchModel.id)).scalar()

    projectInfo = ResearchModel.query.paginate(page,per_page=size)

    projectList = []
    for pro in projectInfo.items:
        manager        =  UsersModel.query.get(pro.manager)
        managerName    =  manager.username
        managerkeshi   =  manager.keshi
        managerworknum =  manager.worknum
        managerkeshi   =  KeshiModel.query.get(managerkeshi).name
        projectList.append({            "id"   : pro.id,
                                     "number"  : pro.number,
                                       "name"  : pro.name,
                                 "managername" : managerName ,
                                 "manager" : manager.worknum,
                            "managerworknum"   : managerworknum,
                             "managerkeshi"    : managerkeshi ,"isBig":pro.isBig,"state":pro.state})
    
    return jsonify(code=RET.OK, flag=True, message='获取科研项目成功', data=projectList, total=total)

# 获取所有进行中科研项目的信息
@planning_blue.route('/getcurprojectlist', methods=['GET'])
@authorize
def getCurProjectList(): 
    projectInfo = ResearchModel.query.filter_by(state='进行中').all()
    
    projectList = []
    for pro in projectInfo:
        projectList.append({"id":pro.id,"name":pro.name})
    
    return jsonify(code=RET.OK, flag=True, message='获取科研项目成功', data=projectList)


# 新增科研项目
@planning_blue.route('/create', methods=['POST'])
@authorize
def createResearchProject(): 
    number = request.json.get('number')
    name = request.json.get('name')
    manager = request.json.get('manager')
    isBig = request.json.get('isBig')
    state = request.json.get('state')

    userInfo = UsersModel.query.filter_by(worknum=manager).first()
    if (userInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该项目经理不存在')

    research = ResearchModel(number=number,name=name, manager=userInfo.id, isBig=isBig, state=state)
    result = ResearchModel.add(ResearchModel, research)

    # 添加角色
    roleInfo = RolesModel.query.filter_by(userId=userInfo.id,role="manager_prok").first()
    if(roleInfo is None):
        role = RolesModel(userId=userInfo.id,role="manager_prok")
        result = RolesModel.add(RolesModel, role)

    if research.id:
        return jsonify(code=RET.OK, flag=True, message='新增科研项目成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增科研项目失败')

# 修改科研项目
@planning_blue.route('/change', methods=['POST'])
@authorize
def changeResearchProject(): 
    id = request.json.get('id')
    name = request.json.get('name')
    manager = request.json.get('manager')
    isBig = request.json.get('isBig')
    state = request.json.get('state')
    number = request.json.get('number')
    researchInfo = ResearchModel.query.get(id)
    if(researchInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该科研项目不存在')

    newUser = UsersModel.query.filter_by(worknum=manager).first()
    if (newUser is None):
        return jsonify(code=RET.NODATA, flag=False, message='该项目经理不存在')
    
    oriUserId = researchInfo.manager

    researchInfo.name = name
    researchInfo.manager = newUser.id
    researchInfo.isBig = isBig
    researchInfo.state = state
    researchInfo.number = number
    researchInfo.update()

    if(oriUserId!=newUser.id):
        # 添加角色
        roleInfo = RolesModel.query.filter_by(userId=newUser.id,role="manager_prok").first()
        if(roleInfo is None):
            role = RolesModel(userId=newUser.id,role="manager_prok")
            result = RolesModel.add(RolesModel, role)

        # 修改角色
        oriPro = ResearchModel.query.filter_by(manager=oriUserId).first()
        if(oriPro is None):
            roleInfo = RolesModel.query.filter_by(userId=oriUserId,role="manager_prok").first()
            roleInfo.delete(roleInfo.id)
    

    return jsonify(code=RET.OK, flag=True, message='修改科研项目信息成功')

# 查找科研项目
@planning_blue.route('/search/<int:page>/<int:size>', methods=['GET'])
@authorize
def searchProject(page,size):
    keyword = request.args.get('q')
    total = db.session.query(db.func.count(ResearchModel.id)).filter(ResearchModel.name.like("%"+keyword+"%")).scalar()

    projectInfo = ResearchModel.query.filter(ResearchModel.name.like("%"+keyword+"%")).paginate(page,per_page=size)

    projectList = []
    for pro in projectInfo.items:
        manager        =  UsersModel.query.get(pro.manager)
        managerName    =  manager.username
        managerkeshi   =  manager.keshi
        managerworknum =  manager.worknum
        managerkeshi   =  KeshiModel.query.get(managerkeshi).name
        projectList.append({            "id"   : pro.id,
                                     "number"  : pro.number,
                                       "name"  : pro.name,
                                 "managername" : managerName ,
                                 "manager" : manager.worknum,
                            "managerworknum"   : managerworknum,
                             "managerkeshi"    : managerkeshi ,"isBig":pro.isBig,"state":pro.state})
    
    return jsonify(code=RET.OK, flag=True, message='搜索科研项目成功', data=projectList, total=total)



@planning_blue.route('/importprojects', methods=['POST'])
def importProjects():
    rows = request.json.get('rows')

    for row in rows:
        research_b = ResearchModel.query.filter_by(number=row['所级项目编号']).first()
        if(research_b):
            return jsonify(code=RET.DBERR, flag=False, message='项目'+row['项目名称']+'的所级编号已存在')

        user = UsersModel.query.filter_by(idnum=row['项目经理身份证号']).first()
        isBig = True if row['是否为大项目']=='是' else False
        research = ResearchModel(number=row['所级项目编号'],name=row['项目名称'], manager=user.id, isBig=isBig, state=row['状态'])
        result = ResearchModel.add(ResearchModel, research)

        if (research.id is None):
            return jsonify(code=RET.DBERR, flag=False, message='添加项目'+row['项目名称']+'失败')

        # 添加角色
        roleInfo = RolesModel.query.filter_by(userId=user.id,role="manager_prok").first()
        if(roleInfo is None):
            role = RolesModel(userId=user.id,role="manager_prok")
            result = RolesModel.add(RolesModel, role)
        
    
    return jsonify(code=RET.OK, flag=True, message='导入项目成功')
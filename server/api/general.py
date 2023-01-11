from flask import g, current_app, jsonify, request, session
from server.models import category

from utils.response_code import RET


# TODO 总览可以选所有计划，现在只能选进行中的计划

from . import general_blue
from server.models import db
from . import authorize
from models.user import UsersModel
from models.role import RolesModel
from models.keshi import KeshiModel
from models.category import CategoryModel
from models.manage import ManageModel
from models.research import ResearchModel
from models.bonusplan import BonusPlanModel

from models.bonusdetail import BonusDetailModel
from models.userdetail import UserDetailModel
from models.detail_history import DetailHistoryModel
from models.koufa import KoufaModel
import uuid

def makeUserList(userInfo):
    userList = []

    allKeshi = KeshiModel.query.all()
    keshiInfo = {}
    for keshi in allKeshi:
        keshiInfo[keshi.id] = keshi.name

    allCategory = CategoryModel.query.all()
    categoryInfo = {}
    for category in allCategory:
        categoryInfo[category.id] = category.name

    for user in userInfo:
        roles = RolesModel.query.filter_by(userId=user.id).all()
        roleslist = []
        for role in roles: roleslist.append(role.role)
        userList.append({
                            "id"             :  user.id ,
                            "username"       :  user.username ,
                            "department"     :  user.department ,
                            "worknum"        :  user.worknum ,
                            "idnum"          :  user.idnum,
                            "category"       :  categoryInfo[user.category],
                            "wage_category"  :  user.wage_category,
                            "role"           :  roleslist,
                            "keshiname"      :  keshiInfo[user.keshi],
                            "keshi"          :  user.keshi,
                            "job"            :  user.job,
                            "position"       :  user.position,
                            "remarks"        :  user.remarks,
                            "bonus_category" :  user.bonus_category
                        })
    return userList
   

# 获取所有user的信息
@general_blue.route('/getuserslist/<int:page>/<int:size>', methods=['GET'])
@authorize
def getUsersList(page,size): 
    total = db.session.query(db.func.count(UsersModel.id)).scalar()

    userInfo = UsersModel.query.paginate(page,per_page=size)
    userList = makeUserList(userInfo.items)
    db.session.commit()
    return jsonify(code=RET.OK, flag=True , message='获取user信息成功', data=userList, total=total)

# 查找用户
@general_blue.route('/search/<int:page>/<int:size>', methods=['GET'])
@authorize
def searchProject(page,size):
    keyword = request.args.get('q')
    total = db.session.query(db.func.count(UsersModel.id)).filter(UsersModel.username.like("%"+keyword+"%")).scalar()

    userInfo = UsersModel.query.filter(UsersModel.username.like("%"+keyword+"%")).paginate(page,per_page=size)
    userList = makeUserList(userInfo.items)
    db.session.commit()    
    return jsonify(code=RET.OK, flag=True, message='搜索用户成功', data=userList, total=total)


# 获取某个科室所有user的信息
@general_blue.route('/getkeshilistbykeshi', methods=['GET'])
@authorize
def getUserListByKeshi():
    _keshi = request.json.get('keshi')
    userInfo = UsersModel.query.filter_by( keshi = _keshi ).all()
    userList = makeUserList( userInfo )
    return jsonify(code=RET.OK, flag=True , message='获取user信息成功', data = userList )
    
# 获取所有科室的信息
@general_blue.route('/getkeshilist', methods=['GET'])
@authorize
def getKeshiList(): 
    keshiInfo = KeshiModel.query.all()
    keshiList = []
    for keshi in keshiInfo:
        keshiList.append({"id":keshi.id,"name":keshi.name})
    return jsonify(code=RET.OK, flag=True , message='获取科室信息成功', data = keshiList)

# 获取所有科室的详细信息
@general_blue.route('/getkeshifulllist', methods=['GET'])
@authorize
def getKeshiFullList(): 
    keshiInfo = KeshiModel.query.all()
    keshiList = []
    for keshi in keshiInfo:
        userInfo = UsersModel.query.get(keshi.manager)
        keshiList.append({"id":keshi.id,"name":keshi.name,"manager_worknum":userInfo.worknum,"manager_name":userInfo.username,"type":keshi.type})
    return jsonify(code=RET.OK, flag=True , message='获取科室信息成功', data = keshiList)


# 获取所有类别的信息
@general_blue.route('/getcategorylist', methods=['GET'])
# @authorize
def getCategoryList(): 
    categoryInfo = CategoryModel.query.all()
    categoryList = []
    for category in categoryInfo:
        categoryList.append(category.name)
    return jsonify(code=RET.OK, flag=True , message='获取科室信息成功', data = categoryList)

# 修改用户信息
@general_blue.route('/changeuser', methods=['POST'])
@authorize
def changeUser(): 
    id = request.json.get('id')
    idnum =  request.json.get('idnum')
    username   =  request.json.get('username')
    department = request.json.get('department')
    keshi = request.json.get('keshi')
    category = request.json.get('category')
    wage_category = request.json.get('wage_category')
    job = request.json.get('job')
    position = request.json.get('position')
    remarks = request.json.get('remarks')
    bonus_category = request.json.get('bonus_category')
    password = request.json.get('password')
    print(remarks)
    userInfo = UsersModel.query.get(id)
    if (userInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='找不到用户')
    userInfo.username  = username
    userInfo.idnum     = idnum
    userInfo.department = department
    userInfo.keshi = keshi #KeshiModel.query.filter_by(name=keshi).first().id
    userInfo.category = CategoryModel.query.filter_by(name=category).first().id
    userInfo.wage_category = wage_category
    userInfo.job = job
    userInfo.position = position
    userInfo.remarks = remarks
    userInfo.bonus_category = bonus_category

    if(password!=None):
        userInfo.password = userInfo.set_password(password)
    userInfo.update()
    return jsonify(code=RET.OK, flag=True, message='修改用户信息成功')

#新增加用户信息
@general_blue.route('/adduser', methods=['POST'])
@authorize
def createUser():
    idnum =  request.json.get('idnum')
    username   =  request.json.get('username')
    department = request.json.get('department')
    keshi = request.json.get('keshi')
    category = request.json.get('category')
    wage_category = request.json.get('wage_category')
    job = request.json.get('job')
    position = request.json.get('position')
    remarks = request.json.get('remarks')
    worknum  = request.json.get('worknum')
    bonus_category = request.json.get('bonus_category')

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
    user.keshi = keshi
    user.category = CategoryModel.query.filter_by(name=category).first().id
    # 添加用户
    result = UsersModel.add(UsersModel, user)

    # 添加角色
    role = RolesModel(userId=user.id,role="user")
    result = RolesModel.add(RolesModel, role)

    if user.id:
        return jsonify(code=RET.OK, flag=True, message='添加用户成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='添加用户失败')
     

# 获取所有管理项目的信息
@general_blue.route('/getprojectlist', methods=['GET'])
@authorize
def getProjectList(): 
    projectInfo = ManageModel.query.all()
    
    projectList = []
    for pro in projectInfo:
        userInfo = UsersModel.query.get(pro.manager)
        projectList.append({"id":pro.id,"name":pro.name,"manager":userInfo.worknum,"managername":userInfo.username, "isBig":pro.isBig,"state":pro.state})
    
    return jsonify(code=RET.OK, flag=True, message='获取管理项目成功', data=projectList)


# 获取所有进行中管理项目的信息
@general_blue.route('/getcurprojectlist', methods=['GET'])
@authorize
def getCurProjectList(): 
    projectInfo = ManageModel.query.filter_by(state='进行中').all()
    
    projectList = []
    for pro in projectInfo:
        projectList.append({"id":pro.id,"name":pro.name})
    
    return jsonify(code=RET.OK, flag=True, message='获取管理项目成功', data=projectList)



# 新增管理项目
@general_blue.route('/createproject', methods=['POST'])
@authorize
def createManageProject(): 
    name = request.json.get('name')
    manager = request.json.get('manager')
    state = request.json.get('state')
    isBig = request.json.get('isBig')

    user = UsersModel.query.filter_by(username=manager).first()
    if (user is None):
        return jsonify(code=RET.NODATA, flag=False, message='该项目经理不存在')

    manage = ManageModel(name=name, manager=user.id, isBig=isBig, state=state)
    result = ManageModel.add(ManageModel, manage)

    keshi = KeshiModel.query.filter_by(manager=user.id).first()
    if(keshi is None):
        # 添加角色
        roleInfo = RolesModel.query.filter_by(userId=user.id,role="manager_prom").first()
        if(roleInfo is None):
            role = RolesModel(userId=user.id,role="manager_prom")
            result = RolesModel.add(RolesModel, role)

    if manage.id:
        return jsonify(code=RET.OK, flag=True, message='新增管理项目成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增管理项目失败')

# 删除管理项目
@general_blue.route('/del/<int:id>', methods=['DELETE'])
@authorize
def delManageProject(id): 
    project = ManageModel.query.get(id)
    if (project is None):
        return jsonify(code=RET.NODATA, flag=False, message='该管理项目不存在')
    project.delete(id)
    return jsonify(code=RET.OK, flag=True, message='删除管理项目成功')


# 修改管理项目
@general_blue.route('/changeproject', methods=['POST'])
@authorize
def changeManageProject(): 
    id = request.json.get('id')
    name = request.json.get('name')
    manager = request.json.get('manager')
    state = request.json.get('state')
    isBig = request.json.get('isBig')

    manageInfo = ManageModel.query.get(id)
    if(manageInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该管理项目不存在')

    newUser = UsersModel.query.filter_by(worknum=manager).first()
    if (newUser is None):
        return jsonify(code=RET.NODATA, flag=False, message='该项目经理不存在')

    oriUserId = manageInfo.manager

    manageInfo.name = name
    manageInfo.manager = newUser.id
    manageInfo.state = state
    manageInfo.isBig = isBig
    manageInfo.update()

    if(oriUserId!=newUser.id):
        # 添加角色
        roleInfo = RolesModel.query.filter_by(userId=newUser.id,role="manager_prom").first()
        if(roleInfo is None):
            role = RolesModel(userId=newUser.id,role="manager_prom")
            result = RolesModel.add(RolesModel, role)

        # 修改角色
        oriPro = ManageModel.query.filter_by(manager=oriUserId).first()
        if(oriPro is None):
            roleInfo = RolesModel.query.filter_by(userId=oriUserId,role="manager_prom").first()
            roleInfo.delete(roleInfo.id)


    return jsonify(code=RET.OK, flag=True, message='修改管理项目信息成功')


# 获取所有发放计划的信息
@general_blue.route('/getplanlist', methods=['GET'])
@authorize
def getPlanList(): 
    planInfo = BonusPlanModel.query.all()
    
    planList = []
    for plan in planInfo:
        planList.append({"id":plan.id,"name":plan.name,"year":plan.year,"quarter":plan.quarter,"state":plan.state})
    
    return jsonify(code=RET.OK, flag=True, message='获取所有发放计划成功', data=planList)

# 新增发放计划
@general_blue.route('/createplan', methods=['POST'])
@authorize
def createBonusPlan(): 
    year = request.json.get('year')
    quarter = request.json.get('quarter')
    state = request.json.get('state')
    name = year+quarter

    plan = BonusPlanModel(name=name, year=year, quarter=quarter, state=state)
    result = BonusPlanModel.add(ManageModel, plan)

    if plan.id:
        return jsonify(code=RET.OK, flag=True, message='新增发放计划成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增发放计划失败')

# 修改发放计划
@general_blue.route('/changeplan', methods=['POST'])
@authorize
def changePlan(): 
    id = request.json.get('id')
    year = request.json.get('year')
    quarter = request.json.get('quarter')
    state = request.json.get('state')

    planInfo = BonusPlanModel.query.get(id)
    if(planInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该发放计划不存在')

    planInfo.name = year+quarter
    planInfo.year = year
    planInfo.quarter = quarter
    planInfo.state = state
    planInfo.update()

    return jsonify(code=RET.OK, flag=True, message='修改发放计划信息成功')

# 获取初始化发放计划的信息
@general_blue.route('/getcurplanlist', methods=['GET'])
@authorize
def getCurPlanList(): 
    planInfo = BonusPlanModel.query.filter_by(state="初始化").all()
    
    planList = []
    for plan in planInfo:
        planList.append({"id":plan.id,"name":plan.name})
    
    return jsonify(code=RET.OK, flag=True, message='获取所有初始化的发放计划成功', data=planList)

# 获取审核发放计划的信息
@general_blue.route('/getshenplanlist', methods=['GET'])
@authorize
def getShenPlanList(): 
    planInfo = BonusPlanModel.query.filter_by(state="审核").all()
    
    planList = []
    for plan in planInfo:
        planList.append({"id":plan.id,"name":plan.name})
    
    return jsonify(code=RET.OK, flag=True, message='获取所有审核的发放计划成功', data=planList)


# 获取项目经理发放计划的信息
@general_blue.route('/getproplanlist', methods=['GET'])
@authorize
def getProPlanList(): 
    planInfo = BonusPlanModel.query.filter_by(state="项目经理发放中").all()
    
    planList = []
    for plan in planInfo:
        planList.append({"id":plan.id,"name":plan.name})
    
    return jsonify(code=RET.OK, flag=True, message='获取所有项目经理发放中的发放计划成功', data=planList)


# 获取室主任发放计划的信息
@general_blue.route('/getshiplanlist', methods=['GET'])
@authorize
def getShiPlanList(): 
    planInfo = BonusPlanModel.query.filter(BonusPlanModel.state.in_(["室主任发放中", "项目经理发放中"])).all()
        
    planList = []
    for plan in planInfo:
        planList.append({"id":plan.id,"name":plan.name,"state":plan.state})
    
    return jsonify(code=RET.OK, flag=True, message='获取所有室主任发放中的发放计划成功', data=planList)




#新增加科室
@general_blue.route('/addkeshi', methods=['POST'])
@authorize
def addKeshi():
    name =  request.json.get('name')
    worknum = request.json.get('manager_worknum')
    isMan = request.json.get('isMan')

    keshiInfo = KeshiModel.query.filter_by(name=name).first()
    if (keshiInfo):
        return jsonify(code=RET.NODATA, flag=False, message='该科室已存在')
    
    userInfo = UsersModel.query.filter_by(worknum=worknum).first()
    if (userInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该工号不存在')

    keshiInfo = KeshiModel.query.filter_by(manager=userInfo.id).first()
    if (keshiInfo):
        return jsonify(code=RET.NODATA, flag=False, message='该工号已是其他室主任')

    newKeshi = KeshiModel(name=name, manager=userInfo.id, type=isMan)
    # 添加科室
    result = KeshiModel.add(KeshiModel, newKeshi)

    # 添加角色
    roleInfo = RolesModel.query.filter_by(userId=userInfo.id,role="manager_shi").first()
    if(roleInfo is None):
        role = RolesModel(userId=userInfo.id,role="manager_shi")
        result = RolesModel.add(RolesModel, role)

    if newKeshi.id:
        return jsonify(code=RET.OK, flag=True, message='添加新科室成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='添加新科室失败')

# 修改科室信息
@general_blue.route('/changekeshi', methods=['POST'])
@authorize
def changeKeshi(): 
    id = request.json.get('id')
    name =  request.json.get('name')
    manager_worknum   =  request.json.get('manager_worknum')
    isMan = request.json.get('isMan')

    keshiInfo = KeshiModel.query.filter_by(name=name).first()
    if (keshiInfo and keshiInfo.id!=id):
        return jsonify(code=RET.NODATA, flag=False, message='该科室已存在')
    
    newUser = UsersModel.query.filter_by(worknum=manager_worknum).first()
    if (newUser is None):
        return jsonify(code=RET.NODATA, flag=False, message='该工号不存在')
    
    keshiInfo = KeshiModel.query.filter_by(manager=newUser.id).first()
    if (keshiInfo and keshiInfo.id!=id):
        return jsonify(code=RET.NODATA, flag=False, message='该工号已是其他室主任')

    curKeshi = KeshiModel.query.get(id)
    oriUserId = curKeshi.manager
    curKeshi.name = name
    curKeshi.manager = newUser.id
    curKeshi.type = isMan
    curKeshi.update()

    if(oriUserId!=newUser.id):
        # 添加角色
        roleInfo = RolesModel.query.filter_by(userId=newUser.id,role="manager_shi").first()
        if(roleInfo is None):
            role = RolesModel(userId=newUser.id,role="manager_shi")
            result = RolesModel.add(RolesModel, role)

        # 修改角色
        oriPro = KeshiModel.query.filter_by(manager=oriUserId).first()
        if(oriPro is None):
            roleInfo = RolesModel.query.filter_by(userId=oriUserId,role="manager_shi").first()
            roleInfo.delete(roleInfo.id)
    

    return jsonify(code=RET.OK, flag=True, message='修改科室信息成功')

# 删除一个科室
@general_blue.route('/delkeshi/<int:id>', methods=['DELETE'])
@authorize
def delKeshi(id): 
    keshi = KeshiModel.query.get(id)
    if (keshi is None):
        return jsonify(code=RET.NODATA, flag=False, message='该科室不存在')
    keshi.delete(id)
    return jsonify(code=RET.OK, flag=True, message='删除该科室成功')
     

# 获取所有人每个科研项目分多少钱的总体信息
@general_blue.route('/getresdetail/<int:planId>/<int:page>/<int:size>', methods=['GET'])
@authorize
def getResAllDetail(planId,page,size): 

    totalnum = db.session.query(db.func.count(UsersModel.id)).scalar()
    db.session.commit()
    # page = 6
    # size = 500
    allMember = UsersModel.query.paginate(page,per_page=size).items
    allProject = BonusDetailModel.query.filter_by(planId=planId, projectType=0).all()

    allMemberId = [x.id for x in allMember]

    memberDetailList = []
    projectList = []
    projectIdList = []

    allKeshi = KeshiModel.query.all()
    keshiInfo = {}
    for keshi in allKeshi:
        keshiInfo[keshi.id] = keshi.name

    allCategory = CategoryModel.query.all()
    categoryInfo = {}
    for cate in allCategory:
        categoryInfo[cate.id] = cate.name

    for project in allProject:
        pro = ResearchModel.query.get(project.projectId)
        name = pro.number + ": "+ pro.name
        projectList.append({"id":str(project.projectId),"name":name})
        projectIdList.append(project.projectId)

    # allDetail = UserDetailModel.query.filter(UserDetailModel.userId.in_(allMemberId), UserDetailModel.planId==planId, UserDetailModel.projectType==0).all()



    for member in allMember:
        if(member.category==15): continue
        total = 0
        # keshi = KeshiModel.query.get(member.keshi).name
        keshi = keshiInfo[member.keshi]
        # category = CategoryModel.query.get(member.category).name
        category = categoryInfo[member.category]
        memberdict = {"userId":member.id,"department":member.department,"keshi":keshi,"username":member.username,
            "idnum":member.idnum+"\u200b","category":category,"wage_category":member.wage_category,"job":member.job,"position":member.position,"remarks":member.remarks}

        memberAllDetail = UserDetailModel.query.filter(UserDetailModel.userId==member.id, UserDetailModel.planId==planId, UserDetailModel.projectType==0, UserDetailModel.projectId.in_(projectIdList)).all()
       
        # for project in allProject:
        #     memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=project.projectId, projectType=0, userId=member.id).first()
        #     if(memberdetail is None):
        #         memberdict[str(project.projectId)] = 0
        #     else: 
        #         memberdict[str(project.projectId)] = memberdetail.amount
        #         total += memberdetail.amount

        #     history = DetailHistoryModel.query.filter_by(planId=planId,projectId=project.projectId,projectType=0 ,userId=member.id).first()
        #     if(history is None):
        #         memberdict[str(project.projectId)+"flag"] = False
        #     else: 
        #         memberdict[str(project.projectId)+"flag"] = True
        #         # total += memberdetail.amount

        for detail in memberAllDetail:
            memberdict[str(detail.projectId)] = detail.amount
            total += detail.amount
                   
        memberdict['total'] = total
        memberDetailList.append(memberdict)
    
    # 若选择第一页，在最上方添加各项目的汇总信息
    if(page==1):
        amount = 0
        amount_zhan = 0
        amount_buzhan = 0
        memberdict1 = {"username":"合计(占工资总额)"}
        memberdict2 = {"username":"合计(不占工资总额)"}
        memberdict3 = {"username":"总合计"}
        memberdict4 = {"username":"浮动绩效额度"}
        for project in allProject:
            projectdetail = BonusDetailModel.query.filter_by(planId=planId, projectId=project.projectId, projectType=0).first()
            curamount_zhan = 0 if projectdetail.amount_zhan==None else projectdetail.amount_zhan
            curamount_buzhan = 0 if projectdetail.amount_buzhan==None else projectdetail.amount_buzhan
            memberdict1[str(project.projectId)] = curamount_zhan
            memberdict2[str(project.projectId)] = curamount_buzhan
            memberdict3[str(project.projectId)] = curamount_zhan + curamount_buzhan
            memberdict1[str(project.projectId)+"flag"] = False
            memberdict2[str(project.projectId)+"flag"] = False
            memberdict3[str(project.projectId)+"flag"] = False
            amount_zhan += curamount_zhan
            amount_buzhan += curamount_buzhan
            amount += projectdetail.amount
            memberdict4[str(project.projectId)] = projectdetail.amount
            memberdict4[str(project.projectId)+"flag"] = False

        memberdict1['total'] = amount_zhan
        memberdict2['total'] = amount_buzhan
        memberdict3['total'] = amount_zhan + amount_buzhan
        memberdict4['total'] = amount

        memberDetailList.insert(0,memberdict3)
        memberDetailList.insert(0,memberdict2)
        memberDetailList.insert(0,memberdict1)
        memberDetailList.insert(0,memberdict4)
        # memberDetailList.insert(0,memberdict4)

    
    return jsonify(code=RET.OK, flag=True, message='获取所有人每个科研项目分配信息成功',detail=memberDetailList, project=projectList, total=totalnum)

# 获取所有人每个管理项目分多少钱的总体信息
@general_blue.route('/getmandetail/<int:planId>/<int:page>/<int:size>', methods=['GET'])
@authorize
def getManAllDetail(planId,page,size): 
    totalnum = db.session.query(db.func.count(UsersModel.id)).scalar()
    db.session.commit()
    allMember = UsersModel.query.paginate(page,per_page=size).items
    allProject = BonusDetailModel.query.filter_by(planId=planId, projectType=1).all()

    allMemberId = [x.id for x in allMember]

    memberDetailList = []
    projectList = []
    projectIdList = []

    allKeshi = KeshiModel.query.all()
    keshiInfo = {}
    for keshi in allKeshi:
        keshiInfo[keshi.id] = keshi.name

    allCategory = CategoryModel.query.all()
    categoryInfo = {}
    for cate in allCategory:
        categoryInfo[cate.id] = cate.name

    for project in allProject:
        name = ManageModel.query.get(project.projectId).name
        projectList.append({"id":str(project.projectId),"name":name})
        projectIdList.append(project.projectId)


    for member in allMember:
        if(member.category==15): continue
        total = 0
        keshi = keshiInfo[member.keshi]
        category = categoryInfo[member.category]
        memberdict = {"userId":member.id,"keshi":keshi,"username":member.username,
            "idnum":member.idnum+"\u200b","category":category,"wage_category":member.wage_category,"job":member.job,"position":member.position,"remarks":member.remarks}
        
        memberAllDetail = UserDetailModel.query.filter(UserDetailModel.userId==member.id, UserDetailModel.planId==planId, UserDetailModel.projectType==1, UserDetailModel.projectId.in_(projectIdList)).all()
       

        # for project in allProject:
        #     memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=project.projectId, projectType=1, userId=member.id).first()
        #     if(memberdetail is None):
        #         memberdict[str(project.projectId)] = 0
        #     else: 
        #         memberdict[str(project.projectId)] = memberdetail.amount
        #         total += memberdetail.amount

        #     history = DetailHistoryModel.query.filter_by(planId=planId,projectId=project.projectId,projectType=1 ,userId=member.id).first()
        #     if(history is None):
        #         memberdict[str(project.projectId)+"flag"] = False
        #     else: 
        #         memberdict[str(project.projectId)+"flag"] = True
        #         # total += memberdetail.amount
        
        for detail in memberAllDetail:
            memberdict[str(detail.projectId)] = detail.amount
            total += detail.amount

        # 扣发
        koufaInfo = KoufaModel.query.filter_by(planId=planId,userId=member.id).first()
        if(koufaInfo is not None):
            memberdict['koufa'] = koufaInfo.amount
            total -= koufaInfo.amount
        
        memberdict['total'] = total
        memberDetailList.append(memberdict)
    
    # 若选择第一页，在最上方添加各项目的汇总信息
    if(page==1):
        amount_zhan = 0
        amount_buzhan = 0
        amount = 0
        amount_b = 0
        memberdict1 = {"username":"合计(占工资总额)"}
        memberdict2 = {"username":"合计(不占工资总额)"}
        memberdict3 = {"username":"占工资总额奖金包"}
        memberdict4 = {"username":"不占工资总额奖金包"}
        for project in allProject:
            projectdetail = BonusDetailModel.query.filter_by(planId=planId, projectId=project.projectId, projectType=1).first()
            memberdict1[str(project.projectId)] = projectdetail.amount_zhan
            memberdict2[str(project.projectId)] = projectdetail.amount_buzhan
            memberdict3[str(project.projectId)] = projectdetail.amount
            memberdict4[str(project.projectId)] = projectdetail.amount_b
            amount_zhan += projectdetail.amount_zhan
            amount_buzhan += projectdetail.amount_buzhan
            amount += projectdetail.amount
            amount_b += projectdetail.amount_b
        memberdict1['total'] = amount_zhan
        memberdict2['total'] = amount_buzhan
        memberdict3['total'] = amount
        memberdict4['total'] = amount_b
        memberDetailList.insert(0,memberdict2)
        memberDetailList.insert(0,memberdict4)
        memberDetailList.insert(0,memberdict1)
        memberDetailList.insert(0,memberdict3)

    return jsonify(code=RET.OK, flag=True, message='获取所有人每个管理项目分配信息成功',detail=memberDetailList, project=projectList,total=totalnum)


# 获取项目成员历史分配情况
@general_blue.route('/getreshistory', methods=['POST'])
@authorize
def getResHistory(): 
    userId = request.form.get('userId')
    planId = request.form.get('planId')
    projectId =request.form.get('project')

    historydetail = DetailHistoryModel.query.filter_by(planId=planId, projectId=projectId, projectType=0, userId=userId).all()
    historyList = []

    for history in historydetail:
        historyList.append({"amount":history.amount, "time":history.time})


    return jsonify(code=RET.OK, flag=True, message='获取该项目成员历史分配', data=historyList)

# 获取项目成员历史分配情况
@general_blue.route('/getmanhistory', methods=['POST'])
@authorize
def getManHistory(): 
    userId = request.form.get('userId')
    planId = request.form.get('planId')
    projectId =request.form.get('project')

    historydetail = DetailHistoryModel.query.filter_by(planId=planId, projectId=projectId, projectType=1, userId=userId).all()
    historyList = []

    for history in historydetail:
        historyList.append({"amount":history.amount, "time":history.time})


    return jsonify(code=RET.OK, flag=True, message='获取该项目成员历史分配', data=historyList)

# 获取所有人所有项目详情信息
@general_blue.route('/getdetail/<int:planId>', methods=['GET'])
@authorize
def getAllDetail(planId): 
    allMember = UsersModel.query.filter(UsersModel.category!=15).all()
    allProject = BonusDetailModel.query.filter_by(planId=planId, projectType=1).all()

    allKeshi = KeshiModel.query.all()
    keshiInfo = {}
    for keshi in allKeshi:
        keshiInfo[keshi.id] = keshi.name

    allCategory = CategoryModel.query.all()
    categoryInfo = {}
    for cate in allCategory:
        categoryInfo[cate.id] = cate.name

    memberDetailList = []
    projectList = []
    projectIdList = []

    for project in allProject:
        name = ManageModel.query.get(project.projectId).name
        projectList.append({"id":str(project.projectId),"name":name})
        projectIdList.append(project.projectId)


    for member in allMember:
        total = 0
        keshi = keshiInfo[member.keshi]
        category = categoryInfo[member.category]
        memberdict = {"userId":member.id,"department":member.department,"keshi":keshi,"username":member.username,
            "idnum":member.idnum+"\u200b","category":category,"wage_category":member.wage_category,
            "job":member.job,"position":member.position,"remarks":member.remarks,"bonus_category":member.bonus_category}
        
        memberAllDetail = UserDetailModel.query.filter(UserDetailModel.userId==member.id, UserDetailModel.planId==planId, UserDetailModel.projectType==1, UserDetailModel.projectId.in_(projectIdList)).all()
       
        for detail in memberAllDetail:
            memberdict[str(detail.projectId)] = detail.amount
            total += detail.amount
        
        # 科研项目总和
        allResDetail = UserDetailModel.query.filter_by(planId=planId, projectType=0, userId=member.id).all()
        total = 0
        for detail in allResDetail: total += detail.amount
        memberdict['total_res'] = total

        # 扣发
        koufaInfo = KoufaModel.query.filter_by(planId=planId,userId=member.id).first()
        if(koufaInfo is not None):
            memberdict['koufa'] = koufaInfo.amount

        memberDetailList.append(memberdict)


    return jsonify(code=RET.OK, flag=True, message='获取所有人分配信息成功',detail=memberDetailList, project=projectList)

from flask import g, current_app, jsonify, request, session
from pyrsistent import v
from server.models import category

# from server.app import db
# from server.api.models import User
from utils.response_code import RET
# from server.api import user_blue
# from bson.objectid import ObjectId

# user_cl = db.users # select the collection

from . import project_blue
from . import authorize
from models.user import UsersModel
from models.role import RolesModel
from models.keshi import KeshiModel
from models.category import CategoryModel
from models.manage import ManageModel
from models.research import ResearchModel
from models.bonusplan import BonusPlanModel

from models.bonusdetail import BonusDetailModel
from models.keshidetail import KeshiDetailModel
from models.member import MemberModel
from models.userdetail import UserDetailModel
from models.detail_history import DetailHistoryModel
from decimal import *
import uuid
import time

# 获取本人的大项目列表
@project_blue.route('/getmybigproject/<int:planId>', methods=['GET'])
@authorize
def getBigProjectList(planId): 
    userId = session.get('userid')

    detailList = BonusDetailModel.query.filter_by(planId=planId).all()

    projectList = []
    i = 0

    for detail in detailList:
        if(detail.projectType==0):
            projectInfo = ResearchModel.query.get(detail.projectId)
            if(projectInfo.isBig and projectInfo.manager==userId):
                projectList.append({"id":i,"projectId":detail.projectId, "projectType":0, "projectName":projectInfo.name, "amount":detail.amount})
                i += 1
        else:
            projectInfo = ManageModel.query.get(detail.projectId)
            if(projectInfo.isBig and projectInfo.manager==userId):
                projectList.append({"id":i,"projectId":detail.projectId, "projectType":1, "projectName":projectInfo.name, "amount":detail.amount})
                i += 1
            
    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配信息成功', data=projectList)

# 获取本人的小项目列表
@project_blue.route('/getmysmallproject/<int:planId>', methods=['GET'])
@authorize
def getSmallProjectList(planId): 
    userId = session.get('userid')
    keshi = KeshiModel.query.filter_by(manager=userId).first()

    detailList = BonusDetailModel.query.filter_by(planId=planId).all()

    projectList = []

    for detail in detailList:
        if(detail.projectType==0):
            projectInfo = ResearchModel.query.get(detail.projectId)
            if(not projectInfo.isBig and projectInfo.manager==userId):
                projectList.append({"bonusId":detail.id,"projectId":detail.projectId, "projectType":0, "projectName":projectInfo.name, "amount":detail.amount, "amount_zhan":detail.amount_zhan, "amount_buzhan":detail.amount_buzhan})
        elif(keshi is None):
            projectInfo = ManageModel.query.get(detail.projectId)
            if(not projectInfo.isBig and projectInfo.manager==userId):
                projectList.append({"bonusId":detail.id,"projectId":detail.projectId, "projectType":1, "projectName":projectInfo.name, "amount":detail.amount, "amountb":detail.amount_b, "amount_zhan":detail.amount_zhan, "amount_buzhan":detail.amount_buzhan})
            
    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配信息成功', data=projectList)


# 统计项目经理发放进度
@project_blue.route('/getprogress/<int:planId>', methods=['GET'])
@authorize
def getProgressList(planId): 
    allRes = ResearchModel.query.all()
    resInfo = {}
    for res in allRes:
        resInfo[res.id] = res

    allProject = BonusDetailModel.query.filter_by(planId=planId, projectType=0).all()
    proProgressList = []
    for pro in allProject:
        curres = resInfo[pro.projectId]
        userInfo = UsersModel.query.get(curres.manager)

        state = 0
        if(not curres.isBig):
            if(pro.amount_zhan!=pro.amount): state = 1
        else:
            detail = KeshiDetailModel.query.filter_by(planId=planId, projectId=curres.id, projectType=0).first()
            if(detail is None): state = 1
        
        proProgressList.append({"projectName":curres.name,"manager":userInfo.username,"state":state})
    
    proProgressList.sort(key= lambda x:x["state"], reverse=True)

    return jsonify(code=RET.OK, flag=True, message='获取项目经理分配进度信息成功',data=proProgressList)


# 获取科研项目奖金包分配（每个项目分多少）的信息
@project_blue.route('/getbigprojectdetail', methods=['POST'])
@authorize
def getBigProjectDetail(): 
    planId =request.form.get('planId')
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')


    detailInfo = KeshiDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType).all()
    detailDict = {}
    i = 0
    for detail in detailInfo:
        detailDict[detail.keshiId] = i
        i += 1
    
    keshiInfo = KeshiModel.query.filter_by(type=projectType)


    detailList = []
    for keshi in keshiInfo:
        if(keshi.id in detailDict):
            detail = detailInfo[detailDict[keshi.id]]
            detailList.append({"id":detail.id,"keshiId":keshi.id,"keshiname":keshi.name,"amount":detail.amount,"amount_zhan":detail.amount_zhan,"amount_buzhan":detail.amount_buzhan})
        else:
            detailList.append({"keshiId":keshi.id,"keshiname":keshi.name,"amount":0,"amount_zhan":0,"amount_buzhan":0})
    

    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配信息成功', data=detailList)

# 增加大项目奖金包分配（每个室分多少）的信息
@project_blue.route('/createallkeshidetail', methods=['POST'])
@authorize
def createAllKeshiDetail(): 
    planId = request.json.get('planId')
    projectId = request.json.get('projectId')
    projectType = request.json.get('projectType')
    keshidetail = request.json.get('keshiDetailList')

    for info in keshidetail:
        if(info['amount']=='' or info['amount']==0):
            if(info.get('id')):
                KeshiDetailModel.delete(KeshiDetailModel, info['id'])
        else:
            if(info.get('id')):
                detail = KeshiDetailModel.query.get(info['id'])
                if(detail.amount!=Decimal(info['amount'])):
                    detail.amount = info['amount']
                    detail.update()
            else:
                newdetail = KeshiDetailModel(planId=planId, projectId=projectId, projectType=projectType, keshiId=info['keshiId'], amount=info['amount'])
                result = KeshiDetailModel.add(KeshiDetailModel, newdetail) 

    
    return jsonify(code=RET.OK, flag=True, message='新增项目奖金包所有科室分配信息成功')


# 增加一条大项目奖金包分配（每个室分多少）的信息
# TODO 更新占不占工资总额
@project_blue.route('/createkeshidetail', methods=['POST'])
@authorize
def createKeshiDetail(): 
    planId = request.json.get('planId')
    keshiId = request.json.get('keshiId')
    projectId = request.json.get('projectId')
    projectType = request.json.get('projectType')
    amount = request.json.get('amount')

    detail = KeshiDetailModel.query.filter_by(planId=planId, keshiId=keshiId, projectId=projectId, projectType=projectType).first()
    if (detail):
        return jsonify(code=RET.NODATA, flag=False, message='该科室奖金包已分配')

    detail = KeshiDetailModel(planId=planId, projectId=projectId, projectType=projectType, keshiId=keshiId, amount=amount)

    result = KeshiDetailModel.add(KeshiDetailModel, detail)

    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='新增项目奖金包科室分配信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增项目奖金包科室分配信息失败')

# 修改一条项目奖金包分配（每个科室分多少）的信息
@project_blue.route('/changekeshidetail', methods=['POST'])
@authorize
def changeKeshiDetail(): 
    id = request.json.get('id')
    amount = request.json.get('amount')

    detail = KeshiDetailModel.query.get(id)
    if (detail is None):
        return jsonify(code=RET.NODATA, flag=False, message='该条信息不存在')
    
    detail.amount = amount
    detail.update()

    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='修改科室奖金包分配信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='修改科室奖金包分配信息失败')


# 删除一条项目奖金包分配（每个科室分多少）的信息
@project_blue.route('/delkeshi/<int:id>', methods=['DELETE'])
@authorize
def delKeshiDetail(id): 
    detail = KeshiDetailModel.query.get(id)
    if (detail is None):
        return jsonify(code=RET.NODATA, flag=False, message='该条信息不存在')
    detail.delete(id)
    return jsonify(code=RET.OK, flag=True, message='删除项目奖金包分配信息成功')


# 获取项目成员信息
@project_blue.route('/getmember', methods=['POST'])
@authorize
def getMember(): 
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')

    memberInfo = MemberModel.query.filter_by(projectId=projectId, projectType=projectType).all()

    memberList = []
    for member in memberInfo:
        userInfo = UsersModel.query.get(member.userId)
        keshi = KeshiModel.query.get(userInfo.keshi).name
        category = CategoryModel.query.get(userInfo.category).name

        memberList.append({"id":member.id,"userId":userInfo.id,"keshi":keshi,"username":userInfo.username,"idnum":userInfo.idnum,"category":category,"wage_category":userInfo.wage_category,"position":userInfo.position,"bonus_category":userInfo.bonus_category})
    
    return jsonify(code=RET.OK, flag=True, message='获取该项目成员信息成功', data=memberList)

# 获取项目成员信息
@project_blue.route('/addmember', methods=['POST'])
@authorize
def addMember(): 
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')
    username = request.form.get('username')
    user = UsersModel.query.filter_by(username=username).first()

    if (user is None):
        return jsonify(code=RET.NODATA, flag=False, message='该姓名不存在')

    if(projectType=='1'):
        if(user.bonus_category=="科研" or user.bonus_category=="固定发放"):
            return jsonify(code=RET.NODATA, flag=False, message='管理项目奖金不能发给科研、固定发放类型人员')
        if(user.position=="A类" or user.position=="B类"):
            return jsonify(code=RET.NODATA, flag=False, message='管理项目奖金不能发给A类或B类人员')
    else:
        if(user.bonus_category=="管理" or user.bonus_category=="固定发放"):
            return jsonify(code=RET.NODATA, flag=False, message='科研项目奖金不能发给管理、固定发放类型人员')
        if(user.position=="A类" or user.position=="B类"):
            return jsonify(code=RET.NODATA, flag=False, message='科研项目奖金不能发给A(B)类人员')
    
    member = MemberModel.query.filter_by(projectId=projectId, projectType=projectType, userId=user.id).first()
    if (member):
        return jsonify(code=RET.NODATA, flag=False, message='该成员已存在')

    member = MemberModel(projectId=projectId, projectType=projectType, userId=user.id)

    result = MemberModel.add(MemberModel, member)

    if member.id:
        return jsonify(code=RET.OK, flag=True, message='新增项目成员成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增项目成员失败')


# 删除一个项目中的一个成员
@project_blue.route('/delmember/<int:id>/<int:planId>', methods=['DELETE'])
@authorize
def delMember(id,planId): 
    member = MemberModel.query.get(id)
    if (member is None):
        return jsonify(code=RET.NODATA, flag=False, message='该成员不存在')
    member.delete(id)

    memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=member.projectId, projectType=member.projectType, userId=member.userId).first()
    if(memberdetail):
        memberdetail.delete(memberdetail.id)

    return jsonify(code=RET.OK, flag=True, message='删除项目成员成功')


# 获取项目成员分配情况
@project_blue.route('/getmemberdetail', methods=['POST'])
@authorize
def getMemberDetail(): 
    planId = request.form.get('planId')
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')

    memberInfo = MemberModel.query.filter_by(projectId=projectId, projectType=projectType).all()
    memberDetailList = []

    for member in memberInfo:
        user = UsersModel.query.get(member.userId)
        if(user.wage_category == '占工资总额'): username = user.username + '(' + user.wage_category +')'
        else: username = user.username + '(' + user.wage_category + user.position +')'
        user_category = user.wage_category

        memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=member.userId).first()
        if(memberdetail is None):
            memberDetailList.append({"userId":member.userId, "username":username, "user_category":user_category,"position":user.position,"bonus_category":user.bonus_category,"amount":0})
        else:
            memberDetailList.append({"userId":member.userId, "username":username, "user_category":user_category, "position":user.position, "bonus_category":user.bonus_category,"amount":memberdetail.amount})
    
    return jsonify(code=RET.OK, flag=True, message='获取该项目成员详细信息成功', data=memberDetailList)


# 用于导出项目成员分配情况
@project_blue.route('/getmemberdetailexport', methods=['POST'])
@authorize
def getMemberDetailExport(): 
    planId = request.form.get('planId')
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')

    memberInfo = MemberModel.query.filter_by(projectId=projectId, projectType=projectType).all()
    memberDetailList = []
    memberDetailList.append(["室","姓名","身份证号","类别","工资总额类别","奖金库","岗位","金额"])

    for member in memberInfo:
        user = UsersModel.query.get(member.userId)
        keshi = KeshiModel.query.get(user.keshi).name

        category = CategoryModel.query.get(user.category).name

        memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=member.userId).first()
        if(memberdetail is None):
            memberDetailList.append([keshi, user.username,user.idnum,category, user.wage_category, user.bonus_category, user.position, 0])
        else:
            memberDetailList.append([keshi, user.username,user.idnum,category, user.wage_category, user.bonus_category, user.position, float(memberdetail.amount)])
    
    return jsonify(code=RET.OK, flag=True, message='导出该项目成员详细信息成功', data=memberDetailList)


# 修改项目成员分配情况
@project_blue.route('/changememberdetail', methods=['POST'])
@authorize
def changeMemberDetail(): 
    bonusId = request.json.get('bonusId')
    planId = request.json.get('planId')
    projectId = request.json.get('projectId')
    projectType = request.json.get('projectType')
    memberdetailList = request.json.get('memberDetailList')

    zhan_total = 0
    buzhan_total = 0

    for info in memberdetailList:
        if(info['amount']=='' or info['amount']==0):
            memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=info['userId']).first()
            if(memberdetail):
                newhistory = DetailHistoryModel(planId=planId,projectId=projectId,projectType=projectType,userId=info['userId'],amount=memberdetail.amount,time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                result = DetailHistoryModel.add(DetailHistoryModel, newhistory)
                memberdetail.delete(memberdetail.id)
        else:
            if(info['user_category']=='占工资总额'): zhan_total += Decimal(info['amount'])
            else: buzhan_total += Decimal(info['amount'])

            memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=info['userId']).first()
            if(memberdetail):
                if(memberdetail.amount!=Decimal(info['amount'])):
                    newhistory = DetailHistoryModel(planId=planId,projectId=projectId,projectType=projectType,userId=info['userId'],amount=memberdetail.amount,time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    result = DetailHistoryModel.add(DetailHistoryModel, newhistory)
                    memberdetail.amount = info['amount']
                    memberdetail.update()
            else:
                newdetail = UserDetailModel(planId=planId, projectId=projectId, projectType=projectType, userId=info['userId'], amount=info['amount'])
                result = UserDetailModel.add(UserDetailModel, newdetail) 
    
    bonusdetail = BonusDetailModel.query.get(bonusId)
    bonusdetail.amount_zhan = zhan_total
    bonusdetail.amount_buzhan = buzhan_total
    bonusdetail.update()

    
    return jsonify(code=RET.OK, flag=True, message='修改项目成员详细分配金额成功')


# 导入项目成员分配情况
@project_blue.route('/importmemberdetail', methods=['POST'])
@authorize
def importMemberDetail(): 
    form = request.json.get('form')
    bonusId = form['bonusId']
    planId = form['planId']
    projectId = form['projectId']
    projectType = form['projectType']

    rows = request.json.get('rows')
    # print(rows)

    zhan_total = 0
    buzhan_total = 0

    for row in rows:
        user = UsersModel.query.filter_by(idnum=row['身份证号']).first()
        # 项目成员变动
        if(user is None):
            return jsonify(code=RET.NODATA, flag=False, message='用户'+row['姓名']+'不存在')
        memberInfo = MemberModel.query.filter_by(projectId=projectId, projectType=projectType,userId=user.id).first()
        if(memberInfo is None):
            member = MemberModel(projectId=projectId, projectType=projectType, userId=user.id)
            result = MemberModel.add(MemberModel, member)
        
        # 成员金额变动
        if(row.get('金额')==0 or row.get('金额')==None):
            memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=user.id).first()
            if(memberdetail):
                memberdetail.delete(memberdetail.id)
        else:
            if(row['工资总额类别']=='占工资总额'): zhan_total += Decimal(row['金额'])
            else: buzhan_total += Decimal(row['金额'])

            memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=user.id).first()
            if(memberdetail):
                if(memberdetail.amount!=row['金额']):
                    memberdetail.amount = row['金额']
                    memberdetail.update()
            else:
                newdetail = UserDetailModel(planId=planId, projectId=projectId, projectType=projectType, userId=user.id, amount=row['金额'])
                result = UserDetailModel.add(UserDetailModel, newdetail) 
    
    bonusdetail = BonusDetailModel.query.get(bonusId)
    bonusdetail.amount_zhan = zhan_total
    bonusdetail.amount_buzhan = buzhan_total
    bonusdetail.update()

    return jsonify(code=RET.OK, flag=True, message='导入项目成员详细分配金额成功')


     
# 获取所有人每个科研项目分多少钱的总体信息
@project_blue.route('/getdetail/<int:planId>', methods=['GET'])
@authorize
def getAllDetail(planId):
    userId = session.get('userid') 
    allProject = BonusDetailModel.query.filter_by(planId=planId,projectType=0).all()

    # allMember = UsersModel.query.filter(category!=14).all()
    # memberDetailList = []

    projectList = []
    memberList = []
    memberTmp = set()
    for project in allProject:
        if(project.projectType==0): 
            cur = ResearchModel.query.get(project.projectId)
            name = cur.number + ": "+cur.name
        else: 
            cur = ManageModel.query.get(project.projectId)
            name = cur.name
        if(cur.manager==userId):
            projectList.append({"id":str(cur.id), "type":str(project.projectType),"name":name})
            alldetail = UserDetailModel.query.filter_by(planId=planId, projectId=cur.id, projectType=0).all()
            for detail in alldetail:
                if(detail.userId not in memberTmp):
                    memberTmp.add(detail.userId)
                    memberList.append(UsersModel.query.get(detail.userId))
    
    memberDetailList = []
    for member in memberList:
        total = 0
        keshi = KeshiModel.query.get(member.keshi).name
        category = CategoryModel.query.get(member.category).name

        memberdict = {"userId":member.id,"department":member.department,"keshi":keshi,"username":member.username,
            "idnum":member.idnum+"\u200b","category":category,"wage_category":member.wage_category,"position":member.position}
       

        for project in projectList:
            memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=int(project['id']), projectType=project['type'], userId=member.id).first()
            if(memberdetail is None):
                memberdict[project['id']] = 0
            else: 
                memberdict[project['id']] = memberdetail.amount
                total += memberdetail.amount

            history = DetailHistoryModel.query.filter_by(planId=planId, projectId=int(project['id']), projectType=project['type'], userId=member.id).first()
            if(history is None):
                memberdict[project['id']+"flag"] = False
            else: 
                memberdict[project['id']+"flag"] = True
                # total += memberdetail.amount
        memberdict['total'] = total
        memberDetailList.append(memberdict)
    
    amount = 0
    amount_zhan = 0
    amount_buzhan = 0
    memberdict1 = {"username":"合计(占工资总额)"}
    memberdict2 = {"username":"合计(不占工资总额)"}
    memberdict3 = {"username":"总合计"}
    memberdict4 = {"username":"浮动绩效额度"}
    for project in projectList:
        projectdetail = BonusDetailModel.query.filter_by(planId=planId, projectId=int(project['id']), projectType=project['type']).first()
        curamount_zhan = 0 if projectdetail.amount_zhan==None else projectdetail.amount_zhan
        curamount_buzhan = 0 if projectdetail.amount_buzhan==None else projectdetail.amount_buzhan
        memberdict1[project['id']] = curamount_zhan
        memberdict2[project['id']] = curamount_buzhan
        memberdict3[project['id']] = curamount_zhan + curamount_buzhan
        memberdict1[project['id']+"flag"] = False
        memberdict2[project['id']+"flag"] = False
        memberdict3[project['id']+"flag"] = False
        amount_zhan += curamount_zhan
        amount_buzhan += curamount_buzhan
        amount += projectdetail.amount
        memberdict4[project['id']] = projectdetail.amount
        memberdict4[project['id']+"flag"] = False

    memberdict1['total'] = amount_zhan
    memberdict2['total'] = amount_buzhan
    memberdict3['total'] = amount_zhan + amount_buzhan
    memberdict4['total'] = amount

    memberDetailList.append(memberdict4)
    memberDetailList.append(memberdict1)
    memberDetailList.append(memberdict2)
    memberDetailList.append(memberdict3)
    # memberDetailList.insert(0,memberdict4)

    return jsonify(code=RET.OK, flag=True, message='获取所有人每个项目分配信息成功',detail=memberDetailList, project=projectList)


# 获取项目成员历史分配情况
@project_blue.route('/gethistory', methods=['POST'])
@authorize
def getHistory(): 
    userId = request.form.get('userId')
    planId = request.form.get('planId')
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')

    historydetail = DetailHistoryModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=userId).all()
    historyList = []

    for history in historydetail:
        historyList.append({"amount":history.amount, "time":history.time})
        # print(history.amount)
    

    return jsonify(code=RET.OK, flag=True, message='获取该项目成员历史分配', data=historyList)


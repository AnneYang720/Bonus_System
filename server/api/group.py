from flask import g, current_app, jsonify, request, session

# from server.app import db
# from server.api.models import User
from utils.response_code import RET
# from server.api import user_blue
# from bson.objectid import ObjectId

# user_cl = db.users # select the collection

from . import group_blue
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


# 获取科研项目奖金包分配（每个项目分多少）的信息
# TODO 室主任权限管理
@group_blue.route('/getkeshiproject/<int:planId>', methods=['GET'])
@authorize
def getKeshiProjectDetail(planId): 
    userId = session.get('userid')
    keshiId = KeshiModel.query.filter_by(manager=userId).first().id
    keshiType = UsersModel.query.get(userId).department

    resProjectDetail = KeshiDetailModel.query.filter_by(planId=planId,keshiId=keshiId)
    keshiProjectList = []
    for detail in resProjectDetail:
        if(detail.projectType==0):
            projectInfo = ResearchModel.query.get(detail.projectId)
            keshiProjectList.append({"id":detail.id,"projectId":detail.projectId, "projectType":0, "projectName":projectInfo.name, "amount":detail.amount, "amount_zhan":detail.amount_zhan, "amount_buzhan":detail.amount_buzhan})
    
    
        # else:
        #     projectInfo = ManageModel.query.get(detail.projectId)
        #     keshiProjectList.append({"id":detail.id,"projectId":detail.projectId, "projectType":1, "projectName":projectInfo.name, "amount":detail.amount, "amount_zhan":detail.amount_zhan, "amount_buzhan":detail.amount_buzhan})

    manProjects = ManageModel.query.filter_by(manager=userId)
    for pro in manProjects:
        detail = BonusDetailModel.query.filter_by(planId=planId, projectId=pro.id, projectType=1).first()
        if(detail is not None):
            projectInfo = ManageModel.query.get(detail.projectId)
            keshiProjectList.append({"id":detail.id,"projectId":detail.projectId, "projectType":1, "projectName":projectInfo.name, "amount":detail.amount, "amountb":detail.amount_b, "amount_zhan":detail.amount_zhan, "amount_buzhan":detail.amount_buzhan})

    return jsonify(code=RET.OK, flag=True, message='获取该次计划本室分配信息成功',data=keshiProjectList, keshiId=keshiId, keshiType=keshiType)

# 统计室主任发放进度
@group_blue.route('/getprogress/<int:planId>', methods=['GET'])
@authorize
def getProgressList(planId): 
    allKeshi = KeshiModel.query.all()
    keshiInfo = {}
    keshiProgressList = []
    i = 0
    for keshi in allKeshi:
        userInfo = UsersModel.query.get(keshi.manager)
        keshiProgressList.append({"id":keshi.id,"keshiName":keshi.name,"manager":userInfo.username,"state":0})
        keshiInfo[keshi.id] = i
        i += 1


    resProjectDetail = KeshiDetailModel.query.filter_by(planId=planId).all()
    for detail in resProjectDetail:
        if(detail.amount_zhan!=detail.amount):
            keshiProgressList[keshiInfo[detail.keshiId]]["state"]=1
    
    manProjectDetail = BonusDetailModel.query.filter_by(planId=planId, projectType=1).all()
    for detail in manProjectDetail:       
        if(detail.amount_zhan!=detail.amount):
            userId = ManageModel.query.get(detail.projectId).manager
            keshiId = KeshiModel.query.filter_by(manager=userId).first().id
            keshiProgressList[keshiInfo[keshiId]]["state"]=1
    
    keshiProgressList.sort(key= lambda x:x["state"], reverse=True)

    return jsonify(code=RET.OK, flag=True, message='获取科室分配进度信息成功',data=keshiProgressList)


# 获取项目成员分配情况
@group_blue.route('/getmemberdetail', methods=['POST'])
@authorize
def getMemberDetail(): 
    planId = request.form.get('planId')
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')
    keshiId = request.form.get('keshiId')
    keshi_manager = KeshiModel.query.get(keshiId).manager

    memberInfo = UsersModel.query.filter_by(keshi=keshiId).all()
    
    memberDetailList = []

    for member in memberInfo:
        # if(member.id==keshi_manager): continue
        # print(member.bonus_category)
        if(member.bonus_category=="固定发放"): continue
        if(member.category==15): continue

        username = member.username + '(' + member.wage_category + ')'

        memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=member.id).first()
        if(memberdetail is None):
            memberDetailList.append({"userId":member.id, "username":username, "user_category":member.wage_category,"position":member.position,"bonus_category":member.bonus_category,"amount":0})
        else:
            memberDetailList.append({"userId":member.id, "username":username, "user_category":member.wage_category,"position":member.position,"bonus_category":member.bonus_category, "amount":memberdetail.amount})
    
    return jsonify(code=RET.OK, flag=True, message='获取该项目成员详细信息成功', data=memberDetailList)

# 获取项目成员分配情况
@group_blue.route('/exportmemberdetail', methods=['POST'])
@authorize
def exportMemberDetail(): 
    planId = request.form.get('planId')
    projectId =request.form.get('projectId')
    projectType =request.form.get('projectType')
    keshiId = request.form.get('keshiId')
    keshi = KeshiModel.query.get(keshiId)

    memberInfo = UsersModel.query.filter_by(keshi=keshiId).all()
    
    memberDetailList = []
    memberDetailList.append(["室","姓名","身份证号","类别","工资总额类别","奖金库","岗位","备注","金额"])

    for member in memberInfo:
        if(member.bonus_category=="固定发放"): continue
        if(member.category==15): continue
        category = CategoryModel.query.get(member.category).name

        memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=member.id).first()
        if(memberdetail is None):
            memberDetailList.append([keshi.name, member.username,member.idnum,category, member.wage_category, member.bonus_category, member.position, member.remarks, 0])
        else:
            memberDetailList.append([keshi.name, member.username,member.idnum,category, member.wage_category, member.bonus_category, member.position, member.remarks, float(memberdetail.amount)])
    
    return jsonify(code=RET.OK, flag=True, message='导出该项目成员详细信息成功', data=memberDetailList)




# 修改科室成员分配情况
@group_blue.route('/changememberdetail', methods=['POST'])
@authorize
def changeMemberDetail(): 
    keshiDetailId = request.json.get('keshiDetailId')
    planId = request.json.get('planId')
    projectId = request.json.get('projectId')
    projectType = request.json.get('projectType')
    memberdetail = request.json.get('memberDetailList')

    zhan_total = 0
    buzhan_total = 0

    for info in memberdetail:
        if(info['amount']=='' or info['amount']==0):
            detail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=info['userId']).first()
            if(detail):
                detail.delete(detail.id)
        else:
            if(info['user_category']=='占工资总额'): zhan_total += Decimal(info['amount'])
            else: buzhan_total += Decimal(info['amount'])

            detail = UserDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=info['userId']).first()
            if(detail):
                if(detail.amount!=Decimal(info['amount'])):
                    detail.amount = info['amount']
                    detail.update()
            else:
                newdetail = UserDetailModel(planId=planId, projectId=projectId, projectType=projectType, userId=info['userId'], amount=info['amount'])
                result = UserDetailModel.add(UserDetailModel, newdetail) 
    
    # TODO bonusdetail 的下面三项组成的只能有一个
    bonusdetail = BonusDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType).first()
    if(projectType==0):
        keshidetail = KeshiDetailModel.query.get(keshiDetailId)
        bonusdetail.amount_zhan -= keshidetail.amount_zhan
        bonusdetail.amount_buzhan -= keshidetail.amount_buzhan
        bonusdetail.amount_zhan += zhan_total
        bonusdetail.amount_buzhan += buzhan_total
        bonusdetail.update()
        keshidetail.amount_zhan = zhan_total
        keshidetail.amount_buzhan = buzhan_total
        keshidetail.update()
    else:
        bonusdetail.amount_zhan = zhan_total
        bonusdetail.amount_buzhan = buzhan_total
        bonusdetail.update()

    return jsonify(code=RET.OK, flag=True, message='修改项目成员详细分配金额成功')

# 导入科室成员分配情况
@group_blue.route('/importmemberdetail', methods=['POST'])
@authorize
def importMemberDetail(): 
    form = request.json.get('form')

    keshiDetailId = form['keshiDetailId']
    planId = form['planId']
    projectId = form['projectId']
    projectType = form['projectType']

    rows = request.json.get('rows')

    zhan_total = 0
    buzhan_total = 0

    for row in rows:
        user = UsersModel.query.filter_by(idnum=row['身份证号']).first()
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
    
    bonusdetail = BonusDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType).first()
    if(projectType==0):
    # TODO bonusdetail 的下面三项组成的只能有一个
        keshidetail = KeshiDetailModel.query.get(keshiDetailId)
        bonusdetail.amount_zhan -= keshidetail.amount_zhan
        bonusdetail.amount_buzhan -= keshidetail.amount_buzhan
        bonusdetail.amount_zhan += zhan_total
        bonusdetail.amount_buzhan += buzhan_total
        bonusdetail.update()
        keshidetail.amount_zhan = zhan_total
        keshidetail.amount_buzhan = buzhan_total

        keshidetail.update()
    else:
        bonusdetail.amount_zhan = zhan_total
        bonusdetail.amount_buzhan = buzhan_total
        bonusdetail.update()

    return jsonify(code=RET.OK, flag=True, message='修改项目成员详细分配金额成功')


# 获取该科室每个人每个项目分多少钱的总体信息
@group_blue.route('/getkeshidetail/<int:planId>', methods=['GET'])
@authorize
def getKeshiAllDetail(planId): 
    userId = session.get('userid')
    keshi = KeshiModel.query.filter_by(manager=userId).first()
    allMember = UsersModel.query.filter_by(keshi=keshi.id).all()

    memberDetailList = []
    projectList = []
    projectTmp = set()

    for member in allMember:
        if(member.bonus_category=="固定发放"): continue
        if(member.category==15): continue
        category = CategoryModel.query.get(member.category).name

        memberdict = {"userId":member.id,"department":member.department,"keshi":keshi.name,"username":member.username,
            "idnum":member.idnum+"\u200b","category":category,"wage_category":member.wage_category,"position":member.position,
            "remarks":member.remarks,"bonus_category":member.bonus_category}
       
        memberdetail = UserDetailModel.query.filter_by(planId=planId, userId=member.id).all()
        
        total = 0
        for detail in memberdetail:
            key = str(detail.projectId)+'_'+str(detail.projectType)
            memberdict[key] = detail.amount
            total += detail.amount

            history = DetailHistoryModel.query.filter_by(planId=planId,projectId=detail.projectId,projectType=detail.projectType,userId=member.id).first()
            if(history is None):
                memberdict[key+"flag"] = False
                # memberdict[key] = [detail.amount,False]
            else:
                memberdict[key+"flag"] = True
                # memberdict[key] = [detail.amount,True]

            if(key not in projectTmp):
                projectTmp.add(key)
                if(detail.projectType==0): 
                    pro = ResearchModel.query.get(detail.projectId)
                    name = pro.number + ": "+ pro.name
                else: name = ManageModel.query.get(detail.projectId).name
                projectList.append({"id":key,"name":name})
        
        memberdict['total'] = total
        memberDetailList.append(memberdict)
    
    resProjectDetail = KeshiDetailModel.query.filter_by(planId=planId,keshiId=keshi.id).all()
    for keshidetail in resProjectDetail:
        key = str(keshidetail.projectId)+'_'+str(keshidetail.projectType)
        if(key not in projectTmp):
            projectTmp.add(key)
            name = ResearchModel.query.get(keshidetail.projectId).name
            projectList.append({"id":key,"name":name})
    
    manProjects = ManageModel.query.filter_by(manager=userId)
    for pro in manProjects:
        detail = BonusDetailModel.query.filter_by(planId=planId, projectId=pro.id, projectType=1).first()
        if(detail is not None):
            key = str(detail.projectId)+'_'+str(detail.projectType)
            if(key not in projectTmp):
                projectTmp.add(key)
                name = ManageModel.query.get(detail.projectId).name
                projectList.append({"id":key,"name":name})
        

    return jsonify(code=RET.OK, flag=True, message='获取该次计划本室分配信息成功',detail=memberDetailList,project=projectList)


# 获取项目成员历史分配情况
@group_blue.route('/gethistory', methods=['POST'])
@authorize
def getMemberHistory(): 
    userId = request.form.get('userId')
    planId = request.form.get('planId')
    project =request.form.get('project')
    projectId = project.split('_')[0]
    projectType = project.split('_')[1]

    historydetail = DetailHistoryModel.query.filter_by(planId=planId, projectId=projectId, projectType=projectType, userId=userId).all()
    historyList = []

    for history in historydetail:
        historyList.append({"amount":history.amount, "time":history.time})


    return jsonify(code=RET.OK, flag=True, message='获取该项目成员历史分配', data=historyList)

# 获取科室成员信息
@group_blue.route('/getkeshimember/<int:keshiId>', methods=['GET'])
@authorize
def getKeshiMember(keshiId): 
    memberInfo = UsersModel.query.filter_by(keshi=keshiId).all()
    keshi = KeshiModel.query.get(keshiId)
    
    memberList = []
    # memberDetailList.append(["部门","室","姓名","身份证号","类别","工资总额类别","奖金库","岗位","金额"])

    for member in memberInfo:
        if(member.bonus_category=="固定发放"): continue
        if(member.category==15): continue
        category = CategoryModel.query.get(member.category).name
        memberList.append([keshi.name, member.username,member.idnum, category, member.wage_category, member.bonus_category, member.position, member.remarks])

    return jsonify(code=RET.OK, flag=True, message='获取科室成员详细信息成功', data=memberList)


# 导入科室成员全部项目分配情况
@group_blue.route('/importkeshidetail', methods=['POST'])
@authorize
def importKeshiDetail(): 
    form = request.json.get('form')

    keshiId = form['keshiId']
    planId = form['planId']

    # keshiDetailId = form['keshiDetailId']
    # planId = form['planId']
    # projectId = form['projectId']
    # projectType = form['projectType']
    rows = request.json.get('rows')
    proDetailList = request.json.get('proDetailList')


    for pro in proDetailList:
        zhan_total = 0
        buzhan_total = 0
        for row in rows:
            user = UsersModel.query.filter_by(idnum=row['身份证号']).first()
            if(row.get(pro['projectName'])==0 or row.get(pro['projectName'])==None):
                memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=pro['projectId'], projectType=pro['projectType'], userId=user.id).first()
                if(memberdetail):
                    memberdetail.delete(memberdetail.id)
            else:
                if(row['工资总额类别']=='占工资总额'): zhan_total += Decimal(row[pro['projectName']])
                else: buzhan_total += Decimal(row[pro['projectName']])

                memberdetail = UserDetailModel.query.filter_by(planId=planId, projectId=pro['projectId'], projectType=pro['projectType'], userId=user.id).first()
                if(memberdetail):
                    if(memberdetail.amount!=row[pro['projectName']]):
                        memberdetail.amount = row[pro['projectName']]
                        memberdetail.update()
                else:
                    newdetail = UserDetailModel(planId=planId, projectId=pro['projectId'], projectType=pro['projectType'], userId=user.id, amount=row[pro['projectName']])
                    result = UserDetailModel.add(UserDetailModel, newdetail) 
        
        bonusdetail = BonusDetailModel.query.filter_by(planId=planId, projectId=pro['projectId'], projectType=pro['projectType']).first()
        if(pro['projectType']==0):

            keshidetail = KeshiDetailModel.query.filter_by(planId=planId, projectId=pro['projectId'], projectType=pro['projectType'], keshiId=keshiId).first()
            bonusdetail.amount_zhan -= keshidetail.amount_zhan
            bonusdetail.amount_buzhan -= keshidetail.amount_buzhan
            bonusdetail.amount_zhan += zhan_total
            bonusdetail.amount_buzhan += buzhan_total
            bonusdetail.update()
            keshidetail.amount_zhan = zhan_total
            keshidetail.amount_buzhan = buzhan_total
            keshidetail.update()
        else:
            bonusdetail.amount_zhan = zhan_total
            bonusdetail.amount_buzhan = buzhan_total
            bonusdetail.update()

    return jsonify(code=RET.OK, flag=True, message='导入科室成员全部项目详细分配金额成功')
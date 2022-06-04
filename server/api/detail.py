from flask import g, current_app, jsonify, request, session

from utils.response_code import RET

from . import detail_blue
from . import authorize
from models.user import UsersModel
from models.manage import ManageModel
from models.research import ResearchModel
from models.bonusplan import BonusPlanModel
from models.koufa import KoufaModel

from models.bonusdetail import BonusDetailModel
import uuid

# 获取科研项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/getresprojectdetail/<int:planId>', methods=['GET'])
@authorize
def getResProjectDetailList(planId): 
    detailInfo = BonusDetailModel.query.filter_by(planId=planId, projectType=0).all()
    
    detailList = []
    for detail in detailInfo:
        projectInfo = ResearchModel.query.get(detail.projectId)
        detailList.append({"id":detail.id,"name":projectInfo.name,"amount":detail.amount,"amount_zhan":detail.amount_zhan,"amount_buzhan":detail.amount_buzhan})
    
    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配信息成功', data=detailList)

# 用于导出科研项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/getallresprojectdetail/<int:planId>', methods=['GET'])
@authorize
def getAllResProjectDetailList(planId): 
    allProject = ResearchModel.query.filter_by(state="进行中").all()
    allProDetailList = []
    allProDetailList.append(["所级项目编号","项目名称","项目经理","金额"])

    for pro in allProject:
        detailInfo = BonusDetailModel.query.filter_by(planId=planId, projectType=0, projectId=pro.id).first()
        manager = UsersModel.query.get(pro.manager).username
        if(detailInfo is None):
            allProDetailList.append([pro.number,pro.name,manager,0])
        else:
            allProDetailList.append([pro.number,pro.name,manager,detailInfo.amount])
       
    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配模板成功', data=allProDetailList)


# 获取管理项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/getmanprojectdetail/<int:planId>', methods=['GET'])
@authorize
def getManProjectDetailList(planId): 
    detailInfo = BonusDetailModel.query.filter_by(planId=planId, projectType=1).all()
    
    detailList = []
    for detail in detailInfo:
        projectInfo = ManageModel.query.get(detail.projectId)
        detailList.append({"id":detail.id,"name":projectInfo.name,"amount":detail.amount,"amountb":detail.amount_b,"amount_zhan":detail.amount_zhan,"amount_buzhan":detail.amount_buzhan})
    
    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配信息成功', data=detailList)

# 用于导出管理项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/getallmanprojectdetail/<int:planId>', methods=['GET'])
@authorize
def getAllManProjectDetailList(planId): 
    allProject = ManageModel.query.filter_by(state="进行中").all()
    allProDetailList = []
    allProDetailList.append(["项目名称","金额（占工资总额）","金额（不占工资总额）"])

    for pro in allProject:
        detailInfo = BonusDetailModel.query.filter_by(planId=planId, projectType=1, projectId=pro.id).first()
        if(detailInfo is None):
            allProDetailList.append([pro.name,0,0])
        else:
            allProDetailList.append([pro.name,detailInfo.amount,detailInfo.amount_b])
       
    return jsonify(code=RET.OK, flag=True, message='获取该次方法计划分配模板成功', data=allProDetailList)


# 增加一条科研项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/createresdetail', methods=['POST'])
@authorize
def createResProjectDetail(): 
    planId = request.json.get('planId')
    projectId = request.json.get('projectId')
    amount = request.json.get('amount')

    projectInfo = ResearchModel.query.get(projectId)
    if (projectInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该科研项目不存在')

    planInfo = BonusPlanModel.query.get(planId)
    if (planInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该发放计划不存在')

    detail = BonusDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=0).first()
    if (detail):
        return jsonify(code=RET.NODATA, flag=False, message='该项目奖金包已分配')

    detail = BonusDetailModel(planId=planId, projectId=projectId, projectType=0, amount=amount)

    result = BonusDetailModel.add(BonusDetailModel, detail)

    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='新增项目奖金包分配信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增项目奖金包分配信息失败')

# 导入科研项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/importresdetail', methods=['POST'])
@authorize
def createResProjectDetailFromFile(): 
    planId = request.json.get('planId')
    rows = request.json.get('rows')

    for row in rows:
        projectId = ResearchModel.query.filter_by(number=row['所级项目编号']).first().id
        if(row.get('金额')==0 or row.get('金额')==None):
            detail = BonusDetailModel.query.filter_by(planId=planId, projectType=0, projectId=projectId).first()
            if(detail):
                detail.delete(detail.id)
        else:
            detail = BonusDetailModel.query.filter_by(planId=planId, projectType=0, projectId=projectId).first()
            if(detail):
                if(detail.amount!=row['金额']):
                    detail.amount = row['金额']
                    detail.update()
            else:
                detail = BonusDetailModel(planId=planId, projectId=projectId, projectType=0, amount=row['金额'])
                result = BonusDetailModel.add(BonusDetailModel, detail)

    return jsonify(code=RET.OK, flag=True, message='导入分配模板成功')

# 导入管理项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/importmandetail', methods=['POST'])
@authorize
def createManProjectDetailFromFile(): 
    planId = request.json.get('planId')
    rows = request.json.get('rows')

    for row in rows:
        projectId = ManageModel.query.filter_by(name=row['项目名称']).first().id
        if((row.get('金额（占工资总额）')==0 or row.get('金额（占工资总额）')==None) and (row.get('金额（不占工资总额）')==0 or row.get('金额（不占工资总额）')==None)):
            detail = BonusDetailModel.query.filter_by(planId=planId, projectType=1, projectId=projectId).first()
            if(detail):
                detail.delete(detail.id)
        else:
            detail = BonusDetailModel.query.filter_by(planId=planId, projectType=1, projectId=projectId).first()
            if(detail):
                detail.amount = row['金额（占工资总额）']
                detail.amountb = row['金额（不占工资总额）']
                detail.update()
            else:
                detail = BonusDetailModel(planId=planId, projectId=projectId, projectType=1, amount=row['金额（占工资总额）'], amount_b=row['金额（不占工资总额）'])
                result = BonusDetailModel.add(BonusDetailModel, detail)

    return jsonify(code=RET.OK, flag=True, message='导入分配模板成功')



# 增加一条管理项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/createmandetail', methods=['POST'])
@authorize
def createManProjectDetail(): 
    planId = request.json.get('planId')
    projectId = request.json.get('projectId')
    amount = request.json.get('amount')
    amountb = request.json.get('amountb')

    projectInfo = ManageModel.query.get(projectId)
    if (projectInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该管理项目不存在')

    planInfo = BonusPlanModel.query.get(planId)
    if (planInfo is None):
        return jsonify(code=RET.NODATA, flag=False, message='该发放计划不存在')

    detail = BonusDetailModel.query.filter_by(planId=planId, projectId=projectId, projectType=1).first()
    if (detail):
        return jsonify(code=RET.NODATA, flag=False, message='该项目奖金包已分配')

    detail = BonusDetailModel(planId=planId, projectId=projectId, projectType=1, amount=amount)
    detail.amount_b = amountb

    result = ManageModel.add(ManageModel, detail)

    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='新增项目奖金包分配信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增项目奖金包分配信息失败')


# 修改一条项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/changedetail', methods=['POST'])
@authorize
def changeProjectDetail(): 
    id = request.json.get('id')
    amount = request.json.get('amount')
    amountb = request.json.get('amountb')

    detail = BonusDetailModel.query.get(id)
    if (detail is None):
        return jsonify(code=RET.NODATA, flag=False, message='该条信息不存在')
    
    detail.amount = amount
    detail.amount_b = amountb
    detail.update()


    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='修改项目奖金包分配信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='修改项目奖金包分配信息失败')


# 删除一条项目奖金包分配（每个项目分多少）的信息
@detail_blue.route('/del/<int:id>', methods=['DELETE'])
@authorize
def delProjectDetail(id): 
    detail = BonusDetailModel.query.get(id)
    if (detail is None):
        return jsonify(code=RET.NODATA, flag=False, message='该条信息不存在')
    detail.delete(id)
    return jsonify(code=RET.OK, flag=True, message='删除项目奖金包分配信息成功')

# 获取人员扣发信息
@detail_blue.route('/getkoufadetail/<int:planId>', methods=['GET'])
@authorize
def getKoufaDetailList(planId): 
    detailInfo = KoufaModel.query.filter_by(planId=planId).all()
    detailList = []

    for detail in detailInfo:
        userInfo = UsersModel.query.get(detail.userId)
        detailList.append({"id":detail.id,"userId":detail.userId,"username":userInfo.username,"amount":detail.amount,"remark":detail.remark})
    
    return jsonify(code=RET.OK, flag=True, message='获取该次计划扣发信息成功', data=detailList)

# 增加一条扣发的信息
@detail_blue.route('/createkoufadetail', methods=['POST'])
@authorize
def createKoufaDetail(): 
    planId = request.json.get('planId')
    username = request.json.get('username')
    amount = request.json.get('amount')
    remark = request.json.get('remark')

    user = UsersModel.query.filter_by(username=username).first()
    if (user is None):
        return jsonify(code=RET.NODATA, flag=False, message='该姓名不存在')

    detail = KoufaModel.query.filter_by(userId=user.id).all()
    if (detail):
        return jsonify(code=RET.NODATA, flag=False, message='该人员已被扣发')

    detail = KoufaModel(planId=planId, userId=user.id, amount=amount, remark=remark)
    result = KoufaModel.add(KoufaModel, detail)

    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='新增扣发信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='新增扣发信息失败')


# 修改一条扣发信息
@detail_blue.route('/changekoufadetail', methods=['POST'])
@authorize
def changeKoufaDetail(): 
    id = request.json.get('id')
    amount = request.json.get('amount')
    remark = request.json.get('remark')

    detail = KoufaModel.query.get(id)
    if (detail is None):
        return jsonify(code=RET.NODATA, flag=False, message='该条信息不存在')
    
    detail.amount = amount
    detail.remark = remark
    detail.update()


    if detail.id:
        return jsonify(code=RET.OK, flag=True, message='修改扣发信息成功')
    else:
        return jsonify(code=RET.DBERR, flag=False, message='修改扣发信息失败')

# 删除一条扣发信息
@detail_blue.route('/delkoufa/<int:id>', methods=['DELETE'])
@authorize
def delKoufaxDetail(id): 
    detail = KoufaModel.query.get(id)
    if (detail is None):
        return jsonify(code=RET.NODATA, flag=False, message='该条信息不存在')
    detail.delete(id)
    return jsonify(code=RET.OK, flag=True, message='删除扣发信息成功')

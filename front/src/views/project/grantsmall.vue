<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlan" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%">
            <el-option v-for="item in planList" :label="item.name" :key="item.id" :value="item.id"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="fetchMyProject()">选择</el-button>
    </div>


    <el-table
      :data="proDetailList"
      :row-style="{height:40+'px'}"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="projectName"
        label="项目名称"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="projectType"
        label="项目类型"
        :formatter="formatter"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="amount"
        label="占工资总额奖金包"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="amountb"
        label="不占工资总额奖金包(A类/B类/研究生)"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="amount_zhan"
        label="已发占工资总额"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="amount_buzhan"
        label="已发不占工资总额"
        min-width="15%">
      </el-table-column>

      <el-table-column
        label="操作"
        min-width="6%">
        <template slot-scope="scope">
          <el-button @click.native.stop="openWrite(scope.row)" type="text" size="small">填写</el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        min-width="6%">
        <template slot-scope="scope">
          <el-button @click.native.stop="openManage(scope.row)" type="text" size="small">管理</el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        min-width="10%">
        <template slot-scope="scope">
          <el-button @click.native.stop="exportTemp(scope.row)" type="text" size="small">导出模板</el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        min-width="10%">
        <template slot-scope="scope">
            <el-upload
                action="aaa"
                accept=".xlsx"
                :multiple="false"
                :auto-upload="false"
                :on-change="importTemp"
                :show-file-list="false"
                :file-list="fileList">
                <el-button @click="curRowIndex=scope.$index" type="text" size="small">导入模板</el-button>
                <!-- <el-button type="warning" icon="el-icon-upload2" >模板导入</el-button> -->
            </el-upload>
        </template>
      </el-table-column>

    </el-table>
    
    <!-- 人员管理弹出窗口 -->
    <el-dialog
      title="项目人员管理"
      :visible.sync="manageVisible"
      width="60%"
      >

      <el-form label-width="50px" >  
        <el-form-item label="姓名">
            <el-col :span="12">
                <el-input v-model="newMember" placeholder="成员姓名"></el-input>
            </el-col>
            <el-button @click="handleAddMember()" type="warning" size="small" style="margin-left:2%">新增</el-button>
        </el-form-item>
      </el-form>
      

      <el-table
      :data="memberList"
      :row-style="{height:40+'px'}"
      style="width:100%;margin-top:2%">

      <el-table-column
        prop="keshi" label="科室" min-width="10%">
      </el-table-column>

      <el-table-column
        prop="username" label="姓名" min-width="10%">
      </el-table-column>

      <el-table-column
        prop="idnum" label="身份证号" min-width="10%">
      </el-table-column>

      <el-table-column
        prop="category" label="类别" min-width="10%">
      </el-table-column>

      <el-table-column
        prop="wage_category" label="工资总额类别" min-width="10%">
      </el-table-column>

      <el-table-column
        prop="position" label="岗位" min-width="10%">
      </el-table-column>

      <el-table-column
        prop="bonus_category" label="奖金库" min-width="10%">
      </el-table-column>

      <el-table-column
        label="操作"
        min-width="6%">
        <template slot-scope="scope">
          <el-button @click.native.stop="delMember(scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>

       </el-table>

    </el-dialog>


    <!-- 人员分配奖金弹出窗口 -->
    <el-dialog
      title="奖金分配"
      :visible.sync="writeVisible"
      width="50%"
      >
        <el-form label-width="120px" >  
            <el-form-item
                v-for="(item,index) in memberDetailForm.memberDetailList"
                :key="index"
                :label="item.username"
            >
            <el-input v-model="item.amount" clearable></el-input>
            </el-form-item>
        </el-form>
        <el-button @click="handleWrite()" type="warning" size="small">提交</el-button>
    </el-dialog>

  </div>



</template>
<script>
import generalApi from '@/api/general'
import projectApi from '@/api/project'
import XLSX from 'xlsx'
import FileSaver from 'file-saver'

export default {
    data(){
        return {
            planList: [],
            proDetailList: [], 
            chosenPlan: '',
            curChosenPlan: '',
            projectList: [],
            manageVisible: false,
            memberList: [], 
            curRow: {},
            newMember: '',
            writeVisible: false,
            memberDetailForm:{
                bonusId: '',
                planId: '',
                projectId: '',
                projectType: '',
                memberDetailList:[{
                    userId: '',
                    username: '',
                    amount: '' ,
                    user_category: '',
                }]
            },
            exportList:[],
            curRowIndex: null,
            fileList: []
        }
    },
    created () {
        this.fetchPlanList()
    },
    methods: {
        fetchPlanList(){
            generalApi.getProPlanList().then(response =>{
                this.planList = response.data;
            }).catch((err) => {
                this.planList = []
            });
        },

        fetchMyProject(){
            if(this.chosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }
            this.curChosenPlan = this.chosenPlan
            projectApi.getMySmallProjectList(this.curChosenPlan).then(response =>{
                this.proDetailList = response.data;
            }).catch((err) => {
                this.proDetailList = []
            });
        },

        openWrite(row){
            let formData = new FormData();
            formData.append('planId', this.curChosenPlan)
            formData.append('projectId', row.projectId)
            formData.append('projectType',row.projectType)
            
            projectApi.getMemberDetail(formData).then(response =>{
                this.memberDetailForm.memberDetailList = response.data;
                console.log(this.memberDetailForm.memberDetailList)
            }).catch((err) => {
                this.memberDetailForm.memberDetailList = []
            });

            this.writeVisible = true
            this.curRow = row
        },

        handleWrite(){
            // console.log(this.memberDetailList)
            // console.log(this.curRow)
            let total = 0
            let totalb = 0
            let flag0 = false
            let flag1 = false
            let flag2 = false
            if(this.curRow.projectType==0){
                this.memberDetailForm.memberDetailList.forEach((member, index) => {
                    if(member.category==15){
                        flag2 = true
                        return
                    }
                    if(member.bonus_category=='管理' || member.bonus_category=='固定发放' || member.position == 'A类' || member.position == 'B类'){
                        if(parseFloat(member.amount) >0 ){
                            flag0 = true
                            return
                        }
                    }
                    if(member.user_category=='占工资总额'){
                        if(member.amount == '') total += 0
                        else total += parseFloat(member.amount)
                    }
                })
            }else{
                this.memberDetailForm.memberDetailList.forEach((member, index) => {
                    if(member.category==15){
                        flag2 = true
                        return
                    }
                    if(member.bonus_category=='科研' || member.bonus_category=='固定发放' || member.position == 'C类'){
                        if(parseFloat(member.amount) >0 ){
                            flag1 = true
                            return
                        }
                    }
                    if(member.user_category=='占工资总额'){
                        if(member.amount == '') total += 0
                        else total += parseFloat(member.amount)
                    }else{
                        if(member.amount == '') totalb += 0
                        else totalb += parseFloat(member.amount)
                    }
                })
            }

            if(flag2){
                this.$message.error('离职人员不能发放奖金')
                return false
            }

            if(flag0){
                this.$message.error('科研项目不能发放给奖金库为管理或固定发放及A类、B类的人员')
                return false
            }

            if(flag1){
                this.$message.error('管理项目不能发放给奖金库为科研或固定发放及C类的人员')
                return false
            }

            if(total-this.curRow.amount>0.00001 || this.curRow.amount-total>0.00001){
                this.$message.error('已分发总额(占工资)与奖金包不相等')
                return false
            }

            if(totalb - this.curRow.amountb > 0.00001){
                this.$message.error('已分发总额(不占工资总额)超过奖金包')
                return false
            }

            this.memberDetailForm.bonusId = this.curRow.bonusId
            this.memberDetailForm.planId = this.curChosenPlan
            this.memberDetailForm.projectId = this.curRow.projectId
            this.memberDetailForm.projectType = this.curRow.projectType
            // this.memberDetailForm.memberList = this.memberDetailList
            projectApi.changeMemberDetail(this.memberDetailForm).then(response =>{
                this.closeWrite()
            })
        },

        closeWrite(){
            this.memberDetailForm.memberDetailList=[]
            this.writeVisible = false
            this.fetchMyProject()
        },

        formatter(row, column) {
          return row[column.property]==0?'科研项目':'管理项目'
        },

        openManage(row){
            let formData = new FormData();
            formData.append('projectId', row.projectId)
            formData.append('projectType',row.projectType)

            projectApi.getProjectMember(formData).then(response =>{
                this.memberList = response.data;
                this.manageVisible = true
                this.curRow = row
            }).catch((err) => {
                this.memberList = []
            });  
        },

        handleAddMember(){
            if(this.newMember==''){
                this.$message.error('请填写姓名')
                return false
            }
            let formData = new FormData();
            formData.append('projectId', this.curRow.projectId)
            formData.append('projectType',this.curRow.projectType)
            formData.append('username',this.newMember)
            
            projectApi.addMember(formData).then(response =>{
                if(!response.flag) {
                    this.$message.error(response.message)
                }
                this.newMember=''
            })
        },

        closeManage(){
            this.newMember=''
            this.memberList = []
            this.manageVisible = false
        },


        delMember(row){
            projectApi.delMember(row.id,this.curChosenPlan).then(response =>{
                // this.closeManage()
                this.openManage(this.curRow)
            })
        },

        exportTemp(row){
            let formData = new FormData();
            formData.append('planId', this.curChosenPlan)
            formData.append('projectId', row.projectId)
            formData.append('projectType',row.projectType)
            
            projectApi.getMemberDetailExport(formData).then(response =>{
                this.exportList = response.data;
                console.log(this.exportList)
                
                var ws = XLSX.utils.aoa_to_sheet(this.exportList)
                var wb = XLSX.utils.book_new()
                XLSX.utils.book_append_sheet(wb, ws, "sheet");
                let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
                
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), row.projectName+'-项目经理导出模板.xlsx')
                } catch (e) { 
                    if (typeof console !== 'undefined') console.log(e, wbout) 
                }

            }).catch((err) => {
                this.exportList = []
            });
        },

        importTemp(file, fileList){
            if (fileList.length > 0) {
                this.fileList = [fileList[fileList.length - 1]] // 这一步，是展示最后一次选择的文件
            }
            // console.log(this.fileList)

            this.$confirm('确认导入该模板', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                var reader = new FileReader();

                var vm = this
                reader.onload = function (e) {
                    var workbook = XLSX.read(e.target.result, {
                        type: 'binary'
                    });
                    var Sheet = workbook.SheetNames[0];
                    var excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[Sheet]);


                    // 1. 判断金额对不对
                    let total = 0
                    let totalb = 0
                    let flag0 = false
                    let flag1 = false
                    let flag2 = false
                    let row = vm.proDetailList[vm.curRowIndex]

                    if(row.projectType==0){
                        excelRows.forEach((member, index) => {
                            if(member['类别']=='离职（不发放）'){
                                flag2 = true
                                return
                            }
                            if(member['奖金库']=='管理' || member['奖金库']=='固定发放' || member['岗位'] == 'A类' || member['岗位'] == 'B类'){
                                if(parseFloat(member['金额']) >0 ){
                                    flag0 = true
                                    return
                                }
                            }
                            if(member['工资总额类别']=='占工资总额'){
                                if(typeof(member['金额'])=="undefined" || member['金额'] == 0) total += 0
                                else total += parseFloat(member['金额'])
                            }
                        })
                    }else{
                        excelRows.forEach((member, index) => {
                            if(member['类别']=='离职（不发放）'){
                                flag2 = true
                                return
                            }
                            if(member['奖金库']=='科研' || member['奖金库']=='固定发放' || member['岗位'] == 'C类'){
                                if(parseFloat(member['金额']) >0 ){
                                    flag1 = true
                                    return
                                }
                            }
                            if(member['工资总额类别']=='占工资总额'){
                                if(typeof(member['金额'])=="undefined" || member['金额'] == 0) total += 0
                                else total += parseFloat(member['金额'])
                            }else{
                                // if(member['岗位']=='B类'){
                                //     if(typeof(member['金额'])=="undefined" || member['金额'] == 0) totalb += 0
                                //     else totalb += parseFloat(member['金额'])
                                // }
                                if(typeof(member['金额'])=="undefined" || member['金额'] == 0) totalb += 0
                                else totalb += parseFloat(member['金额'])
                            }
                        })
                    }
                    if(flag2){
                        this.$message.error('离职人员不能发放奖金')
                        return false
                    }

                    if(flag0){
                        this.$message.error('科研项目不能发放给奖金库为管理或固定发放及A类、B类的人员')
                        return false
                    }

                    if(flag1){
                        this.$message.error('管理项目不能发放给奖金库为科研或固定发放及C类的人员')
                        return false
                    }

                    if(total-row.amount>0.00001 || row.amount-total>0.00001){
                        vm.$message.error('已分发总额(占工资)与奖金包不相等')
                        return false
                    }

                    if(totalb - row.amountb > 0.00001){
                        vm.$message.error('已分发总额(不占工资总额)超过奖金包')
                        return false
                    }


                    // 2. 传到后端
                    var form = {"bonusId":row.bonusId,"planId":vm.curChosenPlan,"projectId":row.projectId,"projectType":row.projectType}

                    projectApi.importMemberDetail(form,excelRows).then(response =>{
                        if(response.flag){//如果成功
                            vm.$message.success(response.message)
                            vm.fetchMyProject()
                        }
                        
                    })
                    // console.log(excelRows)
                };
                reader.readAsBinaryString(this.fileList[0].raw);
            })
        }

    },
}
      
</script>

<style rel="stylesheet/scss" lang="scss">
.el-dialog {
  // // transform: translateY(-50%);
  // //border-radius: 10px;
  // // width: 500px;
  // // height: 500px!important;
  .el-dialog__header{  
    background: #f7f7f7;
    text-align: left;   
    font-weight: 600;
  }
}
.el-table--enable-row-hover .el-table__body tr:hover>td{
	background-color: rgba(185,211,249,0.75);
}
</style>
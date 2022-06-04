<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlanIndex" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%">
            <el-option v-for="(item,index) in planList" :label="item.name" :key="index" :value="index"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="fetchKeshiProject()">选择</el-button>
        <el-button type="info" icon="el-icon-download" @click="exportTempAll">模板导出</el-button>
    </div>

    <el-col :span="12" style="margin-left:5%;margin-top:1%">
      <el-upload
        v-if="curChosenPlanState==='室主任发放中'"
        action="aaa"
        accept=".xlsx"
        :multiple="false"
        :auto-upload="false"
        :on-change="handleUploadChange"
        :file-list="tempList">
        <el-button type="warning" icon="el-icon-upload2" >模板导入</el-button>
      </el-upload>
    </el-col>


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
        min-width="17%">
      </el-table-column>

      <el-table-column
        prop="amount_zhan"
        label="已发占工资总额"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="amount_buzhan"
        label="已发不占工资总额"
        min-width="20%">
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
        min-width="10%">
        <template slot-scope="scope">
          <el-button @click.native.stop="exportTemp(scope.row)" type="text" size="small">导出模板</el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        v-if="curChosenPlanState==='室主任发放中'"
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
    

    <!-- 人员分配奖金弹出窗口 -->
    <el-dialog
      title="奖金分配"
      :visible.sync="writeVisible"
      width="50%"
      >
        <el-form label-width="150px" >  
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
import groupApi from '@/api/group'
import XLSX from 'xlsx'
import FileSaver from 'file-saver'

export default {
    data(){
        return {
            planList: [],
            proDetailList: [], 
            chosenPlanIndex: '',
            curChosenPlan: '',
            curChosenPlanState: '',
            keshiId: '',
            keshiType: '',
            curRow: {},
            writeVisible: false,
            memberDetailForm:{
                keshiDetailId :'',
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
            fileList: [],
            tempList: [],
            keshiMember: []
        }
    },
    created () {
        this.fetchPlanList()
    },
    methods: {
        fetchPlanList(){
            generalApi.getShiPlanList().then(response =>{
                this.planList = response.data;
            }).catch((err) => {
                this.planList = []
            });
        },

        fetchKeshiProject(){
            if(this.chosenPlanIndex===''){
                this.$message.error('请选择发放计划')
                return false
            }
            this.curChosenPlan = this.planList[this.chosenPlanIndex].id
            this.curChosenPlanState = this.planList[this.chosenPlanIndex].state
            groupApi.getKeshiProjectList(this.curChosenPlan).then(response =>{
                this.proDetailList = response.data;
                this.keshiId = response.keshiId
                this.keshiType = response.keshiType
                // console.log(this.proDetailList)
            }).catch((err) => {
                this.proDetailList = []
                this.keshiId = ''
            });
        },

        openWrite(row){
            if(this.curChosenPlanState==='项目经理发放中' && row.projectType==0){
                this.$message.error('科研项目暂时无法填写')
                return false
            }

            let formData = new FormData();
            formData.append('planId', this.curChosenPlan)
            formData.append('projectId', row.projectId)
            formData.append('projectType',row.projectType)
            formData.append('keshiId',this.keshiId)
            
            groupApi.getMemberDetail(formData).then(response =>{
                this.memberDetailForm.memberDetailList = response.data;
            }).catch((err) => {
                this.memberDetailForm.memberDetailList = []
            });

            this.writeVisible = true
            this.curRow = row
        },


        handleWrite(){
            let total = 0
            let totalb = 0
            let flag0 = false
            let flag1 = false
            let flag2 = false
            if(this.curRow.projectType==0){
                this.memberDetailForm.memberDetailList.forEach((member, index) => {
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
                    
                    if(member.bonus_category=='固定发放' || member.position == 'C类'){
                        if(parseFloat(member.amount) >0.00001 ){
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


            if(flag0){
                this.$message.error('科研项目不能发放给奖金库为管理或固定发放及A类、B类的人员')
                return false
            }

            if(flag1){
                this.$message.error('管理项目不能发放给奖金库为固定发放及C类的人员')
                return false
            }

            if(flag2){
                this.$message.error('管理项目不能发放给奖金库为科研或固定发放的人员')
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

            this.memberDetailForm.keshiDetailId = this.curRow.id
            this.memberDetailForm.planId = this.curChosenPlan
            this.memberDetailForm.projectId = this.curRow.projectId
            this.memberDetailForm.projectType = this.curRow.projectType
            groupApi.changeMemberDetail(this.memberDetailForm).then(response =>{
                this.closeWrite()
            })
        },


        closeWrite(){
            this.memberDetailForm.memberDetailList=[]
            this.writeVisible = false
            this.fetchKeshiProject()
        },

        formatter(row, column) {
          return row[column.property]==0?'科研项目':'管理项目'
        },

        exportTemp(row){
            let formData = new FormData();
            formData.append('planId', this.curChosenPlan)
            formData.append('projectId', row.projectId)
            formData.append('projectType',row.projectType)
            formData.append('keshiId',this.keshiId)
            
            groupApi.exportMemberDetail(formData).then(response =>{
                this.exportList = response.data;
                // console.log(this.exportList)
                
                var ws = XLSX.utils.aoa_to_sheet(this.exportList)
                var wb = XLSX.utils.book_new()
                XLSX.utils.book_append_sheet(wb, ws, "sheet");
                let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
                
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), row.projectName+'科室导出模板.xlsx')
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
                            if( parseFloat(member['金额'])>0.00001 && (member['奖金库']=='管理' || member['奖金库']=='固定发放' || member['岗位'] == 'A类' || member['岗位'] == 'B类')){
                                flag0 = true
                                return
                            }
                            if(member['工资总额类别']=='占工资总额'){
                                if(typeof(member['金额'])=="undefined" || member['金额'] == 0) total += 0
                                else total += parseFloat(member['金额'])
                            }
                        })
                    }else{
                        excelRows.forEach((member, index) => {
                            if( parseFloat(member['金额'])>0.00001 && (member['奖金库']=='固定发放' || member['岗位'] == 'C类')){
                                flag1 = true
                                return
                            }
                            if(member['工资总额类别']=='占工资总额'){
                                if(typeof(member['金额'])=="undefined" || member['金额'] == 0) total += 0
                                else total += parseFloat(member['金额'])
                            }else{
                                if(typeof(member['金额'])=="undefined" || member['金额'] == 0) totalb += 0
                                else totalb += parseFloat(member['金额'])
                                
                            }
                        })
                    }

                    if(flag0){
                        vm.$message.error('科研项目不能发放给奖金库为管理或固定发放及A类、B类的人员')
                        return false
                    }

                    if(flag1){
                        vm.$message.error('管理项目不能发放给奖金库为固定发放及C类的人员')
                        return false
                    }

                    if(flag2){
                        vm.$message.error('管理项目不能发放给奖金库为科研或固定发放的人员')
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
                    var form = {"keshiDetailId":row.id,"planId":vm.curChosenPlan,"projectId":row.projectId,"projectType":row.projectType}

                    groupApi.importMemberDetail(form,excelRows).then(response =>{
                        if(response.flag){//如果成功
                            vm.$message.success(response.message)
                            vm.fetchKeshiProject()
                        }
                        
                    })
                    // console.log(excelRows)
                };
                reader.readAsBinaryString(this.fileList[0].raw);
            })
        },

        exportTempAll(){
            if(this.curChosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }

            groupApi.getKeshiMember(this.keshiId).then(response =>{
                this.keshiMember = response.data;

                var title = ["室","姓名","身份证号","类别","工资总额类别","奖金库","岗位","备注"]
                this.proDetailList.forEach((pro, index) => {
                    title.push(pro.projectName)
                })

                var exportList = []
                exportList.push(title)
                this.keshiMember.forEach((member, index) => {
                    exportList.push(member)
                })
                


                var ws = XLSX.utils.aoa_to_sheet(exportList)
                var wb = XLSX.utils.book_new()
                XLSX.utils.book_append_sheet(wb, ws, "sheet");
                let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
                
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '科室完整模板.xlsx')
                } catch (e) { 
                    if (typeof console !== 'undefined') console.log(e, wbout) 
                }

            }).catch((err) => {
                this.keshiMember = []
            });
                       
        },

        handleUploadChange(file, fileList){
            if(this.curChosenPlan==''){
                this.tempList = []
                this.$message.error('请选择发放计划')
                return false
            }

            if (fileList.length > 0) {
                this.tempList = [fileList[fileList.length - 1]] // 这一步，是展示最后一次选择的文件
            }

            this.$confirm('确认导入该模板', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                var reader = new FileReader();
                var vm = this
                reader.onload = function (e) {
                    var workbook = XLSX.read(e.target.result, {type: 'binary'});
                    var Sheet = workbook.SheetNames[0];
                    var excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[Sheet]);
                    
                    let flag = false
                    vm.proDetailList.forEach((project, proIndex) => {
                        let total = 0
                        let totalb = 0
                        let flag0 = false
                        let flag1 = false
                        let flag2 = false

                        if(project.projectType==0){
                            excelRows.forEach((member, rowIndex) => {
                                if(parseFloat(member[project.projectName])>0.00001 && (member['奖金库']=='管理' || member['奖金库']=='固定发放' || member['岗位'] == 'A类' || member['岗位'] == 'B类')){
                                    flag0 = true
                                    return
                                }
                                if(member['工资总额类别']=='占工资总额'){
                                    if(typeof(member[project.projectName])=="undefined" || member[project.projectName] == 0) total += 0
                                    else total += parseFloat(member[project.projectName])
                                }
                            })
                        }else{
                            excelRows.forEach((member, rowIndex) => {
                                if(parseFloat(member[project.projectName])>0.00001 &&(member['奖金库']=='固定发放' || member['岗位'] == 'C类')){
                                    flag1 = true
                                    return
                                }
                                if(member['工资总额类别']=='占工资总额'){
                                    if(typeof(member[project.projectName])=="undefined" || member[project.projectName] == 0) total += 0
                                    else total += parseFloat(member[project.projectName])
                                }else{
                                    if(typeof(member[project.projectName])=="undefined" || member[project.projectName] == 0) totalb += 0
                                    else totalb += parseFloat(member[project.projectName])
                                }
                            })
                            
                            
                        }

                        if(flag0){
                            vm.$message.error('科研项目'+project.projectName+'不能发放给奖金库为管理或固定发放及A类、B类的人员')
                            flag = true
                            return false
                        }

                        if(flag1){
                            vm.$message.error('管理项目'+project.projectName+'不能发放给奖金库为固定发放及C类的人员')
                            flag = true
                            return false
                        }

                        if(flag2){
                            vm.$message.error('管理项目不能发放给奖金库为科研或固定发放的人员')
                            flag = true
                            return false
                        }

                        // console.log('uploadall')
                        // console.log(total)

                        if(total-project.amount>0.00001 || project.amount-total>0.00001){
                            vm.$message.error('项目'+project.projectName+'已分发总额(占工资)与奖金包不相等')
                            flag = true
                            return false
                        }

                        if(totalb - project.amountb > 0.00001){
                            vm.$message.error('项目'+project.projectName+'已分发总额(不占工资总额)超过奖金包')
                            flag = true
                            return false
                        }                        
                    })

                    if(flag){ return false}
                    
                    

                    var form = {"planId":vm.curChosenPlan,"keshiId":vm.keshiId}
                    groupApi.importKeshiDetail(form, excelRows, vm.proDetailList).then(async(response) => {
                        if(response.flag){//如果成功
                            vm.$message.success(response.message)
                            vm.fetchKeshiProject()
                        }
                    })
                };
                reader.readAsBinaryString(this.tempList[0].raw);
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
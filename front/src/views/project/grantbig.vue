<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlan" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%" @change="fetchMyProject">
            <el-option v-for="item in planList" :label="item.name" :key="item.id" :value="item.id"/>
        </el-select>

        <el-select v-model="chosenProject" placeholder="请选择项目" style="margin-left:2%;margin-top:2%">
            <el-option v-for="item in projectList" :label="item.projectName" :key="item.id" :value="item.id"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="handleShowDetail()">选择</el-button>
    </div>

    <div style="margin-left:5%;margin-top:2%"> 项目类型：{{curProjectTypeName}} </div>
    <div style="margin-left:5%;margin-top:2%"> 占工资总额奖金包：{{curProjectTotal}}(元) </div>
    

    <!-- <div>
       <el-button style="margin-left:5%;margin-top:5%" type="primary" @click="openAdd()">添加</el-button>
    </div> -->

    <div>
       <el-button style="margin-left:5%;margin-top:5%" type="primary" @click="openWrite()">填写</el-button>
    </div>

    <el-table
      :data="proDetailListNew"
      :row-style="{height:40+'px'}"
      show-summary
      :summary-method="getTotal"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="keshiname"
        label="科室"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="amount"
        label="分配金额"
        min-width="20%">
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

      <!-- <el-table-column
        label="操作"
        min-width="6%">
        <template slot-scope="scope">
          <el-button @click.native.stop="openChange(scope.row)" type="text" size="small">修改</el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        min-width="6%">
        <template slot-scope="scope">
          <el-button @click.native.stop="handleDel(scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column> -->
    </el-table>

    <!-- 增加项目金额分配弹出窗口 -->
    <el-dialog
      title="添加科室奖金"
      :visible.sync="addVisible"
      width="30%"
      >

      <el-form label-width="100px" :model="newKeshiDetailForm" ref="newProjectForm">  
        
        <el-form-item label="科室">
          <el-select v-model="newKeshiDetailForm.keshiId" >
            <el-option v-for="item in keshiList" :label="item.name" :key="item.id" :value="item.id"/>
          </el-select>
        </el-form-item>

        <el-form-item label="奖金金额">
            <el-input v-model="newKeshiDetailForm.amount" placeholder="占工资总额（单位：元）"></el-input>
        </el-form-item>

      </el-form>

      <el-button @click="handleAdd()" type="warning" style="margin-left:5%" size="small">新增</el-button>

    </el-dialog>

    <!-- 修改项目金额分配弹出窗口 -->
    <el-dialog
      title="修改项目奖金"
      :visible.sync="changeVisible"
      width="30%"
      >

      <el-form label-width="100px" :model="changeKeshiDetailForm" ref="newProjectForm">  
        
        <el-form-item label="奖金金额">
            <el-input v-model="changeKeshiDetailForm.amount" placeholder="占工资总额（单位：元）"></el-input>
        </el-form-item>

      </el-form>

      <el-button @click="handleChange()" type="warning" style="margin-left:5%" size="small">修改</el-button>

    </el-dialog>

    <!-- 科室分配奖金弹出窗口 -->
    <el-dialog
      title="科室奖金分配"
      :visible.sync="writeVisible"
      width="50%"
      >
        <el-form label-width="120px" >  
            <el-form-item
                v-for="(item,index) in allKeshiDetailForm.keshiDetailList"
                :key="index"
                :label="item.keshiname"
            >
            <el-input v-model="item.amount" clearable></el-input>
            </el-form-item>
        </el-form>
        <el-button @click="handleWrite()" type="warning" size="small">提交</el-button>
    </el-dialog>
    
  </div>



</template>
<script>
import planningApi from '@/api/planning'
import generalApi from '@/api/general'
import detailApi from '@/api/detail'
import projectApi from '@/api/project'

export default {
    data(){
        return {
            planList: [],
            chosenPlan: '',
            curChosenPlan: '',
            projectList: [],
            chosenProject: '', //index
            curProjectId: '',
            curProjectType: -1,
            curProjectTypeName: '',
            curProjectTotal: '',
            keshiList: [],
            proDetailList: [],

            newKeshiDetailForm:{
                planId: '',
                keshiId: '',
                projectId: '',
                projectType: '',
                amount: '',
            },

            allKeshiDetailForm:{
                planId: '',
                projectId: '',
                projectType: '',
                keshiDetailList:[{
                    id: '',
                    keshiId: '',
                    keshiname: '',
                    amount: '' ,
                }]
            },


            changeKeshiDetailForm:{
                id: '',
                amount: '',
            },

            addVisible: false,
            writeVisible: false,
            changeVisible: false,
            
        }
    },
    created () {
        this.fetchPlanList()
    },
    computed: {
        proDetailListNew: function () {
            return this.proDetailList.filter( (data) =>{
                return data.amount>0
            })
        }
    },
    methods: {
        fetchPlanList(){
            generalApi.getProPlanList().then(response =>{
                this.planList = response.data;
            }).catch((err) => {
                this.planList = []
            });
        },

        fetchKeshiList(){
            // console.log("fetch"+this.currentPage+' '+this.pageSize);
            generalApi.getKeshiList().then(response =>{
                this.keshiList = response.data;
            }).catch((err) => {
                this.keshiList = []
            })  
        },

        fetchMyProject(){
            this.curChosenPlan = this.chosenPlan
            projectApi.getMyBigProjectList(this.curChosenPlan).then(response =>{
                this.projectList = response.data;
            }).catch((err) => {
                this.projectList = []
            });
        },

        handleShowDetail(){
            if(this.curChosenPlan==''){
                this.$message.error('请选择计划')
                return false
            }
            if(this.chosenProject+' '==' '){
                this.$message.error('请选择项目')
                return false
            }

            this.curProjectId = this.projectList[this.chosenProject].projectId
            this.curProjectType = this.projectList[this.chosenProject].projectType
            this.curProjectTypeName = this.curProjectType==0?'科研项目':'管理项目'
            this.curProjectTotal = this.projectList[this.chosenProject].amount


            let formData = new FormData();
            formData.append('planId', this.curChosenPlan)
            formData.append('projectId', this.curProjectId)
            formData.append('projectType',this.curProjectType)
            
            projectApi.getBigProjectDetail(formData).then(response =>{
                this.proDetailList = response.data;
                // if(this.keshiList.length == 0) this.fetchKeshiList();
            }).catch((err) => {
                this.proDetailList = []
            });

        },


        openAdd(){
            if(this.curChosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }
            if(this.curProjectId==''){
                this.$message.error('请选择项目')
                return false
            }
            this.addVisible = true
        },

        openWrite(){
            if(this.curChosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }
            if(this.curProjectId==''){
                this.$message.error('请选择项目')
                return false
            }


            this.allKeshiDetailForm.keshiDetailList=JSON.parse(JSON.stringify(this.proDetailList))

            this.writeVisible = true
        },

        closeAdd(){
            this.handleShowDetail()
            this.addVisible = false
            this.newKeshiDetailForm.keshiId=''
            this.newKeshiDetailForm.amount=''
        },

        beforeAdd(){
            if(this.newKeshiDetailForm.keshiId==''){
                this.$message.error('请选择科室')
                return false
            }
            if(this.newKeshiDetailForm.amount==''){
                this.$message.error('请填写金额')
                return false
            }
            this.newKeshiDetailForm.planId = this.curChosenPlan
            this.newKeshiDetailForm.projectId = this.curProjectId
            this.newKeshiDetailForm.projectType = this.curProjectType
            return true
        },
        
        // 单独提交某科室金额
        handleAdd(){
            this.$confirm('确认新增项目奖金分配', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                if(this.beforeAdd()){
                    projectApi.createKeshiDetail(this.newKeshiDetailForm).then(async(response) => {
                        if(response.flag){//如果成功
                            this.$message.success(response.message)
                            this.closeAdd()
                        }
                    })
                }
            })
        },

        // 提交全部科室金额
        handleWrite(){

            let total = 0
            this.allKeshiDetailForm.keshiDetailList.forEach((keshi, index) => {
                total += parseFloat(keshi.amount)
            })

            if(total-this.curProjectTotal>0.00001 || this.curProjectTotal-total>0.00001){
                this.$message.error('已分发总额与奖金包不相等')
                return false
            }


            this.allKeshiDetailForm.planId = this.curChosenPlan
            this.allKeshiDetailForm.projectId = this.curProjectId
            this.allKeshiDetailForm.projectType = this.curProjectType

            projectApi.createAllKeshiDetail(this.allKeshiDetailForm).then(async(response) => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.handleShowDetail()
                    this.writeVisible = false
                }
            })

        },

        handleChange(){
            this.$confirm('确认修改项目奖金金额', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                if(this.changeKeshiDetailForm.amount==''){
                    this.$message.error('请填写金额')
                    return false
                }
                projectApi.changeKeshiDetail(this.changeKeshiDetailForm).then(async(response) => {
                    if(response.flag){//如果成功
                        this.$message.success(response.message)
                        this.changeVisible = false
                        this.handleShowDetail()
                    }
                })
            })
        },

        openChange(row){
          this.changeVisible = true
          this.changeKeshiDetailForm.id = row.id
          this.changeKeshiDetailForm.amount = row.amount
        },

        handleDel(row){
          this.$confirm('确认删除该项目奖金分配', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                projectApi.delKeshiDetail(row.id).then(async(response) => {
                    if(response.flag){//如果成功
                        this.$message.success(response.message)
                        this.handleShowDetail(this.curChosenPlan)
                    }
                })
            })
        },

        getTotal(param) {
            const { columns, data } = param;
            const sums = [];
            columns.forEach((column, index) => {
                if (index === 0) {
                    sums[index] = '合计';
                    return;
                }
                const values = data.map(item => Number(item[column.property]));
                if (column.property === 'amount' || column.property === 'amount_zhan' || column.property === 'amount_buzhan') {
                    sums[index] = values.reduce((prev, curr) => {
                        const value = Number(curr);
                        if (!isNaN(value)) {
                            return prev + curr;
                        } else {
                            return prev;
                        }
                    }, 0);
                    sums[index] = sums[index].toFixed(2);
                } else {
                    sums[index] = '--';
                }
            });

            return sums;
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
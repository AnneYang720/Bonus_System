<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlan" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%">
            <el-option v-for="item in planList" :label="item.name" :key="item.id" :value="item.id"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="handleShowDetail()">选择</el-button>
        <!-- <el-button style="margin-left:2%" type="primary" @click="handleShowDescription()">填写说明</el-button> -->
    </div>

    <div>
       <el-button style="margin-left:5%;margin-top:5%" type="primary" @click="openAdd()">添加</el-button>
    </div>

    <el-table
      :data="koufaList"
      :row-style="{height:40+'px'}"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="username"
        label="姓名"
        min-width="20%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.username }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="amount"
        label="扣发金额"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="remark"
        label="备注"
        min-width="20%">
      </el-table-column>


      <el-table-column
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
      </el-table-column>
      
    </el-table>

    <!-- 增加项目金额分配弹出窗口 -->
    <el-dialog
      title="添加人员扣发"
      :visible.sync="addVisible"
      width="50%"
      >

      <el-form label-width="100px" :model="newKoufaForm" ref="newProjectForm">  
        
        <el-form-item label="姓名">
          <el-input v-model="newKoufaForm.username" placeholder="人员姓名"></el-input>
        </el-form-item>

        <el-form-item label="扣发金额">
            <el-input v-model="newKoufaForm.amount" placeholder="扣罚金额（单位：元）"></el-input>
        </el-form-item>

        <el-form-item label="备注">
            <el-input v-model="newKoufaForm.remark" placeholder="备注"></el-input>
        </el-form-item>

      </el-form>

      <el-button @click="handleAdd()" type="warning" style="margin-left:5%" size="small">新增</el-button>

    </el-dialog>

    <!-- 修改项目金额分配弹出窗口 -->
    <el-dialog
      title="修改人员扣发"
      :visible.sync="changeVisible"
      width="30%"
      >
      <div style="margin-left:15px"> 姓名：{{curUser}} </div>

      <el-form label-width="80px" :model="changeKoufaForm" ref="newProjectForm">  
        
        <el-form-item label="扣发金额">
            <el-input v-model="changeKoufaForm.amount" placeholder="扣发金额（单位：元）"></el-input>
        </el-form-item>

        <el-form-item label="备注">
            <el-input v-model="changeKoufaForm.remark" placeholder="备注"></el-input>
        </el-form-item>

      </el-form>

      <el-button @click="handleChange()" type="warning" style="margin-left:5%" size="small">修改</el-button>

    </el-dialog>
    

  </div>



</template>
<script>
import planningApi from '@/api/planning'
import generalApi from '@/api/general'
import detailApi from '@/api/detail'

export default {
    data(){
        return {
            koufaList: [], 
            planList: [],
            newKoufaForm:{
                planId: '',
                username: '',
                amount: '',
                remark: '',
            },            
            changeKoufaForm:{
                id: '',
                amount: '',
                remark: '',
            },
            addVisible: false,
            changeVisible: false,

            chosenPlan: '',
            curChosenPlan: '',
            curUser: '',
        }
    },
    created () {
        this.fetchPlanList()
        // this.fetchProjectList()
    },
    methods: {
        // TODO 填写说明

        fetchPlanList(){
            generalApi.getShenPlanList().then(response =>{
                this.planList = response.data;
            }).catch((err) => {
                this.planList = []
            });
        },

        // fetchProjectList(){
        //     planningApi.getCurProjectList().then(response =>{
        //         this.projectList = response.data;
        //     }).catch((err) => {
        //         this.projectList = []
        //     });
        // },

        handleShowDetail(){
            this.curChosenPlan = this.chosenPlan
            detailApi.getKoufaDetailList(this.curChosenPlan).then(response =>{
                this.koufaList = response.data;
            }).catch((err) => {
                this.koufaList = []
          });
        },

        openAdd(row){
            if(this.curChosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }
            this.addVisible = true
        },

        closeAdd(){
            this.handleShowDetail(this.curChosenPlan)
            this.addVisible = false
        },

        beforeAdd(){
            if(this.newKoufaForm.username==''){
                this.$message.error('请填写姓名')
                return false
            }
            if(this.newKoufaForm.amount==''){
                this.$message.error('请填写金额')
                return false
            }
            return true
        },

        handleAdd(){
            this.$confirm('确认新增扣发', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                if(this.beforeAdd()){
                    this.newKoufaForm.planId = this.curChosenPlan
                    detailApi.createKoufaDetail(this.newKoufaForm).then(async(response) => {
                        if(response.flag){//如果成功
                            this.$message.success(response.message)
                            this.closeAdd()
                        }
                    })
                }
            })
        },

        handleChange(){
            if(this.changeKoufaForm.amount==''){
                this.$message.error('请填写金额')
                return false
            }
            detailApi.changeKoufaDetail(this.changeKoufaForm).then(async(response) => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.changeVisible = false
                    this.handleShowDetail(this.curChosenPlan)
                }
            })
            
        },

        openChange(row){
          this.changeVisible = true
          this.curUser = row.username
          this.changeKoufaForm.id = row.id
          this.changeKoufaForm.amount = row.amount
          this.changeKoufaForm.remark = row.remark
        },

        handleDel(row){
          this.$confirm('确认删除该扣发', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                detailApi.delKoufaDetail(row.id).then(async(response) => {
                    if(response.flag){//如果成功
                        this.$message.success(response.message)
                        this.handleShowDetail(this.curChosenPlan)
                    }
                })
            })
        },


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
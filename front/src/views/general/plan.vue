<template>
  <div>
    <br>

    <el-button @click="openAdd" type="primary" icon="el-icon-plus" style="margin-left:10%;margin-bottom:1%;margin-top:2%" plain>添加发放计划</el-button>

    <el-table
      :data="planList"
      :row-style="{height:40+'px'}"
      style="width:80%;margin-left:10%;margin-top:2%">

      <el-table-column
        prop="name"
        label="名称"
        min-width="15%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="year"
        label="年度"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="quarter"
        label="季度"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="state"
        label="状态"
        min-width="20%">
      </el-table-column>

      <el-table-column
        label="操作" 
        min-width="5%">
        <template slot-scope="scope">
          <el-button @click.native.stop="openChange(scope.row)" type="text" size="small">修改</el-button>
        </template>
      </el-table-column>

    </el-table>


    <!-- 增加发放计划弹出窗口 -->
    <el-dialog
      title="添加发放计划"
      :visible.sync="addPlanVisible"
      width="30%"
      >

      <el-form label-width="100px" :model="newPlanForm" ref="newPlanForm">  
        
        <el-form-item label="年">
            <el-input v-model="newPlanForm.year" placeholder="如：2020年"></el-input>
        </el-form-item>

        <el-form-item label="季度">
            <el-select v-model="newPlanForm.quarter" >
              <el-option v-for="item in quarterList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="newPlanForm.state" >
            <el-option v-for="item in stateList" :label="item" :key="item" :value="item"/>
          </el-select>
        </el-form-item>
      </el-form>

      <el-button @click="handleCreate()" type="warning" style="margin-left:5%" size="small">新增</el-button>

    </el-dialog>

    <!-- 修改发放计划信息弹出窗口 -->
    <el-dialog
      title="修改项目信息"
      :visible.sync="changePlanVisible"
      width="50%"
      >

      <el-form label-width="100px" :model="changePlanForm" ref="changePlanForm">        
        <el-form-item label="年">
          <el-input class="el-input-change" v-model="changePlanForm.year" placeholder="如：2020年"></el-input>
        </el-form-item>

        <el-form-item label="季度">
          <el-select v-model="changePlanForm.quarter" >
            <el-option v-for="item in quarterList" :label="item" :key="item" :value="item"/>
          </el-select>
        </el-form-item>

        <el-form-item label="状态">
          <el-select v-model="changePlanForm.state" >
            <el-option v-for="item in stateList" :label="item" :key="item" :value="item"/>
          </el-select>
        </el-form-item>

      </el-form>
      
      <el-button @click="changePlan()" type="warning" style="margin-left:5%" size="small">修改</el-button>

    </el-dialog>


  </div>
</template>
<script>
import generalApi from '@/api/general'
export default {
    data(){
        return {
          stateList: ["初始化", "项目经理发放中", "室主任发放中", "审核", "结束"],
          quarterList: ["第一季度","第二季度","第三季度","年终"],

          planList: [],
          newPlanForm: {
            year: '',
            quarter: '',
				    state: '',
			    },
          changePlanForm: {
            year: '',
            quarter: '',
				    state: '',
			    },

          addPlanVisible: false,
          changePlanVisible: false,
        }
    },
    created() {
        this.fetchPlanList()
    },
    methods: {
        fetchPlanList(){
            generalApi.getPlanList().then(response =>{
                this.planList = response.data;
            }).catch((err) => {
                this.planList = []
            });
        },
        emptyDict(dict_){
          for (var key in dict_) {
　　          var item = dict_[key];
　　          console.log(item); 
              dict_[key] ='';
          }
        },

        changePlan(){
          if(this.beforeChange()){
            this.loading = true
            generalApi.changePlan(this.changePlanForm).then(response => {
              if(response.flag){//如果成功
                this.$message.success(response.message)
              }
              this.closeChange()
            })
          }
        },

        beforeChange(){
          if(this.changePlanForm.year==''){
            this.$message.error('请填写年度')
            return false
          }
          if(this.changePlanForm.quarter==''){
            this.$message.error('请选择季度')
            return false
          }
          if(this.changePlanForm.state==''){
            this.$message.error('请选择状态')
            return false
          }
          return true
        },

        openChange(row){
          this.changePlanVisible = true
          this.changePlanForm = row
        },

        closeChange(){
          this.changePlanVisible = false
          this.fetchPlanList()
        },

        handleCreate(){
          this.$confirm('确认新增该管理项目', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(async() => {
            if(this.beforeCreate()){
              generalApi.createPlan(this.newPlanForm).then(async(response) => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.closeAdd()
                }
              })
            }
          })
        },

        beforeCreate(){
          if(this.newPlanForm.year==''){
            this.$message.error('请填写年度')
            return false
          }
          if(this.newPlanForm.quarter==''){
            this.$message.error('请选择季度')
            return false
          }
          if(this.newPlanForm.state==''){
            this.$message.error('请选择状态')
            return false
          }
          return true
        },


        openAdd(row){
          this.addPlanVisible = true
        },

        closeAdd(){
          this.fetchPlanList()
          this.addPlanVisible = false
          this.emptyDict(this.newPlanForm)
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
.el-input-change {
      display: inline-block;
      height: 47px;
      width: 85%;
}
</style>
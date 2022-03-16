<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlanIndex" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%">
            <el-option v-for="(item,index) in planList" :label="item.name" :key="index" :value="index"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="fetchProgress()">选择</el-button>
    </div>
    <div style="margin-left:5%;margin-top:2%"> 当前进度：{{curChosenPlanState}} </div>


    <el-table
      :data="progressList"
      :row-style="{height:40+'px'}"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="projectName"
        label="项目名称"
        v-if="curChosenPlanState==='项目经理发放中'"
        min-width="20%">
      </el-table-column>

    <el-table-column
        prop="keshiName"
        label="科室"
        v-if="curChosenPlanState==='室主任发放中'"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="manager"
        label="负责人"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="state"
        label="状态"
        :formatter="formatter"
        min-width="15%">
      </el-table-column>

    </el-table>
    
  </div>



</template>
<script>
import generalApi from '@/api/general'
import groupApi from '@/api/group'
import projectApi from '@/api/project'

export default {
    data(){
        return {
            planList: [],
            progressList: [], 
            chosenPlanIndex: '',
            curChosenPlan: '',
            curChosenPlanState: '',
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

        fetchProgress(){
            if(this.chosenPlanIndex===''){
                this.$message.error('请选择发放计划')
                return false
            }
            this.curChosenPlan = this.planList[this.chosenPlanIndex].id
            this.curChosenPlanState = this.planList[this.chosenPlanIndex].state

            if(this.curChosenPlanState==="项目经理发放中"){
                projectApi.getProgressList(this.curChosenPlan).then(response =>{
                    this.progressList = response.data;
                }).catch((err) => {
                    this.progressList = []
                });
            }else{
                groupApi.getProgressList(this.curChosenPlan).then(response =>{
                    this.progressList = response.data;
                }).catch((err) => {
                    this.progressList = []
                });
            }


        },

        formatter(row, column) {
          return row[column.property]==0?'已完成':'未完成'
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
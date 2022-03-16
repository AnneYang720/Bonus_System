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
        <el-button type="primary" style="margin-left:5%;margin-top:5%" @click="openAdd()">添加</el-button>
        <el-button type="info" icon="el-icon-download" @click="exportTemp">模板导出</el-button>        
    </div>

    <el-col :span="12" style="margin-left:5%;margin-top:1%">
      <el-upload
        action="aaa"
        accept=".xlsx"
        :multiple="false"
        :auto-upload="false"
        :on-change="handleUploadChange"
        :file-list="fileList">
        <el-button type="warning" icon="el-icon-upload2" >模板导入</el-button>
      </el-upload>
    </el-col>
    

    <el-table
      :data="proDetailList"
      :row-style="{height:40+'px'}"
      show-summary
      :summary-method="getTotal"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="name"
        label="项目名称"
        min-width="20%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.name }}</span>
        </template>
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
      title="添加项目奖金"
      :visible.sync="addVisible"
      width="30%"
      >

      <el-form label-width="100px" :model="newProDetailForm" ref="newProjectForm">  
        
        <el-form-item label="项目名称">
          <el-select v-model="newProDetailForm.projectId" >
            <el-option v-for="item in projectList" :label="item.name" :key="item.id" :value="item.id"/>
          </el-select>
        </el-form-item>

        <el-form-item label="奖金金额">
            <el-input v-model="newProDetailForm.amount" placeholder="占工资总额（单位：元）"></el-input>
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

      <el-form label-width="100px" :model="changeProDetailForm" ref="newProjectForm">  
        
        <el-form-item label="奖金金额">
            <el-input v-model="changeProDetailForm.amount" placeholder="占工资总额（单位：元）"></el-input>
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
import XLSX from 'xlsx'
import FileSaver from 'file-saver'
import {pFileReader} from '@/utils/filereader'

export default {
    data(){
        return {
            proDetailList: [], 
            planList: [],
            projectList: [],
            newProDetailForm:{
                planId: '',
                projectId: '',
                amount: '',
            },
            changeProDetailForm:{
                id: '',
                amount: '',
            },

            addVisible: false,
            changeVisible: false,

            chosenPlan: '',
            curChosenPlan: '',

            allProDetailList: [], 
            fileList: []
        }
    },
    created () {
        this.fetchPlanList()
        this.fetchProjectList()
    },
    methods: {
        // TODO 填写说明

        fetchPlanList(){
            generalApi.getCurPlanList().then(response =>{
                this.planList = response.data;
            }).catch((err) => {
                this.planList = []
            });
        },

        fetchProjectList(){
            planningApi.getCurProjectList().then(response =>{
                this.projectList = response.data;
            }).catch((err) => {
                this.projectList = []
            });
        },

        handleShowDetail(){
            this.curChosenPlan = this.chosenPlan
            detailApi.getResProjectDetailList(this.curChosenPlan).then(response =>{
                this.proDetailList = response.data;
            }).catch((err) => {
                this.proDetailList = []
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
            this.newProDetailForm.planId = ''
            this.newProDetailForm.projectId = ''
            this.newProDetailForm.amount = ''
        },

        beforeAdd(){
            if(this.newProDetailForm.id==''){
                this.$message.error('请选择项目')
                return false
            }
            if(this.newProDetailForm.amount==''){
                this.$message.error('请填写金额')
                return false
            }
            return true
        },

        handleAdd(){
            this.$confirm('确认新增项目奖金分配', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                if(this.beforeAdd()){
                    this.newProDetailForm.planId = this.curChosenPlan
                    detailApi.createResDetail(this.newProDetailForm).then(async(response) => {
                        if(response.flag){//如果成功
                            this.$message.success(response.message)
                            this.closeAdd()
                        }
                    })
                }
            })
        },

        handleChange(){
            this.$confirm('确认修改项目奖金金额', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                if(this.changeProDetailForm.amount==''){
                    this.$message.error('请填写金额')
                    return false
                }
                detailApi.changeDetail(this.changeProDetailForm).then(async(response) => {
                    if(response.flag){//如果成功
                        this.$message.success(response.message)
                        this.changeVisible = false
                        this.handleShowDetail(this.curChosenPlan)
                    }
                })
            })
        },

        openChange(row){
          this.changeVisible = true
          this.changeProDetailForm.id = row.id
          this.changeProDetailForm.amount = row.amount
        },

        handleDel(row){
          this.$confirm('确认删除该项目奖金分配', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                detailApi.delDetail(row.id).then(async(response) => {
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
        },

        exportTemp(){
            if(this.curChosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }

            detailApi.getAllResProjectDetailList(this.curChosenPlan).then(response =>{
                this.allProDetailList = response.data;
                console.log(this.allProDetailList)

                var ws = XLSX.utils.aoa_to_sheet(this.allProDetailList)
                var wb = XLSX.utils.book_new()
                XLSX.utils.book_append_sheet(wb, ws, "sheet");
                let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
                
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '科研项目模板.xlsx')
                } catch (e) { 
                    if (typeof console !== 'undefined') console.log(e, wbout) 
                }

            }).catch((err) => {
                this.allProDetailList = []
            });
                       
        },

        handleUploadChange(file, fileList) {
            // console.log('b')
            if(this.curChosenPlan==''){
                this.fileList = []
                this.$message.error('请选择发放计划')
                return false
            }
            if (fileList.length > 0) {
                this.fileList = [fileList[fileList.length - 1]] // 这一步，是展示最后一次选择的文件
            }
            
            this.$confirm('确认导入该模板', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                var reader = new FileReader();
                var planId = this.curChosenPlan
                var vm = this
                reader.onload = function (e) {
                    var workbook = XLSX.read(e.target.result, {
                        type: 'binary'
                    });
                    var Sheet = workbook.SheetNames[0];
                    var excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[Sheet]);
                    console.log("plan")
                    console.log(planId)
                    detailApi.createResDetailFromFile(planId, excelRows).then(async(response) => {
                        if(response.flag){//如果成功
                            vm.$message.success(response.message)
                            vm.handleShowDetail(this.curChosenPlan)
                        }
                    })
                };
                reader.readAsBinaryString(this.fileList[0].raw);
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
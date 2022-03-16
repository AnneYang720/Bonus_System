<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlan" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%">
            <el-option v-for="item in planList" :label="item.name" :key="item.id" :value="item.id"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="fetchAllDetail()">选择</el-button>
        <el-tooltip content="导出数据" placement="top">
          <el-button type="warning" plain @click="exportExcel()">导出</el-button>
        </el-tooltip>
    </div>


    <el-table
      :data="detailList"
      :row-style="{height:40+'px'}"
      id="table"
      stripe
      border
      height="76vh"
      style="margin-left:50px;margin-top:20px">

      <el-table-column
        prop="department" label="部门" fixed width="70">
      </el-table-column>

      <el-table-column
        prop="keshi" label="科室" fixed width="70">
      </el-table-column>

      <el-table-column
        prop="username" label="姓名" fixed width="70">
      </el-table-column>

      <el-table-column
        prop="idnum" label="身份证号" width="95">
      </el-table-column>

      <el-table-column
        prop="category" label="类别" width="80">
      </el-table-column>

      <el-table-column
        prop="wage_category" label="工资总额类别" width="70">
      </el-table-column>

      <el-table-column
        prop="job" label="职务" width="70">
      </el-table-column>

      <el-table-column
        prop="position" label="岗位" width="70">
      </el-table-column>

      <el-table-column
        prop="remarks" label="备注" width="70">
      </el-table-column>

      <el-table-column
        prop="bonus_category" label="奖金库" width="70">
      </el-table-column>

      <el-table-column width="90" v-for="(item,index) in projectList" :key="index" :prop="item.id" :label="item.name">
      </el-table-column>    

      <el-table-column
        prop="total_res"
        label="科研项目"
        width="90">
      </el-table-column>

      <el-table-column
        prop="koufa"
        label="扣发"
        width="90">
      </el-table-column>

      
      
    </el-table>


  </div>



</template>
<script>
import generalApi from '@/api/general'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'

export default {
    data(){
        return {
            planList: [],
            projectList: [],
            detailList: [],
            chosenPlan: '',
            curChosenPlan: '',
        }
    },
    created () {
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

        fetchAllDetail(){
            if(this.chosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }
            this.curChosenPlan = this.chosenPlan
            generalApi.getAllDetail(this.curChosenPlan).then(response =>{
                this.detailList = response.detail;
                this.projectList = response.project
            }).catch((err) => {
                this.detailList = []
                this.projectList = []
            });
        },

        exportExcel(){
            let fix = document.querySelector('.el-table__fixed');
            let wb;
            if(fix){ //判断要导出的节点中是否有fixed的表格，如果有，转换excel时先将该dom移除，然后append回去
                wb = XLSX.utils.table_to_book(document.querySelector('#table').removeChild(fix));
                document.querySelector('#table').appendChild(fix);
            }else{
                wb = XLSX.utils.table_to_book(document.querySelector('#table'));
                var ws = wb.Sheets["Sheet1"]
                for(var i=2; i<this.detailList.length+2; i++){
                  var key = "D"+i
                  ws[key].v = String(ws[key].v)
                  ws[key].t = 's'
                }
            }
            let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
            try {
                FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '奖金总览.xlsx')
            } catch (e) { 
                if (typeof console !== 'undefined') console.log(e, wbout) 
            }
            return wbout
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
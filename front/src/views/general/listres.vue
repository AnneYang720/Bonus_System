<template>
  <div>
    <br>

    <div>
        <el-select v-model="chosenPlan" placeholder="请选择发放计划" style="margin-left:5%;margin-top:2%">
            <el-option v-for="item in planList" :label="item.name" :key="item.id" :value="item.id"/>
        </el-select>
        <el-button style="margin-left:2%" type="primary" @click="fetchResAllDetail()">选择</el-button>
        <el-tooltip content="导出数据" placement="top">
          <el-button type="warning" plain @click="exportExcel()">导出</el-button>
        </el-tooltip>
    </div>


    <el-table
      :data="resDetailList"
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


      <el-table-column width="90" v-for="(item,index) in projectList" :key="index" :prop="item.id" :label="item.name">
        <template slot-scope="scope">
          <span v-if='scope.row[(projectList[index].id)+"flag"]==true' style="color: Red" @click="handleCheck(scope.row, projectList[index].id, projectList[index].name)" >{{ scope.row[projectList[index].id] }}</span>
          <span v-else style="color: Black">{{ scope.row[projectList[index].id] }}</span>

          <!-- <span v-if='scope.row[(projectList[index].id)+"flag"]==false' style="color: Black">{{ scope.row[projectList[index].id] }}</span>
          <span v-else style="color: Red" @click="handleCheck(scope.row, projectList[index].id, projectList[index].name)" >{{ scope.row[projectList[index].id] }}</span> -->
        </template>
      </el-table-column>    

      <el-table-column
        prop="total"
        label="合计"
        width="90">
      </el-table-column>
      
    </el-table>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[50,100,200]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      align="center"
      style="margin-top:3%">
    </el-pagination>

    <!-- 历史分配弹出窗口 -->
    <el-dialog
      title="历史分配查看"
      :visible.sync="historyVisible"
      width="50%"
      >

      <div> 姓名：{{curUser}} </div>
      <div> 项目：{{curProject}} </div>

      <el-table
      :data="historyList"
      :row-style="{height:40+'px'}"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="amount"
        label="金额"
        min-width="10%">
      </el-table-column>

      <el-table-column
        prop="time"
        label="时间"
        min-width="20%">
      </el-table-column>

       </el-table>

    </el-dialog>

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
            resDetailList: [],
            chosenPlan: '',
            curChosenPlan: '',
            historyVisible: false,
            historyList: [],

            curUser: '',
            curProject: '',

            total: 0,
            currentPage: 1,
            pageSize: 50,

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

        fetchResAllDetail(){
            if(this.chosenPlan==''){
                this.$message.error('请选择发放计划')
                return false
            }
            this.curChosenPlan = this.chosenPlan
            generalApi.getResAllDetail(this.curChosenPlan,this.currentPage,this.pageSize).then(response =>{
                this.total = response.total
                this.resDetailList = response.detail;
                this.projectList = response.project
            }).catch((err) => {
                this.resDetailList = []
                this.projectList = []
            });
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
                // console.log(column.property===null)
                sums[index] = values.reduce((prev, curr) => {
                    const value = Number(curr);
                    if (!isNaN(value)) {
                        return prev + curr;
                    } else {
                        return prev;
                    }
                }, 0);
                sums[index] = sums[index].toFixed(2);;
            });
            return sums;
        },

        handleCheck(row,project,projectname){

            let formData = new FormData();
            formData.append('userId', row.userId)
            formData.append('projectId', project)
            formData.append('planId', this.curChosenPlan)


            generalApi.getResHistory(formData).then(response =>{
                this.historyList = response.data;
                this.curUser = row.username
                this.curProject = projectname
                this.historyVisible = true
            }).catch((err) => {
                this.historyList = []
                this.curUser = ''
                this.curProject = ''
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
                for(var i=2; i<this.resDetailList.length+2; i++){
                  var key = "D"+i
                  ws[key].v = String(ws[key].v)
                  ws[key].t = 's'
                }
            }
            let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
            try {
                FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '科研项目奖金总览.xlsx')
            } catch (e) { 
                if (typeof console !== 'undefined') console.log(e, wbout) 
            }
            return wbout
        },

        handleSizeChange(val) {
            this.pageSize = val;
            this.fetchResAllDetail();
        },

        handleCurrentChange(val) {
            this.currentPage = val;
            this.fetchResAllDetail();
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
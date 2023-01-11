<template>
  <div>
    <br>
    <el-form :inline="true" align="left" style="margin-left:5%;margin-top:2%">     
          <el-form-item >
            <el-input v-model="keyword"></el-input>
          </el-form-item>
        
        <el-button @click="handleSearch()" type="primary" plain>搜索</el-button>
        <el-button type="warning" plain @click="exportExcel()">导出</el-button>
        <el-button type="info" icon="el-icon-download" @click="exportTemp">模板导出</el-button>
    </el-form>
    
    
    <el-col :span="12" style="margin-left:5%;">
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
      :data="projectList"
      :row-style="{height:40+'px'}"
      id="table"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="number"
        label="所级项目编号"
        min-width="15%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.number }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="name"
        label="项目名称"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="managername"
        label="项目经理"
        min-width="15%">
      </el-table-column>
      
      <el-table-column
        prop="managerkeshi"
        label="项目经理科室"
        min-width="15%">
      </el-table-column>
      <el-table-column
        prop="managerworknum"
        label="项目经理工号"
        min-width="15%">
      </el-table-column>
      
      <el-table-column
        prop="isBig"
        label="是否为大项目"
        :formatter="formatter"
        min-width="20%">
      </el-table-column>

      <el-table-column
        prop="state"
        label="状态"
        min-width="15%">
      </el-table-column>

      <el-table-column
        label="操作" 
        min-width="10%">
        <template slot-scope="scope">
          <el-button @click.native.stop="openChange(scope.row)" type="text" size="small">修改</el-button>
        </template>
      </el-table-column>

    </el-table>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10,50]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      align="center"
      style="margin-top:3%">
    </el-pagination>
    

    <!-- 修改项目信息弹出窗口 -->
    <el-dialog
      title="修改项目信息"
      :visible.sync="changeProjectVisible"
      width="50%"
      >

      <el-form label-width="100px" :model="changeProjectForm" ref="changeProjectForm">
        <el-form-item label="项目编号">
          <el-input class="el-input-change" v-model="changeProjectForm.number" placeholder="请输入项目编号"></el-input>
        </el-form-item>
        
        <el-form-item label="项目名称">
          <el-input class="el-input-change" v-model="changeProjectForm.name" placeholder="请输入项目名称"></el-input>
        </el-form-item>

        <el-form-item label="项目经理">
          <el-input class="el-input-change" v-model="changeProjectForm.manager" placeholder="请输入项目经理"></el-input>
        </el-form-item>

        <el-form-item label="是否为大项目">
          <el-checkbox v-model="changeProjectForm.isBig"></el-checkbox>
        </el-form-item>

        <el-form-item label="项目状态">
          <el-select v-model="changeProjectForm.state" >
            <el-option v-for="item in stateList" :label="item" :key="item" :value="item"/>
          </el-select>
        </el-form-item>

      </el-form>
      
      <el-button @click="changeProject()" type="warning" style="margin-left:5%" size="small">修改</el-button>

    </el-dialog>

  </div>
</template>
<script>

import planningApi from '@/api/planning'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'

export default {
    data(){
        return {
          projectList: [],
          changeProjectVisible: false,
          changeProjectForm: {
            name: '',
            manager: '',
				    isBig: false,
            state: '',
          },
          changeProjectRules: {
				    name: [{ required: true, trigger: 'blur'}],
				    manager: [{ required: true, trigger: 'blur'}],
            state: [{ required: true, trigger: 'blur'}],
          },
          stateList: ["进行中", "结束"],
          keyword:'', //搜索关键词
          total: 0,
          currentPage: 1,
          pageSize: 10,
          fileList: []
        }
    },
    created() {
        this.fetchProjectList()
    },
    methods: {
      
        fetchProjectList(){
            planningApi.getProjectList(this.currentPage,this.pageSize).then(response =>{
                this.total = response.total
                this.projectList = response.data
            }).catch((err) => {
                this.total = 0
                this.projectList = []
            });
        },

        changeProject(){
          if(this.beforeChange()){
            this.loading = true
            planningApi.changeProject(this.changeProjectForm).then(
              response => {
              if(response.flag){//如果成功
                this.$message.success(response.message)
              }
              this.closeChange()
            })
          }
          this.fetchProjectList()
        },

        beforeChange(){
          if(this.changeProjectForm.number==''){
            this.$message.error('请填写项目编号')
            return false
          }
          if(this.changeProjectForm.name==''){
            this.$message.error('请填写项目名称')
            return false
          }
          if(this.changeProjectForm.manager==''){
            this.$message.error('请填写项目经理')
            return false
          }
          if(this.changeProjectForm.state==''){
            this.$message.error('请选择项目状态')
            return false
          }
          return true
        },

        openChange(row){
          this.changeProjectVisible = true
          this.changeProjectForm = row
        },

        closeChange(){
          this.fetchProjectList()
          this.changeProjectVisible = false
        },


        formatter(row, column) {
          return row[column.property]?"是":"否"
        },

        handleSizeChange(val) {
          this.pageSize = val;
          this.currentPage = 1;
          this.handleSearch();
        },

        handleCurrentChange(val) {
          this.currentPage = val;
          this.handleSearch();
        },


        handleSearch(){
          if(this.keyword==='') this.fetchProjectList()
          else {
            this.currentPage = 1;
            planningApi.search(this.currentPage, this.pageSize, this.keyword).then(response =>{
                this.total = response.total
                this.projectList = response.data
            }).catch(() => {
                this.total = 0
                this.projectList = []
            });
          }
        },

        exportExcel(){
            let fix = document.querySelector('.el-table__fixed');
            let wb;
            if(fix){ //判断要导出的节点中是否有fixed的表格，如果有，转换excel时先将该dom移除，然后append回去
                wb = XLSX.utils.table_to_book(document.querySelector('#table').removeChild(fix));
                document.querySelector('#table').appendChild(fix);
            }else{
                wb = XLSX.utils.table_to_book(document.querySelector('#table'));
            }
            let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
            try {
                FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '项目-'+this.currentPage+'.xlsx')
            } catch (e) { 
                if (typeof console !== 'undefined') console.log(e, wbout) 
            }
            return wbout
        },

        exportTemp(){
            var list = [["所级项目编号","项目名称","项目经理","项目经理工号","是否为大项目","状态"]]

            var ws = XLSX.utils.aoa_to_sheet(list)
            var wb = XLSX.utils.book_new()
            XLSX.utils.book_append_sheet(wb, ws, "sheet");
            let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
            
            try {
                FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '科研项目模板.xlsx')
            } catch (e) { 
                if (typeof console !== 'undefined') console.log(e, wbout) 
            }        
        },

        handleUploadChange(file, fileList) {
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

                    planningApi.importProjects(excelRows).then(async(response) => {
                        if(response.flag){//如果成功
                            vm.$message.success(response.message)
                            vm.fileList = []
                            vm.fetchProjectList()
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
.el-input-change {
      display: inline-block;
      height: 47px;
      width: 85%;
}
</style>
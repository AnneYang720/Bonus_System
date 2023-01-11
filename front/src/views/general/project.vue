<template>
  <div>
    <br>

    <el-button @click="openAdd" type="primary" icon="el-icon-plus" style="margin-left:5%;margin-bottom:1%;margin-top:2%" plain>添加管理项目</el-button>

    <el-table
      :data="projectList"
      :row-style="{height:40+'px'}"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="id"
        label="ID"
        min-width="10%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.id }}</span>
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

      <el-table-column
        label="操作"
        min-width="6%">
        <template slot-scope="scope">
          <el-button @click.native.stop="handleDel(scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>

    </el-table>


    <!-- 增加管理项目弹出窗口 -->
    <el-dialog
      title="添加管理项目"
      :visible.sync="addProjectVisible"
      width="30%"
      >

      <el-form label-width="100px" :model="newProjectForm" ref="newProjectForm">  
        
        <el-form-item label="项目名称">
            <el-input v-model="newProjectForm.name" placeholder="选填写项目名称"></el-input>
        </el-form-item>

        <el-form-item label="项目经理">
            <el-input v-model="newProjectForm.manager" placeholder="选填写项目经理姓名"></el-input>
        </el-form-item>

        <!-- <el-form-item label="是否为大项目">
          <el-checkbox v-model="newProjectForm.isBig"></el-checkbox>
        </el-form-item> -->
        
        <el-form-item label="项目状态">
          <el-select v-model="newProjectForm.state" >
            <el-option v-for="item in stateList" :label="item" :key="item" :value="item"/>
          </el-select>
        </el-form-item>
      </el-form>

      <el-button @click="handleCreate()" type="warning" style="margin-left:5%" size="small">新增</el-button>

    </el-dialog>

    <!-- 修改项目信息弹出窗口 -->
    <el-dialog
      title="修改项目信息"
      :visible.sync="changeProjectVisible"
      width="50%"
      >

      <el-form label-width="100px" :model="changeProjectForm" ref="changeProjectForm">        
        <el-form-item label="项目名称">
          <el-input class="el-input-change" v-model="changeProjectForm.name" placeholder="请输入项目名称"></el-input>
        </el-form-item>

        <el-form-item label="项目经理">
          <el-input class="el-input-change" v-model="changeProjectForm.manager" placeholder="请输入项目经理工号"></el-input>
        </el-form-item>

        <!-- <el-form-item label="是否为大项目">
          <el-checkbox v-model="changeProjectForm.isBig"></el-checkbox>
        </el-form-item> -->

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
import generalApi from '@/api/general'
export default {
    data(){
        return {
          stateList: ["进行中", "结束"],
          projectList: [],
          newProjectForm: {
            name: '',
            manager: '',
				    state: '',
            isBig: false,
			    },
          changeProjectForm: {
            name: '',
            manager: '',
				    state: '',
            isBig: false,
			    },
          addProjectVisible: false,
          changeProjectVisible: false,
        }
    },
    created() {
        this.fetchProjectList()
    },
    methods: {
      // TODO 当前方法信息查询量和次数较多
        fetchProjectList(){
            // console.log("fetch"+this.currentPage+' '+this.pageSize);
            generalApi.getProjectList().then(response =>{
                this.projectList = response.data;
            }).catch((err) => {
                this.projectList = []
            });
        },


        changeProject(){
          if(this.beforeChange()){
            this.loading = true
            generalApi.changeProject(this.changeProjectForm).then(response => {
              if(response.flag){//如果成功
                this.$message.success(response.message)
              }
              this.closeChange()
            })
          }
        },

        handleDel(row){
            generalApi.delProject(row.id).then(async(response) => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.fetchProjectList()
                }
            })
            
        },

        beforeChange(){
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

        // TODO 不能直接复制row，应该复制row的值
        openChange(row){
          this.changeProjectVisible = true
          this.changeProjectForm = row
        },

        closeChange(){
          this.changeProjectVisible = false
          this.fetchProjectList()
        },

        handleCreate(){
          this.$confirm('确认新增该管理项目', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(async() => {
            if(this.beforeCreate()){
              generalApi.createProject(this.newProjectForm).then(async(response) => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.closeAdd()
                }
              })
            }
          })
        },

        beforeCreate(){
          if(this.newProjectForm.name==''){
            this.$message.error('请填写项目名称')
            return false
          }
          if(this.newProjectForm.manager==''){
            this.$message.error('请填写项目经理姓名')
            return false
          }
          if(this.newProjectForm.state==''){
            this.$message.error('请选择项目状态')
            return false
          }
          return true
        },


        openAdd(row){
          this.addProjectVisible = true
        },

        closeAdd(){
          this.fetchProjectList()
          this.addProjectVisible = false
          this.newProjectForm.name = ''
          this.newProjectForm.manager = ''
          this.newProjectForm.state = ''
          this.newProjectForm.isBig = false
        },

        formatter(row, column) {
          return row[column.property]?"是":"否"
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
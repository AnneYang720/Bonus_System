<template>
  <div>
    <br>

    <el-button @click="openAdd" type="primary" icon="el-icon-plus" style="margin-left:5%;margin-bottom:1%;margin-top:2%" plain>添加科室</el-button>

    <el-table
      :data="keshiList"
      :row-style="{height:40+'px'}"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="name"
        label="科室"
        min-width="15%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="manager_name"
        label="室主任"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="type"
        label="类型"
        :formatter="formatter"
        min-width="15%">
      </el-table-column>
          
      <el-table-column
        label="操作"
        min-width="10%">
        <template slot-scope="scope">
          <el-button @click.native.stop="openChange(scope.row)" type="text" size="small">修改</el-button>
        </template>
      </el-table-column>

      <!-- <el-table-column
        label="操作"
        min-width="10%">
        <template slot-scope="scope">
          <el-button @click.native.stop="handleDel(scope.row)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column> -->

    </el-table>
    
    <!-- 增加科室弹出窗口 -->
    <el-dialog
      title="添加科室"
      :visible.sync="addKeshiVisible"
      width="30%"
      >

      <el-form label-width="120px" :model="newKeshiForm" ref="newK e shiForm">  
        <el-form-item label="科室名称">
            <el-input v-model="newKeshiForm.name" placeholder="选填写新科室名称"></el-input>
        </el-form-item>
        <el-form-item label="室主任工号">
            <el-input v-model="newKeshiForm.manager_worknum" placeholder="选填写室主任工号"></el-input>
        </el-form-item>
        <el-form-item label="是否为管理部门">
          <el-checkbox v-model="newKeshiForm.isMan"></el-checkbox>
        </el-form-item>
      </el-form>

      <el-button @click="handleAdd()" type="warning" style="margin-left:5%" size="small">新增</el-button>

    </el-dialog>

    <!-- 修改科室信息弹出窗口 -->
    <el-dialog
      title="修改用户信息"
      :visible.sync="changeVisible"
      width="50%"
      >

      <el-form label-width="120px" :model="changeKeshiForm" ref="changeKeshiForm">
        
        <el-form-item label="科室名称">
          <el-input v-model="changeKeshiForm.name"></el-input>
        </el-form-item>

        <el-form-item label="室主任工号">
          <el-input v-model="changeKeshiForm.manager_worknum"></el-input>
        </el-form-item>

        <el-form-item label="是否为管理部门">
          <el-checkbox v-model="changeKeshiForm.isMan"></el-checkbox>
        </el-form-item>

      </el-form>
      
      <el-button @click="changeKeshi()" type="warning" style="margin-left:5%" size="small">修改</el-button>

    </el-dialog>
    

    
  </div>
</template>
<script>
import generalApi from '@/api/general'
export default {
    data(){
        return {
            keshiList: [], 
            addKeshiVisible:false,
            newKeshiForm: {
                name: '',
                manager_worknum: '',
                isMan: false,
			},
            changeVisible: false,
            changeKeshiForm: {
                id:'',
                name:'',
                manager_worknum:'',
                isMan: false,
            },
        }
    },
    created() {
        this.fetchKeshiList()
    },
    methods: {
        fetchKeshiList(){
            // console.log("fetch"+this.currentPage+' '+this.pageSize);
            generalApi.getKeshiFullList().then(response =>{
                this.keshiList = response.data;
            }).catch((err) => {
                this.keshiList = []
            })  
        },

        openAdd(){
          this.addKeshiVisible = true
          this.newKeshiForm.name = ''
          this.newKeshiForm.manager_worknum = ''
          this.newKeshiForm.isMan = false
        },

        beforeAdd(){
	      	if(this.newKeshiForm.name==''){
			    this.$message.error('请填写新科室名称')
	      		return false
      		}
            if(this.newKeshiForm.manager_worknum==''){
                this.$message.error('请填写新科室室主任的工号')
              return false
            }
            return true
        },

        handleAdd(){
            this.$confirm('确认新增该科室', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                if(this.beforeAdd()){
                    generalApi.addKeshi(this.newKeshiForm).then(async(response) => {
                        if(response.flag){//如果成功
                            this.$message.success(response.message)
                            this.closeAdd()
                        }
                    })
                }
            })
        },

        closeAdd(){
          this.fetchKeshiList()
          this.addKeshiVisible = false
        },

        formatter(row, column) {
          return row[column.property]?'管理部门':'科研部门'
        },

        openChange(row){
            this.changeVisible = true
            this.changeKeshiForm.id = row.id
            this.changeKeshiForm.name = row.name
            this.changeKeshiForm.manager_worknum = row.manager_worknum
            this.changeKeshiForm.isMan = row.type
        },

        changeKeshi(){
          if(this.beforeChange()){
            this.loading = true
            generalApi.changeKeshi(this.changeKeshiForm).then(response => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.closeChange() 
                }
            })
          }
        },

        beforeChange(){
            if(this.changeKeshiForm.name==''){
              this.$message.error('请填写科室名称')
              return false
            }
            if(this.changeKeshiForm.manager_worknum==''){
              this.$message.error('请填写科室室主任的工号')
              return false
            }
            return true
        },

        closeChange(){
          this.fetchKeshiList()
          this.changeVisible = false
        },

        handleDel(row){
            this.$confirm('确认删除该科室', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                generalApi.delKeshi(row.id).then(async(response) => {
                    if(response.flag){//如果成功
                        this.$message.success(response.message)
                        this.fetchKeshiList()
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
.el-input-change {
      display: inline-block;
      height: 47px;
      width: 85%;
}
</style>
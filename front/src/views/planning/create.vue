<template>
  <div>
    <br>
      <div style="line-height:60px;margin-left:5%;font-size:20px"> 新建科研项目 </div>
      
      <el-form label-width="100px" :model="newProjectForm" ref="newProjectForm" style="margin-left:5%">  

        <el-form-item label="所级项目编号">
          <el-col :span="8">
            <el-input v-model="newProjectForm.number" placeholder="填写所级项目编号"></el-input>
          </el-col>
        </el-form-item>
        
        <el-form-item label="项目名称">
          <el-col :span="8">
            <el-input v-model="newProjectForm.name" placeholder="填写项目名称"></el-input>
          </el-col>
        </el-form-item>

        <el-form-item label="项目经理">
          <el-col :span="8">
            <el-input v-model="newProjectForm.manager" placeholder="填写项目经理工号"></el-input>
          </el-col>
        </el-form-item>

        <el-form-item label="是否为大项目">
          <el-checkbox v-model="newProjectForm.isBig"></el-checkbox>
        </el-form-item>
        
        <el-form-item label="项目状态">
          <el-select v-model="newProjectForm.state" >
            <el-option v-for="item in stateList" :label="item" :key="item" :value="item"/>
          </el-select>
        </el-form-item>


      </el-form>

      <el-button style="margin-left:5%" type="primary"  :loading="loading" @click="handleCreate()">创 建</el-button>


  </div>
</template>
<script>

import planningApi from '@/api/planning'

export default {
    data(){
        return {
			loading: false,
            newProjectForm: {
                number: '',
				name: '',
                manager: '',
				isBig: false,
                state: '',
			},
			newProjectRules: {
                number: [{ required: true, trigger: 'blur'}],
				name: [{ required: true, trigger: 'blur'}],
				manager: [{ required: true, trigger: 'blur'}],
                state: [{ required: true, trigger: 'blur'}],
            },
            stateList: ["进行中", "结束"]
        }
    },

    methods: {
        
        // Final
        handleCreate(){
			this.$confirm('确认新增该科研项目', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(async() => {
                if(this.beforeCreate()){
                    planningApi.createProject(this.newProjectForm).then(async(response) => {
                        if(response.flag){//如果成功
                            this.$message.success(response.message)
                            this.closeCreate() // 清空前端用户数据
                        }
                    })
                }
				this.loading = false
            })
		},

        beforeCreate(){
			if(this.newProjectForm.number==''){
				this.$message.error('请填写项目编号')
				return false
			}
			if(this.newProjectForm.name==''){
				this.$message.error('请填写项目名称')
				return false
			}
            if(this.newProjectForm.manager==''){
				this.$message.error('请填写项目经理的工号')
				return false
			}
			if(this.newProjectForm.state==''){
				this.$message.error('请选择项目状态')
				return false
			}
			return true
        },

        closeCreate(){
            this.newProjectForm.number = ''
		    this.newProjectForm.name = ''
            this.newProjectForm.manager = ''
            this.newProjectForm.isBig = false
            this.newProjectForm.state = ''
        },

        formatter(row, column) {
            return row[column.property]?"是":"否"
        },

    }
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

.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}

</style>
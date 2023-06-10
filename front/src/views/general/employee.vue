<template>
  <div>
    <br>

    <el-form :inline="true" align="left" style="margin-left:5%;margin-top:2%">     
        <el-form-item >
            <el-input v-model="keyword" placeholder="姓名"></el-input>
        </el-form-item>

        <el-select
          v-model="keyword_keshi"
          multiple
          collapse-tags
          placeholder="选择科室"
          @change="handleKeshiChange">
            <el-option
                v-for="item in keshiSelList"
                :key="item.id"
                :label="item.name"
                :value="item.id">
            </el-option>
        </el-select>

        <el-select
          v-model="keyword_category"
          multiple
          collapse-tags
          placeholder="选择类别"
          @change="handleCategoryChange">
            <el-option
                v-for="item in categorySelList"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
        </el-select>
        
        <el-button @click="handleSearch()" type="primary" plain>搜索</el-button>
        
        <el-button @click="openAdd" type="primary" icon="el-icon-plus"  plain>添加人员</el-button>
        <el-button type="warning" plain @click="exportExcel()">导出</el-button>
    </el-form>

    <el-table
      :data="userList"
      :row-style="{height:40+'px'}"
      id="table"
      style="width:90%;margin-left:5%;margin-top:2%">

      <el-table-column
        prop="worknum"
        label="工号"
        min-width="15%">
        <template slot-scope="scope">
          <span style="color: DodgerBlue">{{ scope.row.worknum }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="username"
        label="姓名"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="department"
        label="部门"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="keshiname"
        label="科室"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="idnum"
        label="身份证号"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="category"
        label="类别"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="wage_category"
        label="工资总额类别"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="job"
        label="职务"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="position"
        label="岗位"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="remarks"
        label="备注"
        min-width="15%">
      </el-table-column>

      <el-table-column
        prop="bonus_category"
        label="人员所在奖金库"
        min-width="15%">
      </el-table-column>
      
      
      <el-table-column
        prop="role"
        label="用户角色"
        :formatter="formatList"
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
      :page-sizes="[10,50,100,200]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      align="center"
      style="margin-top:3%">
    </el-pagination>
    
    <!-- 增加用户弹出窗口 -->
    <el-dialog
      title="添加人员"
      :visible.sync="addUserVisible"
      width="30%"
      >

      <el-form label-width="100px" :model="newUserForm" ref="newUserForm">  
        
        <el-form-item label="人员工号">
            <el-input v-model="newUserForm.worknum" placeholder="选填写人员工号"></el-input>
        </el-form-item>

        <el-form-item label="人员姓名">
            <el-input v-model="newUserForm.username" placeholder="选填写人员姓名"></el-input>
        </el-form-item>

        <el-form-item label="人员部门">
            <el-input v-model="newUserForm.department" placeholder="选填写人员部门"></el-input>
        </el-form-item>

        <el-form-item label="人员科室">
          <el-select v-model="newUserForm.keshi" >
            <el-option v-for="item in keshiList" :label="item.name" :key="item.id" :value="item.id"/>
          </el-select>
        </el-form-item>

        <el-form-item label="身份证号">
            <el-input v-model="newUserForm.idnum" placeholder="选填写人员身份证号"></el-input>
        </el-form-item>
        
        <el-form-item label="类别">
            <el-select v-model="newUserForm.category" >
                <el-option v-for="item in categoryList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>

        <el-form-item label="工资总额类别">
            <el-select v-model="newUserForm.wage_category" >
                <el-option v-for="item in wageCategoryList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>

        <el-form-item label="职务">
            <el-input v-model="newUserForm.job"></el-input>
        </el-form-item>

        <el-form-item label="岗位">
            <el-input v-model="newUserForm.position"></el-input>
        </el-form-item>

        <el-form-item label="备注">
            <el-input v-model="newUserForm.remarks"></el-input>
        </el-form-item>

        <el-form-item label="所在奖金库">
            <el-select v-model="newUserForm.bonus_category" >
                <el-option v-for="item in bonusCategoryList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>
      </el-form>

      <el-button @click="handleCreate()" type="warning" style="margin-left:5%" size="small">新增</el-button>

    </el-dialog>
    <!-- 修改用户信息弹出窗口 -->
    <el-dialog
      title="修改用户信息"
      :visible.sync="changeVisible"
      width="50%"
      >

      <el-form label-width="100px" :model="changeUserForm" ref="changeUserForm">
        
        <el-form-item label="用户名">
          <el-input v-model="changeUserForm.username"></el-input>
        </el-form-item>

        <el-form-item label="身份证号">
          <el-input v-model="changeUserForm.idnum"></el-input>
        </el-form-item>

        <el-form-item label="部门">
          <el-input v-model="changeUserForm.department"></el-input>
        </el-form-item>

        <el-form-item label="室">
          <el-select v-model="changeUserForm.keshi" >
            <el-option v-for="item in keshiList" :label="item.name" :key="item.id" :value="item.id"/>
          </el-select>
        </el-form-item>

        <el-form-item label="类别">
            <el-select v-model="changeUserForm.category" >
                <el-option v-for="item in categoryList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>

        <el-form-item label="工资总额类别">
            <el-select v-model="changeUserForm.wage_category" >
                <el-option v-for="item in wageCategoryList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>

        <el-form-item label="职务">
            <el-input v-model="changeUserForm.job"></el-input>
        </el-form-item>

        <el-form-item label="岗位">
            <el-input v-model="changeUserForm.position"></el-input>
        </el-form-item>

        <el-form-item label="备注">
            <el-input v-model="changeUserForm.remarks"></el-input>
        </el-form-item>

        <el-form-item label="所在奖金库">
            <el-select v-model="changeUserForm.bonus_category" >
                <el-option v-for="item in bonusCategoryList" :label="item" :key="item" :value="item"/>
            </el-select>
        </el-form-item>
      
        <el-form-item label="密码">
            <el-input name="password" :type="pwdType" v-model="changeUserForm.password" 
                class="el-input-change" placeholder="password"></el-input>
            <span class="show-pwd" @click="showPwd"><svg-icon icon-class="eye" /></span>
        </el-form-item>
      </el-form>
      
      <el-button @click="changeUser()" type="warning" style="margin-left:5%" size="small">修改</el-button>

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
            userList: [], //首页用包名得到的列表
            keshiList: [], 
            categoryList: [],
            wageCategoryList: ["占工资总额","不占工资总额"],
            bonusCategoryList: ["科研" , "管理" , "科研及管理", "固定发放"],

            changeVisible: false,
            changeUserForm: {
                id:'',
                username:'',
                idnum:'',
                department: '',
                keshi: '',
                category: '',
                wage_category: '',
                job: '',
                position: '',
                remarks: '',
                bonus_category: '',
                password: '',
            },
            addUserVisible:false,
            newUserForm: {
                username:'',
                idnum:'',
                department: '',
                keshi: '',
                category: '',
                wage_category: '',
                job: '',
                position: '',
                remarks: '',
                bonus_category: '',
                password: '',
			},

            pwdType: 'password',
            keyword:'', //搜索关键词

            keshiSelList:[],  // keshiList + 'ALL_SELECT'
            keyword_keshi:[],
            keyword_keshi_old:[],

            categorySelList:[],
            keyword_category:[],
            keyword_category_old:[],

            total: 0,
            currentPage: 1,
            pageSize: 10,
        }
    },
    created() {
        this.fetchUsersList()
        this.fetchKeshiList()
        this.fetchCategoryList()
    },
    methods: {
                
        fetchUsersList(){
            generalApi.getUsersList(this.currentPage,this.pageSize).then(response =>{
                this.total = response.total
                this.userList = response.data;
            }).catch((err) => {
                this.total = 0
                this.userList = []
            })  
        },

        fetchKeshiList(){
            // console.log("fetch"+this.currentPage+' '+this.pageSize);
            let _all = {id:'ALL_SELECT', name:'全选'}
            generalApi.getKeshiList().then(response =>{
                this.keshiList = response.data;
                this.keshiSelList = [_all].concat(this.keshiList)
            }).catch((err) => {
                this.keshiList = []
            })  
        },

        fetchCategoryList(){
            // console.log("fetch"+this.currentPage+' '+this.pageSize);
            let _all = '全选'
            generalApi.getCategoryList().then(response =>{
                this.categoryList = response.data;
                this.categorySelList = [_all].concat(this.categoryList)
            }).catch((err) => {
                this.categoryList = []
            })
        },
        
        emptyDict(dict_){
          for (var key in dict_) {
              var item = dict_[key];
              console.log(item); 
              dict_[key] ='';
          }
        },

        changeUser(){
          if(this.beforeChange()){
            this.loading = true
            generalApi.changeUser(this.changeUserForm).then(response => {
                if(response.flag){//如果成功
                    this.$message.success(response.message)
                    this.closeChange() 
                }
            })
          }
        },

        beforeChange(){
            if(this.changeUserForm.department==''){
              this.$message.error('请填写部门')
              return false
            }
            if(this.changeUserForm.keshi==''){
              this.$message.error('请填写科室')
              return false
            }
            if(this.changeUserForm.category==''){
              this.$message.error('请选择类别')
              return false
            }
            if(this.changeUserForm.wage_category==''){
              this.$message.error('请选择工资总额类别')
              return false
            }
            if(this.changeUserForm.bonus_category==''){
              this.$message.error('请选择所在奖金库')
              return false
            }
            return true
        },

        openChange(row){
          this.changeVisible = true
          this.changeUserForm = row
        },

        closeChange(){
          this.handleSearch()
          this.changeVisible = false
        },
        
        openAdd(row){
          this.addUserVisible = true

          this.$nextTick(()=>{
            this.emptyDict(this.newUserForm)
            this.$refs['newUserForm'].resetFields()
          })
        },

        closeAdd(){
          this.fetchUsersList()
          this.addUserVisible = false
        },
        
        beforeCreate(){
            if(this.newUserForm.department==''){
                this.$message.error('请填写部门')
                return false
            }
            if(this.newUserForm.keshi==''){
            this.$message.error('请填写科室')
              return false
            }
            if(this.newUserForm.category==''){
              this.$message.error('请选择类别')
              return false
            }
            if(this.newUserForm.wage_category==''){
              this.$message.error('请选择工资总额类别')
              return false
            }
            if(this.newUserForm.bonus_category ==''){
              this.$message.error('请选择所在的奖金库')
              return false
            }
            return true
        },

        handleCreate(){
              this.$confirm('确认新增该人员', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(async() => {
                if(this.beforeCreate()){
                  generalApi.addUser(this.newUserForm).then(async(response) => {
                  if(response.flag){//如果成功
                      this.$message.success(response.message)
                      this.closeAdd()
                      
                  }
                   })
                }
            })
         
        },

        formatList(row, column) {
          return row[column.property].join(", ")
        },

        showPwd() {
          if (this.pwdType === 'password') {this.pwdType = ''} 
          else {this.pwdType = 'password'}
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
                FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '用户-'+this.currentPage+'.xlsx')
            } catch (e) { 
                if (typeof console !== 'undefined') console.log(e, wbout) 
            }
            return wbout
        },
        
        handleSizeChange(val) {
            this.pageSize = val;
            this.handleSearch();
        },

        handleCurrentChange(val) {
            this.currentPage = val;
            this.handleSearch();
        },

        // 全选支持，来自 https://blog.csdn.net/sleepwalker_1992/article/details/88876114
        handleKeshiChange(val) {
          const allValues = this.keshiSelList.map(item => {
            return item.id;
          });
          // 用来储存上一次选择的值，可进行对比
          const oldVal = this.keyword_keshi_old.length > 0 ? this.keyword_keshi_old : [];
    
          // 若选择全部
          if (val.includes('ALL_SELECT')) {
            this.keyword_keshi = allValues;
          }
    
          // 取消全部选中， 上次有， 当前没有， 表示取消全选
          if (oldVal.includes('ALL_SELECT') && !val.includes('ALL_SELECT')) {
            this.keyword_keshi = [];
          }
    
          // 点击非全部选中，需要排除全部选中 以及 当前点击的选项
          // 新老数据都有全部选中
          if (oldVal.includes('ALL_SELECT') && val.includes('ALL_SELECT')) {
            const index = val.indexOf('ALL_SELECT');
            val.splice(index, 1); // 排除全选选项
            this.keyword_keshi = val;
          }
    
          // 全选未选，但是其他选项都全部选上了，则全选选上
          if (!oldVal.includes('ALL_SELECT') && !val.includes('ALL_SELECT')) {
            if (val.length === allValues.length - 1) {
              this.keyword_keshi = ['ALL_SELECT'].concat(val);
            }
          }
    
          // 储存当前选择的最后结果 作为下次的老数据
          this.keyword_keshi_old = this.keyword_keshi;
	      },

        handleCategoryChange(val) {
          const allValues = this.categorySelList;
          // 用来储存上一次选择的值，可进行对比
          const oldVal = this.keyword_category_old.length > 0 ? this.keyword_category_old : [];
    
          // 若选择全部
          if (val.includes('全选')) {
            this.keyword_category = allValues;
          }
    
          // 取消全部选中， 上次有， 当前没有， 表示取消全选
          if (oldVal.includes('全选') && !val.includes('全选')) {
            this.keyword_category = [];
          }
    
          // 点击非全部选中，需要排除全部选中 以及 当前点击的选项
          // 新老数据都有全部选中
          if (oldVal.includes('全选') && val.includes('全选')) {
            const index = val.indexOf('全选');
            val.splice(index, 1); // 排除全选选项
            this.keyword_category = val;
          }
    
          // 全选未选，但是其他选项都全部选上了，则全选选上
          if (!oldVal.includes('全选') && !val.includes('全选')) {
            if (val.length === allValues.length - 1) {
              this.keyword_category = ['全选'].concat(val);
            }
          }
    
          // 储存当前选择的最后结果 作为下次的老数据
          this.keyword_category_old = this.keyword_category;
	      },

        // 人员搜索
        handleSearch(){
            if(this.keyword==='' && this.keyword_keshi.length==0 && this.keyword_category.length==0) {
                this.fetchUsersList()
            }
            else {
                const formData = new FormData()
                // remove ALL_SELECT from keyword_keshi and keyword_category
                let keyword_keshi = this.keyword_keshi.filter(item => item !== 'ALL_SELECT')
                let keyword_category = this.keyword_category.filter(item => item !== 'ALL_SELECT')

                formData.append('keshi', keyword_keshi)
                formData.append('category', keyword_category)
                formData.append('keyword', this.keyword)
                formData.append('pageSize', this.pageSize)
                formData.append('currentPage', this.currentPage)

                generalApi.search(formData).then(response =>{
                    this.total = response.total
                    this.userList = response.data
                }).catch(() => {
                    this.total = 0
                    this.userList = []
                });
            }
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
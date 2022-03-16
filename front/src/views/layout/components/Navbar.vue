<template>
  <el-menu class="navbar" mode="horizontal">
    <hamburger class="hamburger-container" :toggleClick="toggleSideBar" :isActive="sidebar.opened"></hamburger>
    <breadcrumb></breadcrumb>
    <el-dropdown class="avatar-container" trigger="click">
      <div class="avatar-wrapper">
        <img class="user-avatar" src='/static/img/avatar.png' />

        <i class="el-icon-caret-bottom"></i>
      </div>
      <el-dropdown-menu class="user-dropdown" slot="dropdown">
        <el-dropdown-item @click.native="changeVisible=true" divided>
          <span style="display:block;">修改密码</span>
        </el-dropdown-item>
        <el-dropdown-item @click.native="logout" divided>
          <span style="display:block;">退出登录</span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  

    <el-dialog
      title = "修改密码"
      :visible.sync="changeVisible"
      width="50%"
      >

      <el-form label-width="100px"   style="margin-left:5%">  

          <el-form-item label="新密码">
            <el-col :span="8">
              <el-input v-model="newPwd" placeholder="填写新密码"></el-input>
            </el-col>
          </el-form-item>
      </el-form>

      <el-button style="margin-left:5%" type="primary" @click="handleChange()">提 交</el-button>
    </el-dialog>

  </el-menu>
  
</template>


<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'
import {changePwd} from '@/api/login'

export default {
  data(){
    return {
      list:[],
      pojo:{},//编辑实体
      changeVisible: false,
      newPwd:'',
    }
  },
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters([
      'userId',
      'sidebar'
    ])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('ToggleSideBar')
    },
    logout() {
      this.$store.dispatch('LogOut').then(() => {
        location.reload() // 为了重新实例化vue-router对象 避免bug
      })
    },
    handleChange(){
      changePwd(this.newPwd).then(response=>{
        if(response.flag){//如果成功
            this.$message.success(response.message)
            this.logout()
        }
      })
    }

  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.navbar {
  height: 50px;
  // line-height: 50px;
  border-radius: 0px !important;
  .hamburger-container {
    line-height: 58px;
    height: 50px;
    float: left;
    padding: 0 10px;
  }
  .screenfull {
    position: absolute;
    right: 90px;
    top: 16px;
    color: red;
  }
  .avatar-container {
    height: 50px;
    display: inline-block;
    position: absolute;
    right: 35px;
    .avatar-wrapper {
      cursor: pointer;
      margin-top: 5px;
      position: relative;
      .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 10px;
      }
      .el-icon-caret-bottom {
        position: absolute;
        right: -20px;
        top: 25px;
        font-size: 12px;
      }
    }
  }
}

</style>


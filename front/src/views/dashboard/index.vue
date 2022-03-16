<template>
<div class="dashboard-container">
  <img src="/static/img/206.PNG" class="frontpic"/>
  <div style="font-size:32px;color:#130B52;text-align:center;margin-top:1%">欢迎使用</div> 
  <div style="font-size:32px;color:#130B52;text-align:center;margin-top:1%">设计所奖金核算管理系统</div> 
  <div style="font-size:32px;color:#130B52;text-align:center;margin-top:1%">(试行版)</div>
</div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'dashboard',
  computed: {
    ...mapGetters([
      'userName',
      'userId'
    ])
  },
  data(){
      return {
      }
  },
  created () {
  },
  methods: {
  },
  watch: {
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.dashboard {
  &-container {
    margin: 30px;
  }
}
.frontpic{
  width:50%;
  margin-top:5%;
  margin-left:25%
}
</style>

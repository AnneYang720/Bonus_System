import { login, logout, getInfo } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'
import  { resetRouter } from '@/router'

const user = {
  state: {
    username: '',
    userId:'',
    roles: [],
  },

  mutations: {
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_USERID: (state, userId) => {
      state.userId = userId
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo.worknum, userInfo.password).then( response => {
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          // TODO 之后取消注释
          // roles must be a non-empty array
          if (!response.data.roles || response.data.roles.length <= 0) {
            reject('getInfo: roles must be a non-null array!')
          }
          
          commit('SET_ROLES', response.data.roles)
          commit('SET_USERNAME', response.data.username)
          commit('SET_USERID', response.data.id)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        // logout(state.token).then(() => {
          // commit('SET_TOKEN', '')
          removeToken()
          resetRouter()
          resolve()
        // }).catch(error => {
        //   reject(error)
        // })
      })
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        // commit('SET_TOKEN', '')
        removeToken()
        resetRouter()
        resolve()
      })
    }
  }
}

export default user

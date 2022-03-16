import request from '@/utils/request'

export function login(worknum, password) {
  return request({
    url: '/login',
    method: 'post',
    data: {
      worknum,
      password
    }
  })
}

export function register(pojo){
  return request({
      url: '/signup',
      method: 'post',
      data: pojo
  })
}

export function getInfo() {
  return request({
    url: '/userinfo',
    method: 'get'
  })
}

export function changePwd(password) {
  return request({
    url: '/changepwd',
    method: 'post',
    data:{
      password
    }
  })
}

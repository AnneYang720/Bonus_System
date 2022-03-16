import Cookies from 'js-cookie'

const TokenKey = 'session'

export function getToken() {
  return Cookies.get(TokenKey)
  // return document.cookie
  // return true
}

// export function setToken(token) {
//   return Cookies.set(TokenKey, token)
// }

export function setToken() {
  return Cookies.set()
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

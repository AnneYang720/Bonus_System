const getters = {
  sidebar: state => state.app.sidebar,
  token: state => state.user.token,
  username: state => state.user.username,
  userId: state => state.user.userId,
  roles: state => state.user.roles,
  addRouters: state => state.permission.routers,
}
export default getters

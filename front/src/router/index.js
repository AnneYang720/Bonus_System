import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/register', component: () => import('@/views/register/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Dashboard',
    hidden: true,
    children: [{
      path: 'dashboard',
      component: () => import('@/views/dashboard/index')
    }]
  },


  { path: '*', redirect: '/404', hidden: true }
]

/**
 * asyncRouterMap
 * the routes that need to be dynamically loaded based on user roles
 */
 export const asyncRouterMap = [
  {
    path: '/planning',
    component: Layout,
    name: 'Planning',
    meta: { roles: ['admin','admin_ghfz'], title: '规划发展部', icon: 'example' },
    children: [
      {
        path: 'create',
        name: 'AddResearchProject',
        component: () => import('@/views/planning/create'),
        meta: { title: '新增项目绩效', icon: 'table', reuse: false }
      },
      {
        path: 'project',
        name: 'ResearchProject',
        component: () => import('@/views/planning/project'),
        meta: { title: '查看项目绩效', icon: 'table', reuse: false }
      },
    ]
  },

  {
    path: '/general',
    component: Layout,
    name: 'GeneralManagement',
    meta: { roles: ['admin','admin_zhgl', 'admin_zhgl_ky', 'admin_zhgl_gl', 'admin_user'], title: '综合管理部', icon: 'example' },
    children: [
      {
        path: 'project',
        name: 'ManagementProject',
        component: () => import('@/views/general/project'),
        meta: { title: '新建管理绩效', icon: 'table', roles: ['admin','admin_zhgl','admin_zhgl_gl'] }
      },
      {
        path: 'plan',
        name: 'BonusPlan',
        component: () => import('@/views/general/plan'),
        meta: { title: '发放计划', icon: 'table', roles: ['admin','admin_zhgl'] }
      },
      {
        path: 'grantres',
        name: 'GrantResearch',
        component: () => import('@/views/general/grantres'),
        meta: { title: '项目绩效发放', icon: 'table', roles: ['admin','admin_zhgl', 'admin_zhgl_ky'] }
      },
      {
        path: 'grantman',
        name: 'GrantManage',
        component: () => import('@/views/general/grantman'),
        meta: { title: '管理绩效发放', icon: 'table', roles: ['admin','admin_zhgl', 'admin_zhgl_gl']  }
      },
      {
        path: 'grantred',
        name: 'GrantReduce',
        component: () => import('@/views/general/grantred'),
        meta: { title: '绩效扣发', icon: 'table', roles: ['admin','admin_zhgl', 'admin_zhgl_gl']  }
      },
      {
        path: 'listres',
        name: 'ListResearch',
        component: () => import('@/views/general/listres'),
        meta: { title: '项目绩效总览', icon: 'table', roles: ['admin','admin_zhgl', 'admin_zhgl_ky']  }
      },
      {
        path: 'listman',
        name: 'ListManage',
        component: () => import('@/views/general/listman'),
        meta: { title: '管理绩效总览', icon: 'table', roles: ['admin','admin_zhgl', 'admin_zhgl_gl'] }
      },
      {
        path: 'list',
        name: 'ListAll',
        component: () => import('@/views/general/list'),
        meta: { title: '绩效总览', icon: 'table', roles: ['admin','admin_zhgl']  }
      },
      {
        path: 'employee',
        name: 'Employee',
        component: () => import('@/views/general/employee'),
        meta: { title: '人员管理', icon: 'table', roles: ['admin','admin_zhgl', 'admin_user']  }
      },
      {
        path: 'keshi',
        name: 'Keshi',
        component: () => import('@/views/general/keshi'),
        meta: { title: '科室管理', icon: 'table', roles: ['admin','admin_zhgl', 'admin_user'] }
      }
    ]
  },

  {
    path: '/project',
    component: Layout,
    name: 'ProjectManagement',
    meta: { roles: ['admin','manager_prom', 'manager_prok'], title: '项目经理', icon: 'example' },
    children: [
      {
        path: 'grantbig',
        name: 'GrantBig',
        component: () => import('@/views/project/grantbig'),
        meta: { title: '绩效发放(大)', icon: 'table', reuse: false  }
      },
      {
        path: 'grantsmall',
        name: 'GrantSmall',
        component: () => import('@/views/project/grantsmall'),
        meta: { title: '绩效发放(小)', icon: 'table', reuse: false  }
      },
      {
        path: 'list',
        name: 'List',
        component: () => import('@/views/project/list'),
        meta: { title: '绩效总览', icon: 'table', reuse: false  }
      }
    ]
  },

  {
    path: '/group',
    component: Layout,
    name: 'GroupManagement',
    meta: { roles: ['admin','manager_shi'], title: '室主任', icon: 'example' },
    children: [
      {
        path: 'grant',
        name: 'Grant',
        component: () => import('@/views/group/grant'),
        meta: { title: '绩效发放', icon: 'table', reuse: false }
      },
      {
        path: 'list',
        name: 'ListGroup',
        component: () => import('@/views/group/list'),
        meta: { title: '绩效总览', icon: 'table', reuse: false }
      }
    ]
  },

  {
    path: '/progress',
    component: Layout,
    name: 'Progress',
    meta: { roles: ['admin','admin_zhgl', 'admin_zhgl_ky', 'admin_zhgl_gl', 'admin_user','manager_shi','manager_prom', 'manager_prok'], title: '进度', icon: 'example' },
    children: [{
      path: 'info',
      name: 'Info',
      component: () => import('@/views/progress/index'),
      meta: { title: '进度', icon: 'table', reuse: false }
    }]
  },

  { path: '*', redirect: '/404', hidden: true }
]


const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export function selfaddRoutes(params) {
  router.matcher = new Router().matcher;
  router.addRoutes(params)
}

export default router





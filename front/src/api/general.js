import request from '@/utils/request'
export default{
    getUsersList(page,size){
        return request({
            url: `/general/getuserslist/${page}/${size}`,
            method: 'get'
        });
    },

    getKeshiList(){
        return request({
            url: `/general/getkeshilist`,
            method: 'get'
        });
    },

    getKeshiFullList(){
        return request({
            url: `/general/getkeshifulllist`,
            method: 'get'
        });
    },

    getCategoryList(){
        return request({
            url: `/general/getcategorylist`,
            method: 'get'
        });
    },

    changeUser(pojo){
        return request({
            url: '/general/changeuser',
            method: 'post',
            data: pojo
        })
    },

    addUser(pojo){
        return request({
            url: '/general/adduser',
            method: 'post',
            data: pojo
        })
    },

    search(page,size,keyword){
        return request({
            url: `/general/search/${page}/${size}?q=${keyword}`,//ES6写法
            method: 'get',
        });
    },

    getProjectList(){
        return request({
            url: `/general/getprojectlist`,
            method: 'get'
        });
    },

    createProject(pojo){
        return request({
            url: `/general/createproject`,
            method: 'post',
            data: pojo
        })
    },

    changeProject(pojo){
        return request({
            url: `/general/changeproject`,
            method: 'post',
            data: pojo
        })
    },

    delProject(projectId){
        return request({
            url: `/general/del/${projectId}`, //ES6写法
            method: 'delete',    
        })
    },

    getPlanList(){
        return request({
            url: `/general/getplanlist`,
            method: 'get'
        });
    },

    getShenPlanList(){
        return request({
            url: `/general/getshenplanlist`,
            method: 'get'
        });
    },

    getCurPlanList(){
        return request({
            url: `/general/getcurplanlist`,
            method: 'get'
        });
    },

    getProPlanList(){
        return request({
            url: `/general/getproplanlist`,
            method: 'get'
        });
    },

    getShiPlanList(){
        return request({
            url: `/general/getshiplanlist`,
            method: 'get'
        });
    },

    createPlan(pojo){
        return request({
            url: `/general/createplan`,
            method: 'post',
            data: pojo
        })
    },

    changePlan(pojo){
        return request({
            url: `/general/changeplan`,
            method: 'post',
            data: pojo
        })
    },

    getProjectDetailList(planId){
        return request({
            url: `/general/getprojectdetail/${planId}`, //ES6写法
            method: 'post',    
        })
    },

    getCurProjectList(){
        return request({
            url: `/general/getcurprojectlist`,
            method: 'get'
        });
    },


    addKeshi(pojo){
        return request({
            url: '/general/addkeshi',
            method: 'post',
            data: pojo
        })
    },

    changeKeshi(pojo){
        return request({
            url: '/general/changekeshi',
            method: 'post',
            data: pojo
        })
    },

    delKeshi(id){
        return request({
            url: `/general/delkeshi/${id}`, //ES6写法
            method: 'delete',    
        })
    },

    getResAllDetail(planId,page,size){
        return request({
            url: `/general/getresdetail/${planId}/${page}/${size}`, //ES6写法
            method: 'get',    
        })
    },

    getManAllDetail(planId,page,size){
        return request({
            url: `/general/getmandetail/${planId}/${page}/${size}`, //ES6写法
            method: 'get',    
        })
    },

    getResHistory(pojo){
        return request({
            url: `/general/getreshistory`, //ES6写法
            method: 'post',
            data: pojo
        })
    },

    getManHistory(pojo){
        return request({
            url: `/general/getmanhistory`, //ES6写法
            method: 'post',
            data: pojo
        })
    },

    getAllDetail(planId){
        return request({
            url: `/general/getdetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

} 

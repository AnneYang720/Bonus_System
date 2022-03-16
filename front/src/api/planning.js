import request from '@/utils/request'
export default{
    getProjectList(page,size){
        return request({
            url: `/planning/getprojectlist/${page}/${size}`,
            method: 'get'
        });
    },

    createProject(pojo){
        return request({
            url: `/planning/create`,
            method: 'post',
            data: pojo
        })
    },

    changeProject(pojo){
        return request({
            url: `/planning/change`,
            method: 'post',
            data: pojo
        })
    },

    getCurProjectList(){
        return request({
            url: `/planning/getcurprojectlist`,
            method: 'get'
        });
    },

    getProjectDetailList(planId){
        return request({
            url: `/planning/getprojectdetail/${planId}`, //ES6写法
            method: 'post',    
        })
    },

    search(page,size,keyword){
        return request({
            url: `/planning/search/${page}/${size}?q=${keyword}`,//ES6写法
            method: 'get',
        });
    },

    importProjects(rows){
        return request({
            url: `/planning/importprojects`,
            method: 'post',
            data: {
                rows
            }
        })
    },

} 

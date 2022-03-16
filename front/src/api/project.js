import request from '@/utils/request'
export default{

    getMyBigProjectList(planId){
        return request({
            url: `/project/getmybigproject/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getMySmallProjectList(planId){
        return request({
            url: `/project/getmysmallproject/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getProgressList(planId){
        return request({
            url: `/project/getprogress/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getBigProjectDetail(pojo){
        return request({
            url: `/project/getbigprojectdetail`, //ES6写法
            method: 'post',    
            data: pojo
        })
    },

    getProjectMember(pojo){
        return request({
            url: `/project/getmember`, //ES6写法
            method: 'post',    
            data: pojo
        })
    },

    addMember(pojo){
        return request({
            url: `/project/addmember`, //ES6写法
            method: 'post',   
            data: pojo 
        })
    },

    delMember(id,planId){
        return request({
            url: `/project/delmember/${id}/${planId}`, //ES6写法
            method: 'delete'
        })
    },

    getMemberDetail(pojo){
        return request({
            url: `/project/getmemberdetail`, //ES6写法
            method: 'post',    
            data: pojo
        })
    },

    getMemberDetailExport(pojo){
        return request({
            url: `/project/getmemberdetailexport`, //ES6写法
            method: 'post',    
            data: pojo
        })
    },

    changeMemberDetail(pojo){
        return request({
            url: `/project/changememberdetail`, //ES6写法
            method: 'post',   
            data: pojo 
        })
    },   

    importMemberDetail(form,rows){
        return request({
            url: `/project/importmemberdetail`, //ES6写法
            method: 'post',  
            data: {
                form,
                rows
            }
        })
    },

    createAllKeshiDetail(pojo){
        return request({
            url: `/project/createallkeshidetail`,
            method: 'post',
            data: pojo
        })
    },

    createKeshiDetail(pojo){
        return request({
            url: `/project/createkeshidetail`,
            method: 'post',
            data: pojo
        })
    },

    changeKeshiDetail(pojo){
        return request({
            url: `/project/changekeshidetail`,
            method: 'post',
            data: pojo
        })
    },

    delKeshiDetail(detailId){
        return request({
            url: `/project/delkeshi/${detailId}`, //ES6写法
            method: 'delete',    
        })
    },

    getAllDetail(planId){
        return request({
            url: `/project/getdetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getHistory(pojo){
        return request({
            url: `/project/gethistory`, //ES6写法
            method: 'post',
            data: pojo
        })
    },

    getManProjectDetailList(planId){
        return request({
            url: `/detail/getmanprojectdetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    createManDetail(pojo){
        return request({
            url: `/detail/createmandetail`,
            method: 'post',
            data: pojo
        })
    },

} 

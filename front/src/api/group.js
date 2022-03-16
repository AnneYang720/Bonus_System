import request from '@/utils/request'
export default{

    getKeshiProjectList(planId){
        return request({
            url: `/group/getkeshiproject/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getProgressList(planId){
        return request({
            url: `/group/getprogress/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getMemberDetail(pojo){
        return request({
            url: `/group/getmemberdetail`, //ES6写法
            method: 'post',
            data: pojo
        })
    },

    exportMemberDetail(pojo){
        return request({
            url: `/group/exportmemberdetail`, //ES6写法
            method: 'post',
            data: pojo
        })
    },


    changeMemberDetail(pojo){
        return request({
            url: `/group/changememberdetail`, //ES6写法
            method: 'post',   
            data: pojo 
        })
    },

    importMemberDetail(form,rows){
        return request({
            url: `/group/importmemberdetail`, //ES6写法
            method: 'post',  
            data: {
                form,
                rows
            }
        })
    },

    getKeshiAllDetail(planId){
        return request({
            url: `/group/getkeshidetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getHistory(pojo){
        return request({
            url: `/group/gethistory`, //ES6写法
            method: 'post',
            data: pojo
        })
    },

    getKeshiMember(keshiId){
        return request({
            url: `/group/getkeshimember/${keshiId}`, //ES6写法
            method: 'get',    
        })
    },

    importKeshiDetail(form,rows,proDetailList){
        return request({
            url: `/group/importkeshidetail`, //ES6写法
            method: 'post',  
            data: {
                form,
                rows,
                proDetailList
            }
        })
    },


} 

import request from '@/utils/request'
export default{

    getResProjectDetailList(planId){
        return request({
            url: `/detail/getresprojectdetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getAllResProjectDetailList(planId){
        return request({
            url: `/detail/getallresprojectdetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    getManProjectDetailList(planId){
        return request({
            url: `/detail/getmanprojectdetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    createResDetail(pojo){
        return request({
            url: `/detail/createresdetail`,
            method: 'post',
            data: pojo
        })
    },

    createResDetailFromFile(planId,rows){
        return request({
            url: `/detail/importresdetail`,
            method: 'post',
            data: {
                planId,
                rows
            }
        })
    },

    createManDetail(pojo){
        return request({
            url: `/detail/createmandetail`,
            method: 'post',
            data: pojo
        })
    },

    changeDetail(pojo){
        return request({
            url: `/detail/changedetail`,
            method: 'post',
            data: pojo
        })
    },

    delDetail(detailId){
        return request({
            url: `/detail/del/${detailId}`, //ES6写法
            method: 'delete',    
        })
    },

    getKoufaDetailList(planId){
        return request({
            url: `/detail/getkoufadetail/${planId}`, //ES6写法
            method: 'get',    
        })
    },

    createKoufaDetail(pojo){
        return request({
            url: `/detail/createkoufadetail`,
            method: 'post',
            data: pojo
        })
    },

    changeKoufaDetail(pojo){
        return request({
            url: `/detail/changekoufadetail`,
            method: 'post',
            data: pojo
        })
    },

    delKoufaDetail(detailId){
        return request({
            url: `/detail/delkoufa/${detailId}`, //ES6写法
            method: 'delete',    
        })
    },
} 

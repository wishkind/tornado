const axios = require('axios')
axios.defaults.baseURL = 'https://127.0.0.1:8888/api'
// 配置超时时间
axios.defaults.timeout = 3000;
// 配置公共请求头
const AUTH_TOKEN = 0;
axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
//配置公共的post的Content-Type
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
//1.请求拦截器
axios.interceptors.request.use(function(config){
    console.log(config.url)
    //任何一部都会经过这一步,在发送请求前做些什么
    config.headers.mytoken = 'token字符串'
    //这里一定要return 否则配置不成功
    return config
},function(err){
    //请求错误的时候
    console.log(err)
})
//2.响应拦截器
axios.interceptors.response.use(function(res){
    //接收响应后做些什么
    var data = res.data;
    return data;
},function(err){
    //打印错误
    console.log(err)
})

//1. 发送get 请求 
axios.get('http://localhost:8888/adata').then(function(ret){ 
      //  拿到 ret 是一个对象      所有的对象都存在 ret 的data 属性里面
      // 注意data属性是固定的用法，用于获取后台的实际数据
    console.log(ret.data)
    console.log(ret)
    })
	// 2.  get 请求传递参数
    // 2.1  通过传统的url  以 ? 的形式传递参数
axios.get('http://localhost:8888/axios?id=123').then(function(ret){
    console.log(ret.data)
    })
    // 2.2  restful 形式传递参数 
axios.get('http://localhost:8888/axios/123').then(function(ret){
      console.log(ret.data)
    })
	// 2.3  通过params  形式传递参数 
axios.get('http://localhost:8888/axios', {
      params: {
        id: 789
      }
    }).then(function(ret){
      console.log(ret.data)
    })
	//3 axios delete 请求传参     传参的形式和 get 请求一样
axios.delete('http://localhost:8888/axios', {
      params: {
        id: 111
      }
    }).then(function(ret){
      console.log(ret.data)
    })

	// 4  axios 的 post 请求
    // 4.1  通过选项传递参数
axios.post('http://localhost:8888/axios', {
      uname: 'lisi',
      pwd: 123
    }).then(function(ret){
      console.log(ret.data)
    })
	// 4.2  通过 URLSearchParams  传递参数 
var params = new URLSearchParams();
params.append('uname', 'zhangsan');
params.append('pwd', '111');
axios.post('http://localhost:8888/axios', params).then(function(ret){
      console.log(ret.data)
    })

 	//5  axios put 请求传参   和 post 请求一样 
axios.put('http://localhost:8888/axios/123', {
      uname: 'lisi',
      pwd: 123
    }).then(function(ret){
      console.log(ret.data)
    })


async function queryData() {
      // 2.1  添加await之后 当前的await 返回结果之后才会执行后面的代码   
      
      var info = await axios.get('async1');
      //2.2  让异步代码看起来、表现起来更像同步代码
      var ret = await axios.get('async2?info=' + info.data);
      return ret.data;
    }

queryData().then(function(data){
      console.log(data)
    })


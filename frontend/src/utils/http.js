import axios from 'axios'

// 根据运行环境切换后端地址：
// - 开发环境：指向本地 Flask 服务
// - 生产（打包后部署）：使用相对路径，与站点同域
const baseURL = (import.meta.env && import.meta.env.VITE_API_BASE)
  || (import.meta.env && import.meta.env.DEV ? 'http://127.0.0.1:5000' : '/')

// 创建axios实例
const service = axios.create({
  baseURL,
  timeout: 200000,
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    return Promise.reject(error)
  }
)

export default service

import axios from 'axios'

// 获取 API 地址
// 开发环境：使用当前主机的 IP 地址
// 生产环境：使用相对路径
const getBaseURL = () => {
  // 如果是生产环境，使用相对路径
  if (import.meta.env.PROD) {
    return '/api'
  }
  
  // 开发环境：使用当前页面的 hostname
  // 这样手机和电脑都能正确访问
  const hostname = window.location.hostname
  return `http://${hostname}:8000/api`
}

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000 // 增加超时时间到10秒
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log(`[API请求] ${config.method?.toUpperCase()} ${config.url}`)
    console.log(`[API地址] ${config.baseURL}`)
    return config
  },
  error => {
    console.error('[API请求错误]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log(`[API响应] ${response.config.url} - 状态: ${response.status}`)
    return response.data
  },
  error => {
    console.error('[API响应错误]', error)
    if (error.response) {
      // 服务器返回了错误状态码
      console.error(`[错误详情] 状态码: ${error.response.status}`, error.response.data)
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.error('[错误详情] 无法连接到服务器，请检查：')
      console.error('1. 后端服务是否正在运行？')
      console.error('2. 防火墙是否允许8000端口？')
      console.error(`3. 手机是否与电脑在同一网络？`)
      console.error(`4. 当前API地址: ${error.config?.baseURL}`)
    } else {
      // 请求配置出错
      console.error('[错误详情]', error.message)
    }
    return Promise.reject(error)
  }
)

// 用户API
export const userAPI = {
  getUsers: () => api.get('/users/'),
  getUser: (id) => api.get(`/users/${id}`),
  createUser: (data) => api.post('/users/', data),
  deleteUser: (id) => api.delete(`/users/${id}`)
}

// 会议室API
export const roomAPI = {
  getRooms: () => api.get('/rooms/'),
  getRoom: (id) => api.get(`/rooms/${id}`),
  createRoom: (data) => api.post('/rooms/', data),
  updateRoom: (id, data) => api.put(`/rooms/${id}`, data),
  deleteRoom: (id) => api.delete(`/rooms/${id}`)
}

// 预约API
export const bookingAPI = {
  getBookings: () => api.get('/bookings/'),
  getBooking: (id) => api.get(`/bookings/${id}`),
  getUserBookings: (userId) => api.get(`/bookings/user/${userId}`),
  getRoomBookings: (roomId) => api.get(`/bookings/room/${roomId}`),
  createBooking: (data) => api.post('/bookings/', data),
  cancelBooking: (id) => api.put(`/bookings/${id}/cancel`),
  deleteBooking: (id) => api.delete(`/bookings/${id}`)
}

export default api


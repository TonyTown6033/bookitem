import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
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


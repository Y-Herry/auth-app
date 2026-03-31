import request from '../utils/request'

// 注册
export const register = data => request.post('/auth/register', data)

// 登录
export const login = data => request.post('/auth/login', data)

// 获取用户信息
export const getProfile = () => request.get('/auth/profile')

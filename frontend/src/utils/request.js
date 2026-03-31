import axios from 'axios'

const request = axios.create({
	baseURL: '/api',
	timeout: 10000
})

// 请求拦截器：自动携带 Token
request.interceptors.request.use(
	config => {
		const token = localStorage.getItem('token')
		if (token) {
			config.headers['Authorization'] = `Bearer ${token}`
		}
		return config
	},
	error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
	response => response.data,
	error => {
		const msg = error.response?.data?.message || '请求失败，请稍后重试'
		return Promise.reject(new Error(msg))
	}
)

export default request

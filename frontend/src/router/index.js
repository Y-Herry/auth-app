import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
	{ path: '/', redirect: '/login' },
	{ path: '/login', name: 'Login', component: Login },
	{ path: '/register', name: 'Register', component: Register },
	{
		path: '/home',
		name: 'Home',
		component: Home,
		meta: { requiresAuth: true }
	}
]

const router = new VueRouter({
	mode: 'history',
	routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
	const token = localStorage.getItem('token')
	if (to.meta.requiresAuth && !token) {
		next('/login')
	} else {
		next()
	}
})

export default router

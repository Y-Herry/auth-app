<template>
	<div class="home-container">
		<div class="home-card">
			<div class="home-header">
				<span class="home-icon">🏠</span>
				<h1>欢迎回来！</h1>
				<p class="welcome-text">你已成功登录系统</p>
			</div>
			<div class="user-info" v-if="userInfo">
				<div class="info-item">
					<span class="info-label">👤 用户名</span>
					<span class="info-value">{{ userInfo.username }}</span>
				</div>
				<div class="info-item">
					<span class="info-label">📧 邮箱</span>
					<span class="info-value">{{ userInfo.email }}</span>
				</div>
			</div>
			<button class="btn-logout" @click="handleLogout">退出登录</button>
		</div>
	</div>
</template>

<script>
export default {
	name: 'Home',
	data() {
		return { userInfo: null }
	},
	created() {
		const info = localStorage.getItem('userInfo')
		if (info) this.userInfo = JSON.parse(info)
	},
	methods: {
		handleLogout() {
			localStorage.removeItem('token')
			localStorage.removeItem('userInfo')
			this.$router.push('/login')
		}
	}
}
</script>

<style scoped>
.home-container {
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%;
	padding: 20px;
}
.home-card {
	background: #fff;
	border-radius: 20px;
	padding: 48px 40px;
	width: 100%;
	max-width: 440px;
	box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
	animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
	from {
		opacity: 0;
		transform: translateY(30px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}
.home-header {
	text-align: center;
	margin-bottom: 32px;
}
.home-icon {
	font-size: 52px;
	display: block;
	margin-bottom: 12px;
}
.home-header h1 {
	font-size: 26px;
	font-weight: 700;
	color: #2d3748;
	margin-bottom: 6px;
}
.welcome-text {
	color: #718096;
	font-size: 14px;
}
.user-info {
	background: #f7fafc;
	border-radius: 14px;
	padding: 20px;
	margin-bottom: 28px;
}
.info-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px 0;
	border-bottom: 1px solid #e2e8f0;
}
.info-item:last-child {
	border-bottom: none;
}
.info-label {
	font-size: 14px;
	color: #718096;
}
.info-value {
	font-size: 14px;
	font-weight: 600;
	color: #2d3748;
}
.btn-logout {
	width: 100%;
	padding: 13px;
	background: linear-gradient(135deg, #fc5c7d, #6a3093);
	color: #fff;
	border: none;
	border-radius: 12px;
	font-size: 16px;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s;
}
.btn-logout:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 25px rgba(252, 92, 125, 0.4);
}
</style>

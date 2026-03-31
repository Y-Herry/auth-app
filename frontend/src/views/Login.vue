<template>
	<div class="auth-container">
		<div class="auth-card">
			<!-- Logo -->
			<div class="auth-logo">
				<span class="logo-icon">🔐</span>
				<h1 class="logo-text">欢迎登录</h1>
				<p class="logo-sub">请输入您的账号和密码</p>
			</div>

			<!-- 表单 -->
			<form @submit.prevent="handleLogin" class="auth-form">
				<div class="form-group" :class="{ error: errors.username }">
					<label>用户名 / 邮箱</label>
					<div class="input-wrapper">
						<span class="input-icon">👤</span>
						<input v-model="form.username" type="text" placeholder="请输入用户名或邮箱" @input="clearError('username')" />
					</div>
					<span v-if="errors.username" class="error-msg">{{ errors.username }}</span>
				</div>

				<div class="form-group" :class="{ error: errors.password }">
					<label>密码</label>
					<div class="input-wrapper">
						<span class="input-icon">🔒</span>
						<input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码" @input="clearError('password')" />
						<span class="input-toggle" @click="showPassword = !showPassword">
							{{ showPassword ? '🙈' : '👁️' }}
						</span>
					</div>
					<span v-if="errors.password" class="error-msg">{{ errors.password }}</span>
				</div>

				<!-- 提示信息 -->
				<div v-if="alertMsg" class="alert" :class="alertType">
					{{ alertMsg }}
				</div>

				<button type="submit" class="btn-primary" :disabled="loading">
					<span v-if="loading" class="loading-spinner"></span>
					{{ loading ? '登录中...' : '立即登录' }}
				</button>
			</form>

			<div class="auth-footer">
				<span>还没有账号？</span>
				<router-link to="/register" class="link">立即注册</router-link>
			</div>
		</div>
	</div>
</template>

<script>
import { login } from '../api/auth'

export default {
	name: 'Login',
	data() {
		return {
			form: { username: '', password: '' },
			errors: {},
			alertMsg: '',
			alertType: '',
			loading: false,
			showPassword: false
		}
	},
	methods: {
		clearError(field) {
			this.$delete(this.errors, field)
			this.alertMsg = ''
		},
		validate() {
			const errs = {}
			if (!this.form.username.trim()) errs.username = '请输入用户名或邮箱'
			if (!this.form.password) errs.password = '请输入密码'
			this.errors = errs
			return Object.keys(errs).length === 0
		},
		async handleLogin() {
			if (!this.validate()) return
			this.loading = true
			this.alertMsg = ''
			try {
				const res = await login({ username: this.form.username, password: this.form.password })
				localStorage.setItem('token', res.data.token)
				localStorage.setItem('userInfo', JSON.stringify(res.data.user))
				this.alertMsg = '登录成功，即将跳转...'
				this.alertType = 'success'
				setTimeout(() => this.$router.push('/home'), 1000)
			} catch (err) {
				this.alertMsg = err.message || '登录失败'
				this.alertType = 'danger'
			} finally {
				this.loading = false
			}
		}
	}
}
</script>

<style scoped>
.auth-container {
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%;
	padding: 20px;
}

.auth-card {
	background: #fff;
	border-radius: 20px;
	padding: 48px 40px;
	width: 100%;
	max-width: 420px;
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

.auth-logo {
	text-align: center;
	margin-bottom: 36px;
}

.logo-icon {
	font-size: 48px;
	display: block;
	margin-bottom: 12px;
}
.logo-text {
	font-size: 26px;
	font-weight: 700;
	color: #2d3748;
	margin-bottom: 6px;
}
.logo-sub {
	color: #718096;
	font-size: 14px;
}

.form-group {
	margin-bottom: 20px;
}

.form-group label {
	display: block;
	font-size: 14px;
	font-weight: 600;
	color: #4a5568;
	margin-bottom: 8px;
}

.input-wrapper {
	position: relative;
	display: flex;
	align-items: center;
	background: #f7fafc;
	border: 2px solid #e2e8f0;
	border-radius: 12px;
	transition: all 0.3s;
}

.input-wrapper:focus-within {
	border-color: #667eea;
	background: #fff;
	box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.form-group.error .input-wrapper {
	border-color: #e53e3e;
}

.input-icon {
	padding: 0 12px;
	font-size: 16px;
}

.input-wrapper input {
	flex: 1;
	padding: 12px 0;
	border: none;
	background: transparent;
	font-size: 15px;
	color: #2d3748;
	outline: none;
}

.input-toggle {
	padding: 0 14px;
	cursor: pointer;
	font-size: 16px;
	user-select: none;
}

.error-msg {
	display: block;
	color: #e53e3e;
	font-size: 12px;
	margin-top: 5px;
}

.alert {
	padding: 12px 16px;
	border-radius: 10px;
	font-size: 14px;
	margin-bottom: 16px;
	text-align: center;
}

.alert.success {
	background: #f0fff4;
	color: #276749;
	border: 1px solid #9ae6b4;
}
.alert.danger {
	background: #fff5f5;
	color: #c53030;
	border: 1px solid #feb2b2;
}

.btn-primary {
	width: 100%;
	padding: 14px;
	background: linear-gradient(135deg, #667eea, #764ba2);
	color: #fff;
	border: none;
	border-radius: 12px;
	font-size: 16px;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	margin-top: 8px;
}

.btn-primary:hover:not(:disabled) {
	transform: translateY(-2px);
	box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
	opacity: 0.7;
	cursor: not-allowed;
}

.loading-spinner {
	width: 18px;
	height: 18px;
	border: 2px solid rgba(255, 255, 255, 0.4);
	border-top-color: #fff;
	border-radius: 50%;
	animation: spin 0.8s linear infinite;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.auth-footer {
	text-align: center;
	margin-top: 24px;
	font-size: 14px;
	color: #718096;
}

.link {
	color: #667eea;
	font-weight: 600;
	text-decoration: none;
	margin-left: 4px;
}

.link:hover {
	text-decoration: underline;
}
</style>

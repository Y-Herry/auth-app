<template>
	<div class="auth-container">
		<div class="auth-card">
			<div class="auth-logo">
				<span class="logo-icon">✨</span>
				<h1 class="logo-text">创建账号</h1>
				<p class="logo-sub">填写以下信息完成注册</p>
			</div>

			<form @submit.prevent="handleRegister" class="auth-form">
				<div class="form-group" :class="{ error: errors.username }">
					<label>用户名</label>
					<div class="input-wrapper">
						<span class="input-icon">👤</span>
						<input v-model="form.username" type="text" placeholder="请输入用户名（2-50个字符）" @input="clearError('username')" />
					</div>
					<span v-if="errors.username" class="error-msg">{{ errors.username }}</span>
				</div>

				<div class="form-group" :class="{ error: errors.email }">
					<label>邮箱</label>
					<div class="input-wrapper">
						<span class="input-icon">📧</span>
						<input v-model="form.email" type="text" placeholder="请输入邮箱地址" @input="clearError('email')" />
					</div>
					<span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
				</div>

				<div class="form-group" :class="{ error: errors.password }">
					<label>密码</label>
					<div class="input-wrapper">
						<span class="input-icon">🔒</span>
						<input
							v-model="form.password"
							:type="showPassword ? 'text' : 'password'"
							placeholder="请输入密码（至少6位）"
							@input="clearError('password')"
						/>
						<span class="input-toggle" @click="showPassword = !showPassword">
							{{ showPassword ? '🙈' : '👁️' }}
						</span>
					</div>
					<span v-if="errors.password" class="error-msg">{{ errors.password }}</span>
				</div>

				<div class="form-group" :class="{ error: errors.confirmPassword }">
					<label>确认密码</label>
					<div class="input-wrapper">
						<span class="input-icon">🔏</span>
						<input
							v-model="form.confirmPassword"
							:type="showConfirm ? 'text' : 'password'"
							placeholder="请再次输入密码"
							@input="clearError('confirmPassword')"
						/>
						<span class="input-toggle" @click="showConfirm = !showConfirm">
							{{ showConfirm ? '🙈' : '👁️' }}
						</span>
					</div>
					<span v-if="errors.confirmPassword" class="error-msg">{{ errors.confirmPassword }}</span>
				</div>

				<!-- 密码强度 -->
				<div v-if="form.password" class="password-strength">
					<div class="strength-bar">
						<div class="strength-fill" :class="strengthClass" :style="{ width: strengthWidth }"></div>
					</div>
					<span class="strength-label" :class="strengthClass">{{ strengthText }}</span>
				</div>

				<div v-if="alertMsg" class="alert" :class="alertType">{{ alertMsg }}</div>

				<button type="submit" class="btn-primary" :disabled="loading">
					<span v-if="loading" class="loading-spinner"></span>
					{{ loading ? '注册中...' : '立即注册' }}
				</button>
			</form>

			<div class="auth-footer">
				<span>已有账号？</span>
				<router-link to="/login" class="link">立即登录</router-link>
			</div>
		</div>
	</div>
</template>

<script>
import { register } from '../api/auth'

export default {
	name: 'Register',
	data() {
		return {
			form: { username: '', email: '', password: '', confirmPassword: '' },
			errors: {},
			alertMsg: '',
			alertType: '',
			loading: false,
			showPassword: false,
			showConfirm: false
		}
	},
	computed: {
		passwordStrength() {
			const p = this.form.password
			if (!p) return 0
			let score = 0
			if (p.length >= 6) score++
			if (p.length >= 10) score++
			if (/[A-Z]/.test(p)) score++
			if (/[0-9]/.test(p)) score++
			if (/[^A-Za-z0-9]/.test(p)) score++
			return score
		},
		strengthClass() {
			const s = this.passwordStrength
			if (s <= 1) return 'weak'
			if (s <= 3) return 'medium'
			return 'strong'
		},
		strengthWidth() {
			return `${Math.min(this.passwordStrength * 20, 100)}%`
		},
		strengthText() {
			const s = this.passwordStrength
			if (s <= 1) return '弱'
			if (s <= 3) return '中等'
			return '强'
		}
	},
	methods: {
		clearError(field) {
			this.$delete(this.errors, field)
			this.alertMsg = ''
		},
		validate() {
			const errs = {}
			const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
			if (!this.form.username.trim()) {
				errs.username = '请输入用户名'
			} else if (this.form.username.length < 2) {
				errs.username = '用户名至少2个字符'
			}
			if (!this.form.email.trim()) {
				errs.email = '请输入邮箱'
			} else if (!emailRegex.test(this.form.email)) {
				errs.email = '邮箱格式不正确'
			}
			if (!this.form.password) {
				errs.password = '请输入密码'
			} else if (this.form.password.length < 6) {
				errs.password = '密码至少6位'
			}
			if (!this.form.confirmPassword) {
				errs.confirmPassword = '请确认密码'
			} else if (this.form.password !== this.form.confirmPassword) {
				errs.confirmPassword = '两次密码不一致'
			}
			this.errors = errs
			return Object.keys(errs).length === 0
		},
		async handleRegister() {
			if (!this.validate()) return
			this.loading = true
			this.alertMsg = ''
			try {
				await register({
					username: this.form.username,
					email: this.form.email,
					password: this.form.password
				})
				this.alertMsg = '注册成功！即将跳转到登录页...'
				this.alertType = 'success'
				setTimeout(() => this.$router.push('/login'), 1500)
			} catch (err) {
				this.alertMsg = err.message || '注册失败'
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
	padding: 40px;
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
	margin-bottom: 28px;
}
.logo-icon {
	font-size: 44px;
	display: block;
	margin-bottom: 10px;
}
.logo-text {
	font-size: 24px;
	font-weight: 700;
	color: #2d3748;
	margin-bottom: 6px;
}
.logo-sub {
	color: #718096;
	font-size: 14px;
}
.form-group {
	margin-bottom: 16px;
}
.form-group label {
	display: block;
	font-size: 14px;
	font-weight: 600;
	color: #4a5568;
	margin-bottom: 6px;
}
.input-wrapper {
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
	padding: 11px 0;
	border: none;
	background: transparent;
	font-size: 14px;
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
	margin-top: 4px;
}
.password-strength {
	display: flex;
	align-items: center;
	gap: 10px;
	margin-bottom: 12px;
}
.strength-bar {
	flex: 1;
	height: 6px;
	background: #e2e8f0;
	border-radius: 3px;
	overflow: hidden;
}
.strength-fill {
	height: 100%;
	border-radius: 3px;
	transition: all 0.4s;
}
.strength-fill.weak {
	background: #e53e3e;
}
.strength-fill.medium {
	background: #ed8936;
}
.strength-fill.strong {
	background: #38a169;
}
.strength-label {
	font-size: 12px;
	font-weight: 600;
	min-width: 28px;
}
.strength-label.weak {
	color: #e53e3e;
}
.strength-label.medium {
	color: #ed8936;
}
.strength-label.strong {
	color: #38a169;
}
.alert {
	padding: 11px 14px;
	border-radius: 10px;
	font-size: 14px;
	margin-bottom: 14px;
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
	padding: 13px;
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
	margin-top: 20px;
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

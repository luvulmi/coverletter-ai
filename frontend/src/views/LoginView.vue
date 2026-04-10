<template>
  <div class="login-wrap">
    <div class="login-card">

      <div class="logo">
        <span class="logo-icon">✦</span>
        <span class="logo-text">커버레터 AI</span>
      </div>

      <div class="tab-group">
        <button
          :class="['tab', { active: isLogin }]"
          @click="isLogin = true"
        >로그인</button>
        <button
          :class="['tab', { active: !isLogin }]"
          @click="isLogin = false"
        >회원가입</button>
      </div>

      <form @submit.prevent="submit">
        <div class="field">
          <label>이메일</label>
          <input
            v-model="email"
            type="email"
            placeholder="example@email.com"
            required
          />
        </div>
        <div class="field">
          <label>비밀번호</label>
          <input
            v-model="password"
            type="password"
            placeholder="비밀번호 입력"
            required
          />
        </div>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '처리 중...' : isLogin ? '로그인' : '회원가입' }}
        </button>
      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

const submit = async () => {
  errorMsg.value = ''
  loading.value = true
  try {
    if (isLogin.value) {
      await authStore.login(email.value, password.value)
    } else {
      await authStore.register(email.value, password.value)
    }
    router.push('/')
  } catch {
    errorMsg.value = '이메일 또는 비밀번호를 확인해주세요'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
}
.login-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 28px;
}
.logo-icon {
  font-size: 22px;
  color: #7F77DD;
}
.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}
.tab-group {
  display: flex;
  gap: 4px;
  background: #f1f5f9;
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 28px;
}
.tab {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  background: transparent;
  color: #94a3b8;
  transition: all 0.15s;
}
.tab.active {
  background: #fff;
  color: #1e293b;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.field {
  margin-bottom: 16px;
}
.field label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  margin-bottom: 6px;
}
.field input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s;
}
.field input:focus {
  border-color: #7F77DD;
}
.error {
  font-size: 13px;
  color: #ef4444;
  margin-bottom: 12px;
}
.submit-btn {
  width: 100%;
  padding: 12px;
  background: #7F77DD;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 4px;
  transition: background 0.15s;
}
.submit-btn:hover {
  background: #6c63d4;
}
.submit-btn:disabled {
  background: #c4c1ee;
  cursor: not-allowed;
}
</style>

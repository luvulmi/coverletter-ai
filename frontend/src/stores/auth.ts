import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

// 인증 상태 관리 스토어
export const useAuthStore = defineStore('auth', () => {
  // 토큰
  const token = ref<string | null>(localStorage.getItem('access_token'))
  // 로그인 여부
  const isLoggedIn = computed(() => !!token.value)

  // 회원가입
  const register = async (email: string, password: string) => {
    const res = await api.post('/auth/register', { email, password })

    // 회원가입 후 자동 로그인
    token.value = res.data.access_token
    localStorage.setItem('access_token', res.data.access_token)
  }

  // 로그인
  const login = async (email: string, password: string) => {
    const res = await api.post('/auth/login', { email, password })
    token.value = res.data.access_token
    localStorage.setItem('access_token', res.data.access_token)
  }

  // 로그아웃
  const logout = () => {
    token.value = null
    localStorage.removeItem('access_token')
  }

  return { token, isLoggedIn, register, login, logout }
})

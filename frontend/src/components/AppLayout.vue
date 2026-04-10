<template>
  <div class="wrap">

    <nav class="nav">
      <div class="nav-logo">
        <RouterLink to="/" class="logo">
          <span class="logo-icon">✦</span>
          <span class="logo-text">커버레터 AI</span>
        </RouterLink>
      </div>
      <div class="nav-links">
        <RouterLink to="/resume">내 이력서</RouterLink>
        <RouterLink to="/generate">커버레터 생성</RouterLink>
        <RouterLink to="/history">히스토리</RouterLink>
        <button class="logout-btn" @click="handleLogout">로그아웃</button>
      </div>
    </nav>

    <div class="page">
      <!-- 각 페이지 내용이 여기 들어옴 -->
      <slot />
    </div>

  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.wrap {
  min-height: 100vh;
  background: #f8fafc;
}
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 10;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}
.logo-icon { font-size: 18px; color: #7F77DD; }
.logo-text { font-size: 16px; font-weight: 600; color: #1e293b; }
.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}
.nav-links a {
  font-size: 14px;
  color: #64748b;
  text-decoration: none;
  transition: color 0.15s;
}
.nav-links a:hover { color: #1e293b; }
.nav-links a.router-link-active { color: #7F77DD; font-weight: 500; }
.logout-btn {
  font-size: 14px;
  color: #94a3b8;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.15s;
}
.logout-btn:hover { color: #ef4444; }
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}
</style>

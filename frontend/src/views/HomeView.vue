<template>
  <AppLayout>
    <div class="hero">
      <h1>안녕하세요 👋</h1>
      <p class="hero-sub">JD와 이력서를 입력하면 AI가 맞춤 커버레터를 만들어드려요</p>
      <RouterLink to="/generate" class="cta-btn">커버레터 생성하기 →</RouterLink>
    </div>

    <div class="cards">
      <RouterLink to="/resume" class="card">
        <div class="card-icon" style="background:#EEEDFE; color:#7F77DD">📄</div>
        <div class="card-body">
          <div class="card-title">내 이력서</div>
          <div class="card-desc">이력서를 저장해두면 매번 붙여넣을 필요 없어요</div>
        </div>
        <span class="card-arrow">→</span>
      </RouterLink>

      <RouterLink to="/generate" class="card">
        <div class="card-icon" style="background:#ECFDF5; color:#059669">✨</div>
        <div class="card-body">
          <div class="card-title">커버레터 생성</div>
          <div class="card-desc">JD를 붙여넣으면 AI가 맞춤 커버레터를 생성해요</div>
        </div>
        <span class="card-arrow">→</span>
      </RouterLink>

      <RouterLink to="/history" class="card">
        <div class="card-icon" style="background:#FFF7ED; color:#D97706">🗂</div>
        <div class="card-body">
          <div class="card-title">히스토리</div>
          <div class="card-desc">저장된 커버레터를 모아보고 다시 불러올 수 있어요</div>
        </div>
        <span class="card-arrow">→</span>
      </RouterLink>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.home-wrap {
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
.nav-logo {
  display: flex;
  align-items: center;
  gap: 8px;
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
.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 60px 20px;
}
.hero {
  text-align: center;
  margin-bottom: 56px;
}
h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}
.hero-sub {
  font-size: 16px;
  color: #64748b;
  margin-bottom: 28px;
}
.cta-btn {
  display: inline-block;
  padding: 14px 32px;
  background: #7F77DD;
  color: #fff;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.15s;
}
.cta-btn:hover { background: #6c63d4; }
.cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px 24px;
  text-decoration: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.card:hover {
  border-color: #7F77DD;
  box-shadow: 0 2px 12px rgba(127,119,221,0.1);
}
.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.card-body { flex: 1; }
.card-title {
  font-size: 15px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 4px;
}
.card-desc {
  font-size: 13px;
  color: #94a3b8;
}
.card-arrow {
  font-size: 16px;
  color: #cbd5e1;
  transition: color 0.15s;
}
.card:hover .card-arrow { color: #7F77DD; }
</style>

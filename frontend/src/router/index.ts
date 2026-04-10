import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('@/views/ResumeView.vue'),
    },
    {
      path: '/generate',
      name: 'generate',
      component: () => import('@/views/GenerateView.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryView.vue'),
    },
  ],
})

// 네비게이션 가드
router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.name !== 'login' && !authStore.isLoggedIn) {
    // 로그인 안 된 상태로 / 접근하면 /login으로
    return { name: 'login' }
  }
})

export default router

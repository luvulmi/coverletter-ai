<template>
  <AppLayout>
    <div class="page-header">
      <h2>히스토리</h2>
      <span class="count">총 {{ list.length }}개</span>
    </div>

    <div v-if="loading" class="empty">불러오는 중...</div>

    <div v-else-if="list.length === 0" class="empty">
      아직 생성된 커버레터가 없어요
    </div>

    <div v-else class="list">
      <div
        v-for="item in list"
        :key="item.id"
        class="card"
      >
        <div class="card-header" @click="toggle(item.id)">
          <div class="card-info">
            <div class="card-title">{{ item.company_name }} · {{ item.position }}</div>
            <div class="card-date">{{ formatDate(item.created_at) }}</div>
          </div>
          <div class="card-actions">
            <button
              class="delete-btn"
              @click.stop="remove(item.id)"
            >삭제</button>
            <span class="chevron" :class="{ open: openId === item.id }">▾</span>
          </div>
        </div>

        <div v-if="openId === item.id" class="card-body">
          <div class="card-content">{{ item.content }}</div>
          <button class="copy-btn" @click="copy(item.content)">
            {{ copied === item.id ? '복사됨 ✓' : '클립보드 복사' }}
          </button>
        </div>

      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import AppLayout from '@/components/AppLayout.vue'

interface CoverLetter {
  id: number
  company_name: string
  position: string
  content: string
  created_at: string
}

const list = ref<CoverLetter[]>([])
const loading = ref(true)
const openId = ref<number | null>(null)
const copied = ref<number | null>(null)

onMounted(async () => {
  try {
    const res = await api.get('/cover-letters/')
    list.value = res.data
  } finally {
    loading.value = false
  }
})

const toggle = (id: number) => {
  openId.value = openId.value === id ? null : id
}

const remove = async (id: number) => {
  if (!confirm('정말 삭제할까요?')) return
  await api.delete(`/cover-letters/${id}`)
  list.value = list.value.filter((item) => item.id !== id)
  if (openId.value === id) openId.value = null
}

const copy = async (content: string) => {
  await navigator.clipboard.writeText(content)
  copied.value = list.value.find((i) => i.content === content)?.id ?? null
  setTimeout(() => (copied.value = null), 2000)
}

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr)
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
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
  gap: 24px;
}
.nav-links a {
  font-size: 14px;
  color: #64748b;
  text-decoration: none;
  transition: color 0.15s;
}
.nav-links a:hover { color: #1e293b; }
.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}
.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}
h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
}
.count {
  font-size: 13px;
  color: #94a3b8;
}
.empty {
  text-align: center;
  padding: 80px 0;
  color: #94a3b8;
  font-size: 14px;
}
.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden;
  transition: border-color 0.15s;
}
.card:hover { border-color: #c4c1ee; }
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  cursor: pointer;
  user-select: none;
}
.card-title {
  font-size: 15px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 4px;
}
.card-date {
  font-size: 12px;
  color: #94a3b8;
}
.card-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.delete-btn {
  font-size: 12px;
  color: #94a3b8;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.15s;
}
.delete-btn:hover {
  color: #ef4444;
  background: #fef2f2;
}
.chevron {
  font-size: 16px;
  color: #94a3b8;
  transition: transform 0.2s;
  display: inline-block;
}
.chevron.open { transform: rotate(180deg); }
.card-body {
  padding: 0 24px 20px;
  border-top: 1px solid #f1f5f9;
}
.card-content {
  font-size: 14px;
  line-height: 1.8;
  color: #334155;
  white-space: pre-wrap;
  padding: 16px 0;
}
.copy-btn {
  font-size: 13px;
  color: #7F77DD;
  background: #EEEDFE;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background 0.15s;
}
.copy-btn:hover { background: #dddaf9; }
</style>

<template>
  <AppLayout>
    <div class="resume-card">
      <div class="header">
        <div>
          <h2>자기소개서</h2>
          <p class="sub">저장해두면 커버레터 생성 시 자동으로 사용돼요</p>
        </div>
        <button class="save-btn" @click="save" :disabled="loading">
          {{ loading ? '저장 중...' : '저장' }}
        </button>
      </div>

      <div v-if="fetchLoading" class="loading-state">불러오는 중...</div>

      <textarea
        v-else
        v-model="content"
        placeholder="자기소개서 내용을 붙여넣어 주세요"
        class="textarea"
      />

      <div v-if="successMsg" class="success">{{ successMsg }}</div>
      <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '@/components/AppLayout.vue'
import api from '@/api'

const content = ref('')
const loading = ref(false)
const fetchLoading = ref(true)
const successMsg = ref('')
const errorMsg = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/resume/')
    content.value = res.data.content
  } catch {
  } finally {
    fetchLoading.value = false
  }
})

const save = async () => {
  if (!content.value.trim()) {
    errorMsg.value = '자기소개서 내용을 입력해주세요'
    return
  }
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await api.put('/resume/', { content: content.value })
    successMsg.value = '저장됐어요!'
    setTimeout(() => (successMsg.value = ''), 3000)
  } catch {
    errorMsg.value = '저장 중 오류가 발생했어요'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.resume-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 32px;
  max-width: 800px;
  margin: 0 auto;
}
.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}
h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}
.sub { font-size: 13px; color: #94a3b8; }
.save-btn {
  padding: 10px 24px;
  background: #7F77DD;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
  white-space: nowrap;
}
.save-btn:hover { background: #6c63d4; }
.save-btn:disabled { background: #c4c1ee; cursor: not-allowed; }
.textarea {
  width: 100%;
  height: 480px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.7;
  resize: vertical;
  outline: none;
  color: #334155;
  transition: border-color 0.15s;
  font-family: inherit;
}
.textarea:focus { border-color: #7F77DD; }
.loading-state {
  height: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 14px;
}
.success { margin-top: 12px; font-size: 13px; color: #059669; }
.error { margin-top: 12px; font-size: 13px; color: #ef4444; }
</style>

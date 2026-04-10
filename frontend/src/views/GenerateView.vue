<template>
  <AppLayout>
    <div class="left">

      <div class="section-title">지원 정보</div>

      <div class="field">
        <label>회사명</label>
        <input v-model="companyName" type="text" placeholder="카카오" />
      </div>

      <div class="field">
        <label>포지션</label>
        <input v-model="position" type="text" placeholder="백엔드 개발자" />
      </div>

      <div class="field">
        <label>채용공고 (JD)</label>
        <textarea
          v-model="jdText"
          placeholder="채용공고 내용을 붙여넣어 주세요"
          class="jd-textarea"
        />
      </div>

      <div class="field">
        <label>
          자기소개서
          <span class="label-sub">(비워두면 저장된 이력서 사용)</span>
        </label>
        <textarea
          v-model="resumeText"
          placeholder="직접 입력하거나 비워두세요"
          class="resume-textarea"
        />
      </div>

      <button
        class="generate-btn"
        @click="generate"
        :disabled="generating || !companyName || !position || !jdText"
      >
        {{ generating ? 'AI 생성 중...' : '커버레터 생성하기' }}
      </button>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

    </div>

    <div class="right">

      <div class="result-header">
        <div class="section-title">생성 결과</div>
        <button
          v-if="result && !generating"
          class="save-btn"
          @click="save"
          :disabled="saving"
        >
          {{ saving ? '저장 중...' : saved ? '저장됨 ✓' : '저장하기' }}
        </button>
      </div>

      <div class="result-box">
        <div v-if="!result && !generating" class="result-empty">
          생성 버튼을 눌러주세요
        </div>
        <div v-else class="result-text">
          {{ result }}
          <span v-if="generating" class="cursor">|</span>
        </div>
      </div>

    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import AppLayout from '@/components/AppLayout.vue'

const companyName = ref('')
const position = ref('')
const jdText = ref('')
const resumeText = ref('')

const result = ref('')
const generating = ref(false)
const saving = ref(false)
const saved = ref(false)
const errorMsg = ref('')

const generate = async () => {
  result.value = ''
  saved.value = false
  errorMsg.value = ''
  generating.value = true

  try {
    const token = localStorage.getItem('access_token')

    // fetch로 SSE 수신 — axios는 스트리밍 미지원
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/cover-letters/generate`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          company_name: companyName.value,
          position: position.value,
          jd_text: jdText.value,
          resume_text: resumeText.value || null,
        }),
      }
    )

    if (!response.ok) {
      throw new Error('생성 요청에 실패했어요')
    }

    const decoder = new TextDecoder()

    // for await으로 청크 순서대로 읽기
    for await (const chunk of response.body as any) {
      const lines = decoder.decode(chunk).split('\n')
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        const data = line.slice(6)
        if (data === '[DONE]') {
          generating.value = false
          return
        }
        if (data.startsWith('[ERROR]')) {
          throw new Error(data)
        }
        result.value += data.replace(/\\n/g, '\n')
      }
    }
  } catch (e: any) {
    errorMsg.value = e.message || '오류가 발생했어요'
    generating.value = false
  }
}

const save = async () => {
  saving.value = true
  try {
    await api.post('/cover-letters/', {
      company_name: companyName.value,
      position: position.value,
      jd_text: jdText.value,
      content: result.value,
    })
    saved.value = true
  } catch {
    errorMsg.value = '저장 중 오류가 발생했어요'
  } finally {
    saving.value = false
  }
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}
.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
}
.left, .right {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 28px;
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
.label-sub {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 400;
  margin-left: 4px;
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
.field input:focus { border-color: #7F77DD; }
.jd-textarea {
  width: 100%;
  height: 180px;
  padding: 12px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s;
}
.jd-textarea:focus { border-color: #7F77DD; }
.resume-textarea {
  width: 100%;
  height: 120px;
  padding: 12px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s;
}
.resume-textarea:focus { border-color: #7F77DD; }
.generate-btn {
  width: 100%;
  padding: 13px;
  background: #7F77DD;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 4px;
  transition: background 0.15s;
}
.generate-btn:hover:not(:disabled) { background: #6c63d4; }
.generate-btn:disabled {
  background: #c4c1ee;
  cursor: not-allowed;
}
.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.save-btn {
  padding: 8px 20px;
  background: #fff;
  color: #7F77DD;
  border: 1px solid #7F77DD;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.save-btn:hover:not(:disabled) {
  background: #7F77DD;
  color: #fff;
}
.save-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.result-box {
  height: calc(100% - 52px);
  min-height: 500px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 20px;
  overflow-y: auto;
}
.result-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 14px;
}
.result-text {
  font-size: 14px;
  line-height: 1.8;
  color: #334155;
  white-space: pre-wrap;
}
.cursor {
  display: inline-block;
  animation: blink 0.8s infinite;
  color: #7F77DD;
  font-weight: 300;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.error {
  margin-top: 12px;
  font-size: 13px;
  color: #ef4444;
}
</style>

<script setup lang="ts">
import type { AnalysisStatus } from '../types'

const props = defineProps<{
  modelStatusText: string
  modelProgress: number
  modelReady: boolean
  analysisStatus: AnalysisStatus
}>()

const emit = defineEmits<{
  analyze: []
  cancel: []
}>()
</script>

<template>
  <div class="scene-input">
    <label class="label">
      场景描述
      <div class="label-actions">
        <span v-if="!modelReady && modelStatusText" class="hint">请先加载模型</span>
        <button
          v-if="analysisStatus !== 'analyzing'"
          class="btn btn-primary"
          :disabled="!modelReady"
          @click="emit('analyze')"
        >开始分析</button>
        <button
          v-else
          class="btn btn-danger"
          @click="emit('cancel')"
        ><span class="spinner" />停止分析</button>
      </div>
    </label>
    <textarea
      class="textarea"
      :placeholder="`描述你的系统场景，例如：\n「我需要在校园内实现一个共享单车系统，学生可以通过手机扫码解锁单车，骑行结束后上锁结算。管理员可以在后台管理单车和查看使用统计。」`"
      rows="5"
    />
  </div>
</template>

<style scoped>
.scene-input {
  margin-bottom: 16px;
}

.label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 8px;
}
.label-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
  align-items: center;
}

.textarea {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  font-family: inherit;
  box-sizing: border-box;
}

.textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-alpha);
}

.hint {
  font-size: 13px;
  color: var(--text-secondary);
}
.label-actions :deep(.btn) {
  font-size: 16px;
  padding: 6px 16px;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin .6s linear infinite;
  margin-right: 4px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

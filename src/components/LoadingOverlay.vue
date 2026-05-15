<script setup lang="ts">
import type { ProgressInfo } from '../types'

defineProps<{
  visible: boolean
  status: string
  progress: ProgressInfo
}>()
</script>

<template>
  <Teleport to="body">
    <div v-if="visible" class="overlay">
      <div class="overlay-card">
        <div class="spinner-large" />
        <h3 class="overlay-title">
          {{ status === 'downloading' ? '下载模型中...' : '加载模型中...' }}
        </h3>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${progress.progress * 100}%` }" />
        </div>
        <p class="overlay-text">{{ progress.text }}</p>
        <p class="overlay-hint">
          模型体积较大，首次加载需要下载约 1-2.5GB。
          下载后会自动缓存，后续使用无需重复下载。
        </p>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, .5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.overlay-card {
  background: var(--surface);
  border-radius: 12px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, .3);
}

.spinner-large {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin .8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.overlay-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 16px;
}

.progress-bar {
  height: 6px;
  background: var(--bg);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 3px;
  transition: width .3s ease;
}

.overlay-text {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 8px;
}

.overlay-hint {
  font-size: 12px;
  color: var(--text-secondary);
  opacity: .7;
  margin: 0;
}
</style>

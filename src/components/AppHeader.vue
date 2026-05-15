<script setup lang="ts">
defineProps<{
  showHistory: boolean
  modelStatusText: string
}>()

const emit = defineEmits<{
  toggleHistory: []
}>()
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <h1 class="app-title">场景需求分析器</h1>
      <span class="subtitle">自然语言 → 系统需求 + 流程图</span>
    </div>
    <div class="header-right">
      <span class="model-status">{{ modelStatusText }}</span>
      <button
        class="btn btn-ghost"
        :class="{ active: showHistory }"
        @click="emit('toggleHistory')"
        title="历史记录"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        历史
      </button>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.app-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

.subtitle {
  font-size: 13px;
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.model-status {
  font-size: 12px;
  color: var(--text-secondary);
}

.btn-ghost {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all .15s;
}

.btn-ghost:hover {
  background: var(--bg);
  color: var(--text);
}

.btn-ghost.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
</style>

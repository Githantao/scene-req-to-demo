<script setup lang="ts">
import type { HistoryEntry } from '../types'

defineProps<{
  visible: boolean
  entries: HistoryEntry[]
}>()

const emit = defineEmits<{
  restore: [entry: HistoryEntry]
  delete: [id: string]
  clear: []
  close: []
}>()

function formatDate(ts: number) {
  const d = new Date(ts)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>

<template>
  <Teleport to="body">
    <Transition name="panel">
      <div v-if="visible" class="history-overlay">
        <div class="history-panel">
          <div class="panel-header">
            <h2>历史记录</h2>
            <div class="panel-actions">
              <button
                v-if="entries.length"
                class="btn btn-sm btn-outline"
                @click="emit('clear')"
              >
                清空
              </button>
              <button class="btn btn-sm btn-ghost" @click="emit('close')">
                ✕
              </button>
            </div>
          </div>

          <div class="panel-body">
            <div
              v-for="entry in entries"
              :key="entry.id"
              class="history-item"
              @click="emit('restore', entry)"
            >
              <div class="item-header">
                <span class="item-title">{{ entry.result.requirements.title || '未命名' }}</span>
                <span class="item-model">{{ entry.modelUsed.split('-').slice(0, 2).join('-') }}</span>
              </div>
              <p class="item-scene">{{ entry.sceneText.slice(0, 80) }}{{ entry.sceneText.length > 80 ? '...' : '' }}</p>
              <span class="item-time">{{ formatDate(entry.timestamp) }}</span>
              <button
                class="item-delete"
                @click.stop="emit('delete', entry.id)"
                title="删除"
              >
                🗑
              </button>
            </div>

            <p v-if="entries.length === 0" class="empty-state">暂无历史记录</p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.history-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, .3);
  z-index: 900;
  display: flex;
  justify-content: flex-end;
}

.history-panel {
  width: 360px;
  max-width: 90vw;
  background: var(--surface);
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 20px rgba(0, 0, 0, .1);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.panel-header h2 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text);
}

.panel-actions {
  display: flex;
  gap: 8px;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.history-item {
  position: relative;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all .15s;
}

.history-item:hover {
  border-color: var(--primary);
  background: var(--bg);
}

.item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.item-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}

.item-model {
  font-size: 11px;
  color: var(--primary);
  background: var(--primary-alpha);
  padding: 1px 6px;
  border-radius: 3px;
}

.item-scene {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 4px 0;
  line-height: 1.4;
}

.item-time {
  font-size: 11px;
  color: var(--text-secondary);
  opacity: .7;
}

.item-delete {
  position: absolute;
  top: 8px;
  right: 8px;
  background: none;
  border: none;
  font-size: 14px;
  cursor: pointer;
  opacity: 0;
  transition: opacity .15s;
  padding: 4px;
}

.history-item:hover .item-delete {
  opacity: .5;
}

.history-item:hover .item-delete:hover {
  opacity: 1;
}

.empty-state {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 40px;
}

.panel-enter-active,
.panel-leave-active {
  transition: transform .2s ease;
}

.panel-enter-from,
.panel-leave-to {
  transform: translateX(100%);
}
</style>

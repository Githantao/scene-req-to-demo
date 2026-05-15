<script setup lang="ts">
import { onMounted } from 'vue'
import { MODEL_OPTIONS } from '../composables/useWebLLM'
import { useModelCache } from '../composables/useModelCache'
import type { ModelId, LoadingStatus } from '../types'

const props = defineProps<{
  modelId: ModelId
  loadingStatus: LoadingStatus
}>()

const emit = defineEmits<{
  selectModel: [id: ModelId]
  loadModel: []
  unloadModel: []
}>()

const cache = useModelCache()

onMounted(() => { cache.refresh() })

async function handleClear() {
  const ok = await cache.clearCache()
  if (ok) cache.refresh()
}
</script>

<template>
  <div class="model-selector">
    <label class="label">模型选择</label>
    <div class="selector-row">
      <select
        class="select"
        :value="modelId"
        :disabled="loadingStatus === 'downloading' || loadingStatus === 'loading'"
        @change="emit('selectModel', ($event.target as HTMLSelectElement).value)"
      >
        <option
          v-for="m in MODEL_OPTIONS"
          :key="m.id"
          :value="m.id"
        >
          {{ m.label }} ({{ m.size }})
        </option>
      </select>

      <button
        v-if="loadingStatus === 'ready'"
        class="btn btn-sm btn-outline"
        @click="emit('unloadModel')"
      >
        卸载
      </button>
      <button
        v-else
        class="btn btn-sm btn-primary"
        :disabled="loadingStatus === 'downloading' || loadingStatus === 'loading'"
        @click="emit('loadModel')"
      >
        {{ loadingStatus === 'downloading' || loadingStatus === 'loading' ? '加载中...' : '加载模型' }}
      </button>
    </div>
    <p class="model-desc">{{ MODEL_OPTIONS.find(m => m.id === modelId)?.description }}</p>

    <div class="cache-info">
      <span class="cache-size">
        {{ cache.cacheEntries.value > 0 ? `缓存: ${cache.cacheSize.value}` : '无缓存' }}
        <button
          class="cache-refresh"
          title="刷新"
          @click="cache.refresh()"
        >↻</button>
      </span>
      <button
        v-if="cache.cacheEntries.value > 0"
        class="btn btn-xs btn-danger"
        :disabled="cache.isClearing.value"
        @click="handleClear"
      >
        {{ cache.isClearing.value ? '清除中...' : '清除缓存' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.model-selector {
  margin-bottom: 16px;
}

.label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: .5px;
}

.selector-row {
  display: flex;
  gap: 8px;
}

.select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
}

.select:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.model-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 4px 0 0;
}

.cache-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}

.cache-size {
  font-size: 11px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.cache-refresh {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 14px;
  padding: 0 2px;
  line-height: 1;
}

.cache-refresh:hover {
  color: var(--text);
}

.btn-xs {
  padding: 2px 8px;
  font-size: 11px;
}

.btn-danger {
  background: #fce8e6;
  color: #c5221f;
  border: 1px solid #f5c6cb;
}

.btn-danger:hover:not(:disabled) {
  background: #f5c6cb;
}

.btn-danger:disabled {
  opacity: .5;
  cursor: not-allowed;
}
</style>

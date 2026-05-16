<script setup lang="ts">
import { onMounted } from 'vue'
import { MODEL_OPTIONS } from '../composables/useWebLLM'
import { useModelCache } from '../composables/useModelCache'
import type { ModelId, LoadingStatus } from '../types'

const props = defineProps<{
  modelId: ModelId
  loadingStatus: LoadingStatus
  mirrorSource: 'auto' | 'china'
}>()

const emit = defineEmits<{
  selectModel: [id: ModelId]
  loadModel: []
  unloadModel: []
  'update:mirrorSource': [value: 'auto' | 'china']
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
        <option v-for="m in MODEL_OPTIONS" :key="m.id" :value="m.id">{{ m.label }} ({{ m.size }})</option>
      </select>
      <button v-if="loadingStatus === 'ready'" class="btn btn-sm btn-outline" @click="emit('unloadModel')">卸载</button>
      <button v-else class="btn btn-sm btn-primary" :disabled="loadingStatus === 'downloading' || loadingStatus === 'loading'" @click="emit('loadModel')">
        {{ loadingStatus === 'downloading' || loadingStatus === 'loading' ? '加载中...' : '加载模型' }}
      </button>
    </div>
    <p class="model-desc">{{ MODEL_OPTIONS.find(m => m.id === modelId)?.description }}</p>

    <div class="mirror-row">
      <span class="mirror-label">下载源</span>
      <label class="mirror-toggle"><input type="radio" :value="'auto'" :checked="mirrorSource==='auto'" :disabled="loadingStatus==='downloading'||loadingStatus==='loading'" @change="emit('update:mirrorSource', 'auto')"><span>自动</span></label>
      <label class="mirror-toggle"><input type="radio" :value="'china'" :checked="mirrorSource==='china'" :disabled="loadingStatus==='downloading'||loadingStatus==='loading'" @change="emit('update:mirrorSource', 'china')"><span>国内镜像</span></label>
    </div>

    <div class="cache-info">
      <span class="cache-size">
        {{ cache.cacheEntries.value > 0 ? `缓存: ${cache.cacheSize.value}` : '无缓存' }}
        <button class="cache-refresh" title="刷新" @click="cache.refresh()">↻</button>
      </span>
      <button v-if="cache.cacheEntries.value > 0" class="btn btn-xs btn-danger" :disabled="cache.isClearing.value" @click="handleClear">
        {{ cache.isClearing.value ? '清除中...' : '清除缓存' }}
      </button>
    </div>

    <details class="copy-help"><summary>如何从其他电脑复制已缓存的模型</summary><ol><li>在已下载模型的电脑上打开 Chrome，地址栏输入 <code>chrome://version/</code>，找到"个人资料路径"</li><li>关闭 Chrome，进入该路径的父目录，找到 <code>Default/IndexedDB</code> 和 <code>Default/File System</code> 目录</li><li>将这两个目录复制到新电脑的相同位置</li><li>重新打开本页面，缓存即可生效</li></ol><p style="margin:6px 0 0;font-size:11px"><strong>提示：</strong>每台电脑只需下载一次，后续离线可用。直接在新电脑上下载是最简单的方式。</p></details>
  </div>
</template>

<style scoped>
.model-selector { margin-bottom: 16px; }
.label { display: block; font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; text-transform: uppercase; letter-spacing: .5px; }
.selector-row { display: flex; gap: 8px; }
.select { flex: 1; padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); color: var(--text); font-size: 14px; cursor: pointer; }
.select:disabled { opacity: .6; cursor: not-allowed; }
.model-desc { font-size: 12px; color: var(--text-secondary); margin: 4px 0 0; }
.mirror-row { display: flex; align-items: center; gap: 10px; margin-top: 6px; font-size: 12px; }
.mirror-label { color: var(--text-secondary); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: .5px; }
.mirror-toggle { display: flex; align-items: center; gap: 3px; cursor: pointer; color: var(--text); }
.mirror-toggle input { cursor: pointer; }
.cache-info { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border); }
.cache-size { font-size: 11px; color: var(--text-secondary); display: flex; align-items: center; gap: 4px; }
.cache-refresh { background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 14px; padding: 0 2px; line-height: 1; }
.cache-refresh:hover { color: var(--text); }
.btn-xs { padding: 2px 8px; font-size: 11px; }
.btn-danger { background: #fce8e6; color: #c5221f; border: 1px solid #f5c6cb; }
.btn-danger:hover:not(:disabled) { background: #f5c6cb; }
.btn-danger:disabled { opacity: .5; cursor: not-allowed; }
.copy-help { font-size: 12px; color: var(--text-secondary); margin-top: 8px; padding-top: 6px; border-top: 1px solid var(--border); }
.copy-help summary { cursor: pointer; font-weight: 500; }
.copy-help ol { margin: 6px 0; padding-left: 18px; }
.copy-help li { margin-bottom: 4px; line-height: 1.5; }
.copy-help code { font-size: 11px; background: var(--bg); padding: 1px 4px; border-radius: 2px; }
</style>

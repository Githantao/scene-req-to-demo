<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { BackendType, ApiLLMConfig } from '../types'
import { API_PROVIDERS } from '../composables/useApiLLM'

const props = defineProps<{
  visible: boolean
  backend: BackendType
  apiConfig: ApiLLMConfig
}>()

const emit = defineEmits<{
  'update:visible': [v: boolean]
  'update:backend': [v: BackendType]
  'update:apiConfig': [v: ApiLLMConfig]
}>()

const localBackend = ref(props.backend)
const localConfig = ref<ApiLLMConfig>({ ...props.apiConfig })
const testing = ref(false)
const testStatus = ref<{type:'ok'|'err';msg:string}|null>(null)
const fetchedModels = ref<string[]>([])
const modelOptionsList = computed(() =>
  fetchedModels.value.length ? fetchedModels.value : (API_PROVIDERS[localConfig.value.provider]?.models || [])
)

watch(() => props.visible, (v) => {
  if (v) {
    localBackend.value = props.backend
    localConfig.value = { ...props.apiConfig }
  }
})

function onProviderChange(provider: string) {
  const p = API_PROVIDERS[provider]
  if (p && provider !== 'custom') {
    localConfig.value.endpoint = p.endpoint
    localConfig.value.model = p.defaultModel
  }
  localConfig.value.provider = provider
}

function onModelSelect(model: string) {
  if (model !== '__custom__') localConfig.value.model = model
}

async function testApiConnection() {
  testing.value = true
  testStatus.value = null
  fetchedModels.value = []
  try {
    const cfg = localConfig.value
    let models: string[] = []
    if (cfg.provider === 'ollama') {
      const url = cfg.endpoint.replace(/\/v1\/?$/, '') + '/api/tags'
      const resp = await fetch(url)
      if (!resp.ok) throw new Error('连接失败 (' + resp.status + ')')
      const data = await resp.json()
      models = (data.models || []).map((m: any) => m.name)
    } else {
      if (!cfg.apiKey) throw new Error('请先输入 API Key')
      const resp = await fetch(cfg.endpoint + '/models', { headers: { 'Authorization': 'Bearer ' + cfg.apiKey } })
      if (!resp.ok) throw new Error('连接失败 (' + resp.status + '): ' + (await resp.text()).slice(0, 100))
      const data = await resp.json()
      models = (data.data || []).map((m: any) => m.id).filter((id: string) => !id.includes('ft:'))
    }
    fetchedModels.value = models
    if (models.length) {
      testStatus.value = { type: 'ok', msg: '连接成功，发现 ' + models.length + ' 个模型' }
    } else {
      testStatus.value = { type: 'ok', msg: '连接成功，但未发现可用模型' }
    }
  } catch (e: any) {
    testStatus.value = { type: 'err', msg: e.message || '连接失败' }
  } finally {
    testing.value = false
  }
}

function save() {
  emit('update:backend', localBackend.value)
  emit('update:apiConfig', { ...localConfig.value })
  emit('update:visible', false)
}

function close() {
  emit('update:visible', false)
}
</script>

<template>
  <Teleport to="body">
    <div v-if="visible" class="as-overlay" @click.self="close">
      <div class="as-panel">
        <div class="as-header">
          <h2>推理引擎设置</h2>
          <button class="as-close" @click="close">✕</button>
        </div>

        <div class="as-body">
          <div class="as-section">
            <label class="as-label">推理后端</label>
            <div class="as-backend-row">
              <label class="as-radio" :class="{ active: localBackend === 'webllm' }">
                <input type="radio" v-model="localBackend" value="webllm" />
                <span>WebLLM（本地浏览器）</span>
              </label>
              <label class="as-radio" :class="{ active: localBackend === 'api' }">
                <input type="radio" v-model="localBackend" value="api" />
                <span>第三方 API</span>
              </label>
            </div>
          </div>

          <template v-if="localBackend === 'api'">
            <div class="as-section">
              <label class="as-label">API 提供商</label>
              <select class="as-select" :value="localConfig.provider" @change="onProviderChange(($event.target as HTMLSelectElement).value)">
                <option v-for="(p, key) in API_PROVIDERS" :key="key" :value="key">{{ p.name }}</option>
              </select>
            </div>

            <div class="as-section">
              <label class="as-label">API 地址</label>
              <input class="as-input" v-model="localConfig.endpoint" placeholder="https://api.openai.com/v1" />
            </div>

            <div class="as-section">
              <label class="as-label">API Key</label>
              <input class="as-input" v-model="localConfig.apiKey" type="password" placeholder="sk-..." />
              <p class="as-hint">存储在本地浏览器，不会上传到任何服务器</p>
            </div>

            <div class="as-section">
              <label class="as-label">模型名称</label>
              <div class="as-model-group">
                <select class="as-select" :value="localConfig.model" @change="onModelSelect(($event.target as HTMLSelectElement).value)">
                  <option value="" disabled>选择模型</option>
                  <option v-for="m in modelOptionsList" :key="m" :value="m">{{ m }}</option>
                  <option value="__custom__">自定义...</option>
                </select>
                <input class="as-input" v-model="localConfig.model" placeholder="选择或输入模型名称" />
              </div>
            </div>

            <div class="as-section">
              <label class="as-label">连接测试</label>
              <div class="as-test-row">
                <button class="btn btn-sm btn-outline" :disabled="testing" @click="testApiConnection">
                  {{ testing ? '测试中...' : '测试连接' }}
                </button>
                <span v-if="testStatus" :class="'as-test-'+testStatus.type">{{ testStatus.msg }}</span>
              </div>
            </div>

            <div class="as-section">
              <label class="as-label">Temperature: {{ localConfig.temperature }}</label>
              <input type="range" min="0" max="1" step="0.05" v-model.number="localConfig.temperature" class="as-range" />
              <div class="as-range-labels"><span>0（确定）</span><span>1（创造）</span></div>
            </div>

            <div class="as-section">
              <label class="as-label">最大 Token 数</label>
              <input class="as-input" v-model.number="localConfig.maxTokens" type="number" min="256" max="32768" step="256" />
            </div>

            <div class="as-cors-notice">
              <strong>⚠ CORS 说明</strong>
              <p>部分 API 提供商（如 Anthropic Claude）可能不支持浏览器端跨域请求。</p>
              <p>如果遇到 CORS 错误，请尝试：使用 OpenAI / DeepSeek（支持浏览器请求），或在本地运行 Ollama。</p>
            </div>
          </template>
        </div>

        <div class="as-footer">
          <button class="btn btn-outline" @click="close">取消</button>
          <button class="btn btn-primary" @click="save">保存</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.as-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.3);
  z-index: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}
.as-panel {
  width: 480px;
  max-width: 90vw;
  max-height: 85vh;
  background: var(--surface);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0,0,0,.2);
}
.as-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}
.as-header h2 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}
.as-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 4px;
}
.as-close:hover { color: var(--text); }
.as-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}
.as-section {
  margin-bottom: 14px;
}
.as-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: .5px;
}
.as-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
}
.as-input::placeholder { color: var(--text-secondary); opacity: .5; }
.as-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
}
.as-hint {
  font-size: 11px;
  color: var(--text-secondary);
  margin: 4px 0 0;
}
.as-range {
  width: 100%;
  margin: 4px 0;
  accent-color: var(--primary);
}
.as-range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-secondary);
}
.as-backend-row {
  display: flex;
  gap: 8px;
}
.as-radio {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all .15s;
  font-size: 13px;
}
.as-radio.active {
  border-color: var(--primary);
  background: var(--primary-alpha);
}
.as-radio input { display: none; }
.as-cors-notice {
  background: #fef7e0;
  border: 1px solid #f9d849;
  border-radius: 8px;
  padding: 12px;
  font-size: 12px;
  color: #5f3b00;
  line-height: 1.5;
}
.as-cors-notice strong { display: block; margin-bottom: 4px; }
.as-cors-notice p { margin: 4px 0; }
.as-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid var(--border);
}
.as-model-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.as-test-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.as-test-ok {
  font-size: 12px;
  color: #137333;
}
.as-test-err {
  font-size: 12px;
  color: #c5221f;
}
</style>

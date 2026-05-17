import { ref } from 'vue'
import type { ApiLLMConfig } from '../types'

const STORAGE_KEY = 'api-llm-config'

export const API_PROVIDERS: Record<string, { name: string; endpoint: string; defaultModel: string; models: string[] }> = {
  openai: { name: 'OpenAI', endpoint: 'https://api.openai.com/v1', defaultModel: 'gpt-4o', models: ['gpt-4o','gpt-4o-mini','gpt-4-turbo','gpt-3.5-turbo'] },
  deepseek: { name: 'DeepSeek', endpoint: 'https://api.deepseek.com/v1', defaultModel: 'deepseek-chat', models: ['deepseek-chat','deepseek-reasoner','deepseek-coder'] },
  ollama: { name: 'Ollama (本地)', endpoint: 'http://localhost:11434/v1', defaultModel: 'qwen2.5:7b', models: ['qwen2.5:7b','qwen2.5:14b','qwen2.5:32b','llama3.2:3b','llama3.1:8b','mistral:7b','gemma2:9b'] },
  custom: { name: '自定义', endpoint: '', defaultModel: '', models: [] },
}

function defaultConfig(): ApiLLMConfig {
  return {
    provider: 'openai',
    endpoint: API_PROVIDERS.openai.endpoint,
    apiKey: '',
    model: API_PROVIDERS.openai.defaultModel,
    temperature: 0.3,
    maxTokens: 4096,
  }
}

function loadConfig(): ApiLLMConfig {
  try {
    const d = localStorage.getItem(STORAGE_KEY)
    if (d) return { ...defaultConfig(), ...JSON.parse(d) }
  } catch {}
  return defaultConfig()
}

function saveConfig(c: ApiLLMConfig) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(c))
}

function buildHeaders(config: ApiLLMConfig): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  if (config.provider === 'claude') {
    headers['x-api-key'] = config.apiKey
    headers['anthropic-version'] = '2023-06-01'
  } else {
    headers['Authorization'] = `Bearer ${config.apiKey}`
  }
  return headers
}

export function useApiLLM() {
  const config = ref<ApiLLMConfig>(loadConfig())
  const error = ref<string>('')

  function updateConfig(partial: Partial<ApiLLMConfig>) {
    config.value = { ...config.value, ...partial }
    saveConfig(config.value)
  }

  function resetConfig() {
    config.value = defaultConfig()
    saveConfig(config.value)
  }

  async function chat(systemPrompt: string, userPrompt: string, externalSignal?: AbortSignal): Promise<string> {
    error.value = ''
    const cfg = config.value
    if (!cfg.apiKey && cfg.provider !== 'ollama') {
      throw new Error('请先在 API 设置中配置 API Key')
    }

    const API_TIMEOUT = 600000

    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), API_TIMEOUT)
    if (externalSignal) {
      externalSignal.addEventListener('abort', () => { clearTimeout(timer); controller.abort(); }, { once: true })
    }
    try {
      const response = await fetch(`${cfg.endpoint}/chat/completions`, {
        method: 'POST',
        headers: buildHeaders(cfg),
        signal: controller.signal,
        body: JSON.stringify({
          model: cfg.model,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt },
          ],
          temperature: cfg.temperature,
          max_tokens: cfg.maxTokens,
          seed: 42,
        }),
      })

      if (!response.ok) {
        const body = await response.text()
        throw new Error(`API 请求失败 (${response.status}): ${body}`)
      }

      const data = await response.json()
      return data.choices?.[0]?.message?.content || ''
    } catch (e: any) {
      if (e.name === 'AbortError') throw new Error('API 请求已取消')
      error.value = e.message || 'API 请求失败'
      throw e
    } finally { clearTimeout(timer) }
  }

  async function chatRaw(messages: { role: string; content: string }[], externalSignal?: AbortSignal): Promise<string> {
    error.value = ''
    const cfg = config.value
    if (!cfg.apiKey && cfg.provider !== 'ollama') {
      throw new Error('请先在 API 设置中配置 API Key')
    }

    const API_TIMEOUT = 600000

    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), API_TIMEOUT)
    if (externalSignal) {
      externalSignal.addEventListener('abort', () => { clearTimeout(timer); controller.abort(); }, { once: true })
    }
    try {
      const response = await fetch(`${cfg.endpoint}/chat/completions`, {
        method: 'POST',
        headers: buildHeaders(cfg),
        signal: controller.signal,
        body: JSON.stringify({
          model: cfg.model,
          messages,
          temperature: cfg.temperature,
          max_tokens: cfg.maxTokens,
          seed: 42,
        }),
      })

      if (!response.ok) {
        const body = await response.text()
        throw new Error(`API 请求失败 (${response.status}): ${body}`)
      }

      const data = await response.json()
      return data.choices?.[0]?.message?.content || ''
    } catch (e: any) {
      if (e.name === 'AbortError') throw new Error('API 请求已取消')
      error.value = e.message || 'API 请求失败'
      throw e
    } finally { clearTimeout(timer) }
  }

  return {
    config,
    error,
    updateConfig,
    resetConfig,
    chat,
    chatRaw,
  }
}

import { ref } from 'vue'
import type { ModelId, ModelOption, LoadingStatus, ProgressInfo } from '../types'

export const MODEL_OPTIONS: ModelOption[] = [
  {
    id: 'Qwen2.5-1.5B-Instruct-q4f16_1-MLC',
    label: 'Qwen2.5-1.5B',
    description: '中文能力强，速度较快，推荐',
    size: '~1GB',
  },
  {
    id: 'gemma-2-2b-it-q4f16_1-MLC',
    label: 'Gemma-2-2B',
    description: '结构化输出稳定，英文能力强',
    size: '~1.5GB',
  },
  {
    id: 'Phi-3-mini-4k-instruct-q4f16_1-MLC',
    label: 'Phi-3-mini-3.8B',
    description: '能力最强，但加载慢，体积大',
    size: '~2.5GB',
  },
]

export function useWebLLM() {
  const status = ref<LoadingStatus>('idle')
  const progress = ref<ProgressInfo>({ text: '', progress: 0, timeElapsed: 0 })
  const error = ref<string>('')
  const currentModel = ref<ModelId>(MODEL_OPTIONS[0].id)
  const mirrorSource = ref<'auto' | 'china'>('auto')

  let engine: any = null

  async function loadModel(modelId: ModelId) {
    status.value = 'downloading'
    error.value = ''
    progress.value = { text: '初始化中...', progress: 0, timeElapsed: 0 }
    currentModel.value = modelId

    try {
      const { CreateMLCEngine, prebuiltAppConfig } = await import('@mlc-ai/web-llm')

      const engineConfig: any = {}
      if (mirrorSource.value === 'china') {
        const mirroredList = prebuiltAppConfig.model_list.map((r: any) => ({
          ...r,
          model: r.model.replace('https://huggingface.co/', 'https://hf-mirror.com/'),
        }))
        engineConfig.appConfig = { ...prebuiltAppConfig, model_list: mirroredList }
      }

      engine = await CreateMLCEngine(modelId, {
        initProgressCallback: (p: any) => {
          if (p.text && p.text.includes('Loading')) {
            status.value = 'loading'
          }
          progress.value = {
            text: p.text || '加载中...',
            progress: p.progress || 0,
            timeElapsed: p.timeElapsed || 0,
          }
        },
        ...engineConfig,
      })

      status.value = 'ready'
    } catch (e: any) {
      status.value = 'error'
      error.value = e.message || '模型加载失败'
      throw e
    }
  }

  async function unloadModel() {
    engine = null
    status.value = 'idle'
    progress.value = { text: '', progress: 0, timeElapsed: 0 }
  }

  async function chat(systemPrompt: string, userPrompt: string, _signal?: AbortSignal): Promise<string> {
    if (!engine) throw new Error('模型未加载')

    const reply = await engine.chat.completions.create({
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt },
      ],
      temperature: 0.2,
      max_tokens: 4096,
      top_p: 0.9,
    })

    return reply.choices[0]?.message?.content || ''
  }

  async function chatRaw(messages: { role: string; content: string }[], _signal?: AbortSignal): Promise<string> {
    if (!engine) throw new Error('模型未加载')

    const reply = await engine.chat.completions.create({
      messages,
      temperature: 0.2,
      max_tokens: 4096,
      top_p: 0.9,
    })

    return reply.choices[0]?.message?.content || ''
  }

  function resetChat() {
    if (engine) {
      engine.resetChat()
    }
  }

  return {
    status,
    progress,
    error,
    currentModel,
    mirrorSource,
    loadModel,
    unloadModel,
    chat,
    chatRaw,
    resetChat,
  }
}

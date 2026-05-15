import { ref } from 'vue'
import type { AnalysisResult, AnalysisStatus } from '../types'
import { SYSTEM_PROMPT, buildUserPrompt } from '../utils/prompt'
import { parseModelOutput, validateMermaid, generateFallbackMermaid } from '../utils/parser'

export function useAnalysis() {
  const result = ref<AnalysisResult | null>(null)
  const status = ref<AnalysisStatus>('idle')
  const error = ref<string>('')

  async function analyze(
    sceneText: string,
    chatFn: (system: string, user: string) => Promise<string>
  ): Promise<AnalysisResult | null> {
    if (!sceneText.trim()) {
      error.value = '请输入场景描述'
      return null
    }

    status.value = 'analyzing'
    error.value = ''
    result.value = null

    try {
      const raw = await chatFn(SYSTEM_PROMPT, buildUserPrompt(sceneText))
      const parsed = parseModelOutput(raw)

      if (!parsed) {
        status.value = 'error'
        error.value = '模型输出格式异常，请重试或换一个模型'
        return null
      }

      const mermaidCheck = validateMermaid(parsed.mermaidCode)
      if (!mermaidCheck.valid) {
        parsed.mermaidCode = generateFallbackMermaid(parsed.requirements.title)
      }

      result.value = parsed
      status.value = 'done'
      return parsed
    } catch (e: any) {
      status.value = 'error'
      error.value = e.message || '分析失败'
      return null
    }
  }

  function reset() {
    result.value = null
    status.value = 'idle'
    error.value = ''
  }

  return {
    result,
    status,
    error,
    analyze,
    reset,
  }
}

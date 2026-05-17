import { ref } from 'vue'
import type { AnalysisResult, AnalysisStatus } from '../types'
import { SYSTEM_PROMPT, buildUserPrompt } from '../utils/prompt'
import { parseModelOutput, validateMermaid, generateFallbackMermaid } from '../utils/parser'

function isComplexScene(text: string): boolean {
  return text.length > 50 || /同时|此外|并且|另外|以及|且|不但|而且|不仅|还有|除此之外|另一方面/.test(text)
}

export function useAnalysis() {
  const result = ref<AnalysisResult | null>(null)
  const status = ref<AnalysisStatus>('idle')
  const error = ref<string>('')
  const analysisTime = ref<string>('')
  let _startTime = 0
  let _timeInterval: ReturnType<typeof setInterval> | null = null
  let _verifyId = 0
  let _abortController: AbortController | null = null

  function cancel() {
    if (_abortController) {
      _abortController.abort()
      _abortController = null
    }
  }

  async function analyze(
    sceneText: string,
    chatFn: (system: string, user: string, signal?: AbortSignal) => Promise<string>,
    chatRawFn?: (messages: { role: string; content: string }[], signal?: AbortSignal) => Promise<string>,
  ): Promise<AnalysisResult | null> {
    if (!sceneText.trim()) {
      error.value = '请输入场景描述'
      return null
    }

    status.value = 'analyzing'
    analysisTime.value = ''
    error.value = ''
    result.value = null
    _abortController = new AbortController()
    _startTime = Date.now()
    _timeInterval = setInterval(() => {
      const e = Date.now() - _startTime
      analysisTime.value = e < 1000 ? (e + 'ms') : ((e / 1000).toFixed(1) + 's')
    }, 100)

    try {
      const raw = await chatFn(SYSTEM_PROMPT, buildUserPrompt(sceneText), _abortController.signal)
      if (_abortController.signal.aborted) { status.value = 'idle'; return null }

      let parsed = parseModelOutput(raw)

      if (!parsed) {
        status.value = 'error'
        error.value = '模型输出格式异常，请重试或换一个模型'
        return null
      }

      // Show first result immediately
      result.value = parsed
      status.value = 'done'
      if (_timeInterval) { clearInterval(_timeInterval); _timeInterval = null }

      const elapsed = Date.now() - _startTime
      analysisTime.value = elapsed < 1000 ? (elapsed + 'ms') : ((elapsed / 1000).toFixed(1) + 's')

      const mermaidCheck = validateMermaid(parsed.mermaidCode)
      if (!mermaidCheck.valid) {
        parsed.mermaidCode = generateFallbackMermaid(parsed.requirements.title)
      }

      // Background CoVe — improve quality without blocking UX
      if (isComplexScene(sceneText) && chatRawFn) {
        backgroundVerify(sceneText, parsed, chatRawFn)
      }

      return parsed
    } catch (e: any) {
      if (_timeInterval) { clearInterval(_timeInterval); _timeInterval = null }
      if (e.name === 'AbortError') {
        status.value = 'idle'
        analysisTime.value = ''
        error.value = ''
        return null
      }
      status.value = 'error'
      error.value = e.message || '分析失败'
      return null
    } finally { _abortController = null }
  }

  async function backgroundVerify(
    sceneText: string,
    initialResult: AnalysisResult,
    chatRawFn: (messages: { role: string; content: string }[]) => Promise<string>,
  ) {
    const vid = ++_verifyId
    try {
      const verifyPrompt = '原始场景：\n' + sceneText + '\n\n初步分析结果：\n' + JSON.stringify(initialResult, null, 2) + '\n\n请逐项检查：\n1) 是否有场景中未提到的幻觉需求\n2) 是否有遗漏的关键功能\n3) 是否有需求被过度拆分（粒度应为完整能力而非操作步骤）\n4) 是否逻辑一致\n\n有问题请修正后重新输出完整的 JSON 结果；无问题则输出与初步结果一致的 JSON。'
      const raw = await chatRawFn([
        { role: 'system', content: '你是一个严谨的需求质量检查专家。请检查并修正给定的需求分析结果。' },
        { role: 'user', content: verifyPrompt },
      ])
      // Stale guard: skip if a newer analysis has started
      if (vid !== _verifyId) return
      const verified = parseModelOutput(raw)
      if (!verified) return
      if (JSON.stringify(verified.requirements) === JSON.stringify(result.value?.requirements)) return

      // Update display with verified result
      result.value = verified
    } catch (e) {
      console.warn('CoVe 验证失败:', e)
    }
  }

  function reset() {
    if (_timeInterval) { clearInterval(_timeInterval); _timeInterval = null }
    result.value = null
    status.value = 'idle'
    error.value = ''
    analysisTime.value = ''
  }

  return {
    result,
    status,
    error,
    analysisTime,
    analyze,
    cancel,
    reset,
  }
}

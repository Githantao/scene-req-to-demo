import type { AnalysisResult } from '../types'

export function parseModelOutput(raw: string): AnalysisResult | null {
  const json = extractJSON(raw)
  if (!json) return null

  try {
    const parsed = JSON.parse(json)
    if (!parsed.requirements || !parsed.mermaidCode) return null

    const result: AnalysisResult = {
      requirements: {
        title: parsed.requirements.title || '未命名系统',
        layers: parsed.requirements.layers || null,
        systemBoundary: parsed.requirements.systemBoundary || '',
        stakeholders: Array.isArray(parsed.requirements.stakeholders)
          ? parsed.requirements.stakeholders
          : [],
        functionalRequirements: Array.isArray(parsed.requirements.functionalRequirements)
          ? parsed.requirements.functionalRequirements
          : [],
        dataFlows: Array.isArray(parsed.requirements.dataFlows)
          ? parsed.requirements.dataFlows
          : [],
        nonFunctionalRequirements: Array.isArray(parsed.requirements.nonFunctionalRequirements)
          ? parsed.requirements.nonFunctionalRequirements
          : [],
      },
      mermaidCode: parsed.mermaidCode || '',
      rawOutput: raw,
    }

    return result
  } catch {
    return null
  }
}

function extractJSON(text: string): string | null {
  const codeBlockMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/)
  if (codeBlockMatch) return codeBlockMatch[1].trim()

  const braceMatch = text.match(/{[\s\S]*}/)
  if (braceMatch) return braceMatch[0].trim()

  return null
}

export function validateMermaid(code: string): { valid: boolean; error?: string } {
  if (!code || code.trim().length === 0) {
    return { valid: false, error: 'Mermaid 代码为空' }
  }

  if (!code.startsWith('flowchart TD') && !code.startsWith('flowchart LR')) {
    return { valid: false, error: '只支持 flowchart TD/LR 格式' }
  }

  return { valid: true }
}

export function generateFallbackMermaid(title: string): string {
  return `flowchart TD
  A[${title}] --> B[待分析]`
}

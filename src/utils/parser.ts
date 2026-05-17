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
        diagramType: parsed.requirements.diagramType || 'flowchart',
        layers: parsed.requirements.layers || null,
        mainRequirement: parsed.requirements.mainRequirement || null,
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

  return { valid: true }
}

export function generateFallbackMermaid(title: string, type = 'flowchart'): string {
  if (type === 'erDiagram') return `erDiagram\n  实体 ||--o{ 子实体 : 包含`
  if (type === 'sequenceDiagram') return `sequenceDiagram\n  actor 用户\n  participant 系统\n  用户->>系统: 请求\n  系统-->>用户: 响应`
  if (type === 'stateDiagram-v2') return `stateDiagram-v2\n  [*] --> 初始\n  初始 --> [*]`
  if (type === 'classDiagram') return `classDiagram\n  class 系统 {\n    +操作()\n  }`
  return `flowchart TD\n  A[${title}] --> B[待分析]`
}

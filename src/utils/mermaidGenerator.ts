import type { Requirements } from '../types'

const DIAGRAM_LABELS: Record<string, string> = {
  flowchart: '流程图',
  sequenceDiagram: '时序图',
  classDiagram: '类图',
  'stateDiagram-v2': '状态图',
  erDiagram: 'ER图',
}

function esc(s: string): string {
  return s.replace(/[{}[\]()]/g, '').trim()
}

function sanitizeId(s: string): string {
  return s.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '_').replace(/_{2,}/g, '_').replace(/^_|_$/g, '') || 'node'
}

function generateFlowchart(r: Requirements): string {
  const frs = r.functionalRequirements
  if (!frs.length) return `flowchart TD\n  A[系统] --> B[待分析]`
  const lines: string[] = ['flowchart TD']
  frs.forEach((fr, i) => {
    const id = `FR${i + 1}`
    lines.push(`  ${id}["${esc(fr.name)}"]`)
  })
  r.dataFlows.forEach(df => {
    const fromId = `src_${sanitizeId(df.from)}`
    const toId = `dst_${sanitizeId(df.to)}`
    if (!lines.find(l => l.startsWith(`  ${fromId}[`))) lines.push(`  ${fromId}["${esc(df.from)}"]`)
    if (!lines.find(l => l.startsWith(`  ${toId}[`))) lines.push(`  ${toId}["${esc(df.to)}"]`)
    lines.push(`  ${fromId} -->|${esc(df.data)}| ${toId}`)
  })
  if (frs.length === 1) {
    lines.push(`  FR1 --> A[完成]`)
  } else {
    for (let i = 0; i < frs.length - 1; i++) {
      lines.push(`  FR${i + 1} --> FR${i + 2}`)
    }
  }
  return lines.join('\n')
}

function generateSequenceDiagram(r: Requirements): string {
  const lines: string[] = ['sequenceDiagram']
  const actors = r.stakeholders.length ? r.stakeholders : ['用户']
  actors.forEach(a => lines.push(`  actor ${esc(a)}`))
  lines.push(`  participant ${esc(r.title || '系统')}`)
  if (r.dataFlows.length) {
    r.dataFlows.forEach(df => {
      const arrow = df.type === 'output' ? '-->>' : '->>'
      lines.push(`  ${esc(df.from)}${arrow}${esc(df.to)}: ${esc(df.data)}`)
    })
  } else {
    const frs = r.functionalRequirements.slice(0, actors.length * 2)
    frs.forEach((fr, i) => {
      const a = actors[i % actors.length]
      lines.push(`  ${esc(a)}->>${esc(r.title || '系统')}: ${esc(fr.name)}`)
      lines.push(`  ${esc(r.title || '系统')}-->>${esc(a)}: ${esc(fr.description.slice(0, 30))}`)
    })
  }
  return lines.join('\n')
}

function generateClassDiagram(r: Requirements): string {
  const lines: string[] = ['classDiagram']
  const sysName = esc(r.title || '系统')
  lines.push(`  class ${sanitizeId(sysName)} {`)
  r.functionalRequirements.slice(0, 8).forEach(fr => {
    const p = fr.priority === 'high' ? '+' : fr.priority === 'medium' ? '#' : '-'
    lines.push(`    ${p}${esc(fr.name)}()`)
  })
  lines.push('  }')
  r.stakeholders.forEach(s => {
    const id = sanitizeId(esc(s))
    lines.push(`  class ${id} {`)
    lines.push(`    +${esc(s)}`)
    lines.push('  }')
    lines.push(`  ${id} --> ${sanitizeId(sysName)} : 使用`)
  })
  return lines.join('\n')
}

function generateStateDiagram(r: Requirements): string {
  const lines: string[] = ['stateDiagram-v2']
  lines.push('  [*] --> 待处理')
  lines.push('  待处理 --> 处理中')
  if (r.functionalRequirements.length > 2) {
    lines.push('  处理中 --> 审核中')
    lines.push('  审核中 --> 已完成')
    lines.push('  审核中 --> 已拒绝')
  } else {
    lines.push('  处理中 --> 已完成')
    lines.push('  处理中 --> 已拒绝')
  }
  lines.push('  已完成 --> [*]')
  lines.push('  已拒绝 --> [*]')
  r.functionalRequirements.slice(0, 3).forEach(fr => {
    const stateName = esc(fr.name).slice(0, 10)
    if (stateName) {
      lines.push(`  处理中 --> ${sanitizeId(stateName)} : ${esc(fr.name)}`)
      lines.push(`  ${sanitizeId(stateName)} --> 已完成`)
    }
  })
  return lines.join('\n')
}

function generateErDiagram(r: Requirements): string {
  const lines: string[] = ['erDiagram']
  const entities = new Set<string>()
  r.stakeholders.forEach(s => entities.add(esc(s)))
  if (r.title) entities.add(esc(r.title))
  entities.forEach(e => {
    const id = sanitizeId(e)
    lines.push(`  ${id} {`)
    r.functionalRequirements.slice(0, 4).forEach(fr => {
      lines.push(`    string ${sanitizeId(fr.name)}`)
    })
    lines.push('  }')
  })
  r.dataFlows.forEach(df => {
    const fromId = sanitizeId(esc(df.from))
    const toId = sanitizeId(esc(df.to))
    if (entities.has(esc(df.from)) && entities.has(esc(df.to))) {
      lines.push(`  ${fromId} ||--o{ ${toId} : ${esc(df.data)}`)
    }
  })
  if (!r.dataFlows.length && entities.size >= 2) {
    const ents = Array.from(entities)
    for (let i = 0; i < ents.length - 1; i++) {
      lines.push(`  ${sanitizeId(ents[i])} ||--o{ ${sanitizeId(ents[i + 1])} : 包含`)
    }
  }
  return lines.join('\n')
}

export function generateMermaidForType(r: Requirements, type: string): string {
  switch (type) {
    case 'flowchart': return generateFlowchart(r)
    case 'sequenceDiagram': return generateSequenceDiagram(r)
    case 'classDiagram': return generateClassDiagram(r)
    case 'stateDiagram-v2': return generateStateDiagram(r)
    case 'erDiagram': return generateErDiagram(r)
    default: return ''
  }
}

export function getDiagramOptions(): { value: string; label: string }[] {
  return Object.entries(DIAGRAM_LABELS).map(([value, label]) => ({ value, label }))
}

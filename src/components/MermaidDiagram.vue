<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import type { Requirements } from '../types'
import { generateMermaidForType, getDiagramOptions } from '../utils/mermaidGenerator'

const props = defineProps<{
  code: string
  requirements?: Requirements | null
  diagramType?: string
}>()

const emit = defineEmits<{
  'update:code': [value: string]
  'update:diagramType': [value: string]
}>()

const diagramOptions = getDiagramOptions()
const selectedType = ref(props.diagramType || 'flowchart')
const svgRef = ref<string>('')
const renderError = ref<string>('')
const editableCode = ref('')
const showEditor = ref(true)
const editorDirty = ref(false)
let editorTimer: ReturnType<typeof setTimeout> | null = null
let mermaid: any = null

const displayCode = computed(() => {
  if (!props.requirements) return props.code
  const originalType = props.requirements.diagramType || 'flowchart'
  if (selectedType.value === originalType) {
    return props.code
  }
  return generateMermaidForType(props.requirements, selectedType.value)
})

function onTypeChange(type: string) {
  selectedType.value = type
  emit('update:diagramType', type)
  editableCode.value = displayCode.value
  editorDirty.value = false
  renderCode(displayCode.value)
}

watch(() => props.code, (val) => {
  if (val && !props.requirements) {
    if (!editableCode.value) editableCode.value = val
    renderCode(val)
  }
})

watch(editableCode, (val) => {
  if (!val || val === displayCode.value) { editorDirty.value = false; return }
  editorDirty.value = true
  if (editorTimer) clearTimeout(editorTimer)
  editorTimer = setTimeout(async () => {
    emit('update:code', val)
    await renderCode(val)
    editorDirty.value = false
  }, 600)
})

onMounted(() => {
  const startCode = displayCode.value || props.code
  if (startCode) {
    editableCode.value = startCode
    renderCode(startCode)
  }
})

async function renderCode(code: string) {
  if (!code) return
  try {
    if (!mermaid) {
      mermaid = await import('mermaid')
      mermaid.default.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        fontFamily: 'inherit',
      })
    }
    renderError.value = ''
    const cleaned = code.replace(/\\n/g, '\n').trim()
    const { svg } = await mermaid.default.render('mermaid-' + Date.now(), cleaned)
    svgRef.value = svg
  } catch (e: any) {
    renderError.value = e.message || '渲染失败'
    svgRef.value = ''
  }
}

async function copyCode() {
  try {
    await navigator.clipboard.writeText(editableCode.value)
  } catch {
    const ta = document.createElement('textarea')
    ta.value = editableCode.value
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
  }
}

function openDiagramInNewTab() {
  const code = editableCode.value || props.code
  if (!code) return
  const cdnBase = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js'
  const html = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>需求分析图</title><script src="'+cdnBase+'"><\/script><style>body{margin:0;min-height:100vh;display:flex;justify-content:center;padding:40px 20px;box-sizing:border-box;background:#fff;font-family:system-ui,-apple-system,sans-serif}.mermaid{max-width:1200px;width:100%}.mermaid svg{max-width:100%;height:auto!important}@media(prefers-color-scheme:dark){body{background:#1e1e1e}}</style></head><body><div class="mermaid">'+code.replace(/<\/script>/gi,'<\\/script>')+'</div><script>mermaid.initialize({startOnLoad:true,theme:"default",securityLevel:"loos"})<\/script></body></html>'
  const win = window.open('', '_blank')
  if (win) { win.document.write(html); win.document.close() }
}

async function svgToBlob(): Promise<Blob | null> {
  const svgEl = document.querySelector('.svg-container svg')
  if (!svgEl) return null
  const svgClone = svgEl.cloneNode(true) as SVGElement
  svgClone.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  const svgStr = new XMLSerializer().serializeToString(svgClone)
  const svgBlob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' })
  const url = URL.createObjectURL(svgBlob)
  const img = new Image()
  await new Promise<void>((res, rej) => { img.onload = () => res(); img.onerror = rej; img.src = url })
  URL.revokeObjectURL(url)
  const rect = svgEl.getBoundingClientRect()
  const cvs = document.createElement('canvas')
  const dpr = window.devicePixelRatio || 1
  cvs.width = (rect.width || 800) * dpr
  cvs.height = (rect.height || 600) * dpr
  const ctx = cvs.getContext('2d')!
  ctx.scale(dpr, dpr)
  ctx.fillStyle = '#fff'
  ctx.fillRect(0, 0, cvs.width, cvs.height)
  ctx.drawImage(img, 0, 0, rect.width || 800, rect.height || 600)
  return new Promise(r => cvs.toBlob(b => r(b), 'image/png'))
}

async function copyDiagramAsImage() {
  const blob = await svgToBlob()
  if (!blob) return
  try {
    await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })])
  } catch {
    alert('复制图片失败，请尝试「保存图片」')
  }
}

async function saveDiagramAsImage() {
  const blob = await svgToBlob()
  if (!blob) return
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = 'diagram.png'
  document.body.appendChild(a); a.click()
  setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url) }, 100)
}
</script>

<template>
  <div class="diagram">
    <div class="diagram-header">
      <h3 class="section-heading">需求场景流程图</h3>
      <select v-if="requirements" class="dia-select" :value="selectedType" @change="onTypeChange(($event.target as HTMLSelectElement).value)">
        <option v-for="opt in diagramOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>
    <div v-if="renderError" class="error-box">
      <p class="error-title">Mermaid 渲染错误</p>
      <pre class="error-detail">{{ renderError }}</pre>
    </div>
    <div v-else-if="displayCode" class="svg-container" v-html="svgRef" />
    <p v-else class="empty">无流程图</p>

    <div v-if="displayCode" class="code-editor">
      <div class="editor-toolbar">
        <span class="editor-label">编辑 Mermaid 代码</span>
        <div class="editor-actions">
          <span v-if="editorDirty" class="editor-hint">已修改·自动渲染</span>
          <button class="btn btn-xs btn-outline" @click="openDiagramInNewTab">新标签页</button>
          <button class="btn btn-xs btn-outline" @click="copyDiagramAsImage">复制图片</button>
          <button class="btn btn-xs btn-outline" @click="saveDiagramAsImage">保存图片</button>
          <button class="btn btn-xs btn-outline" @click="copyCode">复制代码</button>
          <button class="btn btn-xs btn-ghost" @click="showEditor=!showEditor">{{ showEditor?'收起':'展开' }}</button>
        </div>
      </div>
      <textarea v-if="showEditor" v-model="editableCode" class="editor-textarea" rows="6" spellcheck="false"></textarea>
    </div>
  </div>
</template>

<style scoped>
.diagram-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.diagram-header .section-heading {
  margin: 0;
}
.dia-select {
  font-size: 12px;
  padding: 3px 8px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
.section-heading {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: .5px;
}
.svg-container { overflow: auto; background: #fff; border-radius: 8px; border: 1px solid var(--border); padding: 16px; min-height: 300px; display: flex; align-items: flex-start; justify-content: center; }
.svg-container :deep(svg) { max-width: 100%; height: auto; }
.error-box { border: 1px solid #f5c6cb; background: #fce8e6; border-radius: 8px; padding: 12px; }
.error-title { font-size: 14px; font-weight: 600; color: #c5221f; margin: 0 0 8px; }
.error-detail { font-size: 12px; color: #c5221f; white-space: pre-wrap; margin: 0; }
.empty { font-size: 13px; color: var(--text-secondary); font-style: italic; }
.code-editor { margin-top: 12px; }
.editor-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.editor-label { font-size: 11px; color: var(--text-secondary); font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }
.editor-actions { display: flex; align-items: center; gap: 6px; }
.editor-hint { font-size: 11px; color: var(--primary); font-style: italic; }
.editor-textarea { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 6px; background: #1e1e1e; color: #d4d4d4; font-family: 'SF Mono','Menlo','Monaco','Courier New',monospace; font-size: 12px; line-height: 1.5; resize: vertical; min-height: 80px; tab-size: 2; box-sizing: border-box; }
.editor-textarea:focus { outline: none; border-color: var(--primary); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 4px; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; cursor: pointer; transition: all .15s; white-space: nowrap; border: none; }
.btn-xs { padding: 2px 8px; font-size: 11px; }
.btn-outline { border: 1px solid var(--border); background: transparent; color: var(--text); }
.btn-outline:hover { background: var(--bg); }
.btn-ghost { background: transparent; color: var(--text-secondary); border: none; }
.btn-ghost:hover { color: var(--text); }
</style>

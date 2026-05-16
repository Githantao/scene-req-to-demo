<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  code: string
}>()

const emit = defineEmits<{
  'update:code': [value: string]
}>()

const svgRef = ref<string>('')
const renderError = ref<string>('')
const editableCode = ref('')
const showEditor = ref(true)
const editorDirty = ref(false)
let editorTimer: ReturnType<typeof setTimeout> | null = null
let mermaid: any = null

watch(() => props.code, (val) => {
  if (val) {
    editableCode.value = val
    editorDirty.value = false
  }
  render()
})

watch(editableCode, (val) => {
  if (!val || val === props.code) { editorDirty.value = false; return }
  editorDirty.value = true
  if (editorTimer) clearTimeout(editorTimer)
  editorTimer = setTimeout(async () => {
    emit('update:code', val)
    await renderCode(val)
    editorDirty.value = false
  }, 600)
})

onMounted(() => {
  if (props.code) {
    editableCode.value = props.code
    render()
  }
})

async function render() {
  await renderCode(props.code)
}

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
</script>

<template>
  <div class="diagram">
    <h3 class="section-heading">系统流程图</h3>
    <div v-if="renderError" class="error-box">
      <p class="error-title">Mermaid 渲染错误</p>
      <pre class="error-detail">{{ renderError }}</pre>
    </div>
    <div v-else-if="code" class="svg-container" v-html="svgRef" />
    <p v-else class="empty">无流程图</p>

    <div v-if="code" class="code-editor">
      <div class="editor-toolbar">
        <span class="editor-label">编辑 Mermaid 代码</span>
        <div class="editor-actions">
          <span v-if="editorDirty" class="editor-hint">已修改·自动渲染</span>
          <button class="btn btn-xs btn-outline" @click="copyCode">复制</button>
          <button class="btn btn-xs btn-ghost" @click="showEditor=!showEditor">{{ showEditor?'收起':'展开' }}</button>
        </div>
      </div>
      <textarea v-if="showEditor" v-model="editableCode" class="editor-textarea" rows="6" spellcheck="false"></textarea>
    </div>
  </div>
</template>

<style scoped>
.section-heading {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: .5px;
}
.svg-container { overflow: auto; background: #fff; border-radius: 8px; border: 1px solid var(--border); padding: 16px; min-height: 200px; }
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

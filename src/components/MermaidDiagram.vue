<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  code: string
}>()

const svgRef = ref<string>('')
const renderError = ref<string>('')

let mermaid: any = null

async function render() {
  if (!props.code) return

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
    const cleaned = props.code.replace(/\\n/g, '\n').trim()
    const { svg } = await mermaid.default.render('mermaid-' + Date.now(), cleaned)
    svgRef.value = svg
  } catch (e: any) {
    renderError.value = e.message || '渲染失败'
    svgRef.value = ''
  }
}

watch(() => props.code, () => render(), { immediate: false })
onMounted(() => { if (props.code) render() })
</script>

<template>
  <div class="diagram">
    <h3 class="section-heading">系统流程图</h3>
    <div v-if="renderError" class="error-box">
      <p class="error-title">Mermaid 渲染错误</p>
      <pre class="error-detail">{{ renderError }}</pre>
      <details>
        <summary>查看源码</summary>
        <pre class="code-block">{{ code }}</pre>
      </details>
    </div>
    <div v-else-if="code" class="svg-container" v-html="svgRef" />
    <p v-else class="empty">无流程图</p>
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

.svg-container {
  overflow: auto;
  background: #fff;
  border-radius: 8px;
  border: 1px solid var(--border);
  padding: 16px;
  min-height: 200px;
}

.svg-container :deep(svg) {
  max-width: 100%;
  height: auto;
}

.error-box {
  border: 1px solid #f5c6cb;
  background: #fce8e6;
  border-radius: 8px;
  padding: 12px;
}

.error-title {
  font-size: 14px;
  font-weight: 600;
  color: #c5221f;
  margin: 0 0 8px;
}

.error-detail {
  font-size: 12px;
  color: #c5221f;
  white-space: pre-wrap;
  margin: 0;
}

.code-block {
  font-size: 12px;
  background: var(--bg);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 8px 0 0;
}

.empty {
  font-size: 13px;
  color: var(--text-secondary);
  font-style: italic;
}
</style>

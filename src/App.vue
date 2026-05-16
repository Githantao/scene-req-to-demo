<script setup lang="ts">
import { ref, computed } from 'vue'
import AppHeader from './components/AppHeader.vue'
import ModelSelector from './components/ModelSelector.vue'
import SceneInput from './components/SceneInput.vue'
import LoadingOverlay from './components/LoadingOverlay.vue'
import AnalysisResult from './components/AnalysisResult.vue'
import HistoryPanel from './components/HistoryPanel.vue'
import { useWebLLM } from './composables/useWebLLM'
import { useAnalysis } from './composables/useAnalysis'
import { useHistory } from './composables/useHistory'
import type { HistoryEntry } from './types'

const llm = useWebLLM()
const analysis = useAnalysis()
const history = useHistory()

const showHistory = ref(false)
const sceneText = ref('')

const modelStatusText = computed(() => {
  if (llm.status.value === 'idle') return ''
  if (llm.status.value === 'downloading') return '下载中...'
  if (llm.status.value === 'loading') return '加载中...'
  if (llm.status.value === 'ready') return `${llm.currentModel.value.split('-').slice(0, 2).join('-')} 已就绪`
  if (llm.status.value === 'error') return '加载失败'
  return ''
})

async function handleLoadModel() {
  try {
    await llm.loadModel(llm.currentModel.value)
  } catch {
    // error already set in composable
  }
}

async function handleUnloadModel() {
  llm.unloadModel()
  analysis.reset()
}

async function handleAnalyze() {
  const input = document.querySelector('.textarea') as HTMLTextAreaElement
  if (!input) return

  sceneText.value = input.value.trim()
  if (!sceneText.value) return

  const result = await analysis.analyze(sceneText.value, (sys, usr) => llm.chat(sys, usr))

  if (result) {
    history.addEntry({
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
      timestamp: Date.now(),
      sceneText: sceneText.value,
      result,
      modelUsed: llm.currentModel.value,
    })
  }
}

function handleRestoreEntry(entry: HistoryEntry) {
  sceneText.value = entry.sceneText
  analysis.result.value = entry.result
  analysis.status.value = 'done'
  showHistory.value = false
}

function handleDeleteEntry(id: string) {
  history.deleteEntry(id)
}

function exportMarkdown() {
  const r = analysis.result.value?.requirements
  if (!r) return
  let md = '# ' + r.title + '\n\n'
  if (r.layers) {
    md += '## 需求分层\n\n'
    if (r.layers.business) md += '### 🏢 业务层\n- **目标：** ' + r.layers.business.goal + '\n- **价值：** ' + r.layers.business.value + '\n\n'
    if (r.layers.user) md += '### 👤 用户层\n- **场景：** ' + r.layers.user.scenario + '\n- **痛点：** ' + (r.layers.user.painPoints||[]).join('、') + '\n\n'
    if (r.layers.system) md += '### ⚙️ 系统层\n- **职责：** ' + r.layers.system.summary + '\n\n'
  }
  md += '## 系统边界\n\n' + r.systemBoundary + '\n\n'
  if (r.stakeholders?.length) md += '## 干系人\n\n' + r.stakeholders.map(s=>'- '+s).join('\n') + '\n\n'
  if (r.functionalRequirements?.length) {
    md += '## 功能需求\n\n'
    r.functionalRequirements.forEach(fr => {
      const p = fr.priority==='high'?'高':fr.priority==='medium'?'中':'低'
      md += '### ' + fr.id + ' ' + fr.name + '（' + p + '优先级）\n' + fr.description + '\n\n'
    })
  }
  if (r.dataFlows?.length) {
    md += '## 数据流\n\n| 来源 | 方向 | 目标 | 数据 | 类型 |\n|------|------|------|------|------|\n'
    r.dataFlows.forEach(df => {
      const t = df.type==='input'?'输入':df.type==='output'?'输出':'存储'
      md += '| ' + df.from + ' | → | ' + df.to + ' | ' + df.data + ' | ' + t + ' |\n'
    })
    md += '\n'
  }
  if (r.nonFunctionalRequirements?.length) md += '## 非功能性需求\n\n' + r.nonFunctionalRequirements.map(n=>'- '+n).join('\n') + '\n\n'
  md += '## 系统流程图\n\n```mermaid\n' + (analysis.result.value?.mermaidCode||'') + '\n```\n'
  const blob = new Blob([md], {type:'text/markdown;charset=utf-8'})
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = r.title.replace(/[\\/:*?"<>|]/g,'_') + '.md'
  document.body.appendChild(a); a.click()
  setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url) }, 100)
}
</script>

<template>
  <div class="app">
    <AppHeader
      :show-history="showHistory"
      :model-status-text="modelStatusText"
      @toggle-history="showHistory = !showHistory"
    />

    <main class="main">
      <div class="container">
        <ModelSelector
          :model-id="llm.currentModel.value"
          :loading-status="llm.status.value"
          :mirror-source="llm.mirrorSource.value"
          @select-model="llm.currentModel.value = $event"
          @load-model="handleLoadModel"
          @unload-model="handleUnloadModel"
          @update:mirror-source="llm.mirrorSource.value = $event"
        />

        <SceneInput
          :model-status-text="modelStatusText"
          :model-progress="llm.progress.value.progress"
          :model-ready="llm.status.value === 'ready'"
          :analysis-status="analysis.status.value"
          @analyze="handleAnalyze"
        />

        <div v-if="analysis.error.value" class="error-banner">
          {{ analysis.error.value }}
        </div>

        <AnalysisResult
          v-if="analysis.result.value"
          :result="analysis.result.value"
          @update:mermaid-code="analysis.result.value.mermaidCode = $event"
          @export-md="exportMarkdown"
        />
      </div>
    </main>

    <LoadingOverlay
      :visible="llm.status.value === 'downloading' || llm.status.value === 'loading'"
      :status="llm.status.value"
      :progress="llm.progress.value"
    />

    <HistoryPanel
      :visible="showHistory"
      :entries="history.entries.value"
      @restore="handleRestoreEntry"
      @delete="handleDeleteEntry"
      @clear="history.clearAll"
      @close="showHistory = false"
    />
  </div>
</template>

<style>
:root {
  --primary: #1967d2;
  --primary-alpha: rgba(25, 103, 210, .1);
  --bg: #f8f9fa;
  --surface: #ffffff;
  --text: #202124;
  --text-secondary: #5f6368;
  --border: #dadce0;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
}

.app {
  min-height: 100vh;
}

.main {
  padding: 24px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all .15s;
  white-space: nowrap;
}

.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn-primary:disabled {
  opacity: .5;
  cursor: not-allowed;
}

.btn-outline {
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text);
}

.btn-outline:hover {
  background: var(--bg);
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border: none;
}

.btn-ghost:hover {
  color: var(--text);
}

.error-banner {
  background: #fce8e6;
  border: 1px solid #f5c6cb;
  color: #c5221f;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
}
</style>

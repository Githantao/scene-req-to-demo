<script setup lang="ts">
import { ref } from 'vue'

const APP_VERSION = '2.0.0'
const RELEASE_NOTES = [
  { ver:'v2.0.0', date:'2026-05-16', items:['多图表类型支持：根据场景自动选择 flowchart / sequenceDiagram / classDiagram / stateDiagram-v2 / erDiagram','图表类型徽标展示','System Prompt 5 种图表选择规则','版本信息与更新说明展示'] },
  { ver:'v1.1.0', date:'2026-05-16', items:['国内镜像下载源（hf-mirror.com）','打包与跨电脑使用文档'] },
  { ver:'v1.0.0', date:'2026-05-16', items:['Mermaid 代码编辑器 + 实时预览','三层需求展示（BR→UR→SR）','导出 Markdown','复制 Mermaid 代码'] },
  { ver:'v0.2.0', date:'2026-05-16', items:['System Prompt 需求分析规则升级','安装 requirements-analysis / mermaid-diagrams skills'] },
  { ver:'v0.1.0', date:'2026-05-16', items:['项目初始化：Vue + Vite + TypeScript 工程','单 HTML 文件版本 analyzer.html','WebLLM 浏览器本地推理（3 模型支持）','基础 Mermaid 流程图生成','模型下载进度 + 缓存管理','历史记录（localStorage）','WebGPU 检测 + 首次引导'] },
]

defineProps<{
  showHistory: boolean
  modelStatusText: string
}>()

const emit = defineEmits<{
  toggleHistory: []
}>()

const showReleaseNotes = ref(false)
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <h1 class="app-title">场景需求分析器</h1>
      <span class="subtitle">自然语言 → 系统需求 + 流程图 <span class="ver-badge">v{{ APP_VERSION }}</span></span>
    </div>
    <div class="header-right">
      <span class="model-status">{{ modelStatusText }}</span>
      <button class="btn-ghost btn-icon" @click="showReleaseNotes = !showReleaseNotes" title="更新说明">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
      </button>
      <button
        class="btn-ghost"
        :class="{ active: showHistory }"
        @click="emit('toggleHistory')"
        title="历史记录"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        历史
      </button>
    </div>
  </header>

  <!-- release notes overlay -->
  <Teleport to="body">
    <div v-if="showReleaseNotes" class="rn-overlay" @click.self="showReleaseNotes = false">
      <div class="rn-panel">
        <div class="rn-h">
          <div><span class="rn-ver-badge">v{{ APP_VERSION }}</span><h2>更新说明</h2></div>
          <button class="rn-close" @click="showReleaseNotes = false">✕</button>
        </div>
        <div class="rn-body">
          <div v-for="rn in RELEASE_NOTES" :key="rn.ver" class="rn-item" :class="{active: rn.ver === 'v' + APP_VERSION}">
            <div class="rn-ver">{{ rn.ver }}</div>
            <div class="rn-date">{{ rn.date }}</div>
            <ul class="rn-list">
              <li v-for="item in rn.items" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.app-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

.subtitle {
  font-size: 13px;
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.model-status {
  font-size: 12px;
  color: var(--text-secondary);
}

.btn-ghost {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all .15s;
}

.btn-ghost:hover {
  background: var(--bg);
  color: var(--text);
}

.btn-ghost.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.ver-badge { font-size:11px; font-weight:600; color:var(--text-secondary); background:var(--bg); padding:1px 6px; border-radius:3px; margin-left:4px; }
.btn-icon { padding:6px 8px; }

.rn-overlay{position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:950;display:flex;align-items:center;justify-content:center}
.rn-panel{width:500px;max-width:90vw;max-height:80vh;background:var(--surface);border-radius:12px;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.2)}
.rn-h{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border)}
.rn-h div{display:flex;align-items:center;gap:8px}
.rn-h h2{font-size:16px;font-weight:600;margin:0}
.rn-ver-badge{font-size:11px;font-weight:700;background:var(--primary);color:#fff;padding:2px 8px;border-radius:4px}
.rn-close{background:none;border:none;font-size:18px;cursor:pointer;color:var(--text-secondary);padding:4px}
.rn-close:hover{color:var(--text)}
.rn-body{flex:1;overflow-y:auto;padding:16px 20px}
.rn-item{padding:12px 0;border-bottom:1px solid var(--border)}
.rn-item.active{background:var(--primary-alpha);margin:-8px -12px;padding:12px;border-radius:8px;border-bottom-color:transparent}
.rn-item:last-child{border-bottom:none}
.rn-ver{font-size:15px;font-weight:700;color:var(--text)}
.rn-date{font-size:11px;color:var(--text-secondary);margin:2px 0 6px}
.rn-list{margin:0;padding-left:18px}
.rn-list li{font-size:13px;line-height:1.6;color:var(--text)}
</style>

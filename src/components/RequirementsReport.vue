<script setup lang="ts">
import { ref } from 'vue'
import type { Requirements } from '../types'

const props = defineProps<{
  requirements: Requirements
}>()

const emit = defineEmits<{
  exportMd: []
}>()

const collapseFR = ref(true)
const collapseDF = ref(true)
const collapseNFR = ref(true)

function priorityClass(p: string) {
  if (p === 'high') return 'tag-red'
  if (p === 'medium') return 'tag-yellow'
  return 'tag-gray'
}
</script>

<template>
  <div class="report">
    <h2 class="report-title">{{ requirements.title }}
      <span v-if="requirements.diagramType" class="dia-badge">{{ {flowchart:'流程图',sequenceDiagram:'时序图',classDiagram:'类图','stateDiagram-v2':'状态图',erDiagram:'ER图'}[requirements.diagramType] || requirements.diagramType }}</span>
      <button class="btn-export" @click="emit('exportMd')">导出 MD</button>
    </h2>

    <!-- three layers -->
    <div v-if="requirements.layers" class="layers-row">
      <div class="layer-card layer-biz">
        <span class="layer-ico">🏢</span>
        <div class="layer-body">
          <div class="layer-lbl">业务层</div>
          <div class="layer-t">{{ requirements.layers.business?.goal }}</div>
          <div class="layer-d">{{ requirements.layers.business?.value }}</div>
        </div>
      </div>
      <div class="layer-arr">→</div>
      <div class="layer-card layer-user">
        <span class="layer-ico">👤</span>
        <div class="layer-body">
          <div class="layer-lbl">用户层</div>
          <div class="layer-t">{{ requirements.layers.user?.scenario }}</div>
          <div class="layer-d">{{ requirements.layers.user?.painPoints?.join('、') }}</div>
        </div>
      </div>
      <div class="layer-arr">→</div>
      <div class="layer-card layer-sys">
        <span class="layer-ico">⚙️</span>
        <div class="layer-body">
          <div class="layer-lbl">系统层</div>
          <div class="layer-t">{{ requirements.layers.system?.summary }}</div>
        </div>
      </div>
    </div>

    <section class="section">
      <h3 class="section-heading">系统边界</h3>
      <p class="section-text">{{ requirements.systemBoundary }}</p>
    </section>

    <section class="section">
      <h3 class="section-heading">干系人</h3>
      <div class="tag-list">
        <span v-for="s in requirements.stakeholders" :key="s" class="tag tag-blue">{{ s }}</span>
      </div>
    </section>

    <section class="section">
      <h3 class="section-heading collapsible" @click="collapseFR = !collapseFR">
        <span class="collapse-icon">{{ collapseFR ? '▶' : '▼' }}</span> 功能需求
      </h3>
      <template v-if="!collapseFR">
        <div v-for="fr in requirements.functionalRequirements" :key="fr.id" class="req-card">
          <div class="req-header">
            <span class="req-id">{{ fr.id }}</span>
            <span class="tag" :class="priorityClass(fr.priority)">{{ fr.priority === 'high' ? '高' : fr.priority === 'medium' ? '中' : '低' }}</span>
          </div>
          <h4 class="req-name">{{ fr.name }}</h4>
          <p class="req-desc">{{ fr.description }}</p>
        </div>
        <p v-if="requirements.functionalRequirements.length === 0" class="empty">无功能需求</p>
      </template>
    </section>

    <section class="section">
      <h3 class="section-heading collapsible" @click="collapseDF = !collapseDF">
        <span class="collapse-icon">{{ collapseDF ? '▶' : '▼' }}</span> 数据流
      </h3>
      <template v-if="!collapseDF">
        <div v-for="(df, i) in requirements.dataFlows" :key="i" class="dataflow-item">
          <span class="df-from">{{ df.from }}</span>
          <span class="df-arrow">→</span>
          <span class="df-to">{{ df.to }}</span>
          <span class="df-data">({{ df.data }})</span>
          <span class="tag" :class="df.type === 'input' ? 'tag-green' : df.type === 'output' ? 'tag-blue' : 'tag-gray'" style="margin-left:auto">
            {{ df.type === 'input' ? '输入' : df.type === 'output' ? '输出' : '存储' }}
          </span>
        </div>
        <p v-if="requirements.dataFlows.length === 0" class="empty">无数据流</p>
      </template>
    </section>

    <section class="section">
      <h3 class="section-heading collapsible" @click="collapseNFR = !collapseNFR">
        <span class="collapse-icon">{{ collapseNFR ? '▶' : '▼' }}</span> 非功能性需求
      </h3>
      <template v-if="!collapseNFR">
        <ul v-if="requirements.nonFunctionalRequirements.length" class="nfr-list">
          <li v-for="(nfr, i) in requirements.nonFunctionalRequirements" :key="i">{{ nfr }}</li>
        </ul>
        <p v-else class="empty">无非功能性需求</p>
      </template>
    </section>
  </div>
</template>

<style scoped>
.report-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 20px;
}

.section {
  margin-bottom: 20px;
}

.section-heading {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: .5px;
}
.section-heading.collapsible {
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 6px;
}
.section-heading.collapsible:hover {
  color: var(--text);
}
.collapse-icon {
  font-size: 10px;
  width: 12px;
  text-align: center;
  flex-shrink: 0;
}

.section-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  margin: 0;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.tag-blue { background: #e8f0fe; color: #1967d2; }
.tag-red { background: #fce8e6; color: #c5221f; }
.tag-yellow { background: #fef7e0; color: #ea8600; }
.tag-gray { background: #f1f3f4; color: #5f6368; }
.tag-green { background: #e6f4ea; color: #137333; }

.req-card {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
}

.req-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.req-id {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  font-family: monospace;
}

.req-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin: 4px 0;
}

.req-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.dataflow-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}

.dataflow-item:last-child {
  border-bottom: none;
}

.df-from, .df-to {
  font-weight: 500;
  color: var(--text);
}

.df-arrow {
  color: var(--primary);
}

.df-data {
  color: var(--text-secondary);
}

.nfr-list {
  margin: 0;
  padding-left: 20px;
}

.nfr-list li {
  font-size: 13px;
  color: var(--text);
  line-height: 1.6;
  margin-bottom: 4px;
}

.empty {
  font-size: 13px;
  color: var(--text-secondary);
  font-style: italic;
}

.btn-export { font-size:11px; padding:2px 10px; border:1px solid var(--border); border-radius:4px; background:transparent; color:var(--text-secondary); cursor:pointer; vertical-align:middle; margin-left:8px; font-weight:400; }
.btn-export:hover { background:var(--bg); color:var(--text); }
.dia-badge { display:inline-block; font-size:10px; font-weight:700; padding:2px 8px; border-radius:4px; background:#1967d2; color:#fff; margin-left:6px; vertical-align:middle; text-transform:uppercase; letter-spacing:.3px; }

.layers-row { display:flex; align-items:stretch; gap:8px; margin-bottom:20px; }
@media(max-width:600px){ .layers-row { flex-direction:column; } }
.layer-card { flex:1; border-radius:8px; padding:12px; display:flex; gap:10px; align-items:flex-start; }
.layer-biz { background:#e8f0fe; border:1px solid #c5d9f7; }
.layer-user { background:#e6f4ea; border:1px solid #b7dfc5; }
.layer-sys { background:#fef7e0; border:1px solid #fde8b3; }
.layer-ico { font-size:20px; line-height:1; }
.layer-body { min-width:0; }
.layer-lbl { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.5px; opacity:.6; margin-bottom:2px; }
.layer-t { font-size:13px; font-weight:600; line-height:1.4; margin-bottom:2px; }
.layer-d { font-size:11px; color:var(--text-secondary); line-height:1.4; }
.layer-arr { display:flex; align-items:center; color:var(--text-secondary); font-size:18px; padding:0 2px; }
@media(max-width:600px){ .layer-arr { transform:rotate(90deg); padding:2px 0; justify-content:center; } }
</style>

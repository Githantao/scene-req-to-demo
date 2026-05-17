<script setup lang="ts">
import type { AnalysisResult } from '../types'
import RequirementsReport from './RequirementsReport.vue'
import MermaidDiagram from './MermaidDiagram.vue'

defineProps<{
  result: AnalysisResult
  diagramType?: string
}>()

const emit = defineEmits<{
  'update:mermaidCode': [value: string]
  'update:diagramType': [value: string]
  'exportMd': []
}>()
</script>

<template>
  <div class="analysis-result">
    <div class="result-panel result-left">
      <RequirementsReport :requirements="result.requirements" @export-md="emit('exportMd')" />
    </div>
    <div class="result-divider" />
    <div class="result-panel result-right">
      <MermaidDiagram
        :code="result.mermaidCode"
        :requirements="result.requirements"
        :diagram-type="diagramType || result.requirements.diagramType || 'flowchart'"
        @update:code="emit('update:mermaidCode', $event)"
        @update:diagram-type="emit('update:diagramType', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
.analysis-result {
  display: flex;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  background: var(--surface);
}

.result-panel {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: 70vh;
}

.result-divider {
  width: 1px;
  background: var(--border);
}

@media (max-width: 768px) {
  .analysis-result {
    flex-direction: column;
  }
  .result-divider {
    width: 100%;
    height: 1px;
  }
}
</style>

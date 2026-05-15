<script setup lang="ts">
import type { AnalysisResult } from '../types'
import RequirementsReport from './RequirementsReport.vue'
import MermaidDiagram from './MermaidDiagram.vue'

defineProps<{
  result: AnalysisResult
}>()
</script>

<template>
  <div class="analysis-result">
    <div class="result-panel result-left">
      <RequirementsReport :requirements="result.requirements" />
    </div>
    <div class="result-divider" />
    <div class="result-panel result-right">
      <MermaidDiagram :code="result.mermaidCode" />
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

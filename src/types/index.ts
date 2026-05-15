export interface FunctionalRequirement {
  id: string
  name: string
  description: string
  priority: 'high' | 'medium' | 'low'
}

export interface DataFlow {
  from: string
  to: string
  data: string
  type: 'input' | 'output' | 'storage'
}

export interface Requirements {
  title: string
  systemBoundary: string
  stakeholders: string[]
  functionalRequirements: FunctionalRequirement[]
  dataFlows: DataFlow[]
  nonFunctionalRequirements: string[]
}

export interface AnalysisResult {
  requirements: Requirements
  mermaidCode: string
  rawOutput: string
}

export interface HistoryEntry {
  id: string
  timestamp: number
  sceneText: string
  result: AnalysisResult
  modelUsed: string
}

export type ModelId = string

export interface ModelOption {
  id: ModelId
  label: string
  description: string
  size: string
}

export type LoadingStatus = 'idle' | 'downloading' | 'loading' | 'ready' | 'error'
export type AnalysisStatus = 'idle' | 'analyzing' | 'done' | 'error'

export interface ProgressInfo {
  text: string
  progress: number
  timeElapsed: number
}

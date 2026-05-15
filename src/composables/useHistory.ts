import { ref } from 'vue'
import type { HistoryEntry } from '../types'

const STORAGE_KEY = 'scene-to-req-history'
const MAX_ENTRIES = 50

export function useHistory() {
  const entries = ref<HistoryEntry[]>(loadAll())

  function loadAll(): HistoryEntry[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      return raw ? JSON.parse(raw) : []
    } catch {
      return []
    }
  }

  function saveAll() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(entries.value))
    } catch {
      // localStorage full or unavailable
    }
  }

  function addEntry(entry: HistoryEntry) {
    entries.value.unshift(entry)
    if (entries.value.length > MAX_ENTRIES) {
      entries.value = entries.value.slice(0, MAX_ENTRIES)
    }
    saveAll()
  }

  function deleteEntry(id: string) {
    entries.value = entries.value.filter(e => e.id !== id)
    saveAll()
  }

  function clearAll() {
    entries.value = []
    localStorage.removeItem(STORAGE_KEY)
  }

  function getEntry(id: string): HistoryEntry | undefined {
    return entries.value.find(e => e.id === id)
  }

  return {
    entries,
    addEntry,
    deleteEntry,
    clearAll,
    getEntry,
  }
}

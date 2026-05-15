import { ref } from 'vue'

const WEBCACHE_PREFIXES = ['mlc', 'webllm', 'web-llm', 'llm']

export function useModelCache() {
  const cacheSize = ref<string>('')
  const cacheEntries = ref(0)
  const isClearing = ref(false)

  async function scanCache(): Promise<{ entries: number; caches: string[] }> {
    if (!('caches' in window)) return { entries: 0, caches: [] }

    const names = await caches.keys()
    const relevant = names.filter(n =>
      WEBCACHE_PREFIXES.some(p => n.toLowerCase().includes(p))
    )

    let total = 0
    for (const name of relevant) {
      const cache = await caches.open(name)
      const keys = await cache.keys()
      total += keys.length
    }

    return { entries: total, caches: relevant }
  }

  async function refresh() {
    const { entries } = await scanCache()
    cacheEntries.value = entries

    if ('storage' in navigator && 'estimate' in navigator.storage) {
      const est = await navigator.storage.estimate()
      const usage = est.usage || 0
      cacheSize.value = formatBytes(usage)
    } else {
      cacheSize.value = entries > 0 ? '~' + formatBytes(entries * 50 * 1024 * 1024) : '0 KB'
    }
  }

  async function clearCache(): Promise<boolean> {
    isClearing.value = true
    try {
      const { caches: relevant } = await scanCache()
      for (const name of relevant) {
        await caches.delete(name)
      }
      if ('storage' in navigator && 'estimate' in navigator.storage) {
          await navigator.serviceWorker?.getRegistration().then(r => r?.unregister())
      }
      await refresh()
      return true
    } catch {
      return false
    } finally {
      isClearing.value = false
    }
  }

  return {
    cacheSize,
    cacheEntries,
    isClearing,
    refresh,
    clearCache,
  }
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 KB'
  const units = ['B', 'KB', 'MB', 'GB']
  const i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)
  const val = bytes / Math.pow(1024, i)
  return `${val.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}

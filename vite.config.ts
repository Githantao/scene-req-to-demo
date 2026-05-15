import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  optimizeDeps: {
    exclude: ['@mlc-ai/web-llm'],
  },
  build: {
    chunkSizeWarningLimit: 3000,
  },
})

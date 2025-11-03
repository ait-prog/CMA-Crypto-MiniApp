import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages использует подпуть репозитория
const base = process.env.NODE_ENV === 'production' ? '/CMA-Crypto-MiniApp/' : '/'

export default defineConfig({
  plugins: [react()],
  base: base,
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  }
})


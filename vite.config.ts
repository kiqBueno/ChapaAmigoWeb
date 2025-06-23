import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'exclude-carousel-images',
      generateBundle(_, bundle) {
        Object.keys(bundle).forEach(fileName => {
          if (fileName.startsWith('carrousel') && fileName.endsWith('.jpg')) {
            delete bundle[fileName]
          }
          if (fileName === 'temp_carrousel.jpg') {
            delete bundle[fileName]
          }
        })
      }
    }
  ],
  build: {
    rollupOptions: {
      external: [],
    },
    copyPublicDir: true
  },
  publicDir: 'public',
  base: '/'
})

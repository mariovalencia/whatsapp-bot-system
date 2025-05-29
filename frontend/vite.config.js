import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true
    },
    // Configuración clave para el proxy de API
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Usa el nombre del servicio de tu backend en Docker
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false,
        ws: true
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  define: {
    'process.env': {
      ...process.env,
      // Inyecta variables específicas para el frontend
      VITE_API_BASE_URL: JSON.stringify('http://localhost:5173/api'),
      VITE_GOOGLE_CLIENT_ID: JSON.stringify(process.env.VITE_GOOGLE_CLIENT_ID)
    }
  }
});
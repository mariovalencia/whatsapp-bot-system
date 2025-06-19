// vite.config.js
import { defineConfig } from "file:///app/node_modules/vite/dist/node/index.js";
import react from "file:///app/node_modules/@vitejs/plugin-react/dist/index.mjs";
var vite_config_default = defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true
    },
    // Configuración clave para el proxy de API
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        // Usa el nombre del servicio de tu backend en Docker
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
        secure: false,
        ws: true
      },
      "/auth": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  },
  define: {
    "process.env": {
      ...process.env,
      // Inyecta variables específicas para el frontend
      VITE_API_BASE_URL: JSON.stringify("http://localhost:5173/api"),
      VITE_GOOGLE_CLIENT_ID: JSON.stringify(process.env.VITE_GOOGLE_CLIENT_ID)
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvYXBwXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvYXBwL3ZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9hcHAvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJztcbmltcG9ydCByZWFjdCBmcm9tICdAdml0ZWpzL3BsdWdpbi1yZWFjdCc7XG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIHBsdWdpbnM6IFtyZWFjdCgpXSxcbiAgc2VydmVyOiB7XG4gICAgaG9zdDogdHJ1ZSxcbiAgICBwb3J0OiA1MTczLFxuICAgIHdhdGNoOiB7XG4gICAgICB1c2VQb2xsaW5nOiB0cnVlXG4gICAgfSxcbiAgICAvLyBDb25maWd1cmFjaVx1MDBGM24gY2xhdmUgcGFyYSBlbCBwcm94eSBkZSBBUElcbiAgICBwcm94eToge1xuICAgICAgJy9hcGknOiB7XG4gICAgICAgIHRhcmdldDogJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMCcsICAvLyBVc2EgZWwgbm9tYnJlIGRlbCBzZXJ2aWNpbyBkZSB0dSBiYWNrZW5kIGVuIERvY2tlclxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgIHJld3JpdGU6IChwYXRoKSA9PiBwYXRoLnJlcGxhY2UoL15cXC9hcGkvLCAnJyksXG4gICAgICAgIHNlY3VyZTogZmFsc2UsXG4gICAgICAgIHdzOiB0cnVlXG4gICAgICB9LFxuICAgICAgJy9hdXRoJzoge1xuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWVcbiAgICAgIH1cbiAgICB9XG4gIH0sXG4gIGRlZmluZToge1xuICAgICdwcm9jZXNzLmVudic6IHtcbiAgICAgIC4uLnByb2Nlc3MuZW52LFxuICAgICAgLy8gSW55ZWN0YSB2YXJpYWJsZXMgZXNwZWNcdTAwRURmaWNhcyBwYXJhIGVsIGZyb250ZW5kXG4gICAgICBWSVRFX0FQSV9CQVNFX1VSTDogSlNPTi5zdHJpbmdpZnkoJ2h0dHA6Ly9sb2NhbGhvc3Q6NTE3My9hcGknKSxcbiAgICAgIFZJVEVfR09PR0xFX0NMSUVOVF9JRDogSlNPTi5zdHJpbmdpZnkocHJvY2Vzcy5lbnYuVklURV9HT09HTEVfQ0xJRU5UX0lEKVxuICAgIH1cbiAgfVxufSk7Il0sCiAgIm1hcHBpbmdzIjogIjtBQUE4TCxTQUFTLG9CQUFvQjtBQUMzTixPQUFPLFdBQVc7QUFFbEIsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDMUIsU0FBUyxDQUFDLE1BQU0sQ0FBQztBQUFBLEVBQ2pCLFFBQVE7QUFBQSxJQUNOLE1BQU07QUFBQSxJQUNOLE1BQU07QUFBQSxJQUNOLE9BQU87QUFBQSxNQUNMLFlBQVk7QUFBQSxJQUNkO0FBQUE7QUFBQSxJQUVBLE9BQU87QUFBQSxNQUNMLFFBQVE7QUFBQSxRQUNOLFFBQVE7QUFBQTtBQUFBLFFBQ1IsY0FBYztBQUFBLFFBQ2QsU0FBUyxDQUFDLFNBQVMsS0FBSyxRQUFRLFVBQVUsRUFBRTtBQUFBLFFBQzVDLFFBQVE7QUFBQSxRQUNSLElBQUk7QUFBQSxNQUNOO0FBQUEsTUFDQSxTQUFTO0FBQUEsUUFDUCxRQUFRO0FBQUEsUUFDUixjQUFjO0FBQUEsTUFDaEI7QUFBQSxJQUNGO0FBQUEsRUFDRjtBQUFBLEVBQ0EsUUFBUTtBQUFBLElBQ04sZUFBZTtBQUFBLE1BQ2IsR0FBRyxRQUFRO0FBQUE7QUFBQSxNQUVYLG1CQUFtQixLQUFLLFVBQVUsMkJBQTJCO0FBQUEsTUFDN0QsdUJBQXVCLEtBQUssVUFBVSxRQUFRLElBQUkscUJBQXFCO0FBQUEsSUFDekU7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K

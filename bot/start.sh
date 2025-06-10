#!/bin/bash

# Script de inicio para el bot de WhatsApp
echo "🚀 Iniciando bot de WhatsApp..."

# Verificar directorios
echo "📁 Verificando directorios..."
mkdir -p /app/tokens /app/sessions /app/logs

# Verificar permisos
echo "🔐 Verificando permisos..."
ls -la /app/

# Mostrar información del sistema
echo "💻 Información del sistema:"
echo "Usuario actual: $(whoami)"
echo "ID del usuario: $(id)"
echo "Directorio actual: $(pwd)"

# Verificar variables de entorno
echo "🌍 Variables de entorno:"
echo "DJANGO_API_URL: $DJANGO_API_URL"
echo "NODE_ENV: $NODE_ENV"

# Verificar instalación de Node.js
echo "📦 Versiones instaladas:"
node --version
npm --version

# Iniciar la aplicación
echo "🎯 Iniciando aplicación Node.js..."
exec node app.js
# Sistema de Atención al Cliente vía WhatsApp

## Descripción
Sistema automatizado de atención al cliente a través de WhatsApp con capacidad de transferencia a agentes humanos. El sistema utiliza WPPConnect para la integración con WhatsApp, Django para el backend, y React para el frontend.

## Componentes del Sistema
- **Backend (Django)**: API REST para gestión de usuarios, sesiones, mensajes y configuración del bot
- **Frontend (React)**: Interfaz para administradores y técnicos
- **Bot (Python)**: Servicio de conexión con WhatsApp y procesamiento de mensajes
- **Base de datos (PostgreSQL)**: Almacenamiento de datos
- **Nginx**: Servidor web para producción

## Requisitos
- Docker y Docker Compose
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

## Instalación y Ejecución

### Usando Docker (recomendado)
1. Clonar el repositorio
```bash
git clone https://github.com/tuusuario/whatsapp-bot-system.git
cd whatsapp-bot-system
```

2. Configurar las variables de entorno
```bash
cp .env.example .env
# Editar .env con las configuraciones adecuadas
```

3. Construir y ejecutar los contenedores
```bash
docker-compose up -d
```

4. Acceder a la aplicación
- Frontend: http://localhost:80
- Backend API: http://localhost:80/api/
- Admin Django: http://localhost:80/admin/

### Desarrollo local
1. Configurar entorno virtual para el backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

2. Configurar frontend
```bash
cd frontend
npm install
npm start
```

3. Configurar bot
```bash
cd bot
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Estructura del Proyecto
La estructura del proyecto sigue un patrón modular con separación clara de responsabilidades:

- `backend/`: Aplicación Django con múltiples apps
- `frontend/`: Aplicación React
- `bot/`: Servicio Python para conexión con WhatsApp
- `nginx/`: Configuración del servidor web
- `docker-compose.yml`: Configuración de todos los servicios

## Funcionalidades
- Autenticación y gestión de usuarios
- Conexión con WhatsApp mediante escaneo de código QR
- Respuestas automáticas basadas en patrones
- Transferencia a agentes humanos cuando sea necesario
- Interfaz en tiempo real para técnicos
- Reportes y métricas

## Desarrollo
Este proyecto utiliza la metodología Scrum con sprints de 2 semanas. Consulta el cronograma detallado en la documentación del proyecto.

## Licencia
[MIT](LICENSE)
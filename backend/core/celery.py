import os
from celery import Celery

# Establecer la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Crear la instancia de Celery
app = Celery('core')

# Cargar configuración desde settings.py usando el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubrir tareas en todos los apps registrados
app.autodiscover_tasks()

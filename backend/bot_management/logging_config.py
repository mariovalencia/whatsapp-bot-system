import logging
from django.conf import settings
import os

def setup_logging():
    log_dir = os.path.join(settings.BASE_DIR, 'backend', 'logs')
    
    try:
        os.makedirs(log_dir, exist_ok=True)
        
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '{levelname} {asctime} {module} {message}',
                    'style': '{',
                },
            },
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(log_dir, 'bot_management.log'),
                    'formatter': 'verbose',
                    'mode': 'a',
                },
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                'bot_management': {
                    'handlers': ['file', 'console'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
                'nlp_engine': {
                    'handlers': ['file', 'console'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
            },
            'root': {
                    'handlers': ['console'],
                    'level': 'WARNING',
            }
        }
        
        logging.config.dictConfig(logging_config)
    except PermissionError as e:
        logging.error(f"Error de permisos al configurar logging: {e}")
        # Fallback a solo consola
        logging.basicConfig(level=logging.INFO)
    except Exception as e:
        logging.error(f"Error inesperado al configurar logging: {e}")
        logging.basicConfig(level=logging.INFO)
    
from celery import shared_task
from bot_management.nlp_engine import NLPEngine
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def train_nlp_model(self):
    try:
        engine = NLPEngine()
        success = engine.train()
        return {
            "status": "success" if success else "warning",
            "message": "Modelo entrenado" if success else "No hay datos suficientes"
        }
    except Exception as e:
        logger.error(f"Error en entrenamiento: {str(e)}")
        raise self.retry(exc=e, countdown=60)

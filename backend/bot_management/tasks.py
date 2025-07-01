from celery import shared_task
from bot_management.nlp_engine import NLPEngine
import logging

logger = logging.getLogger('bot_management')

@shared_task(bind=True)
def train_nlp_model(self):
    logger.info("🚀 Tarea Celery iniciada: entrenamiento del modelo NLP")
    try:
        engine = NLPEngine()
        success = engine.train()
        if success:
            logger.info("✅ Entrenamiento completado exitosamente")
            return {
                "status": "success",
                "message": "Modelo entrenado correctamente"
            }
        else:
            logger.warning("⚠️ Entrenamiento finalizado sin suficientes datos")
            return {
                "status": "warning",
                "message": "No hay suficientes datos para entrenar el modelo"
            }
    except Exception as e:
        logger.error(f"❌ Error durante el entrenamiento: {str(e)}", exc_info=True)
        raise self.retry(exc=e, countdown=60)

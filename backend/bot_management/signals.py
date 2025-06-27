from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Intent, Response
from .nlp_engine import NLPEngine
import logging

logger = logging.getLogger('bot_management')

nlp_engine = NLPEngine()

@receiver(post_save, sender=Intent)
def retrain_on_intent_update(sender, instance, **kwargs):
    try:
        nlp_engine.train()
    except Exception as e:
        logger.error(f"Error al reentrenar modelo: {e}")

@receiver(post_save, sender=Response)
def retrain_on_response_update(sender, instance, **kwargs):
    if instance.is_default:  # Solo reentrenar si es respuesta predeterminada
        retrain_on_intent_update(sender, instance.intent, **kwargs)
from celery import shared_task
from django.db import transaction
from bot_management.nlp_engine import NLPService
from bot_management.models import Intent
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def train_nlp_model(self):
    try:
        with transaction.atomic():
            intents = Intent.objects.all()
            intent_map = {intent.id: idx for idx, intent in enumerate(intents)}
            
            texts = []
            labels = []
            
            for intent in intents:
                for phrase in intent.training_phrases:
                    texts.append(phrase)
                    labels.append(intent_map[intent.id])
            
            nlp = NLPService()
            nlp.train_model(texts, labels)
            
        return {
            "status": "success",
            "details": f"Model trained with {len(texts)} samples"
        }
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise self.retry(exc=e, countdown=60)
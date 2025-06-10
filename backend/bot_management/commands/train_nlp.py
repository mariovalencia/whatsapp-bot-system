from django.core.management.base import BaseCommand
from backend.bot_management.nlp_engine import NLPEngine

class Command(BaseCommand):
    help = 'Entrena el modelo NLP con las intenciones actuales'

    def handle(self, *args, **options):
        if NLPEngine().train():
            self.stdout.write(self.style.SUCCESS('Modelo NLP entrenado exitosamente'))
        else:
            self.stdout.write(self.style.WARNING('No hay frases de entrenamiento'))
import django
django.setup()
from bot_management.nlp_engine import NLPService

nlp = NLPService()

# Ejemplo de entrenamiento
texts = ["hola cómo estás", "quiero comprar un producto", "dónde está mi pedido"]
labels = [0, 1, 2]  # IDs de intenciones

nlp.train_model(texts, labels)

# Prueba de predicción
intent, confidence = nlp.predict_intent("Hola buenos días")
print(f"Intención: {intent}, Confianza: {confidence:.2%}")
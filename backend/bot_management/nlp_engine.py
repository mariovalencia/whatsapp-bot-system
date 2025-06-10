import spacy
import joblib
import os
from django.conf import settings
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from .models import Intent
from .exceptions import NLPModelNotTrainedError

MODEL_PATH = os.path.join(settings.BASE_DIR, 'bot_management', 'intents_model.pkl')

class NLPEngine:
    def __init__(self):
        self.spacy_nlp = spacy.load('es_core_news_sm')
        self.model = None
        self.label_map = {}
        self.load_model()

    def preprocess(self, text):
        doc = self.spacy_nlp(text.lower())
        return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

    def train(self):
        intents = Intent.objects.filter(is_active=True)
        texts, labels = [], []
        self.label_map = {}

        for idx, intent in enumerate(intents):
            self.label_map[intent.id] = intent.name
            for phrase in intent.training_phrases:
                texts.append(self.preprocess(phrase))
                labels.append(intent.id)

        if not texts:
            return False
        
        unique_labels = set(labels)
        if len(unique_labels) < 2:
            raise ValueError("Se requieren al menos 2 intenciones diferentes con frases de entrenamiento para entrenar el modelo.")

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer()),
            ("clf", LogisticRegression())
        ])
        pipeline.fit(texts, labels)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump((pipeline, self.label_map), MODEL_PATH)
        self.model = pipeline
        return True

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model, self.label_map = joblib.load(MODEL_PATH)

    def predict_intent(self, text):
        if not self.model:
            raise NLPModelNotTrainedError()

        preprocessed = self.preprocess(text)
        intent_id = self.model.predict([preprocessed])[0]
        confidence = max(self.model.predict_proba([preprocessed])[0])
        return intent_id, confidence

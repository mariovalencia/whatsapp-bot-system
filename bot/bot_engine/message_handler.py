import logging
import json
import re

logger = logging.getLogger(__name__)

class MessageHandler:
    """
    Clase para manejar los mensajes entrantes y salientes del bot de WhatsApp
    """
    
    def __init__(self, bot_instance):
        """Inicializa el manejador de mensajes con una instancia del bot"""
        self.bot = bot_instance
        self.knowledge_base = {}
    
    def set_knowledge_base(self, knowledge_base):
        """Establece la base de conocimientos para responder preguntas"""
        self.knowledge_base = knowledge_base
    
    def process_incoming_message(self, message):
        """
        Procesa un mensaje entrante y determina la respuesta apropiada
        
        Args:
            message (dict): Mensaje entrante con formato de WPPConnect
            
        Returns:
            str: Respuesta a enviar al usuario
        """
        try:
            # Solo procesamos mensajes de texto por ahora
            if message.get('type') != 'chat':
                logger.info(f"Ignorando mensaje no soportado de tipo: {message.get('type')}")
                return None
            
            # Extraer el contenido del mensaje
            content = message.get('content', '').strip()
            
            # Si el mensaje está vacío, no procesamos
            if not content:
                return None
            
            # Buscar la mejor respuesta en la base de conocimientos
            response = self.find_best_answer(content)
            
            # Registrar la interacción
            logger.info(f"Mensaje procesado: '{content}', Respuesta: '{response}'")
            
            return response
        
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}")
            return "Lo siento, ha ocurrido un error al procesar tu mensaje."
    
    def find_best_answer(self, message_text):
        """
        Encuentra la mejor respuesta para un mensaje dado basado en la base de conocimientos
        
        Args:
            message_text (str): Texto del mensaje a responder
            
        Returns:
            str: La mejor respuesta encontrada o una respuesta por defecto
        """
        if not self.knowledge_base:
            return "Lo siento, no tengo información para responder a tu pregunta en este momento."
        
        message_text = message_text.lower()
        
        # Buscar coincidencia exacta en preguntas
        for qa_id, qa in self.knowledge_base.get('questions', {}).items():
            if message_text == qa['question'].lower():
                return qa['answer']
        
        # Buscar coincidencia parcial en preguntas
        for qa_id, qa in self.knowledge_base.get('questions', {}).items():
            if message_text in qa['question'].lower() or qa['question'].lower() in message_text:
                return qa['answer']
        
        # Buscar palabras clave
        matched_qa_ids = []
        words = set(self._tokenize(message_text))
        
        for word in words:
            if word in self.knowledge_base.get('keywords', {}):
                matched_qa_ids.extend(self.knowledge_base['keywords'][word])
        
        if matched_qa_ids:
            # Contar coincidencias y obtener la mejor
            from collections import Counter
            count = Counter(matched_qa_ids)
            best_match_id = count.most_common(1)[0][0]
            return self.knowledge_base['questions'][best_match_id]['answer']
        
        # Si no hay coincidencias, respuesta por defecto
        return "Lo siento, no entiendo tu pregunta. ¿Podrías reformularla o ser más específico?"
    
    def _tokenize(self, text):
        """
        Divide el texto en tokens (palabras) para búsqueda
        
        Args:
            text (str): Texto a tokenizar
            
        Returns:
            list: Lista de tokens
        """
        # Eliminar caracteres especiales y convertir a minúsculas
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Dividir por espacios
        return [word for word in text.split() if len(word) > 2]
    
    def format_response(self, response_text):
        """
        Da formato a la respuesta para ser enviada a WhatsApp
        
        Args:
            response_text (str): Texto de respuesta a formatear
            
        Returns:
            str: Respuesta formateada
        """
        # Por ahora, simplemente devolvemos el texto sin modificar
        # En el futuro, podríamos agregar formato, emojis, etc.
        return response_text
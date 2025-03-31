# bot/app.py
import os
import time
import logging
import requests
import json
from datetime import datetime
from wppconnect import WPPConnect

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración del bot
API_URL = os.getenv('API_URL', 'http://localhost:8000/api')
API_TOKEN = os.getenv('API_TOKEN', 'your_api_token')
SESSION_ID = os.getenv('SESSION_ID', 'whatsapp-bot-main')
SESSION_PATH = os.path.join('session', SESSION_ID)

class WhatsAppBot:
    def __init__(self):
        self.client = None
        self.session_id = SESSION_ID
        self.session_path = SESSION_PATH
        self.api_url = API_URL
        self.api_token = API_TOKEN
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        self.active_conversations = {}
        self.knowledge_base = {}
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Carga la base de conocimientos desde la API"""
        try:
            response = requests.get(f"{self.api_url}/questions/", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                # Procesar datos para búsqueda rápida
                self.knowledge_base = {
                    'questions': {qa['id']: qa for qa in data},
                    'keywords': {}
                }
                
                for qa in data:
                    if qa['keywords']:
                        keywords = [kw.strip().lower() for kw in qa['keywords'].split(',')]
                        for kw in keywords:
                            if kw not in self.knowledge_base['keywords']:
                                self.knowledge_base['keywords'][kw] = []
                            self.knowledge_base['keywords'][kw].append(qa['id'])
                
                logger.info(f"Loaded {len(data)} questions into knowledge base")
            else:
                logger.error(f"Failed to load knowledge base: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def find_best_answer(self, message_text):
        """Busca la mejor respuesta para un mensaje dado"""
        # Implementación simple - buscar coincidencias de palabras clave
        message_text = message_text.lower()
        
        # Buscar coincidencia exacta en preguntas
        for qa_id, qa in self.knowledge_base['questions'].items():
            if message_text in qa['question'].lower():
                return qa['answer']
        
        # Buscar palabras clave
        matched_qa_ids = []
        for word in message_text.split():
            if word in self.knowledge_base['keywords']:
                matched_qa_ids.extend(self.knowledge_base['keywords'][word])
        
        if matched_qa_ids:
            # Contar cuántas veces aparece cada ID (más coincidencias = mejor match)
            from collections import Counter
            count = Counter(matched_qa_ids)
            best_match_id = count.most_common(1)[0][0]
            return self.knowledge_base['questions'][best_match_id]['answer']
        
        # Respuesta por defecto si no hay coincidencias
        return "Lo siento, no tengo una respuesta para esa pregunta. ¿Puedo ayudarte con algo más?"
    
    def register_contact(self, phone):
        """Registra un nuevo contacto en la API"""
        try:
            # Verificar si ya existe
            response = requests.get(f"{self.api_url}/contacts/?phone={phone}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]['id']
            
            # Crear nuevo contacto
            contact_data = {
                'phone': phone,
                'name': phone  # Usamos el teléfono como nombre inicial
            }
            response = requests.post(f"{self.api_url}/contacts/", json=contact_data, headers=self.headers)
            if response.status_code == 201:
                return response.json()['id']
            else:
                logger.error(f"Failed to create contact: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error registering contact: {e}")
            return None
    
    def create_or_get_conversation(self, contact_id):
        """Crea o recupera una conversación activa"""
        try:
            # Buscar conversación activa
            response = requests.get(
                f"{self.api_url}/conversations/?contact={contact_id}&is_active=true", 
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]['id']
            
            # Crear nueva conversación
            conversation_data = {
                'contact': contact_id,
                'is_active': True,
                'bot_mode': True
            }
            response = requests.post(
                f"{self.api_url}/conversations/", 
                json=conversation_data, 
                headers=self.headers
            )
            
            if response.status_code == 201:
                return response.json()['id']
            else:
                logger.error(f"Failed to create conversation: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            return None
    
    def save_message(self, conversation_id, content, msg_type='incoming', from_bot=False):
        """Guarda un mensaje en la API"""
        try:
            message_data = {
                'conversation': conversation_id,
                'content': content,
                'type': msg_type,
                'is_from_bot': from_bot
            }
            response = requests.post(
                f"{self.api_url}/conversations/{conversation_id}/send_message/", 
                json=message_data, 
                headers=self.headers
            )
            
            if response.status_code != 200 and response.status_code != 201:
                logger.error(f"Failed to save message: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error saving message: {e}")
    
    def on_message(self, message):
        """Manejador de mensajes entrantes"""
        try:
            # Solo procesamos mensajes de texto por ahora
            if message.get('type') != 'chat':
                return
            
            # Extraer información del mensaje
            content = message.get('content', '')
            from_number = message.get('from', '').split('@')[0]
            
            logger.info(f"Message received from {from_number}: {content}")
            
            # Registrar contacto y crear/obtener conversación
            contact_id = self.register_contact(from_number)
            if not contact_id:
                logger.error(f"Could not register contact for {from_number}")
                return
            
            conversation_id = self.create_or_get_conversation(contact_id)
            if not conversation_id:
                logger.error(f"Could not create conversation for {from_number}")
                return
            
            # Guardar mensaje recibido
            self.save_message(conversation_id, content, 'incoming', False)
            
            # Verificar si la conversación está en modo bot
            response = requests.get(
                f"{self.api_url}/conversations/{conversation_id}/", 
                headers=self.headers
            )
            
            if response.status_code == 200:
                conversation = response.json()
                if not conversation.get('bot_mode', True):
                    # Conversación asignada a un agente, no respondemos automáticamente
                    logger.info(f"Conversation {conversation_id} is handled by an agent")
                    return
            
            # Buscar respuesta en la base de conocimientos
            answer = self.find_best_answer(content)
            
            # Enviar respuesta
            self.client.send_message(message['from'], answer)
            
            # Guardar respuesta
            self.save_message(conversation_id, answer, 'outgoing', True)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def update_session_info(self, session, is_active, qr_code=None):
        """Actualiza la información de la sesión en la API"""
        data = {'is_active': is_active}
        
        if qr_code:
            data['last_qr_code'] = qr_code
            data['qr_generated_at'] = datetime.now().isoformat()
        elif is_active:
            data['connected_at'] = datetime.now().isoformat()
        else:
            data['disconnected_at'] = datetime.now().iso
import os
import json
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class BotDatabase:
    """
    Clase para manejar las interacciones con la base de datos a través de la API
    """
    
    def __init__(self, api_url, api_token):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            api_url (str): URL base de la API
            api_token (str): Token de autenticación para la API
        """
        self.api_url = api_url
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self):
        """
        Prueba la conexión con la API
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            response = requests.get(f"{self.api_url}/ping/", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error de conexión con la API: {str(e)}")
            return False
    
    def get_knowledge_base(self):
        """
        Obtiene la base de conocimientos desde la API
        
        Returns:
            dict: Base de conocimientos estructurada para búsqueda rápida
        """
        try:
            response = requests.get(f"{self.api_url}/questions/", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                
                # Estructurar datos para búsqueda eficiente
                knowledge_base = {
                    'questions': {str(qa['id']): qa for qa in data},
                    'keywords': {}
                }
                
                # Organizar por palabras clave
                for qa in data:
                    if qa.get('keywords'):
                        keywords = [kw.strip().lower() for kw in qa['keywords'].split(',')]
                        for kw in keywords:
                            if kw not in knowledge_base['keywords']:
                                knowledge_base['keywords'][kw] = []
                            knowledge_base['keywords'][kw].append(str(qa['id']))
                
                logger.info(f"Cargadas {len(data)} preguntas en la base de conocimientos")
                return knowledge_base
            else:
                logger.error(f"Error al obtener base de conocimientos: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error al cargar la base de conocimientos: {str(e)}")
            return {}
    
    def register_contact(self, phone, name=None):
        """
        Registra un nuevo contacto o actualiza uno existente
        
        Args:
            phone (str): Número de teléfono del contacto
            name (str, optional): Nombre del contacto, si está disponible
            
        Returns:
            int: ID del contacto, o None si hubo un error
        """
        try:
            # Verificar si ya existe
            response = requests.get(f"{self.api_url}/contacts/?phone={phone}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    contact_id = data[0]['id']
                    # Actualizar nombre si se proporcionó
                    if name and data[0]['name'] != name and data[0]['name'] == phone:
                        update_data = {'name': name}
                        requests.patch(
                            f"{self.api_url}/contacts/{contact_id}/", 
                            json=update_data, 
                            headers=self.headers
                        )
                    return contact_id
            
            # Crear nuevo contacto
            contact_data = {
                'phone': phone,
                'name': name or phone
            }
            response = requests.post(f"{self.api_url}/contacts/", json=contact_data, headers=self.headers)
            if response.status_code == 201:
                return response.json()['id']
            else:
                logger.error(f"Error al crear contacto: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error al registrar contacto: {str(e)}")
            return None
    
    def get_or_create_conversation(self, contact_id):
        """
        Obtiene una conversación activa o crea una nueva
        
        Args:
            contact_id (int): ID del contacto
            
        Returns:
            int: ID de la conversación, o None si hubo un error
        """
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
                logger.error(f"Error al crear conversación: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error al obtener/crear conversación: {str(e)}")
            return None
    
    def save_message(self, conversation_id, content, msg_type='incoming', from_bot=False):
        """
        Guarda un mensaje en la base de datos
        
        Args:
            conversation_id (int): ID de la conversación
            content (str): Contenido del mensaje
            msg_type (str): Tipo de mensaje ('incoming' o 'outgoing')
            from_bot (bool): Si el mensaje es del bot o no
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            message_data = {
                'conversation': conversation_id,
                'content': content,
                'type': msg_type,
                'is_from_bot': from_bot
            }
            response = requests.post(
                f"{self.api_url}/messages/", 
                json=message_data, 
                headers=self.headers
            )
            
            if response.status_code in (200, 201):
                return True
            else:
                logger.error(f"Error al guardar mensaje: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error al guardar mensaje: {str(e)}")
            return False
    
    def update_session_status(self, session_id, is_active, qr_code=None):
        """
        Actualiza el estado de una sesión de WhatsApp
        
        Args:
            session_id (str): ID de la sesión
            is_active (bool): Si la sesión está activa o no
            qr_code (str, optional): Código QR si está disponible
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            # Verificar si la sesión existe
            response = requests.get(
                f"{self.api_url}/whatsapp-sessions/?session_id={session_id}", 
                headers=self.headers
            )
            
            data = {
                'is_active': is_active
            }
            
            if qr_code:
                data['last_qr_code'] = qr_code
                data['qr_generated_at'] = datetime.now().isoformat()
            elif is_active:
                data['connected_at'] = datetime.now().isoformat()
            else:
                data['disconnected_at'] = datetime.now().isoformat()
            
            session_exists = response.status_code == 200 and response.json()
            
            if session_exists:
                session_db_id = response.json()[0]['id']
                response = requests.patch(
                    f"{self.api_url}/whatsapp-sessions/{session_db_id}/", 
                    json=data, 
                    headers=self.headers
                )
            else:
                # Crear nueva sesión
                data.update({
                    'name': f"Sesión {session_id}",
                    'session_id': session_id
                })
                response = requests.post(
                    f"{self.api_url}/whatsapp-sessions/", 
                    json=data, 
                    headers=self.headers
                )
            
            return response.status_code in (200, 201)
        except Exception as e:
            logger.error(f"Error al actualizar estado de sesión: {str(e)}")
            return False
    
    def get_conversation_status(self, conversation_id):
        """
        Obtiene el estado de una conversación
        
        Args:
            conversation_id (int): ID de la conversación
            
        Returns:
            dict: Estado de la conversación, o None si hubo un error
        """
        try:
            response = requests.get(
                f"{self.api_url}/conversations/{conversation_id}/", 
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error al obtener estado de conversación: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error al obtener estado de conversación: {str(e)}")
            return None
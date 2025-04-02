"""
Aplicación principal del bot de WhatsApp.
Este archivo sirve como punto de entrada para el servicio del bot.
"""
import os
import sys
import time
import json
import requests
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from wppconnect import Wppconnect
from threading import Thread

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('whatsapp_bot')

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000/api')
API_TOKEN = os.getenv('API_TOKEN', '')

# Inicializar Flask para endpoints de administración del bot
app = Flask(__name__)

# Variable global para mantener la instancia de WPPConnect
wpp_instance = None
is_connected = False

def create_session(session_id="default_session"):
    """Crear y devolver una nueva instancia de WPPConnect"""
    global wpp_instance, is_connected
    
    # Crear directorio de sesión si no existe
    session_dir = os.path.join(os.path.dirname(__file__), 'session')
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    # Crear instancia de WPPConnect
    wpp_instance = Wppconnect(session=session_id, session_path=session_dir)
    
    try:
        # Conectar a WhatsApp
        logger.info(f"Iniciando sesión: {session_id}")
        wpp_instance.connect()
        
        # Configurar manejador de mensajes
        @wpp_instance.on_message
        def handle_message(message):
            if not message.get('fromMe', False):  # Ignorar mensajes propios
                process_incoming_message(message)
        
        # Verificar si la conexión fue exitosa
        max_attempts = 30
        for _ in range(max_attempts):
            if wpp_instance.is_logged():
                is_connected = True
                logger.info("Conexión exitosa a WhatsApp")
                break
            time.sleep(1)
        
        if not is_connected:
            logger.error("No se pudo conectar a WhatsApp")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error al crear sesión: {e}")
        return False

def process_incoming_message(message):
    """Procesar mensajes entrantes y enviar a la API backend"""
    try:
        # Ignorar mensajes de grupos por ahora
        if message.get('isGroupMsg', False):
            return
        
        phone = message.get('from', '').split('@')[0]  # Extraer número de teléfono
        content = message.get('body', '')
        message_id = message.get('id', '')
        
        logger.info(f"Mensaje recibido de {phone}: {content[:50]}...")
        
        # Enviar el mensaje al backend para procesamiento
        payload = {
            'phone': phone,
            'content': content,
            'message_id': message_id,
            'type': 'incoming'
        }
        
        headers = {
            'Authorization': f'Token {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{API_URL}/messages/", 
            json=payload,
            headers=headers
        )
        
        if response.status_code != 201:
            logger.error(f"Error al enviar mensaje a backend: {response.status_code}")
            logger.error(response.text)
        
    except Exception as e:
        logger.error(f"Error al procesar mensaje: {e}")

def send_message(phone, content):
    """Enviar mensaje a un número de teléfono"""
    global wpp_instance, is_connected
    
    if not is_connected or not wpp_instance:
        logger.error("No hay conexión activa a WhatsApp")
        return False
    
    try:
        # Añadir sufijo @c.us si no está presente
        if '@' not in phone:
            phone = f"{phone}@c.us"
        
        # Enviar mensaje
        result = wpp_instance.send_message(phone, content)
        logger.info(f"Mensaje enviado a {phone}: {content[:50]}...")
        return result
        
    except Exception as e:
        logger.error(f"Error al enviar mensaje: {e}")
        return False

# Endpoints de la API Flask para administración
@app.route('/status', methods=['GET'])
def status():
    """Verificar el estado de la conexión"""
    global is_connected
    return jsonify({
        'status': 'connected' if is_connected else 'disconnected',
    })

@app.route('/send', methods=['POST'])
def api_send_message():
    """Endpoint para enviar mensajes"""
    data = request.json
    phone = data.get('phone')
    content = data.get('content')
    
    if not phone or not content:
        return jsonify({'error': 'Se requieren phone y content'}), 400
    
    result = send_message(phone, content)
    
    if result:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No se pudo enviar el mensaje'}), 500

@app.route('/reconnect', methods=['POST'])
def reconnect():
    """Reiniciar la conexión con WhatsApp"""
    global wpp_instance, is_connected
    
    # Cerrar conexión existente si la hay
    if wpp_instance:
        try:
            wpp_instance.close()
        except:
            pass
        wpp_instance = None
        is_connected = False
    
    # Crear nueva sesión
    success = create_session()
    
    if success:
        return jsonify({'status': 'success', 'message': 'Reconectado correctamente'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No se pudo reconectar'}), 500

def main():
    """Función principal para iniciar el bot"""
    # Iniciar conexión con WhatsApp
    success = create_session()
    
    if not success:
        logger.error("No se pudo iniciar el bot. Saliendo.")
        sys.exit(1)
    
    # Iniciar servidor Flask en un hilo separado
    host = '0.0.0.0'
    port = 5000
    logger.info(f"Iniciando servidor en {host}:{port}")
    
    from waitress import serve
    serve(app, host=host, port=port)

if __name__ == "__main__":
    main()
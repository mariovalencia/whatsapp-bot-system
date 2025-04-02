"""
Script para probar el envío y recepción de mensajes usando WPPConnect.
Este script enviará un mensaje de prueba al número especificado y
configurará un listener básico para recibir mensajes.
"""
import os
import time
from dotenv import load_dotenv
from wppconnect import Wppconnect

# Cargar variables de entorno
load_dotenv()

# Configuración
TEST_PHONE_NUMBER = os.getenv('TEST_PHONE_NUMBER', '')  # Formato: 1234567890 (sin prefijo + ni código de país)
TEST_MESSAGE = "Hola, este es un mensaje de prueba del bot WhatsApp."

def test_messages():
    """Prueba básica de envío y recepción de mensajes"""
    print("Iniciando prueba de mensajes con WhatsApp...")
    
    # Crear directorio de sesión si no existe
    session_dir = os.path.join(os.path.dirname(__file__), 'session')
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    # Inicializar WPPConnect
    wp = Wppconnect(session="test_session", session_path=session_dir)
    
    try:
        # Conectar (utilizará la sesión existente si está disponible)
        print("Conectando a WhatsApp...")
        wp.connect()
        
        # Verificar si estamos conectados
        if not wp.is_logged():
            print("No está conectado. Por favor, ejecute primero wpp_connect_test.py para escanear el QR.")
            return False
        
        # Configurar manejador de mensajes entrantes
        @wp.on_message
        def on_message(message):
            print(f"Mensaje recibido de {message['from']}:")
            print(f"  Contenido: {message['body']}")
            
            # Responder automáticamente si no es un mensaje de grupo
            if not message['isGroupMsg']:
                wp.send_message(
                    message['from'], 
                    f"Recibí tu mensaje: {message['body']}\nEsto es una respuesta automática."
                )
        
        # Enviar mensaje de prueba si se proporciona un número
        if TEST_PHONE_NUMBER:
            full_number = f"{TEST_PHONE_NUMBER}@c.us"  # Formato requerido por WPPConnect
            print(f"Enviando mensaje de prueba a {TEST_PHONE_NUMBER}...")
            wp.send_message(full_number, TEST_MESSAGE)
            print("Mensaje enviado. Esperando respuestas...")
        else:
            print("No se especificó número de prueba. Configurado solo para recibir mensajes.")
        
        # Mantener el script en ejecución para recibir mensajes
        print("Escuchando mensajes entrantes. Presione Ctrl+C para salir.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDetención solicitada por el usuario.")
    except Exception as e:
        print(f"Error en la prueba de mensajes: {e}")
    finally:
        # Cerrar conexión
        print("Cerrando conexión...")
        wp.close()
        return True

if __name__ == "__main__":
    test_messages()
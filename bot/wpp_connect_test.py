"""
Script de prueba para verificar la conexión con WhatsApp usando WPPConnect.
Este script genera un código QR para escanear con WhatsApp y establece una conexión.
"""
import os
import time
from dotenv import load_dotenv
from wppconnect import Wppconnect

# Cargar variables de entorno
load_dotenv()

def test_connection():
    """Prueba básica de conexión a WhatsApp"""
    print("Iniciando prueba de conexión con WhatsApp...")
    
    # Crear directorio de sesión si no existe
    session_dir = os.path.join(os.path.dirname(__file__), 'session')
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    # Inicializar WPPConnect
    wp = Wppconnect(session="test_session", session_path=session_dir)
    
    try:
        print("Generando código QR. Escanee con WhatsApp del teléfono...")
        wp.connect()  # Esto genera el código QR
        
        # Esperar a que se escanee el QR y se conecte
        print("Esperando conexión... (60 segundos máximo)")
        for _ in range(60):
            if wp.is_logged():
                print("¡Conexión exitosa!")
                break
            time.sleep(1)
        else:
            print("Tiempo de espera agotado. No se pudo conectar.")
            return False
        
        # Obtener información de conexión
        info = wp.get_connection_info()
        print(f"Conectado como: {info['name']} ({info['phone']})")
        
        # Cerrar sesión
        wp.close()
        print("Sesión cerrada correctamente")
        return True
        
    except Exception as e:
        print(f"Error al conectar: {e}")
        return False

if __name__ == "__main__":
    test_connection()
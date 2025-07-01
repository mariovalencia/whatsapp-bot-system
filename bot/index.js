const venom = require('venom-bot');
const axios = require("axios");
const fs = require('fs');
const path = require('path');
const { setTimeout } = require('timers/promises');
const handleMessage = require('./handlers/messageHandlers');

async function cleanSession() {
  const sessionPath = path.join(__dirname, 'tokens');
  
  if (!fs.existsSync(sessionPath)) return;

  console.log('Intentando eliminar sesión anterior...');
  
  let retries = 5;
  while (retries > 0) {
    try {
      fs.rmSync(sessionPath, { recursive: true, force: true });
      console.log('Sesión anterior eliminada con éxito');
      return;
    } catch (err) {
      if (err.code === 'EBUSY') {
        console.log(`Recurso ocupado, reintentando... (${retries} intentos restantes)`);
        retries--;
        await setTimeout(1000);
      } else {
        console.error('Error al eliminar sesión:', err);
        return;
      }
    }
  }
  console.error('No se pudo eliminar la sesión después de varios intentos');
}

let userSessions = {};
let clientInstance = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

async function initializeClient() {
  try {
    await cleanSession();
    
    clientInstance = await venom.create({
      session: 'bot-session',
      multidevice: true,
      headless: true,
      logQR: true, // Muestra el QR en la consola
      // Opciones adicionales para mejor manejo de conexión
      browserWS: '', // Fuerza nueva instancia del navegador
      puppeteerOptions: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        headless: true
      },
      disableWelcome: true
    });
    
    console.log('Bot iniciado correctamente');
    reconnectAttempts = 0; // Reinicia contador de reconexiones
    
    start(clientInstance);
    
    // Manejar cierre inesperado
    clientInstance.onStreamChange((state) => {
      console.log('Estado de conexión:', state);
      if (state === 'DISCONNECTED') {
        console.log('Conexión perdida, intentando reconectar...');
        setTimeout(() => initializeClient(), 5000);
      }
    });
    
  } catch (err) {
    console.error('Error al iniciar Venom:', err);
    
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      reconnectAttempts++;
      console.log(`Intentando reconectar (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`);
      await setTimeout(5000); // Espera 5 segundos antes de reintentar
      await initializeClient();
    } else {
      console.error('Número máximo de intentos de reconexión alcanzado');
      process.exit(1); // Sale del proceso si no puede reconectar
    }
  }
}

function start(client) {
  client.onMessage(async (message) => {
    const userId = message.from;
        
    if (!userSessions[userId]) {
      userSessions[userId] = { step: 1, data: {} };
      client.sendText(userId, "👋 Hola, bienvenido al sistema de atención al cliente, ¿Con quien tengo el gusto?");
      return;
    }
    
    const session = userSessions[userId];
      await handleMessage(message, client);
  });
}

// Iniciar el cliente
(async () => {
  await initializeClient();
})();
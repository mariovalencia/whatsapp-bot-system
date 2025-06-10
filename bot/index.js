require('dotenv').config();
const venom = require('venom-bot');
const axios = require('axios');
const fs = require("fs");
const path = require("path");

// Configuración de la sesión
const SESSION_FILE = path.join(__dirname, 'session.json');

// Verificar si existe sesión guardada
function hasSavedSession() {
  return fs.existsSync(SESSION_FILE);
}

// Configuración de Venom
/*const venomConfig = {
  session: 'customer-service-bot',
  multidevice: true,
  headless: false,
  folderNameToken: 'tokens', // Carpeta para almacenar tokens
  disableWelcome: true,
  logQR: true, // Muestra QR en consola
  catchQR: (base64Qr, asciiQR) => {
    console.log(asciiQR); // Opcional: guarda esto para mostrarlo en tu frontend
    fs.writeFileSync('/app/qr.txt', asciiQR); // Guarda QR en archivo temporal
  },
  statusFind: (statusSession, session) => {
    console.log('Estado de la sesión:', statusSession);
    if (statusSession === 'isLogged') {
      fs.writeFileSync(SESSION_FILE, JSON.stringify({ connected: true }));
    }
  }
};*/

console.log('Iniciando WhatsApp Bot...');

// Configuración de la API Django (ajusta la URL según tu entorno)
const DJANGO_API = process.env.DJANGO_API_URL;

console.log('Conectando a API Django en:', DJANGO_API); // Para debug

venom
  .create({
    session: 'customer-service-bot',
    multidevice: true,
    headless: false,
    puppeteerOptions: {
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--single-process'  // Añade esta línea
  ]},
    folderNameToken: 'tokens', // Carpeta para almacenar tokens
    disableWelcome: false,
    logQR: true, // Muestra QR en consola
    catchQR: (base64Qr, asciiQR) => {
      console.log('Escanea este QR con tu WhatsApp:');
      console.log(asciiQR); // Opcional: guarda esto para mostrarlo en tu frontend
      fs.writeFileSync('/app/qr.txt', asciiQR); // Guarda QR en archivo temporal
    },
    statusFind: (statusSession, session) => {
      console.log('Estado de la sesión:', statusSession);
      if (statusSession === 'isLogged') {
        fs.writeFileSync(SESSION_FILE, JSON.stringify({ connected: true }));
      }
    },
    puppeteerOptions: {
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage'
    ]
  }
  })
  .then((client) => {
    console.log('Bot iniciado correctamente');
    start(client);
  })
  .catch((err) => {
    console.error('Error al iniciar el bot:', err);
  });

function start(client) {
  client.onMessage(async (message) => {
    if (message.isGroupMsg === false) {
      console.log('Mensaje recibido:', message.body);
      // 1. Obtener respuesta del backend
      const botResponse = await getBotResponse(message.body);
      
      // 2. Enviar respuesta al usuario
      client.sendText(message.from, botResponse)
        .then(() => console.log('Respuesta enviada:', botResponse))
        .catch(err => console.error('Error al enviar:', err));
    }
  });
}

const userContexts = {};

async function getBotResponse(messageText, userId) {
  try {
    const context = userContexts[userId] || {};
    const response = await axios.post(`${DJANGO_API}/ask/`, {
      message: messageText,
      context: context
    });
    userContexts[userId] = response.data.context;
    return response.data.response;
  } catch (error) {
    console.error('Error al llamar a la API:', error);
    return 'Ocurrió un error al procesar tu mensaje';
  }
}
require('dotenv').config();
const venom = require('venom-bot');

console.log('Iniciando WhatsApp Bot...');

venom
  .create({
    session: 'customer-service-bot',
    multidevice: true
  })
  .then((client) => {
    console.log('Bot iniciado correctamente');
    start(client);
  })
  .catch((err) => {
    console.error('Error al iniciar el bot:', err);
  });

function start(client) {
  client.onMessage((message) => {
    if (message.isGroupMsg === false) {
      console.log('Mensaje recibido:', message.body);
      // Aquí procesaremos los mensajes en el Sprint 4
    }
  });
}
const venom = require('venom-bot');
const axios = require("axios");

venom
  .create({
    session: 'bot-session',
    multidevice: true,
    headless: true,           // ✅ Necesario para consola
    //useChrome: false,         // ✅ Muy importante para modo headless + consola
    //browserArgs: ['--no-sandbox', '--disable-setuid-sandbox'],
    //disableWelcome: true,
  })
  .then((client) => start(client))
  .catch((err) => {
    console.error('Error al iniciar Venom:', err);
  });

function start(client) {
  console.log('Bot iniciado correctamente');
}

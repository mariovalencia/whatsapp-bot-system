const fs = require('fs');
const path = require('path');
const { askBot } = require('../services/apiClient');

const userDataPath = path.join(__dirname, '../sessions/user_data.json');

function loadUserData() {
  if (!fs.existsSync(userDataPath)) return {};
  return JSON.parse(fs.readFileSync(userDataPath, 'utf-8'));
}

function saveUserData(data) {
  fs.writeFileSync(userDataPath, JSON.stringify(data, null, 2));
}

function extractName(text) {
  const lower = text.toLowerCase().trim();
  const patterns = [
    /me llamo ([a-záéíóúñ\s]+)/i,
    /mi nombre es ([a-záéíóúñ\s]+)/i,
    /soy ([a-záéíóúñ\s]+)/i,
    /me dicen ([a-záéíóúñ\s]+)/i,
    /puedes llamarme ([a-záéíóúñ\s]+)/i,
    /con ([a-záéíóúñ\s]+)/i
  ];
  for (const pattern of patterns) {
    const match = lower.match(pattern);
    if (match) return match[1].trim();
  }
  // Lista de palabras comunes que no son nombres
  const palabrasComunes = ['hola', 'gracias', 'sí', 'no', 'ok', 'buenos', 'días', 'tarde', 'noche'];

  // Si es una sola palabra y no es común, asumir que es un nombre
  if (/^[a-záéíóúñ]{3,20}$/i.test(lower) && !palabrasComunes.includes(lower)) {
    return lower.charAt(0).toUpperCase() + lower.slice(1);
  }
  return null;
}

module.exports = async (message, client) => {
  try {
    const userId = message.from;
    const text = message.body;
    const userData = loadUserData();

    const nombreDetectado = extractName(text);
    if (nombreDetectado) {
      userData[userId] = { ...userData[userId], nombre: nombreDetectado };
      saveUserData(userData);
      await client.sendText(userId, `¡Encantado, ${nombreDetectado}! He guardado tu nombre.`);
      return;
    }

    const context = {
      cliente_id: userId,
      nombre: userData[userId]?.nombre || "Estimado(a)"
    };

    const response = await askBot(text, context);
    const reply = response.data.response || "No entendí. ¿Puedes reformular?";
    await client.sendText(userId, reply);
  } catch (error) {
    console.error("❌ Error al comunicar con el backend:", error.message);
    await client.sendText(message.from, "Hubo un error procesando tu mensaje. Intenta más tarde.");
  }
};

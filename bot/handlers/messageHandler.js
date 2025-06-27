const { classifyIntent } = require('../services/apiClient');

module.exports = async (message, client) => {
  try {
    // Simulación de contexto (puedes enriquecerlo más adelante)
    const context = {
      cliente_id: message.from,
      nombre: "Estimado(a)" // Esto puede venir de una base de datos o lógica previa
    };

    const response = await classifyIntent(message.body, context);
    const intent = response.data.intent;

    let reply = "";
    switch (intent) {
      case "saludo":
        reply = `¡Hola ${context.nombre}! ¿Cómo puedo ayudarte?`;
        break;
      case "soporte":
        reply = "Por favor, describe tu problema.";
        break;
      default:
        reply = "No entendí. ¿Puedes reformular?";
    }

    await client.sendText(message.from, reply);
  } catch (error) {
    console.error("Error al clasificar mensaje:", error);
  }
};

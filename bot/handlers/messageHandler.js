const { classifyIntent } = require('../services/apiClient');

module.exports = async (message, client) => {
    try {
        const response = await classifyIntent(message.body);
        const intent = response.data.intent;
        
        let reply = "";
        switch (intent) {
            case "saludo":
                reply = "¡Hola! ¿Cómo puedo ayudarte?";
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
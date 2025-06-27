import React, { useState } from 'react';
import axios from '../services/api';

const CreateIntent = () => {
    const [formData, setFormData] = useState({ text: "", intent: "" });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/api/bot/intents/', formData);
            alert("Intención guardada!");
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Texto (ej: 'hola')"
                value={formData.text}
                onChange={(e) => setFormData({ ...formData, text: e.target.value })}
            />
            <input
                type="text"
                placeholder="Intención (ej: 'saludo')"
                value={formData.intent}
                onChange={(e) => setFormData({ ...formData, intent: e.target.value })}
            />
            <button type="submit">Guardar</button>
        </form>
    );
};
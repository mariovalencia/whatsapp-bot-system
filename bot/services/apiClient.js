const axios = require('axios');

const API_URL = process.env.BACKEND_URL || "http://localhost:8000";

exports.classifyIntent = (text) => {
    return axios.post(`${API_URL}/api/classify-intent/`, { text });
};
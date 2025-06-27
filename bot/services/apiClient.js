const axios = require('axios');
const API_URL = process.env.BACKEND_URL || "http://localhost:8000";

exports.classifyIntent = (text, context = {}) => {
  return axios.post(`${API_URL}/api/ask/`, {
    message: text,
    context: context
  });
};

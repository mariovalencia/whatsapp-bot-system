import axios from 'axios';

// Crear instancia de axios
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
});

// Interceptor para agregar token a las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para refrescar token cuando expire
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Si es un error 401 (no autorizado) y no es un retry
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Intentar refrescar el token
        const refreshToken = localStorage.getItem('refreshToken');
        
        if (!refreshToken) {
          // No hay token de refresco, redireccionar a login
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(error);
        }
        
        const response = await axios.post(
          `${process.env.REACT_APP_API_URL}/auth/refresh/`,
          { refresh: refreshToken }
        );
        
        if (response.data.access) {
          // Guardar nuevo token
          localStorage.setItem('token', response.data.access);
          
          // Volver a intentar la petición original
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return axios(originalRequest);
        }
      } catch (refreshError) {
        // Error al refrescar token, redireccionar a login
        localStorage.clear();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Funciones de API
const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  getCurrentUser: () => api.get('/users/me/'),
};

const usersAPI = {
  getAll: () => api.get('/users/'),
  getById: (id) => api.get(`/users/${id}/`),
  create: (userData) => api.post('/users/', userData),
  update: (id, userData) => api.put(`/users/${id}/`, userData),
  delete: (id) => api.delete(`/users/${id}/`),
};

const rolesAPI = {
  getAll: () => api.get('/roles/'),
  getById: (id) => api.get(`/roles/${id}/`),
  create: (roleData) => api.post('/roles/', roleData),
  update: (id, roleData) => api.put(`/roles/${id}/`, roleData),
  delete: (id) => api.delete(`/roles/${id}/`),
};

const botAPI = {
  getCategories: () => api.get('/categories/'),
  getQuestions: () => api.get('/questions/'),
  getQuestionById: (id) => api.get(`/questions/${id}/`),
  createQuestion: (questionData) => api.post('/questions/', questionData),
  updateQuestion: (id, questionData) => api.put(`/questions/${id}/`, questionData),
  deleteQuestion: (id) => api.delete(`/questions/${id}/`),
  getActiveQuestions: () => api.get('/questions/active/'),
};

const whatsappAPI = {
  getSessions: () => api.get('/whatsapp-sessions/'),
  getCurrentQR: (sessionId) => api.get(`/whatsapp-sessions/${sessionId}/qr/`),
  getContacts: () => api.get('/contacts/'),
  getConversations: () => api.get('/conversations/'),
  getConversationById: (id) => api.get(`/conversations/${id}/`),
  sendMessage: (data) => api.post('/whatsapp-sessions/send-message/', data),
  logout: (sessionId) => api.post(`/whatsapp-sessions/${sessionId}/logout/`),
  reconnect: (sessionId) => api.post(`/whatsapp-sessions/${sessionId}/reconnect/`),
  transferToBot: (conversationId) => api.post(`/conversations/${conversationId}/transfer-to-bot/`),
  transferToHuman: (conversationId, userId) => api.post(`/conversations/${conversationId}/transfer-to-human/`, { user_id: userId }),
};

export {
  api,
  authAPI,
  usersAPI,
  rolesAPI,
  botAPI,
  whatsappAPI,
};
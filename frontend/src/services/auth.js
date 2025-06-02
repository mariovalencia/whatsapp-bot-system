import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true
})

export const login = async ({ username, password }) => {
  try {
    console.log('Enviando credenciales:', { username, password }); // ← Verifica esto
    const response = await API.post('/auth/login/', {
      username: username,  // Asegúrate que coincida con lo que espera el backend
      password: password
    });
    return response;
  } catch (error) {
    console.error('Detalles del error:', {
      status: error.response?.status,
      data: error.response?.data,  // ← Esto contiene el mensaje específico del backend
      config: error.config  // ← Verifica qué se envió realmente
    });
    throw error;
  }
};
export const googleLogin = (token) => API.post('/auth/google/', { token })
import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL
})

export const login = (credentials) => API.post('/auth/login/', credentials)
export const googleLogin = (token) => API.post('/auth/google/', { token })
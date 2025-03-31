import React, { createContext, useState, useEffect, useContext } from 'react';
import { authAPI } from '../services/api';

// Crear contexto
const AuthContext = createContext(null);

// Proveedor del contexto
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Cargar usuario al inicio
  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setLoading(false);
          return;
        }

        const response = await authAPI.getCurrentUser();
        setCurrentUser(response.data);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error al obtener el usuario actual:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
      } finally {
        setLoading(false);
      }
    };

    fetchCurrentUser();
  }, []);

  // Función de login
  const login = async (credentials) => {
    try {
      setError(null);
      const response = await authAPI.login(credentials);
      
      // Guardar tokens
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      
      // Guardar datos del usuario
      setCurrentUser(response.data.user);
      setIsAuthenticated(true);
      
      return response.data.user;
    } catch (error) {
      setError(error.response?.data?.detail || 'Error al iniciar sesión');
      throw error;
    }
  };

  // Función de registro
  const register = async (userData) => {
    try {
      setError(null);
      const response = await authAPI.register(userData);
      return response.data;
    } catch (error) {
      setError(error.response?.data?.detail || 'Error al registrar usuario');
      throw error;
    }
  };

  // Función de logout
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setCurrentUser(null);
    setIsAuthenticated(false);
    window.location.href = '/login';
  };

  // Verificar si el usuario está autenticado
  const checkAuth = () => {
    return !!localStorage.getItem('token');
  };

  // Verificar si el usuario tiene el rol requerido
  const hasRole = (requiredRole) => {
    if (!currentUser || !currentUser.roles) return false;
    return currentUser.roles.includes(requiredRole);
  };

  // Valores del contexto
  const value = {
    currentUser,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    checkAuth,
    hasRole
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Hook personalizado para usar el contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export default AuthContext;
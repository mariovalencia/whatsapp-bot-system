import React, { useState } from 'react'
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google'
import { login, googleLogin } from '../services/auth'
import { useNavigate } from 'react-router-dom'
import axios from 'axios';
import { useForm } from 'react-hook-form';
import { MessageSquare } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors } } = useForm();

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      console.log(credentialResponse);

      const { data } = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/auth/google/`,
      { access_token: credentialResponse.credential },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      }
    );
      localStorage.setItem('token', data.access)
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Google login failed:', error.response?.data || error.message);
      alert('Error al iniciar sesión con Google');
    }
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    try {
      const { data } = await login({ 
        username: email,
        password: password 
      });
      localStorage.setItem('token', data.access)
      window.location.href = '/dashboard'; 
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 
                       error.response?.data?.non_field_errors?.[0] || 
                       'Error al iniciar sesión';
      console.error('Error completo:', {
        message: errorMessage,
        response: error.response?.data
      });
      alert(errorMessage);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-700 to-primary-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl overflow-hidden">
        <div className="p-6 sm:p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-100 text-primary-600 mb-4">
              <MessageSquare size={28} />
            </div>
            <h2 className="text-3xl font-bold text-center">Servicio de atencion al cliente con Whatsapp</h2>
            <p className="text-gray-600 mt-2">Inicia sesion en tu cuenta</p>
          </div>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Correo electrónico
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                 {...register('username', { required: 'Username is required' })}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                  errors.username ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {errors.username && (
                  <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contraseña
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  {...register('password', { required: 'Password is required' })}
                    className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${errors.password ? 'border-red-500' : 'border-gray-300'}`
                  }
                />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
              </div>

              <button
                type="submit"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Iniciar sesión
              </button>
            </form>
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center">
                <span className="px-2 bg-white text-gray-500">o</span>
              </div>
            </div>
            <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
              <div className="flex justify-center">
                <GoogleLogin
                  onSuccess={handleGoogleSuccess}
                  onError={() => console.log('Google login failed')}
                  size="large"
                />
              </div>
            </GoogleOAuthProvider> 
        </div>  
      </div>
    </div>
  )
}

export default Login
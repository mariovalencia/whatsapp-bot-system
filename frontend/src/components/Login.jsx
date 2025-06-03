import { useState } from 'react'
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google'
import { login, googleLogin } from '../services/auth'
import { useNavigate } from 'react-router-dom'
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

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

  const handleSubmit = async (e) => {
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
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
        <h2 className="text-3xl font-bold text-center">Iniciar sesión</h2>
        
        <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
          <div className="flex justify-center">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => console.log('Google login failed')}
              size="large"
            />
          </div>
        </GoogleOAuthProvider>

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center">
            <span className="px-2 bg-white text-gray-500">o</span>
          </div>
        </div>

        <form className="space-y-6" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Correo electrónico
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Iniciar sesión
          </button>
        </form>
      </div>
    </div>
  )
}

export default Login
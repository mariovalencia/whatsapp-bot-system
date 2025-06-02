import { Navigate } from 'react-router-dom';

const RoleProtectedRoute = ({ roles, children }) => {
  const storedRoles = JSON.parse(localStorage.getItem('user_roles') || []);
  const hasRole = roles.some(role => storedRoles.includes(role));
  
  return hasRole ? children : <Navigate to="/forbidden" />;
};

// Uso:
<RoleProtectedRoute roles={['support', 'admin']}>
  <WhatsAppDashboard />
</RoleProtectedRoute>
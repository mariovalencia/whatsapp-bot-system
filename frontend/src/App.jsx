import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './components/Login'
import Dashboard from './pages/Dashboard'
import LogsTable from './pages/LogsTable';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/logs" element={<LogsTable />} />
      </Routes>
    </Router>
  )
}

export default App

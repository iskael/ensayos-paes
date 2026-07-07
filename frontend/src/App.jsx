import { Routes, Route } from 'react-router-dom'
import RutaPrivada from './components/RutaPrivada.jsx'
import Login from './pages/Login.jsx'
import Registro from './pages/Registro.jsx'
import ConfigurarEnsayo from './pages/ConfigurarEnsayo.jsx'
import RendirEnsayo from './pages/RendirEnsayo.jsx'
import Resultado from './pages/Resultado.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Registro />} />
      <Route
        path="/"
        element={
          <RutaPrivada>
            <ConfigurarEnsayo />
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id"
        element={
          <RutaPrivada>
            <RendirEnsayo />
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id/resultado"
        element={
          <RutaPrivada>
            <Resultado />
          </RutaPrivada>
        }
      />
    </Routes>
  )
}

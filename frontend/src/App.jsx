import { Routes, Route } from 'react-router-dom'
import RutaPrivada from './components/RutaPrivada.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<div>Login (placeholder)</div>} />
      <Route path="/registro" element={<div>Registro (placeholder)</div>} />
      <Route
        path="/"
        element={
          <RutaPrivada>
            <div>Configurar ensayo (placeholder)</div>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id"
        element={
          <RutaPrivada>
            <div>Rendir ensayo (placeholder)</div>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id/resultado"
        element={
          <RutaPrivada>
            <div>Resultado (placeholder)</div>
          </RutaPrivada>
        }
      />
    </Routes>
  )
}

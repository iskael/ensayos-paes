import { Routes, Route } from 'react-router-dom'
import RutaPrivada from './components/RutaPrivada.jsx'
import LayoutAutenticado from './components/LayoutAutenticado.jsx'
import Login from './pages/Login.jsx'
import Registro from './pages/Registro.jsx'
import ConfigurarEnsayo from './pages/ConfigurarEnsayo.jsx'
import RendirEnsayo from './pages/RendirEnsayo.jsx'
import Resultado from './pages/Resultado.jsx'
import Dashboard from './pages/Dashboard.jsx'
import BancoExamenes from './pages/BancoExamenes.jsx'
import ExamenForm from './pages/ExamenForm.jsx'
import ItemForm from './pages/ItemForm.jsx'
import BancoItems from './pages/BancoItems.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Registro />} />
      <Route
        path="/"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ConfigurarEnsayo />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <RendirEnsayo />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id/resultado"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <Resultado />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/dashboard"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <Dashboard />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/examenes"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <BancoExamenes />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/examenes/nuevo"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ExamenForm />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/examenes/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ExamenForm />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/items"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <BancoItems />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/items/nuevo"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ItemForm />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/items/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ItemForm />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
    </Routes>
  )
}

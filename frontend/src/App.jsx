import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
import RutaPrivada from './components/RutaPrivada.jsx'
import LayoutAutenticado from './components/LayoutAutenticado.jsx'
import Login from './pages/Login.jsx'
import Registro from './pages/Registro.jsx'
import VerificarEmail from './pages/VerificarEmail.jsx'
import ConfigurarEnsayo from './pages/ConfigurarEnsayo.jsx'
import RendirEnsayo from './pages/RendirEnsayo.jsx'
import Resultado from './pages/Resultado.jsx'
import Dashboard from './pages/Dashboard.jsx'
import MiMeta from './pages/MiMeta.jsx'
import BancoExamenes from './pages/BancoExamenes.jsx'
import ExamenForm from './pages/ExamenForm.jsx'
import ItemForm from './pages/ItemForm.jsx'
import BancoItems from './pages/BancoItems.jsx'
import BancoEstimulos from './pages/BancoEstimulos.jsx'
import EstimuloForm from './pages/EstimuloForm.jsx'
import ExamenClave from './pages/ExamenClave.jsx'
import MisGruposProfesor from './pages/MisGruposProfesor.jsx'
import GrupoDetalle from './pages/GrupoDetalle.jsx'
import ProgresoEstudianteGrupo from './pages/ProgresoEstudianteGrupo.jsx'
import MisGruposEstudiante from './pages/MisGruposEstudiante.jsx'
import Pupilos from './pages/Pupilos.jsx'
import PupiloProgreso from './pages/PupiloProgreso.jsx'
import Institucion from './pages/Institucion.jsx'
import InstitucionGrupo from './pages/InstitucionGrupo.jsx'
import AdminUsuarios from './pages/AdminUsuarios.jsx'

function InicioPorRol() {
  const { usuario } = useAuth()
  if (usuario?.rol === 'admin' || usuario?.rol === 'editor') return <Navigate to="/banco/items" replace />
  if (usuario?.rol === 'apoderado') return <Navigate to="/pupilos" replace />
  if (usuario?.rol === 'institucion') return <Navigate to="/institucion" replace />
  if (usuario?.rol === 'profesor') return <Navigate to="/grupos" replace />
  return <ConfigurarEnsayo />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Registro />} />
      <Route path="/verificar-email" element={<VerificarEmail />} />
      <Route
        path="/"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <InicioPorRol />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado sinNavegacion>
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
        path="/meta"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <MiMeta />
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
        path="/banco/examenes/:id/clave"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ExamenClave />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/pupilos"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <Pupilos />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/pupilos/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <PupiloProgreso />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/institucion"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <Institucion />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/institucion/grupos/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <InstitucionGrupo />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/admin/usuarios"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <AdminUsuarios />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/textos"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <BancoEstimulos />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/textos/nuevo"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <EstimuloForm />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/banco/textos/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <EstimuloForm />
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
      <Route
        path="/grupos"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <MisGruposProfesor />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/grupos/:id"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <GrupoDetalle />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/grupos/:id/estudiantes/:estudianteId"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <ProgresoEstudianteGrupo />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
      <Route
        path="/mis-grupos"
        element={
          <RutaPrivada>
            <LayoutAutenticado>
              <MisGruposEstudiante />
            </LayoutAutenticado>
          </RutaPrivada>
        }
      />
    </Routes>
  )
}

import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import Dashboard from './Dashboard.jsx'

export default function PupiloProgreso() {
  const { id } = useParams()
  const { llamar } = useApi()
  const navigate = useNavigate()
  const [nombre, setNombre] = useState('')

  useEffect(() => {
    llamar((t) => api.listarPupilos(t))
      .then((lista) => setNombre(lista.find((p) => p.id === id)?.nombre ?? ''))
      .catch(() => {})
  }, [llamar, id])

  async function dejarDeSeguir() {
    if (!window.confirm(`¿Dejar de seguir a ${nombre || 'este estudiante'}?`)) return
    await llamar((t) => api.desvincularPupilo(t, id))
    navigate('/pupilos', { replace: true })
  }

  const volver = (
    <div className="fila-con-accion">
      <Link to="/pupilos" className="boton-enlace">
        ← Mis estudiantes
      </Link>
      <button type="button" className="boton-enlace" onClick={dejarDeSeguir}>
        Dejar de seguir
      </button>
    </div>
  )

  return <Dashboard estudianteId={id} titulo={nombre ? `Progreso de ${nombre}` : 'Progreso'} volver={volver} />
}

import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'

export default function InstitucionGrupo() {
  const { id } = useParams()
  const { llamar } = useApi()
  const [grupo, setGrupo] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    llamar((t) => api.grupoInstitucion(t, id))
      .then(setGrupo)
      .catch(() => setError('No se pudo cargar el grupo'))
  }, [llamar, id])

  if (!grupo) {
    return (
      <div className="pantalla">
        <div className="tarjeta">{error ?? 'Cargando…'}</div>
      </div>
    )
  }

  const conPuntaje = grupo.miembros.filter((m) => m.ultimo_puntaje != null)
  const promedio = conPuntaje.length ? Math.round(conPuntaje.reduce((s, m) => s + m.ultimo_puntaje, 0) / conPuntaje.length) : null

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <Link to="/institucion" className="boton-enlace">
          ← Institución
        </Link>
        <h1>{grupo.nombre}</h1>
        <p className="texto-suave">
          {grupo.miembros.length} {grupo.miembros.length === 1 ? 'estudiante' : 'estudiantes'}
          {promedio != null ? ` · promedio del último puntaje: ${promedio}` : ''}
        </p>
        {grupo.miembros.length === 0 ? (
          <p>El grupo aún no tiene estudiantes.</p>
        ) : (
          <ul className="lista-textos">
            {grupo.miembros.map((m) => (
              <li key={m.estudiante_id} className="fila-texto">
                <span className="fila-texto-titulo">{m.nombre}</span>
                <span className="texto-suave">
                  {m.total_ensayos} {m.total_ensayos === 1 ? 'ensayo' : 'ensayos'}
                  {m.ultimo_puntaje != null ? ` · último puntaje ${m.ultimo_puntaje}` : ''}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

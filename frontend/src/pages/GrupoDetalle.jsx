import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { etiquetaEje } from '../constantes.js'

export default function GrupoDetalle() {
  const { id } = useParams()
  const { llamar } = useApi()
  const [grupo, setGrupo] = useState(null)
  const [miembros, setMiembros] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    Promise.all([llamar((token) => api.obtenerGrupo(token, id)), llamar((token) => api.listarMiembros(token, id))])
      .then(([g, m]) => {
        if (cancelado) return
        setGrupo(g)
        setMiembros(m)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el grupo')
      })
    return () => {
      cancelado = true
    }
  }, [id, llamar])

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!grupo || !miembros) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>{grupo.nombre}</h1>
        <p>
          Código de invitación: <strong>{grupo.codigo_invitacion}</strong>
        </p>
        <p>
          {grupo.cantidad_miembros} estudiante{grupo.cantidad_miembros === 1 ? '' : 's'}
        </p>
        <p>Promedio del grupo: {grupo.promedio_grupo == null ? '—' : Math.round(grupo.promedio_grupo)}</p>

        <h2>Desempeño por eje</h2>
        <ul>
          {grupo.desempeno_por_eje.map((d) => (
            <li key={d.eje}>
              {etiquetaEje(d.eje)}: {d.correctas}/{d.total}
            </li>
          ))}
        </ul>

        <h2>Miembros</h2>
        {miembros.length === 0 ? (
          <p>Todavía no se unió ningún estudiante.</p>
        ) : (
          <table className="banco-tabla">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Unión</th>
                <th>Ensayos</th>
                <th>Último puntaje</th>
              </tr>
            </thead>
            <tbody>
              {miembros.map((m) => (
                <tr key={m.estudiante_id}>
                  <td>
                    <Link to={`/grupos/${id}/estudiantes/${m.estudiante_id}`}>{m.nombre}</Link>
                  </td>
                  <td>{new Date(m.fecha_union).toLocaleDateString()}</td>
                  <td>{m.total_ensayos}</td>
                  <td>{m.ultimo_puntaje == null ? '—' : m.ultimo_puntaje}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

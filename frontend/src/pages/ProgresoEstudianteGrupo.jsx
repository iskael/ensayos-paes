import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { etiquetaEje } from '../constantes.js'

function formatearFecha(fechaIso) {
  const d = new Date(fechaIso)
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`
}

export default function ProgresoEstudianteGrupo() {
  const { id, estudianteId } = useParams()
  const { llamar } = useApi()
  const [progreso, setProgreso] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.progresoEstudiante(token, id, estudianteId))
      .then((p) => {
        if (!cancelado) setProgreso(p)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el progreso del estudiante')
      })
    return () => {
      cancelado = true
    }
  }, [id, estudianteId, llamar])

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!progreso) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  const datosGrafico = progreso.evolucion.map((p) => ({ fecha: formatearFecha(p.fecha), puntaje: p.puntaje }))

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>{progreso.estudiante.nombre}</h1>
        <p>
          {progreso.estudiante.total_ensayos} ensayos rendidos — último puntaje:{' '}
          {progreso.estudiante.ultimo_puntaje == null ? '—' : progreso.estudiante.ultimo_puntaje}
        </p>

        <h2>Desempeño por eje</h2>
        <ul>
          {progreso.desempeno_por_eje.map((d) => (
            <li key={d.eje}>
              {etiquetaEje(d.eje)}: {d.correctas}/{d.total}
            </li>
          ))}
        </ul>

        {datosGrafico.length > 0 && (
          <>
            <h2>Evolución del puntaje</h2>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={datosGrafico}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="fecha" />
                <YAxis domain={[0, 1000]} />
                <Tooltip />
                <Line type="monotone" dataKey="puntaje" stroke="#2f6fed" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </>
        )}
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { etiquetaEje, PRUEBAS } from '../constantes.js'

function formatearFecha(fechaIso) {
  const d = new Date(fechaIso)
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`
}

export default function Dashboard() {
  const { llamar } = useApi()
  const [resumen, setResumen] = useState(null)
  const [evolucion, setEvolucion] = useState(null)
  const [error, setError] = useState(null)
  const [nivel, setNivel] = useState('')

  useEffect(() => {
    let cancelado = false
    Promise.all([
      llamar((token) => api.dashboardResumen(token, nivel)),
      llamar((token) => api.dashboardEvolucion(token, nivel)),
    ])
      .then(([r, e]) => {
        if (cancelado) return
        setResumen(r)
        setEvolucion(e)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el dashboard')
      })
    return () => {
      cancelado = true
    }
  }, [llamar, nivel])

  const filtros = (
    <div className="chips" style={{ margin: '4px 0 14px' }}>
      <button type="button" className={'chip' + (nivel === '' ? ' activo' : '')} onClick={() => setNivel('')}>
        Todas
      </button>
      {PRUEBAS.map((p) => (
        <button key={p.nivel} type="button" className={'chip' + (nivel === p.nivel ? ' activo' : '')} onClick={() => setNivel(p.nivel)}>
          {p.nombre}
        </button>
      ))}
    </div>
  )

  if (error) {
    return (
      <div className="contenido">
        <p className="error">{error}</p>
      </div>
    )
  }

  if (!resumen || !evolucion) return <p className="cargando">Cargando…</p>

  if (resumen.total_ensayos === 0) {
    return (
      <div className="contenido">
        <h1>Mi progreso</h1>
        {filtros}
        <div className="panel vacio">
          <p>{nivel ? 'Todavía no rendiste ensayos de esta prueba.' : 'Todavía no rendiste ningún ensayo.'}</p>
          <Link to="/" className="boton">
            Rendir mi primer ensayo
          </Link>
        </div>
      </div>
    )
  }

  const datosGrafico = evolucion.map((p) => ({ fecha: formatearFecha(p.fecha), puntaje: p.puntaje }))

  const metricas = [
    [resumen.total_ensayos, 'Ensayos rendidos'],
    [resumen.ultimo_puntaje, 'Último puntaje'],
    [resumen.mejor_puntaje, 'Mejor puntaje'],
    [Math.round(resumen.promedio_puntaje), 'Promedio'],
  ]

  return (
    <div className="contenido">
      <div>
        <h1>Mi progreso</h1>
        {filtros}

        <div className="dashboard-tarjetas">
          {metricas.map(([valor, etiqueta]) => (
            <div className="dashboard-metrica" key={etiqueta}>
              <span className="dashboard-metrica-valor">{valor}</span>
              <span className="dashboard-metrica-etiqueta">{etiqueta}</span>
            </div>
          ))}
        </div>

        <div className="panel">
          <h2 style={{ marginTop: 0 }}>Por tema</h2>
          {resumen.desempeno_por_eje.map((d) => (
            <div className="barra-eje" key={d.eje}>
              <div className="barra-eje-fila">
                <span>{etiquetaEje(d.eje)}</span>
                <span className="texto-suave">
                  {d.total ? Math.round((d.correctas / d.total) * 100) : 0} % · {d.correctas}/{d.total}
                </span>
              </div>
              <div className="barra-eje-fondo">
                <div style={{ width: `${d.total ? (d.correctas / d.total) * 100 : 0}%` }} />
              </div>
            </div>
          ))}
        </div>

        {datosGrafico.length > 0 && (
          <div className="panel">
            <h2 style={{ marginTop: 0 }}>Evolución del puntaje</h2>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={datosGrafico}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-borde)" />
                <XAxis dataKey="fecha" />
                <YAxis domain={[0, 1000]} />
                <Tooltip />
                <Line type="monotone" dataKey="puntaje" stroke="#4f46e5" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}

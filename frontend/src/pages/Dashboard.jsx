import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES } from '../constantes.js'

function etiquetaEje(valor) {
  return EJES.find((e) => e.valor === valor)?.etiqueta ?? valor
}

function formatearFecha(fechaIso) {
  const d = new Date(fechaIso)
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`
}

export default function Dashboard() {
  const { llamar } = useApi()
  const [resumen, setResumen] = useState(null)
  const [evolucion, setEvolucion] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    Promise.all([
      llamar((token) => api.dashboardResumen(token)),
      llamar((token) => api.dashboardEvolucion(token)),
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
  }, [llamar])

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!resumen || !evolucion) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  if (resumen.total_ensayos === 0) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>Mi progreso</h1>
          <p>Todavía no rendiste ningún ensayo.</p>
          <Link to="/" className="boton" style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>
            Rendir mi primer ensayo
          </Link>
        </div>
      </div>
    )
  }

  const datosGrafico = evolucion.map((p) => ({ fecha: formatearFecha(p.fecha), puntaje: p.puntaje }))

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Mi progreso</h1>

        <div className="dashboard-tarjetas">
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{resumen.total_ensayos}</span>
            <span className="dashboard-metrica-etiqueta">Ensayos rendidos</span>
          </div>
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{resumen.ultimo_puntaje}</span>
            <span className="dashboard-metrica-etiqueta">Último puntaje</span>
          </div>
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{resumen.mejor_puntaje}</span>
            <span className="dashboard-metrica-etiqueta">Mejor puntaje</span>
          </div>
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{Math.round(resumen.promedio_puntaje)}</span>
            <span className="dashboard-metrica-etiqueta">Promedio</span>
          </div>
        </div>

        <h2>Desempeño por eje</h2>
        <ul>
          {resumen.desempeno_por_eje.map((d) => (
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

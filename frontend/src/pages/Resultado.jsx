import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES } from '../constantes.js'
import Formula from '../components/Formula.jsx'

function etiquetaEje(valor) {
  return EJES.find((e) => e.valor === valor)?.etiqueta ?? valor
}

function textoAlternativa(alternativas, etiqueta) {
  return alternativas.find((a) => a.etiqueta === etiqueta)?.texto ?? null
}

export default function Resultado() {
  const { id } = useParams()
  const { llamar } = useApi()
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.obtenerResultado(token, id))
      .then((r) => {
        if (!cancelado) setResultado(r)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el resultado')
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

  if (!resultado) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Puntaje: {resultado.puntaje} / 1000</h1>
        <p>
          {resultado.correctas} de {resultado.total} correctas
        </p>

        <h2>Desglose por eje</h2>
        <ul>
          {resultado.desglose_por_eje.map((d) => (
            <li key={d.eje}>
              {etiquetaEje(d.eje)}: {d.correctas}/{d.total}
            </li>
          ))}
        </ul>

        <h2>Revisión</h2>
        {resultado.revision.map((item) => (
          <div
            key={item.orden}
            style={{ marginBottom: 16, paddingBottom: 16, borderBottom: '1px solid var(--color-borde)' }}
          >
            <p>
              {item.orden}. <Formula texto={item.enunciado} />
            </p>
            <p>
              Tu respuesta:{' '}
              {item.respuesta_seleccionada ? (
                <>
                  {item.respuesta_seleccionada}){' '}
                  <Formula texto={textoAlternativa(item.alternativas, item.respuesta_seleccionada)} />
                </>
              ) : (
                '(sin responder)'
              )}
              {' — '}
              Correcta: {item.respuesta_correcta}){' '}
              <Formula texto={textoAlternativa(item.alternativas, item.respuesta_correcta)} />
              {' — '}
              <strong style={{ color: item.es_correcta ? 'green' : 'var(--color-error)' }}>
                {item.es_correcta ? 'Correcta' : 'Incorrecta'}
              </strong>
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

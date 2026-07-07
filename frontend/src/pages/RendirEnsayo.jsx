import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import Formula from '../components/Formula.jsx'

export default function RendirEnsayo() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { llamar } = useApi()

  const [preguntas, setPreguntas] = useState(null)
  const [indice, setIndice] = useState(0)
  const [respuestas, setRespuestas] = useState({})
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.obtenerEnsayo(token, id))
      .then((ensayo) => {
        if (cancelado) return
        setPreguntas(ensayo.preguntas)
        const iniciales = {}
        for (const p of ensayo.preguntas) {
          if (p.respuesta_seleccionada) iniciales[p.ensayo_item_id] = p.respuesta_seleccionada
        }
        setRespuestas(iniciales)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el ensayo')
      })
    return () => {
      cancelado = true
    }
  }, [id, llamar])

  const guardarRespuesta = useCallback(
    async (ensayoItemId, etiqueta) => {
      setRespuestas((actuales) => ({ ...actuales, [ensayoItemId]: etiqueta }))
      try {
        await llamar((token) =>
          api.guardarRespuestas(token, id, {
            respuestas: [{ ensayo_item_id: ensayoItemId, respuesta_seleccionada: etiqueta }],
          }),
        )
      } catch {
        setError('No se pudo guardar la respuesta, revisá tu conexión')
      }
    },
    [id, llamar],
  )

  async function alEnviarEnsayo() {
    if (!window.confirm('¿Enviar el ensayo? No vas a poder cambiar las respuestas después.')) return
    setEnviando(true)
    setError(null)
    try {
      await llamar((token) => api.enviarEnsayo(token, id))
      navigate(`/ensayos/${id}/resultado`)
    } catch (e) {
      setError(e instanceof ApiError && e.status === 409 ? 'Este ensayo ya fue enviado' : 'No se pudo enviar el ensayo')
      setEnviando(false)
    }
  }

  if (error && !preguntas) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!preguntas) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  const pregunta = preguntas[indice]
  const esUltima = indice === preguntas.length - 1

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <p>
          Pregunta {indice + 1} de {preguntas.length}
        </p>
        <Formula texto={pregunta.enunciado} />
        <div style={{ marginTop: 16 }}>
          {pregunta.alternativas.map((alt) => (
            <button
              key={alt.etiqueta}
              type="button"
              className={
                'alternativa' + (respuestas[pregunta.ensayo_item_id] === alt.etiqueta ? ' seleccionada' : '')
              }
              onClick={() => guardarRespuesta(pregunta.ensayo_item_id, alt.etiqueta)}
            >
              {alt.etiqueta}) <Formula texto={alt.texto} />
            </button>
          ))}
        </div>
        {error && <p className="error">{error}</p>}
        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <button
            className="boton-secundario"
            type="button"
            disabled={indice === 0}
            onClick={() => setIndice((i) => i - 1)}
          >
            Anterior
          </button>
          {esUltima ? (
            <button className="boton" type="button" disabled={enviando} onClick={alEnviarEnsayo}>
              {enviando ? 'Enviando…' : 'Enviar ensayo'}
            </button>
          ) : (
            <button className="boton" type="button" onClick={() => setIndice((i) => i + 1)}>
              Siguiente
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

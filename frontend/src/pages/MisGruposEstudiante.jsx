import { useState, useEffect } from 'react'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'

export default function MisGruposEstudiante() {
  const { llamar } = useApi()
  const [grupos, setGrupos] = useState(null)
  const [error, setError] = useState(null)
  const [codigo, setCodigo] = useState('')
  const [uniendo, setUniendo] = useState(false)
  const [errorUnirse, setErrorUnirse] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.misGrupos(token))
      .then((lista) => {
        if (!cancelado) setGrupos(lista)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudieron cargar tus grupos')
      })
    return () => {
      cancelado = true
    }
  }, [llamar])

  async function unirse(evento) {
    evento.preventDefault()
    if (!codigo.trim()) return
    setErrorUnirse(null)
    setUniendo(true)
    try {
      await llamar((token) => api.unirseGrupo(token, codigo.trim().toUpperCase()))
      const lista = await llamar((token) => api.misGrupos(token))
      setGrupos(lista)
      setCodigo('')
    } catch (err) {
      setErrorUnirse(
        err instanceof ApiError ? err.mensaje || 'No se pudo unir al grupo' : 'No se pudo conectar con el servidor',
      )
    } finally {
      setUniendo(false)
    }
  }

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!grupos) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Mis grupos</h1>

        <form onSubmit={unirse} style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <input
            type="text"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            placeholder="Código de invitación"
            style={{
              flex: 1,
              minHeight: 44,
              padding: '0 12px',
              border: '1px solid var(--color-borde)',
              borderRadius: 8,
            }}
          />
          <button className="boton" type="submit" disabled={uniendo} style={{ width: 'auto', padding: '0 16px' }}>
            {uniendo ? 'Uniendo…' : 'Unirme'}
          </button>
        </form>
        {errorUnirse && <p className="error">{errorUnirse}</p>}

        {grupos.length === 0 ? (
          <p>Todavía no perteneces a ningún grupo. Pedile el código a tu profesor.</p>
        ) : (
          <ul>
            {grupos.map((g) => (
              <li key={g.id}>
                <strong>{g.nombre}</strong> — profesor {g.profesor_nombre} (desde{' '}
                {new Date(g.fecha_union).toLocaleDateString()})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

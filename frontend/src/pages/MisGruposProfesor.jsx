import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'

export default function MisGruposProfesor() {
  const { llamar } = useApi()
  const [grupos, setGrupos] = useState(null)
  const [error, setError] = useState(null)
  const [nombreNuevo, setNombreNuevo] = useState('')
  const [creando, setCreando] = useState(false)
  const [errorCrear, setErrorCrear] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.listarGrupos(token))
      .then((lista) => {
        if (!cancelado) setGrupos(lista)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudieron cargar los grupos')
      })
    return () => {
      cancelado = true
    }
  }, [llamar])

  async function crearGrupo(evento) {
    evento.preventDefault()
    if (!nombreNuevo.trim()) return
    setErrorCrear(null)
    setCreando(true)
    try {
      const grupo = await llamar((token) => api.crearGrupo(token, { nombre: nombreNuevo.trim() }))
      setGrupos((actuales) => [grupo, ...(actuales ?? [])])
      setNombreNuevo('')
    } catch (err) {
      setErrorCrear(
        err instanceof ApiError ? err.mensaje || 'No se pudo crear el grupo' : 'No se pudo conectar con el servidor',
      )
    } finally {
      setCreando(false)
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
      <div className="tarjeta tarjeta-ancha">
        <h1>Mis grupos</h1>

        <form onSubmit={crearGrupo} style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <input
            type="text"
            value={nombreNuevo}
            onChange={(e) => setNombreNuevo(e.target.value)}
            placeholder="Nombre del grupo"
            style={{
              flex: 1,
              minHeight: 44,
              padding: '0 12px',
              border: '1px solid var(--color-borde)',
              borderRadius: 8,
            }}
          />
          <button className="boton" type="submit" disabled={creando} style={{ width: 'auto', padding: '0 16px' }}>
            {creando ? 'Creando…' : 'Crear grupo'}
          </button>
        </form>
        {errorCrear && <p className="error">{errorCrear}</p>}

        {grupos.length === 0 ? (
          <p>Todavía no creaste ningún grupo.</p>
        ) : (
          <table className="banco-tabla">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Código</th>
                <th>Creado</th>
              </tr>
            </thead>
            <tbody>
              {grupos.map((g) => (
                <tr key={g.id}>
                  <td>
                    <Link to={`/grupos/${g.id}`}>{g.nombre}</Link>
                  </td>
                  <td>{g.codigo_invitacion}</td>
                  <td>{new Date(g.fecha_creacion).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

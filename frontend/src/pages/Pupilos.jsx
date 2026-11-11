import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'

export default function Pupilos() {
  const { llamar } = useApi()
  const [lista, setLista] = useState(null)
  const [codigo, setCodigo] = useState('')
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)

  const cargar = useCallback(() => {
    llamar((t) => api.listarPupilos(t))
      .then(setLista)
      .catch(() => setError('No se pudo cargar la lista'))
  }, [llamar])

  useEffect(() => {
    cargar()
  }, [cargar])

  async function vincular(e) {
    e.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      await llamar((t) => api.vincularPupilo(t, codigo))
      setCodigo('')
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Mis estudiantes</h1>
        <p className="texto-suave">
          Pídele al estudiante el código que aparece en su pestaña <strong>Grupos</strong>, en «Mi apoderado».
        </p>
        <form onSubmit={vincular} className="form-en-linea">
          <input type="text" value={codigo} onChange={(e) => setCodigo(e.target.value)} placeholder="Código del estudiante" required />
          <button className="boton boton-auto" type="submit" disabled={enviando}>
            {enviando ? 'Agregando…' : 'Agregar'}
          </button>
        </form>
        {error && <p className="error">{error}</p>}

        {!lista ? (
          <p>Cargando…</p>
        ) : lista.length === 0 ? (
          <p>Aún no sigues a ningún estudiante.</p>
        ) : (
          <ul className="lista-textos">
            {lista.map((p) => (
              <li key={p.id}>
                <Link to={`/pupilos/${p.id}`} className="fila-texto">
                  <span className="fila-texto-titulo">{p.nombre}</span>
                  <span className="texto-suave">
                    {p.total_ensayos} {p.total_ensayos === 1 ? 'ensayo' : 'ensayos'}
                    {p.ultimo_puntaje != null ? ` · último puntaje ${p.ultimo_puntaje}` : ''}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

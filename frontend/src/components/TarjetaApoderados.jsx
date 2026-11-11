import { useState, useEffect, useCallback } from 'react'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'

export default function TarjetaApoderados() {
  const { llamar } = useApi()
  const [codigo, setCodigo] = useState(null)
  const [apoderados, setApoderados] = useState([])
  const [error, setError] = useState(null)

  const cargar = useCallback(() => {
    Promise.all([llamar((t) => api.codigoApoderado(t)), llamar((t) => api.misApoderados(t))])
      .then(([c, a]) => {
        setCodigo(c)
        setApoderados(a)
      })
      .catch(() => setError('No se pudo cargar la información de apoderados'))
  }, [llamar])

  useEffect(() => {
    cargar()
  }, [cargar])

  async function regenerar() {
    setError(null)
    try {
      setCodigo(await llamar((t) => api.nuevoCodigoApoderado(t)))
    } catch {
      setError('No se pudo generar un código nuevo')
    }
  }

  async function quitar(id) {
    if (!window.confirm('¿Quitar a este apoderado? Ya no verá tu progreso.')) return
    try {
      await llamar((t) => api.quitarApoderado(t, id))
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje : 'No se pudo quitar')
    }
  }

  return (
    <div className="tarjeta">
      <h2>Mi apoderado</h2>
      <p className="texto-suave">
        Comparte este código con tu mamá, papá o apoderado: al ingresarlo en su cuenta verá tu progreso (puntajes y desempeño por eje),
        no tus respuestas. Vence en 7 días.
      </p>
      {codigo && (
        <div className="codigo-grande">
          <span aria-label="Código para tu apoderado">{codigo.codigo}</span>
          <small className="texto-suave">vence el {new Date(codigo.expira_en).toLocaleDateString('es-CL')}</small>
        </div>
      )}
      <button type="button" className="boton-enlace" onClick={regenerar}>
        Generar otro código
      </button>
      {error && <p className="error">{error}</p>}
      {apoderados.length > 0 && (
        <ul className="lista-textos">
          {apoderados.map((a) => (
            <li key={a.id} className="fila-texto fila-con-accion">
              <span>
                <span className="fila-texto-titulo">{a.nombre}</span>
                <br />
                <span className="texto-suave">{a.email}</span>
              </span>
              <button type="button" className="boton-enlace" onClick={() => quitar(a.id)}>
                Quitar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

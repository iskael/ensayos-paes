import { useState, useEffect } from 'react'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'

export default function TarjetaInstitucionProfesor() {
  const { llamar } = useApi()
  const [institucion, setInstitucion] = useState(undefined)
  const [codigo, setCodigo] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    llamar((t) => api.institucionDelProfesor(t))
      .then(setInstitucion)
      .catch(() => setInstitucion(null))
  }, [llamar])

  async function unirse(e) {
    e.preventDefault()
    setError(null)
    try {
      setInstitucion(await llamar((t) => api.unirseInstitucion(t, codigo)))
      setCodigo('')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje : 'No se pudo unir')
    }
  }

  async function salir() {
    if (!window.confirm('¿Salir de la institución? Dejará de ver tus grupos.')) return
    try {
      await llamar((t) => api.salirInstitucion(t))
      setInstitucion(null)
    } catch {
      setError('No se pudo salir')
    }
  }

  if (institucion === undefined) return null

  return (
    <div className="tarjeta tarjeta-ancha">
      <h2>Institución</h2>
      {institucion ? (
        <div className="fila-con-accion">
          <span>
            Perteneces a <strong>{institucion.nombre}</strong>. Su responsable ve tus grupos y el resumen de tus estudiantes.
          </span>
          <button type="button" className="boton-enlace" onClick={salir}>
            Salir
          </button>
        </div>
      ) : (
        <>
          <p className="texto-suave">Si tu colegio o preuniversitario usa la app, ingresa el código que te dio su responsable.</p>
          <form onSubmit={unirse} className="form-en-linea">
            <input type="text" value={codigo} onChange={(e) => setCodigo(e.target.value)} placeholder="Código de la institución" required />
            <button className="boton boton-auto" type="submit">
              Unirme
            </button>
          </form>
        </>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  )
}

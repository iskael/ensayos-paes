import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'

export default function Institucion() {
  const { llamar } = useApi()
  const [datos, setDatos] = useState(undefined)
  const [nombre, setNombre] = useState('')
  const [error, setError] = useState(null)

  const cargar = useCallback(() => {
    llamar((t) => api.miInstitucion(t))
      .then(setDatos)
      .catch((err) => {
        if (err instanceof ApiError && err.status === 404) setDatos(null)
        else setError('No se pudo cargar la institución')
      })
  }, [llamar])

  useEffect(() => {
    cargar()
  }, [cargar])

  async function crear(e) {
    e.preventDefault()
    setError(null)
    try {
      await llamar((t) => api.crearInstitucion(t, nombre))
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje : 'No se pudo crear')
    }
  }

  async function regenerar() {
    if (!window.confirm('El código actual dejará de funcionar. ¿Generar uno nuevo?')) return
    try {
      await llamar((t) => api.nuevoCodigoInstitucion(t))
      cargar()
    } catch {
      setError('No se pudo generar el código')
    }
  }

  async function quitar(p) {
    if (!window.confirm(`¿Quitar a ${p.nombre} de la institución?`)) return
    try {
      await llamar((t) => api.quitarProfesorInstitucion(t, p.id))
      cargar()
    } catch {
      setError('No se pudo quitar al profesor')
    }
  }

  if (datos === undefined) {
    return (
      <div className="pantalla">
        <div className="tarjeta">{error ?? 'Cargando…'}</div>
      </div>
    )
  }

  if (datos === null) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>Crea tu institución</h1>
          <p className="texto-suave">
            Tus profesores se unen con un código y tú ves sus grupos y el avance de sus estudiantes.
          </p>
          <form onSubmit={crear}>
            <div className="campo">
              <label htmlFor="nombre">Nombre</label>
              <input id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Ej.: Liceo Bicentenario de…" required maxLength={120} />
            </div>
            {error && <p className="error">{error}</p>}
            <button className="boton" type="submit">
              Crear institución
            </button>
          </form>
        </div>
      </div>
    )
  }

  const { institucion, profesores, grupos } = datos
  const totalEstudiantes = grupos.reduce((s, g) => s + g.miembros, 0)

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>{institucion.nombre}</h1>
        <div className="dashboard-tarjetas">
          {[
            [profesores.length, 'Profesores'],
            [grupos.length, 'Grupos'],
            [totalEstudiantes, 'Inscripciones'],
          ].map(([v, e]) => (
            <div className="dashboard-metrica" key={e}>
              <span className="dashboard-metrica-valor">{v}</span>
              <span className="dashboard-metrica-etiqueta">{e}</span>
            </div>
          ))}
        </div>

        <h2>Código para profesores</h2>
        <p className="texto-suave">Cada profesor lo ingresa en su pestaña Grupos, en «Institución».</p>
        <div className="codigo-grande">
          <span>{institucion.codigo_invitacion}</span>
        </div>
        <button type="button" className="boton-enlace" onClick={regenerar}>
          Generar otro código
        </button>
        {error && <p className="error">{error}</p>}

        <h2>Profesores</h2>
        {profesores.length === 0 ? (
          <p className="texto-suave">Aún no se une ningún profesor.</p>
        ) : (
          <ul className="lista-textos">
            {profesores.map((p) => (
              <li key={p.id} className="fila-texto fila-con-accion">
                <span>
                  <span className="fila-texto-titulo">{p.nombre}</span>
                  <br />
                  <span className="texto-suave">
                    {p.email} · {p.grupos} {p.grupos === 1 ? 'grupo' : 'grupos'} · {p.estudiantes}{' '}
                    {p.estudiantes === 1 ? 'estudiante' : 'estudiantes'}
                  </span>
                </span>
                <button type="button" className="boton-enlace" onClick={() => quitar(p)}>
                  Quitar
                </button>
              </li>
            ))}
          </ul>
        )}

        <h2>Grupos</h2>
        {grupos.length === 0 ? (
          <p className="texto-suave">Los grupos de tus profesores aparecerán aquí.</p>
        ) : (
          <ul className="lista-textos">
            {grupos.map((g) => (
              <li key={g.id}>
                <Link to={`/institucion/grupos/${g.id}`} className="fila-texto">
                  <span className="fila-texto-titulo">{g.nombre}</span>
                  <span className="texto-suave">
                    {g.profesor_nombre} · {g.miembros} {g.miembros === 1 ? 'estudiante' : 'estudiantes'}
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

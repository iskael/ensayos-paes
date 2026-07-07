import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { NIVELES, TIPOS_EXAMEN } from '../constantes.js'

const VACIO = {
  nombre: '',
  anio_admision: new Date().getFullYear(),
  tipo: TIPOS_EXAMEN[0].valor,
  nivel: NIVELES[0],
  edicion: '',
  url_pdf: '',
  fecha_publicacion: '',
}

export default function ExamenForm() {
  const { id } = useParams()
  const esNuevo = id === undefined
  const navigate = useNavigate()
  const { llamar } = useApi()
  const [form, setForm] = useState(VACIO)
  const [cargando, setCargando] = useState(!esNuevo)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    if (esNuevo) return
    let cancelado = false
    llamar((token) => api.obtenerExamen(token, id))
      .then((ex) => {
        if (cancelado) return
        setForm({
          nombre: ex.nombre,
          anio_admision: ex.anio_admision,
          tipo: ex.tipo,
          nivel: ex.nivel,
          edicion: ex.edicion ?? '',
          url_pdf: ex.url_pdf ?? '',
          fecha_publicacion: ex.fecha_publicacion ?? '',
        })
        setCargando(false)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el examen')
      })
    return () => {
      cancelado = true
    }
  }, [esNuevo, id, llamar])

  function actualizarCampo(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }))
  }

  async function guardar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    const cuerpo = {
      nombre: form.nombre,
      anio_admision: Number(form.anio_admision),
      tipo: form.tipo,
      nivel: form.nivel,
      edicion: form.edicion || null,
      url_pdf: form.url_pdf || null,
      fecha_publicacion: form.fecha_publicacion || null,
    }
    try {
      if (esNuevo) {
        await llamar((token) => api.crearExamen(token, cuerpo))
      } else {
        await llamar((token) => api.actualizarExamen(token, id, cuerpo))
      }
      navigate('/banco/examenes')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo guardar el examen' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  async function eliminar() {
    if (!window.confirm('¿Eliminar este examen?')) return
    try {
      await llamar((token) => api.eliminarExamen(token, id))
      navigate('/banco/examenes')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo eliminar el examen' : 'No se pudo conectar con el servidor')
    }
  }

  if (cargando) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>{esNuevo ? 'Nuevo examen' : 'Editar examen'}</h1>
        <form onSubmit={guardar}>
          <div className="campo">
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              type="text"
              value={form.nombre}
              onChange={(e) => actualizarCampo('nombre', e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="anio">Año de admisión</label>
            <input
              id="anio"
              type="number"
              value={form.anio_admision}
              onChange={(e) => actualizarCampo('anio_admision', e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="tipo">Tipo</label>
            <select id="tipo" value={form.tipo} onChange={(e) => actualizarCampo('tipo', e.target.value)}>
              {TIPOS_EXAMEN.map((t) => (
                <option key={t.valor} value={t.valor}>
                  {t.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="nivel">Nivel</label>
            <select id="nivel" value={form.nivel} onChange={(e) => actualizarCampo('nivel', e.target.value)}>
              {NIVELES.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="edicion">Edición (opcional)</label>
            <input id="edicion" type="text" value={form.edicion} onChange={(e) => actualizarCampo('edicion', e.target.value)} />
          </div>
          <div className="campo">
            <label htmlFor="url_pdf">URL del PDF (opcional)</label>
            <input id="url_pdf" type="text" value={form.url_pdf} onChange={(e) => actualizarCampo('url_pdf', e.target.value)} />
          </div>
          <div className="campo">
            <label htmlFor="fecha_publicacion">Fecha de publicación (opcional)</label>
            <input
              id="fecha_publicacion"
              type="date"
              value={form.fecha_publicacion}
              onChange={(e) => actualizarCampo('fecha_publicacion', e.target.value)}
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Guardando…' : 'Guardar'}
          </button>
        </form>
        {!esNuevo && (
          <button
            type="button"
            className="boton-secundario"
            style={{ marginTop: 12, borderColor: 'var(--color-error)', color: 'var(--color-error)' }}
            onClick={eliminar}
          >
            Eliminar examen
          </button>
        )}
      </div>
    </div>
  )
}

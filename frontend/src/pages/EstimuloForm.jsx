import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { api, ApiError, urlImagen } from '../api.js'
import { useApi } from '../useApi.js'
import { PRUEBAS, etiquetaEje } from '../constantes.js'
import Estimulo from '../components/Estimulo.jsx'

export default function EstimuloForm() {
  const { id } = useParams()
  const esNuevo = id === undefined
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { llamar } = useApi()
  const [form, setForm] = useState({ nivel: searchParams.get('nivel') || 'CL', titulo: '', texto: '', fuente: '', imagen_url: null })
  const [info, setInfo] = useState(null)
  const [items, setItems] = useState([])
  const [cargando, setCargando] = useState(!esNuevo)
  const [error, setError] = useState(null)
  const [aviso, setAviso] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [subiendo, setSubiendo] = useState(false)

  useEffect(() => {
    if (esNuevo) return
    let cancelado = false
    Promise.all([
      llamar((token) => api.obtenerEstimulo(token, id)),
      llamar((token) => api.listarItems(token, { estimuloId: id, limit: 100 })),
    ])
      .then(([e, its]) => {
        if (cancelado) return
        setInfo(e)
        setItems(its)
        setForm({ nivel: e.nivel ?? '', titulo: e.titulo ?? '', texto: e.texto, fuente: e.fuente ?? '', imagen_url: e.imagen_url ?? null })
        setCargando(false)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el texto')
      })
    return () => {
      cancelado = true
    }
  }, [esNuevo, id, llamar])

  function campo(nombre, valor) {
    setAviso(null)
    setForm((f) => ({ ...f, [nombre]: valor }))
  }

  async function subirImagen(archivo) {
    setSubiendo(true)
    try {
      const datos = new FormData()
      datos.append('archivo', archivo)
      const { url } = await llamar((token) => api.subirImagen(token, datos))
      campo('imagen_url', url)
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo subir la imagen' : 'No se pudo subir la imagen')
    } finally {
      setSubiendo(false)
    }
  }

  async function guardar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    const cuerpo = { ...form, nivel: form.nivel || null }
    try {
      if (esNuevo) {
        const creado = await llamar((token) => api.crearEstimulo(token, cuerpo))
        navigate(`/banco/textos/${creado.id}`, { replace: true })
      } else {
        const actualizado = await llamar((token) => api.actualizarEstimulo(token, id, cuerpo))
        setInfo(actualizado)
        setAviso('Cambios guardados')
      }
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo guardar el texto' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  async function eliminar() {
    if (!window.confirm('¿Eliminar este texto? No se puede deshacer.')) return
    setError(null)
    try {
      await llamar((token) => api.eliminarEstimulo(token, id))
      navigate('/banco/textos', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo eliminar' : 'No se pudo conectar con el servidor')
    }
  }

  if (cargando) {
    return (
      <div className="pantalla">
        <div className="tarjeta tarjeta-ancha">{error ?? 'Cargando…'}</div>
      </div>
    )
  }

  const siguienteOrden = items.reduce((m, it) => Math.max(m, it.orden_estimulo ?? 0), 0) + 1
  const conPreguntas = (info?.cantidad_items ?? 0) > 0

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <Link to="/banco/textos" className="boton-enlace">
          ← Textos
        </Link>
        <h1>{esNuevo ? 'Nuevo texto' : 'Editar texto'}</h1>
        <div className="editor-texto">
          <form onSubmit={guardar}>
            <div className="campo">
              <label htmlFor="nivel">Prueba</label>
              <select id="nivel" value={form.nivel} disabled={conPreguntas} onChange={(e) => campo('nivel', e.target.value)}>
                {PRUEBAS.map((p) => (
                  <option key={p.nivel} value={p.nivel}>
                    {p.nombre}
                  </option>
                ))}
              </select>
              {conPreguntas && <small className="texto-suave">No se puede cambiar porque ya tiene preguntas.</small>}
            </div>
            <div className="campo">
              <label htmlFor="titulo">Título</label>
              <input id="titulo" type="text" value={form.titulo} onChange={(e) => campo('titulo', e.target.value)} />
            </div>
            <div className="campo">
              <label htmlFor="texto">Texto</label>
              <textarea id="texto" className="textarea-largo" value={form.texto} onChange={(e) => campo('texto', e.target.value)} required />
              <small className="texto-suave">
                Separa los párrafos con una línea en blanco: la app los numera y las preguntas pueden referirse a «el párrafo 2». Un
                salto de línea simple se mantiene dentro del párrafo (sirve para versos).
              </small>
            </div>
            <div className="campo">
              <label htmlFor="fuente">Fuente</label>
              <input id="fuente" type="text" value={form.fuente} onChange={(e) => campo('fuente', e.target.value)} />
            </div>
            <div className="campo">
              <label htmlFor="imagen">Imagen (opcional)</label>
              <input id="imagen" type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => e.target.files[0] && subirImagen(e.target.files[0])} />
              {subiendo && <p>Subiendo imagen…</p>}
              {form.imagen_url && (
                <>
                  <img src={urlImagen(form.imagen_url)} alt="" style={{ maxWidth: '100%', marginTop: 8 }} />
                  <button type="button" className="boton-enlace" onClick={() => campo('imagen_url', null)}>
                    Quitar imagen
                  </button>
                </>
              )}
            </div>
            {error && <p className="error">{error}</p>}
            {aviso && <p className="aviso-ok">{aviso}</p>}
            <button className="boton" type="submit" disabled={enviando}>
              {enviando ? 'Guardando…' : 'Guardar'}
            </button>
            {!esNuevo && !conPreguntas && (
              <button type="button" className="boton-secundario" onClick={eliminar} style={{ marginTop: 8 }}>
                Eliminar texto
              </button>
            )}
          </form>

          <div>
            <h2>Vista previa</h2>
            {form.texto.trim() ? (
              <Estimulo estimulo={{ ...form, titulo: form.titulo || null, fuente: form.fuente || null }} numerar={form.nivel === 'CL'} />
            ) : (
              <p className="texto-suave">Escribe el texto para ver cómo lo verá el estudiante.</p>
            )}
          </div>
        </div>

        {!esNuevo && (
          <>
            <div className="cabecera-banco" style={{ marginTop: 24 }}>
              <h2>Preguntas ({items.length})</h2>
              <Link to={`/banco/items/nuevo?estimuloId=${id}&nivel=${form.nivel}&orden=${siguienteOrden}`} className="boton boton-auto">
                Agregar pregunta
              </Link>
            </div>
            {items.length === 0 ? (
              <p className="texto-suave">Este texto aún no tiene preguntas.</p>
            ) : (
              <ol className="lista-textos">
                {items.map((it) => (
                  <li key={it.id}>
                    <Link to={`/banco/items/${it.id}`} className="fila-texto">
                      <span className="fila-texto-titulo">
                        {it.orden_estimulo ?? '–'}. {it.enunciado}
                      </span>
                      <span className="texto-suave">
                        {etiquetaEje(it.eje)} · {it.estado}
                      </span>
                    </Link>
                  </li>
                ))}
              </ol>
            )}
          </>
        )}
      </div>
    </div>
  )
}

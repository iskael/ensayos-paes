import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { NIVELES, EJES, DIFICULTADES } from '../constantes.js'
import Formula from '../components/Formula.jsx'
import AlternativaCampos from '../components/AlternativaCampos.jsx'

const ALTERNATIVAS_VACIAS = ['A', 'B', 'C', 'D'].map((etiqueta) => ({
  etiqueta,
  texto: '',
  imagen_url: null,
  es_correcta: false,
}))

const VACIO = {
  enunciado: '',
  imagen_url: null,
  eje: EJES[0].valor,
  nivel: NIVELES[0],
  dificultad: DIFICULTADES[0].valor,
  peso: '',
  examen_fuente_id: '',
  explicacion: '',
  alternativas: ALTERNATIVAS_VACIAS,
}

export default function ItemForm() {
  const { id } = useParams()
  const esNuevo = id === undefined
  const navigate = useNavigate()
  const { llamar } = useApi()
  const [form, setForm] = useState(VACIO)
  const [examenes, setExamenes] = useState([])
  const [cargando, setCargando] = useState(!esNuevo)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [subiendoImagen, setSubiendoImagen] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.listarExamenes(token))
      .then((lista) => {
        if (!cancelado) setExamenes(lista)
      })
      .catch(() => {})
    return () => {
      cancelado = true
    }
  }, [llamar])

  useEffect(() => {
    if (esNuevo) return
    let cancelado = false
    llamar((token) => api.obtenerItem(token, id))
      .then((it) => {
        if (cancelado) return
        setForm({
          enunciado: it.enunciado,
          imagen_url: it.imagen_url,
          eje: it.eje,
          nivel: it.nivel,
          dificultad: it.dificultad,
          peso: it.peso ?? '',
          examen_fuente_id: it.examen_fuente_id ?? '',
          explicacion: it.explicacion ?? '',
          alternativas: it.alternativas.map((a) => ({
            etiqueta: a.etiqueta,
            texto: a.texto,
            imagen_url: a.imagen_url,
            es_correcta: a.es_correcta,
          })),
        })
        setCargando(false)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el ítem')
      })
    return () => {
      cancelado = true
    }
  }, [esNuevo, id, llamar])

  function actualizarCampo(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }))
  }

  function cambiarTextoAlternativa(etiqueta, texto) {
    setForm((f) => ({
      ...f,
      alternativas: f.alternativas.map((a) => (a.etiqueta === etiqueta ? { ...a, texto } : a)),
    }))
  }

  function marcarCorrecta(etiqueta) {
    setForm((f) => ({
      ...f,
      alternativas: f.alternativas.map((a) => ({ ...a, es_correcta: a.etiqueta === etiqueta })),
    }))
  }

  async function subirImagenItem(archivo) {
    setSubiendoImagen('item')
    try {
      const datos = new FormData()
      datos.append('archivo', archivo)
      const { url } = await llamar((token) => api.subirImagen(token, datos))
      actualizarCampo('imagen_url', url)
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo subir la imagen' : 'No se pudo subir la imagen')
    } finally {
      setSubiendoImagen(null)
    }
  }

  async function subirImagenAlternativa(etiqueta, archivo) {
    setSubiendoImagen(etiqueta)
    try {
      const datos = new FormData()
      datos.append('archivo', archivo)
      const { url } = await llamar((token) => api.subirImagen(token, datos))
      setForm((f) => ({
        ...f,
        alternativas: f.alternativas.map((a) => (a.etiqueta === etiqueta ? { ...a, imagen_url: url } : a)),
      }))
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo subir la imagen' : 'No se pudo subir la imagen')
    } finally {
      setSubiendoImagen(null)
    }
  }

  async function guardar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    const cuerpo = {
      examen_fuente_id: form.examen_fuente_id || null,
      enunciado: form.enunciado,
      imagen_url: form.imagen_url,
      eje: form.eje,
      nivel: form.nivel,
      dificultad: form.dificultad,
      peso: form.peso === '' ? null : Number(form.peso),
      explicacion: form.explicacion || null,
      alternativas: form.alternativas,
    }
    try {
      if (esNuevo) {
        await llamar((token) => api.crearItem(token, cuerpo))
      } else {
        await llamar((token) => api.actualizarItem(token, id, cuerpo))
      }
      navigate('/banco/items')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo guardar el ítem' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  if (cargando) {
    return (
      <div className="pantalla">
        <div className="tarjeta tarjeta-ancha">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>{esNuevo ? 'Nuevo ítem' : 'Editar ítem'}</h1>
        <form onSubmit={guardar}>
          <div className="campo">
            <label htmlFor="enunciado">Enunciado (soporta LaTeX)</label>
            <textarea
              id="enunciado"
              value={form.enunciado}
              onChange={(e) => actualizarCampo('enunciado', e.target.value)}
              required
            />
            {form.enunciado && <Formula texto={form.enunciado} />}
          </div>
          <div className="campo">
            <label htmlFor="imagen-item">Imagen del ítem (opcional)</label>
            <input
              id="imagen-item"
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => e.target.files[0] && subirImagenItem(e.target.files[0])}
            />
            {subiendoImagen === 'item' && <p>Subiendo imagen…</p>}
            {form.imagen_url && <img src={form.imagen_url} alt="" style={{ maxWidth: '100%', marginTop: 8 }} />}
          </div>
          <div className="campo">
            <label htmlFor="eje">Eje</label>
            <select id="eje" value={form.eje} onChange={(e) => actualizarCampo('eje', e.target.value)}>
              {EJES.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
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
            <label htmlFor="dificultad">Dificultad</label>
            <select id="dificultad" value={form.dificultad} onChange={(e) => actualizarCampo('dificultad', e.target.value)}>
              {DIFICULTADES.map((d) => (
                <option key={d.valor} value={d.valor}>
                  {d.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="peso">Peso (requerido para publicar)</label>
            <input id="peso" type="number" min="0" value={form.peso} onChange={(e) => actualizarCampo('peso', e.target.value)} />
          </div>
          <div className="campo">
            <label htmlFor="examen">Examen fuente (opcional)</label>
            <select
              id="examen"
              value={form.examen_fuente_id}
              onChange={(e) => actualizarCampo('examen_fuente_id', e.target.value)}
            >
              <option value="">(ninguno)</option>
              {examenes.map((ex) => (
                <option key={ex.id} value={ex.id}>
                  {ex.nombre}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="explicacion">Explicación (opcional)</label>
            <textarea id="explicacion" value={form.explicacion} onChange={(e) => actualizarCampo('explicacion', e.target.value)} />
          </div>

          <h2>Alternativas</h2>
          {form.alternativas.map((alt) => (
            <AlternativaCampos
              key={alt.etiqueta}
              alternativa={alt}
              onCambiarTexto={cambiarTextoAlternativa}
              onCambiarImagen={subirImagenAlternativa}
              onMarcarCorrecta={marcarCorrecta}
              subiendo={subiendoImagen === alt.etiqueta}
            />
          ))}

          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando} style={{ marginTop: 8 }}>
            {enviando ? 'Guardando…' : 'Guardar'}
          </button>
        </form>
      </div>
    </div>
  )
}

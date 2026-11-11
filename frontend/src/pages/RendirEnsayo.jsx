import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, ApiError, urlImagen } from '../api.js'
import { useApi } from '../useApi.js'
import { datosPrueba, etiquetaEje } from '../constantes.js'
import Formula from '../components/Formula.jsx'
import Icono from '../components/Icono.jsx'
import Hoja from '../components/Hoja.jsx'
import Estimulo from '../components/Estimulo.jsx'

const TAMANOS_TEXTO = [16, 17, 19, 21]

function leerLocal(clave, porDefecto) {
  try {
    const v = localStorage.getItem(clave)
    return v ? JSON.parse(v) : porDefecto
  } catch {
    return porDefecto
  }
}

function guardarLocal(clave, valor) {
  try {
    localStorage.setItem(clave, JSON.stringify(valor))
  } catch {
    /* sin almacenamiento local */
  }
}

function formatearReloj(segundos) {
  const s = Math.max(0, segundos)
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const ss = String(s % 60).padStart(2, '0')
  return h ? `${h}:${String(m).padStart(2, '0')}:${ss}` : `${m}:${ss}`
}

export default function RendirEnsayo() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { llamar } = useApi()

  const [ensayo, setEnsayo] = useState(null)
  const [indice, setIndice] = useState(0)
  const [respuestas, setRespuestas] = useState({})
  const [correcciones, setCorrecciones] = useState({})
  const [marcadas, setMarcadas] = useState(() => leerLocal(`marcadas-${id}`, {}))
  const [tachadas, setTachadas] = useState(() => leerLocal(`tachadas-${id}`, {}))
  const [tamTexto, setTamTexto] = useState(() => leerLocal('tam-texto', 17))
  const [hoja, setHoja] = useState(null)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [revisando, setRevisando] = useState(false)
  const [ahora, setAhora] = useState(() => Date.now())
  const guardadosEnVuelo = useRef(new Map())
  const enviadoRef = useRef(false)
  const cuerpoRef = useRef(null)

  useEffect(() => {
    const enVuelo = guardadosEnVuelo.current
    return () => {
      for (const control of enVuelo.values()) control.abort()
      enVuelo.clear()
    }
  }, [])

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.obtenerEnsayo(token, id))
      .then((e) => {
        if (cancelado) return
        if (e.estado === 'finalizado') {
          navigate(`/ensayos/${id}/resultado`, { replace: true })
          return
        }
        setEnsayo(e)
        const iniciales = {}
        const corr = {}
        for (const p of e.preguntas) {
          if (p.respuesta_seleccionada) iniciales[p.ensayo_item_id] = p.respuesta_seleccionada
          if (p.correccion) corr[p.ensayo_item_id] = p.correccion
        }
        setRespuestas(iniciales)
        setCorrecciones(corr)
        const primeraLibre = e.preguntas.findIndex((p) => !p.respuesta_seleccionada)
        setIndice(primeraLibre > 0 ? primeraLibre : 0)
      })
      .catch(() => !cancelado && setError('No se pudo cargar el ensayo'))
    return () => {
      cancelado = true
    }
  }, [id, llamar, navigate])

  useEffect(() => guardarLocal(`marcadas-${id}`, marcadas), [id, marcadas])
  useEffect(() => guardarLocal(`tachadas-${id}`, tachadas), [id, tachadas])
  useEffect(() => {
    guardarLocal('tam-texto', tamTexto)
    document.documentElement.style.setProperty('--tam-texto', `${tamTexto}px`)
  }, [tamTexto])

  const limiteMs = useMemo(() => {
    if (!ensayo?.limite_minutos) return null
    return new Date(ensayo.fecha_inicio).getTime() + ensayo.limite_minutos * 60000
  }, [ensayo])

  useEffect(() => {
    if (!limiteMs) return
    const t = setInterval(() => setAhora(Date.now()), 1000)
    return () => clearInterval(t)
  }, [limiteMs])

  const enviar = useCallback(async () => {
    if (enviadoRef.current) return
    enviadoRef.current = true
    setEnviando(true)
    setError(null)
    try {
      await llamar((token) => api.enviarEnsayo(token, id))
      try {
        localStorage.removeItem(`marcadas-${id}`)
        localStorage.removeItem(`tachadas-${id}`)
      } catch {
        /* sin almacenamiento local */
      }
      navigate(`/ensayos/${id}/resultado`)
    } catch (e) {
      enviadoRef.current = false
      if (e instanceof ApiError && e.status === 409) {
        navigate(`/ensayos/${id}/resultado`)
        return
      }
      setError('No se pudo entregar el ensayo. Revisá tu conexión e intentá de nuevo.')
      setEnviando(false)
    }
  }, [id, llamar, navigate])

  const restanteSeg = limiteMs ? Math.round((limiteMs - ahora) / 1000) : null
  useEffect(() => {
    if (restanteSeg !== null && restanteSeg <= 0) enviar()
  }, [restanteSeg, enviar])

  const guardarRespuesta = useCallback(
    async (ensayoItemId, etiqueta) => {
      setRespuestas((actuales) => ({ ...actuales, [ensayoItemId]: etiqueta }))
      guardadosEnVuelo.current.get(ensayoItemId)?.abort()
      const control = new AbortController()
      guardadosEnVuelo.current.set(ensayoItemId, control)
      try {
        await llamar((token) =>
          api.guardarRespuestas(token, id, { respuestas: [{ ensayo_item_id: ensayoItemId, respuesta_seleccionada: etiqueta }] }, control.signal),
        )
        setError(null)
      } catch (e) {
        if (e instanceof ApiError && e.codigo === 'CANCELADO') return
        setError('No se pudo guardar la respuesta. Revisá tu conexión.')
      } finally {
        if (guardadosEnVuelo.current.get(ensayoItemId) === control) guardadosEnVuelo.current.delete(ensayoItemId)
      }
    },
    [id, llamar],
  )

  const preguntas = ensayo?.preguntas ?? []
  const pregunta = preguntas[indice]
  const total = preguntas.length
  const esPractica = ensayo?.modo === 'practica'
  const correccion = pregunta ? correcciones[pregunta.ensayo_item_id] : null
  const seleccion = pregunta ? respuestas[pregunta.ensayo_item_id] : null

  const irA = useCallback(
    (i) => {
      setIndice(Math.min(Math.max(i, 0), total - 1))
      setHoja(null)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    [total],
  )

  async function revisar() {
    if (!pregunta || !seleccion) return
    setRevisando(true)
    try {
      guardadosEnVuelo.current.get(pregunta.ensayo_item_id)?.abort()
      await llamar((token) =>
        api.guardarRespuestas(token, id, { respuestas: [{ ensayo_item_id: pregunta.ensayo_item_id, respuesta_seleccionada: seleccion }] }),
      )
      const c = await llamar((token) => api.revelarPregunta(token, id, pregunta.ensayo_item_id))
      setCorrecciones((actuales) => ({ ...actuales, [pregunta.ensayo_item_id]: c }))
    } catch {
      setError('No se pudo revisar la pregunta')
    } finally {
      setRevisando(false)
    }
  }

  function elegir(etiqueta) {
    if (!pregunta || correccion) return
    const ya = tachadas[pregunta.ensayo_item_id] ?? []
    if (ya.includes(etiqueta)) alternarTachada(etiqueta)
    guardarRespuesta(pregunta.ensayo_item_id, etiqueta)
  }

  function alternarTachada(etiqueta) {
    const clave = pregunta.ensayo_item_id
    setTachadas((actuales) => {
      const lista = actuales[clave] ?? []
      const nueva = lista.includes(etiqueta) ? lista.filter((l) => l !== etiqueta) : [...lista, etiqueta]
      return { ...actuales, [clave]: nueva }
    })
  }

  function alternarMarca() {
    const clave = pregunta.ensayo_item_id
    setMarcadas((actuales) => {
      const nueva = { ...actuales }
      if (nueva[clave]) delete nueva[clave]
      else nueva[clave] = true
      return nueva
    })
  }

  useEffect(() => {
    function alTeclear(e) {
      if (hoja || !pregunta || e.target.closest?.('input, textarea')) return
      if (e.key === 'ArrowRight') irA(indice + 1)
      else if (e.key === 'ArrowLeft') irA(indice - 1)
      else {
        const letra = e.key.toUpperCase()
        if (pregunta.alternativas.some((a) => a.etiqueta === letra)) elegir(letra)
      }
    }
    document.addEventListener('keydown', alTeclear)
    return () => document.removeEventListener('keydown', alTeclear)
  })

  if (error && !ensayo) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
          <button className="boton-secundario" type="button" onClick={() => navigate('/')}>
            Volver al inicio
          </button>
        </div>
      </div>
    )
  }

  if (!ensayo || !pregunta) return <p className="cargando">Cargando…</p>

  const respondidas = preguntas.filter((p) => respuestas[p.ensayo_item_id]).length
  const nMarcadas = preguntas.filter((p) => marcadas[p.ensayo_item_id]).length
  const enBlanco = total - respondidas
  const tachadasAqui = tachadas[pregunta.ensayo_item_id] ?? []
  const esUltima = indice === total - 1
  const prueba = datosPrueba(ensayo.nivel)

  function claseCelda(p, i) {
    const c = correcciones[p.ensayo_item_id]
    let clase = 'celda-pregunta'
    if (c) clase += c.es_correcta ? ' correcta' : ' incorrecta'
    else if (respuestas[p.ensayo_item_id]) clase += ' respondida'
    if (marcadas[p.ensayo_item_id]) clase += ' marcada'
    if (i === indice) clase += ' actual'
    return clase
  }

  function claseAlternativa(etiqueta) {
    let clase = 'alternativa'
    if (correccion) {
      if (etiqueta === correccion.respuesta_correcta) clase += ' correcta'
      else if (etiqueta === seleccion) clase += ' incorrecta'
    } else if (etiqueta === seleccion) clase += ' seleccionada'
    if (tachadasAqui.includes(etiqueta)) clase += ' tachada'
    return clase
  }

  const urgente = restanteSeg !== null && restanteSeg <= 600

  return (
    <div className="rendir">
      <header className="rendir-cabecera">
        <div className="rendir-cabecera-fila">
          <button type="button" className="boton-icono" aria-label="Salir del ensayo" onClick={() => navigate('/')}>
            <Icono nombre="cerrar" />
          </button>
          <div className="rendir-cabecera-titulo">
            {restanteSeg !== null ? (
              <span className={'reloj' + (urgente ? ' urgente' : '')} aria-live={urgente ? 'polite' : 'off'}>
                {formatearReloj(restanteSeg)}
              </span>
            ) : (
              <span>{prueba.nombre}</span>
            )}
            <small>
              Pregunta {indice + 1} de {total}
            </small>
          </div>
          <button
            type="button"
            className="boton-icono"
            aria-label="Tamaño del texto"
            onClick={() => setTamTexto((t) => TAMANOS_TEXTO[(TAMANOS_TEXTO.indexOf(t) + 1) % TAMANOS_TEXTO.length])}
          >
            <Icono nombre="letra" />
          </button>
          <button type="button" className="boton-icono" aria-label="Ver todas las preguntas" onClick={() => setHoja('navegador')}>
            <Icono nombre="grilla" />
          </button>
        </div>
        <div className="barra-progreso" aria-hidden="true">
          <div style={{ width: `${(respondidas / total) * 100}%` }} />
        </div>
      </header>

      <div ref={cuerpoRef} className={'rendir-cuerpo' + (pregunta.estimulo ? ' con-estimulo' : '')}>
        {pregunta.estimulo && (
          <Estimulo
            key={`${pregunta.estimulo.id}-${indice}`}
            estimulo={pregunta.estimulo}
            numerar={ensayo.nivel === 'CL'}
            abiertoInicial={indice === 0 || preguntas[indice - 1].estimulo?.id !== pregunta.estimulo.id}
          />
        )}

        <section className="pregunta" aria-labelledby="enunciado">
          <div className="pregunta-meta">
            <span className="badge">{etiquetaEje(pregunta.eje)}</span>
            <button
              type="button"
              className={'boton-icono' + (marcadas[pregunta.ensayo_item_id] ? ' activo' : '')}
              aria-pressed={!!marcadas[pregunta.ensayo_item_id]}
              onClick={alternarMarca}
            >
              <Icono nombre="bandera" relleno={!!marcadas[pregunta.ensayo_item_id]} />
              <span style={{ fontSize: 14 }}>{marcadas[pregunta.ensayo_item_id] ? 'Marcada' : 'Marcar'}</span>
            </button>
          </div>
          <div id="enunciado" className="pregunta-enunciado">
            <Formula texto={pregunta.enunciado} />
          </div>
          {pregunta.imagen_url && <img className="figura-item" src={urlImagen(pregunta.imagen_url)} alt="Figura de la pregunta" />}

          <div className="alternativas" role="radiogroup" aria-labelledby="enunciado">
            {pregunta.alternativas.map((alt) => (
              <div className="alternativa-fila" key={alt.etiqueta}>
                <button
                  type="button"
                  role="radio"
                  aria-checked={seleccion === alt.etiqueta}
                  disabled={!!correccion}
                  className={claseAlternativa(alt.etiqueta)}
                  onClick={() => elegir(alt.etiqueta)}
                >
                  <span className="letra">{alt.etiqueta}</span>
                  <span className="alternativa-texto">
                    <Formula texto={alt.texto} />
                    {alt.imagen_url && <img className="figura-alternativa" src={urlImagen(alt.imagen_url)} alt="" />}
                  </span>
                </button>
                {!correccion && (
                  <button
                    type="button"
                    className={'tachar' + (tachadasAqui.includes(alt.etiqueta) ? ' activo' : '')}
                    aria-label={`${tachadasAqui.includes(alt.etiqueta) ? 'Destachar' : 'Tachar'} alternativa ${alt.etiqueta}`}
                    onClick={() => alternarTachada(alt.etiqueta)}
                  >
                    <Icono nombre="tachar" tam={20} />
                  </button>
                )}
              </div>
            ))}
          </div>

          {correccion && (
            <>
              <p className={'veredicto ' + (correccion.es_correcta ? 'ok' : 'mal')}>
                <Icono nombre={correccion.es_correcta ? 'ok' : 'mal'} />
                {correccion.es_correcta ? '¡Correcta!' : `Incorrecta. La respuesta es la ${correccion.respuesta_correcta}.`}
              </p>
              {correccion.explicacion && (
                <div className="explicacion">
                  <Formula texto={correccion.explicacion} />
                </div>
              )}
            </>
          )}
          {error && <p className="error">{error}</p>}
        </section>
      </div>

      <footer className="rendir-pie">
        <button className="boton-secundario" type="button" disabled={indice === 0} onClick={() => irA(indice - 1)} style={{ flex: '0 0 auto', width: 56 }} aria-label="Anterior">
          <Icono nombre="atras" />
        </button>
        {esPractica && !correccion ? (
          <button className="boton" type="button" disabled={!seleccion || revisando} onClick={revisar}>
            {revisando ? 'Revisando…' : 'Revisar respuesta'}
          </button>
        ) : esUltima ? (
          <button className="boton" type="button" disabled={enviando} onClick={() => setHoja('entregar')}>
            Terminar
          </button>
        ) : (
          <button className="boton" type="button" onClick={() => irA(indice + 1)}>
            Siguiente
          </button>
        )}
        {esPractica && !correccion && !esUltima && (
          <button className="boton-secundario" type="button" onClick={() => irA(indice + 1)} style={{ flex: '0 0 auto', width: 56 }} aria-label="Siguiente">
            <Icono nombre="adelante" />
          </button>
        )}
      </footer>

      {hoja === 'navegador' && (
        <Hoja titulo="Preguntas" onCerrar={() => setHoja(null)}>
          <div className="leyenda">
            <span className="l-resp">Respondida</span>
            <span>Sin responder</span>
            <span className="l-marca">Marcada</span>
          </div>
          <div className="grilla-navegador">
            {preguntas.map((p, i) => (
              <button key={p.ensayo_item_id} type="button" className={claseCelda(p, i)} onClick={() => irA(i)} aria-label={`Ir a la pregunta ${i + 1}`}>
                {i + 1}
              </button>
            ))}
          </div>
          <button className="boton" type="button" onClick={() => setHoja('entregar')}>
            Terminar ensayo
          </button>
        </Hoja>
      )}

      {hoja === 'entregar' && (
        <Hoja titulo="¿Terminar el ensayo?" onCerrar={() => setHoja(null)}>
          <div className="resumen-entrega">
            <div>
              <strong>{respondidas}</strong>
              <span>Respondidas</span>
            </div>
            <div>
              <strong>{nMarcadas}</strong>
              <span>Marcadas</span>
            </div>
            <div>
              <strong>{enBlanco}</strong>
              <span>En blanco</span>
            </div>
          </div>
          {enBlanco > 0 && (
            <p className="aviso">Las preguntas en blanco cuentan como incorrectas. Después de terminar no se pueden cambiar las respuestas.</p>
          )}
          {error && <p className="error">{error}</p>}
          <div style={{ display: 'grid', gap: 10 }}>
            <button className="boton" type="button" disabled={enviando} onClick={enviar}>
              {enviando ? 'Entregando…' : 'Terminar y ver resultado'}
            </button>
            {enBlanco > 0 && (
              <button
                className="boton-secundario"
                type="button"
                onClick={() => irA(preguntas.findIndex((p) => !respuestas[p.ensayo_item_id]))}
              >
                Ir a la primera en blanco
              </button>
            )}
            {nMarcadas > 0 && (
              <button className="boton-secundario" type="button" onClick={() => irA(preguntas.findIndex((p) => marcadas[p.ensayo_item_id]))}>
                Revisar las marcadas
              </button>
            )}
          </div>
        </Hoja>
      )}
    </div>
  )
}

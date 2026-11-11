import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { useAuth } from '../AuthContext.jsx'
import { CANTIDADES, MODOS, datosPrueba, etiquetaEje } from '../constantes.js'
import Hoja from '../components/Hoja.jsx'
import Icono from '../components/Icono.jsx'

function minutosPara(prueba, cantidad) {
  return Math.ceil((cantidad * prueba.minutos_oficiales) / prueba.preguntas_oficiales)
}

function formatearDuracion(min) {
  if (min < 60) return `${min} min`
  const h = Math.floor(min / 60)
  const m = min % 60
  return m ? `${h} h ${m} min` : `${h} h`
}

function ConfigurarPrueba({ prueba, onCerrar }) {
  const { llamar } = useApi()
  const navigate = useNavigate()
  const ejesConStock = prueba.ejes.filter((e) => (prueba.publicadas_por_eje[e] ?? 0) > 0)
  const [ejes, setEjes] = useState(ejesConStock)
  const [modo, setModo] = useState('practica')
  const [cantidad, setCantidad] = useState(10)
  const [electivo, setElectivo] = useState('')
  const esCiencias = prueba.nivel === 'CIENCIAS'
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)

  const ejesEfectivos = esCiencias && electivo ? prueba.ejes : ejes
  const disponibles = ejesEfectivos.reduce((suma, e) => suma + (prueba.publicadas_por_eje[e] ?? 0), 0)
  const cantidades = CANTIDADES.filter((c) => c <= Math.max(disponibles, 5))
  const oficial = prueba.preguntas_oficiales

  useEffect(() => {
    if (cantidad > disponibles && cantidades.length) setCantidad(cantidades[cantidades.length - 1])
  }, [cantidad, disponibles, cantidades])

  function alternarEje(eje) {
    setEjes((actuales) => (actuales.includes(eje) ? actuales.filter((e) => e !== eje) : [...actuales, eje]))
  }

  async function comenzar() {
    setError(null)
    if (ejesEfectivos.length === 0) {
      setError('Elegí al menos un tema')
      return
    }
    setEnviando(true)
    try {
      const cuerpo = { nivel: prueba.nivel, ejes, cantidad, modo }
      if (esCiencias && electivo) {
        cuerpo.electivo = electivo
        cuerpo.ejes = prueba.ejes
      }
      const ensayo = await llamar((token) => api.crearEnsayo(token, cuerpo))
      navigate(`/ensayos/${ensayo.id}`)
    } catch (e) {
      if (e instanceof ApiError && e.codigo === 'STOCK_INSUFICIENTE') {
        setError(
          prueba.usa_estimulos
            ? 'No hay textos suficientes para esa cantidad exacta de preguntas. Probá con otra cantidad.'
            : `Hay solo ${e.extra?.max_disponible ?? 0} preguntas para esos temas. Elegí menos preguntas o más temas.`,
        )
      } else {
        setError(e instanceof ApiError ? e.mensaje || 'No se pudo generar el ensayo' : 'No se pudo conectar con el servidor')
      }
      setEnviando(false)
    }
  }

  const modoActual = MODOS.find((m) => m.valor === modo)

  return (
    <Hoja titulo={prueba.nombre} onCerrar={onCerrar}>
      <span className="etiqueta-campo">Modo</span>
      <div className="segmentos">
        {MODOS.map((m) => (
          <button key={m.valor} type="button" className={'segmento' + (modo === m.valor ? ' activo' : '')} onClick={() => setModo(m.valor)}>
            {m.etiqueta}
          </button>
        ))}
      </div>
      <p className="texto-suave" style={{ fontSize: 14, margin: '8px 0 18px' }}>
        {modoActual.ayuda}
      </p>

      {esCiencias && (
        <>
          <span className="etiqueta-campo">Módulo electivo</span>
          <div className="segmentos" style={{ marginBottom: 6 }}>
            {[['', 'Ninguno'], ['biologia', 'Biología'], ['fisica', 'Física'], ['quimica', 'Química']].map(([v, t]) => (
              <button key={v} type="button" className={'segmento' + (electivo === v ? ' activo' : '')} onClick={() => setElectivo(v)}>
                {t}
              </button>
            ))}
          </div>
          <p className="texto-suave" style={{ fontSize: 14, margin: '0 0 18px' }}>
            {electivo ? 'Como en la PAES: 54 de cada 80 preguntas del módulo común y el resto del electivo.' : 'Elegí los temas libremente.'}
          </p>
        </>
      )}

      {!prueba.usa_estimulos && prueba.ejes.length > 1 && !(esCiencias && electivo) && (
        <>
          <span className="etiqueta-campo">Temas</span>
          <div className="chips" style={{ marginBottom: 18 }}>
            {prueba.ejes.map((e) => {
              const n = prueba.publicadas_por_eje[e] ?? 0
              return (
                <button
                  key={e}
                  type="button"
                  disabled={n === 0}
                  className={'chip' + (ejes.includes(e) ? ' activo' : '')}
                  onClick={() => alternarEje(e)}
                >
                  {etiquetaEje(e)}
                </button>
              )
            })}
          </div>
        </>
      )}

      <span className="etiqueta-campo">Preguntas</span>
      <div className="chips">
        {cantidades.map((c) => (
          <button key={c} type="button" className={'chip' + (cantidad === c ? ' activo' : '')} onClick={() => setCantidad(c)}>
            {c === oficial ? `${c} · completa` : c}
          </button>
        ))}
      </div>

      <p className="resumen-config">
        {modo === 'simulacro'
          ? `Tiempo: ${formatearDuracion(minutosPara(prueba, cantidad))} (proporcional a la prueba oficial de ${oficial} preguntas).`
          : `${disponibles} preguntas disponibles en los temas elegidos.`}
      </p>
      {error && <p className="error">{error}</p>}
      <button className="boton" type="button" disabled={enviando} onClick={comenzar}>
        {enviando ? 'Preparando…' : 'Comenzar'}
      </button>
    </Hoja>
  )
}

export default function ConfigurarEnsayo() {
  const { llamar } = useApi()
  const { usuario } = useAuth()
  const [pruebas, setPruebas] = useState(null)
  const [enCurso, setEnCurso] = useState(null)
  const [elegida, setElegida] = useState(null)
  const [error, setError] = useState(null)
  const cerrar = useCallback(() => setElegida(null), [])

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.listarPruebas(token))
      .then((p) => !cancelado && setPruebas(p))
      .catch(() => !cancelado && setError('No se pudo cargar el catálogo de pruebas'))
    llamar((token) => api.listarEnsayos(token))
      .then((lista) => !cancelado && setEnCurso(lista.find((e) => e.estado === 'en_progreso') ?? null))
      .catch(() => {})
    return () => {
      cancelado = true
    }
  }, [llamar])

  const nombre = (usuario?.nombre ?? '').split(' ')[0]

  return (
    <div className="contenido">
      <div className="saludo">
        <h1>{nombre ? `Hola, ${nombre}` : 'Practicar'}</h1>
        <p>Elegí una prueba para empezar un ensayo.</p>
      </div>

      {enCurso && (
        <Link to={`/ensayos/${enCurso.id}`} className="continuar">
          <div>
            <strong>Continuar ensayo</strong>
            <span>{datosPrueba(enCurso.nivel).nombre} en curso</span>
          </div>
          <Icono nombre="adelante" />
        </Link>
      )}

      {error && <p className="error">{error}</p>}
      {!pruebas && !error && <p className="cargando">Cargando…</p>}

      {pruebas && (
        <div className="grilla-pruebas">
          {pruebas.map((p) => {
            const d = datosPrueba(p.nivel)
            const total = Object.values(p.publicadas_por_eje).reduce((a, b) => a + b, 0)
            return (
              <button key={p.nivel} type="button" className="tarjeta-prueba" disabled={total === 0} onClick={() => setElegida(p)}>
                <span className="icono-prueba" style={{ background: d.color }}>
                  {d.sigla}
                </span>
                <span className="tarjeta-prueba-texto">
                  <strong>{p.nombre}</strong>
                  <span>{total > 0 ? `${total.toLocaleString('es-CL')} preguntas` : 'Próximamente'}</span>
                </span>
              </button>
            )
          })}
        </div>
      )}

      {elegida && <ConfigurarPrueba prueba={elegida} onCerrar={cerrar} />}
    </div>
  )
}

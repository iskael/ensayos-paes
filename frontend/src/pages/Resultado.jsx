import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api, urlImagen } from '../api.js'
import { useApi } from '../useApi.js'
import { etiquetaEje } from '../constantes.js'
import Formula from '../components/Formula.jsx'
import Estimulo from '../components/Estimulo.jsx'

const FILTROS = [
  { valor: 'todas', etiqueta: 'Todas' },
  { valor: 'incorrectas', etiqueta: 'Incorrectas' },
  { valor: 'correctas', etiqueta: 'Correctas' },
]

function Anillo({ valor, max = 1000, tam = 132 }) {
  const r = 54
  const c = 2 * Math.PI * r
  const proporcion = Math.max(0, Math.min(1, valor / max))
  return (
    <svg className="anillo" width={tam} height={tam} viewBox="0 0 132 132" role="img" aria-label={`Puntaje ${valor} de ${max}`}>
      <circle cx="66" cy="66" r={r} fill="none" stroke="var(--color-fondo-suave)" strokeWidth="12" />
      {proporcion > 0 && <circle
        cx="66"
        cy="66"
        r={r}
        fill="none"
        stroke="var(--color-primario)"
        strokeWidth="12"
        strokeLinecap="round"
        strokeDasharray={`${c * proporcion} ${c}`}
        transform="rotate(-90 66 66)"
      />}
      <text x="66" y="66" textAnchor="middle" fontSize="30" fontWeight="800">
        {valor}
      </text>
      <text x="66" y="88" textAnchor="middle" fontSize="12" style={{ fill: 'var(--color-texto-suave)' }}>
        de {max}
      </text>
    </svg>
  )
}

function ItemRevision({ item }) {
  const [abierto, setAbierto] = useState(false)
  const estado = !item.respuesta_seleccionada ? 'blanco' : item.es_correcta ? 'ok' : 'mal'
  const simbolo = { ok: '✓', mal: '✕', blanco: '–' }[estado]

  function clase(etiqueta) {
    if (etiqueta === item.respuesta_correcta) return 'alternativa correcta'
    if (etiqueta === item.respuesta_seleccionada) return 'alternativa incorrecta'
    return 'alternativa'
  }

  return (
    <div className="revision-item">
      <button type="button" className="revision-cabecera" aria-expanded={abierto} onClick={() => setAbierto((a) => !a)}>
        <span className={'punto-estado ' + estado}>{simbolo}</span>
        <span className="resumen-enunciado">
          <strong>{item.orden}.</strong> <Formula texto={item.enunciado} />
        </span>
      </button>
      {abierto && (
        <div className="revision-cuerpo">
          {item.estimulo && <Estimulo estimulo={item.estimulo} abiertoInicial={false} />}
          <span className="badge">{etiquetaEje(item.eje)}</span>
          <div className="pregunta-enunciado" style={{ marginTop: 10 }}>
            <Formula texto={item.enunciado} />
          </div>
          {item.imagen_url && <img className="figura-item" src={urlImagen(item.imagen_url)} alt="Figura de la pregunta" />}
          <div className="alternativas">
            {item.alternativas.map((a) => (
              <div key={a.etiqueta} className={clase(a.etiqueta)}>
                <span className="letra">{a.etiqueta}</span>
                <span className="alternativa-texto">
                  <Formula texto={a.texto} />
                  {a.etiqueta === item.respuesta_seleccionada && (
                    <span className="texto-suave" style={{ display: 'block', fontSize: 13 }}>
                      Tu respuesta
                    </span>
                  )}
                </span>
              </div>
            ))}
          </div>
          {!item.respuesta_seleccionada && <p className="texto-suave">No respondiste esta pregunta.</p>}
          {item.explicacion && (
            <div className="explicacion">
              <Formula texto={item.explicacion} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function Resultado() {
  const { id } = useParams()
  const { llamar } = useApi()
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState(null)
  const [filtro, setFiltro] = useState('todas')

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.obtenerResultado(token, id))
      .then((r) => !cancelado && setResultado(r))
      .catch(() => !cancelado && setError('No se pudo cargar el resultado'))
    return () => {
      cancelado = true
    }
  }, [id, llamar])

  if (error) {
    return (
      <div className="contenido">
        <p className="error">{error}</p>
      </div>
    )
  }
  if (!resultado) return <p className="cargando">Cargando…</p>

  const items = resultado.revision.filter((it) =>
    filtro === 'todas' ? true : filtro === 'correctas' ? it.es_correcta : !it.es_correcta,
  )

  return (
    <div className="contenido">
      <div className="panel resultado-cabecera">
        <Anillo valor={resultado.puntaje} />
        <div>
          <h1 style={{ marginBottom: 4 }}>Resultado</h1>
          <p className="texto-suave" style={{ margin: 0 }}>
            {resultado.correctas} de {resultado.total} correctas
          </p>
          <Link to="/" className="boton-fantasma" style={{ padding: 0, minHeight: 40, marginTop: 6 }}>
            Practicar otra vez
          </Link>
        </div>
      </div>

      <div className="panel">
        <h2 style={{ marginTop: 0 }}>Por tema</h2>
        {resultado.desglose_por_eje.map((d) => (
          <div className="barra-eje" key={d.eje}>
            <div className="barra-eje-fila">
              <span>{etiquetaEje(d.eje)}</span>
              <span className="texto-suave">
                {d.correctas}/{d.total}
              </span>
            </div>
            <div className="barra-eje-fondo">
              <div style={{ width: `${d.total ? (d.correctas / d.total) * 100 : 0}%` }} />
            </div>
          </div>
        ))}
      </div>

      <h2>Revisión</h2>
      <div className="segmentos" style={{ marginBottom: 14 }}>
        {FILTROS.map((f) => (
          <button key={f.valor} type="button" className={'segmento' + (filtro === f.valor ? ' activo' : '')} onClick={() => setFiltro(f.valor)}>
            {f.etiqueta}
          </button>
        ))}
      </div>
      {items.length === 0 && <p className="vacio">No hay preguntas en este filtro.</p>}
      {items.map((item) => (
        <ItemRevision key={item.orden} item={item} />
      ))}
    </div>
  )
}

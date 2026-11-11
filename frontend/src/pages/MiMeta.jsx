import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import carreras from '../carreras-medicina-2027.json'

const CLAVE = 'mi-meta'
const PRUEBAS_META = [
  { clave: 'cl', nivel: 'CL', nombre: 'Competencia Lectora' },
  { clave: 'm1', nivel: 'M1', nombre: 'Matemática 1' },
  { clave: 'ciencias', nivel: 'CIENCIAS', nombre: 'Ciencias' },
  { clave: 'hcs', nivel: 'HCS', nombre: 'Historia' },
]

function leer() {
  try {
    return JSON.parse(localStorage.getItem(CLAVE)) ?? {}
  } catch {
    return {}
  }
}

function guardar(v) {
  try {
    localStorage.setItem(CLAVE, JSON.stringify(v))
  } catch {
    /* sin almacenamiento local */
  }
}

function ponderado(c, p) {
  const electiva = c.historia_o_ciencias ? Math.max(p.ciencias ?? 0, p.hcs ?? 0) : p.ciencias ?? 0
  const pesoElectiva = c.historia_o_ciencias ? Math.max(c.ciencias, c.hcs) : c.ciencias
  return (c.nem * (p.nem ?? 0) + c.ranking * (p.ranking ?? 0) + c.cl * (p.cl ?? 0) + c.m1 * (p.m1 ?? 0) + pesoElectiva * electiva) / 100
}

function promedioUltimos(ensayos, nivel) {
  const notas = ensayos
    .filter((e) => e.nivel === nivel && e.estado === 'finalizado' && typeof e.puntaje === 'number')
    .slice(0, 3)
    .map((e) => e.puntaje)
  if (!notas.length) return null
  return Math.round(notas.reduce((a, b) => a + b, 0) / notas.length)
}

function CampoPuntaje({ etiqueta, ayuda, valor, onCambiar }) {
  return (
    <div className="campo" style={{ marginBottom: 12 }}>
      <label>
        {etiqueta}
        {ayuda && <span style={{ fontWeight: 400 }}> · {ayuda}</span>}
      </label>
      <input
        type="number"
        inputMode="numeric"
        min="100"
        max="1000"
        placeholder="100 a 1000"
        value={valor ?? ''}
        onChange={(e) => onCambiar(e.target.value === '' ? null : Math.max(0, Math.min(1000, Number(e.target.value))))}
      />
    </div>
  )
}

export default function MiMeta() {
  const { llamar } = useApi()
  const [datos, setDatos] = useState(leer)
  const [ensayos, setEnsayos] = useState(null)
  const [busqueda, setBusqueda] = useState('')

  useEffect(() => {
    llamar((token) => api.listarEnsayos(token))
      .then(setEnsayos)
      .catch(() => setEnsayos([]))
  }, [llamar])

  useEffect(() => guardar(datos), [datos])

  const sugeridos = useMemo(() => {
    const s = {}
    for (const p of PRUEBAS_META) s[p.clave] = ensayos ? promedioUltimos(ensayos, p.nivel) : null
    return s
  }, [ensayos])

  const puntajes = { ...datos }
  for (const p of PRUEBAS_META) if (puntajes[p.clave] == null) puntajes[p.clave] = sugeridos[p.clave]

  const completo = ['nem', 'ranking', 'cl', 'm1', 'ciencias'].every((k) => puntajes[k] != null)
  const filtro = busqueda.trim().toLowerCase()
  const lista = carreras
    .map((c) => ({ ...c, ponderado: ponderado(c, puntajes) }))
    .filter((c) => !filtro || `${c.universidad} ${c.sede}`.toLowerCase().includes(filtro))
    .sort((a, b) => (b.ponderado - (b.corte_2026 ?? 0)) - (a.ponderado - (a.corte_2026 ?? 0)))
  const alcanzables = lista.filter((c) => c.corte_2026 && c.ponderado >= c.corte_2026).length

  function cambiar(clave, valor) {
    setDatos((d) => ({ ...d, [clave]: valor }))
  }

  return (
    <div className="contenido">
      <h1>Mi meta: Medicina</h1>
      <p className="texto-suave" style={{ marginTop: -4 }}>
        Tu puntaje ponderado estimado frente al corte 2026 de cada programa de Medicina, con las ponderaciones oficiales de la admisión 2027.
      </p>

      <div className="panel">
        <h2 style={{ marginTop: 0 }}>Tus puntajes</h2>
        <CampoPuntaje etiqueta="NEM" ayuda="puntaje de notas" valor={datos.nem} onCambiar={(v) => cambiar('nem', v)} />
        <CampoPuntaje etiqueta="Ranking" valor={datos.ranking} onCambiar={(v) => cambiar('ranking', v)} />
        {PRUEBAS_META.map((p) => (
          <CampoPuntaje
            key={p.clave}
            etiqueta={p.nombre}
            ayuda={datos[p.clave] == null && sugeridos[p.clave] != null ? `promedio de tus últimos ensayos: ${sugeridos[p.clave]}` : p.clave === 'hcs' ? 'opcional' : null}
            valor={datos[p.clave] ?? sugeridos[p.clave]}
            onCambiar={(v) => cambiar(p.clave, v)}
          />
        ))}
        <p className="texto-suave" style={{ fontSize: 13, margin: 0 }}>
          Los puntajes de los ensayos se calculan como porcentaje de logro sobre 1000 y no equivalen exactamente a la escala PAES; usalos como referencia. Tus datos quedan solo en este dispositivo.
        </p>
      </div>

      {!completo ? (
        <div className="aviso">
          Completá NEM, Ranking, Lectora, Matemática 1 y Ciencias para ver tu ponderado. ¿Te falta algún puntaje? <Link to="/">Rendí un ensayo</Link>.
        </div>
      ) : (
        <div className="aviso">
          Con estos puntajes superarías el corte 2026 en <strong>{alcanzables}</strong> de {lista.filter((c) => c.corte_2026).length} programas.
        </div>
      )}

      <div className="campo">
        <input type="text" placeholder="Buscar universidad o ciudad" value={busqueda} onChange={(e) => setBusqueda(e.target.value)} />
      </div>

      {lista.map((c) => {
        const dif = c.corte_2026 ? c.ponderado - c.corte_2026 : null
        return (
          <div className="panel" key={c.codigo} style={{ padding: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10 }}>
              <div style={{ minWidth: 0 }}>
                <strong>{c.universidad}</strong>
                <div className="texto-suave" style={{ fontSize: 14 }}>
                  {c.sede || '—'} · Lectora {c.cl} % · M1 {c.m1} % · Ciencias {c.ciencias} %{c.historia_o_ciencias ? ' (o Historia)' : ''}
                </div>
              </div>
              <div style={{ textAlign: 'right', flex: '0 0 auto' }}>
                <div style={{ fontWeight: 800, fontSize: 18 }}>{completo ? c.ponderado.toFixed(1) : '—'}</div>
                <div className="texto-suave" style={{ fontSize: 12 }}>corte {c.corte_2026 ? c.corte_2026.toFixed(1) : 'nuevo'}</div>
              </div>
            </div>
            {completo && dif !== null && (
              <div style={{ marginTop: 8, fontSize: 14, fontWeight: 650, color: dif >= 0 ? 'var(--color-ok)' : 'var(--color-error)' }}>
                {dif >= 0 ? `${dif.toFixed(1)} puntos sobre el corte` : `Te faltan ${(-dif).toFixed(1)} puntos`}
              </div>
            )}
          </div>
        )
      })}
      <p className="texto-suave" style={{ fontSize: 13 }}>
        Fuente: DEMRE, oferta definitiva de carreras admisión 2027 (ponderaciones); cortes 2026 del último seleccionado según Filadd. Confirmá siempre en la ficha oficial de cada carrera.
      </p>
    </div>
  )
}

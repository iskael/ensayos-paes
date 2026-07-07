import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { NIVELES, CANTIDADES, EJES } from '../constantes.js'

export default function ConfigurarEnsayo() {
  const [nivel, setNivel] = useState(NIVELES[0])
  const [ejesElegidos, setEjesElegidos] = useState([])
  const [cantidad, setCantidad] = useState(CANTIDADES[0])
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const { llamar } = useApi()
  const navigate = useNavigate()

  function alternarEje(valor) {
    setEjesElegidos((actuales) =>
      actuales.includes(valor) ? actuales.filter((e) => e !== valor) : [...actuales, valor],
    )
  }

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    if (ejesElegidos.length === 0) {
      setError('Elegí al menos un eje')
      return
    }
    setEnviando(true)
    try {
      const ensayo = await llamar((token) =>
        api.crearEnsayo(token, { nivel, ejes: ejesElegidos, cantidad }),
      )
      navigate(`/ensayos/${ensayo.id}`)
    } catch (e) {
      if (e instanceof ApiError && e.codigo === 'STOCK_INSUFICIENTE') {
        setError(`No hay suficientes preguntas disponibles (máximo ${e.extra?.max_disponible ?? 0}). Elegí menos cantidad o más ejes.`)
      } else if (e instanceof ApiError) {
        setError(e.mensaje || 'No se pudo generar el ensayo')
      } else {
        setError('No se pudo conectar con el servidor')
      }
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Configurar ensayo</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="nivel">Nivel</label>
            <select id="nivel" value={nivel} onChange={(e) => setNivel(e.target.value)}>
              {NIVELES.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label>Ejes</label>
            {EJES.map((eje) => (
              <label key={eje.valor} style={{ display: 'block', marginBottom: 6 }}>
                <input
                  type="checkbox"
                  checked={ejesElegidos.includes(eje.valor)}
                  onChange={() => alternarEje(eje.valor)}
                />{' '}
                {eje.etiqueta}
              </label>
            ))}
          </div>
          <div className="campo">
            <label htmlFor="cantidad">Cantidad de preguntas</label>
            <select id="cantidad" value={cantidad} onChange={(e) => setCantidad(Number(e.target.value))}>
              {CANTIDADES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Generando…' : 'Comenzar ensayo'}
          </button>
        </form>
      </div>
    </div>
  )
}

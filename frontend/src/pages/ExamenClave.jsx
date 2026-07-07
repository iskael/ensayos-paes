import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES, DIFICULTADES } from '../constantes.js'

export default function ExamenClave() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { llamar } = useApi()
  const [items, setItems] = useState(null)
  const [pesos, setPesos] = useState({})
  const [error, setError] = useState(null)
  const [guardando, setGuardando] = useState(false)
  const [mensajeGuardado, setMensajeGuardado] = useState(null)

  const [archivoPdf, setArchivoPdf] = useState(null)
  const [ejePdf, setEjePdf] = useState(EJES[0].valor)
  const [dificultadPdf, setDificultadPdf] = useState(DIFICULTADES[0].valor)
  const [importando, setImportando] = useState(false)
  const [errorPdf, setErrorPdf] = useState(null)

  const cargar = useCallback(() => {
    setError(null)
    Promise.all([
      llamar((token) => api.listarItems(token, { examenId: id, limit: 200 })),
      llamar((token) => api.obtenerClave(token, id)),
    ])
      .then(([listaItems, clave]) => {
        setItems(listaItems)
        const iniciales = {}
        for (const it of listaItems) iniciales[it.id] = it.peso ?? 0
        for (const p of clave.pesos) iniciales[p.item_id] = p.peso
        setPesos(iniciales)
      })
      .catch(() => setError('No se pudo cargar la clave'))
  }, [llamar, id])

  useEffect(() => {
    cargar()
  }, [cargar])

  const suma = Object.values(pesos).reduce((acc, p) => acc + Number(p || 0), 0)

  function cambiarPeso(itemId, valor) {
    setPesos((p) => ({ ...p, [itemId]: valor }))
  }

  async function guardarClave() {
    setGuardando(true)
    setError(null)
    setMensajeGuardado(null)
    try {
      const cuerpo = Object.entries(pesos).map(([itemId, peso]) => ({ item_id: itemId, peso: Number(peso) }))
      await llamar((token) => api.definirClave(token, id, cuerpo))
      setMensajeGuardado('Clave guardada')
    } catch (err) {
      setError(err.mensaje || 'No se pudo guardar la clave')
    } finally {
      setGuardando(false)
    }
  }

  async function importarPdf(evento) {
    evento.preventDefault()
    if (!archivoPdf) return
    setImportando(true)
    setErrorPdf(null)
    try {
      const datos = new FormData()
      datos.append('archivo', archivoPdf)
      datos.append('eje', ejePdf)
      datos.append('dificultad', dificultadPdf)
      await llamar((token) => api.importarPdf(token, id, datos))
      navigate(`/banco/items?examenId=${id}&estado=borrador`)
    } catch (err) {
      setErrorPdf(err.mensaje || 'No se pudo importar el PDF')
    } finally {
      setImportando(false)
    }
  }

  if (error && !items) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!items) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Clave del examen</h1>

        {items.length === 0 ? (
          <p>Este examen todavía no tiene ítems asociados.</p>
        ) : (
          <>
            <table className="banco-tabla">
              <thead>
                <tr>
                  <th>Enunciado</th>
                  <th>Estado</th>
                  <th>Peso</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it) => (
                  <tr key={it.id}>
                    <td>
                      {it.enunciado.slice(0, 50)}
                      {it.enunciado.length > 50 ? '…' : ''}
                    </td>
                    <td>{it.estado}</td>
                    <td>
                      <input
                        type="number"
                        min="0"
                        style={{ width: 80, minHeight: 36 }}
                        value={pesos[it.id] ?? 0}
                        onChange={(e) => cambiarPeso(it.id, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className={suma === 1000 ? 'clave-suma-valida' : 'clave-suma-invalida'}>Suma de pesos: {suma} / 1000</p>
            {error && <p className="error">{error}</p>}
            {mensajeGuardado && <p>{mensajeGuardado}</p>}
            <button
              className="boton"
              type="button"
              disabled={guardando}
              style={{ width: 'auto', padding: '0 16px' }}
              onClick={guardarClave}
            >
              {guardando ? 'Guardando…' : 'Guardar clave'}
            </button>
          </>
        )}

        <h2>Importar preguntas desde PDF</h2>
        <form onSubmit={importarPdf}>
          <div className="campo">
            <label htmlFor="archivo-pdf">Archivo PDF</label>
            <input
              id="archivo-pdf"
              type="file"
              accept="application/pdf"
              onChange={(e) => setArchivoPdf(e.target.files[0] ?? null)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="eje-pdf">Eje por defecto</label>
            <select id="eje-pdf" value={ejePdf} onChange={(e) => setEjePdf(e.target.value)}>
              {EJES.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="dificultad-pdf">Dificultad por defecto</label>
            <select id="dificultad-pdf" value={dificultadPdf} onChange={(e) => setDificultadPdf(e.target.value)}>
              {DIFICULTADES.map((d) => (
                <option key={d.valor} value={d.valor}>
                  {d.etiqueta}
                </option>
              ))}
            </select>
          </div>
          {errorPdf && <p className="error">{errorPdf}</p>}
          <button className="boton" type="submit" disabled={importando} style={{ width: 'auto', padding: '0 16px' }}>
            {importando ? 'Importando…' : 'Importar'}
          </button>
        </form>
      </div>
    </div>
  )
}

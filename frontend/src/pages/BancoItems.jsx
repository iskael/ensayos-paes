import { useState, useEffect, useCallback } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES, NIVELES, DIFICULTADES, ESTADOS_ITEM, etiquetaEje } from '../constantes.js'

const TAMANO_PAGINA = 20

export default function BancoItems() {
  const { llamar } = useApi()
  const [searchParams, setSearchParams] = useSearchParams()
  const [items, setItems] = useState(null)
  const [error, setError] = useState(null)
  const [accionError, setAccionError] = useState(null)
  const [pagina, setPagina] = useState(0)

  const nivel = searchParams.get('nivel') ?? ''
  const eje = searchParams.get('eje') ?? ''
  const dificultad = searchParams.get('dificultad') ?? ''
  const estado = searchParams.get('estado') ?? ''
  const examenId = searchParams.get('examenId') ?? ''

  const cargar = useCallback(() => {
    setError(null)
    llamar((token) =>
      api.listarItems(token, {
        nivel: nivel || undefined,
        eje: eje || undefined,
        dificultad: dificultad || undefined,
        estado: estado || undefined,
        examenId: examenId || undefined,
        limit: TAMANO_PAGINA,
        offset: pagina * TAMANO_PAGINA,
      }),
    )
      .then(setItems)
      .catch(() => setError('No se pudieron cargar los ítems'))
  }, [llamar, nivel, eje, dificultad, estado, examenId, pagina])

  useEffect(() => {
    cargar()
  }, [cargar])

  function actualizarFiltro(clave, valor) {
    setPagina(0)
    const nuevos = new URLSearchParams(searchParams)
    if (valor) nuevos.set(clave, valor)
    else nuevos.delete(clave)
    setSearchParams(nuevos)
  }

  async function publicar(id) {
    setAccionError(null)
    try {
      await llamar((token) => api.publicarItem(token, id))
      cargar()
    } catch (err) {
      setAccionError(err.mensaje || 'No se pudo publicar el ítem')
    }
  }

  async function ocultar(id) {
    setAccionError(null)
    try {
      await llamar((token) => api.ocultarItem(token, id))
      cargar()
    } catch (err) {
      setAccionError(err.mensaje || 'No se pudo ocultar el ítem')
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Ítems</h1>
        <Link
          to="/banco/items/nuevo"
          className="boton"
          style={{ display: 'inline-block', width: 'auto', padding: '0 16px', textDecoration: 'none' }}
        >
          Nuevo ítem
        </Link>

        {examenId && (
          <p>
            Filtrando por examen.{' '}
            <button type="button" className="boton-enlace" onClick={() => actualizarFiltro('examenId', '')}>
              Quitar filtro
            </button>
          </p>
        )}

        <div className="banco-filtros">
          <select value={nivel} onChange={(e) => actualizarFiltro('nivel', e.target.value)}>
            <option value="">Nivel: todos</option>
            {NIVELES.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
          <select value={eje} onChange={(e) => actualizarFiltro('eje', e.target.value)}>
            <option value="">Eje: todos</option>
            {EJES.map((e) => (
              <option key={e.valor} value={e.valor}>
                {e.etiqueta}
              </option>
            ))}
          </select>
          <select value={dificultad} onChange={(e) => actualizarFiltro('dificultad', e.target.value)}>
            <option value="">Dificultad: todas</option>
            {DIFICULTADES.map((d) => (
              <option key={d.valor} value={d.valor}>
                {d.etiqueta}
              </option>
            ))}
          </select>
          <select value={estado} onChange={(e) => actualizarFiltro('estado', e.target.value)}>
            <option value="">Estado: todos</option>
            {ESTADOS_ITEM.map((e) => (
              <option key={e.valor} value={e.valor}>
                {e.etiqueta}
              </option>
            ))}
          </select>
        </div>

        {accionError && <p className="error">{accionError}</p>}
        {error && <p className="error">{error}</p>}

        {!items ? (
          <p>Cargando…</p>
        ) : items.length === 0 ? (
          <p>No hay ítems con estos filtros.</p>
        ) : (
          <table className="banco-tabla">
            <thead>
              <tr>
                <th>Enunciado</th>
                <th>Eje</th>
                <th>Estado</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {items.map((it) => (
                <tr key={it.id}>
                  <td>
                    {it.enunciado.slice(0, 60)}
                    {it.enunciado.length > 60 ? '…' : ''}
                  </td>
                  <td>{etiquetaEje(it.eje)}</td>
                  <td>
                    <span className="badge-estado-item">{it.estado}</span>
                  </td>
                  <td>
                    <Link to={`/banco/items/${it.id}`}>Editar</Link>
                    {' · '}
                    {it.estado === 'publicado' ? (
                      <button type="button" className="boton-enlace" onClick={() => ocultar(it.id)}>
                        Ocultar
                      </button>
                    ) : (
                      <button type="button" className="boton-enlace" onClick={() => publicar(it.id)}>
                        Publicar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <button
            className="boton-secundario"
            type="button"
            style={{ width: 'auto', padding: '0 16px' }}
            disabled={pagina === 0}
            onClick={() => setPagina((p) => p - 1)}
          >
            Anterior
          </button>
          <button
            className="boton-secundario"
            type="button"
            style={{ width: 'auto', padding: '0 16px' }}
            disabled={!items || items.length < TAMANO_PAGINA}
            onClick={() => setPagina((p) => p + 1)}
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  )
}

import { useState, useEffect, useCallback } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { PRUEBAS, datosPrueba } from '../constantes.js'

const TAMANO_PAGINA = 20

export default function BancoEstimulos() {
  const { llamar } = useApi()
  const [searchParams, setSearchParams] = useSearchParams()
  const [lista, setLista] = useState(null)
  const [error, setError] = useState(null)
  const [pagina, setPagina] = useState(0)
  const nivel = searchParams.get('nivel') ?? 'CL'
  const buscar = searchParams.get('buscar') ?? ''
  const [busqueda, setBusqueda] = useState(buscar)

  const cargar = useCallback(() => {
    setError(null)
    llamar((token) =>
      api.listarEstimulos(token, { nivel: nivel || undefined, buscar: buscar || undefined, limit: TAMANO_PAGINA, offset: pagina * TAMANO_PAGINA }),
    )
      .then(setLista)
      .catch(() => setError('No se pudieron cargar los textos'))
  }, [llamar, nivel, buscar, pagina])

  useEffect(() => {
    cargar()
  }, [cargar])

  function actualizarFiltro(clave, valor) {
    setPagina(0)
    const nuevos = new URLSearchParams(searchParams)
    nuevos.set(clave, valor)
    if (!valor && clave === 'buscar') nuevos.delete(clave)
    setSearchParams(nuevos)
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <div className="cabecera-banco">
          <h1>Textos</h1>
          <Link to={`/banco/textos/nuevo?nivel=${nivel}`} className="boton boton-auto">
            Nuevo texto
          </Link>
        </div>
        <p className="texto-suave">
          Los textos que comparten varias preguntas, como los de Competencia Lectora. Al editar uno, el cambio se ve en todas
          sus preguntas.
        </p>

        <div className="banco-filtros">
          <select value={nivel} onChange={(e) => actualizarFiltro('nivel', e.target.value)} aria-label="Prueba">
            <option value="">Prueba: todas</option>
            {PRUEBAS.map((p) => (
              <option key={p.nivel} value={p.nivel}>
                {p.nombre}
              </option>
            ))}
          </select>
          <form
            onSubmit={(e) => {
              e.preventDefault()
              actualizarFiltro('buscar', busqueda.trim())
            }}
            style={{ display: 'flex', gap: 8, flex: 1 }}
          >
            <input type="search" placeholder="Buscar por título o contenido" value={busqueda} onChange={(e) => setBusqueda(e.target.value)} />
          </form>
        </div>

        {error && <p className="error">{error}</p>}
        {!lista ? (
          <p>Cargando…</p>
        ) : lista.length === 0 ? (
          <p>No hay textos con estos filtros.</p>
        ) : (
          <ul className="lista-textos">
            {lista.map((e) => (
              <li key={e.id}>
                <Link to={`/banco/textos/${e.id}`} className="fila-texto">
                  <span className="fila-texto-titulo">{e.titulo ?? e.texto.slice(0, 60)}</span>
                  <span className="texto-suave">
                    {e.nivel ? datosPrueba(e.nivel).sigla : 'Sin prueba'} · {e.cantidad_publicados} de {e.cantidad_items}{' '}
                    {e.cantidad_items === 1 ? 'pregunta publicada' : 'preguntas publicadas'}
                    {e.fecha_edicion ? ' · editado' : ''}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}

        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <button className="boton-secundario boton-auto" type="button" disabled={pagina === 0} onClick={() => setPagina((p) => p - 1)}>
            Anterior
          </button>
          <button
            className="boton-secundario boton-auto"
            type="button"
            disabled={!lista || lista.length < TAMANO_PAGINA}
            onClick={() => setPagina((p) => p + 1)}
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  )
}

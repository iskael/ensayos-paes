import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'

export default function BancoExamenes() {
  const { llamar } = useApi()
  const [examenes, setExamenes] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.listarExamenes(token))
      .then((lista) => {
        if (!cancelado) setExamenes(lista)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudieron cargar los exámenes')
      })
    return () => {
      cancelado = true
    }
  }, [llamar])

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!examenes) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Exámenes fuente</h1>
        <Link
          to="/banco/examenes/nuevo"
          className="boton"
          style={{ display: 'inline-block', width: 'auto', padding: '0 16px', textDecoration: 'none' }}
        >
          Nuevo examen
        </Link>

        {examenes.length === 0 ? (
          <p>Todavía no hay exámenes registrados.</p>
        ) : (
          <table className="banco-tabla">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Nivel</th>
                <th>Año</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {examenes.map((ex) => (
                <tr key={ex.id}>
                  <td>{ex.nombre}</td>
                  <td>{ex.tipo}</td>
                  <td>{ex.nivel}</td>
                  <td>{ex.anio_admision}</td>
                  <td>
                    <Link to={`/banco/examenes/${ex.id}`}>Editar</Link>
                    {' · '}
                    <Link to={`/banco/examenes/${ex.id}/clave`}>Clave</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

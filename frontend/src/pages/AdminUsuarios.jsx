import { useState, useEffect, useCallback } from 'react'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { useAuth } from '../AuthContext.jsx'
import { ETIQUETA_ROL, ROLES_ASIGNABLES } from '../constantes.js'

export default function AdminUsuarios() {
  const { llamar } = useApi()
  const { usuario } = useAuth()
  const [buscar, setBuscar] = useState('')
  const [consulta, setConsulta] = useState('')
  const [lista, setLista] = useState(null)
  const [error, setError] = useState(null)
  const [aviso, setAviso] = useState(null)

  const cargar = useCallback(() => {
    llamar((t) => api.listarUsuarios(t, consulta))
      .then(setLista)
      .catch(() => setError('No se pudo cargar los usuarios'))
  }, [llamar, consulta])

  useEffect(() => {
    cargar()
  }, [cargar])

  async function cambiar(u, rol) {
    setError(null)
    setAviso(null)
    try {
      await llamar((t) => api.cambiarRol(t, u.id, rol))
      setAviso(`${u.nombre} ahora es ${ETIQUETA_ROL[rol]}. Verá el cambio al volver a iniciar sesión.`)
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje : 'No se pudo cambiar el rol')
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Usuarios</h1>
        <p className="texto-suave">
          Aquí asignas el rol <strong>Editor</strong> (edita el banco de preguntas y textos, sin acceso a usuarios) o corriges el rol de
          una cuenta. Los administradores se crean desde el servidor.
        </p>
        <form
          className="banco-filtros"
          onSubmit={(e) => {
            e.preventDefault()
            setConsulta(buscar.trim())
          }}
        >
          <input type="search" placeholder="Buscar por nombre o email" value={buscar} onChange={(e) => setBuscar(e.target.value)} />
        </form>
        {error && <p className="error">{error}</p>}
        {aviso && <p className="aviso-ok">{aviso}</p>}
        {!lista ? (
          <p>Cargando…</p>
        ) : (
          <ul className="lista-textos">
            {lista.map((u) => (
              <li key={u.id} className="fila-texto fila-con-accion">
                <span>
                  <span className="fila-texto-titulo">{u.nombre}</span>
                  <br />
                  <span className="texto-suave">{u.email}</span>
                </span>
                {u.rol === 'admin' || u.id === usuario?.id ? (
                  <span className="badge-rol">{ETIQUETA_ROL[u.rol] ?? u.rol}</span>
                ) : (
                  <select aria-label={`Rol de ${u.nombre}`} value={u.rol} onChange={(e) => cambiar(u, e.target.value)}>
                    {ROLES_ASIGNABLES.map((r) => (
                      <option key={r} value={r}>
                        {ETIQUETA_ROL[r]}
                      </option>
                    ))}
                  </select>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'

export default function Registro() {
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rol, setRol] = useState('estudiante')
  const [aceptaTerminos, setAceptaTerminos] = useState(false)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [registrado, setRegistrado] = useState(false)

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      await api.registrar({
        nombre,
        email,
        password,
        rol,
        acepta_terminos: aceptaTerminos,
      })
      setRegistrado(true)
    } catch (e) {
      setError(e instanceof ApiError ? e.mensaje || 'No se pudo registrar' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  if (registrado) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>Revisá tu correo</h1>
          <p>
            Te registraste correctamente. Te enviamos un correo a <strong>{email}</strong> para
            confirmar tu cuenta — hacé clic en el link antes de iniciar sesión.
          </p>
          <p>
            <Link to="/login">Ir a iniciar sesión</Link>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Crear cuenta</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="nombre">Nombre</label>
            <input id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="password">Contraseña (mínimo 8 caracteres)</label>
            <input
              id="password"
              type="password"
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="rol">Soy</label>
            <select id="rol" value={rol} onChange={(e) => setRol(e.target.value)}>
              <option value="estudiante">Estudiante</option>
              <option value="profesor">Profesor</option>
            </select>
          </div>
          <div className="campo">
            <label>
              <input
                type="checkbox"
                checked={aceptaTerminos}
                onChange={(e) => setAceptaTerminos(e.target.checked)}
              />{' '}
              Acepto los Términos y Condiciones
            </label>
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Creando cuenta…' : 'Crear cuenta'}
          </button>
        </form>
        <p>
          ¿Ya tenés cuenta? <Link to="/login">Iniciar sesión</Link>
        </p>
      </div>
    </div>
  )
}

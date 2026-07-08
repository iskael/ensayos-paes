import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useAuth } from '../AuthContext.jsx'
import { useReenviarVerificacion } from '../useReenviarVerificacion.js'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [emailNoVerificado, setEmailNoVerificado] = useState(false)
  const [enviando, setEnviando] = useState(false)
  const { reenviando, mensajeReenvio, reenviar } = useReenviarVerificacion()
  const { guardarSesion } = useAuth()
  const navigate = useNavigate()

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    setEmailNoVerificado(false)
    setEnviando(true)
    try {
      const respuesta = await api.iniciarSesion({ email, password })
      guardarSesion(respuesta.token, respuesta.usuario)
      navigate('/')
    } catch (e) {
      if (e instanceof ApiError && e.codigo === 'EMAIL_NO_VERIFICADO') {
        setEmailNoVerificado(true)
      } else if (e instanceof ApiError && e.status === 401) {
        setError('Email o contraseña incorrectos')
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
        <h1>Iniciar sesión</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          {emailNoVerificado && (
            <div className="campo">
              <p className="error">Todavía no verificaste tu email.</p>
              <button
                type="button"
                className="boton-secundario"
                disabled={reenviando}
                onClick={() => reenviar(email)}
              >
                {reenviando ? 'Reenviando…' : 'Reenviar verificación'}
              </button>
              {mensajeReenvio && <p>{mensajeReenvio}</p>}
            </div>
          )}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Ingresando…' : 'Ingresar'}
          </button>
        </form>
        <p>
          ¿No tenés cuenta? <Link to="/registro">Crear cuenta</Link>
        </p>
      </div>
    </div>
  )
}

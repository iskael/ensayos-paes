import { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'

export default function VerificarEmail() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [estado, setEstado] = useState('cargando')
  const [mensaje, setMensaje] = useState(null)
  const [email, setEmail] = useState('')
  const [reenviando, setReenviando] = useState(false)
  const [mensajeReenvio, setMensajeReenvio] = useState(null)

  useEffect(() => {
    if (!token) {
      setEstado('error')
      setMensaje('Este link no incluye un token de verificación.')
      return
    }
    let cancelado = false
    api
      .verificarEmail(token)
      .then((respuesta) => {
        if (cancelado) return
        setEstado('exito')
        setMensaje(respuesta.mensaje)
      })
      .catch((e) => {
        if (cancelado) return
        setEstado('error')
        setMensaje(e instanceof ApiError ? e.mensaje || 'Este link ya no es válido' : 'Este link ya no es válido')
      })
    return () => {
      cancelado = true
    }
  }, [token])

  async function alReenviar(evento) {
    evento.preventDefault()
    setReenviando(true)
    setMensajeReenvio(null)
    try {
      const respuesta = await api.reenviarVerificacion(email)
      setMensajeReenvio(respuesta.mensaje)
    } catch {
      setMensajeReenvio('No se pudo reenviar el correo, intentá de nuevo más tarde.')
    } finally {
      setReenviando(false)
    }
  }

  if (estado === 'cargando') {
    return (
      <div className="pantalla">
        <div className="tarjeta">Verificando tu cuenta…</div>
      </div>
    )
  }

  if (estado === 'exito') {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>¡Listo!</h1>
          <p>{mensaje}</p>
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
        <h1>Este link ya no es válido</h1>
        <p className="error">{mensaje}</p>
        <form onSubmit={alReenviar}>
          <div className="campo">
            <label htmlFor="email">Reenviar verificación a</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <button className="boton" type="submit" disabled={reenviando}>
            {reenviando ? 'Reenviando…' : 'Reenviar'}
          </button>
        </form>
        {mensajeReenvio && <p>{mensajeReenvio}</p>}
      </div>
    </div>
  )
}

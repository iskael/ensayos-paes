import { useState } from 'react'
import { api } from './api.js'

export function useReenviarVerificacion() {
  const [reenviando, setReenviando] = useState(false)
  const [mensajeReenvio, setMensajeReenvio] = useState(null)

  async function reenviar(email) {
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

  return { reenviando, mensajeReenvio, reenviar }
}

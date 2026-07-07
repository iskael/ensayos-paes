import { createContext, useContext, useState, useCallback } from 'react'
import { leerSesionGuardada, guardarSesion as persistirSesion, borrarSesion } from './sesion.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [sesion, setSesion] = useState(leerSesionGuardada)

  const guardarSesionEnContexto = useCallback((token, usuario) => {
    const nuevaSesion = { token, usuario }
    persistirSesion(nuevaSesion)
    setSesion(nuevaSesion)
  }, [])

  const cerrarSesion = useCallback(() => {
    borrarSesion()
    setSesion(null)
  }, [])

  const valor = {
    token: sesion?.token ?? null,
    usuario: sesion?.usuario ?? null,
    guardarSesion: guardarSesionEnContexto,
    cerrarSesion,
  }

  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const contexto = useContext(AuthContext)
  if (!contexto) throw new Error('useAuth debe usarse dentro de <AuthProvider>')
  return contexto
}

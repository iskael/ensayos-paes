import { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
import { ApiError } from './api.js'

export function useApi() {
  const { token, cerrarSesion } = useAuth()
  const navigate = useNavigate()

  const llamar = useCallback(
    async (fn) => {
      try {
        return await fn(token)
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          cerrarSesion()
          navigate('/login')
        }
        throw error
      }
    },
    [token, cerrarSesion, navigate],
  )

  return { llamar }
}

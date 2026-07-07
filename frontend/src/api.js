const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080'

export class ApiError extends Error {
  constructor(status, codigo, mensaje, extra) {
    super(mensaje || 'Error de red')
    this.status = status
    this.codigo = codigo
    this.extra = extra
  }
}

async function pedir(ruta, { metodo = 'GET', body, token } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers.Authorization = `Bearer ${token}`

  let res
  try {
    res = await fetch(`${BASE_URL}${ruta}`, {
      method: metodo,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new ApiError(0, 'ERROR_RED', 'No se pudo conectar con el servidor')
  }

  if (res.status === 204) return null

  const datos = await res.json().catch(() => null)
  if (!res.ok) {
    throw new ApiError(res.status, datos?.codigo, datos?.mensaje, datos)
  }
  return datos
}

export const api = {
  registrar: (body) => pedir('/api/v1/auth/register', { metodo: 'POST', body }),
  iniciarSesion: (body) => pedir('/api/v1/auth/login', { metodo: 'POST', body }),
  crearEnsayo: (token, body) => pedir('/api/v1/ensayos', { metodo: 'POST', body, token }),
  obtenerEnsayo: (token, id) => pedir(`/api/v1/ensayos/${id}`, { token }),
  guardarRespuestas: (token, id, body) =>
    pedir(`/api/v1/ensayos/${id}/respuestas`, { metodo: 'PATCH', body, token }),
  enviarEnsayo: (token, id) => pedir(`/api/v1/ensayos/${id}/enviar`, { metodo: 'POST', token }),
  obtenerResultado: (token, id) => pedir(`/api/v1/ensayos/${id}/resultado`, { token }),
}

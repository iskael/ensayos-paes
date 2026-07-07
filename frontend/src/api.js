// Sin VITE_API_URL (build de produccion), se deriva del host que uso el
// navegador para cargar la pagina -- asi el mismo build funciona accedido
// por LAN, por Tailscale, o por cualquier otro host/IP, sin fijar uno solo
// en tiempo de compilacion.
const BASE_URL =
  import.meta.env.VITE_API_URL || `${window.location.protocol}//${window.location.hostname}:8080`

export class ApiError extends Error {
  constructor(status, codigo, mensaje, extra) {
    super(mensaje || 'Error de red')
    this.status = status
    this.codigo = codigo
    this.mensaje = mensaje
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
  dashboardResumen: (token) => pedir('/api/v1/dashboard/resumen', { token }),
  dashboardEvolucion: (token) => pedir('/api/v1/dashboard/evolucion', { token }),
}

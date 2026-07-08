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
  const esFormData = typeof FormData !== 'undefined' && body instanceof FormData
  const headers = {}
  if (!esFormData) headers['Content-Type'] = 'application/json'
  if (token) headers.Authorization = `Bearer ${token}`

  let res
  try {
    res = await fetch(`${BASE_URL}${ruta}`, {
      method: metodo,
      headers,
      body: esFormData ? body : body !== undefined ? JSON.stringify(body) : undefined,
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
  verificarEmail: (token) => pedir('/api/v1/auth/verificar-email', { metodo: 'POST', body: { token } }),
  reenviarVerificacion: (email) => pedir('/api/v1/auth/reenviar-verificacion', { metodo: 'POST', body: { email } }),
  crearEnsayo: (token, body) => pedir('/api/v1/ensayos', { metodo: 'POST', body, token }),
  obtenerEnsayo: (token, id) => pedir(`/api/v1/ensayos/${id}`, { token }),
  guardarRespuestas: (token, id, body) =>
    pedir(`/api/v1/ensayos/${id}/respuestas`, { metodo: 'PATCH', body, token }),
  enviarEnsayo: (token, id) => pedir(`/api/v1/ensayos/${id}/enviar`, { metodo: 'POST', token }),
  obtenerResultado: (token, id) => pedir(`/api/v1/ensayos/${id}/resultado`, { token }),
  dashboardResumen: (token) => pedir('/api/v1/dashboard/resumen', { token }),
  dashboardEvolucion: (token) => pedir('/api/v1/dashboard/evolucion', { token }),
  crearExamen: (token, body) => pedir('/api/v1/examenes', { metodo: 'POST', body, token }),
  listarExamenes: (token, { limit, offset } = {}) => {
    const params = new URLSearchParams()
    if (limit !== undefined) params.set('limit', limit)
    if (offset !== undefined) params.set('offset', offset)
    const qs = params.toString()
    return pedir(`/api/v1/examenes${qs ? `?${qs}` : ''}`, { token })
  },
  obtenerExamen: (token, id) => pedir(`/api/v1/examenes/${id}`, { token }),
  actualizarExamen: (token, id, body) => pedir(`/api/v1/examenes/${id}`, { metodo: 'PUT', body, token }),
  eliminarExamen: (token, id) => pedir(`/api/v1/examenes/${id}`, { metodo: 'DELETE', token }),
  obtenerClave: (token, examenId) => pedir(`/api/v1/examenes/${examenId}/clave`, { token }),
  definirClave: (token, examenId, pesos) =>
    pedir(`/api/v1/examenes/${examenId}/clave`, { metodo: 'PUT', body: { pesos }, token }),
  importarPdf: (token, examenId, formData) =>
    pedir(`/api/v1/examenes/${examenId}/importacion-pdf`, { metodo: 'POST', body: formData, token }),
  crearItem: (token, body) => pedir('/api/v1/items', { metodo: 'POST', body, token }),
  listarItems: (token, filtros = {}) => {
    const params = new URLSearchParams()
    for (const [clave, valor] of Object.entries(filtros)) {
      if (valor !== undefined && valor !== null && valor !== '') params.set(clave, valor)
    }
    const qs = params.toString()
    return pedir(`/api/v1/items${qs ? `?${qs}` : ''}`, { token })
  },
  obtenerItem: (token, id) => pedir(`/api/v1/items/${id}`, { token }),
  actualizarItem: (token, id, body) => pedir(`/api/v1/items/${id}`, { metodo: 'PUT', body, token }),
  eliminarItem: (token, id) => pedir(`/api/v1/items/${id}`, { metodo: 'DELETE', token }),
  publicarItem: (token, id) => pedir(`/api/v1/items/${id}/publicar`, { metodo: 'POST', token }),
  ocultarItem: (token, id) => pedir(`/api/v1/items/${id}/ocultar`, { metodo: 'POST', token }),
  subirImagen: (token, formData) => pedir('/api/v1/imagenes', { metodo: 'POST', body: formData, token }),
  crearGrupo: (token, body) => pedir('/api/v1/grupos', { metodo: 'POST', body, token }),
  listarGrupos: (token) => pedir('/api/v1/grupos', { token }),
  unirseGrupo: (token, codigo) => pedir('/api/v1/grupos/unirse', { metodo: 'POST', body: { codigo }, token }),
  obtenerGrupo: (token, id) => pedir(`/api/v1/grupos/${id}`, { token }),
  listarMiembros: (token, id) => pedir(`/api/v1/grupos/${id}/miembros`, { token }),
  progresoEstudiante: (token, grupoId, estudianteId) =>
    pedir(`/api/v1/grupos/${grupoId}/estudiantes/${estudianteId}`, { token }),
  misGrupos: (token) => pedir('/api/v1/grupos/mis-grupos', { token }),
}

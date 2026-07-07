export const CLAVE_SESION = 'sesion'

export function leerSesionGuardada(storage = window.localStorage) {
  try {
    const crudo = storage.getItem(CLAVE_SESION)
    return crudo ? JSON.parse(crudo) : null
  } catch {
    return null
  }
}

export function guardarSesion(sesion, storage = window.localStorage) {
  storage.setItem(CLAVE_SESION, JSON.stringify(sesion))
}

export function borrarSesion(storage = window.localStorage) {
  storage.removeItem(CLAVE_SESION)
}

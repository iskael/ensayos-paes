const CLAVE = 'ensayos-paes-tema'

export function temaGuardado() {
  try {
    return localStorage.getItem(CLAVE) || 'auto'
  } catch {
    return 'auto'
  }
}

export function aplicarTema(tema) {
  const raiz = document.documentElement
  if (tema === 'claro' || tema === 'oscuro') raiz.dataset.tema = tema
  else delete raiz.dataset.tema
  try {
    localStorage.setItem(CLAVE, tema)
  } catch {
    /* sin almacenamiento local */
  }
}

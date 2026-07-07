const PATRON_FORMULA = /\$\$(.+?)\$\$|\$(.+?)\$/g

export function partirTexto(texto) {
  const partes = []
  if (!texto) return partes

  let ultimoIndice = 0
  let match
  PATRON_FORMULA.lastIndex = 0
  while ((match = PATRON_FORMULA.exec(texto)) !== null) {
    if (match.index > ultimoIndice) {
      partes.push({ tipo: 'texto', valor: texto.slice(ultimoIndice, match.index) })
    }
    if (match[1] !== undefined) {
      partes.push({ tipo: 'bloque', valor: match[1] })
    } else {
      partes.push({ tipo: 'inline', valor: match[2] })
    }
    ultimoIndice = PATRON_FORMULA.lastIndex
  }
  if (ultimoIndice < texto.length) {
    partes.push({ tipo: 'texto', valor: texto.slice(ultimoIndice) })
  }
  return partes
}

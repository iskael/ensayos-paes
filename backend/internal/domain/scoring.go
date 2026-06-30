package domain

// CalcularPuntaje devuelve el puntaje en escala 1000, normalizado:
// round((puntosObtenidos / puntosPosibles) * 1000). Si puntosPosibles es 0, retorna 0.
func CalcularPuntaje(puntosObtenidos, puntosPosibles int) int {
	if puntosPosibles <= 0 {
		return 0
	}
	return int(float64(puntosObtenidos)/float64(puntosPosibles)*1000.0 + 0.5)
}

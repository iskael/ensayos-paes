package domain

// PesoTotalClave es la suma que deben cumplir los pesos de una clave de examen (RN-03).
const PesoTotalClave = 1000

func SumaPesos(pesos []int) int {
	total := 0
	for _, p := range pesos {
		total += p
	}
	return total
}

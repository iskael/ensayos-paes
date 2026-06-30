package domain

import "testing"

func TestCalcularPuntaje(t *testing.T) {
	casos := []struct {
		obtenidos, posibles, esperado int
	}{
		{300, 300, 1000}, // todo correcto
		{0, 300, 0},      // nada correcto
		{150, 300, 500},  // mitad
		{100, 300, 333},  // redondeo
		{0, 0, 0},        // sin posibles
	}
	for _, c := range casos {
		if got := CalcularPuntaje(c.obtenidos, c.posibles); got != c.esperado {
			t.Errorf("CalcularPuntaje(%d,%d)=%d; esperado %d", c.obtenidos, c.posibles, got, c.esperado)
		}
	}
}

package domain

import "testing"

func TestSumaPesos(t *testing.T) {
	if got := SumaPesos([]int{100, 200, 700}); got != PesoTotalClave {
		t.Fatalf("esperado %d, obtuve %d", PesoTotalClave, got)
	}
	if got := SumaPesos(nil); got != 0 {
		t.Fatalf("esperado 0, obtuve %d", got)
	}
	if got := SumaPesos([]int{500, 400}); got == PesoTotalClave {
		t.Fatal("no debería sumar 1000")
	}
}

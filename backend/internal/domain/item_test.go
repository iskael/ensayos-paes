package domain

import "testing"

func alternativasBase(correctaIdx int) []Alternativa {
	et := []EtiquetaAlternativa{AltA, AltB, AltC, AltD}
	out := make([]Alternativa, len(et))
	for i, e := range et {
		out[i] = Alternativa{Etiqueta: e, Texto: "x", EsCorrecta: i == correctaIdx}
	}
	return out
}

func TestValidarAlternativas_CasoValido(t *testing.T) {
	if err := ValidarAlternativas(alternativasBase(0)); err != nil {
		t.Fatalf("caso válido falló: %v", err)
	}
}

func TestValidarAlternativas_MenosDeCuatro(t *testing.T) {
	if err := ValidarAlternativas(alternativasBase(0)[:3]); err == nil {
		t.Fatal("esperaba error por menos de 4 alternativas")
	}
}

func TestValidarAlternativas_DosCorrectas(t *testing.T) {
	alts := alternativasBase(0)
	alts[1].EsCorrecta = true
	if err := ValidarAlternativas(alts); err == nil {
		t.Fatal("esperaba error por dos alternativas correctas")
	}
}

func TestValidarAlternativas_NingunaCorrecta(t *testing.T) {
	if err := ValidarAlternativas(alternativasBase(-1)); err == nil {
		t.Fatal("esperaba error por ninguna alternativa correcta")
	}
}

func TestValidarAlternativas_EtiquetaRepetida(t *testing.T) {
	alts := alternativasBase(0)
	alts[1].Etiqueta = AltA
	if err := ValidarAlternativas(alts); err == nil {
		t.Fatal("esperaba error por etiqueta repetida")
	}
}

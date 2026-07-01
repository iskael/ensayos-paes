package pdfimport

import "testing"

func TestSegmentarPreguntas_CasoCompleto(t *testing.T) {
	texto := `Instrucciones generales del examen, ignorar esta parte.

1. ¿Cuánto es 2+2?
A) 3
B) 4
C) 5
D) 6

2. ¿Cuál es la capital de Chile?
A) Valparaíso
B) Santiago
C) Concepción
D) Temuco
`
	preguntas := SegmentarPreguntas(texto)
	if len(preguntas) != 2 {
		t.Fatalf("esperaba 2 preguntas, obtuve %d", len(preguntas))
	}

	p1 := preguntas[0]
	if p1.NumeroDetectado != 1 || p1.Enunciado != "¿Cuánto es 2+2?" {
		t.Fatalf("pregunta 1 inesperada: %+v", p1)
	}
	if len(p1.Alternativas) != 4 {
		t.Fatalf("pregunta 1 debería tener 4 alternativas, obtuve %d", len(p1.Alternativas))
	}
	esperadas := []AlternativaCruda{{"A", "3"}, {"B", "4"}, {"C", "5"}, {"D", "6"}}
	for i, e := range esperadas {
		if p1.Alternativas[i] != e {
			t.Fatalf("alternativa %d inesperada: %+v (esperaba %+v)", i, p1.Alternativas[i], e)
		}
	}

	p2 := preguntas[1]
	if p2.NumeroDetectado != 2 || p2.Enunciado != "¿Cuál es la capital de Chile?" {
		t.Fatalf("pregunta 2 inesperada: %+v", p2)
	}
}

func TestSegmentarPreguntas_MenosDeCuatroAlternativas(t *testing.T) {
	texto := `1. Pregunta incompleta
A) Uno
B) Dos
`
	preguntas := SegmentarPreguntas(texto)
	if len(preguntas) != 1 {
		t.Fatalf("esperaba 1 pregunta, obtuve %d", len(preguntas))
	}
	if len(preguntas[0].Alternativas) != 2 {
		t.Fatalf("esperaba 2 alternativas detectadas, obtuve %d", len(preguntas[0].Alternativas))
	}
}

func TestSegmentarPreguntas_SinNumeracion(t *testing.T) {
	texto := "Esto es solo un párrafo sin numeración de preguntas."
	preguntas := SegmentarPreguntas(texto)
	if len(preguntas) != 0 {
		t.Fatalf("esperaba 0 preguntas, obtuve %d", len(preguntas))
	}
}

func TestSegmentarPreguntas_NuncaMarcaCorrecta(t *testing.T) {
	// La heurística no tiene forma de saber cuál alternativa es correcta;
	// esto se valida indirectamente: AlternativaCruda no tiene ese campo.
	texto := "1. Pregunta\nA) x\nB) y\nC) z\nD) w\n"
	p := SegmentarPreguntas(texto)[0]
	for _, a := range p.Alternativas {
		if a.Etiqueta == "" || a.Texto == "" {
			t.Fatalf("alternativa incompleta: %+v", a)
		}
	}
}

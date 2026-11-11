package domain

import (
	"fmt"
	"time"
)

type Alternativa struct {
	ID         string              `json:"id,omitempty"`
	Etiqueta   EtiquetaAlternativa `json:"etiqueta"`
	Texto      string              `json:"texto"`
	ImagenURL  *string             `json:"imagen_url,omitempty"`
	EsCorrecta bool                `json:"es_correcta"`
}

type Item struct {
	ID             string        `json:"id"`
	ExamenFuenteID *string       `json:"examen_fuente_id,omitempty"`
	Enunciado      string        `json:"enunciado"`
	ImagenURL      *string       `json:"imagen_url,omitempty"`
	Eje            Eje           `json:"eje"`
	Nivel          Nivel         `json:"nivel"`
	Dificultad     Dificultad    `json:"dificultad"`
	Origen         OrigenItem    `json:"origen"`
	Estado         EstadoItem    `json:"estado"`
	Peso           *int          `json:"peso,omitempty"`
	Explicacion    *string       `json:"explicacion,omitempty"`
	Alternativas   []Alternativa `json:"alternativas"`
	FechaCreacion  time.Time     `json:"fecha_creacion"`
}

// ValidarAlternativas: 4 (A-D) o 5 (A-E) alternativas, con las etiquetas consecutivas desde A, sin repetir y una sola correcta.
// Las de 5 son las de suficiencia de datos de la PAES M2.
func ValidarAlternativas(alts []Alternativa) error {
	if len(alts) != 4 && len(alts) != 5 {
		return fmt.Errorf("un ítem debe tener 4 o 5 alternativas")
	}
	permitidas := map[EtiquetaAlternativa]bool{}
	for _, e := range ordenEtiquetas[:len(alts)] {
		permitidas[e] = true
	}
	vistas := map[EtiquetaAlternativa]bool{}
	correctas := 0
	for _, a := range alts {
		if !a.Etiqueta.Valida() {
			return fmt.Errorf("etiqueta de alternativa inválida: %s", a.Etiqueta)
		}
		if !permitidas[a.Etiqueta] {
			return fmt.Errorf("con %d alternativas las etiquetas deben ir de A a %s", len(alts), ordenEtiquetas[len(alts)-1])
		}
		if vistas[a.Etiqueta] {
			return fmt.Errorf("etiqueta de alternativa repetida: %s", a.Etiqueta)
		}
		vistas[a.Etiqueta] = true
		if a.EsCorrecta {
			correctas++
		}
	}
	if correctas != 1 {
		return fmt.Errorf("debe existir exactamente una alternativa correcta")
	}
	return nil
}

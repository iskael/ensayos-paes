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

// ValidarAlternativas: exactamente 4, etiquetas A-D sin repetir, una sola correcta.
func ValidarAlternativas(alts []Alternativa) error {
	if len(alts) != 4 {
		return fmt.Errorf("un ítem debe tener exactamente 4 alternativas")
	}
	vistas := map[EtiquetaAlternativa]bool{}
	correctas := 0
	for _, a := range alts {
		if !a.Etiqueta.Valida() {
			return fmt.Errorf("etiqueta de alternativa inválida: %s", a.Etiqueta)
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

package pdfimport

import (
	"regexp"
	"strconv"
	"strings"
)

type AlternativaCruda struct {
	Etiqueta string
	Texto    string
}

type PreguntaCruda struct {
	NumeroDetectado int
	Enunciado       string
	Alternativas    []AlternativaCruda
}

var reInicioPregunta = regexp.MustCompile(`^\s*(\d{1,3})[.)]\s+(.*)$`)
var reInicioAlternativa = regexp.MustCompile(`^\s*([A-Da-d])[.)]\s+(.*)$`)

// SegmentarPreguntas aplica una heurística de "extracción asistida": separa
// el texto en bloques por numeración ("1.", "2)", ...) y, dentro de cada
// bloque, identifica alternativas A-D por su marcador ("A)", "B.", ...).
//
// Es best-effort a propósito: NUNCA determina cuál alternativa es correcta
// (eso normalmente no está en el PDF del examen, sino en una clave aparte),
// por lo que todo resultado requiere revisión humana antes de publicarse
// (RN-04) — el propio validador de publicación ya bloquea ítems sin una
// alternativa marcada como correcta.
func SegmentarPreguntas(texto string) []PreguntaCruda {
	type bloque struct {
		numero int
		lineas []string
	}

	var bloques []bloque
	var actual *bloque
	for _, linea := range strings.Split(texto, "\n") {
		if m := reInicioPregunta.FindStringSubmatch(linea); m != nil {
			if actual != nil {
				bloques = append(bloques, *actual)
			}
			n, _ := strconv.Atoi(m[1])
			actual = &bloque{numero: n, lineas: []string{m[2]}}
			continue
		}
		if actual != nil {
			actual.lineas = append(actual.lineas, linea)
		}
	}
	if actual != nil {
		bloques = append(bloques, *actual)
	}

	out := make([]PreguntaCruda, 0, len(bloques))
	for _, b := range bloques {
		p := procesarBloque(b.numero, b.lineas)
		if p.Enunciado == "" {
			continue // ruido: numeración sin contenido reconocible
		}
		out = append(out, p)
	}
	return out
}

func procesarBloque(numero int, lineas []string) PreguntaCruda {
	var enunciado []string
	textoPorEtiqueta := map[string][]string{}
	var ordenEtiquetas []string
	etiquetaActual := ""

	for _, linea := range lineas {
		if m := reInicioAlternativa.FindStringSubmatch(linea); m != nil {
			etq := strings.ToUpper(m[1])
			if _, existe := textoPorEtiqueta[etq]; !existe {
				ordenEtiquetas = append(ordenEtiquetas, etq)
			}
			textoPorEtiqueta[etq] = []string{m[2]}
			etiquetaActual = etq
			continue
		}
		if etiquetaActual == "" {
			enunciado = append(enunciado, linea)
		} else {
			textoPorEtiqueta[etiquetaActual] = append(textoPorEtiqueta[etiquetaActual], linea)
		}
	}

	alternativas := make([]AlternativaCruda, 0, 4)
	for _, etq := range ordenEtiquetas {
		if len(alternativas) >= 4 {
			break
		}
		txt := strings.TrimSpace(strings.Join(textoPorEtiqueta[etq], " "))
		if txt == "" {
			continue
		}
		alternativas = append(alternativas, AlternativaCruda{Etiqueta: etq, Texto: txt})
	}

	return PreguntaCruda{
		NumeroDetectado: numero,
		Enunciado:       strings.TrimSpace(strings.Join(enunciado, " ")),
		Alternativas:    alternativas,
	}
}

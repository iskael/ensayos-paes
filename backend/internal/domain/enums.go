package domain

type Nivel string

const (
	NivelM1       Nivel = "M1"
	NivelM2       Nivel = "M2"
	NivelCL       Nivel = "CL"
	NivelHCS      Nivel = "HCS"
	NivelCiencias Nivel = "CIENCIAS"
)

func (n Nivel) Valido() bool {
	_, ok := pruebasPorNivel[n]
	return ok
}

type Eje string

const (
	EjeNumeros                 Eje = "numeros"
	EjeAlgebraFunciones        Eje = "algebra_funciones"
	EjeGeometria               Eje = "geometria"
	EjeProbabilidadEstadistica Eje = "probabilidad_estadistica"
	EjeLocalizar               Eje = "localizar"
	EjeInterpretar             Eje = "interpretar"
	EjeEvaluar                 Eje = "evaluar"
	EjeHistoria                Eje = "historia"
	EjeFormacionCiudadana      Eje = "formacion_ciudadana"
	EjeSistemaEconomico        Eje = "sistema_economico"
	EjeBiologia                Eje = "biologia"
	EjeFisica                  Eje = "fisica"
	EjeQuimica                 Eje = "quimica"
)

func (e Eje) Valido() bool {
	_, ok := nivelDeEje[e]
	return ok
}

// Prueba describe una PAES: sus ejes, su tamaño y su tiempo oficiales, y si sus preguntas se agrupan bajo un texto común.
type Prueba struct {
	Nivel              Nivel  `json:"nivel"`
	Nombre             string `json:"nombre"`
	Ejes               []Eje  `json:"ejes"`
	PreguntasOficiales int    `json:"preguntas_oficiales"`
	MinutosOficiales   int    `json:"minutos_oficiales"`
	UsaEstimulos       bool   `json:"usa_estimulos"`
}

var ejesMatematica = []Eje{EjeNumeros, EjeAlgebraFunciones, EjeGeometria, EjeProbabilidadEstadistica}

var Pruebas = []Prueba{
	{NivelCL, "Competencia Lectora", []Eje{EjeLocalizar, EjeInterpretar, EjeEvaluar}, 65, 150, true},
	{NivelM1, "Competencia Matemática 1", ejesMatematica, 65, 140, false},
	{NivelM2, "Competencia Matemática 2", ejesMatematica, 55, 140, false},
	{NivelCiencias, "Ciencias", []Eje{EjeBiologia, EjeFisica, EjeQuimica}, 80, 160, false},
	{NivelHCS, "Historia y Ciencias Sociales", []Eje{EjeHistoria, EjeFormacionCiudadana, EjeSistemaEconomico}, 65, 120, false},
}

var pruebasPorNivel = map[Nivel]Prueba{}
var nivelDeEje = map[Eje]Nivel{}

func init() {
	for _, p := range Pruebas {
		pruebasPorNivel[p.Nivel] = p
		for _, e := range p.Ejes {
			if _, ok := nivelDeEje[e]; !ok {
				nivelDeEje[e] = p.Nivel
			}
		}
	}
}

func PruebaDe(n Nivel) (Prueba, bool) {
	p, ok := pruebasPorNivel[n]
	return p, ok
}

// EjePerteneceA indica si el eje es de la prueba (los ejes de matemática son de M1 y de M2).
func EjePerteneceA(e Eje, n Nivel) bool {
	p, ok := pruebasPorNivel[n]
	if !ok {
		return false
	}
	for _, x := range p.Ejes {
		if x == e {
			return true
		}
	}
	return false
}

// LimiteMinutos prorratea el tiempo oficial de la prueba según la cantidad de preguntas del ensayo.
func LimiteMinutos(n Nivel, cantidad int) int {
	p, ok := pruebasPorNivel[n]
	if !ok || p.PreguntasOficiales == 0 {
		return 0
	}
	return (cantidad*p.MinutosOficiales + p.PreguntasOficiales - 1) / p.PreguntasOficiales
}

type Dificultad string

const (
	DificultadBaja  Dificultad = "baja"
	DificultadMedia Dificultad = "media"
	DificultadAlta  Dificultad = "alta"
)

func (d Dificultad) Valido() bool {
	switch d {
	case DificultadBaja, DificultadMedia, DificultadAlta:
		return true
	}
	return false
}

type OrigenItem string

const (
	OrigenOficial  OrigenItem = "oficial"
	OrigenGenerado OrigenItem = "generado"
)

type EstadoItem string

const (
	EstadoBorrador  EstadoItem = "borrador"
	EstadoPublicado EstadoItem = "publicado"
	EstadoOculto    EstadoItem = "oculto"
)

type TipoExamen string

const (
	TipoPAESRegular  TipoExamen = "PAES_Regular"
	TipoPAESInvierno TipoExamen = "PAES_Invierno"
	TipoPDT          TipoExamen = "PDT"
)

func (t TipoExamen) Valido() bool {
	switch t {
	case TipoPAESRegular, TipoPAESInvierno, TipoPDT:
		return true
	}
	return false
}

type EtiquetaAlternativa string

const (
	AltA EtiquetaAlternativa = "A"
	AltB EtiquetaAlternativa = "B"
	AltC EtiquetaAlternativa = "C"
	AltD EtiquetaAlternativa = "D"
	AltE EtiquetaAlternativa = "E"
)

var ordenEtiquetas = []EtiquetaAlternativa{AltA, AltB, AltC, AltD, AltE}

func (e EtiquetaAlternativa) Valida() bool {
	switch e {
	case AltA, AltB, AltC, AltD, AltE:
		return true
	}
	return false
}

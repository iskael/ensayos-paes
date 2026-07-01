package domain

type Nivel string

const (
	NivelM1 Nivel = "M1"
	NivelM2 Nivel = "M2"
)

func (n Nivel) Valido() bool { return n == NivelM1 || n == NivelM2 }

type Eje string

const (
	EjeNumeros                 Eje = "numeros"
	EjeAlgebraFunciones        Eje = "algebra_funciones"
	EjeGeometria               Eje = "geometria"
	EjeProbabilidadEstadistica Eje = "probabilidad_estadistica"
)

func (e Eje) Valido() bool {
	switch e {
	case EjeNumeros, EjeAlgebraFunciones, EjeGeometria, EjeProbabilidadEstadistica:
		return true
	}
	return false
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
)

func (e EtiquetaAlternativa) Valida() bool {
	switch e {
	case AltA, AltB, AltC, AltD:
		return true
	}
	return false
}

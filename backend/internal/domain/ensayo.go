package domain

import "time"

type ModoEnsayo string

const ModoLibre ModoEnsayo = "libre" // 'cronometrado' se incorpora en v2

type EstadoEnsayo string

const (
	EnsayoEnProgreso EstadoEnsayo = "en_progreso"
	EnsayoFinalizado EstadoEnsayo = "finalizado"
)

var CantidadesEnsayoValidas = map[int]bool{10: true, 20: true, 30: true}

func CantidadEnsayoValida(c int) bool { return CantidadesEnsayoValidas[c] }

func EjesValidos(ejes []Eje) bool {
	if len(ejes) == 0 {
		return false
	}
	vistos := map[Eje]bool{}
	for _, e := range ejes {
		if !e.Valido() || vistos[e] {
			return false
		}
		vistos[e] = true
	}
	return true
}

type Ensayo struct {
	ID              string
	EstudianteID    string
	Nivel           Nivel
	Ejes            []Eje
	Cantidad        int
	Modo            ModoEnsayo
	Estado          EstadoEnsayo
	FechaInicio     time.Time
	FechaFin        *time.Time
	Puntaje         *int
	PuntosObtenidos *int
	PuntosPosibles  *int
	Correctas       *int
	Total           *int
}

// DistribuirCantidad reparte `cantidad` de forma equitativa entre los ejes
// elegidos (RN-01). Si algún eje no tiene stock para su cuota, el remanente
// se completa con la capacidad extra de otros ejes. Retorna la selección por
// eje y el `faltante` que no se pudo cubrir (0 si se logró completar todo).
func DistribuirCantidad(cantidad int, ejes []Eje, disponible map[Eje]int) (map[Eje]int, int) {
	n := len(ejes)
	if n == 0 {
		return map[Eje]int{}, cantidad
	}
	base := cantidad / n
	resto := cantidad % n

	objetivo := map[Eje]int{}
	for i, e := range ejes {
		objetivo[e] = base
		if i < resto {
			objetivo[e]++
		}
	}

	seleccion := map[Eje]int{}
	capacidadExtra := map[Eje]int{}
	faltante := 0
	for _, e := range ejes {
		disp := disponible[e]
		obj := objetivo[e]
		if disp >= obj {
			seleccion[e] = obj
			capacidadExtra[e] = disp - obj
		} else {
			seleccion[e] = disp
			faltante += obj - disp
		}
	}

	for _, e := range ejes {
		if faltante == 0 {
			break
		}
		extra := capacidadExtra[e]
		if extra <= 0 {
			continue
		}
		usar := extra
		if usar > faltante {
			usar = faltante
		}
		seleccion[e] += usar
		faltante -= usar
	}

	return seleccion, faltante
}

// ---- Resultado / desglose (RN-02, RN-05) ----

type ItemResultado struct {
	Eje          Eje
	EsCorrecta   bool
	PesoSnapshot int
}

type DesgloseEje struct {
	Eje             Eje
	Correctas       int
	Total           int
	PuntosObtenidos int
	PuntosPosibles  int
}

// ordenEjes fija un orden determinístico para el desglose.
var ordenEjes = []Eje{EjeNumeros, EjeAlgebraFunciones, EjeGeometria, EjeProbabilidadEstadistica}

func CalcularDesglosePorEje(items []ItemResultado) []DesgloseEje {
	acc := map[Eje]*DesgloseEje{}
	for _, it := range items {
		d, ok := acc[it.Eje]
		if !ok {
			d = &DesgloseEje{Eje: it.Eje}
			acc[it.Eje] = d
		}
		d.Total++
		d.PuntosPosibles += it.PesoSnapshot
		if it.EsCorrecta {
			d.Correctas++
			d.PuntosObtenidos += it.PesoSnapshot
		}
	}
	out := make([]DesgloseEje, 0, len(acc))
	for _, e := range ordenEjes {
		if d, ok := acc[e]; ok {
			out = append(out, *d)
		}
	}
	return out
}

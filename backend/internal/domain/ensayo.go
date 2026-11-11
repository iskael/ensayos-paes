package domain

import "time"

type ModoEnsayo string

const (
	ModoLibre     ModoEnsayo = "libre"
	ModoPractica  ModoEnsayo = "practica"
	ModoSimulacro ModoEnsayo = "simulacro"
)

func (m ModoEnsayo) Valido() bool { return m == ModoLibre || m == ModoPractica || m == ModoSimulacro }

type EstadoEnsayo string

const (
	EnsayoEnProgreso EstadoEnsayo = "en_progreso"
	EnsayoFinalizado EstadoEnsayo = "finalizado"
)

var CantidadesEnsayoValidas = map[int]bool{5: true, 10: true, 15: true, 20: true, 30: true, 40: true, 55: true, 65: true, 80: true}

func CantidadEnsayoValida(c int) bool { return CantidadesEnsayoValidas[c] }

func EjesValidos(nivel Nivel, ejes []Eje) bool {
	if len(ejes) == 0 {
		return false
	}
	vistos := map[Eje]bool{}
	for _, e := range ejes {
		if !EjePerteneceA(e, nivel) || vistos[e] {
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
	LimiteMinutos   *int
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
	return completarObjetivo(ejes, objetivo, disponible)
}

// ObjetivoCiencias reparte un ensayo de Ciencias como la PAES: 54 de cada 80 preguntas son del módulo común, en partes
// iguales entre Biología, Física y Química, y las 26 restantes son del módulo electivo elegido.
func ObjetivoCiencias(cantidad int, electivo Eje) map[Eje]int {
	comun := (cantidad*54 + 40) / 80
	porEje := comun / 3
	objetivo := map[Eje]int{EjeBiologia: porEje, EjeFisica: porEje, EjeQuimica: porEje}
	objetivo[electivo] += cantidad - 3*porEje
	return objetivo
}

// DistribuirConObjetivo es como DistribuirCantidad, pero con la cuota de cada eje ya fijada.
func DistribuirConObjetivo(ejes []Eje, objetivo map[Eje]int, disponible map[Eje]int) (map[Eje]int, int) {
	return completarObjetivo(ejes, objetivo, disponible)
}

func completarObjetivo(ejes []Eje, objetivo map[Eje]int, disponible map[Eje]int) (map[Eje]int, int) {
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
var ordenEjes = []Eje{EjeNumeros, EjeAlgebraFunciones, EjeGeometria, EjeProbabilidadEstadistica,
	EjeLocalizar, EjeInterpretar, EjeEvaluar, EjeBiologia, EjeFisica, EjeQuimica,
	EjeHistoria, EjeFormacionCiudadana, EjeSistemaEconomico}

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

// ElegirGruposExactos elige, recorriendo los grupos en el orden dado (ya barajado), un subconjunto cuyos tamaños sumen
// exactamente `objetivo`. Devuelve los índices elegidos en el orden en que se recorrieron, o nil si no hay solución.
func ElegirGruposExactos(objetivo int, tamanos []int) []int {
	alcanzable := make([][]int, objetivo+1)
	alcanzable[0] = []int{}
	for i, t := range tamanos {
		if t <= 0 {
			continue
		}
		for suma := objetivo; suma >= t; suma-- {
			if alcanzable[suma] == nil && alcanzable[suma-t] != nil {
				camino := append(append([]int{}, alcanzable[suma-t]...), i)
				alcanzable[suma] = camino
			}
		}
		if alcanzable[objetivo] != nil {
			break
		}
	}
	return alcanzable[objetivo]
}

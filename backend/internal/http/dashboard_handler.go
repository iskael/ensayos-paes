package httpx

import (
	"net/http"
	"time"

	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type dashboardHandler struct {
	ensayos *repo.Ensayos
}

type dashboardResumenResp struct {
	TotalEnsayos    int               `json:"total_ensayos"`
	UltimoPuntaje   *int              `json:"ultimo_puntaje,omitempty"`
	PromedioPuntaje *float64          `json:"promedio_puntaje,omitempty"`
	MejorPuntaje    *int              `json:"mejor_puntaje,omitempty"`
	DesempenoPorEje []desgloseEjeResp `json:"desempeno_por_eje"`
}

func (h *dashboardHandler) resumen(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())

	// FinalizadosPorEstudiante viene ordenado por fecha_fin ASC: el último
	// elemento es el más reciente (ultimo_puntaje) sin necesidad de otra consulta.
	finalizados, err := h.ensayos.FinalizadosPorEstudiante(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el resumen")
		return
	}

	resp := dashboardResumenResp{TotalEnsayos: len(finalizados), DesempenoPorEje: []desgloseEjeResp{}}
	if len(finalizados) > 0 {
		suma := 0
		mejor := valorInt(finalizados[0].Puntaje)
		for _, e := range finalizados {
			p := valorInt(e.Puntaje)
			suma += p
			if p > mejor {
				mejor = p
			}
		}
		ultimo := valorInt(finalizados[len(finalizados)-1].Puntaje)
		promedio := float64(suma) / float64(len(finalizados))
		resp.UltimoPuntaje = &ultimo
		resp.MejorPuntaje = &mejor
		resp.PromedioPuntaje = &promedio
	}

	items, err := h.ensayos.DesempenoPorEjeEstudiante(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el desempeño por eje")
		return
	}
	for _, d := range domain.CalcularDesglosePorEje(items) {
		resp.DesempenoPorEje = append(resp.DesempenoPorEje, desgloseEjeResp{
			Eje: d.Eje, Correctas: d.Correctas, Total: d.Total,
			PuntosObtenidos: d.PuntosObtenidos, PuntosPosibles: d.PuntosPosibles,
		})
	}

	escribirJSON(w, http.StatusOK, resp)
}

type puntoEvolucionResp struct {
	Fecha   time.Time `json:"fecha"`
	Puntaje int       `json:"puntaje"`
}

func (h *dashboardHandler) evolucion(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	finalizados, err := h.ensayos.FinalizadosPorEstudiante(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener la evolución")
		return
	}
	out := make([]puntoEvolucionResp, 0, len(finalizados))
	for _, e := range finalizados {
		if e.FechaFin == nil {
			continue
		}
		out = append(out, puntoEvolucionResp{Fecha: *e.FechaFin, Puntaje: valorInt(e.Puntaje)})
	}
	escribirJSON(w, http.StatusOK, out)
}

package httpx

import (
	"context"
	"errors"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"

	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type ensayoHandler struct {
	ensayos *repo.Ensayos
}

type apiErr struct {
	status  int
	codigo  string
	mensaje string
}

func (h *ensayoHandler) responderErr(w http.ResponseWriter, e *apiErr) {
	escribirError(w, e.status, e.codigo, e.mensaje)
}

// obtenerPropioBase verifica que el ensayo exista y pertenezca al estudiante.
// Ante ensayos de otro dueño responde 404 (no se revela su existencia).
func (h *ensayoHandler) obtenerPropioBase(ctx context.Context, ensayoID, usuarioID string) (domain.Ensayo, *apiErr) {
	e, err := h.ensayos.ObtenerBase(ctx, ensayoID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		return domain.Ensayo{}, &apiErr{http.StatusNotFound, "NO_ENCONTRADO", "Ensayo no encontrado"}
	}
	if err != nil {
		return domain.Ensayo{}, &apiErr{http.StatusInternalServerError, "INTERNO", "Error al obtener el ensayo"}
	}
	if e.EstudianteID != usuarioID {
		return domain.Ensayo{}, &apiErr{http.StatusNotFound, "NO_ENCONTRADO", "Ensayo no encontrado"}
	}
	return e, nil
}

// ---------------- Crear / listar / obtener ----------------

type crearEnsayoReq struct {
	Nivel    string   `json:"nivel"`
	Ejes     []string `json:"ejes"`
	Cantidad int      `json:"cantidad"`
	Modo     string   `json:"modo"`
}

func (h *ensayoHandler) crear(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	var in crearEnsayoReq
	if !decodificar(w, r, &in) {
		return
	}

	nivel := domain.Nivel(in.Nivel)
	if !nivel.Valido() {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Nivel inválido")
		return
	}
	ejes := make([]domain.Eje, 0, len(in.Ejes))
	for _, e := range in.Ejes {
		ejes = append(ejes, domain.Eje(e))
	}
	if !domain.EjesValidos(ejes) {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Debe seleccionar al menos un eje válido, sin repetir")
		return
	}
	if !domain.CantidadEnsayoValida(in.Cantidad) {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "La cantidad debe ser 10, 20 o 30")
		return
	}
	modo := domain.ModoLibre
	if in.Modo != "" && domain.ModoEnsayo(in.Modo) != domain.ModoLibre {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Modo inválido (solo 'libre' disponible en el MVP)")
		return
	}

	detalle, err := h.ensayos.GenerarAleatorio(r.Context(), claims.UsuarioID, nivel, ejes, in.Cantidad, modo)
	if err != nil {
		var stockErr *repo.StockInsuficienteError
		if errors.As(err, &stockErr) {
			escribirJSON(w, http.StatusUnprocessableEntity, stockErrResp(stockErr))
			return
		}
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo generar el ensayo")
		return
	}
	escribirJSON(w, http.StatusCreated, ensayoResp(detalle))
}

func stockErrResp(e *repo.StockInsuficienteError) map[string]any {
	porEje := make([]map[string]any, 0, len(e.DisponiblesPorEje))
	for eje, n := range e.DisponiblesPorEje {
		porEje = append(porEje, map[string]any{"eje": eje, "disponibles": n})
	}
	return map[string]any{
		"codigo":              "STOCK_INSUFICIENTE",
		"mensaje":             "No hay suficientes ítems publicados para esta configuración",
		"max_disponible":      e.MaxDisponible,
		"disponibles_por_eje": porEje,
	}
}

func (h *ensayoHandler) listar(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	limit, offset := paginacion(r)
	lista, err := h.ensayos.ListarPorEstudiante(r.Context(), claims.UsuarioID, limit, offset)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los ensayos")
		return
	}
	out := make([]ensayoResumenResp, 0, len(lista))
	for _, e := range lista {
		out = append(out, ensayoResumenResp{ID: e.ID, Nivel: e.Nivel, Ejes: e.Ejes, Estado: e.Estado, Puntaje: e.Puntaje, FechaFin: e.FechaFin})
	}
	escribirJSON(w, http.StatusOK, out)
}

func (h *ensayoHandler) obtener(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "ensayoId")
	if _, aerr := h.obtenerPropioBase(r.Context(), id, claims.UsuarioID); aerr != nil {
		h.responderErr(w, aerr)
		return
	}
	detalle, err := h.ensayos.ObtenerDetalle(r.Context(), id)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el ensayo")
		return
	}
	escribirJSON(w, http.StatusOK, ensayoResp(detalle))
}

// ---------------- Responder / enviar / resultado ----------------

type respuestaInputReq struct {
	EnsayoItemID          string `json:"ensayo_item_id"`
	RespuestaSeleccionada string `json:"respuesta_seleccionada"`
}

type guardarRespuestasReq struct {
	Respuestas []respuestaInputReq `json:"respuestas"`
}

func (h *ensayoHandler) guardarRespuestas(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "ensayoId")
	ensayo, aerr := h.obtenerPropioBase(r.Context(), id, claims.UsuarioID)
	if aerr != nil {
		h.responderErr(w, aerr)
		return
	}
	if ensayo.Estado != domain.EnsayoEnProgreso {
		escribirError(w, http.StatusConflict, "ENSAYO_FINALIZADO", "El ensayo ya fue finalizado")
		return
	}

	var in guardarRespuestasReq
	if !decodificar(w, r, &in) {
		return
	}
	respuestas := make([]repo.RespuestaInput, 0, len(in.Respuestas))
	for _, resp := range in.Respuestas {
		et := domain.EtiquetaAlternativa(resp.RespuestaSeleccionada)
		if !et.Valida() {
			escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Respuesta inválida")
			return
		}
		respuestas = append(respuestas, repo.RespuestaInput{EnsayoItemID: resp.EnsayoItemID, Respuesta: et})
	}

	if err := h.ensayos.GuardarRespuestas(r.Context(), id, respuestas); err != nil {
		if errors.Is(err, repo.ErrNoEncontrado) {
			escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Alguna pregunta no pertenece a este ensayo")
			return
		}
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudieron guardar las respuestas")
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *ensayoHandler) enviar(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "ensayoId")
	ensayo, aerr := h.obtenerPropioBase(r.Context(), id, claims.UsuarioID)
	if aerr != nil {
		h.responderErr(w, aerr)
		return
	}
	if ensayo.Estado != domain.EnsayoEnProgreso {
		escribirError(w, http.StatusConflict, "ENSAYO_FINALIZADO", "El ensayo ya fue finalizado")
		return
	}
	if _, err := h.ensayos.Finalizar(r.Context(), id); err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo finalizar el ensayo")
		return
	}
	detalle, err := h.ensayos.ObtenerDetalle(r.Context(), id)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener el resultado")
		return
	}
	escribirJSON(w, http.StatusOK, resultadoResp(detalle))
}

func (h *ensayoHandler) resultado(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "ensayoId")
	ensayo, aerr := h.obtenerPropioBase(r.Context(), id, claims.UsuarioID)
	if aerr != nil {
		h.responderErr(w, aerr)
		return
	}
	if ensayo.Estado != domain.EnsayoFinalizado {
		escribirError(w, http.StatusConflict, "ENSAYO_EN_PROGRESO", "El ensayo aún no se finaliza")
		return
	}
	detalle, err := h.ensayos.ObtenerDetalle(r.Context(), id)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener el resultado")
		return
	}
	escribirJSON(w, http.StatusOK, resultadoResp(detalle))
}

// ---------------- Respuestas JSON ----------------

type alternativaPublicaResp struct {
	Etiqueta  domain.EtiquetaAlternativa `json:"etiqueta"`
	Texto     string                     `json:"texto"`
	ImagenURL *string                    `json:"imagen_url,omitempty"`
}

type preguntaEnsayoResp struct {
	EnsayoItemID          string                      `json:"ensayo_item_id"`
	Orden                 int                         `json:"orden"`
	Enunciado             string                      `json:"enunciado"`
	ImagenURL             *string                     `json:"imagen_url,omitempty"`
	Eje                   domain.Eje                  `json:"eje"`
	Alternativas          []alternativaPublicaResp    `json:"alternativas"`
	RespuestaSeleccionada *domain.EtiquetaAlternativa `json:"respuesta_seleccionada,omitempty"`
}

type ensayoRespT struct {
	ID          string                `json:"id"`
	Nivel       domain.Nivel          `json:"nivel"`
	Ejes        []domain.Eje          `json:"ejes"`
	Cantidad    int                   `json:"cantidad"`
	Modo        domain.ModoEnsayo     `json:"modo"`
	Estado      domain.EstadoEnsayo   `json:"estado"`
	FechaInicio time.Time             `json:"fecha_inicio"`
	FechaFin    *time.Time            `json:"fecha_fin,omitempty"`
	Preguntas   []preguntaEnsayoResp  `json:"preguntas"`
}

// ensayoResp NO expone la alternativa correcta mientras el ensayo está en
// progreso (se revela recién en resultadoResp, tras finalizar).
func ensayoResp(d repo.EnsayoDetalle) ensayoRespT {
	preguntas := make([]preguntaEnsayoResp, 0, len(d.Items))
	for _, it := range d.Items {
		alts := make([]alternativaPublicaResp, 0, len(it.Alternativas))
		for _, a := range it.Alternativas {
			alts = append(alts, alternativaPublicaResp{Etiqueta: a.Etiqueta, Texto: a.Texto, ImagenURL: a.ImagenURL})
		}
		preguntas = append(preguntas, preguntaEnsayoResp{
			EnsayoItemID:          it.EnsayoItemID,
			Orden:                 it.Orden,
			Enunciado:             it.Enunciado,
			ImagenURL:             it.ImagenURL,
			Eje:                   it.Eje,
			Alternativas:          alts,
			RespuestaSeleccionada: it.RespuestaSeleccionada,
		})
	}
	e := d.Ensayo
	return ensayoRespT{
		ID: e.ID, Nivel: e.Nivel, Ejes: e.Ejes, Cantidad: e.Cantidad,
		Modo: e.Modo, Estado: e.Estado, FechaInicio: e.FechaInicio, FechaFin: e.FechaFin,
		Preguntas: preguntas,
	}
}

type ensayoResumenResp struct {
	ID       string              `json:"id"`
	Nivel    domain.Nivel        `json:"nivel"`
	Ejes     []domain.Eje        `json:"ejes"`
	Estado   domain.EstadoEnsayo `json:"estado"`
	Puntaje  *int                `json:"puntaje,omitempty"`
	FechaFin *time.Time          `json:"fecha_fin,omitempty"`
}

type revisionItemResp struct {
	Orden                 int                         `json:"orden"`
	Enunciado             string                      `json:"enunciado"`
	Eje                   domain.Eje                  `json:"eje"`
	RespuestaSeleccionada *domain.EtiquetaAlternativa `json:"respuesta_seleccionada,omitempty"`
	RespuestaCorrecta     domain.EtiquetaAlternativa  `json:"respuesta_correcta"`
	EsCorrecta            bool                        `json:"es_correcta"`
	Peso                  int                         `json:"peso"`
	Explicacion           *string                     `json:"explicacion,omitempty"`
	Alternativas          []domain.Alternativa        `json:"alternativas"`
}

type desgloseEjeResp struct {
	Eje             domain.Eje `json:"eje"`
	Correctas       int        `json:"correctas"`
	Total           int        `json:"total"`
	PuntosObtenidos int        `json:"puntos_obtenidos"`
	PuntosPosibles  int        `json:"puntos_posibles"`
}

type resultadoRespT struct {
	EnsayoID        string              `json:"ensayo_id"`
	Puntaje         int                 `json:"puntaje"`
	Correctas       int                 `json:"correctas"`
	Total           int                 `json:"total"`
	PuntosObtenidos int                 `json:"puntos_obtenidos"`
	PuntosPosibles  int                 `json:"puntos_posibles"`
	DesglosePorEje  []desgloseEjeResp   `json:"desglose_por_eje"`
	Revision        []revisionItemResp  `json:"revision"`
}

// resultadoResp usa los totales YA PERSISTIDOS por Finalizar (RN-02) para el
// puntaje/correctas/total, y recalcula el desglose por eje (RN-05) a partir
// de los ítems, que es determinístico dado lo persistido.
func resultadoResp(d repo.EnsayoDetalle) resultadoRespT {
	items := make([]domain.ItemResultado, 0, len(d.Items))
	revision := make([]revisionItemResp, 0, len(d.Items))
	for _, it := range d.Items {
		correcta := it.EsCorrecta != nil && *it.EsCorrecta
		var respuestaCorrecta domain.EtiquetaAlternativa
		for _, a := range it.Alternativas {
			if a.EsCorrecta {
				respuestaCorrecta = a.Etiqueta
			}
		}
		items = append(items, domain.ItemResultado{Eje: it.Eje, EsCorrecta: correcta, PesoSnapshot: it.PesoSnapshot})
		revision = append(revision, revisionItemResp{
			Orden: it.Orden, Enunciado: it.Enunciado, Eje: it.Eje,
			RespuestaSeleccionada: it.RespuestaSeleccionada, RespuestaCorrecta: respuestaCorrecta,
			EsCorrecta: correcta, Peso: it.PesoSnapshot, Explicacion: it.Explicacion, Alternativas: it.Alternativas,
		})
	}
	desglose := domain.CalcularDesglosePorEje(items)
	desgloseResp := make([]desgloseEjeResp, 0, len(desglose))
	for _, dg := range desglose {
		desgloseResp = append(desgloseResp, desgloseEjeResp{Eje: dg.Eje, Correctas: dg.Correctas, Total: dg.Total, PuntosObtenidos: dg.PuntosObtenidos, PuntosPosibles: dg.PuntosPosibles})
	}

	e := d.Ensayo
	return resultadoRespT{
		EnsayoID:        e.ID,
		Puntaje:         valorInt(e.Puntaje),
		Correctas:       valorInt(e.Correctas),
		Total:           valorInt(e.Total),
		PuntosObtenidos: valorInt(e.PuntosObtenidos),
		PuntosPosibles:  valorInt(e.PuntosPosibles),
		DesglosePorEje:  desgloseResp,
		Revision:        revision,
	}
}

func valorInt(p *int) int {
	if p == nil {
		return 0
	}
	return *p
}

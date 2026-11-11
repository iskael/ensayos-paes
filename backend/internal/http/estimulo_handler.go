package httpx

import (
	"errors"
	"net/http"
	"strings"

	"github.com/go-chi/chi/v5"

	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type estimuloInput struct {
	Nivel     *string `json:"nivel"`
	Titulo    *string `json:"titulo"`
	Texto     string  `json:"texto"`
	ImagenURL *string `json:"imagen_url"`
	Fuente    *string `json:"fuente"`
}

func (in estimuloInput) aBanco() (repo.EstimuloBanco, error) {
	texto := strings.TrimSpace(in.Texto)
	if texto == "" {
		return repo.EstimuloBanco{}, errors.New("el texto no puede estar vacío")
	}
	e := repo.EstimuloBanco{
		Titulo:    vacioANil(in.Titulo),
		Texto:     texto,
		ImagenURL: vacioANil(in.ImagenURL),
		Fuente:    vacioANil(in.Fuente),
	}
	if n := vacioANil(in.Nivel); n != nil {
		nivel := domain.Nivel(*n)
		if !nivel.Valido() {
			return repo.EstimuloBanco{}, errors.New("prueba inválida")
		}
		e.Nivel = &nivel
	}
	return e, nil
}

func vacioANil(s *string) *string {
	if s == nil {
		return nil
	}
	t := strings.TrimSpace(*s)
	if t == "" {
		return nil
	}
	return &t
}

func (h *bancoHandler) validarEstimuloDeItem(w http.ResponseWriter, r *http.Request, it domain.Item) bool {
	if it.EstimuloID == nil {
		if it.OrdenEstimulo != nil {
			escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El orden solo aplica a preguntas asociadas a un texto")
			return false
		}
		return true
	}
	if it.OrdenEstimulo != nil && *it.OrdenEstimulo < 1 {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El orden dentro del texto debe ser 1 o mayor")
		return false
	}
	e, err := h.estimulos.PorID(r.Context(), *it.EstimuloID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El texto asociado no existe")
		return false
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar el texto asociado")
		return false
	}
	if e.Nivel != nil && *e.Nivel != it.Nivel {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "La pregunta debe ser de la misma prueba que su texto")
		return false
	}
	return true
}

func (h *bancoHandler) listarEstimulos(w http.ResponseWriter, r *http.Request) {
	limit, offset := paginacion(r)
	f := repo.FiltrosEstimulos{Limit: limit, Offset: offset, Buscar: strings.TrimSpace(r.URL.Query().Get("buscar"))}
	if v := r.URL.Query().Get("nivel"); v != "" {
		n := domain.Nivel(v)
		f.Nivel = &n
	}
	lista, err := h.estimulos.Listar(r.Context(), f)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los textos")
		return
	}
	escribirJSON(w, http.StatusOK, lista)
}

func (h *bancoHandler) obtenerEstimulo(w http.ResponseWriter, r *http.Request) {
	e, err := h.estimulos.PorID(r.Context(), chi.URLParam(r, "estimuloId"))
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Texto no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener el texto")
		return
	}
	escribirJSON(w, http.StatusOK, e)
}

func (h *bancoHandler) crearEstimulo(w http.ResponseWriter, r *http.Request) {
	var in estimuloInput
	if !decodificar(w, r, &in) {
		return
	}
	e, err := in.aBanco()
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	creado, err := h.estimulos.Crear(r.Context(), e)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear el texto")
		return
	}
	escribirJSON(w, http.StatusCreated, creado)
}

func (h *bancoHandler) actualizarEstimulo(w http.ResponseWriter, r *http.Request) {
	var in estimuloInput
	if !decodificar(w, r, &in) {
		return
	}
	e, err := in.aBanco()
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	id := chi.URLParam(r, "estimuloId")
	actual, err := h.estimulos.PorID(r.Context(), id)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Texto no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener el texto")
		return
	}
	if actual.CantidadItems > 0 && !mismoNivel(actual.Nivel, e.Nivel) {
		escribirError(w, http.StatusConflict, "EN_USO", "No se puede cambiar la prueba de un texto que ya tiene preguntas")
		return
	}
	actualizado, err := h.estimulos.Actualizar(r.Context(), id, e)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo actualizar el texto")
		return
	}
	escribirJSON(w, http.StatusOK, actualizado)
}

func mismoNivel(a, b *domain.Nivel) bool {
	if a == nil || b == nil {
		return a == b
	}
	return *a == *b
}

func (h *bancoHandler) eliminarEstimulo(w http.ResponseWriter, r *http.Request) {
	err := h.estimulos.Eliminar(r.Context(), chi.URLParam(r, "estimuloId"))
	switch {
	case errors.Is(err, repo.ErrNoEncontrado):
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Texto no encontrado")
	case errors.Is(err, repo.ErrEstimuloEnUso):
		escribirError(w, http.StatusConflict, "EN_USO", "El texto tiene preguntas asociadas; elimínalas o muévelas primero")
	case err != nil:
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo eliminar el texto")
	default:
		w.WriteHeader(http.StatusNoContent)
	}
}

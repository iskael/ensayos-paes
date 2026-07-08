package httpx

import (
	"context"
	"errors"
	"net/http"
	"strings"
	"time"

	"github.com/go-chi/chi/v5"

	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type grupoHandler struct {
	grupos  *repo.Grupos
	ensayos *repo.Ensayos
}

type grupoInput struct {
	Nombre string `json:"nombre"`
}

type grupoResp struct {
	ID               string    `json:"id"`
	Nombre           string    `json:"nombre"`
	CodigoInvitacion string    `json:"codigo_invitacion"`
	ProfesorID       string    `json:"profesor_id"`
	FechaCreacion    time.Time `json:"fecha_creacion"`
}

func grupoRespDe(g domain.Grupo) grupoResp {
	return grupoResp{ID: g.ID, Nombre: g.Nombre, CodigoInvitacion: g.CodigoInvitacion, ProfesorID: g.ProfesorID, FechaCreacion: g.FechaCreacion}
}

func (h *grupoHandler) crear(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	var in grupoInput
	if !decodificar(w, r, &in) {
		return
	}
	in.Nombre = strings.TrimSpace(in.Nombre)
	if in.Nombre == "" {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El nombre del grupo es obligatorio")
		return
	}
	g, err := h.grupos.Crear(r.Context(), in.Nombre, claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear el grupo")
		return
	}
	escribirJSON(w, http.StatusCreated, grupoRespDe(g))
}

func (h *grupoHandler) listar(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	lista, err := h.grupos.ListarPorProfesor(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los grupos")
		return
	}
	out := make([]grupoResp, 0, len(lista))
	for _, g := range lista {
		out = append(out, grupoRespDe(g))
	}
	escribirJSON(w, http.StatusOK, out)
}

type unirseGrupoReq struct {
	Codigo string `json:"codigo"`
}

func (h *grupoHandler) unirse(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	var in unirseGrupoReq
	if !decodificar(w, r, &in) {
		return
	}
	codigo := strings.ToUpper(strings.TrimSpace(in.Codigo))
	if codigo == "" {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Debe indicar un código")
		return
	}
	g, err := h.grupos.UnirsePorCodigo(r.Context(), claims.UsuarioID, codigo)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Código inválido")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo procesar la inscripción")
		return
	}
	escribirJSON(w, http.StatusOK, grupoRespDe(g))
}

// obtenerPropioGrupo verifica que el grupo exista y pertenezca al profesor
// autenticado (RN-06). Grupos de otro profesor responden 404, no 403.
func (h *grupoHandler) obtenerPropioGrupo(w http.ResponseWriter, r *http.Request, grupoID, profesorID string) (domain.Grupo, bool) {
	g, err := h.grupos.PorID(r.Context(), grupoID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Grupo no encontrado")
		return domain.Grupo{}, false
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el grupo")
		return domain.Grupo{}, false
	}
	if g.ProfesorID != profesorID {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Grupo no encontrado")
		return domain.Grupo{}, false
	}
	return g, true
}

type miembroGrupoResp struct {
	EstudianteID  string    `json:"estudiante_id"`
	Nombre        string    `json:"nombre"`
	FechaUnion    time.Time `json:"fecha_union"`
	TotalEnsayos  int       `json:"total_ensayos"`
	UltimoPuntaje *int      `json:"ultimo_puntaje,omitempty"`
}

func (h *grupoHandler) cargarMiembrosConResumen(ctx context.Context, grupoID string) ([]miembroGrupoResp, error) {
	basicos, err := h.grupos.Miembros(ctx, grupoID)
	if err != nil {
		return nil, err
	}
	ids := make([]string, len(basicos))
	for i, m := range basicos {
		ids[i] = m.EstudianteID
	}
	resumen, err := h.ensayos.ResumenPorEstudiantes(ctx, ids)
	if err != nil {
		return nil, err
	}
	out := make([]miembroGrupoResp, 0, len(basicos))
	for _, m := range basicos {
		re := resumen[m.EstudianteID]
		out = append(out, miembroGrupoResp{
			EstudianteID: m.EstudianteID, Nombre: m.Nombre, FechaUnion: m.FechaUnion,
			TotalEnsayos: re.TotalEnsayos, UltimoPuntaje: re.UltimoPuntaje,
		})
	}
	return out, nil
}

func desgloseRespDe(items []domain.ItemResultado) []desgloseEjeResp {
	desglose := domain.CalcularDesglosePorEje(items)
	out := make([]desgloseEjeResp, 0, len(desglose))
	for _, d := range desglose {
		out = append(out, desgloseEjeResp{Eje: d.Eje, Correctas: d.Correctas, Total: d.Total, PuntosObtenidos: d.PuntosObtenidos, PuntosPosibles: d.PuntosPosibles})
	}
	return out
}

func (h *grupoHandler) obtener(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "grupoId")
	g, ok := h.obtenerPropioGrupo(w, r, id, claims.UsuarioID)
	if !ok {
		return
	}

	miembros, err := h.cargarMiembrosConResumen(r.Context(), id)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el progreso del grupo")
		return
	}
	ids := make([]string, len(miembros))
	for i, m := range miembros {
		ids[i] = m.EstudianteID
	}

	promedio, err := h.ensayos.PromedioPuntaje(r.Context(), ids)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el promedio del grupo")
		return
	}
	items, err := h.ensayos.DesempenoPorEje(r.Context(), ids)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el desempeño por eje")
		return
	}

	escribirJSON(w, http.StatusOK, map[string]any{
		"id":                g.ID,
		"nombre":            g.Nombre,
		"codigo_invitacion": g.CodigoInvitacion,
		"profesor_id":       g.ProfesorID,
		"fecha_creacion":    g.FechaCreacion,
		"cantidad_miembros": len(miembros),
		"promedio_grupo":    promedio,
		"desempeno_por_eje": desgloseRespDe(items),
	})
}

func (h *grupoHandler) miembros(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "grupoId")
	if _, ok := h.obtenerPropioGrupo(w, r, id, claims.UsuarioID); !ok {
		return
	}
	miembros, err := h.cargarMiembrosConResumen(r.Context(), id)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener los miembros")
		return
	}
	escribirJSON(w, http.StatusOK, miembros)
}

func (h *grupoHandler) progresoEstudiante(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	grupoID := chi.URLParam(r, "grupoId")
	estudianteID := chi.URLParam(r, "estudianteId")
	if _, ok := h.obtenerPropioGrupo(w, r, grupoID, claims.UsuarioID); !ok {
		return
	}

	esMiembro, err := h.grupos.EsMiembro(r.Context(), grupoID, estudianteID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al verificar la membresía")
		return
	}
	if !esMiembro {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "El estudiante no pertenece a este grupo")
		return
	}

	basicos, err := h.grupos.Miembros(r.Context(), grupoID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el estudiante")
		return
	}
	var nombre string
	var fechaUnion time.Time
	for _, m := range basicos {
		if m.EstudianteID == estudianteID {
			nombre, fechaUnion = m.Nombre, m.FechaUnion
			break
		}
	}

	resumen, err := h.ensayos.ResumenPorEstudiantes(r.Context(), []string{estudianteID})
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el resumen")
		return
	}
	re := resumen[estudianteID]

	finalizados, err := h.ensayos.FinalizadosPorEstudiante(r.Context(), estudianteID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular la evolución")
		return
	}
	evolucion := make([]puntoEvolucionResp, 0, len(finalizados))
	for _, e := range finalizados {
		if e.FechaFin == nil {
			continue
		}
		evolucion = append(evolucion, puntoEvolucionResp{Fecha: *e.FechaFin, Puntaje: valorInt(e.Puntaje)})
	}

	items, err := h.ensayos.DesempenoPorEje(r.Context(), []string{estudianteID})
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el desempeño por eje")
		return
	}

	escribirJSON(w, http.StatusOK, map[string]any{
		"estudiante": miembroGrupoResp{
			EstudianteID: estudianteID, Nombre: nombre, FechaUnion: fechaUnion,
			TotalEnsayos: re.TotalEnsayos, UltimoPuntaje: re.UltimoPuntaje,
		},
		"evolucion":         evolucion,
		"desempeno_por_eje": desgloseRespDe(items),
	})
}

type grupoEstudianteResp struct {
	ID             string    `json:"id"`
	Nombre         string    `json:"nombre"`
	ProfesorNombre string    `json:"profesor_nombre"`
	FechaUnion     time.Time `json:"fecha_union"`
}

func (h *grupoHandler) misGrupos(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	lista, err := h.grupos.ListarPorEstudiante(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los grupos")
		return
	}
	out := make([]grupoEstudianteResp, 0, len(lista))
	for _, g := range lista {
		out = append(out, grupoEstudianteResp{ID: g.ID, Nombre: g.Nombre, ProfesorNombre: g.ProfesorNombre, FechaUnion: g.FechaUnion})
	}
	escribirJSON(w, http.StatusOK, out)
}

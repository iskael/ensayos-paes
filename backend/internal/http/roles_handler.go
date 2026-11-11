package httpx

import (
	"errors"
	"net/http"
	"strings"

	"github.com/go-chi/chi/v5"

	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type codigoReq struct {
	Codigo string `json:"codigo"`
}

func codigoNormalizado(w http.ResponseWriter, r *http.Request) (string, bool) {
	var in codigoReq
	if !decodificar(w, r, &in) {
		return "", false
	}
	codigo := strings.ToUpper(strings.TrimSpace(in.Codigo))
	if codigo == "" {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Debe indicar un código")
		return "", false
	}
	return codigo, true
}

// ---------------- Apoderados ----------------

type apoderadoHandler struct {
	vinculos  *repo.Vinculos
	ensayos   *repo.Ensayos
	dashboard *dashboardHandler
}

func (h *apoderadoHandler) codigo(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	c, err := h.vinculos.CodigoVigente(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener el código")
		return
	}
	escribirJSON(w, http.StatusOK, c)
}

func (h *apoderadoHandler) nuevoCodigo(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	c, err := h.vinculos.NuevoCodigo(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo generar el código")
		return
	}
	escribirJSON(w, http.StatusOK, c)
}

func (h *apoderadoHandler) misApoderados(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	lista, err := h.vinculos.Apoderados(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los apoderados")
		return
	}
	escribirJSON(w, http.StatusOK, lista)
}

func (h *apoderadoHandler) quitarApoderado(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	h.responderDesvinculo(w, h.vinculos.Desvincular(r.Context(), chi.URLParam(r, "apoderadoId"), claims.UsuarioID))
}

func (h *apoderadoHandler) vincular(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	codigo, ok := codigoNormalizado(w, r)
	if !ok {
		return
	}
	p, err := h.vinculos.Vincular(r.Context(), claims.UsuarioID, codigo)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Código inválido o vencido")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo vincular")
		return
	}
	escribirJSON(w, http.StatusOK, p)
}

type pupiloResp struct {
	repo.PersonaVinculada
	TotalEnsayos  int  `json:"total_ensayos"`
	UltimoPuntaje *int `json:"ultimo_puntaje,omitempty"`
}

func (h *apoderadoHandler) pupilos(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	lista, err := h.vinculos.Pupilos(r.Context(), claims.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los estudiantes")
		return
	}
	ids := make([]string, len(lista))
	for i, p := range lista {
		ids[i] = p.ID
	}
	resumen, err := h.ensayos.ResumenPorEstudiantes(r.Context(), ids)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo calcular el resumen")
		return
	}
	out := make([]pupiloResp, 0, len(lista))
	for _, p := range lista {
		re := resumen[p.ID]
		out = append(out, pupiloResp{PersonaVinculada: p, TotalEnsayos: re.TotalEnsayos, UltimoPuntaje: re.UltimoPuntaje})
	}
	escribirJSON(w, http.StatusOK, out)
}

func (h *apoderadoHandler) desvincular(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	h.responderDesvinculo(w, h.vinculos.Desvincular(r.Context(), claims.UsuarioID, chi.URLParam(r, "estudianteId")))
}

func (h *apoderadoHandler) responderDesvinculo(w http.ResponseWriter, err error) {
	switch {
	case errors.Is(err, repo.ErrNoEncontrado):
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Vínculo no encontrado")
	case err != nil:
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo quitar el vínculo")
	default:
		w.WriteHeader(http.StatusNoContent)
	}
}

// pupiloPropio responde 404 si el estudiante no está vinculado al apoderado (no revela si existe).
func (h *apoderadoHandler) pupiloPropio(w http.ResponseWriter, r *http.Request) (string, bool) {
	claims, _ := claimsDe(r.Context())
	estudianteID := chi.URLParam(r, "estudianteId")
	ok, err := h.vinculos.EsApoderadoDe(r.Context(), claims.UsuarioID, estudianteID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar el vínculo")
		return "", false
	}
	if !ok {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Estudiante no encontrado")
		return "", false
	}
	return estudianteID, true
}

func (h *apoderadoHandler) resumenPupilo(w http.ResponseWriter, r *http.Request) {
	if id, ok := h.pupiloPropio(w, r); ok {
		h.dashboard.resumenDe(w, r, id)
	}
}

func (h *apoderadoHandler) evolucionPupilo(w http.ResponseWriter, r *http.Request) {
	if id, ok := h.pupiloPropio(w, r); ok {
		h.dashboard.evolucionDe(w, r, id)
	}
}

// ---------------- Instituciones ----------------

type institucionHandler struct {
	instituciones *repo.Instituciones
	grupos        *grupoHandler
}

type nombreReq struct {
	Nombre string `json:"nombre"`
}

func nombreValido(w http.ResponseWriter, r *http.Request) (string, bool) {
	var in nombreReq
	if !decodificar(w, r, &in) {
		return "", false
	}
	nombre := strings.TrimSpace(in.Nombre)
	if nombre == "" || len(nombre) > 120 {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El nombre es obligatorio (máximo 120 caracteres)")
		return "", false
	}
	return nombre, true
}

func (h *institucionHandler) propia(w http.ResponseWriter, r *http.Request) (repo.Institucion, bool) {
	claims, _ := claimsDe(r.Context())
	inst, err := h.instituciones.DeResponsable(r.Context(), claims.UsuarioID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Aún no has creado tu institución")
		return repo.Institucion{}, false
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener la institución")
		return repo.Institucion{}, false
	}
	return inst, true
}

func (h *institucionHandler) crear(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	nombre, ok := nombreValido(w, r)
	if !ok {
		return
	}
	inst, err := h.instituciones.Crear(r.Context(), nombre, claims.UsuarioID)
	if errors.Is(err, repo.ErrYaExiste) {
		escribirError(w, http.StatusConflict, "CONFLICTO", "Ya tienes una institución")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear la institución")
		return
	}
	escribirJSON(w, http.StatusCreated, inst)
}

func (h *institucionHandler) obtener(w http.ResponseWriter, r *http.Request) {
	inst, ok := h.propia(w, r)
	if !ok {
		return
	}
	profesores, err := h.instituciones.Profesores(r.Context(), inst.ID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los profesores")
		return
	}
	grupos, err := h.instituciones.Grupos(r.Context(), inst.ID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los grupos")
		return
	}
	escribirJSON(w, http.StatusOK, map[string]any{"institucion": inst, "profesores": profesores, "grupos": grupos})
}

func (h *institucionHandler) renombrar(w http.ResponseWriter, r *http.Request) {
	inst, ok := h.propia(w, r)
	if !ok {
		return
	}
	nombre, ok := nombreValido(w, r)
	if !ok {
		return
	}
	if err := h.instituciones.Renombrar(r.Context(), inst.ID, nombre); err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo renombrar")
		return
	}
	inst.Nombre = nombre
	escribirJSON(w, http.StatusOK, inst)
}

func (h *institucionHandler) nuevoCodigo(w http.ResponseWriter, r *http.Request) {
	inst, ok := h.propia(w, r)
	if !ok {
		return
	}
	codigo, err := h.instituciones.NuevoCodigo(r.Context(), inst.ID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo generar el código")
		return
	}
	inst.CodigoInvitacion = codigo
	escribirJSON(w, http.StatusOK, inst)
}

func (h *institucionHandler) quitarProfesor(w http.ResponseWriter, r *http.Request) {
	inst, ok := h.propia(w, r)
	if !ok {
		return
	}
	err := h.instituciones.QuitarProfesor(r.Context(), inst.ID, chi.URLParam(r, "profesorId"))
	switch {
	case errors.Is(err, repo.ErrNoEncontrado):
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Profesor no encontrado en la institución")
	case err != nil:
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo quitar al profesor")
	default:
		w.WriteHeader(http.StatusNoContent)
	}
}

func (h *institucionHandler) grupo(w http.ResponseWriter, r *http.Request) {
	inst, ok := h.propia(w, r)
	if !ok {
		return
	}
	grupoID := chi.URLParam(r, "grupoId")
	es, err := h.instituciones.TieneGrupo(r.Context(), inst.ID, grupoID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar el grupo")
		return
	}
	if !es {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Grupo no encontrado")
		return
	}
	g, err := h.grupos.grupos.PorID(r.Context(), grupoID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener el grupo")
		return
	}
	miembros, err := h.grupos.cargarMiembrosConResumen(r.Context(), grupoID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener los miembros")
		return
	}
	escribirJSON(w, http.StatusOK, map[string]any{"id": g.ID, "nombre": g.Nombre, "miembros": miembros})
}

func (h *institucionHandler) deProfesor(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	inst, err := h.instituciones.DeProfesor(r.Context(), claims.UsuarioID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "No perteneces a ninguna institución")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener la institución")
		return
	}
	escribirJSON(w, http.StatusOK, inst)
}

func (h *institucionHandler) unirseProfesor(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	codigo, ok := codigoNormalizado(w, r)
	if !ok {
		return
	}
	inst, err := h.instituciones.UnirseProfesor(r.Context(), claims.UsuarioID, codigo)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Código inválido")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo unir a la institución")
		return
	}
	escribirJSON(w, http.StatusOK, inst)
}

func (h *institucionHandler) salirProfesor(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	inst, err := h.instituciones.DeProfesor(r.Context(), claims.UsuarioID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "No perteneces a ninguna institución")
		return
	}
	if err == nil {
		err = h.instituciones.QuitarProfesor(r.Context(), inst.ID, claims.UsuarioID)
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo salir de la institución")
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ---------------- Admin: usuarios y roles ----------------

type usuariosAdminHandler struct {
	usuarios *repo.Usuarios
}

func (h *usuariosAdminHandler) listar(w http.ResponseWriter, r *http.Request) {
	limit, offset := paginacion(r)
	lista, err := h.usuarios.Listar(r.Context(), strings.TrimSpace(r.URL.Query().Get("buscar")), limit, offset)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar los usuarios")
		return
	}
	escribirJSON(w, http.StatusOK, lista)
}

type cambiarRolReq struct {
	Rol string `json:"rol"`
}

func (h *usuariosAdminHandler) cambiarRol(w http.ResponseWriter, r *http.Request) {
	claims, _ := claimsDe(r.Context())
	id := chi.URLParam(r, "usuarioId")
	var in cambiarRolReq
	if !decodificar(w, r, &in) {
		return
	}
	rol := domain.Rol(in.Rol)
	if !rol.AsignablePorAdmin() {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Rol inválido (los admin se crean con seed-admin)")
		return
	}
	if id == claims.UsuarioID {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "No puedes cambiar tu propio rol")
		return
	}
	u, err := h.usuarios.CambiarRol(r.Context(), id, rol)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Usuario no encontrado o es admin")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo cambiar el rol")
		return
	}
	escribirJSON(w, http.StatusOK, u)
}

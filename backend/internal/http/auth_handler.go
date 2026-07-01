package httpx

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type authHandler struct {
	usuarios *repo.Usuarios
	jwt      *auth.Manager
}

type registroReq struct {
	Nombre         string `json:"nombre"`
	Email          string `json:"email"`
	Password       string `json:"password"`
	Rol            string `json:"rol"`
	AceptaTerminos bool   `json:"acepta_terminos"`
}

type loginReq struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type tokenResp struct {
	Token   string         `json:"token"`
	Usuario domain.Usuario `json:"usuario"`
}

func (h *authHandler) registrar(w http.ResponseWriter, r *http.Request) {
	var req registroReq
	if !decodificar(w, r, &req) {
		return
	}
	req.Nombre = strings.TrimSpace(req.Nombre)
	req.Email = strings.ToLower(strings.TrimSpace(req.Email))

	if req.Nombre == "" || !strings.Contains(req.Email, "@") || len(req.Password) < 8 {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Datos de registro inválidos")
		return
	}
	if !req.AceptaTerminos {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Debe aceptar los Términos y Condiciones para registrarse")
		return
	}
	rol := domain.Rol(req.Rol)
	if rol != domain.RolEstudiante && rol != domain.RolProfesor {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Rol inválido para registro")
		return
	}

	hash, err := auth.HashPassword(req.Password)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo procesar la contraseña")
		return
	}

	u, err := h.usuarios.Crear(r.Context(), req.Nombre, req.Email, hash, rol, domain.VersionTerminosActual)
	if errors.Is(err, repo.ErrEmailDuplicado) {
		escribirError(w, http.StatusConflict, "EMAIL_DUPLICADO", "El email ya está registrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear el usuario")
		return
	}

	token, err := h.jwt.Emitir(u.ID, string(u.Rol))
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo emitir el token")
		return
	}
	escribirJSON(w, http.StatusCreated, tokenResp{Token: token, Usuario: u})
}

func (h *authHandler) login(w http.ResponseWriter, r *http.Request) {
	var req loginReq
	if !decodificar(w, r, &req) {
		return
	}
	req.Email = strings.ToLower(strings.TrimSpace(req.Email))

	u, hash, err := h.usuarios.PorEmail(r.Context(), req.Email)
	if err != nil || !auth.VerifyPassword(hash, req.Password) {
		escribirError(w, http.StatusUnauthorized, "CREDENCIALES", "Email o contraseña incorrectos")
		return
	}
	token, err := h.jwt.Emitir(u.ID, string(u.Rol))
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo emitir el token")
		return
	}
	escribirJSON(w, http.StatusOK, tokenResp{Token: token, Usuario: u})
}

// logout: con JWT sin estado, el cliente descarta el token.
func (h *authHandler) logout(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}

func (h *authHandler) me(w http.ResponseWriter, r *http.Request) {
	c, ok := claimsDe(r.Context())
	if !ok {
		escribirError(w, http.StatusUnauthorized, "NO_AUTORIZADO", "No autenticado")
		return
	}
	u, err := h.usuarios.PorID(r.Context(), c.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Usuario no encontrado")
		return
	}
	escribirJSON(w, http.StatusOK, u)
}

func decodificar(w http.ResponseWriter, r *http.Request, v any) bool {
	if err := json.NewDecoder(r.Body).Decode(v); err != nil {
		escribirError(w, http.StatusBadRequest, "JSON", "Cuerpo de solicitud inválido")
		return false
	}
	return true
}

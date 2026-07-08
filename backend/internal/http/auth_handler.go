package httpx

import (
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"strings"

	"github.com/go-chi/chi/v5"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/mailer"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type authHandler struct {
	usuarios       *repo.Usuarios
	jwt            *auth.Manager
	mailer         *mailer.Mailer
	verificaciones *repo.Verificaciones
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

type mensajeResp struct {
	Mensaje string `json:"mensaje"`
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

	h.enviarCorreoVerificacion(r, u)

	escribirJSON(w, http.StatusCreated, mensajeResp{
		Mensaje: "Te registraste correctamente. Revisá tu correo para verificar tu cuenta antes de iniciar sesión.",
	})
}

// enviarCorreoVerificacion genera el token y envía el correo. Un error acá
// se loguea pero NUNCA se propaga — no debe hacer fallar el registro.
func (h *authHandler) enviarCorreoVerificacion(r *http.Request, u domain.Usuario) {
	token, err := h.verificaciones.Crear(r.Context(), u.ID)
	if err != nil {
		log.Printf("no se pudo generar el token de verificación para %s: %v", u.Email, err)
		return
	}
	if err := h.mailer.EnviarVerificacion(u.Email, u.Nombre, token); err != nil {
		log.Printf("no se pudo enviar el correo de verificación a %s: %v", u.Email, err)
	}
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
	if !u.EmailVerificado {
		escribirError(w, http.StatusForbidden, "EMAIL_NO_VERIFICADO", "Debes verificar tu email antes de iniciar sesión")
		return
	}
	token, err := h.jwt.Emitir(u.ID, string(u.Rol))
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo emitir el token")
		return
	}
	escribirJSON(w, http.StatusOK, tokenResp{Token: token, Usuario: u})
}

type verificarEmailReq struct {
	Token string `json:"token"`
}

func (h *authHandler) verificarEmail(w http.ResponseWriter, r *http.Request) {
	var req verificarEmailReq
	if !decodificar(w, r, &req) {
		return
	}
	if _, err := h.verificaciones.Consumir(r.Context(), req.Token); err != nil {
		if errors.Is(err, repo.ErrTokenInvalido) {
			escribirError(w, http.StatusUnprocessableEntity, "TOKEN_INVALIDO", "El link de verificación es inválido o expiró")
			return
		}
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar el email")
		return
	}
	escribirJSON(w, http.StatusOK, mensajeResp{Mensaje: "Email verificado correctamente"})
}

type reenviarVerificacionReq struct {
	Email string `json:"email"`
}

// reenviarVerificacion siempre responde 200 con el mismo mensaje genérico,
// exista o no la cuenta, y esté o no ya verificada — no revela el estado
// de una cuenta a quien hace la consulta.
func (h *authHandler) reenviarVerificacion(w http.ResponseWriter, r *http.Request) {
	var req reenviarVerificacionReq
	if !decodificar(w, r, &req) {
		return
	}
	email := strings.ToLower(strings.TrimSpace(req.Email))

	u, _, err := h.usuarios.PorEmail(r.Context(), email)
	if err == nil && !u.EmailVerificado {
		h.enviarCorreoVerificacion(r, u)
	}

	escribirJSON(w, http.StatusOK, mensajeResp{
		Mensaje: "Si el correo está registrado y pendiente de verificar, te enviamos un nuevo link.",
	})
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

func (h *authHandler) verificarEmailAdmin(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "usuarioId")
	u, err := h.usuarios.MarcarVerificado(r.Context(), id)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Usuario no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar la cuenta")
		return
	}
	escribirJSON(w, http.StatusOK, u)
}

package httpx

import (
	"context"
	"net/http"
	"strings"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/domain"
)

type ctxKey int

const claimsKey ctxKey = 0

func claimsDe(ctx context.Context) (*auth.Claims, bool) {
	c, ok := ctx.Value(claimsKey).(*auth.Claims)
	return c, ok
}

// Autenticar exige un JWT válido y guarda los claims en el contexto.
func Autenticar(m *auth.Manager) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			h := r.Header.Get("Authorization")
			if !strings.HasPrefix(h, "Bearer ") {
				escribirError(w, http.StatusUnauthorized, "NO_AUTORIZADO", "No autenticado")
				return
			}
			claims, err := m.Validar(strings.TrimPrefix(h, "Bearer "))
			if err != nil {
				escribirError(w, http.StatusUnauthorized, "NO_AUTORIZADO", "Token inválido o expirado")
				return
			}
			ctx := context.WithValue(r.Context(), claimsKey, claims)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

// RequerirRol restringe el acceso a los roles indicados.
func RequerirRol(roles ...domain.Rol) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			c, ok := claimsDe(r.Context())
			if !ok {
				escribirError(w, http.StatusUnauthorized, "NO_AUTORIZADO", "No autenticado")
				return
			}
			for _, rol := range roles {
				if string(rol) == c.Rol {
					next.ServeHTTP(w, r)
					return
				}
			}
			escribirError(w, http.StatusForbidden, "PROHIBIDO", "El rol no tiene permiso para esta acción")
		})
	}
}

// CabecerasSeguridad agrega cabeceras defensivas estándar a toda respuesta.
func CabecerasSeguridad(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("X-Frame-Options", "DENY")
		w.Header().Set("Referrer-Policy", "no-referrer")
		next.ServeHTTP(w, r)
	})
}

// LimitarBodyGlobal es un tope defensivo aplicado a TODA request (backstop
// contra payloads de cientos de MB). Los endpoints multipart (imágenes,
// PDF) aplican su propio límite más estricto por ruta; como MaxBytesReader
// anida y prevalece el límite más chico, esto no afecta esos casos mientras
// maxBytes se mantenga por encima de sus límites (5MB / 20MB).
func LimitarBodyGlobal(maxBytes int64) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			r.Body = http.MaxBytesReader(w, r.Body, maxBytes)
			next.ServeHTTP(w, r)
		})
	}
}

// CORS habilita llamadas desde el origen del frontend. allowedOrigins puede
// ser "*" (cualquier origen), un origen específico, o una lista separada por
// comas (ej. "http://localhost:5173,http://192.168.0.190"): el backend
// refleja el origen de la request solo si está en la lista.
func CORS(allowedOrigins string) func(http.Handler) http.Handler {
	esComodin := allowedOrigins == "*"
	var origenes []string
	if !esComodin {
		for _, o := range strings.Split(allowedOrigins, ",") {
			o = strings.TrimSpace(o)
			if o != "" {
				origenes = append(origenes, o)
			}
		}
	}
	permitido := func(origen string) bool {
		for _, o := range origenes {
			if o == origen {
				return true
			}
		}
		return false
	}

	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			origen := r.Header.Get("Origin")
			switch {
			case esComodin:
				w.Header().Set("Access-Control-Allow-Origin", "*")
			case origen != "" && permitido(origen):
				w.Header().Set("Access-Control-Allow-Origin", origen)
				w.Header().Set("Vary", "Origin")
			}
			w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
			w.Header().Set("Access-Control-Allow-Headers", "Authorization, Content-Type")
			if r.Method == http.MethodOptions {
				w.WriteHeader(http.StatusNoContent)
				return
			}
			next.ServeHTTP(w, r)
		})
	}
}

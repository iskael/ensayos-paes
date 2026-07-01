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

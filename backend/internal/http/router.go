package httpx

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type Deps struct {
	Usuarios *repo.Usuarios
	JWT      *auth.Manager
}

func New(d Deps) http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)

	r.Get("/health", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	h := &authHandler{usuarios: d.Usuarios, jwt: d.JWT}

	r.Route("/api/v1", func(api chi.Router) {
		api.Post("/auth/register", h.registrar)
		api.Post("/auth/login", h.login)

		api.Group(func(priv chi.Router) {
			priv.Use(Autenticar(d.JWT))
			priv.Post("/auth/logout", h.logout)
			priv.Get("/me", h.me)
		})
	})

	return r
}

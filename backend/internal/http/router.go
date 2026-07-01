package httpx

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
	"github.com/usuario/ensayos-paes/internal/storage"
)

type Deps struct {
	Usuarios   *repo.Usuarios
	Examenes   *repo.Examenes
	Items      *repo.Items
	Clave      *repo.Clave
	Ensayos    *repo.Ensayos
	Imagenes   *storage.Imagenes
	UploadsDir string
	JWT        *auth.Manager
}

func New(d Deps) http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)

	r.Get("/health", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	if d.UploadsDir != "" {
		fs := http.StripPrefix("/uploads/", http.FileServer(http.Dir(d.UploadsDir)))
		r.Handle("/uploads/*", fs)
	}

	authH := &authHandler{usuarios: d.Usuarios, jwt: d.JWT}
	bancoH := &bancoHandler{examenes: d.Examenes, items: d.Items, clave: d.Clave, imagenes: d.Imagenes}
	ensayoH := &ensayoHandler{ensayos: d.Ensayos}
	dashboardH := &dashboardHandler{ensayos: d.Ensayos}

	r.Route("/api/v1", func(api chi.Router) {
		api.Post("/auth/register", authH.registrar)
		api.Post("/auth/login", authH.login)

		api.Group(func(priv chi.Router) {
			priv.Use(Autenticar(d.JWT))

			priv.Post("/auth/logout", authH.logout)
			priv.Get("/me", authH.me)

			priv.Group(func(admin chi.Router) {
				admin.Use(RequerirRol(domain.RolAdmin))

				admin.Route("/examenes", func(e chi.Router) {
					e.Post("/", bancoH.crearExamen)
					e.Get("/", bancoH.listarExamenes)
					e.Route("/{examenId}", func(er chi.Router) {
						er.Get("/", bancoH.obtenerExamen)
						er.Put("/", bancoH.actualizarExamen)
						er.Delete("/", bancoH.eliminarExamen)
						er.Get("/clave", bancoH.obtenerClave)
						er.Put("/clave", bancoH.definirClave)
					})
				})

				admin.Route("/items", func(it chi.Router) {
					it.Post("/", bancoH.crearItem)
					it.Get("/", bancoH.listarItems)
					it.Route("/{itemId}", func(ir chi.Router) {
						ir.Get("/", bancoH.obtenerItem)
						ir.Put("/", bancoH.actualizarItem)
						ir.Delete("/", bancoH.eliminarItem)
						ir.Post("/publicar", bancoH.publicarItem)
						ir.Post("/ocultar", bancoH.ocultarItem)
					})
				})

				admin.Post("/imagenes", bancoH.subirImagen)
			})

			priv.Group(func(est chi.Router) {
				est.Use(RequerirRol(domain.RolEstudiante))

				est.Route("/ensayos", func(en chi.Router) {
					en.Post("/", ensayoH.crear)
					en.Get("/", ensayoH.listar)
					en.Route("/{ensayoId}", func(er chi.Router) {
						er.Get("/", ensayoH.obtener)
						er.Patch("/respuestas", ensayoH.guardarRespuestas)
						er.Post("/enviar", ensayoH.enviar)
						er.Get("/resultado", ensayoH.resultado)
					})
				})

				est.Route("/dashboard", func(dh chi.Router) {
					dh.Get("/resumen", dashboardH.resumen)
					dh.Get("/evolucion", dashboardH.evolucion)
				})
			})
		})
	})

	return r
}

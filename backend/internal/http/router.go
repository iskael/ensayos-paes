package httpx

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/mailer"
	"github.com/usuario/ensayos-paes/internal/repo"
	"github.com/usuario/ensayos-paes/internal/storage"
)

type Deps struct {
	Usuarios       *repo.Usuarios
	Examenes       *repo.Examenes
	Items          *repo.Items
	Clave          *repo.Clave
	Ensayos        *repo.Ensayos
	Grupos         *repo.Grupos
	Verificaciones *repo.Verificaciones
	Imagenes       *storage.Imagenes
	Mailer         *mailer.Mailer
	UploadsDir     string
	JWT            *auth.Manager
	AllowedOrigin  string
}

func New(d Deps) http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(CabecerasSeguridad)
	r.Use(CORS(d.AllowedOrigin))
	r.Use(LimitarBodyGlobal(25 << 20)) // backstop; los endpoints multipart aplican su propio límite más estricto

	r.Get("/health", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	if d.UploadsDir != "" {
		fs := http.StripPrefix("/uploads/", http.FileServer(http.Dir(d.UploadsDir)))
		r.Handle("/uploads/*", fs)
	}

	authH := &authHandler{usuarios: d.Usuarios, jwt: d.JWT, mailer: d.Mailer, verificaciones: d.Verificaciones}
	bancoH := &bancoHandler{examenes: d.Examenes, items: d.Items, clave: d.Clave, imagenes: d.Imagenes}
	ensayoH := &ensayoHandler{ensayos: d.Ensayos}
	dashboardH := &dashboardHandler{ensayos: d.Ensayos}
	grupoH := &grupoHandler{grupos: d.Grupos, ensayos: d.Ensayos}
	limitadorLogin := nuevoLimitadorTasa(10, time.Minute)
	limitadorReenvio := nuevoLimitadorTasa(5, time.Minute)

	r.Route("/api/v1", func(api chi.Router) {
		api.Post("/auth/register", authH.registrar)
		api.With(LimitarTasa(limitadorLogin)).Post("/auth/login", authH.login)
		api.Post("/auth/verificar-email", authH.verificarEmail)
		api.With(LimitarTasa(limitadorReenvio)).Post("/auth/reenviar-verificacion", authH.reenviarVerificacion)

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
						er.Post("/importacion-pdf", bancoH.importarPdf)
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
				admin.Post("/usuarios/{usuarioId}/verificar-email", authH.verificarEmailAdmin)
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

			// Grupos mezcla roles por endpoint (profesor: crear/listar/detalle;
			// estudiante: unirse), por eso se aplica RequerirRol con With() por
			// ruta en vez de un sub-grupo único.
			priv.Route("/grupos", func(gr chi.Router) {
				gr.With(RequerirRol(domain.RolProfesor)).Post("/", grupoH.crear)
				gr.With(RequerirRol(domain.RolProfesor)).Get("/", grupoH.listar)
				gr.With(RequerirRol(domain.RolEstudiante)).Post("/unirse", grupoH.unirse)
				gr.With(RequerirRol(domain.RolEstudiante)).Get("/mis-grupos", grupoH.misGrupos)

				gr.Route("/{grupoId}", func(gid chi.Router) {
					gid.Use(RequerirRol(domain.RolProfesor))
					gid.Get("/", grupoH.obtener)
					gid.Get("/miembros", grupoH.miembros)
					gid.Get("/estudiantes/{estudianteId}", grupoH.progresoEstudiante)
				})
			})
		})
	})

	return r
}

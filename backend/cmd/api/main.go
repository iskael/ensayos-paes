package main

import (
	"context"
	"log"
	"net/http"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/config"
	"github.com/usuario/ensayos-paes/internal/db"
	httpx "github.com/usuario/ensayos-paes/internal/http"
	"github.com/usuario/ensayos-paes/internal/repo"
	"github.com/usuario/ensayos-paes/internal/storage"
)

func main() {
	cfg := config.Load()

	if cfg.JWTSecret == "cambiar-en-produccion" {
		log.Println("ADVERTENCIA: JWT_SECRET usa el valor por defecto. Configúrelo antes de desplegar a producción.")
	}
	if cfg.AllowedOrigin == "*" {
		log.Println("ADVERTENCIA: CORS_ALLOWED_ORIGIN='*' (cualquier origen). Configúrelo al dominio del frontend en producción.")
	}

	ctx := context.Background()
	pool, err := db.Connect(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("db: %v", err)
	}
	defer pool.Close()

	imagenes, err := storage.NewImagenes(cfg.UploadsDir, cfg.UploadsURL)
	if err != nil {
		log.Fatalf("storage: %v", err)
	}

	deps := httpx.Deps{
		Usuarios:      repo.NewUsuarios(pool),
		Examenes:      repo.NewExamenes(pool),
		Items:         repo.NewItems(pool),
		Clave:         repo.NewClave(pool),
		Ensayos:       repo.NewEnsayos(pool),
		Grupos:        repo.NewGrupos(pool),
		Imagenes:      imagenes,
		UploadsDir:    cfg.UploadsDir,
		JWT:           auth.NewManager(cfg.JWTSecret, cfg.JWTTTL),
		AllowedOrigin: cfg.AllowedOrigin,
	}
	handler := httpx.New(deps)

	log.Printf("API escuchando en :%s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, handler); err != nil {
		log.Fatal(err)
	}
}

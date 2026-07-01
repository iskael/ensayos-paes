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
)

func main() {
	cfg := config.Load()

	ctx := context.Background()
	pool, err := db.Connect(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("db: %v", err)
	}
	defer pool.Close()

	usuarios := repo.NewUsuarios(pool)
	jwtManager := auth.NewManager(cfg.JWTSecret, cfg.JWTTTL)
	handler := httpx.New(httpx.Deps{Usuarios: usuarios, JWT: jwtManager})

	log.Printf("API escuchando en :%s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, handler); err != nil {
		log.Fatal(err)
	}
}

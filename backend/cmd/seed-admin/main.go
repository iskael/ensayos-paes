// Comando seed-admin: crea un usuario con rol admin directamente en la base
// de datos. El registro público (POST /auth/register) solo permite
// estudiante/profesor a propósito; el admin se provisiona por esta vía.
//
// Uso:
//
//	go run ./cmd/seed-admin -email=admin@tuempresa.cl -password=UnaClaveSegura123
package main

import (
	"context"
	"flag"
	"fmt"
	"log"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/config"
	"github.com/usuario/ensayos-paes/internal/db"
	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/repo"
)

func main() {
	nombre := flag.String("nombre", "Administrador", "nombre del admin")
	email := flag.String("email", "", "email del admin (obligatorio)")
	password := flag.String("password", "", "contraseña del admin (obligatorio, mínimo 8 caracteres)")
	flag.Parse()

	if *email == "" || len(*password) < 8 {
		log.Fatal("uso: seed-admin -email=admin@ejemplo.com -password=algo-seguro (mínimo 8 caracteres)")
	}

	cfg := config.Load()
	ctx := context.Background()
	pool, err := db.Connect(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("db: %v", err)
	}
	defer pool.Close()

	hash, err := auth.HashPassword(*password)
	if err != nil {
		log.Fatalf("hash: %v", err)
	}

	usuarios := repo.NewUsuarios(pool)
	u, err := usuarios.Crear(ctx, *nombre, *email, hash, domain.RolAdmin, domain.VersionTerminosActual)
	if err != nil {
		log.Fatalf("crear admin: %v", err)
	}
	fmt.Printf("Admin creado: %s <%s> (id %s)\n", u.Nombre, u.Email, u.ID)
}

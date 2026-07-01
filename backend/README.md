# Backend — Ensayos PAES

## Puesta en marcha (Fase 0/1)

```bash
# 1) Dependencias
go mod tidy

# 2) Base de datos (Postgres) y migraciones
#    con golang-migrate:
migrate -path migrations -database "$DATABASE_URL" up

# 3) Variables de entorno (ver ../.env.example) y correr
go run ./cmd/api
```

## Endpoints disponibles (Fase 1)

- `GET  /health`
- `POST /api/v1/auth/register`  (rol: estudiante | profesor)
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`    (requiere Bearer token)
- `GET  /api/v1/me`             (requiere Bearer token)

## Estructura

- `cmd/api` — entrypoint.
- `internal/config` — configuración por entorno.
- `internal/db` — pool de conexión (pgx).
- `internal/domain` — entidades y reglas (Usuario, scoring).
- `internal/auth` — hashing y JWT.
- `internal/repo` — acceso a datos.
- `internal/http` — router, handlers y middleware (paquete `httpx`).
- `migrations` — esquema SQL.

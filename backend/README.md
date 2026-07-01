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

## Endpoints disponibles

**Fase 1 — Auth**
- `GET  /health`
- `POST /api/v1/auth/register`  (rol: estudiante | profesor)
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`    (requiere Bearer token)
- `GET  /api/v1/me`             (requiere Bearer token)

**Fase 2 — Banco de preguntas (requiere rol admin)**
- `POST/GET    /api/v1/examenes`
- `GET/PUT/DELETE /api/v1/examenes/{examenId}`
- `GET/PUT     /api/v1/examenes/{examenId}/clave`   (valida suma de pesos = 1000)
- `POST/GET    /api/v1/items`  (filtros: nivel, eje, dificultad, estado, examenId)
- `GET/PUT/DELETE /api/v1/items/{itemId}`
- `POST        /api/v1/items/{itemId}/publicar`
- `POST        /api/v1/items/{itemId}/ocultar`
- `POST        /api/v1/imagenes`  (multipart, campo `archivo`; sirve estático en `/uploads/*`)

## Estructura

- `cmd/api` — entrypoint.
- `internal/config` — configuración por entorno.
- `internal/db` — pool de conexión (pgx).
- `internal/domain` — entidades y reglas (Usuario, Item, Examen, scoring, clave).
- `internal/auth` — hashing y JWT.
- `internal/repo` — acceso a datos (usuarios, examenes, items, clave).
- `internal/storage` — almacenamiento local de imágenes.
- `internal/http` — router, handlers y middleware (paquete `httpx`).
- `migrations` — esquema SQL.

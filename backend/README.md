# Backend — Ensayos PAES

## Puesta en marcha (Fase 0/1)

```bash
# 0) Dependencia de Fase 6 (importación de PDF) — agregarla una vez:
go get github.com/ledongthuc/pdf@latest

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
- `POST        /api/v1/examenes/{examenId}/importacion-pdf`  (multipart: `archivo` (PDF) + `eje`, `dificultad` por defecto; crea ítems en `borrador`, ver Fase 6)

**Fase 3 — Ensayos (requiere rol estudiante)**
- `POST /api/v1/ensayos`  (nivel, ejes[], cantidad 10|20|30 → genera aleatorio; 422 `STOCK_INSUFICIENTE` si falta stock)
- `GET  /api/v1/ensayos`  (historial)
- `GET  /api/v1/ensayos/{ensayoId}`  (mientras está en progreso, sin revelar la respuesta correcta)
- `PATCH /api/v1/ensayos/{ensayoId}/respuestas`  (guarda progreso)
- `POST /api/v1/ensayos/{ensayoId}/enviar`  (corrige y devuelve el resultado)
- `GET  /api/v1/ensayos/{ensayoId}/resultado`  (puntaje 0–1000, revisión y desglose por eje)

**Fase 4 — Dashboard (requiere rol estudiante)**
- `GET /api/v1/dashboard/resumen`  (total de ensayos, último/mejor/promedio de puntaje, desempeño por eje)
- `GET /api/v1/dashboard/evolucion`  (serie fecha → puntaje, para el gráfico)

**Fase 5 — Grupos**
- `POST /api/v1/grupos`  (rol profesor; genera código de invitación)
- `GET  /api/v1/grupos`  (rol profesor; sus grupos)
- `POST /api/v1/grupos/unirse`  (rol estudiante; código → inscripción idempotente)
- `GET  /api/v1/grupos/{grupoId}`  (rol profesor dueño; detalle + progreso agregado)
- `GET  /api/v1/grupos/{grupoId}/miembros`  (rol profesor dueño)
- `GET  /api/v1/grupos/{grupoId}/estudiantes/{estudianteId}`  (rol profesor dueño; progreso individual)

## Estructura

- `cmd/api` — entrypoint.
- `internal/config` — configuración por entorno.
- `internal/db` — pool de conexión (pgx).
- `internal/domain` — entidades y reglas (Usuario, Item, Examen, scoring, clave).
- `internal/auth` — hashing y JWT.
- `internal/repo` — acceso a datos (usuarios, examenes, items, clave, ensayos, grupos).
- `internal/storage` — almacenamiento local de imágenes.
- `internal/pdfimport` — extracción de texto y segmentación heurística de preguntas desde PDF (Fase 6).
- `internal/http` — router, handlers y middleware (paquete `httpx`).
- `migrations` — esquema SQL.

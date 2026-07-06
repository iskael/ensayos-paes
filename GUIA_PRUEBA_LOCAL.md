# Guía de prueba local — Backend Ensayos PAES

Esta guía te lleva desde cero hasta tener el backend corriendo y validado con
un flujo completo de extremo a extremo.

---

## 1. Prerrequisitos

- **Go 1.22+**
- **PostgreSQL 13+** corriendo (Docker vía `make db-up`, local, o el que ya tengas en tu Proxmox)
- `psql` disponible (o cualquier cliente de Postgres)
- `curl` y `jq` (para el script de prueba end-to-end) — `apt install jq` / `brew install jq`
- Opcional: [`golang-migrate`](https://github.com/golang-migrate/migrate) CLI (si no lo tienes, aplicamos las migraciones a mano con `psql`, ver paso 4)

## 2. Crear la base de datos

**Opción A — Docker (recomendado, no requiere Postgres instalado):**

```bash
make db-up   # o: docker compose up -d
```

Levanta Postgres con las credenciales que ya trae `.env.example` por defecto
(`ensayos`/`ensayos`, db `ensayos_paes`).

**Opción B — Postgres propio (local o Proxmox):**

```bash
createdb ensayos_paes
# o, si prefieres psql directamente:
psql -c "CREATE DATABASE ensayos_paes;"
```

> Si tu PostgreSQL es **anterior a la versión 13**, ejecuta antes:
> `psql ensayos_paes -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"`
> (`gen_random_uuid()` es nativo desde PG 13; las migraciones lo usan para los IDs).

## 3. Variables de entorno

```bash
cd ensayos-paes
cp .env.example .env
```

Edita `.env` y ajusta al menos:
- `DATABASE_URL` — con tu usuario/password/host reales.
- `JWT_SECRET` — pon algo real, no dejes el valor por defecto (el servidor te lo va a recordar con una advertencia si lo olvidas).

Carga las variables en tu shell antes de correr el backend:
```bash
export $(grep -v '^#' .env | xargs)
```

## 4. Migraciones

Con `golang-migrate` instalado:
```bash
migrate -path backend/migrations -database "$DATABASE_URL" up
```

Sin `migrate`, aplicando a mano en orden (usando `psql`):
```bash
psql "$DATABASE_URL" -f backend/migrations/0001_init.up.sql
psql "$DATABASE_URL" -f backend/migrations/0002_terminos.up.sql
```

## 5. Dependencias y compilación

```bash
cd backend
go get github.com/ledongthuc/pdf@latest   # dependencia de Fase 6, una sola vez
go mod tidy
go build ./...
```

Si `go build` se queja de algo, es el primer lugar donde avisarme para que lo revisemos juntos.

## 6. Tests unitarios (sin necesitar Postgres)

```bash
go test ./...
```

Deberían pasar ~20 tests: scoring (puntaje 1000), validación de alternativas,
clave, distribución por eje, desglose por eje, y segmentación heurística de
PDF. Ninguno requiere una base de datos real — son pruebas de dominio puro.

## 7. Crear el primer administrador

El registro público (`POST /auth/register`) **solo permite `estudiante` o
`profesor` a propósito** — es una decisión de diseño, no un descuido. El
admin se crea por esta vía:

```bash
go run ./cmd/seed-admin -email=admin@tuempresa.cl -password=UnaClaveSegura123
```

Deberías ver: `Admin creado: Administrador <admin@tuempresa.cl> (id ...)`.

## 8. Levantar el servidor

```bash
go run ./cmd/api
```

Deberías ver `API escuchando en :8080` (y, si dejaste valores por defecto en
`JWT_SECRET` o `CORS_ALLOWED_ORIGIN`, una advertencia — normal en desarrollo).

Probar en otra terminal:
```bash
curl http://localhost:8080/health
# {"status":"ok"}
```

## 9. Prueba end-to-end automática

Con el servidor corriendo, en otra terminal:
```bash
cd backend
./scripts/smoke_test.sh admin@tuempresa.cl UnaClaveSegura123
```

Recorre automáticamente: registro (con y sin aceptar T&C), examen, 10 ítems
con alternativas, clave, publicación, generación de ensayo, respuestas,
corrección (debería dar **puntaje 1000**, ya que el script responde con la
alternativa marcada como correcta), resultado, dashboard, y grupos
(crear/unirse/consultar). Imprime cada paso con ✓ o ✗ y el detalle de la
respuesta si algo falla.

## 10. Qué revisar manualmente

- `backend/uploads/` — ahí quedan las imágenes que subas por `POST /imagenes`.
- Tabla `terminos_aceptados` — debería tener una fila por cada usuario que
  registró el script (profesor + estudiante + el admin del seed).
- Tabla `ensayo_items`, columna `peso_snapshot` — no debería cambiar aunque
  edites el ítem original después de generado el ensayo.
- Probar el rate limit: 11 intentos seguidos de `POST /auth/login` con
  password incorrecta deberían dar `429` en el último.

## 11. Problemas comunes

- **"connection refused" a Postgres:** revisa `DATABASE_URL` y que el
  servicio esté corriendo (`pg_isready` si lo tienes).
- **Error de tipo en columnas enum durante el primer `POST`:** si ves un
  error como *"column is of type X but expression is of type text"*,
  avísame — es el único punto que quedó marcado como "a verificar" en
  `LEARNINGS.md`, ya que no pude probarlo contra un Postgres real desde este
  entorno.
- **`go get` sin salida a internet:** revisa proxy/firewall; puede que
  necesites configurar `GOPROXY`.
- **`429` en login durante pruebas repetidas:** es el rate limiter (10
  intentos/min por IP); espera un minuto o reinicia el servidor.
- **El script de smoke test falla en el paso de stock:** si ya habías corrido
  el script antes y cambiaste algo a mano, puede que ya no haya 10 ítems
  disponibles de `eje=numeros, nivel=M1` publicados; revisa la tabla `items`.

## 12. Siguiente paso

Con esto validado, seguimos con el **frontend** (React + Vite, mobile-first).

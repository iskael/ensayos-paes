# Verificación de Email en el Registro Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** El registro deja de loguear automáticamente; el usuario debe confirmar un link enviado por correo (Gmail SMTP) antes de poder iniciar sesión, con reenvío, expiración a 24hs, y un endpoint admin-only para verificar cuentas manualmente sin correo.

**Architecture:** Contrato primero (OpenAPI), luego backend (migración → repo/domain → mailer → handlers → rutas), luego frontend (cliente API → páginas). El envío de correo usa `net/smtp` de la librería estándar de Go, sin dependencias nuevas.

**Tech Stack:** Mismo stack del proyecto (Go + chi + pgx; React 18 + react-router-dom). `net/smtp` (stdlib) para SMTP.

## Global Constraints

- Sin dependencias nuevas (ni Go ni npm).
- Nombres de funciones/variables/componentes en español.
- No reescribir archivos completos sin necesidad; ediciones parciales.
- El envío de correo NUNCA debe hacer fallar el registro — si falla, se loguea el error server-side y la cuenta se crea igual (mismo criterio que "avisos de arranque, no fallos duros" ya usado en el proyecto, `LEARNINGS.md` Fase 7).
- La migración debe marcar verificadas TODAS las cuentas existentes (`UPDATE usuarios SET email_verificado = TRUE` después del `ALTER TABLE ... DEFAULT FALSE`) — sin esto, el admin y cualquier cuenta ya creada quedarían bloqueadas.
- `reenviarVerificacion` nunca revela si un email existe o ya está verificado — responde el mismo mensaje genérico en todos los casos.
- El chequeo de `email_verificado` en login ocurre DESPUÉS de validar la contraseña (no antes) — no debe revelar el estado de una cuenta a alguien que no conoce la contraseña.
- El endpoint admin-only de verificación manual no lleva pantalla de frontend (uso operativo vía curl/Postman, mismo criterio que `cmd/seed-admin`).
- Sin verificación en vivo con cuentas reales de admin/profesor por parte del controller (misma restricción de las tandas anteriores, ver `LEARNINGS.md` Fases 10-11) — y a partir de esta tanda, tampoco con cuentas de estudiante recién auto-registradas (el registro ya no loguea automático).

---

### Task 1: Contrato OpenAPI

**Files:**
- Modify: `docs/openapi.yaml`

**Interfaces:**
- Produces: schemas `RegistroResponse { mensaje: string }`, `VerificarEmailRequest { token: string }`, `ReenviarVerificacionRequest { email: string }`, `MensajeResponse { mensaje: string }`; parámetro `UsuarioId`; `Usuario` con el campo nuevo `email_verificado: boolean`; paths nuevos `/auth/verificar-email`, `/auth/reenviar-verificacion`, `/admin/usuarios/{usuarioId}/verificar-email`.

- [ ] **Step 1: Cambiar la respuesta de `POST /auth/register`**

Reemplazar (líneas 44-51 de `docs/openapi.yaml`):

```yaml
      responses:
        '201':
          description: Usuario creado
          content:
            application/json:
              schema: { $ref: '#/components/schemas/TokenResponse' }
        '409': { $ref: '#/components/responses/Conflicto' }
        '422': { $ref: '#/components/responses/ValidacionFallida' }
```

por:

```yaml
      responses:
        '201':
          description: >
            Usuario creado (sin sesión iniciada — debe verificar su email
            antes de poder loguear)
          content:
            application/json:
              schema: { $ref: '#/components/schemas/RegistroResponse' }
        '409': { $ref: '#/components/responses/Conflicto' }
        '422': { $ref: '#/components/responses/ValidacionFallida' }
```

- [ ] **Step 2: Documentar el 403 de `POST /auth/login` y agregar los 2 paths nuevos de Auth**

Reemplazar el bloque `/auth/login` completo (líneas 53-70) por:

```yaml
  /auth/login:
    post:
      tags: [Auth]
      operationId: login
      summary: Iniciar sesión
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/LoginRequest' }
      responses:
        '200':
          description: Sesión iniciada
          content:
            application/json:
              schema: { $ref: '#/components/schemas/TokenResponse' }
        '401': { $ref: '#/components/responses/NoAutorizado' }
        '403':
          description: 'Email no verificado (codigo: EMAIL_NO_VERIFICADO)'
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }

  /auth/verificar-email:
    post:
      tags: [Auth]
      operationId: verificarEmail
      summary: Confirmar la cuenta con el token del correo de verificación
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/VerificarEmailRequest' }
      responses:
        '200':
          description: Email verificado
          content:
            application/json:
              schema: { $ref: '#/components/schemas/MensajeResponse' }
        '422':
          description: 'Token inválido o expirado (codigo: TOKEN_INVALIDO)'
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }

  /auth/reenviar-verificacion:
    post:
      tags: [Auth]
      operationId: reenviarVerificacion
      summary: Reenviar el correo de verificación
      description: >
        Siempre responde 200 con un mensaje genérico, exista o no la cuenta,
        y esté o no ya verificada — no revela el estado de una cuenta.
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/ReenviarVerificacionRequest' }
      responses:
        '200':
          description: Mensaje genérico (ver descripción)
          content:
            application/json:
              schema: { $ref: '#/components/schemas/MensajeResponse' }
```

- [ ] **Step 3: Agregar el endpoint admin-only de verificación manual**

Agregar este path junto a los demás de Banco (después de `/imagenes`, antes de `# ---------------- Grupos ----------------`):

```yaml
  /admin/usuarios/{usuarioId}/verificar-email:
    parameters:
      - { $ref: '#/components/parameters/UsuarioId' }
    post:
      tags: [Auth]
      operationId: verificarEmailAdmin
      summary: Verificar el email de una cuenta manualmente (rol admin, sin correo)
      description: Uso operativo (QA/soporte) — no tiene pantalla de frontend.
      responses:
        '200':
          description: Cuenta verificada
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Usuario' }
        '401': { $ref: '#/components/responses/NoAutorizado' }
        '403': { $ref: '#/components/responses/Prohibido' }
        '404': { $ref: '#/components/responses/NoEncontrado' }
```

- [ ] **Step 4: Agregar el parámetro `UsuarioId`**

Agregar junto a los demás parámetros (`GrupoId`, etc., dentro de `components/parameters`):

```yaml
    UsuarioId:
      name: usuarioId
      in: path
      required: true
      schema: { type: string, format: uuid }
```

- [ ] **Step 5: Agregar `email_verificado` a `Usuario` y los 4 schemas nuevos**

Reemplazar el schema `Usuario` existente (en `components/schemas`, bajo `# ---- Auth ----`):

```yaml
    Usuario:
      type: object
      properties:
        id: { type: string, format: uuid }
        nombre: { type: string }
        email: { type: string, format: email }
        rol: { $ref: '#/components/schemas/Rol' }
        email_verificado: { type: boolean }
        fecha_creacion: { type: string, format: date-time }
```

Agregar estos 4 schemas nuevos junto a `TokenResponse`/`Usuario`:

```yaml
    RegistroResponse:
      type: object
      properties:
        mensaje: { type: string }
    VerificarEmailRequest:
      type: object
      required: [token]
      properties:
        token: { type: string }
    ReenviarVerificacionRequest:
      type: object
      required: [email]
      properties:
        email: { type: string, format: email }
    MensajeResponse:
      type: object
      properties:
        mensaje: { type: string }
```

- [ ] **Step 6: Validar el YAML**

Si `openapi-spec-validator` está disponible:
```bash
python -m openapi_spec_validator docs/openapi.yaml
```
Expected: sin errores. Si la herramienta no está instalada, omitir este paso y decirlo en el reporte — no instalar nada nuevo.

- [ ] **Step 7: Commit**

```bash
git add docs/openapi.yaml
git commit -m "docs(openapi): contrato de verificacion de email"
git push origin main
```

---

### Task 2: Migración de base de datos

**Files:**
- Create: `backend/migrations/0003_verificacion_email.up.sql`
- Create: `backend/migrations/0003_verificacion_email.down.sql`

**Interfaces:**
- Produces: columna `usuarios.email_verificado BOOLEAN NOT NULL DEFAULT FALSE` (con las filas existentes puestas en `TRUE`); tabla `verificaciones_email (token TEXT PRIMARY KEY, usuario_id UUID NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE, fecha_expiracion TIMESTAMPTZ NOT NULL, fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now())`.

- [ ] **Step 1: Escribir `backend/migrations/0003_verificacion_email.up.sql`**

```sql
-- 0003_verificacion_email.up.sql — verificación de email en el registro

ALTER TABLE usuarios ADD COLUMN email_verificado BOOLEAN NOT NULL DEFAULT FALSE;

-- Las cuentas creadas antes de esta migración quedan verificadas: de lo
-- contrario, ningún usuario existente (incluido el admin) podría loguear.
UPDATE usuarios SET email_verificado = TRUE;

CREATE TABLE verificaciones_email (
    token             TEXT PRIMARY KEY,
    usuario_id        UUID NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_expiracion  TIMESTAMPTZ NOT NULL,
    fecha_creacion    TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

- [ ] **Step 2: Escribir `backend/migrations/0003_verificacion_email.down.sql`**

```sql
-- 0003_verificacion_email.down.sql

DROP TABLE verificaciones_email;
ALTER TABLE usuarios DROP COLUMN email_verificado;
```

- [ ] **Step 3: Verificar la sintaxis SQL leyendo el archivo con cuidado**

No hay una base de datos local disponible en este entorno para correr la
migración (Docker no está disponible localmente en esta sesión de
desarrollo). Releé ambos archivos línea por línea contra el estilo de
`backend/migrations/0001_init.up.sql`/`0002_terminos.up.sql` (mismo
proyecto, mismas convenciones de nombres de tabla/columna en snake_case,
mismo estilo de `UUID PRIMARY KEY`/`REFERENCES ... ON DELETE CASCADE`) y
confirmá que no hay errores de sintaxis obvios (paréntesis, comas, tipos).
La migración real corre automáticamente vía el contenedor `migrate` del
`docker-compose.yml` cuando se despliegue (Task 12).

- [ ] **Step 4: Commit**

```bash
git add backend/migrations/0003_verificacion_email.up.sql backend/migrations/0003_verificacion_email.down.sql
git commit -m "feat(backend): migracion de verificacion de email"
git push origin main
```

---

### Task 3: `domain.Usuario` + repo de usuarios

**Files:**
- Modify: `backend/internal/domain/usuario.go`
- Modify: `backend/internal/repo/usuarios.go`

**Interfaces:**
- Consumes: la columna `usuarios.email_verificado` (Task 2).
- Produces: `domain.Usuario.EmailVerificado bool`; `Usuarios.PorEmail`/`Usuarios.PorID` devuelven ese campo poblado; `Usuarios.Crear` sigue creando con `email_verificado = FALSE` (el `DEFAULT FALSE` de la columna ya lo hace, no hace falta tocar el `INSERT`).

- [ ] **Step 1: Agregar el campo a `backend/internal/domain/usuario.go`**

Reemplazar el struct `Usuario` completo:

```go
type Usuario struct {
	ID              string    `json:"id"`
	Nombre          string    `json:"nombre"`
	Email           string    `json:"email"`
	Rol             Rol       `json:"rol"`
	EmailVerificado bool      `json:"email_verificado"`
	FechaCreacion   time.Time `json:"fecha_creacion"`
}
```

- [ ] **Step 2: Actualizar `PorEmail` y `PorID` en `backend/internal/repo/usuarios.go`**

Reemplazar `PorEmail` completo (líneas 61-75):

```go
// PorEmail retorna el usuario y su hash de contraseña (para login).
func (r *Usuarios) PorEmail(ctx context.Context, email string) (domain.Usuario, string, error) {
	var u domain.Usuario
	var hash, rol string
	const q = `SELECT id::text, nombre, email, rol::text, email_verificado, fecha_creacion, password_hash
	           FROM usuarios WHERE email = $1`
	err := r.pool.QueryRow(ctx, q, email).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.EmailVerificado, &u.FechaCreacion, &hash)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Usuario{}, "", ErrNoEncontrado
	}
	if err != nil {
		return domain.Usuario{}, "", err
	}
	u.Rol = domain.Rol(rol)
	return u, hash, nil
}
```

Reemplazar `PorID` completo (líneas 77-91):

```go
func (r *Usuarios) PorID(ctx context.Context, id string) (domain.Usuario, error) {
	var u domain.Usuario
	var rol string
	const q = `SELECT id::text, nombre, email, rol::text, email_verificado, fecha_creacion
	           FROM usuarios WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.EmailVerificado, &u.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Usuario{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Usuario{}, err
	}
	u.Rol = domain.Rol(rol)
	return u, nil
}
```

Nota: `Crear` (líneas 30-58) NO se toca — el `INSERT INTO usuarios (nombre,
email, password_hash, rol)` sigue igual, y la columna nueva se llena sola
con su `DEFAULT FALSE` (Task 2). El `domain.Usuario{Nombre: nombre, Email:
email, Rol: rol}` que arma `Crear` queda con `EmailVerificado: false` (el
zero-value de `bool`), que es el valor correcto para una cuenta recién
creada.

- [ ] **Step 3: Verificar que compila**

```bash
cd backend && go build ./... && go vet ./...
```
Expected: sin salida.

- [ ] **Step 4: Commit**

```bash
git add backend/internal/domain/usuario.go backend/internal/repo/usuarios.go
git commit -m "feat(backend): agrega email_verificado a Usuario y su repo"
git push origin main
```

---

### Task 4: Paquete `mailer`

**Files:**
- Create: `backend/internal/mailer/mailer.go`
- Test: `backend/internal/mailer/mailer_test.go`
- Modify: `backend/internal/config/config.go`

**Interfaces:**
- Produces:
  - `mailer.Config { Host, Port, Usuario, Password, Remitente, AppBaseURL string }`
  - `mailer.New(cfg mailer.Config) *mailer.Mailer`
  - `(*Mailer) EnviarVerificacion(destinatario, nombre, token string) error`
  - `config.Config` gana los campos `SMTPHost, SMTPPort, SMTPUsuario, SMTPPassword, SMTPRemitente, AppBaseURL string`.

- [ ] **Step 1: Escribir el test de la función pura de construcción del mensaje**

Crear `backend/internal/mailer/mailer_test.go`:

```go
package mailer

import "strings"

import "testing"

func TestConstruirMensaje(t *testing.T) {
	m := New(Config{
		Usuario:   "cuenta@gmail.com",
		Remitente: "Ensayos PAES <cuenta@gmail.com>",
		AppBaseURL: "https://ensayos.example.com",
	})
	asunto, cuerpo := m.construirMensajeVerificacion("Ana", "tok123")

	if !strings.Contains(asunto, "Confirma") {
		t.Fatalf("el asunto debería mencionar la confirmación, obtuve: %q", asunto)
	}
	if !strings.Contains(cuerpo, "https://ensayos.example.com/verificar-email?token=tok123") {
		t.Fatalf("el cuerpo debería incluir el link completo con el token, obtuve: %q", cuerpo)
	}
	if !strings.Contains(cuerpo, "Ana") {
		t.Fatalf("el cuerpo debería saludar por nombre, obtuve: %q", cuerpo)
	}
}
```

- [ ] **Step 2: Correr el test y confirmar que falla**

```bash
cd backend && go test ./internal/mailer/... -run TestConstruirMensaje -v
```
Expected: FAIL — `construirMensajeVerificacion` no existe todavía (ni el paquete).

- [ ] **Step 3: Escribir `backend/internal/mailer/mailer.go`**

```go
// Package mailer envía correos por SMTP (pensado para una cuenta de Gmail
// con contraseña de aplicación). Solo internal/http/auth_handler.go lo usa.
package mailer

import (
	"fmt"
	"net/smtp"
)

type Config struct {
	Host       string
	Port       string
	Usuario    string
	Password   string
	Remitente  string
	AppBaseURL string
}

type Mailer struct {
	cfg Config
}

func New(cfg Config) *Mailer {
	return &Mailer{cfg: cfg}
}

// construirMensajeVerificacion arma el asunto y el cuerpo del correo, sin
// tocar la red — separado de EnviarVerificacion para poder testearlo sin
// credenciales SMTP reales.
func (m *Mailer) construirMensajeVerificacion(nombre, token string) (asunto, cuerpo string) {
	link := fmt.Sprintf("%s/verificar-email?token=%s", m.cfg.AppBaseURL, token)
	asunto = "Confirma tu cuenta - Ensayos PAES"
	cuerpo = fmt.Sprintf(
		"Hola %s,\n\nConfirma tu cuenta haciendo clic en este link:\n%s\n\nEste link expira en 24 horas. Si no creaste esta cuenta, ignora este mensaje.",
		nombre, link,
	)
	return asunto, cuerpo
}

// EnviarVerificacion manda el correo de verificación. Un error acá NO debe
// hacer fallar el registro del usuario que lo llama — solo se loguea.
func (m *Mailer) EnviarVerificacion(destinatario, nombre, token string) error {
	asunto, cuerpo := m.construirMensajeVerificacion(nombre, token)
	mensaje := []byte(fmt.Sprintf("To: %s\r\nSubject: %s\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n%s\r\n", destinatario, asunto, cuerpo))

	auth := smtp.PlainAuth("", m.cfg.Usuario, m.cfg.Password, m.cfg.Host)
	addr := fmt.Sprintf("%s:%s", m.cfg.Host, m.cfg.Port)
	return smtp.SendMail(addr, auth, m.cfg.Remitente, []string{destinatario}, mensaje)
}
```

- [ ] **Step 4: Correr el test y confirmar que pasa**

```bash
cd backend && go test ./internal/mailer/... -v
```
Expected: PASS.

- [ ] **Step 5: Agregar los campos SMTP a `backend/internal/config/config.go`**

Reemplazar el archivo completo:

```go
package config

import (
	"os"
	"strconv"
	"time"
)

type Config struct {
	Port          string
	DatabaseURL   string
	JWTSecret     string
	JWTTTL        time.Duration
	UploadsDir    string
	UploadsURL    string
	AllowedOrigin string
	SMTPHost      string
	SMTPPort      string
	SMTPUsuario   string
	SMTPPassword  string
	SMTPRemitente string
	AppBaseURL    string
}

func Load() Config {
	return Config{
		Port:          getenv("PORT", "8080"),
		DatabaseURL:   getenv("DATABASE_URL", "postgres://localhost:5432/ensayos_paes?sslmode=disable"),
		JWTSecret:     getenv("JWT_SECRET", "cambiar-en-produccion"),
		JWTTTL:        time.Duration(getenvInt("JWT_TTL_HORAS", 24)) * time.Hour,
		UploadsDir:    getenv("UPLOADS_DIR", "./uploads"),
		UploadsURL:    getenv("UPLOADS_URL", "http://localhost:8080/uploads"),
		AllowedOrigin: getenv("CORS_ALLOWED_ORIGIN", "*"),
		SMTPHost:      getenv("SMTP_HOST", "smtp.gmail.com"),
		SMTPPort:      getenv("SMTP_PORT", "587"),
		SMTPUsuario:   getenv("SMTP_USUARIO", ""),
		SMTPPassword:  getenv("SMTP_PASSWORD", ""),
		SMTPRemitente: getenv("SMTP_REMITENTE", "Ensayos PAES <no-responder@ensayospaes.cl>"),
		AppBaseURL:    getenv("APP_BASE_URL", "http://localhost:5173"),
	}
}

func getenv(k, def string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return def
}

func getenvInt(k string, def int) int {
	if v := os.Getenv(k); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return def
}
```

- [ ] **Step 6: Verificar que compila**

```bash
cd backend && go build ./... && go vet ./...
```
Expected: sin salida.

- [ ] **Step 7: Commit**

```bash
git add backend/internal/mailer backend/internal/config/config.go
git commit -m "feat(backend): paquete mailer (SMTP) y config SMTP"
git push origin main
```

---

### Task 5: Repo de tokens de verificación

**Files:**
- Create: `backend/internal/repo/verificaciones.go`

**Interfaces:**
- Consumes: la tabla `verificaciones_email` (Task 2).
- Produces:
  - `repo.ErrTokenInvalido error`
  - `type Verificaciones struct{...}`, `NewVerificaciones(pool *pgxpool.Pool) *Verificaciones`
  - `(*Verificaciones) Crear(ctx context.Context, usuarioID string) (token string, error)`
  - `(*Verificaciones) Consumir(ctx context.Context, token string) (usuarioID string, error)`

- [ ] **Step 1: Escribir `backend/internal/repo/verificaciones.go`**

```go
package repo

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

var ErrTokenInvalido = errors.New("token inválido o expirado")

type Verificaciones struct {
	pool *pgxpool.Pool
}

func NewVerificaciones(pool *pgxpool.Pool) *Verificaciones {
	return &Verificaciones{pool: pool}
}

func generarToken() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil
}

// Crear genera un token nuevo para el usuario, válido 24 horas. Si ya
// existía un token para ese usuario, lo reemplaza (un usuario tiene a lo
// sumo un token activo a la vez).
func (r *Verificaciones) Crear(ctx context.Context, usuarioID string) (string, error) {
	token, err := generarToken()
	if err != nil {
		return "", err
	}
	const q = `INSERT INTO verificaciones_email (token, usuario_id, fecha_expiracion)
	           VALUES ($1, $2, now() + interval '24 hours')
	           ON CONFLICT (usuario_id) DO UPDATE
	           SET token = EXCLUDED.token, fecha_expiracion = EXCLUDED.fecha_expiracion, fecha_creacion = now()`
	if _, err := r.pool.Exec(ctx, q, token, usuarioID); err != nil {
		return "", err
	}
	return token, nil
}

// Consumir valida el token y, si es válido, marca la cuenta como
// verificada y borra el token (de un solo uso). ErrTokenInvalido cubre
// tanto "no existe" como "expiró" — la solución es la misma para el
// usuario: pedir un link nuevo.
func (r *Verificaciones) Consumir(ctx context.Context, token string) (string, error) {
	var usuarioID string
	var expiracion time.Time
	const qBuscar = `SELECT usuario_id::text, fecha_expiracion FROM verificaciones_email WHERE token = $1`
	err := r.pool.QueryRow(ctx, qBuscar, token).Scan(&usuarioID, &expiracion)
	if errors.Is(err, pgx.ErrNoRows) {
		return "", ErrTokenInvalido
	}
	if err != nil {
		return "", err
	}
	if time.Now().After(expiracion) {
		return "", ErrTokenInvalido
	}

	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return "", err
	}
	defer tx.Rollback(ctx)

	if _, err := tx.Exec(ctx, `UPDATE usuarios SET email_verificado = TRUE WHERE id = $1`, usuarioID); err != nil {
		return "", err
	}
	if _, err := tx.Exec(ctx, `DELETE FROM verificaciones_email WHERE token = $1`, token); err != nil {
		return "", err
	}
	if err := tx.Commit(ctx); err != nil {
		return "", err
	}
	return usuarioID, nil
}
```

- [ ] **Step 2: Verificar que compila**

```bash
cd backend && go build ./... && go vet ./...
```
Expected: sin salida.

- [ ] **Step 3: Commit**

```bash
git add backend/internal/repo/verificaciones.go
git commit -m "feat(backend): repo de tokens de verificacion de email"
git push origin main
```

---

### Task 6: Handlers de auth (registro, login, verificar, reenviar) + rutas

**Files:**
- Modify: `backend/internal/http/auth_handler.go`
- Modify: `backend/internal/http/router.go`
- Modify: `backend/cmd/api/main.go`

**Interfaces:**
- Consumes: `mailer.Mailer.EnviarVerificacion` (Task 4); `repo.Verificaciones.Crear`/`.Consumir`, `repo.ErrTokenInvalido` (Task 5); `domain.Usuario.EmailVerificado` (Task 3); `nuevoLimitadorTasa`/`LimitarTasa` (ya existentes en `internal/http/ratelimit.go`).
- Produces: `authHandler` gana los campos `mailer *mailer.Mailer` y `verificaciones *repo.Verificaciones`; endpoints `POST /auth/verificar-email` y `POST /auth/reenviar-verificacion` (públicos, sin auth).

- [ ] **Step 1: Reescribir `backend/internal/http/auth_handler.go`**

Reemplazar el archivo completo:

```go
package httpx

import (
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"strings"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/mailer"
	"github.com/usuario/ensayos-paes/internal/repo"
)

type authHandler struct {
	usuarios       *repo.Usuarios
	jwt            *auth.Manager
	mailer         *mailer.Mailer
	verificaciones *repo.Verificaciones
}

type registroReq struct {
	Nombre         string `json:"nombre"`
	Email          string `json:"email"`
	Password       string `json:"password"`
	Rol            string `json:"rol"`
	AceptaTerminos bool   `json:"acepta_terminos"`
}

type loginReq struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type tokenResp struct {
	Token   string         `json:"token"`
	Usuario domain.Usuario `json:"usuario"`
}

type mensajeResp struct {
	Mensaje string `json:"mensaje"`
}

func (h *authHandler) registrar(w http.ResponseWriter, r *http.Request) {
	var req registroReq
	if !decodificar(w, r, &req) {
		return
	}
	req.Nombre = strings.TrimSpace(req.Nombre)
	req.Email = strings.ToLower(strings.TrimSpace(req.Email))

	if req.Nombre == "" || !strings.Contains(req.Email, "@") || len(req.Password) < 8 {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Datos de registro inválidos")
		return
	}
	if !req.AceptaTerminos {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Debe aceptar los Términos y Condiciones para registrarse")
		return
	}
	rol := domain.Rol(req.Rol)
	if rol != domain.RolEstudiante && rol != domain.RolProfesor {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Rol inválido para registro")
		return
	}

	hash, err := auth.HashPassword(req.Password)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo procesar la contraseña")
		return
	}

	u, err := h.usuarios.Crear(r.Context(), req.Nombre, req.Email, hash, rol, domain.VersionTerminosActual)
	if errors.Is(err, repo.ErrEmailDuplicado) {
		escribirError(w, http.StatusConflict, "EMAIL_DUPLICADO", "El email ya está registrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear el usuario")
		return
	}

	h.enviarCorreoVerificacion(r, u)

	escribirJSON(w, http.StatusCreated, mensajeResp{
		Mensaje: "Te registraste correctamente. Revisá tu correo para verificar tu cuenta antes de iniciar sesión.",
	})
}

// enviarCorreoVerificacion genera el token y envía el correo. Un error acá
// se loguea pero NUNCA se propaga — no debe hacer fallar el registro.
func (h *authHandler) enviarCorreoVerificacion(r *http.Request, u domain.Usuario) {
	token, err := h.verificaciones.Crear(r.Context(), u.ID)
	if err != nil {
		log.Printf("no se pudo generar el token de verificación para %s: %v", u.Email, err)
		return
	}
	if err := h.mailer.EnviarVerificacion(u.Email, u.Nombre, token); err != nil {
		log.Printf("no se pudo enviar el correo de verificación a %s: %v", u.Email, err)
	}
}

func (h *authHandler) login(w http.ResponseWriter, r *http.Request) {
	var req loginReq
	if !decodificar(w, r, &req) {
		return
	}
	req.Email = strings.ToLower(strings.TrimSpace(req.Email))

	u, hash, err := h.usuarios.PorEmail(r.Context(), req.Email)
	if err != nil || !auth.VerifyPassword(hash, req.Password) {
		escribirError(w, http.StatusUnauthorized, "CREDENCIALES", "Email o contraseña incorrectos")
		return
	}
	if !u.EmailVerificado {
		escribirError(w, http.StatusForbidden, "EMAIL_NO_VERIFICADO", "Debes verificar tu email antes de iniciar sesión")
		return
	}
	token, err := h.jwt.Emitir(u.ID, string(u.Rol))
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo emitir el token")
		return
	}
	escribirJSON(w, http.StatusOK, tokenResp{Token: token, Usuario: u})
}

type verificarEmailReq struct {
	Token string `json:"token"`
}

func (h *authHandler) verificarEmail(w http.ResponseWriter, r *http.Request) {
	var req verificarEmailReq
	if !decodificar(w, r, &req) {
		return
	}
	if _, err := h.verificaciones.Consumir(r.Context(), req.Token); err != nil {
		if errors.Is(err, repo.ErrTokenInvalido) {
			escribirError(w, http.StatusUnprocessableEntity, "TOKEN_INVALIDO", "El link de verificación es inválido o expiró")
			return
		}
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar el email")
		return
	}
	escribirJSON(w, http.StatusOK, mensajeResp{Mensaje: "Email verificado correctamente"})
}

type reenviarVerificacionReq struct {
	Email string `json:"email"`
}

// reenviarVerificacion siempre responde 200 con el mismo mensaje genérico,
// exista o no la cuenta, y esté o no ya verificada — no revela el estado
// de una cuenta a quien hace la consulta.
func (h *authHandler) reenviarVerificacion(w http.ResponseWriter, r *http.Request) {
	var req reenviarVerificacionReq
	if !decodificar(w, r, &req) {
		return
	}
	email := strings.ToLower(strings.TrimSpace(req.Email))

	u, _, err := h.usuarios.PorEmail(r.Context(), email)
	if err == nil && !u.EmailVerificado {
		h.enviarCorreoVerificacion(r, u)
	}

	escribirJSON(w, http.StatusOK, mensajeResp{
		Mensaje: "Si el correo está registrado y pendiente de verificar, te enviamos un nuevo link.",
	})
}

// logout: con JWT sin estado, el cliente descarta el token.
func (h *authHandler) logout(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}

func (h *authHandler) me(w http.ResponseWriter, r *http.Request) {
	c, ok := claimsDe(r.Context())
	if !ok {
		escribirError(w, http.StatusUnauthorized, "NO_AUTORIZADO", "No autenticado")
		return
	}
	u, err := h.usuarios.PorID(r.Context(), c.UsuarioID)
	if err != nil {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Usuario no encontrado")
		return
	}
	escribirJSON(w, http.StatusOK, u)
}

func decodificar(w http.ResponseWriter, r *http.Request, v any) bool {
	if err := json.NewDecoder(r.Body).Decode(v); err != nil {
		escribirError(w, http.StatusBadRequest, "JSON", "Cuerpo de solicitud inválido")
		return false
	}
	return true
}
```

- [ ] **Step 2: Actualizar `Deps` y el wiring de rutas en `backend/internal/http/router.go`**

Agregar los campos nuevos a `Deps` (junto a los existentes):

```go
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
```

Agregar el import:

```go
"github.com/usuario/ensayos-paes/internal/mailer"
```

Actualizar la construcción de `authH` (reemplazar la línea
`authH := &authHandler{usuarios: d.Usuarios, jwt: d.JWT}`):

```go
	authH := &authHandler{usuarios: d.Usuarios, jwt: d.JWT, mailer: d.Mailer, verificaciones: d.Verificaciones}
```

Agregar un segundo limitador de tasa (junto a `limitadorLogin`, mismo
patrón — 5 reenvíos por minuto por IP, evita que alguien use el reenvío
para bombardear una casilla de correo):

```go
	limitadorReenvio := nuevoLimitadorTasa(5, time.Minute)
```

Agregar las dos rutas públicas nuevas (junto a `/auth/register` y
`/auth/login`, dentro de `api.Post(...)`/`api.With(...)`, ANTES del
`api.Group(func(priv chi.Router) {...})`):

```go
		api.Post("/auth/register", authH.registrar)
		api.With(LimitarTasa(limitadorLogin)).Post("/auth/login", authH.login)
		api.Post("/auth/verificar-email", authH.verificarEmail)
		api.With(LimitarTasa(limitadorReenvio)).Post("/auth/reenviar-verificacion", authH.reenviarVerificacion)
```

(Reemplaza únicamente esas dos líneas existentes por este bloque de 4
líneas — no toca nada del `api.Group(func(priv chi.Router) {...})` que
viene después.)

- [ ] **Step 3: Wiring en `backend/cmd/api/main.go`**

Reemplazar el archivo completo:

```go
package main

import (
	"context"
	"log"
	"net/http"

	"github.com/usuario/ensayos-paes/internal/auth"
	"github.com/usuario/ensayos-paes/internal/config"
	"github.com/usuario/ensayos-paes/internal/db"
	httpx "github.com/usuario/ensayos-paes/internal/http"
	"github.com/usuario/ensayos-paes/internal/mailer"
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
	if cfg.SMTPUsuario == "" || cfg.SMTPPassword == "" {
		log.Println("ADVERTENCIA: SMTP_USUARIO/SMTP_PASSWORD no configurados. El envío de correos de verificación fallará (se registrará en el log, no bloquea el registro).")
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

	correo := mailer.New(mailer.Config{
		Host:       cfg.SMTPHost,
		Port:       cfg.SMTPPort,
		Usuario:    cfg.SMTPUsuario,
		Password:   cfg.SMTPPassword,
		Remitente:  cfg.SMTPRemitente,
		AppBaseURL: cfg.AppBaseURL,
	})

	deps := httpx.Deps{
		Usuarios:       repo.NewUsuarios(pool),
		Examenes:       repo.NewExamenes(pool),
		Items:          repo.NewItems(pool),
		Clave:          repo.NewClave(pool),
		Ensayos:        repo.NewEnsayos(pool),
		Grupos:         repo.NewGrupos(pool),
		Verificaciones: repo.NewVerificaciones(pool),
		Imagenes:       imagenes,
		Mailer:         correo,
		UploadsDir:     cfg.UploadsDir,
		JWT:            auth.NewManager(cfg.JWTSecret, cfg.JWTTTL),
		AllowedOrigin:  cfg.AllowedOrigin,
	}
	handler := httpx.New(deps)

	log.Printf("API escuchando en :%s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, handler); err != nil {
		log.Fatal(err)
	}
}
```

- [ ] **Step 4: Verificar que compila**

```bash
cd backend && go build ./... && go vet ./...
```
Expected: sin salida.

- [ ] **Step 5: Commit**

```bash
git add backend/internal/http/auth_handler.go backend/internal/http/router.go backend/cmd/api/main.go
git commit -m "feat(backend): registro sin auto-login, verificar y reenviar email"
git push origin main
```

---

### Task 7: Endpoint admin-only de verificación manual

**Files:**
- Modify: `backend/internal/repo/usuarios.go`
- Modify: `backend/internal/http/auth_handler.go`
- Modify: `backend/internal/http/router.go`

**Interfaces:**
- Consumes: `repo.ErrNoEncontrado` (ya existente).
- Produces: `(*Usuarios) MarcarVerificado(ctx context.Context, id string) (domain.Usuario, error)`; handler `(*authHandler) verificarEmailAdmin(w, r)`; ruta `POST /admin/usuarios/{usuarioId}/verificar-email` (rol admin).

- [ ] **Step 1: Agregar `MarcarVerificado` a `backend/internal/repo/usuarios.go`**

Agregar al final del archivo:

```go
// MarcarVerificado marca la cuenta como verificada sin pasar por el
// correo — uso operativo (QA/soporte), no expuesto en ninguna pantalla.
func (r *Usuarios) MarcarVerificado(ctx context.Context, id string) (domain.Usuario, error) {
	const q = `UPDATE usuarios SET email_verificado = TRUE WHERE id = $1
	           RETURNING id::text, nombre, email, rol::text, email_verificado, fecha_creacion`
	var u domain.Usuario
	var rol string
	err := r.pool.QueryRow(ctx, q, id).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.EmailVerificado, &u.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Usuario{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Usuario{}, err
	}
	u.Rol = domain.Rol(rol)
	return u, nil
}
```

- [ ] **Step 2: Agregar el handler en `backend/internal/http/auth_handler.go`**

Agregar al final del archivo (después de `decodificar`, o donde termine el
archivo tras la Task 6):

```go
func (h *authHandler) verificarEmailAdmin(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "usuarioId")
	u, err := h.usuarios.MarcarVerificado(r.Context(), id)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Usuario no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo verificar la cuenta")
		return
	}
	escribirJSON(w, http.StatusOK, u)
}
```

Agregar el import `"github.com/go-chi/chi/v5"` al bloque de imports del
archivo (ya se usa `chi.URLParam` en otros handlers del proyecto, ej.
`grupo_handler.go`).

- [ ] **Step 3: Agregar la ruta en `backend/internal/http/router.go`**

Dentro del grupo admin (`priv.Group(func(admin chi.Router) {...})`),
agregar junto a `admin.Post("/imagenes", bancoH.subirImagen)`:

```go
		admin.Post("/imagenes", bancoH.subirImagen)
		admin.Post("/usuarios/{usuarioId}/verificar-email", authH.verificarEmailAdmin)
```

- [ ] **Step 4: Verificar que compila**

```bash
cd backend && go build ./... && go vet ./...
```
Expected: sin salida.

- [ ] **Step 5: Commit**

```bash
git add backend/internal/repo/usuarios.go backend/internal/http/auth_handler.go backend/internal/http/router.go
git commit -m "feat(backend): endpoint admin-only para verificar email manualmente"
git push origin main
```

---

### Task 8: Cliente API (`api.js`)

**Files:**
- Modify: `frontend/src/api.js`

**Interfaces:**
- Produces:
  - `api.registrar(body)` → sigue siendo `POST /api/v1/auth/register`, pero ahora la respuesta es `{ mensaje: string }` (ya no `{ token, usuario }`) — el método en sí NO cambia de firma, solo cambia lo que la Promise resuelve (documentarlo es responsabilidad de quien consuma el método, Tasks 9-10).
  - `api.verificarEmail(token)` → `POST /api/v1/auth/verificar-email` → `Promise<{mensaje}>`
  - `api.reenviarVerificacion(email)` → `POST /api/v1/auth/reenviar-verificacion` → `Promise<{mensaje}>`

- [ ] **Step 1: Agregar los 2 métodos nuevos al objeto `api` en `frontend/src/api.js`**

Agregar junto a `registrar`/`iniciarSesion` (no se toca `registrar` en sí —
su firma HTTP no cambia, solo cambia lo que el backend devuelve):

```js
  verificarEmail: (token) => pedir('/api/v1/auth/verificar-email', { metodo: 'POST', body: { token } }),
  reenviarVerificacion: (email) => pedir('/api/v1/auth/reenviar-verificacion', { metodo: 'POST', body: { email } }),
```

- [ ] **Step 2: Verificar con un script de Node (fetch mockeado)**

```bash
cd frontend && node -e '
import("vite").then(async ({ createServer }) => {
  const server = await createServer({ configFile: "vite.config.js", root: "." })
  try {
    const llamadas = []
    globalThis.fetch = async (url, opciones) => {
      llamadas.push({ url, opciones })
      return { status: 200, ok: true, json: async () => ({ mensaje: "ok" }) }
    }
    const { api } = await server.ssrLoadModule("/src/api.js")

    await api.verificarEmail("tok123")
    let l = llamadas.at(-1)
    console.log("verificarEmail POST /auth/verificar-email:", l.opciones.method === "POST" && l.url.endsWith("/api/v1/auth/verificar-email"))
    console.log("verificarEmail body { token }:", l.opciones.body === JSON.stringify({ token: "tok123" }))

    await api.reenviarVerificacion("a@b.cl")
    l = llamadas.at(-1)
    console.log("reenviarVerificacion POST /auth/reenviar-verificacion:", l.opciones.method === "POST" && l.url.endsWith("/api/v1/auth/reenviar-verificacion"))
    console.log("reenviarVerificacion body { email }:", l.opciones.body === JSON.stringify({ email: "a@b.cl" }))
  } finally {
    await server.close()
  }
})
'
```
Expected: `true` cuatro veces.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/api.js
git commit -m "feat(frontend): cliente API de verificacion de email"
git push origin main
```

---

### Task 9: `Registro.jsx` — sin auto-login

**Files:**
- Modify: `frontend/src/pages/Registro.jsx`

**Interfaces:**
- Consumes: `api.registrar` (respuesta ahora `{mensaje}`, Task 8).
- Produces: `<Registro />` ya no llama `guardarSesion` ni navega tras un registro exitoso.

- [ ] **Step 1: Reescribir `frontend/src/pages/Registro.jsx`**

Reemplazar el archivo completo:

```jsx
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'

export default function Registro() {
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rol, setRol] = useState('estudiante')
  const [aceptaTerminos, setAceptaTerminos] = useState(false)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [registrado, setRegistrado] = useState(false)

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      await api.registrar({
        nombre,
        email,
        password,
        rol,
        acepta_terminos: aceptaTerminos,
      })
      setRegistrado(true)
    } catch (e) {
      setError(e instanceof ApiError ? e.mensaje || 'No se pudo registrar' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  if (registrado) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>Revisá tu correo</h1>
          <p>
            Te registraste correctamente. Te enviamos un correo a <strong>{email}</strong> para
            confirmar tu cuenta — hacé clic en el link antes de iniciar sesión.
          </p>
          <p>
            <Link to="/login">Ir a iniciar sesión</Link>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Crear cuenta</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="nombre">Nombre</label>
            <input id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="password">Contraseña (mínimo 8 caracteres)</label>
            <input
              id="password"
              type="password"
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="rol">Soy</label>
            <select id="rol" value={rol} onChange={(e) => setRol(e.target.value)}>
              <option value="estudiante">Estudiante</option>
              <option value="profesor">Profesor</option>
            </select>
          </div>
          <div className="campo">
            <label>
              <input
                type="checkbox"
                checked={aceptaTerminos}
                onChange={(e) => setAceptaTerminos(e.target.checked)}
              />{' '}
              Acepto los Términos y Condiciones
            </label>
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Creando cuenta…' : 'Crear cuenta'}
          </button>
        </form>
        <p>
          ¿Ya tenés cuenta? <Link to="/login">Iniciar sesión</Link>
        </p>
      </div>
    </div>
  )
}
```

(Cambios respecto al archivo original: se elimina el import de `useAuth`
y `useNavigate` — ya no se usan; se agrega el estado `registrado` y el
bloque de confirmación; `alEnviar` ya no llama `guardarSesion`/`navigate`.)

- [ ] **Step 2: Verificar con build**

```bash
cd frontend && npm run build
```
Expected: build limpio.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/Registro.jsx
git commit -m "feat(frontend): registro ya no loguea automatico, muestra confirmacion"
git push origin main
```

---

### Task 10: `Login.jsx` — manejo de `EMAIL_NO_VERIFICADO`

**Files:**
- Modify: `frontend/src/pages/Login.jsx`

**Interfaces:**
- Consumes: `api.reenviarVerificacion` (Task 8).
- Produces: `<Login />` muestra un mensaje y botón de reenvío cuando `ApiError.codigo === 'EMAIL_NO_VERIFICADO'`.

- [ ] **Step 1: Reescribir `frontend/src/pages/Login.jsx`**

Reemplazar el archivo completo:

```jsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useAuth } from '../AuthContext.jsx'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [emailNoVerificado, setEmailNoVerificado] = useState(false)
  const [enviando, setEnviando] = useState(false)
  const [reenviando, setReenviando] = useState(false)
  const [mensajeReenvio, setMensajeReenvio] = useState(null)
  const { guardarSesion } = useAuth()
  const navigate = useNavigate()

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    setEmailNoVerificado(false)
    setMensajeReenvio(null)
    setEnviando(true)
    try {
      const respuesta = await api.iniciarSesion({ email, password })
      guardarSesion(respuesta.token, respuesta.usuario)
      navigate('/')
    } catch (e) {
      if (e instanceof ApiError && e.codigo === 'EMAIL_NO_VERIFICADO') {
        setEmailNoVerificado(true)
      } else if (e instanceof ApiError && e.status === 401) {
        setError('Email o contraseña incorrectos')
      } else {
        setError('No se pudo conectar con el servidor')
      }
    } finally {
      setEnviando(false)
    }
  }

  async function alReenviar() {
    setReenviando(true)
    setMensajeReenvio(null)
    try {
      const respuesta = await api.reenviarVerificacion(email)
      setMensajeReenvio(respuesta.mensaje)
    } catch {
      setMensajeReenvio('No se pudo reenviar el correo, intentá de nuevo más tarde.')
    } finally {
      setReenviando(false)
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Iniciar sesión</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          {emailNoVerificado && (
            <div className="campo">
              <p className="error">Todavía no verificaste tu email.</p>
              <button
                type="button"
                className="boton-secundario"
                disabled={reenviando}
                onClick={alReenviar}
              >
                {reenviando ? 'Reenviando…' : 'Reenviar verificación'}
              </button>
              {mensajeReenvio && <p>{mensajeReenvio}</p>}
            </div>
          )}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Ingresando…' : 'Ingresar'}
          </button>
        </form>
        <p>
          ¿No tenés cuenta? <Link to="/registro">Crear cuenta</Link>
        </p>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Verificar con build**

```bash
cd frontend && npm run build
```
Expected: build limpio.

Releé el diff propio: ¿`emailNoVerificado` y `error` son estados
separados (no se pisan entre sí)? ¿`alReenviar` reusa el `email` ya
tipeado en el formulario, sin pedirlo de nuevo?

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/Login.jsx
git commit -m "feat(frontend): login maneja email no verificado con reenvio"
git push origin main
```

---

### Task 11: `VerificarEmail.jsx` (nueva página pública) + ruta

**Files:**
- Create: `frontend/src/pages/VerificarEmail.jsx`
- Modify: `frontend/src/App.jsx`

**Interfaces:**
- Consumes: `api.verificarEmail`, `api.reenviarVerificacion` (Task 8).
- Produces: `<VerificarEmail />` (componente de página, default export), montado en la ruta pública `/verificar-email` (fuera de `RutaPrivada` — no hay sesión en este punto).

- [ ] **Step 1: Escribir `frontend/src/pages/VerificarEmail.jsx`**

```jsx
import { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'

export default function VerificarEmail() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [estado, setEstado] = useState('cargando')
  const [mensaje, setMensaje] = useState(null)
  const [email, setEmail] = useState('')
  const [reenviando, setReenviando] = useState(false)
  const [mensajeReenvio, setMensajeReenvio] = useState(null)

  useEffect(() => {
    if (!token) {
      setEstado('error')
      setMensaje('Este link no incluye un token de verificación.')
      return
    }
    let cancelado = false
    api
      .verificarEmail(token)
      .then((respuesta) => {
        if (cancelado) return
        setEstado('exito')
        setMensaje(respuesta.mensaje)
      })
      .catch((e) => {
        if (cancelado) return
        setEstado('error')
        setMensaje(e instanceof ApiError ? e.mensaje || 'Este link ya no es válido' : 'Este link ya no es válido')
      })
    return () => {
      cancelado = true
    }
  }, [token])

  async function alReenviar(evento) {
    evento.preventDefault()
    setReenviando(true)
    setMensajeReenvio(null)
    try {
      const respuesta = await api.reenviarVerificacion(email)
      setMensajeReenvio(respuesta.mensaje)
    } catch {
      setMensajeReenvio('No se pudo reenviar el correo, intentá de nuevo más tarde.')
    } finally {
      setReenviando(false)
    }
  }

  if (estado === 'cargando') {
    return (
      <div className="pantalla">
        <div className="tarjeta">Verificando tu cuenta…</div>
      </div>
    )
  }

  if (estado === 'exito') {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>¡Listo!</h1>
          <p>{mensaje}</p>
          <p>
            <Link to="/login">Ir a iniciar sesión</Link>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Este link ya no es válido</h1>
        <p className="error">{mensaje}</p>
        <form onSubmit={alReenviar}>
          <div className="campo">
            <label htmlFor="email">Reenviar verificación a</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <button className="boton" type="submit" disabled={reenviando}>
            {reenviando ? 'Reenviando…' : 'Reenviar'}
          </button>
        </form>
        {mensajeReenvio && <p>{mensajeReenvio}</p>}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Agregar la ruta pública en `frontend/src/App.jsx`**

Agregar el import:

```jsx
import VerificarEmail from './pages/VerificarEmail.jsx'
```

Agregar la ruta pública (junto a `/login` y `/registro`, SIN
`RutaPrivada`/`LayoutAutenticado`):

```jsx
      <Route path="/login" element={<Login />} />
      <Route path="/registro" element={<Registro />} />
      <Route path="/verificar-email" element={<VerificarEmail />} />
```

(Reemplaza esas 2 líneas existentes por las 3 de arriba — no toca ninguna
otra ruta del archivo.)

- [ ] **Step 3: Verificar con build**

```bash
cd frontend && npm run build
```
Expected: build limpio.

Releé el diff propio: ¿la ruta `/verificar-email` NO está envuelta en
`RutaPrivada`/`LayoutAutenticado` (a diferencia de todas las demás rutas
del archivo)? Un usuario que hace clic en el link del correo no tiene
sesión iniciada todavía.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/VerificarEmail.jsx frontend/src/App.jsx
git commit -m "feat(frontend): pagina de verificacion de email"
git push origin main
```

---

### Task 12: Desplegar en Proxmox

**Files:** ninguno (solo comandos de despliegue).

**Interfaces:** Consumes: todo lo anterior (migración + backend + frontend).

- [ ] **Step 1: Redesplegar backend y frontend en el CT 118 de Proxmox**

```bash
# vía SSH al host 192.168.0.155 -> pct exec 118:
cd /opt/app && git pull && docker compose up -d --build api web
```

El contenedor `migrate` corre automáticamente antes de `api` y aplicará
`0003_verificacion_email.up.sql`.

- [ ] **Step 2: Verificar en vivo**

Abrir `http://192.168.0.190/` (y `http://100.93.161.84/` vía Tailscale).
Registrar un estudiante nuevo con un email real al que tengas acceso (o
usar la cuenta admin ya existente para llamar a `POST
/admin/usuarios/{id}/verificar-email` vía curl si preferís no depender del
correo real, dado que las credenciales SMTP todavía no están configuradas
en este punto — ver Global Constraints):

1. Confirmar que el registro ya NO loguea automático — muestra el mensaje
   "revisá tu correo".
2. Intentar loguear con esa cuenta antes de verificar — confirmar el
   mensaje "Todavía no verificaste tu email" y el botón de reenvío.
3. Si tenés acceso al correo real: hacer clic en el link recibido,
   confirmar que `/verificar-email` marca la cuenta y after eso el login
   funciona. Si las credenciales SMTP todavía no están configuradas (paso
   pendiente del usuario, fuera de esta tanda), usar el endpoint
   admin-only para verificar la cuenta de prueba manualmente y confirmar
   que el login funciona después.
4. Confirmar que las cuentas ya existentes (ej. el admin) siguen
   logueando sin problemas (la migración las marcó verificadas).

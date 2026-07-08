# Verificación de email en el registro

Fecha: 2026-07-08

## Contexto

Hoy `POST /auth/register` crea la cuenta y devuelve un token de sesión al
toque (login automático), sin ninguna confirmación de que el email
ingresado sea real o pertenezca a quien se registra. Esta tanda agrega
verificación por correo: el usuario debe confirmar un link antes de poder
iniciar sesión.

El envío se hace por SMTP desde una cuenta de Gmail (contraseña de
aplicación, no la contraseña real de la cuenta). Las credenciales SMTP se
configuran después, vía variables de entorno — no son necesarias para
desarrollar o revisar este código, y su ausencia no debe romper el registro
(ver Comportamiento).

**Consecuencia operativa para el desarrollo asistido:** hasta ahora,
verificar en vivo funcionalidades de estudiante era posible registrando una
cuenta descartable vía `/registro` (que quedaba logueada al toque). Después
de esta tanda eso deja de ser posible sin acceso real al correo. El usuario
decidió explícitamente aceptar esta limitación y agregar un endpoint
admin-only para verificar cuentas manualmente (uso de QA/soporte, sin
pantalla de frontend), no un bypass automático para agentes.

## Alcance

- Registro deja de loguear automáticamente: crea la cuenta sin verificar,
  envía el correo, responde con un mensaje.
- Login rechaza cuentas sin verificar con un error específico.
- Endpoint para verificar el email vía el token del link.
- Endpoint para reenviar la verificación (token nuevo invalida el
  anterior), con expiración de 24 horas.
- Endpoint admin-only para marcar una cuenta como verificada sin correo
  (QA/soporte, sin UI).
- Cuentas ya existentes (creadas antes de esta migración) quedan
  verificadas automáticamente — no se bloquea a nadie que ya tenía cuenta.

Fuera de alcance: recuperación de contraseña, verificación de teléfono,
reverificación al cambiar el email después del registro.

## Arquitectura

### Backend

**Migración `backend/migrations/0003_verificacion_email.up.sql`:**
```sql
ALTER TABLE usuarios ADD COLUMN email_verificado BOOLEAN NOT NULL DEFAULT FALSE;
UPDATE usuarios SET email_verificado = TRUE;

CREATE TABLE verificaciones_email (
    token             TEXT PRIMARY KEY,
    usuario_id        UUID NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_expiracion  TIMESTAMPTZ NOT NULL,
    fecha_creacion    TIMESTAMPTZ NOT NULL DEFAULT now()
);
```
`UNIQUE(usuario_id)`: un usuario tiene a lo sumo un token activo a la vez;
reenviar reemplaza (no acumula) el token anterior. El `UPDATE` posterior al
`ALTER TABLE` es crítico: sin él, todas las cuentas existentes (incluido el
admin) quedarían con `email_verificado = FALSE` y no podrían loguear más.

**`backend/internal/mailer/mailer.go`** (paquete nuevo): envío por SMTP
usando `net/smtp` (librería estándar de Go, sin dependencias nuevas).
`EnviarVerificacion(destinatario, nombre, token string) error` arma el
link `{APP_BASE_URL}/verificar-email?token=...` (apunta al frontend, no al
backend) y lo envía. Si el envío falla (SMTP no configurado, credenciales
inválidas, etc.), el error se loguea server-side pero **no** hace fallar el
registro — la cuenta queda creada igual, siguiendo el mismo criterio ya
usado en el proyecto para configuración opcional en desarrollo ("avisos de
arranque, no fallos duros", ver `LEARNINGS.md` Fase 7).

**`backend/internal/config/config.go`** (modificado): nuevos campos
`SMTPHost` (default `smtp.gmail.com`), `SMTPPort` (default `587`),
`SMTPUsuario`, `SMTPPassword`, `SMTPRemitente`, `AppBaseURL` (default
`http://localhost:5173`).

**`backend/internal/repo/verificaciones.go`** (nuevo):
- `Crear(ctx, usuarioID string) (token string, error)`: genera 32 bytes con
  `crypto/rand` (codificados en hex, no el alfabeto pronunciable de 32
  símbolos que usa `codigo_invitacion` de grupos — este token no se dicta
  por teléfono, necesita más entropía), guarda con expiración a `now() +
  24h`. Si ya existe un token para ese usuario, lo reemplaza
  (`ON CONFLICT (usuario_id) DO UPDATE`).
- `Consumir(ctx, token string) (usuarioID string, error)`: busca el token;
  si no existe o `fecha_expiracion < now()`, devuelve `ErrTokenInvalido`
  (un solo error cubre ambos casos — la solución para el usuario es la
  misma: pedir un link nuevo). Si es válido, en una transacción marca
  `usuarios.email_verificado = true` y borra la fila del token.

**`backend/internal/http/auth_handler.go`** (modificado):
- `registrar`: ya no emite JWT. Genera el token de verificación, intenta
  enviar el correo (sin fallar si el envío falla), responde `201` con
  `{mensaje: "..."}`.
- `login`: si `usuario.EmailVerificado == false`, responde `403` con
  `{codigo: "EMAIL_NO_VERIFICADO", mensaje: "..."}` — este chequeo ocurre
  **después** de verificar la contraseña (para no revelar si una cuenta
  existe a alguien que no conoce la contraseña).
- `verificarEmail` (nuevo): `POST /auth/verificar-email {token}` → `200
  {mensaje}` en éxito, `422 {codigo: "TOKEN_INVALIDO", mensaje}` si el
  token no existe o expiró.
- `reenviarVerificacion` (nuevo): `POST /auth/reenviar-verificacion
  {email}` → siempre `200` con un mensaje genérico, sin revelar si el
  email existe o ya está verificado. Solo genera y envía un token nuevo
  en el caso real (email existe y no está verificado); en cualquier otro
  caso, no hace nada pero responde igual.
- `verificarEmailAdmin` (nuevo, admin-only): `POST
  /admin/usuarios/{usuarioId}/verificar-email` → marca
  `email_verificado = true` directamente, sin correo. Sin pantalla de
  frontend — uso vía `curl`/Postman para QA o soporte, mismo criterio que
  `cmd/seed-admin` (herramienta operativa, no producto).

**`backend/internal/domain/usuario.go`** (modificado): `Usuario` gana
`EmailVerificado bool `json:"email_verificado"``. `Usuarios.Crear`,
`PorEmail` y `PorID` (en `internal/repo/usuarios.go`) actualizan su
`SELECT`/`RETURNING` para incluir la columna nueva.

**`docs/openapi.yaml`** (modificado):
- `Usuario` gana `email_verificado: boolean`.
- `POST /auth/register` cambia su respuesta `201` de `TokenResponse` a un
  schema nuevo `RegistroResponse { mensaje: string }`.
- `POST /auth/login` documenta el nuevo `403` (schema `Error` ya
  existente, `codigo: EMAIL_NO_VERIFICADO`).
- Paths nuevos: `POST /auth/verificar-email`, `POST
  /auth/reenviar-verificacion`, `POST
  /admin/usuarios/{usuarioId}/verificar-email`.

### Frontend

- **`frontend/src/pages/Registro.jsx`** (modificado): tras un registro
  exitoso, ya no llama `guardarSesion` ni navega — muestra un mensaje de
  confirmación ("revisá tu correo") en la misma pantalla, reemplazando el
  formulario.
- **`frontend/src/pages/Login.jsx`** (modificado): si el error es
  `ApiError` con `codigo === 'EMAIL_NO_VERIFICADO'`, muestra un mensaje
  distinto con un botón "Reenviar verificación" (reusa el email ya
  tipeado en el formulario, llama a `api.reenviarVerificacion`).
- **`frontend/src/pages/VerificarEmail.jsx`** (nueva, ruta pública
  `/verificar-email`, **sin** `RutaPrivada` — no hay sesión en este
  punto): lee `token` de la query string (`useSearchParams`), lo verifica
  automáticamente al montar, muestra cargando → éxito (link a `/login`) →
  o error (token inválido/expirado, con un mini-formulario de reenvío que
  pide el email de nuevo).
- **`frontend/src/api.js`** (modificado): `registrar` ajusta su tipo de
  retorno esperado (ya no trae `token`/`usuario`, solo `mensaje`); se
  agregan `verificarEmail(token)` → `POST /auth/verificar-email` y
  `reenviarVerificacion(email)` → `POST /auth/reenviar-verificacion`.
- **`frontend/src/App.jsx`** (modificado): nueva ruta pública
  `/verificar-email`, junto a `/login` y `/registro`.

## Comportamiento

- **Registro**: valida igual que hoy (nombre, email, password ≥8, T&C). Si
  todo ok, crea la cuenta, genera el token, intenta enviar el correo (sin
  bloquear si falla) y responde 201. La pantalla muestra "Te registraste
  correctamente. Revisá tu correo (`{email}`) para confirmar tu cuenta
  antes de iniciar sesión."
- **Login con cuenta sin verificar**: mensaje "Todavía no verificaste tu
  email." + botón "Reenviar verificación".
- **Verificar email**: al entrar a `/verificar-email?token=...`, la
  verificación es automática (sin que el usuario tenga que hacer nada).
  Éxito: "¡Cuenta verificada! Ya podés iniciar sesión" + link a `/login`.
  Error: "Este link ya no es válido" + mini-formulario de reenvío.
- **Reenviar verificación**: siempre responde con el mismo mensaje neutro
  ("si el correo está registrado y pendiente de verificar, te enviamos un
  nuevo link"), sin revelar si la cuenta existe o ya está verificada.
- **Cuentas existentes**: quedan verificadas automáticamente por el
  `UPDATE` de la migración — ningún login existente se rompe.

## Testing

Backend: sin test unitario para `internal/repo/verificaciones.go` (mismo
criterio que el resto de `internal/repo` — no hay tests de métodos que
tocan la DB en este proyecto). Sin test para el envío SMTP real (no hay
forma de probarlo sin credenciales reales configuradas). Frontend: sin
framework automatizado; verificación manual con `npm run dev`.

**Importante:** después de esta tanda, ya no va a ser posible verificar en
vivo flujos de estudiante con una cuenta descartable auto-registrada (el
registro deja de loguear automático). La verificación de las tareas de
esta tanda se apoya en build limpio + auto-revisión de código línea por
línea contra este spec y `docs/openapi.yaml`, igual que ya se hizo para
Banco de preguntas y partes de Grupos.

## Despliegue

Mismo mecanismo que las tandas anteriores: rebuild de `api` (backend) y
`web` (frontend) en el CT 118 de Proxmox tras el merge. La migración nueva
corre automáticamente vía el contenedor `migrate` al levantar el stack. Las
variables de entorno SMTP (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USUARIO`,
`SMTP_PASSWORD`, `SMTP_REMITENTE`, `APP_BASE_URL`) se configuran después,
fuera de esta tanda — hasta entonces, el envío de correos fallará
silenciosamente (logueado, no bloqueante) y el endpoint admin-only sirve
para destrabar cuentas de prueba mientras tanto.

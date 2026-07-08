# Grupos (profesor + estudiante)

Fecha: 2026-07-07

## Contexto

El backend de Grupos está casi completo desde la Fase 5 del plan original:
crear/listar grupos (profesor), unirse por código (estudiante), detalle de
grupo con progreso agregado, listado de miembros, y progreso individual de
un estudiante dentro del grupo. Ninguna pantalla de frontend lo consume
todavía. El link "Mis grupos" del profesor existe en `MENU_POR_ROL` pero
está `disponible: false, ruta: null`; el estudiante no tiene ninguna entrada
de menú para grupos.

Al brainstormear esta tanda se detectó un hueco real en el contrato: el
estudiante puede unirse a un grupo por código, pero no hay forma de que
después vea a qué grupos pertenece (no existe ningún endpoint `GET` para
eso desde el lado estudiante). Se decidió ampliar el contrato en esta misma
tanda en vez de dejarlo para después.

## Alcance

**Backend (extensión mínima):**
- Nuevo endpoint `GET /grupos/mis-grupos` (rol estudiante): devuelve los
  grupos a los que pertenece el estudiante autenticado, cada uno con
  nombre del grupo, nombre del profesor dueño, y fecha de unión.
- Sin migración nueva: reutiliza `grupo_miembros` (ya tiene `grupo_id`,
  `estudiante_id`, `fecha_union`) y un join a `grupos`/`usuarios`.

**Frontend (el grueso de esta tanda):**
- Profesor: lista de sus grupos (con creación inline, un solo campo:
  nombre), detalle de un grupo (progreso agregado + tabla de miembros), y
  progreso individual de un estudiante dentro del grupo.
- Estudiante: pantalla "Mis grupos" — listado de grupos a los que
  pertenece + formulario para unirse por código.
- Se extiende `InicioPorRol` (ya existente desde la tanda de Banco de
  preguntas) para que un profesor logueado caiga en `/grupos` en vez de
  "Configurar ensayo", mismo criterio que ya se aplicó para admin.

**Fuera de alcance:**
- Que el estudiante pueda salir de un grupo.
- Editar o eliminar un grupo (el contrato actual no lo expone; solo
  crear/listar/detalle/unirse/miembros/progreso).
- Cualquier vínculo entre "ensayo" y "grupo" — los ensayos siguen siendo
  del estudiante, no del grupo; las estadísticas por grupo se calculan
  agregando sobre los ensayos de sus miembros, no sobre una relación
  ensayo↔grupo.
- Verificación de email / aprobación de registro (subsistema aparte,
  decidido explícitamente en la conversación previa a este spec).

## Arquitectura

### Backend

- **`backend/internal/repo/grupos.go`** (modificado): nuevo método
  `ListarPorEstudiante(ctx, estudianteID) ([]GrupoConProfesor, error)`.
  Query: `SELECT g.id, g.nombre, u.nombre AS profesor_nombre, gm.fecha_union
  FROM grupo_miembros gm JOIN grupos g ON g.id = gm.grupo_id JOIN usuarios u
  ON u.id = g.profesor_id WHERE gm.estudiante_id = $1 ORDER BY
  gm.fecha_union DESC`. Mismo estilo que los métodos ya existentes en ese
  archivo (`ListarPorProfesor`, `Miembros`).
- **`backend/internal/http/grupo_handler.go`** (modificado): nuevo handler
  `misGrupos(w, r)` que toma `claims.UsuarioID` del contexto (mismo patrón
  que `listar`/`unirse`) y llama a `ListarPorEstudiante`.
- **`backend/internal/http/router.go`** (modificado): nueva ruta
  `GET /grupos/mis-grupos` dentro del sub-grupo `RequerirRol(RolEstudiante)`
  ya existente (junto a `POST /grupos/unirse`, línea ~122). Chi resuelve
  segmentos estáticos (`mis-grupos`) antes que parámetros (`{grupoId}`),
  así que no hay conflicto con `GET /grupos/{grupoId}` aunque ambas
  cuelguen del mismo prefijo `/grupos`.
- **`docs/openapi.yaml`** (modificado): nuevo path `/grupos/mis-grupos` y
  schema `GrupoEstudiante { id, nombre, profesor_nombre, fecha_union }`.
- Sin tests unitarios nuevos para el repo: ningún método existente de
  `internal/repo/grupos.go` tiene test unitario (los tests del proyecto se
  concentran en `internal/domain` y `internal/pdfimport`, funciones puras
  sin DB) — se mantiene ese mismo criterio para `ListarPorEstudiante`.

### Frontend

Rutas nuevas (todas dentro de `<RutaPrivada><LayoutAutenticado>...`, el
guard de rol vive en el backend):

```
/grupos                               → MisGruposProfesor.jsx  (lista + crear inline)
/grupos/:id                           → GrupoDetalle.jsx       (progreso agregado + miembros)
/grupos/:id/estudiantes/:estudianteId → ProgresoEstudianteGrupo.jsx (evolución individual)
/mis-grupos                           → MisGruposEstudiante.jsx (lista + unirse por código)
```

Archivos nuevos:
- **`frontend/src/pages/MisGruposProfesor.jsx`**: carga `api.listarGrupos`;
  tabla con nombre/código de invitación/fecha, cada fila enlaza a
  `/grupos/:id`. Formulario de una sola línea (input nombre + botón "Crear
  grupo") arriba de la tabla, llama `api.crearGrupo` y agrega el grupo
  nuevo a la lista local sin recargar toda la pantalla.
- **`frontend/src/pages/GrupoDetalle.jsx`**: carga `api.obtenerGrupo`
  (`cantidad_miembros`, `promedio_grupo`, `desempeno_por_eje`) y
  `api.listarMiembros` (tabla con nombre/fecha_union/total_ensayos/
  ultimo_puntaje), cada fila enlaza a `/grupos/:id/estudiantes/:estudianteId`.
- **`frontend/src/pages/ProgresoEstudianteGrupo.jsx`**: carga
  `api.progresoEstudiante`; muestra nombre del estudiante, desglose por
  eje, y gráfico de evolución (`recharts` `LineChart`, mismo bloque que
  `Dashboard.jsx`, duplicado — no extraído a componente compartido, mismo
  criterio ya documentado en `LEARNINGS.md` para duplicación aceptable a
  esta escala).
- **`frontend/src/pages/MisGruposEstudiante.jsx`**: carga `api.misGrupos`;
  lista simple (nombre de grupo + profesor + fecha de unión) y formulario
  de una línea (input código + botón "Unirme") que llama
  `api.unirseGrupo` y refresca la lista.

Archivos modificados:
- **`frontend/src/api.js`**: `crearGrupo(token, body)` → `POST /grupos`;
  `listarGrupos(token)` → `GET /grupos`; `unirseGrupo(token, codigo)` →
  `POST /grupos/unirse`; `obtenerGrupo(token, id)` → `GET /grupos/:id`;
  `listarMiembros(token, id)` → `GET /grupos/:id/miembros`;
  `progresoEstudiante(token, grupoId, estudianteId)` →
  `GET /grupos/:grupoId/estudiantes/:estudianteId`; `misGrupos(token)` →
  `GET /grupos/mis-grupos`.
- **`frontend/src/constantes.js`**: `MENU_POR_ROL.profesor` pasa de
  `{ etiqueta: 'Mis grupos', ruta: null, disponible: false }` a
  `{ etiqueta: 'Mis grupos', ruta: '/grupos', disponible: true }`;
  `MENU_POR_ROL.estudiante` gana una tercera entrada
  `{ etiqueta: 'Mis grupos', ruta: '/mis-grupos', disponible: true }`.
- **`frontend/src/App.jsx`**: 4 rutas nuevas; `InicioPorRol` gana la rama
  `usuario?.rol === 'profesor'` → `<Navigate to="/grupos" replace />`,
  entre la rama `admin` (ya existente) y el fallback a `ConfigurarEnsayo`.
- **`frontend/src/styles.css`**: se reutilizan clases ya existentes
  (`tarjeta-ancha`, `banco-tabla`, `campo`, `boton`, `boton-secundario`) —
  sin clases nuevas previstas; si algún detalle visual las necesita, se
  agregan en la tarea correspondiente siguiendo el patrón append-only.

## Datos y contrato

Ya definidos en `docs/openapi.yaml` (schemas `Grupo`, `GrupoDetalle`,
`MiembroGrupo`, `ProgresoEstudiante`, `UnirseGrupoRequest`, `GrupoInput`) —
ver ese archivo para los tipos completos. Nuevo en esta tanda:

```
GrupoEstudiante:
  id: string (uuid)
  nombre: string
  profesor_nombre: string
  fecha_union: string (date-time)

GET /grupos/mis-grupos (rol estudiante) → GrupoEstudiante[]
```

## Comportamiento

- **`MisGruposProfesor.jsx`**: estados cargando/error/vacío/con datos,
  igual que el resto de listas del proyecto. Si el nombre del formulario
  de creación está vacío, el submit no se envía (validación mínima en el
  cliente); el backend igualmente rechaza con 422 "El nombre del grupo es
  obligatorio" si se lo fuerza. El código de invitación se muestra en la
  fila de cada grupo (el profesor lo necesita para compartirlo con sus
  estudiantes).
- **`GrupoDetalle.jsx`**: si `cantidad_miembros === 0`, mensaje "Todavía no
  se unió ningún estudiante" en vez de una tabla vacía. `promedio_grupo`
  puede venir `null` (grupo sin ensayos rendidos aún) → se muestra "—". En
  la tabla de miembros, `ultimo_puntaje` nulo también se muestra como "—".
- **`ProgresoEstudianteGrupo.jsx`**: mismo patrón que `Dashboard.jsx` — si
  `evolucion` viene vacía, se omite el gráfico sin romper el render (el
  estudiante puede no haber rendido ensayos todavía).
- **`MisGruposEstudiante.jsx`**: si la lista viene vacía, mensaje
  invitando a unirse con el código que le pase su profesor, sin tabla
  vacía. El campo de código se normaliza a mayúsculas antes de enviar
  (mismo criterio que ya aplica el backend, `strings.ToUpper` en
  `unirse`). Tras unirse con éxito, limpia el campo y refresca la lista.
  Si el código no existe, el backend responde 404 "Código inválido" — se
  muestra tal cual, sin reintento automático.
- **Redirección por rol**: `InicioPorRol` pasa a tener 3 ramas (`admin` →
  `/banco/items`, `profesor` → `/grupos`, resto → `ConfigurarEnsayo`), sin
  tocar el comportamiento ya existente para estudiante.

## Testing

Sin framework de testing automatizado de UI (misma decisión de las
tandas anteriores). Verificación manual con `npm run dev`: dado que esta
tanda involucra tanto rol profesor como estudiante (y las restricciones ya
conocidas de esta sesión sobre no usar contraseñas de cuentas reales/
descartables en scripts o formularios), la verificación se hará vía build
limpio + auto-revisión de código línea por línea contra este spec y contra
`docs/openapi.yaml`, salvo que se decida dar acceso a cuentas de prueba
existentes para una verificación en vivo.

## Despliegue

Mismo mecanismo que las tandas anteriores: rebuild de `api` (cambios de
backend) y `web` (frontend) en el CT 118 de Proxmox tras el merge, y
verificar en `http://192.168.0.190/` (y `http://100.93.161.84/` vía
Tailscale).

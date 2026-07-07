# Frontend — flujo estudiante (login, registro, rendir ensayo, resultado)

Fecha: 2026-07-07

## Contexto

El backend (Fases 1-7 del plan) está completo, probado (`go test ./...`) y
desplegado en el CT 118 de Proxmox (`http://192.168.0.190:8080`). El frontend
sigue siendo el scaffold de Fase 0 (`frontend/src/main.jsx`: un único `<h1>`
sin estilos ni lógica).

El proyecto completo cubre 5 flujos por rol (auth, banco/admin, ensayos,
dashboard, grupos/profesor) — demasiado para una sola tanda. Esta spec cubre
**solo el flujo del estudiante**: registro, login, configurar y rendir un
ensayo, y ver el resultado. El resto (dashboard, banco admin, grupos) queda
para tandas siguientes, cada una con su propio ciclo brainstorm → plan →
implementación.

## Alcance de esta tanda

- Registro (`POST /auth/register`) y login (`POST /auth/login`).
- Configurar ensayo: nivel (M1/M2), ejes, cantidad (10/20/30) → `POST /ensayos`.
- Rendir: una pregunta a la vez, autoguardado de respuestas, envío final.
- Resultado: puntaje /1000, desglose por eje, revisión con la alternativa
  correcta marcada.

Fuera de alcance (tandas futuras): dashboard del estudiante, banco de
preguntas (admin), grupos (profesor), importación de PDF.

## Arquitectura

- **Única dependencia nueva:** `react-router-dom` (routing por pantalla,
  decidido sobre manejar todo con estado local — se quiere poder navegar
  con el botón atrás y, más adelante, compartir links directos a un ensayo).
- Sin librería de manejo de estado global (Redux/Zustand) ni de data-fetching
  (React Query): con 5 pantallas y un estado de auth simple, `useState` +
  `useEffect` por pantalla alcanza. Se reevalúa si el dashboard o el banco
  admin (tandas futuras) lo justifican.
- **`src/api.js`**: cliente delgado sobre `fetch`. Lee la URL base de
  `import.meta.env.VITE_API_URL` (fallback `http://localhost:8080` en dev).
  Inyecta `Authorization: Bearer <token>` desde el contexto de auth en cada
  request. Centraliza el manejo de `401` (ver más abajo).
- **`src/AuthContext.jsx`**: contexto de React que guarda `{ token, usuario }`
  en `localStorage` (persiste la sesión entre recargas; TTL del JWT ya es de
  24h en el backend). Expone `login(token, usuario)` y `logout()`.
- **`src/styles.css`**: CSS plano a mano, mobile-first (~375px de ancho base,
  sin media queries de escritorio en esta tanda), variables CSS para color
  primario/texto/fondo, botones táctiles (mínimo 44px).

## Pantallas y rutas (react-router-dom)

| Ruta | Pantalla | Acceso |
|---|---|---|
| `/login` | Login (email, password) | público |
| `/registro` | Registro (nombre, email, password, rol estudiante/profesor, checkbox T&C obligatorio) | público |
| `/` | Configurar ensayo (nivel M1/M2, ejes como checkboxes con etiqueta legible — "Números", "Álgebra y funciones", "Geometría", "Probabilidad y estadística" — mapeados a los valores del enum `Eje`, cantidad 10/20/30) → `POST /ensayos` → redirige a `/ensayos/:id` | estudiante autenticado |
| `/ensayos/:id` | Rendir: una pregunta a la vez, navegación anterior/siguiente, autoguardado, botón "Enviar ensayo" | estudiante autenticado |
| `/ensayos/:id/resultado` | Resultado: puntaje /1000, desglose por eje, revisión ítem a ítem | estudiante autenticado |

**Ruta protegida:** un wrapper (`<RutaPrivada>`) redirige a `/login` si no hay
token en el `AuthContext`. Cualquier `401` de una request (token vencido)
limpia la sesión guardada y redirige a `/login`.

## Flujo de rendición (detalle)

- Al entrar a `/ensayos/:id`, `GET /ensayos/:id` trae las preguntas (sin
  `es_correcta`, ya que el ensayo está `en_progreso`).
- Cada vez que el estudiante selecciona una alternativa o cambia de pregunta
  (anterior/siguiente), se dispara `PATCH /ensayos/:id/respuestas` con la
  respuesta actual (autoguardado — no se pierde progreso si cierra la
  pestaña a mitad de camino).
- "Enviar ensayo" es una acción explícita y separada, con un diálogo de
  confirmación previo (es irreversible: `POST /ensayos/:id/enviar`).
- Tras enviar, navega a `/ensayos/:id/resultado`, que llama a
  `GET /ensayos/:id/resultado`.

## Fórmulas (KaTeX)

`enunciado` y el `texto` de cada alternativa (`ItemInput`/`Alternativa`,
"soporta LaTeX" en el contrato) se renderizan con `react-katex`, detectando
delimitadores `$...$` (inline) y `$$...$$` (bloque). Si el texto no tiene
delimitadores, se muestra tal cual como texto plano — compatible con los
ítems de prueba actuales (sin LaTeX).

## Manejo de errores

- `401` en cualquier request → limpia sesión, redirige a `/login`.
- `422` al crear ensayo con `codigo: STOCK_INSUFICIENTE` → mensaje mostrando
  `max_disponible` (del `ErrorStockInsuficiente`), no un error genérico.
- `409` al guardar/enviar un ensayo ya finalizado → mensaje "este ensayo ya
  fue enviado", no un fallo silencioso.
- Errores de red (backend caído) → mensaje genérico + botón "reintentar",
  nunca una pantalla en blanco sin explicación.
- Errores de validación del backend (`Error.codigo`/`mensaje`) se muestran
  tal cual los devuelve la API (formato uniforme ya definido en el contrato).

## Testing

Sin tests automatizados de UI en esta tanda (no hay infraestructura de
testing de componentes en el proyecto todavía). Verificación manual con el
skill `/run` o navegador contra el backend ya desplegado en
`192.168.0.190:8080`, cubriendo: registro, login, rechazo de T&C, generar
ensayo, responder, autoguardado, enviar, ver resultado, y los casos de error
(401 por token vencido, 422 por stock insuficiente).

## Despliegue

Al terminar, se reconstruye la imagen `web` (`docker compose up -d --build
web`) en el CT 118 de Proxmox y se verifica en `http://192.168.0.190/`. El
`Dockerfile` del frontend ya existe (`frontend/Dockerfile`, build con Vite +
nginx); se necesita pasar `VITE_API_URL=http://192.168.0.190:8080` como
build arg para que el bundle apunte a la API real en producción (en dev,
`npm run dev` seguirá usando `http://localhost:8080` por defecto).

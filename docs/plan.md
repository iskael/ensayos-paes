# Plan de Implementación — App de Ensayos PAES Matemáticas (MVP)

> Paso 4 de SDD. Base: `spec_funcional_mvp.md` + `openapi.yaml`.
> Estrategia: *vertical slices* que entregan incrementos funcionales y testeables.

---

## 1. Stack propuesto (ajustable)

- **Backend:** Go — router liviano (chi/echo), `golang-migrate` para migraciones, `sqlc` o `pgx` para acceso a datos.
- **Contrato → código:** `oapi-codegen` genera tipos y stubs del servidor a partir de `openapi.yaml` (mantiene el contrato como fuente de verdad).
- **Frontend:** React + Vite, **mobile-first**, KaTeX para fórmulas, recharts para el gráfico de evolución.
- **DB:** PostgreSQL (SQLite para desarrollo local si se prefiere).
- **Auth:** JWT (access token), hashing de contraseña con bcrypt/argon2.
- **Imágenes:** almacenamiento en bucket/volumen; la API solo guarda la `url`.

> Si cambias de stack, lo único atado a Go/React es la sección 6; el resto (modelo, orden de fases, reglas) es portable.

## 2. Arquitectura (capas)

- **API (HTTP):** handlers generados desde OpenAPI; validación de request; mapeo a casos de uso.
- **Dominio / servicios:** reglas de negocio (generación de ensayo, scoring, validación de clave, RBAC).
- **Repositorios:** acceso a datos (Postgres).
- **Middleware transversal:** autenticación, autorización por rol, manejo de errores uniforme (schema `Error`).

## 3. Modelo de datos físico (tablas)

- `usuarios` — id, nombre, email (único), password_hash, rol, fecha_creacion, activo.
- `grupos` — id, nombre, profesor_id (FK), codigo_invitacion (único), fecha_creacion.
- `grupo_miembros` — grupo_id (FK), estudiante_id (FK), fecha_union. PK compuesta.
- `examenes_fuente` — id, nombre, anio_admision, tipo, nivel, edicion, url_pdf, fecha_publicacion.
- `items` — id, examen_fuente_id (FK, nullable), enunciado, imagen_url, eje, nivel, dificultad, origen, estado, peso, explicacion, fecha_creacion.
- `alternativas` — id, item_id (FK), etiqueta, texto, imagen_url, es_correcta.
- `ensayos` — id, estudiante_id (FK), nivel, ejes (jsonb/array), cantidad, modo, estado, fecha_inicio, fecha_fin, puntaje, puntos_obtenidos, puntos_posibles, correctas, total.
- `ensayo_items` — id, ensayo_id (FK), item_id (FK), orden, peso_snapshot, respuesta_seleccionada, es_correcta.

**Índices clave**
- `items (estado, nivel, eje)` — para la selección aleatoria.
- `alternativas (item_id)`.
- `ensayos (estudiante_id, fecha_fin)` — historial/dashboard.
- `grupo_miembros (estudiante_id)` y `(grupo_id)`.

## 4. Reglas críticas a implementar (con su test)

- **Generación de ensayo (RN-01):** filtra `estado=publicado` + nivel + ejes; reparto equitativo por eje; sin repetir; si falta stock → `422` con `max_disponible` y `disponibles_por_eje`.
  - *Test:* stock justo, stock insuficiente, distribución por eje, no repetición.
- **Scoring normalizado (RN-02):** `puntaje = round((puntos_obtenidos / puntos_posibles) * 1000)`; sin responder = incorrecto; `puntos_posibles=0 → 0`.
  - *Test:* todo correcto = 1000, mezcla, ítems sin responder, división exacta e inexacta.
- **Snapshot de peso:** `ensayo_items.peso_snapshot` se fija al generar; editar el ítem luego no altera resultados históricos.
  - *Test:* corregir, editar peso del ítem, re-leer resultado → sin cambios.
- **Validación de clave (RN-03):** suma de pesos publicados del examen = 1000, si no → `422`.
- **Publicación (RN-04):** ítem participa solo si `publicado`; importados por PDF entran `borrador`.
- **RBAC (RN-06):** profesor solo ve datos de *sus* grupos; admin solo banco; estudiante solo lo propio.
  - *Test:* acceso cruzado entre roles y entre profesores → `403`.

## 5. Fases (vertical slices)

**Fase 0 — Fundaciones**
- Estructura del repo (SDD-friendly), CI, linters.
- `oapi-codegen` desde `openapi.yaml`; migraciones base; conexión DB.
- Esqueleto de frontend mobile-first (layout base, KaTeX).
- Middleware de errores, auth y RBAC (vacíos pero cableados).

**Fase 1 — Auth y cuentas** (HU-01..03)
- Registro, login, logout, `/me`.
- Emisión/validación de JWT; hashing de contraseña.
- *DoD:* un usuario se registra, inicia sesión y consulta su perfil.

**Fase 2 — Banco (admin), carga manual** (HU-25, 26, 26B, 27, 29, imágenes)
- CRUD de exámenes; CRUD de ítems + alternativas (4, A–D); subir imágenes.
- Definir clave (validación suma 1000); publicar/ocultar.
- *DoD:* el admin carga manualmente ítems oficiales y los publica.

**Fase 3 — Ensayos (estudiante)** (HU-06..08, 11..13, 15, 17..18, 20)
- Configurar (nivel + ejes + cantidad 10/20/30), generar (RN-01).
- Responder/guardar, enviar, corregir (RN-02), resultado + revisión + desglose por eje.
- Frontend de rendición mobile-first (una pregunta a la vez, navegación).
- *DoD:* un estudiante rinde un ensayo completo y ve su puntaje en escala 1000.

**Fase 4 — Dashboard (estudiante)** (HU-21..22)
- Historial; resumen; gráfico de evolución.
- *DoD:* el estudiante visualiza su progreso tras varios ensayos.

**Fase 5 — Grupos (profesor)** (HU-34..38)
- Crear grupo (código), unirse por código, miembros, progreso agregado e individual.
- *DoD:* un profesor crea un grupo, inscribe estudiantes y ve su avance.

**Fase 6 — Importación de PDF asistida** (HU-28)
- Subir PDF → extracción → ítems `borrador` para revisión humana.
- *DoD:* el admin sube un PDF y obtiene borradores editables (con revisión obligatoria antes de publicar).

**Fase 7 — Endurecimiento y cierre**
- Pulido mobile-first; validaciones; pruebas de contrato vs `openapi.yaml`.
- Integración de **Términos y Condiciones** (aceptación en el registro).
- Revisión de seguridad y datos de menores.

> Orden no negociable: **Fase 2 antes de Fase 3** (los ensayos requieren ítems publicados). El resto admite reordenarse.

## 6. Decisiones técnicas transversales

- **Mobile-first:** breakpoints desde móvil hacia arriba; objetivos táctiles grandes; ensayo optimizado para pantalla pequeña (una pregunta visible, barra de avance).
- **Fórmulas:** KaTeX en enunciados y alternativas; las figuras se muestran como imágenes (`imagen_url`).
- **Selección aleatoria:** MVP con `ORDER BY random()` filtrado por índice; en v2 evaluar estrategias más eficientes si crece el banco.
- **Errores:** formato uniforme (`{codigo, mensaje}`); `STOCK_INSUFICIENTE` con datos extra.
- **Seguridad:** validación de entrada, rate limiting básico en login, tokens con expiración.

## 7. Estrategia de pruebas

- **Unitarias:** scoring, generación de ensayo, validación de clave (núcleo del dominio).
- **Integración:** endpoints por fase, con DB de prueba.
- **Contrato:** validar requests/responses contra `openapi.yaml`.
- **RBAC:** matriz de acceso por rol (incluye accesos cruzados que deben fallar).

## 8. Riesgos y mitigaciones

- *Calidad de extracción de PDF (fórmulas/figuras):* revisión humana obligatoria; empezar por carga manual (Fase 2) para no bloquear el resto.
- *Stock insuficiente al inicio:* cargar suficientes ítems oficiales antes de habilitar ensayos amplios.
- *Rendimiento de selección aleatoria al crecer el banco:* aceptable en MVP; optimización en v2.

## 9. Fuera de alcance (v2)
- Generación de ítems con IA (diseño ya cerrado en `diseno_generacion_ia_v2.md`).
- Recomendaciones adaptativas, modo cronometrado, asignación/comparación de grupos, puntaje PAES estimado por equating.

## 10. Entregable de cierre
- **Términos y Condiciones** (confidencialidad + buen uso), integrados a la aceptación en el registro (Fase 7).

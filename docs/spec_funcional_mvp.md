# Spec Funcional — App de Ensayos PAES Matemáticas (MVP)

> Paso 2 de SDD. Base para el contrato OpenAPI y el plan de implementación.
> Documento previo: `historias_usuario_ensayos_paes.md`.

---

## 1. Propósito

- Plataforma web donde estudiantes de 4° medio rinden **ensayos PAES de matemáticas** con ítems aleatorios del banco, filtrados por **nivel (M1/M2)** y **eje temático**.
- Entrega **puntaje en escala 1000** y feedback de progreso por un dashboard.
- Un **administrador** alimenta y cura el banco (exámenes, claves, ítems).
- Un **profesor** agrupa estudiantes y monitorea su avance.

## 2. Alcance

### En MVP
- Cuentas y autenticación para 3 roles.
- Banco de ítems **oficiales** (carga manual + PDF con extracción asistida y revisión humana).
- Clave de corrección por examen (pesos que suman 1000).
- Configuración y ejecución de ensayos aleatorios por nivel + ejes.
- Puntaje normalizado a 1000, revisión de respuestas, desglose por eje.
- Dashboard del estudiante (historial + evolución).
- Grupos del profesor (crear, inscribir, monitorear).

### Fuera de MVP (v2)
- Generación de ítems con IA (con revisión humana).
- Recomendaciones adaptativas de práctica.
- Modo cronometrado.
- Asignación de ensayos a grupos y comparación entre grupos.
- Puntaje PAES estimado por equating (IRT).
- Importación 100% automática de PDF.

## 3. Roles y permisos

| Acción | Estudiante | Profesor | Admin |
|---|:---:|:---:|:---:|
| Registro / login | ✔ | ✔ | ✔ |
| Configurar y rendir ensayos | ✔ | – | – |
| Ver resultados y dashboard propio | ✔ | – | – |
| Unirse a un grupo (por código) | ✔ | – | – |
| Crear grupos e inscribir estudiantes | – | ✔ | – |
| Ver progreso de su grupo / estudiantes | – | ✔ | – |
| Gestionar banco (examen, clave, ítems, PDF) | – | – | ✔ |
| Publicar / ocultar ítems | – | – | ✔ |
| Gestionar usuarios | – | – | ✔ |

- Un usuario tiene **un** rol. (Si en el futuro un profesor también quiere practicar, se evalúa en v2.)

## 4. Dominio (glosario)

- **Nivel:** `M1` (Competencia Matemática 1) / `M2` (Competencia Matemática 2).
- **Eje temático:** `numeros`, `algebra_funciones`, `geometria`, `probabilidad_estadistica`.
- **Dificultad:** `baja`, `media`, `alta`.
- **Origen del ítem:** `oficial` (DEMRE) / `generado` (IA, v2).
- **Estado del ítem:** `borrador`, `publicado`, `oculto`. Solo los `publicado` entran en ensayos.

## 5. Modelo de datos (entidades)

**Usuario**
- `id`, `nombre`, `email` (único), `password_hash`, `rol` (`estudiante|profesor|admin`), `fecha_creacion`, `activo`.

**Grupo**
- `id`, `nombre`, `profesor_id` → Usuario, `codigo_invitacion` (único), `fecha_creacion`.

**GrupoMiembro** (N:M estudiante–grupo)
- `grupo_id` → Grupo, `estudiante_id` → Usuario, `fecha_union`.

**ExamenFuente**
- `id`, `nombre`, `anio_admision`, `tipo` (`PAES_Regular|PAES_Invierno|PDT`), `nivel` (`M1|M2`), `edicion`, `url_pdf`, `fecha_publicacion`.
- La **clave de corrección** del examen = el conjunto de (`respuesta_correcta`, `peso`) de sus ítems. Regla: los pesos de los ítems publicados de un examen suman **1000**.

**Item (Pregunta)**
- `id`, `examen_fuente_id` → ExamenFuente (nullable si suelto/generado), `enunciado` (texto con soporte LaTeX), `imagen_url` (nullable), `eje`, `nivel`, `dificultad`, `origen`, `estado`, `peso` (entero, puntos), `explicacion` (nullable), `fecha_creacion`.

**Alternativa**
- `id`, `item_id` → Item, `etiqueta` (`A|B|C|D`), `texto` (LaTeX), `imagen_url` (nullable), `es_correcta` (bool).
- Cada ítem tiene **exactamente 4 alternativas** (A–D, estándar PAES); exactamente una con `es_correcta = true`.

**Ensayo** (sesión de práctica de un estudiante)
- `id`, `estudiante_id` → Usuario, `nivel`, `ejes` (lista), `cantidad_solicitada`, `modo` (`libre`; `cronometrado` en v2), `estado` (`en_progreso|finalizado`), `fecha_inicio`, `fecha_fin` (nullable), `puntaje` (0–1000, nullable hasta finalizar), `puntos_obtenidos`, `puntos_posibles`, `correctas`, `total`.

**EnsayoItem** (ítems del ensayo + respuesta del estudiante)
- `id`, `ensayo_id` → Ensayo, `item_id` → Item, `orden`, `peso_snapshot` (peso del ítem al momento de generar el ensayo), `respuesta_seleccionada` (nullable), `es_correcta` (nullable hasta corregir).

> **Nota de diseño:** `peso_snapshot` y el desglose se congelan al generar/corregir, para que editar un ítem después **no** altere resultados históricos.

## 6. Reglas de negocio

**RN-01 — Generación de ensayo aleatorio**
- Selecciona ítems con `estado = publicado`, `nivel = nivel_elegido`, `eje ∈ ejes_elegidos`.
- No repite ítems dentro del mismo ensayo.
- **Distribución por eje:** reparte la cantidad solicitada de forma equitativa entre los ejes elegidos cuando hay stock suficiente; completa aleatoriamente el remanente.
- Si no hay ítems suficientes para la cantidad solicitada, **devuelve error** indicando el máximo disponible; **no** se arma un ensayo parcial.

**RN-02 — Cálculo de puntaje (normalizado a 1000)**
- `puntos_posibles` = suma de `peso_snapshot` de todos los ítems del ensayo.
- `puntos_obtenidos` = suma de `peso_snapshot` de los ítems respondidos correctamente.
- `puntaje` = `round( (puntos_obtenidos / puntos_posibles) × 1000 )`.
- Si `puntos_posibles = 0` → `puntaje = 0`.
- Ítem sin responder = incorrecto (no suma puntos).

**RN-03 — Clave de corrección**
- Al definir/cargar la clave de un examen, el sistema valida que la suma de pesos de sus ítems publicados sea **1000**; si no, advierte y no permite publicar hasta corregir.
- Ítems sueltos o sin examen asociado reciben un `peso` por defecto definido por el admin.

**RN-04 — Publicación de ítems**
- Un ítem solo participa en ensayos cuando está `publicado`.
- Ítems cargados desde PDF entran como `borrador` y requieren **revisión/edición humana** antes de `publicado`.

**RN-05 — Desglose por eje**
- Al corregir, se calcula correctas/total y puntos por cada eje presente en el ensayo, para el feedback y el dashboard.

**RN-06 — Acceso del profesor**
- Un profesor solo ve datos de estudiantes que pertenecen a **sus** grupos.

## 7. Requisitos funcionales por módulo

### 7.1 Cuentas y autenticación (E1)
- Registro con nombre, email, contraseña; email único; contraseña con mínimo de seguridad.
- Login / logout; sesión segura.
- (v2) Recuperar contraseña; editar perfil.

### 7.2 Configuración del ensayo (E2)
- Seleccionar nivel (M1 o M2).
- Seleccionar uno o más ejes.
- Definir cantidad de preguntas: valores **predefinidos 10 / 20 / 30** (sin valores libres).
- (v2) Modo cronometrado; filtro por dificultad.

### 7.3 Ejecución del ensayo (E3)
- Generar ensayo (RN-01) y mostrar ítems (enunciado, alternativas, imagen si aplica, fórmulas renderizadas).
- Responder, navegar entre preguntas, enviar.
- Al enviar: confirmar si hay no respondidas; corregir y persistir resultado.
- (v2) Marcar para revisar; cronómetro.

### 7.4 Resultados y feedback (E4)
- Mostrar puntaje (escala 1000) + correctas/total.
- Revisión: por ítem, qué respondió, la correcta y (v2) la explicación.
- Desglose por eje.

### 7.5 Dashboard del estudiante (E5)
- Historial de ensayos (fecha, nivel, ejes, puntaje).
- Gráfico de evolución de puntaje en el tiempo.
- (v2) Mapa de fortalezas/debilidades; recomendaciones.

### 7.6 Administración del banco (E6)
- CRUD de ExamenFuente.
- Definir/cargar clave (respuesta correcta + peso por ítem), con validación de suma 1000.
- CRUD de ítems con alternativas, eje, nivel, dificultad, imagen, explicación.
- Carga de PDF + extracción asistida → ítems en `borrador` para revisión.
- Publicar / ocultar ítems.
- (v2) Gestión de usuarios.

### 7.7 Grupos y seguimiento docente (E9)
- Crear grupo (genera código de invitación).
- Estudiante se une por código.
- Ver miembros del grupo.
- Ver progreso agregado del grupo y detalle por estudiante.
- (v2) Asignar ensayos; comparar grupos.

## 8. Requisitos no funcionales
- Renderizado de fórmulas (MathJax/KaTeX); figuras como **imágenes**.
- Control de acceso por rol (estudiante/profesor/admin).
- Diseño **mobile-first**: se diseña primero para móvil y se escala hacia notebook; debe garantizar el acceso correcto desde dispositivos móviles.
- Protección de datos personales; usuarios menores de edad (ver §11, Términos y Condiciones).
- (v2) Selección aleatoria eficiente al crecer el banco; auditoría de cambios del banco.

## 9. Flujos principales (happy paths)

**F1 — Estudiante rinde un ensayo**
1. Inicia sesión → elige nivel + ejes + cantidad.
2. Sistema genera ensayo aleatorio (RN-01).
3. Responde y navega; envía.
4. Sistema corrige (RN-02) y muestra puntaje + revisión + desglose por eje.
5. Resultado queda en su historial y alimenta el dashboard.

**F2 — Admin incorpora un examen**
1. Registra ExamenFuente (año, tipo, nivel, URL).
2. Sube PDF → extracción asistida → ítems en `borrador`.
3. Revisa/edita ítems y alternativas; define eje/dificultad/imagen.
4. Carga la clave (pesos) → valida suma 1000.
5. Publica los ítems → quedan disponibles para ensayos.

**F3 — Profesor monitorea su grupo**
1. Crea grupo → comparte código.
2. Estudiantes se unen.
3. Revisa progreso agregado y detalle por estudiante.

## 10. Decisiones menores (resueltas)
- [x] **Stock insuficiente:** el sistema **informa error** indicando el máximo disponible; no arma ensayos parciales. ✓
- [x] **Tamaños de ensayo:** valores **predefinidos 10 / 20 / 30**. ✓
- [x] **N° de alternativas:** **4 (A–D)**, estándar PAES. ✓

## 11. Pendiente de cierre — Términos y Condiciones
- Se entregará una propuesta de **T&C** al final del proceso, orientada a:
  - **Confidencialidad** y protección de datos personales (incl. usuarios menores de edad).
  - **Buen uso** de la plataforma (conducta, propiedad del contenido DEMRE, prohibición de scraping/compartir credenciales, etc.).

---

### Próximo paso (SDD)
- Definiciones cerradas. Pendiente, cuando se indique: redactar el **contrato OpenAPI** (`openapi.yaml`) a partir de este modelo y requisitos.

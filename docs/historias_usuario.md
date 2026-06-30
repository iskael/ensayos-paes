# App de Ensayos PAES Matemáticas — Brainstorming & Historias de Usuario

> Documento base (paso 1 de SDD). Objetivo: definir el alcance y extraer historias de usuario antes de pasar a la especificación técnica (spec → OpenAPI → plan → código).

---

## 1. Visión del producto

- Plataforma web que permite a estudiantes de **4° medio** realizar **ensayos PAES de matemáticas** con ejercicios aleatorios.
- El banco de preguntas se nutre de los **exámenes oficiales DEMRE** ya catalogados (2022–2026, M1/M2, Regular/Invierno) más **ejercicios generados** sobre la misma base.
- Cada estudiante tiene un **espacio personal** con dashboard de resultados y feedback de su avance.
- Un **administrador** mantiene el banco: sube exámenes, transcribe/cura ítems y genera nuevos ejercicios.

## 2. Actores

- **Estudiante** — usuario final; rinde ensayos y consulta su progreso.
- **Administrador** — gestor de contenidos; alimenta y cura el banco de preguntas.
- **Profesor** — crea grupos/cursos, inscribe estudiantes y monitorea su progreso (en v2 les asigna ensayos). No edita el banco de preguntas; eso es del administrador.

## 3. Modelo conceptual (entidades preliminares)

- **Usuario** — datos de cuenta + rol.
- **Eje temático** — Números, Álgebra y Funciones, Geometría, Probabilidad y Estadística.
- **Nivel** — M1 / M2.
- **Examen fuente** — referencia al PDF DEMRE (año, edición, nivel, URL).
- **Clave de corrección** — por cada examen, define la respuesta correcta y el **peso (puntos)** de cada pregunta; los pesos del examen completo suman **1000**.
- **Ítem (Pregunta)** — enunciado, alternativas, respuesta correcta, **peso/puntos**, eje, dificultad, nivel, origen (oficial / generado), explicación, examen fuente, imagen/figura opcional.
- **Ensayo** — configuración elegida por el estudiante (ejes, nivel, cantidad de ítems, modo).
- **Intento / Resultado** — instancia rendida: respuestas, puntaje, tiempo, fecha, desempeño por eje.
- **Grupo / Curso** — agrupación de estudiantes creada por un profesor (nombre, profesor dueño, código de invitación, miembros).
- **Asignación** *(v2)* — ensayo/configuración que un profesor propone a un grupo, con fecha sugerida.

## 4. Decisiones abiertas (a confirmar antes de la spec)

- [x] **Alcance de nivel:** M1 **y** M2 desde el inicio. ✓
- [x] **Puntaje:** escala **base 1000**. Cada examen tiene una **clave** que define el peso (puntos) de cada pregunta. ✓
  - [x] *Resuelto:* en ensayos **aleatorios/mixtos** el puntaje se **normaliza** = (puntos obtenidos ÷ puntos posibles del ensayo) × 1000. ✓
- [x] **Generación de ejercicios:** queda para **v2** (con revisión humana obligatoria). El MVP usa solo el banco cargado por el admin. ✓
- [x] **Rol Profesor / grupos:** **incluido en el MVP**. ✓
- [x] **Figuras geométricas:** se almacenan como **imágenes** adjuntas al ítem (sin editor de figuras), para no complejizar la app. ✓
- [x] **Datos de menores / términos:** se abordará con **Términos y Condiciones** (confidencialidad + buen uso de la plataforma), entregados como deliverable de cierre. ✓
- [x] **Carga del banco:** **ambas** — carga de **PDF** (con extracción asistida + revisión humana) y **entrada manual** de textos/preguntas. ✓

## 5. Épicas

- **E1.** Cuenta y autenticación
- **E2.** Configuración del ensayo
- **E3.** Realización del ensayo
- **E4.** Resultados y feedback
- **E5.** Dashboard y progreso
- **E6.** Administración del banco de preguntas
- **E7.** Generación de ejercicios (IA)
- **E8.** Requisitos no funcionales (transversales)
- **E9.** Grupos y seguimiento docente (Profesor)

---

## 6. Historias de usuario

> Formato: *Como [rol], quiero [acción] para [beneficio]* + criterios de aceptación (CA) + prioridad.

### E1 — Cuenta y autenticación

**HU-01 (MVP) — Registro**
- Como estudiante, quiero registrarme con correo y contraseña para tener un espacio personal.
- CA: valida correo único; contraseña con mínimo de seguridad; confirma registro; crea perfil vacío.

**HU-02 (MVP) — Inicio de sesión**
- Como usuario, quiero iniciar sesión para acceder a mis datos.
- CA: credenciales válidas dan acceso; credenciales inválidas muestran error; sesión persistente segura.

**HU-03 (MVP) — Cierre de sesión**
- Como usuario, quiero cerrar sesión para proteger mi cuenta en equipos compartidos.

**HU-04 (v2) — Recuperar contraseña**
- Como usuario, quiero recuperar mi contraseña por correo para no perder el acceso.

**HU-05 (v2) — Editar perfil**
- Como estudiante, quiero editar mis datos (nombre, colegio, nivel objetivo) para personalizar mi experiencia.

### E2 — Configuración del ensayo

**HU-06 (MVP) — Seleccionar contenidos por eje**
- Como estudiante, quiero elegir uno o más ejes temáticos para ejercitar lo que necesito.
- CA: lista de ejes (Números, Álgebra y Funciones, Geometría, Probabilidad y Estadística); selección múltiple; debe elegir al menos uno.

**HU-07 (MVP) — Definir cantidad de preguntas**
- Como estudiante, quiero elegir cuántas preguntas tendrá el ensayo (p. ej. 10/20/30) para ajustarlo a mi tiempo.

**HU-08 (MVP) — Elegir nivel (M1/M2)**
- Como estudiante, quiero elegir el nivel (M1 o M2) para ejercitar según la prueba que rendiré.
- CA: puede elegir M1 o M2; el banco filtra los ítems del nivel seleccionado.

**HU-09 (v2) — Modo cronometrado vs. libre**
- Como estudiante, quiero elegir entre modo cronometrado (simula la PAES real) o libre, según mi objetivo de práctica.

**HU-10 (v2) — Filtrar por dificultad**
- Como estudiante, quiero filtrar por dificultad para ir subiendo el nivel progresivamente.

### E3 — Realización del ensayo

**HU-11 (MVP) — Generar ensayo aleatorio**
- Como estudiante, quiero que el sistema arme un ensayo con preguntas aleatorias según mi configuración, para que cada ensayo sea distinto.
- CA: selecciona ítems aleatorios que cumplan los filtros (ejes, nivel, cantidad); no repite ítems dentro del mismo ensayo; falla con mensaje claro si no hay suficientes ítems.

**HU-12 (MVP) — Responder preguntas**
- Como estudiante, quiero ver y responder cada pregunta (selección de alternativa) para completar el ensayo.
- CA: muestra enunciado, alternativas, figura si aplica; permite seleccionar una alternativa; renderiza fórmulas matemáticas correctamente.

**HU-13 (MVP) — Navegar entre preguntas**
- Como estudiante, quiero avanzar, retroceder y saltar entre preguntas para responder en el orden que prefiera.

**HU-14 (v2) — Marcar pregunta para revisar**
- Como estudiante, quiero marcar preguntas dudosas para volver a ellas antes de enviar.

**HU-15 (MVP) — Enviar ensayo**
- Como estudiante, quiero enviar el ensayo para obtener mi resultado.
- CA: confirma si hay preguntas sin responder; al enviar, calcula y guarda el resultado.

**HU-16 (v2) — Cronómetro / tiempo límite**
- Como estudiante, quiero ver el tiempo transcurrido (y límite si aplica) para entrenar la gestión del tiempo.
- CA: en modo cronometrado, al llegar a 0 se envía automáticamente.

### E4 — Resultados y feedback

**HU-17 (MVP) — Ver puntuación**
- Como estudiante, quiero ver mi puntaje al terminar para saber cómo me fue.
- CA: el puntaje se calcula en **escala base 1000** según el **peso** de cada pregunta (definido en la clave del examen); en ensayos mixtos se normaliza a 1000. Muestra también correctas/total.

**HU-18 (MVP) — Revisar respuestas**
- Como estudiante, quiero revisar cuáles acerté y cuáles fallé, viendo la respuesta correcta, para aprender de mis errores.

**HU-19 (v2) — Ver explicación del ítem**
- Como estudiante, quiero leer la explicación/solución de cada pregunta para entender el procedimiento.

**HU-20 (MVP) — Desempeño por eje**
- Como estudiante, quiero ver mi resultado desglosado por eje temático para identificar mis debilidades.

### E5 — Dashboard y progreso

**HU-21 (MVP) — Historial de ensayos**
- Como estudiante, quiero ver el listado de mis ensayos anteriores (fecha, ejes, puntaje) para llevar registro.

**HU-22 (MVP) — Evolución de puntaje**
- Como estudiante, quiero ver un gráfico de mi puntaje a lo largo del tiempo para visualizar mi progreso.

**HU-23 (v2) — Mapa de fortalezas y debilidades**
- Como estudiante, quiero ver mi desempeño acumulado por eje para enfocar mi estudio.

**HU-24 (v2) — Recomendación de práctica**
- Como estudiante, quiero recibir sugerencias de qué eje practicar según mi desempeño, para estudiar de forma más eficiente.

### E6 — Administración del banco de preguntas

**HU-25 (MVP) — Registrar examen fuente**
- Como administrador, quiero registrar un examen DEMRE (año, edición, nivel, URL del PDF) para tener trazabilidad del origen de los ítems.

**HU-26 (MVP) — Crear/editar ítems**
- Como administrador, quiero crear y editar preguntas (enunciado, alternativas, respuesta correcta, **peso/puntos**, eje, nivel, dificultad, explicación, figura) para construir el banco.
- CA: campos obligatorios validados; soporte para fórmulas matemáticas; soporte para imagen/figura; vínculo opcional al examen fuente.

**HU-26B (MVP) — Definir clave de corrección del examen**
- Como administrador, quiero cargar/definir la clave de un examen (respuesta correcta + peso de cada pregunta) para que el puntaje se calcule en escala 1000.
- CA: permite ingresar el peso por pregunta; valida que los pesos del examen completo sumen 1000; sirve de base para el cálculo de puntaje de los ítems de ese examen.

**HU-27 (MVP) — Etiquetar por eje y dificultad**
- Como administrador, quiero clasificar cada ítem por eje y dificultad para que los filtros del estudiante funcionen.

**HU-28 (MVP) — Cargar PDF y extracción asistida**
- Como administrador, quiero subir el PDF del examen y recibir asistencia para extraer las preguntas, para acelerar la carga del banco.
- CA: permite subir el PDF; ofrece extracción asistida (texto/preguntas); **toda pregunta extraída requiere revisión/edición humana antes de publicarse**; convive con la entrada manual (HU-26).

**HU-29 (v2) — Aprobar / despublicar ítems**
- Como administrador, quiero aprobar, ocultar o despublicar ítems para controlar qué se usa en los ensayos.

**HU-30 (v2) — Gestionar usuarios**
- Como administrador, quiero ver y administrar las cuentas de estudiantes para soporte y moderación.

### E7 — Generación de ejercicios (IA)

**HU-31 (v2) — Generar ítems nuevos por eje**
- Como administrador, quiero generar ejercicios nuevos a partir del banco/eje (vía IA) para ampliar la base de práctica.
- CA: el ítem generado queda en estado "borrador/pendiente"; nunca se publica sin revisión.

**HU-32 (v2) — Revisar y aprobar ítems generados**
- Como administrador, quiero revisar, editar y aprobar los ítems generados antes de publicarlos, para garantizar calidad y correctitud.

**HU-33 (v2) — Distinguir origen del ítem**
- Como administrador y estudiante, quiero saber si un ítem es oficial DEMRE o generado, para transparencia.

### E8 — Requisitos no funcionales (transversales)

- **RNF-01 (MVP)** Renderizado correcto de fórmulas matemáticas (p. ej. MathJax/KaTeX); las figuras se muestran como **imágenes**.
- **RNF-02 (MVP)** Control de acceso por rol (estudiante / profesor / administrador).
- **RNF-03 (MVP)** Diseño **mobile-first** (optimizado para móvil primero; usable también en notebook), para garantizar el acceso correcto desde dispositivos móviles.
- **RNF-04 (MVP)** Protección de datos personales; consideración de usuarios menores de edad.
- **RNF-05 (v2)** Rendimiento: selección aleatoria eficiente aunque el banco crezca.
- **RNF-06 (v2)** Trazabilidad/auditoría de cambios en el banco de preguntas.

### E9 — Grupos y seguimiento docente (Profesor)

**HU-34 (MVP) — Crear grupo/curso**
- Como profesor, quiero crear un grupo (curso) para organizar a mis estudiantes.
- CA: define un nombre; el sistema genera un código/enlace de invitación único.

**HU-35 (MVP) — Unirse a un grupo (estudiante)**
- Como estudiante, quiero unirme al grupo de mi profesor con un código para que pueda ver mi avance.
- CA: un código válido asocia al estudiante con el grupo; un código inválido muestra error.

**HU-36 (MVP) — Ver lista de miembros**
- Como profesor, quiero ver la lista de estudiantes inscritos en cada grupo para gestionarlo.

**HU-37 (MVP) — Ver progreso del grupo**
- Como profesor, quiero ver el desempeño agregado de mi grupo (puntajes, evolución, desempeño por eje) para enfocar mis clases.
- CA: panel con resultados del grupo y acceso al detalle por estudiante.

**HU-38 (MVP) — Ver detalle de un estudiante**
- Como profesor, quiero ver el historial y desempeño individual de un estudiante de mi grupo para apoyarlo de forma puntual.

**HU-39 (v2) — Asignar ensayo a un grupo**
- Como profesor, quiero asignar un ensayo (ejes/nivel definidos) a mi grupo para dirigir su práctica.
- CA: la asignación aparece en el espacio del estudiante; el profesor ve quién la completó.

**HU-40 (v2) — Comparar grupos**
- Como profesor, quiero comparar el desempeño entre mis grupos para detectar diferencias y priorizar apoyo.

---

## 7. Resumen de alcance MVP

- Registro / login / logout (estudiante, profesor, administrador).
- Selección de **nivel M1 y M2**.
- Banco con ítems **oficiales** cargados manualmente por el admin.
- Configuración de ensayo: ejes + nivel + cantidad.
- Ensayo aleatorio, responder, navegar, enviar.
- Resultado: **puntaje en escala base 1000** (según pesos de la clave; normalizado en ensayos mixtos), revisión de respuestas, desglose por eje.
- Dashboard del estudiante: historial + gráfico de evolución.
- Admin: registrar examen fuente + **clave de corrección (pesos)** + CRUD de ítems + etiquetado + **carga de PDF con extracción asistida** + entrada manual.
- **Profesor:** crear grupos, inscribir estudiantes, ver progreso del grupo e individual.

**Para v2:** generación IA con revisión, recomendaciones adaptativas, modo cronometrado, asignación de ensayos a grupos, comparación entre grupos, puntaje PAES estimado por equating.

---

## 8. Próximo paso (SDD)

- Confirmar las **decisiones abiertas** (sección 4).
- Convertir el MVP en **especificación** + **contrato OpenAPI** + **plan de implementación**.

# LEARNINGS

Registro de decisiones técnicas y aprendizajes del proyecto.

## Formato
- **Fecha — Tema:** decisión / contexto / consecuencia.

## Decisiones iniciales
- **Puntaje base 1000 con normalización** en ensayos mixtos: `(obtenidos/posibles)*1000`.
- **peso_snapshot** en `ensayo_items` para no alterar resultados históricos al editar ítems.
- **Figuras como imágenes** (sin editor de figuras) para simplificar.
- **Banco antes que Ensayos** en el orden de implementación.
- **Generación IA → v2** (diseño cerrado en docs/diseno_generacion_ia_v2.md).

## Fase 2 — Banco de preguntas
- **Ítems nacen en `borrador`** siempre (RN-04); publicar exige peso > 0 y 4 alternativas válidas.
- **Clave**: `PUT /examenes/{id}/clave` valida que la suma de pesos enviados sea 1000 antes de aplicar.
- **Imágenes**: almacenamiento local en disco (`UPLOADS_DIR`), servidas estáticas en `/uploads/*`; nombre de archivo aleatorio, whitelist de extensiones.
- **Listar ítems**: N+1 (IDs filtrados + lectura individual con alternativas) aceptable al volumen del MVP; revisar si el banco crece mucho.

## Fase 3 — Ensayos
- **Distribución por eje** (RN-01): reparto equitativo con `domain.DistribuirCantidad`; si un eje no tiene stock para su cuota, el remanente se completa con la capacidad extra de otros ejes elegidos. Si aun así falta, se rechaza el ensayo completo (no se arman parciales) con `STOCK_INSUFICIENTE` + `max_disponible` + detalle por eje.
- **Ocultar respuesta correcta**: `ensayoResp` (mientras `en_progreso`) nunca serializa `es_correcta` de las alternativas; solo `resultadoResp` (tras finalizar) la expone. Es una decisión de la capa HTTP, no del repo (el repo siempre carga el dato completo).
- **peso_snapshot**: se fija al generar (`ensayo_items.peso_snapshot`); el puntaje usa ese valor, no el peso actual del ítem — así una edición posterior del ítem no altera resultados históricos.
- **Acceso cruzado entre estudiantes**: intentar ver/operar el ensayo de otro estudiante responde 404 (no 403), para no revelar que el recurso existe.
- **Pendiente de verificar en el primer run real**: binding de parámetros Go (`[]string`) contra columnas Postgres de tipo enum / enum[] (`rol`, `nivel`, `eje`, `eje[]`, `estado_item`, etc.) sin cast explícito en el SQL. Debería funcionar por inferencia de tipo de Postgres a partir del contexto (columna destino) con el modo de ejecución por defecto de pgx v5, pero no se pudo compilar/ejecutar contra una instancia real en este entorno — probar `go test ./...` y un `POST /ensayos` de extremo a extremo apenas se levante el Postgres local.

## Fase 4 — Dashboard
- **Reutiliza `domain.CalcularDesglosePorEje`**: el desempeño agregado por eje del dashboard usa la misma función pura que el desglose de un ensayo individual, alimentada con ítems de TODOS los ensayos finalizados del estudiante (join `ensayo_items` + `ensayos` + `items`).
- **Una sola consulta para resumen y evolución**: `FinalizadosPorEstudiante` devuelve los ensayos ordenados por `fecha_fin ASC`; el último elemento es el más reciente (`ultimo_puntaje`), evitando una segunda consulta ordenada DESC.

## Fase 5 — Grupos
- **`DesempenoPorEjeEstudiante` se generalizó a `DesempenoPorEje([]string)`**: con un solo ID sirve para el dashboard individual (Fase 4); con varios, para el desempeño agregado de un grupo. Mismo patrón para reutilizar `domain.CalcularDesglosePorEje`.
- **Sin N+1 al listar miembros**: `ResumenPorEstudiantes` calcula total de ensayos y último puntaje de *todos* los miembros en 2 queries agregadas (COUNT GROUP BY + DISTINCT ON), no un loop por estudiante.
- **Código de invitación**: 7 caracteres de un alfabeto de 32 símbolos sin 0/O/1/I/L (evita confusión al dictarlo/leerlo); reintenta ante colisión de unicidad (poco probable).
- **`UnirsePorCodigo` es idempotente**: `ON CONFLICT (grupo_id, estudiante_id) DO NOTHING` — unirse dos veces no falla.
- **RN-06 (aislamiento entre profesores)**: `obtenerPropioGrupo` devuelve 404 si el grupo no es del profesor autenticado (mismo criterio que "ensayo ajeno" en Fase 3: no revela existencia).
- **Rutas con roles mixtos por endpoint** (`/grupos`): en vez de anidar otro sub-grupo de middleware, se usa `chi.Router.With(RequerirRol(...))` por ruta individual, ya que `POST /grupos` (profesor) y `POST /grupos/unirse` (estudiante) conviven bajo el mismo prefijo.

## Fase 6 — Importación de PDF asistida
- **La heurística NUNCA determina la alternativa correcta.** Eso normalmente no está en el PDF del examen (va en una clave/pauta aparte), así que no se intenta adivinar. Los ítems importados quedan sin `es_correcta` marcada, lo que ya bloquea su publicación vía `domain.ValidarAlternativas` — el "requiere revisión humana" (RN-04) queda reforzado por la validación existente, no por una regla nueva.
- **Segmentación por regex de numeración/alternativas** (`internal/pdfimport`), no por ML/heurísticas de layout. Es deliberadamente simple y best-effort: funciona bien con exámenes de una columna y numeración estándar ("1.", "A)"); columnas múltiples, fórmulas o figuras probablemente degradan la calidad de extracción. Está aislada en su propio paquete y testeada con texto plano sintético (sin depender de PDFs reales).
- **`eje` y `dificultad` son obligatorios en la request** (aplicados a todos los ítems del lote) porque las columnas de la BD son `NOT NULL` y no hay forma honesta de inferirlos del texto; el admin los corrige ítem por ítem al revisar.
- **Import no es atómico entre ítems**: cada ítem se crea con su propia transacción (reutiliza `Items.Crear`); si falla a mitad de un lote grande, los ítems ya creados quedan en `borrador` (no se hace rollback de todo el lote). Aceptable para MVP: no hay pérdida de datos, solo una importación parcial que el admin puede completar manualmente o reintentar.
- **Dependencia externa nueva**: `github.com/ledongthuc/pdf` (parser PDF puro Go). No se pudo ejecutar `go get`/`go mod tidy` en este entorno (sin acceso al proxy de módulos de Go), así que **no se tocó `go.mod`** para evitar adivinar un pseudo-version incorrecto — el paso `go get github.com/ledongthuc/pdf@latest` queda documentado en `backend/README.md` como prerrequisito único antes de compilar la Fase 6.

## Fase 7 — Endurecimiento y cierre
- **Drift de contrato corregido**: `openapi.yaml` no reflejaba los campos `eje`/`dificultad` que la Fase 6 sí exige en `POST /examenes/{id}/importacion-pdf`, ni el `acepta_terminos` requerido en el registro. Se actualizó el spec para que vuelva a ser la fuente de verdad real (validado con `openapi-spec-validator`).
- **T&C con historial, no un booleano suelto**: nueva tabla `terminos_aceptados` (usuario_id, version, fecha) en vez de una columna `acepto_terminos` en `usuarios` — permite reconstruir qué versión aceptó cada usuario y cuándo, y soporta versiones futuras del documento sin perder el historial. `Usuarios.Crear` inserta usuario + aceptación en una sola transacción (mismo patrón que Items+Alternativas): si algo falla, no queda un usuario sin aceptación registrada.
- **Un solo campo `acepta_terminos`, sin flujo separado de tutor**: el HU-set del MVP no incluye verificación de identidad de menores; la autorización de padre/madre/tutor para menores queda cubierta por el texto de la propia declaración (T&C sección 4), no por un campo o flujo técnico adicional. Documentado como decisión consciente, no como omisión.
- **Rate limiting sin dependencias nuevas**: limitador de ventana fija en memoria (`internal/http/ratelimit.go`, solo `sync`+`time`+`net`) en vez de `golang.org/x/time/rate` — evita otro `go get` manual no verificable desde este entorno. Aplicado solo a `POST /auth/login` (10/min por IP), el objetivo clásico de fuerza bruta; server single-instance para el MVP, documentado que un despliegue multi-instancia necesitaría un store compartido.
- **CORS y cabeceras de seguridad escritos a mano** (sin `go-chi/cors`), por la misma razón: cero dependencias nuevas no verificables en este entorno.
- **Límite global de body (25MB) como backstop, no como límite operativo**: como `http.MaxBytesReader` anida y prevalece el límite más chico al reutilizarse sobre el mismo `r.Body`, los límites específicos de imágenes (5MB) y PDF (20MB) siguen siendo los efectivos para esas rutas; el global de 25MB solo cierra el hueco que tenían las rutas JSON (auth, ítems, ensayos, grupos), que antes no tenían ningún tope.
- **Avisos de arranque, no fallos duros**: si `JWT_SECRET` o `CORS_ALLOWED_ORIGIN` quedan en su valor por defecto, el servidor loguea una advertencia pero sigue iniciando — prioriza que el entorno de desarrollo funcione sin fricción, dejando la responsabilidad de configurar valores reales antes de producción.

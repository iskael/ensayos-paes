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

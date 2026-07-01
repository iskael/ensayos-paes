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

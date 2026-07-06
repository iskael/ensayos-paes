# CLAUDE.md — Ensayos PAES Matemáticas

Guía para trabajar en este repo con Claude Code.

## Contexto

Plataforma web mobile-first de ensayos PAES de matemáticas (M1/M2). MVP bajo **Spec Driven Development**. La fuente de verdad del contrato es `docs/openapi.yaml`.

## Metodología (SDD)

- El flujo es: historias → spec → OpenAPI → plan → implementación.
- Antes de implementar un endpoint, revisar `docs/openapi.yaml` y `docs/spec_funcional_mvp.md`.
- No introducir endpoints o campos que no estén en el contrato sin actualizar primero el contrato.
- Respetar el orden de fases de `docs/plan.md` (Banco antes que Ensayos).

## Estándares de código

- **Go:** código idiomático, errores envueltos con contexto, sin panics en flujo normal, tests para el dominio (scoring, generación de ensayo, validación de clave).
- **Nombres de archivo fijos** en scripts/utilitarios (no pasarlos por parámetro).
- **No** agregar comentarios explicativos extensos en el código; el código debe ser legible por sí mismo.
- Validación de entrada en el borde (handlers); reglas de negocio en `internal/domain`.
- Errores de API con formato uniforme `{codigo, mensaje}` (ver schema `Error` en el OpenAPI).

## Reglas de negocio que no se pueden romper

- Puntaje normalizado: `round((puntos_obtenidos / puntos_posibles) * 1000)`.
- `peso_snapshot` se fija al generar el ensayo (editar el ítem no altera resultados históricos).
- Ítems participan en ensayos solo si `estado = publicado`.
- Suma de pesos publicados de un examen = 1000.
- RBAC: estudiante ve solo lo suyo; profesor solo sus grupos; admin solo el banco.

## Interacción

- Respuestas concisas, sin preámbulos.
- Ediciones parciales del código (no reescribir archivos completos sin necesidad).
- Ruteo por complejidad: tareas simples → modelo liviano; diseño/refactor complejo → modelo mayor.
- Ante dudas de alcance, preguntar antes de asumir.

## Decisiones y aprendizajes

- Registrar decisiones técnicas y aprendizajes en `LEARNINGS.md`.

## Comandos

```bash
cd backend && go run ./cmd/api        # API (health en :8080/health)
cd backend && go test ./...           # tests
cd backend && go run ./cmd/seed-admin -email=... -password=...   # crear usuario admin (no hay registro público de admin)
cd backend && ./scripts/smoke_test.sh <admin_email> <admin_password>  # smoke test e2e (requiere API corriendo, curl y jq)
cd prototipo-ia && python3 genera_preguntas.py
```

Para la puesta en marcha local paso a paso, ver `GUIA_PRUEBA_LOCAL.md`.

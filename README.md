# Ensayos PAES Matemáticas

Plataforma web (**mobile-first**) para que estudiantes de 4° medio rindan ensayos PAES de matemáticas (M1/M2) con ítems aleatorios, puntaje en escala 1000 y seguimiento de progreso. Incluye administración del banco de preguntas y grupos para profesores.

## Estado

MVP en desarrollo siguiendo **Spec Driven Development (SDD)**. Documentación en `docs/`.

## Stack

- **Backend:** Go (router stdlib/chi), PostgreSQL, migraciones con `golang-migrate`.
- **Contrato:** OpenAPI 3.0.3 (`docs/openapi.yaml`) como fuente de verdad → `oapi-codegen`.
- **Frontend:** React + Vite, mobile-first, KaTeX (fórmulas), recharts (gráficos).
- **Auth:** JWT.

## Estructura

```
docs/         Documentación SDD (historias, spec, openapi, plan, T&C, diseño IA v2)
backend/      API en Go (cmd/api + internal/{domain,http,repo,auth} + migrations)
frontend/     SPA React mobile-first
prototipo-ia/ Prototipo offline de generación de ítems (v2)
```

## Documentación (orden SDD)

1. `docs/historias_usuario.md`
2. `docs/spec_funcional_mvp.md`
3. `docs/openapi.yaml`
4. `docs/plan.md`
5. `docs/diseno_generacion_ia_v2.md` (v2)
6. `docs/terminos_y_condiciones.md` (borrador)

## Desarrollo

Ver `docs/plan.md` para el detalle de fases. Empezar por **Fase 0 (Fundaciones)**.

**Para levantar el backend y probarlo de extremo a extremo, ver [`GUIA_PRUEBA_LOCAL.md`](GUIA_PRUEBA_LOCAL.md).**

```bash
# Backend
cd backend && go run ./cmd/api      # health check en :8080/health

# Prototipo IA (v2)
cd prototipo-ia && python3 genera_preguntas.py
```

# Dashboard del estudiante (estadísticas de progreso)

Fecha: 2026-07-07

## Contexto

El backend ya expone `GET /dashboard/resumen` y `GET /dashboard/evolucion`
(Fase 4 del plan original, construida hace tiempo). El frontend no tiene
ninguna pantalla que los consuma — el menú de usuario (tanda anterior) ya
tiene un link "Mi progreso" para el rol estudiante, pero está marcado
`disponible: false` porque esta pantalla no existía.

Esta tanda construye esa pantalla: un dashboard con las estadísticas de
progreso del estudiante (total de ensayos, último/mejor/promedio de
puntaje, desempeño por eje) y un gráfico de evolución del puntaje en el
tiempo.

## Alcance

- Página nueva en `/dashboard`, activando el link "Mi progreso" ya
  existente en `MENU_POR_ROL.estudiante`.
- Tarjetas de resumen: total de ensayos, último puntaje, mejor puntaje,
  promedio de puntaje.
- Desglose por eje (correctas/total), mismo estilo que ya usa
  `Resultado.jsx`.
- Gráfico de evolución del puntaje (línea, `recharts`, ya instalado — sin
  dependencias nuevas).
- Estado vacío: si el estudiante no rindió ningún ensayo, se muestra un
  mensaje invitándolo a rendir el primero con un link a `/`, en vez de
  tarjetas o gráfico vacíos.

Fuera de alcance: dashboard/reportes para profesor o admin (quedan para
tandas futuras, cuando esas pantallas existan).

## Arquitectura

- **`frontend/src/pages/Dashboard.jsx`** (nuevo): página que carga
  `resumen` y `evolucion` en paralelo (`Promise.all`) dentro de un
  `useEffect`, y renderiza tarjetas + desglose + gráfico, o el estado
  vacío.
- **`frontend/src/api.js`** (modificado): se agregan
  `api.dashboardResumen(token)` → `GET /api/v1/dashboard/resumen` y
  `api.dashboardEvolucion(token)` → `GET /api/v1/dashboard/evolucion`,
  mismo patrón `pedir()` ya existente.
- **`frontend/src/constantes.js`** (modificado): en `MENU_POR_ROL.estudiante`,
  el ítem `"Mi progreso"` pasa de `{ ruta: null, disponible: false }` a
  `{ ruta: '/dashboard', disponible: true }`. No se toca nada de
  profesor/admin.
- **`frontend/src/App.jsx`** (modificado): nueva ruta `/dashboard`,
  envuelta en `<RutaPrivada><LayoutAutenticado><Dashboard /></LayoutAutenticado></RutaPrivada>`,
  igual que las demás rutas privadas.
- Sin dependencias nuevas: `recharts` ya está en `package.json` desde la
  Fase 0 del proyecto.

## Datos y contrato (ya definidos en `docs/openapi.yaml`)

```
DashboardResumen:
  total_ensayos: integer
  ultimo_puntaje: integer | null
  promedio_puntaje: number | null
  mejor_puntaje: integer | null
  desempeno_por_eje: DesgloseEje[]   // { eje, correctas, total, puntos_obtenidos, puntos_posibles }

PuntoEvolucion[]:
  { fecha: string (date-time), puntaje: integer (0-1000) }
```

## Comportamiento

- **Carga**: `useApi().llamar` para ambos requests (maneja 401
  automáticamente, igual que el resto de las páginas). Mientras cargan,
  "Cargando…" (mismo patrón que `Resultado.jsx`/`RendirEnsayo.jsx`).
- **Estado vacío** (`resumen.total_ensayos === 0`): mensaje "Todavía no
  rendiste ningún ensayo" + `<Link to="/">Rendir mi primer ensayo</Link>`,
  sin tarjetas ni gráfico.
- **Con datos**:
  - 4 tarjetas: Total de ensayos, Último puntaje, Mejor puntaje, Promedio
    de puntaje (`Math.round(promedio_puntaje)` para mostrar, ya que
    `promedio_puntaje` es `number` y puede venir con decimales).
  - Desglose por eje: lista `etiquetaEje(d.eje)`: `correctas/total`, mismo
    componente visual que `Resultado.jsx` (no se extrae a un componente
    compartido en esta tanda — está bien duplicado a esta escala, ver
    `LEARNINGS.md` sobre duplicación aceptable entre `Login`/`Registro`).
  - Gráfico de evolución: `recharts`' `LineChart` con `XAxis` (fecha
    formateada `dd/mm`), `YAxis` (dominio fijo `[0, 1000]`), una sola
    `Line` de `puntaje`. Si `evolucion` viene con longitud 0 pero
    `total_ensayos > 0` (caso raro/inconsistente entre ambos endpoints),
    se omite el gráfico sin romper el render — solo tarjetas + desglose.
- **Error de carga**: mensaje genérico "No se pudo cargar el dashboard"
  (mismo patrón que las demás páginas), sin pantalla en blanco.

## Testing

Sin framework de testing automatizado de UI (misma decisión que las
tandas anteriores). Verificación manual con `npm run dev` contra el
backend real: un estudiante sin ensayos (estado vacío), un estudiante con
varios ensayos rendidos (tarjetas + desglose + gráfico con datos reales),
y el link "Mi progreso" del menú navegando correctamente a `/dashboard`.

## Despliegue

Mismo mecanismo que las tandas anteriores: reconstruir la imagen `web`
(`docker compose up -d --build web`) en el CT 118 de Proxmox tras el
merge, y verificar en `http://192.168.0.190/` (y `http://100.93.161.84/`
vía Tailscale).

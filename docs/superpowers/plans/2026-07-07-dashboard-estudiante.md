# Dashboard del estudiante (estadísticas de progreso) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir la pantalla de dashboard del estudiante (`/dashboard`), activando el link "Mi progreso" ya existente en el menú, mostrando el resumen de progreso (total de ensayos, último/mejor/promedio de puntaje, desempeño por eje) y un gráfico de evolución del puntaje.

**Architecture:** Página nueva que consume dos endpoints ya existentes del backend (`/dashboard/resumen`, `/dashboard/evolucion`) vía dos métodos nuevos en el cliente API. Reutiliza `useApi()`, `EJES`/`etiquetaEje` y el patrón de estados (cargando/error/vacío) ya establecido en `Resultado.jsx`.

**Tech Stack:** Mismo stack de las tandas anteriores (React 18, react-router-dom, CSS plano, `recharts` — ya instalado desde Fase 0, sin dependencias nuevas).

## Global Constraints

- Sin dependencias nuevas (`recharts` ya está en `package.json`).
- Sin tests automatizados de UI (misma decisión de las tandas anteriores); verificación manual con `npm run dev` contra el backend ya desplegado en `http://192.168.0.190:8080`.
- Nombres de funciones/variables/componentes en español, siguiendo la convención ya usada (`etiquetaEje`, `useAuth`, `useApi`, etc.).
- No reescribir archivos completos sin necesidad; ediciones parciales.
- Solo se toca `MENU_POR_ROL.estudiante` — profesor y admin no cambian.

---

### Task 1: Cliente API (`api.dashboardResumen`, `api.dashboardEvolucion`)

**Files:**
- Modify: `frontend/src/api.js`

**Interfaces:**
- Produces:
  - `api.dashboardResumen(token)` → `GET /api/v1/dashboard/resumen` → `Promise<{ total_ensayos, ultimo_puntaje, promedio_puntaje, mejor_puntaje, desempeno_por_eje: Array<{eje, correctas, total, puntos_obtenidos, puntos_posibles}> }>`
  - `api.dashboardEvolucion(token)` → `GET /api/v1/dashboard/evolucion` → `Promise<Array<{ fecha, puntaje }>>`
- Consumes: `pedir()` (función interna ya existente en `api.js`, no exportada — no cambia).

- [ ] **Step 1: Agregar los dos métodos al objeto `api` en `frontend/src/api.js`**

Agregar dentro del objeto `export const api = { ... }` ya existente (no reescribir el archivo, solo agregar estas dos líneas junto a las demás entradas del objeto):

```js
  dashboardResumen: (token) => pedir('/api/v1/dashboard/resumen', { token }),
  dashboardEvolucion: (token) => pedir('/api/v1/dashboard/evolucion', { token }),
```

- [ ] **Step 2: Verificar contra el backend real con un script de Node**

Registrar un estudiante nuevo (endpoint público, no requiere credenciales existentes) y confirmar que ambos métodos devuelven la forma esperada:

```bash
cd frontend && node -e '
import("./src/api.js").then(async ({ api }) => {
  const email = `verify-dashboard-task1-${Date.now()}@test.cl`
  const registro = await api.registrar({
    nombre: "Verify Dashboard",
    email,
    password: "ClaveVerify123",
    rol: "estudiante",
    acepta_terminos: true,
  })
  const token = registro.token

  const resumen = await api.dashboardResumen(token)
  console.log("resumen tiene total_ensayos:", typeof resumen.total_ensayos === "number")
  console.log("resumen tiene desempeno_por_eje (array):", Array.isArray(resumen.desempeno_por_eje))
  console.log("estudiante nuevo -> total_ensayos === 0:", resumen.total_ensayos === 0)

  const evolucion = await api.dashboardEvolucion(token)
  console.log("evolucion es array:", Array.isArray(evolucion))
  console.log("estudiante nuevo -> evolucion vacia:", evolucion.length === 0)
})
'
```
Expected: `true` cinco veces. (Nota: si `api.js` usa `import.meta.env`, este script de Node fallará igual que en una tanda anterior — si eso pasa, usar el mismo workaround ya documentado: cargar el módulo vía `vite.createServer(...).ssrLoadModule(...)` en un script temporal, no committeado, en vez de `node -e` directo.)

- [ ] **Step 3: Commit**

```bash
git add frontend/src/api.js
git commit -m "feat(frontend): cliente API para dashboard (resumen y evolucion)"
git push origin main
```

---

### Task 2: Activar "Mi progreso" en `MENU_POR_ROL`

**Files:**
- Modify: `frontend/src/constantes.js`

**Interfaces:**
- Consumes: nada nuevo.
- Produces: `MENU_POR_ROL.estudiante` ahora tiene 2 entradas disponibles: `{ etiqueta: 'Configurar ensayo', ruta: '/', disponible: true }` (sin cambios) y `{ etiqueta: 'Mi progreso', ruta: '/dashboard', disponible: true }` (antes `disponible: false, ruta: null`).

- [ ] **Step 1: Editar `MENU_POR_ROL.estudiante` en `frontend/src/constantes.js`**

Reemplazar únicamente la entrada de "Mi progreso" (no tocar `profesor`/`admin` ni el resto del archivo):

```js
export const MENU_POR_ROL = {
  estudiante: [
    { etiqueta: 'Configurar ensayo', ruta: '/', disponible: true },
    { etiqueta: 'Mi progreso', ruta: '/dashboard', disponible: true },
  ],
  profesor: [{ etiqueta: 'Mis grupos', ruta: null, disponible: false }],
  admin: [{ etiqueta: 'Banco de preguntas', ruta: null, disponible: false }],
}
```

- [ ] **Step 2: Verificar con un script de Node**

```bash
cd frontend && node -e '
import("./src/constantes.js").then(({ MENU_POR_ROL }) => {
  const item = MENU_POR_ROL.estudiante.find((i) => i.etiqueta === "Mi progreso")
  console.log("Mi progreso disponible:", item.disponible === true)
  console.log("Mi progreso ruta correcta:", item.ruta === "/dashboard")
  console.log("profesor sigue sin cambios:", MENU_POR_ROL.profesor[0].disponible === false)
  console.log("admin sigue sin cambios:", MENU_POR_ROL.admin[0].disponible === false)
})
'
```
Expected: `true` cuatro veces.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/constantes.js
git commit -m "feat(frontend): activa el link 'Mi progreso' hacia /dashboard"
git push origin main
```

---

### Task 3: Página `Dashboard` (resumen + gráfico de evolución) y wiring en `App.jsx`

**Files:**
- Create: `frontend/src/pages/Dashboard.jsx`
- Modify: `frontend/src/styles.css` (agregar clases nuevas al final del archivo)
- Modify: `frontend/src/App.jsx` (nueva ruta `/dashboard`)

**Interfaces:**
- Consumes: `api.dashboardResumen`, `api.dashboardEvolucion` (Task 1); `useApi()` (`{ llamar(fn) }`, de una tanda anterior); `EJES` (de `constantes.js`, ya existente); `MENU_POR_ROL.estudiante` con "Mi progreso" activado (Task 2).
- Produces: `<Dashboard />` (componente de página, default export), montado en la ruta `/dashboard`.

- [ ] **Step 1: Escribir `frontend/src/pages/Dashboard.jsx`**

```jsx
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES } from '../constantes.js'

function etiquetaEje(valor) {
  return EJES.find((e) => e.valor === valor)?.etiqueta ?? valor
}

function formatearFecha(fechaIso) {
  const d = new Date(fechaIso)
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`
}

export default function Dashboard() {
  const { llamar } = useApi()
  const [resumen, setResumen] = useState(null)
  const [evolucion, setEvolucion] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    Promise.all([
      llamar((token) => api.dashboardResumen(token)),
      llamar((token) => api.dashboardEvolucion(token)),
    ])
      .then(([r, e]) => {
        if (cancelado) return
        setResumen(r)
        setEvolucion(e)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el dashboard')
      })
    return () => {
      cancelado = true
    }
  }, [llamar])

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!resumen || !evolucion) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  if (resumen.total_ensayos === 0) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <h1>Mi progreso</h1>
          <p>Todavía no rendiste ningún ensayo.</p>
          <Link to="/" className="boton" style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>
            Rendir mi primer ensayo
          </Link>
        </div>
      </div>
    )
  }

  const datosGrafico = evolucion.map((p) => ({ fecha: formatearFecha(p.fecha), puntaje: p.puntaje }))

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Mi progreso</h1>

        <div className="dashboard-tarjetas">
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{resumen.total_ensayos}</span>
            <span className="dashboard-metrica-etiqueta">Ensayos rendidos</span>
          </div>
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{resumen.ultimo_puntaje}</span>
            <span className="dashboard-metrica-etiqueta">Último puntaje</span>
          </div>
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{resumen.mejor_puntaje}</span>
            <span className="dashboard-metrica-etiqueta">Mejor puntaje</span>
          </div>
          <div className="dashboard-metrica">
            <span className="dashboard-metrica-valor">{Math.round(resumen.promedio_puntaje)}</span>
            <span className="dashboard-metrica-etiqueta">Promedio</span>
          </div>
        </div>

        <h2>Desempeño por eje</h2>
        <ul>
          {resumen.desempeno_por_eje.map((d) => (
            <li key={d.eje}>
              {etiquetaEje(d.eje)}: {d.correctas}/{d.total}
            </li>
          ))}
        </ul>

        {datosGrafico.length > 0 && (
          <>
            <h2>Evolución del puntaje</h2>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={datosGrafico}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="fecha" />
                <YAxis domain={[0, 1000]} />
                <Tooltip />
                <Line type="monotone" dataKey="puntaje" stroke="#2f6fed" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Agregar los estilos al final de `frontend/src/styles.css`**

```css
.dashboard-tarjetas {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 16px 0;
}

.dashboard-metrica {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 8px;
  background: var(--color-fondo-suave);
  border-radius: 8px;
}

.dashboard-metrica-valor {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primario);
}

.dashboard-metrica-etiqueta {
  font-size: 12px;
  color: var(--color-texto-suave);
  text-align: center;
  margin-top: 4px;
}
```

- [ ] **Step 3: Agregar la ruta `/dashboard` en `frontend/src/App.jsx`**

Agregar el import:

```jsx
import Dashboard from './pages/Dashboard.jsx'
```

Agregar la nueva ruta (junto a las demás rutas privadas, no reemplaza ninguna existente):

```jsx
<Route
  path="/dashboard"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <Dashboard />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 4: Verificar manualmente con `npm run dev` contra el backend real**

```bash
cd frontend && npm run dev
```

Usar un navegador real (Claude Preview o claude-in-chrome; recordar los quirks ya conocidos de este proyecto: `preview_resize` a mobile antes de interactuar si el viewport arranca en 0x0, y usar `element.click()` vía `preview_eval` como respaldo si `preview_click` no dispara el evento).

**Caso 1 — estado vacío:**
1. Registrar un estudiante nuevo vía `/registro`.
2. Ir a `/dashboard` (directo por URL, o abriendo el drawer y tocando "Mi progreso").
3. Confirmar que se ve "Todavía no rendiste ningún ensayo" y el link "Rendir mi primer ensayo" (sin tarjetas ni gráfico).
4. Tocar el link → debe navegar a `/` (ConfigurarEnsayo).

**Caso 2 — con datos reales:**
5. Con ese mismo estudiante (o uno nuevo), generar un ensayo (`nivel: M1`, cualquier eje con stock, `cantidad: 10`), responder las 10 preguntas, y enviarlo (igual que en las verificaciones de tandas anteriores).
6. Ir a `/dashboard` → confirmar que las 4 tarjetas muestran valores coherentes con el resultado recién obtenido (ej. si el puntaje fue 700/1000, "Último puntaje" y "Mejor puntaje" deben ser 700, "Ensayos rendidos" debe ser 1, "Promedio" debe ser 700).
7. Confirmar que el desglose por eje muestra el eje usado con su etiqueta legible (ej. "Números", no `numeros`).
8. Confirmar que aparece la sección "Evolución del puntaje" con un gráfico — verificar su presencia consultando el DOM por un elemento `svg.recharts-surface` o `.recharts-line` (no depender de un screenshot, que puede no capturar bien el SVG).
9. Repetir el paso de generar+enviar un segundo ensayo con el mismo estudiante, volver a `/dashboard`, y confirmar que ahora "Ensayos rendidos" es 2 y el gráfico tiene 2 puntos.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/Dashboard.jsx frontend/src/styles.css frontend/src/App.jsx
git commit -m "feat(frontend): pagina de dashboard del estudiante (resumen + evolucion)"
git push origin main
```

---

### Task 4: Desplegar en Proxmox

**Files:** ninguno (solo comandos de despliegue).

**Interfaces:** Consumes: todo lo anterior (build de producción del frontend con el dashboard incluido).

- [ ] **Step 1: Redesplegar el frontend en el CT 118 de Proxmox**

```bash
# vía SSH al host 192.168.0.155 -> pct exec 118:
cd /opt/app && git pull && docker compose up -d --build web
```

- [ ] **Step 2: Verificar en el navegador contra el despliegue real**

Abrir `http://192.168.0.190/` (y `http://100.93.161.84/` vía Tailscale), loguear con un estudiante que ya tenga ensayos rendidos, ir a `/dashboard` desde el menú, y confirmar que las tarjetas y el gráfico muestran datos reales igual que en la verificación local (Task 3, Step 4).

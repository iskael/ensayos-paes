# Menú de usuario (datos, navegación por rol, logout) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Agregar una barra superior + drawer de navegación a las 3 rutas privadas del frontend, mostrando los datos del usuario logueado, links de navegación según su rol (los que ya existen y los que aún no, marcados como no disponibles), y un botón para cerrar sesión.

**Architecture:** Un componente nuevo `LayoutAutenticado.jsx` envuelve el contenido de cada ruta privada (separado de `RutaPrivada`, que sigue encargándose solo del guard de auth). Los links por rol se definen como datos (`MENU_POR_ROL` en `constantes.js`), no como código repetido por rol.

**Tech Stack:** Mismo stack de la tanda anterior (React 18, react-router-dom, CSS plano). Sin dependencias nuevas.

## Global Constraints

- Mobile-first, reutilizando las variables CSS ya definidas en `frontend/src/styles.css` (`--color-primario`, `--color-borde`, `--color-fondo`, `--color-fondo-suave`, `--color-texto`, `--color-texto-suave`).
- Sin dependencias nuevas.
- Sin tests automatizados de UI (misma decisión de la tanda anterior); verificación manual con `npm run dev` contra el backend ya desplegado en `http://192.168.0.190:8080`.
- Nombres de funciones/variables/componentes en español, siguiendo la convención ya usada en el resto del frontend (`cerrarSesion`, `useAuth`, `RutaPrivada`, etc.).
- No reescribir archivos completos sin necesidad; ediciones parciales.
- `RutaPrivada.jsx` no cambia — su única responsabilidad sigue siendo el guard de autenticación; el layout visual es un componente separado.

---

### Task 1: Constantes del menú por rol (`MENU_POR_ROL`, `ETIQUETA_ROL`)

**Files:**
- Modify: `frontend/src/constantes.js`

**Interfaces:**
- Produces:
  - `MENU_POR_ROL: { estudiante: Item[], profesor: Item[], admin: Item[] }` donde `Item = { etiqueta: string, ruta: string | null, disponible: boolean }`.
  - `ETIQUETA_ROL: { estudiante: 'Estudiante', profesor: 'Profesor', admin: 'Admin' }`.
- Consumes: nada nuevo (el archivo ya exporta `NIVELES`, `CANTIDADES`, `EJES` de la tanda anterior; esta tarea solo agrega, no modifica lo existente).

- [ ] **Step 1: Agregar las constantes al final de `frontend/src/constantes.js`**

Agregar (sin tocar el contenido existente del archivo):

```js
export const MENU_POR_ROL = {
  estudiante: [
    { etiqueta: 'Configurar ensayo', ruta: '/', disponible: true },
    { etiqueta: 'Mi progreso', ruta: null, disponible: false },
  ],
  profesor: [{ etiqueta: 'Mis grupos', ruta: null, disponible: false }],
  admin: [{ etiqueta: 'Banco de preguntas', ruta: null, disponible: false }],
}

export const ETIQUETA_ROL = {
  estudiante: 'Estudiante',
  profesor: 'Profesor',
  admin: 'Admin',
}
```

- [ ] **Step 2: Verificar con un script de Node**

```bash
cd frontend && node -e '
import("./src/constantes.js").then(({ MENU_POR_ROL, ETIQUETA_ROL }) => {
  console.log("estudiante tiene 2 items:", MENU_POR_ROL.estudiante.length === 2)
  console.log("profesor tiene 1 item no disponible:", MENU_POR_ROL.profesor[0].disponible === false)
  console.log("admin tiene 1 item no disponible:", MENU_POR_ROL.admin[0].disponible === false)
  console.log("etiqueta admin:", ETIQUETA_ROL.admin === "Admin")
})
'
```
Expected: `true` cuatro veces.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/constantes.js
git commit -m "feat(frontend): agrega MENU_POR_ROL y ETIQUETA_ROL"
git push origin main
```

---

### Task 2: Componente `LayoutAutenticado` (barra superior + drawer) y wiring en `App.jsx`

**Files:**
- Create: `frontend/src/components/LayoutAutenticado.jsx`
- Modify: `frontend/src/styles.css` (agregar clases nuevas al final del archivo)
- Modify: `frontend/src/App.jsx` (envolver las 3 rutas privadas)

**Interfaces:**
- Consumes: `useAuth()` → `{ usuario: { nombre, email, rol }, cerrarSesion() }` (de `AuthContext.jsx`, tanda anterior); `MENU_POR_ROL`, `ETIQUETA_ROL` (Task 1).
- Produces: `<LayoutAutenticado>{children}</LayoutAutenticado>` — envuelve cualquier página autenticada agregándole la barra superior y el drawer.

- [ ] **Step 1: Escribir `frontend/src/components/LayoutAutenticado.jsx`**

```jsx
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext.jsx'
import { MENU_POR_ROL, ETIQUETA_ROL } from '../constantes.js'

export default function LayoutAutenticado({ children }) {
  const [abierto, setAbierto] = useState(false)
  const { usuario, cerrarSesion } = useAuth()
  const navigate = useNavigate()

  function alCerrarSesion() {
    setAbierto(false)
    cerrarSesion()
    navigate('/login')
  }

  const items = MENU_POR_ROL[usuario?.rol] ?? []

  return (
    <div className="layout-autenticado">
      <header className="barra-superior">
        <span className="barra-superior-titulo">Ensayos PAES</span>
        <button
          className="boton-hamburguesa"
          type="button"
          aria-label="Abrir menú"
          onClick={() => setAbierto(true)}
        >
          ☰
        </button>
      </header>

      {abierto && (
        <div className="drawer-overlay" onClick={() => setAbierto(false)}>
          <nav className="drawer" onClick={(e) => e.stopPropagation()}>
            <button
              className="drawer-cerrar"
              type="button"
              aria-label="Cerrar menú"
              onClick={() => setAbierto(false)}
            >
              ✕
            </button>

            <div className="drawer-usuario">
              <p className="drawer-usuario-nombre">{usuario?.nombre}</p>
              <p className="drawer-usuario-email">{usuario?.email}</p>
              <span className="badge-rol">{ETIQUETA_ROL[usuario?.rol] ?? usuario?.rol}</span>
            </div>

            <ul className="drawer-links">
              {items.map((item) => (
                <li key={item.etiqueta}>
                  {item.disponible ? (
                    <Link to={item.ruta} onClick={() => setAbierto(false)}>
                      {item.etiqueta}
                    </Link>
                  ) : (
                    <span className="drawer-link-deshabilitado">{item.etiqueta}</span>
                  )}
                </li>
              ))}
            </ul>

            <button className="boton drawer-logout" type="button" onClick={alCerrarSesion}>
              Cerrar sesión
            </button>
          </nav>
        </div>
      )}

      <main>{children}</main>
    </div>
  )
}
```

- [ ] **Step 2: Agregar los estilos al final de `frontend/src/styles.css`**

```css
.layout-autenticado {
  min-height: 100vh;
}

.barra-superior {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 16px;
  background: var(--color-primario);
  color: white;
}

.barra-superior-titulo {
  font-weight: 600;
  font-size: 16px;
}

.boton-hamburguesa {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  min-width: 44px;
  min-height: 44px;
}

.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 20;
  display: flex;
  justify-content: flex-end;
}

.drawer {
  position: relative;
  width: 80%;
  max-width: 320px;
  height: 100%;
  background: var(--color-fondo);
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.drawer-cerrar {
  align-self: flex-end;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  min-width: 44px;
  min-height: 44px;
}

.drawer-usuario {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-borde);
}

.drawer-usuario-nombre {
  font-weight: 600;
  margin: 0 0 4px;
}

.drawer-usuario-email {
  color: var(--color-texto-suave);
  font-size: 14px;
  margin: 0 0 8px;
}

.badge-rol {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--color-fondo-suave);
  color: var(--color-primario);
  font-size: 12px;
  font-weight: 600;
}

.drawer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.drawer-links li {
  margin-bottom: 4px;
}

.drawer-links a {
  display: block;
  padding: 12px 8px;
  color: var(--color-texto);
  text-decoration: none;
  border-radius: 8px;
}

.drawer-links a:hover {
  background: var(--color-fondo-suave);
}

.drawer-link-deshabilitado {
  display: block;
  padding: 12px 8px;
  color: var(--color-texto-suave);
  opacity: 0.5;
}

.drawer-logout {
  margin-top: 16px;
  border-top: 1px solid var(--color-borde);
  padding-top: 16px;
}
```

- [ ] **Step 3: Envolver las 3 rutas privadas en `frontend/src/App.jsx`**

Agregar el import:

```jsx
import LayoutAutenticado from './components/LayoutAutenticado.jsx'
```

Reemplazar el contenido de las 3 rutas privadas (cada `<RutaPrivada><Pagina /></RutaPrivada>` pasa a `<RutaPrivada><LayoutAutenticado><Pagina /></LayoutAutenticado></RutaPrivada>`):

```jsx
<Route
  path="/"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <ConfigurarEnsayo />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
<Route
  path="/ensayos/:id"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <RendirEnsayo />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
<Route
  path="/ensayos/:id/resultado"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <Resultado />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

Las rutas públicas (`/login`, `/registro`) no se tocan — el menú solo aparece en pantallas autenticadas.

- [ ] **Step 4: Verificar manualmente con `npm run dev` contra el backend real**

```bash
cd frontend && npm run dev
```

Con un estudiante ya logueado (o registrar uno nuevo vía `/registro`):

1. Ir a `/` → debe verse la barra superior ("Ensayos PAES" + ☰) arriba de "Configurar ensayo".
2. Tocar ☰ → se abre el drawer con overlay oscuro. Debe mostrar el nombre y email del estudiante, badge "Estudiante", los links "Configurar ensayo" (normal, clickeable) y "Mi progreso" (atenuado/gris), y "Cerrar sesión" al final.
3. Tocar "Mi progreso" (deshabilitado) → no debe pasar nada (no navega, el drawer sigue abierto).
4. Tocar "Configurar ensayo" → navega a `/` (ya estábamos ahí) y el drawer se cierra.
5. Tocar el overlay (fuera del drawer) → el drawer se cierra.
6. Generar un ensayo y verificar que la barra superior y el ☰ siguen presentes en `/ensayos/:id` y, tras enviar, en `/ensayos/:id/resultado`.
7. Abrir el drawer y tocar "Cerrar sesión" → debe limpiar la sesión (verificar `localStorage.getItem('sesion')` es `null`) y navegar a `/login`.

Para probar el rol profesor: registrar un usuario nuevo vía `/registro` con rol "Profesor", loguear, abrir el drawer → debe mostrar badge "Profesor" y el link "Mis grupos" atenuado (sin "Configurar ensayo" ni "Mi progreso").

Para probar el rol admin (no se puede registrar vía `/registro` — el backend solo permite estudiante/profesor por diseño): con cualquier sesión de estudiante ya logueada, abrir devtools → Console y ejecutar:

```js
const s = JSON.parse(localStorage.getItem('sesion'))
s.usuario.rol = 'admin'
localStorage.setItem('sesion', JSON.stringify(s))
location.reload()
```

Esto solo cambia el dato local para ver el render del badge/link de admin ("Banco de preguntas" atenuado) — no es una sesión de admin real (el token JWT real seguiría diciendo el rol original si se intentara llamar a la API), es únicamente para verificar visualmente esta tarea. Tras verificar, cerrar sesión para no dejar ese estado corrupto en el navegador.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/LayoutAutenticado.jsx frontend/src/styles.css frontend/src/App.jsx
git commit -m "feat(frontend): menu de usuario (barra superior + drawer, datos, navegacion por rol, logout)"
git push origin main
```

---

### Task 3: Desplegar en Proxmox

**Files:** ninguno (solo comandos de despliegue).

**Interfaces:** Consumes: todo lo anterior (build de producción del frontend con el menú incluido).

- [ ] **Step 1: Redesplegar el frontend en el CT 118 de Proxmox**

```bash
# vía SSH al host 192.168.0.155 -> pct exec 118:
cd /opt/app && git pull && docker compose up -d --build web
```

- [ ] **Step 2: Verificar en el navegador contra el despliegue real**

Abrir `http://192.168.0.190/`, loguear, confirmar que la barra superior y el drawer aparecen igual que en la verificación local (Task 2, Step 4), y que "Cerrar sesión" funciona.

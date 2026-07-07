# Frontend — flujo estudiante (login, registro, rendir ensayo, resultado) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar el scaffold de `frontend/src/main.jsx` por una interfaz real que permite a un estudiante registrarse, iniciar sesión, configurar y rendir un ensayo, y ver su resultado, consumiendo la API ya desplegada en `http://192.168.0.190:8080`.

**Architecture:** React + Vite existente, con `react-router-dom` como única dependencia nueva para el ruteo por pantalla. Un cliente API delgado (`src/api.js`) sobre `fetch`, un contexto de autenticación (`src/AuthContext.jsx`) que persiste la sesión en `localStorage`, y páginas en `src/pages/` por pantalla. Sin librería de estado global ni de data-fetching (YAGNI para 5 pantallas). Sin framework de testing de UI (decisión del spec); la lógica pura no visual (parseo de respuesta HTTP, persistencia de sesión, detección de fórmulas) se extrae a módulos `.js` verificables con scripts de Node sueltos; los componentes/páginas se verifican manualmente con `npm run dev`.

**Tech Stack:** React 18, Vite 5, react-router-dom, katex + react-katex, CSS plano (sin frameworks de estilos).

## Global Constraints

- Mobile-first: CSS pensado para ~375px de ancho, sin media queries de escritorio en esta tanda (spec, sección "Estilos").
- Única dependencia nueva permitida: `react-router-dom`, `katex`, `react-katex`. No agregar Redux/Zustand/React Query (spec, sección "Arquitectura").
- Sin tests automatizados de UI (spec, sección "Testing"); usar scripts de Node para verificar lógica pura, y `npm run dev` + navegador para páginas/componentes.
- El backend ya está desplegado en el CT 118 de Proxmox: API en `http://192.168.0.190:8080`, frontend (aún el scaffold viejo) en `http://192.168.0.190/`. La base de datos local (Postgres vía Docker) no está disponible en esta máquina de desarrollo (Windows) — toda verificación manual de páginas apunta al backend ya desplegado, nunca a `localhost:8080`.
- Rutas de la API bajo `/api/v1`, excepto `/health` (sin prefijo) — confirmado en `backend/scripts/smoke_test.sh`.
- Nombres de funciones/variables propias en español, siguiendo la convención ya usada en `backend/` (`CalcularDesglosePorEje`, `GenerarAleatorio`, etc.).
- No reescribir archivos completos sin necesidad; ediciones parciales (CLAUDE.md, sección "Interacción").

---

### Task 1: Backend — CORS multi-origen

**Files:**
- Modify: `backend/internal/http/middleware.go:85-103`

**Interfaces:**
- Produces: `CORS(allowedOrigins string) func(http.Handler) http.Handler` — mismo nombre y firma que antes (el parámetro ahora acepta una lista separada por comas, no solo un valor); `router.go:35` (`r.Use(CORS(d.AllowedOrigin))`) no necesita cambios.

- [ ] **Step 1: Reemplazar la función `CORS` para soportar lista de orígenes**

En `backend/internal/http/middleware.go`, reemplazar (líneas 85-103):

```go
// CORS habilita llamadas desde el origen del frontend. allowedOrigins puede
// ser "*" (cualquier origen), un origen específico, o una lista separada por
// comas (ej. "http://localhost:5173,http://192.168.0.190"): el backend
// refleja el origen de la request solo si está en la lista.
func CORS(allowedOrigins string) func(http.Handler) http.Handler {
	esComodin := allowedOrigins == "*"
	var origenes []string
	if !esComodin {
		for _, o := range strings.Split(allowedOrigins, ",") {
			o = strings.TrimSpace(o)
			if o != "" {
				origenes = append(origenes, o)
			}
		}
	}
	permitido := func(origen string) bool {
		for _, o := range origenes {
			if o == origen {
				return true
			}
		}
		return false
	}

	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			origen := r.Header.Get("Origin")
			switch {
			case esComodin:
				w.Header().Set("Access-Control-Allow-Origin", "*")
			case origen != "" && permitido(origen):
				w.Header().Set("Access-Control-Allow-Origin", origen)
				w.Header().Set("Vary", "Origin")
			}
			w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
			w.Header().Set("Access-Control-Allow-Headers", "Authorization, Content-Type")
			if r.Method == http.MethodOptions {
				w.WriteHeader(http.StatusNoContent)
				return
			}
			next.ServeHTTP(w, r)
		})
	}
}
```

- [ ] **Step 2: Verificar que compila y que los tests existentes siguen pasando**

Run:
```bash
cd backend && go build ./... && go vet ./... && go test ./...
```
Expected: sin errores, mismos tests OK que antes (`internal/domain`, `internal/pdfimport`).

- [ ] **Step 3: Commit**

```bash
git add backend/internal/http/middleware.go
git commit -m "feat: CORS soporta lista de origenes separados por coma"
```

- [ ] **Step 4: Redesplegar el backend y habilitar el origen de desarrollo local**

```bash
# En el CT 118 de Proxmox (vía SSH al host 192.168.0.155 -> pct exec 118):
cd /opt/app && git pull
sed -i 's|^CORS_ALLOWED_ORIGIN=.*|CORS_ALLOWED_ORIGIN=http://192.168.0.190,http://localhost:5173|' .env
docker compose up -d --build api
```

- [ ] **Step 5: Verificar CORS con curl (origen permitido vs no permitido)**

```bash
curl -s -D - -o /dev/null http://192.168.0.190:8080/health -H "Origin: http://localhost:5173" | grep -i access-control-allow-origin
curl -s -D - -o /dev/null http://192.168.0.190:8080/health -H "Origin: http://evil.com" | grep -i access-control-allow-origin
```
Expected: la primera imprime `Access-Control-Allow-Origin: http://localhost:5173`; la segunda no imprime nada (el header no se setea).

---

### Task 2: Instalar dependencias del frontend

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/package-lock.json` (generado por npm)

**Interfaces:**
- Produces: paquetes `react-router-dom`, `katex`, `react-katex` disponibles para el resto de las tareas.

- [ ] **Step 1: Instalar**

```bash
cd frontend && npm install react-router-dom katex react-katex
```

- [ ] **Step 2: Verificar que el build sigue funcionando**

```bash
npm run build
```
Expected: `✓ built in ...` sin errores (igual que antes de agregar las dependencias).

- [ ] **Step 3: Commit**

```bash
git add frontend/package.json frontend/package-lock.json
git commit -m "feat(frontend): agrega react-router-dom, katex y react-katex"
```

---

### Task 3: Cliente API (`src/api.js`)

**Files:**
- Create: `frontend/src/api.js`
- Create: `frontend/.env.development` (apunta el dev server al backend ya desplegado, ver Global Constraints)

**Interfaces:**
- Produces:
  - `class ApiError extends Error { status, codigo, mensaje, extra }`
  - `api.registrar(body)` → `POST /api/v1/auth/register`
  - `api.iniciarSesion(body)` → `POST /api/v1/auth/login`
  - `api.crearEnsayo(token, body)` → `POST /api/v1/ensayos`
  - `api.obtenerEnsayo(token, id)` → `GET /api/v1/ensayos/:id`
  - `api.guardarRespuestas(token, id, body)` → `PATCH /api/v1/ensayos/:id/respuestas`
  - `api.enviarEnsayo(token, id)` → `POST /api/v1/ensayos/:id/enviar`
  - `api.obtenerResultado(token, id)` → `GET /api/v1/ensayos/:id/resultado`
  - Todas las funciones de `api.*` devuelven una `Promise` que resuelve al body ya parseado (o `null` para `204`) y rechaza con `ApiError` si `!response.ok`.

- [ ] **Step 1: Crear `frontend/.env.development`**

```
VITE_API_URL=http://192.168.0.190:8080
```

- [ ] **Step 2: Escribir `frontend/src/api.js`**

```js
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080'

export class ApiError extends Error {
  constructor(status, codigo, mensaje, extra) {
    super(mensaje || 'Error de red')
    this.status = status
    this.codigo = codigo
    this.mensaje = mensaje
    this.extra = extra
  }
}

async function pedir(ruta, { metodo = 'GET', body, token } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers.Authorization = `Bearer ${token}`

  let res
  try {
    res = await fetch(`${BASE_URL}${ruta}`, {
      method: metodo,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new ApiError(0, 'ERROR_RED', 'No se pudo conectar con el servidor')
  }

  if (res.status === 204) return null

  const datos = await res.json().catch(() => null)
  if (!res.ok) {
    throw new ApiError(res.status, datos?.codigo, datos?.mensaje, datos)
  }
  return datos
}

export const api = {
  registrar: (body) => pedir('/api/v1/auth/register', { metodo: 'POST', body }),
  iniciarSesion: (body) => pedir('/api/v1/auth/login', { metodo: 'POST', body }),
  crearEnsayo: (token, body) => pedir('/api/v1/ensayos', { metodo: 'POST', body, token }),
  obtenerEnsayo: (token, id) => pedir(`/api/v1/ensayos/${id}`, { token }),
  guardarRespuestas: (token, id, body) =>
    pedir(`/api/v1/ensayos/${id}/respuestas`, { metodo: 'PATCH', body, token }),
  enviarEnsayo: (token, id) => pedir(`/api/v1/ensayos/${id}/enviar`, { metodo: 'POST', token }),
  obtenerResultado: (token, id) => pedir(`/api/v1/ensayos/${id}/resultado`, { token }),
}
```

- [ ] **Step 3: Verificar contra el backend real con un script de Node**

Este proyecto usa `"type": "module"` en `package.json`, así que `node` interpreta `.js` como ESM directamente.

No usar credenciales de admin preexistentes para esto — registrar un usuario de prueba nuevo (endpoint público, no requiere ningún secreto) y usarlo para probar `registrar` y `iniciarSesion` en el mismo script:

```bash
cd frontend && node -e '
import("./src/api.js").then(async ({ api, ApiError }) => {
  const email = `verificacion-task3-${Date.now()}@test.cl`
  const password = "ClaveDePrueba123"

  const registro = await api.registrar({
    nombre: "Verificacion Task3",
    email,
    password,
    rol: "estudiante",
    acepta_terminos: true,
  })
  console.log("registro OK, token presente:", typeof registro.token === "string" && registro.token.length > 0)

  const login = await api.iniciarSesion({ email, password })
  console.log("login OK, token presente:", typeof login.token === "string" && login.token.length > 0)

  try {
    await api.iniciarSesion({ email, password: "clave-incorrecta" })
    console.log("ERROR: deberia haber lanzado ApiError")
  } catch (e) {
    console.log("login invalido -> ApiError:", e instanceof ApiError, "status:", e.status)
  }
})
'
```
Expected:
```
registro OK, token presente: true
login OK, token presente: true
login invalido -> ApiError: true status: 401
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/api.js frontend/.env.development
git commit -m "feat(frontend): cliente API (src/api.js)"
```

---

### Task 4: Persistencia de sesión (`src/sesion.js`)

**Files:**
- Create: `frontend/src/sesion.js`

**Interfaces:**
- Produces:
  - `CLAVE_SESION` (string, `'sesion'`)
  - `leerSesionGuardada(storage = window.localStorage)` → `{ token, usuario } | null`
  - `guardarSesion({ token, usuario }, storage = window.localStorage)` → `void`
  - `borrarSesion(storage = window.localStorage)` → `void`
- Consumes: nada (módulo independiente).

- [ ] **Step 1: Escribir `frontend/src/sesion.js`**

```js
export const CLAVE_SESION = 'sesion'

export function leerSesionGuardada(storage = window.localStorage) {
  try {
    const crudo = storage.getItem(CLAVE_SESION)
    return crudo ? JSON.parse(crudo) : null
  } catch {
    return null
  }
}

export function guardarSesion(sesion, storage = window.localStorage) {
  storage.setItem(CLAVE_SESION, JSON.stringify(sesion))
}

export function borrarSesion(storage = window.localStorage) {
  storage.removeItem(CLAVE_SESION)
}
```

- [ ] **Step 2: Verificar con un script de Node y un storage falso (sin navegador)**

```bash
cd frontend && node -e '
import("./src/sesion.js").then(({ leerSesionGuardada, guardarSesion, borrarSesion }) => {
  const mapa = new Map()
  const storageFalso = {
    getItem: (k) => (mapa.has(k) ? mapa.get(k) : null),
    setItem: (k, v) => mapa.set(k, v),
    removeItem: (k) => mapa.delete(k),
  }

  console.log("vacio al inicio:", leerSesionGuardada(storageFalso) === null)

  guardarSesion({ token: "abc", usuario: { nombre: "Test" } }, storageFalso)
  const leida = leerSesionGuardada(storageFalso)
  console.log("round-trip OK:", leida.token === "abc" && leida.usuario.nombre === "Test")

  borrarSesion(storageFalso)
  console.log("vacio tras borrar:", leerSesionGuardada(storageFalso) === null)

  mapa.set(CLAVE_SESION_INEXISTENTE_OK = "sesion", "{json invalido")
  console.log("null si el JSON esta corrupto:", leerSesionGuardada(storageFalso) === null)
})
'
```
Expected:
```
vacio al inicio: true
round-trip OK: true
vacio tras borrar: true
null si el JSON esta corrupto: true
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/sesion.js
git commit -m "feat(frontend): persistencia de sesion en localStorage (src/sesion.js)"
```

---

### Task 5: Parser de fórmulas (`src/formula.js`)

**Files:**
- Create: `frontend/src/formula.js`

**Interfaces:**
- Produces: `partirTexto(texto: string) => Array<{ tipo: 'texto' | 'inline' | 'bloque', valor: string }>`
- Consumes: nada.

- [ ] **Step 1: Escribir `frontend/src/formula.js`**

```js
const PATRON_FORMULA = /\$\$(.+?)\$\$|\$(.+?)\$/g

export function partirTexto(texto) {
  const partes = []
  if (!texto) return partes

  let ultimoIndice = 0
  let match
  PATRON_FORMULA.lastIndex = 0
  while ((match = PATRON_FORMULA.exec(texto)) !== null) {
    if (match.index > ultimoIndice) {
      partes.push({ tipo: 'texto', valor: texto.slice(ultimoIndice, match.index) })
    }
    if (match[1] !== undefined) {
      partes.push({ tipo: 'bloque', valor: match[1] })
    } else {
      partes.push({ tipo: 'inline', valor: match[2] })
    }
    ultimoIndice = PATRON_FORMULA.lastIndex
  }
  if (ultimoIndice < texto.length) {
    partes.push({ tipo: 'texto', valor: texto.slice(ultimoIndice) })
  }
  return partes
}
```

- [ ] **Step 2: Verificar con un script de Node**

```bash
cd frontend && node -e '
import("./src/formula.js").then(({ partirTexto }) => {
  console.log(JSON.stringify(partirTexto("Sin formulas")) === JSON.stringify([{tipo:"texto",valor:"Sin formulas"}]))
  console.log(JSON.stringify(partirTexto("Resuelve $x^2$ por favor")) === JSON.stringify([
    {tipo:"texto",valor:"Resuelve "},
    {tipo:"inline",valor:"x^2"},
    {tipo:"texto",valor:" por favor"},
  ]))
  console.log(JSON.stringify(partirTexto("$$\\int_0^1 x\\,dx$$")) === JSON.stringify([
    {tipo:"bloque",valor:"\\int_0^1 x\\,dx"},
  ]))
  console.log(JSON.stringify(partirTexto("")) === JSON.stringify([]))
})
'
```
Expected: `true` cuatro veces (una por línea).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/formula.js
git commit -m "feat(frontend): parser de formulas LaTeX (src/formula.js)"
```

---

### Task 6: Componente `Formula`, estilos base y constantes del dominio

**Files:**
- Create: `frontend/src/components/Formula.jsx`
- Create: `frontend/src/styles.css`
- Create: `frontend/src/constantes.js`
- Modify: `frontend/index.html:7` (agregar `<link>` a `styles.css` no aplica — Vite importa CSS desde JS; se importa en `main.jsx` en la Task 7)

**Interfaces:**
- Consumes: `partirTexto` de `src/formula.js` (Task 5).
- Produces:
  - `<Formula texto={string} />` (componente, default export de `Formula.jsx`)
  - `frontend/src/styles.css` (clases usadas por las páginas de tareas siguientes: `.pantalla`, `.tarjeta`, `.boton`, `.boton-secundario`, `.campo`, `.error`, `.alternativa`)
  - `constantes.js`: `NIVELES = ['M1', 'M2']`, `CANTIDADES = [10, 20, 30]`, `EJES = [{ valor: 'numeros', etiqueta: 'Números' }, { valor: 'algebra_funciones', etiqueta: 'Álgebra y funciones' }, { valor: 'geometria', etiqueta: 'Geometría' }, { valor: 'probabilidad_estadistica', etiqueta: 'Probabilidad y estadística' }]`

- [ ] **Step 1: Escribir `frontend/src/components/Formula.jsx`**

```jsx
import { InlineMath, BlockMath } from 'react-katex'
import 'katex/dist/katex.min.css'
import { partirTexto } from '../formula.js'

export default function Formula({ texto }) {
  const partes = partirTexto(texto)
  return (
    <>
      {partes.map((parte, indice) => {
        if (parte.tipo === 'bloque') return <BlockMath key={indice} math={parte.valor} />
        if (parte.tipo === 'inline') return <InlineMath key={indice} math={parte.valor} />
        return <span key={indice}>{parte.valor}</span>
      })}
    </>
  )
}
```

- [ ] **Step 2: Escribir `frontend/src/constantes.js`**

```js
export const NIVELES = ['M1', 'M2']

export const CANTIDADES = [10, 20, 30]

export const EJES = [
  { valor: 'numeros', etiqueta: 'Números' },
  { valor: 'algebra_funciones', etiqueta: 'Álgebra y funciones' },
  { valor: 'geometria', etiqueta: 'Geometría' },
  { valor: 'probabilidad_estadistica', etiqueta: 'Probabilidad y estadística' },
]
```

- [ ] **Step 3: Escribir `frontend/src/styles.css`**

```css
:root {
  --color-primario: #2f6fed;
  --color-primario-oscuro: #1d4fb8;
  --color-texto: #1a1a1a;
  --color-texto-suave: #5a5a5a;
  --color-fondo: #ffffff;
  --color-fondo-suave: #f4f6fb;
  --color-error: #c62828;
  --color-borde: #d8dde6;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--color-texto);
  background: var(--color-fondo-suave);
}

.pantalla {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 16px;
}

.tarjeta {
  width: 100%;
  max-width: 420px;
  background: var(--color-fondo);
  border-radius: 12px;
  padding: 24px 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.campo {
  display: block;
  width: 100%;
  margin-bottom: 16px;
}

.campo label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: var(--color-texto-suave);
}

.campo input[type='text'],
.campo input[type='email'],
.campo input[type='password'],
.campo select {
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;
  border: 1px solid var(--color-borde);
  border-radius: 8px;
  font-size: 16px;
}

.boton {
  width: 100%;
  min-height: 44px;
  border: none;
  border-radius: 8px;
  background: var(--color-primario);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.boton:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.boton:hover:not(:disabled) {
  background: var(--color-primario-oscuro);
}

.boton-secundario {
  width: 100%;
  min-height: 44px;
  border: 1px solid var(--color-primario);
  border-radius: 8px;
  background: transparent;
  color: var(--color-primario);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.boton-secundario:hover:not(:disabled) {
  background: var(--color-fondo-suave);
}

.error {
  color: var(--color-error);
  font-size: 14px;
  margin: 8px 0 16px;
}

.alternativa {
  display: block;
  width: 100%;
  min-height: 44px;
  padding: 12px 14px;
  margin-bottom: 10px;
  border: 1px solid var(--color-borde);
  border-radius: 8px;
  text-align: left;
  background: var(--color-fondo);
  font-size: 15px;
  cursor: pointer;
}

.alternativa.seleccionada {
  border-color: var(--color-primario);
  background: #eaf1ff;
}
```

- [ ] **Step 4: Verificar visualmente el componente `Formula` con un montaje temporal**

Editar temporalmente `frontend/src/main.jsx` (el contenido real de este archivo se reemplaza en la Task 7; este paso es solo para ver `Formula` renderizado antes de que exista una página real que lo use):

```jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import Formula from './components/Formula.jsx'
import './styles.css'

function App() {
  return (
    <div className="pantalla">
      <div className="tarjeta">
        <Formula texto="Resuelve: $x^2 + 2x + 1 = 0$ y luego $$\int_0^1 x\,dx$$" />
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
```

Correr:
```bash
cd frontend && npm run dev
```

Abrir `http://localhost:5173/` en el navegador. Confirmar que se ve el texto "Resuelve:" seguido de la fórmula `x² + 2x + 1 = 0` renderizada con KaTeX (no como texto plano `$x^2...$`), y debajo la integral en bloque. Parar el dev server (Ctrl+C) al terminar de verificar.

**Este `main.jsx` temporal se reemplaza por completo en la Task 7** — no hace falta revertirlo a mano.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/Formula.jsx frontend/src/constantes.js frontend/src/styles.css
git commit -m "feat(frontend): componente Formula (KaTeX), estilos base y constantes del dominio"
```

---

### Task 7: Enrutamiento base (AuthContext, useApi, RutaPrivada, App, main)

**Files:**
- Create: `frontend/src/AuthContext.jsx`
- Create: `frontend/src/useApi.js`
- Create: `frontend/src/components/RutaPrivada.jsx`
- Create: `frontend/src/App.jsx`
- Modify: `frontend/src/main.jsx` (reemplazo completo)

**Interfaces:**
- Consumes: `leerSesionGuardada`, `guardarSesion`, `borrarSesion` de `src/sesion.js` (Task 4); `ApiError` de `src/api.js` (Task 3).
- Produces:
  - `AuthProvider` (componente, envuelve la app)
  - `useAuth()` → `{ token: string|null, usuario: object|null, guardarSesion(token, usuario), cerrarSesion() }`
  - `useApi()` → `{ llamar(fn) }` donde `fn` recibe `token` y devuelve una `Promise`; si `fn` rechaza con `ApiError` de status 401, `llamar` cierra sesión y navega a `/login` antes de re-lanzar el error.
  - `<RutaPrivada>{children}</RutaPrivada>` — redirige a `/login` si no hay `token`.
  - Rutas registradas en `App.jsx`: `/login`, `/registro`, `/` (privada), `/ensayos/:id` (privada), `/ensayos/:id/resultado` (privada). Las páginas reales se agregan en tareas siguientes; por ahora usar placeholders `<div>Login</div>`, etc.

- [ ] **Step 1: Escribir `frontend/src/AuthContext.jsx`**

```jsx
import { createContext, useContext, useState, useCallback } from 'react'
import { leerSesionGuardada, guardarSesion as persistirSesion, borrarSesion } from './sesion.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [sesion, setSesion] = useState(leerSesionGuardada)

  const guardarSesionEnContexto = useCallback((token, usuario) => {
    const nuevaSesion = { token, usuario }
    persistirSesion(nuevaSesion)
    setSesion(nuevaSesion)
  }, [])

  const cerrarSesion = useCallback(() => {
    borrarSesion()
    setSesion(null)
  }, [])

  const valor = {
    token: sesion?.token ?? null,
    usuario: sesion?.usuario ?? null,
    guardarSesion: guardarSesionEnContexto,
    cerrarSesion,
  }

  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const contexto = useContext(AuthContext)
  if (!contexto) throw new Error('useAuth debe usarse dentro de <AuthProvider>')
  return contexto
}
```

- [ ] **Step 2: Escribir `frontend/src/useApi.js`**

```js
import { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
import { ApiError } from './api.js'

export function useApi() {
  const { token, cerrarSesion } = useAuth()
  const navigate = useNavigate()

  const llamar = useCallback(
    async (fn) => {
      try {
        return await fn(token)
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          cerrarSesion()
          navigate('/login')
        }
        throw error
      }
    },
    [token, cerrarSesion, navigate],
  )

  return { llamar }
}
```

- [ ] **Step 3: Escribir `frontend/src/components/RutaPrivada.jsx`**

```jsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '../AuthContext.jsx'

export default function RutaPrivada({ children }) {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return children
}
```

- [ ] **Step 4: Escribir `frontend/src/App.jsx` (con placeholders)**

```jsx
import { Routes, Route } from 'react-router-dom'
import RutaPrivada from './components/RutaPrivada.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<div>Login (placeholder)</div>} />
      <Route path="/registro" element={<div>Registro (placeholder)</div>} />
      <Route
        path="/"
        element={
          <RutaPrivada>
            <div>Configurar ensayo (placeholder)</div>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id"
        element={
          <RutaPrivada>
            <div>Rendir ensayo (placeholder)</div>
          </RutaPrivada>
        }
      />
      <Route
        path="/ensayos/:id/resultado"
        element={
          <RutaPrivada>
            <div>Resultado (placeholder)</div>
          </RutaPrivada>
        }
      />
    </Routes>
  )
}
```

- [ ] **Step 5: Reemplazar `frontend/src/main.jsx` por completo**

```jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './AuthContext.jsx'
import App from './App.jsx'
import './styles.css'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
```

- [ ] **Step 6: Verificar el ruteo y el guard de autenticación manualmente**

```bash
cd frontend && npm run dev
```

En el navegador:
1. Ir a `http://localhost:5173/` → debe redirigir a `/login` (no hay sesión) y mostrar "Login (placeholder)".
2. Ir a `http://localhost:5173/registro` → debe mostrar "Registro (placeholder)" (ruta pública, no redirige).
3. Abrir la consola del navegador y ejecutar `localStorage.setItem('sesion', JSON.stringify({token:'x', usuario:{nombre:'Test'}}))`, luego recargar `http://localhost:5173/` → ahora debe mostrar "Configurar ensayo (placeholder)" (ya hay sesión).
4. Ejecutar `localStorage.removeItem('sesion')` para dejar limpio el estado antes de la siguiente tarea.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/AuthContext.jsx frontend/src/useApi.js frontend/src/components/RutaPrivada.jsx frontend/src/App.jsx frontend/src/main.jsx
git commit -m "feat(frontend): enrutamiento base, AuthContext y guard de rutas privadas"
```

---

### Task 8: Páginas de Registro y Login

**Files:**
- Create: `frontend/src/pages/Registro.jsx`
- Create: `frontend/src/pages/Login.jsx`
- Modify: `frontend/src/App.jsx:8-9` (reemplazar los placeholders de `/registro` y `/login` por las páginas reales)

**Interfaces:**
- Consumes: `api.registrar`, `api.iniciarSesion`, `ApiError` (Task 3); `useAuth` (Task 7).
- Produces: nada nuevo consumido por tareas siguientes (pantallas terminales del flujo de auth).

- [ ] **Step 1: Escribir `frontend/src/pages/Registro.jsx`**

```jsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useAuth } from '../AuthContext.jsx'

export default function Registro() {
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rol, setRol] = useState('estudiante')
  const [aceptaTerminos, setAceptaTerminos] = useState(false)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const { guardarSesion } = useAuth()
  const navigate = useNavigate()

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      const respuesta = await api.registrar({
        nombre,
        email,
        password,
        rol,
        acepta_terminos: aceptaTerminos,
      })
      guardarSesion(respuesta.token, respuesta.usuario)
      navigate('/')
    } catch (e) {
      setError(e instanceof ApiError ? e.mensaje || 'No se pudo registrar' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Crear cuenta</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="nombre">Nombre</label>
            <input id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="password">Contraseña (mínimo 8 caracteres)</label>
            <input
              id="password"
              type="password"
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="rol">Soy</label>
            <select id="rol" value={rol} onChange={(e) => setRol(e.target.value)}>
              <option value="estudiante">Estudiante</option>
              <option value="profesor">Profesor</option>
            </select>
          </div>
          <div className="campo">
            <label>
              <input
                type="checkbox"
                checked={aceptaTerminos}
                onChange={(e) => setAceptaTerminos(e.target.checked)}
              />{' '}
              Acepto los Términos y Condiciones
            </label>
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Creando cuenta…' : 'Crear cuenta'}
          </button>
        </form>
        <p>
          ¿Ya tenés cuenta? <Link to="/login">Iniciar sesión</Link>
        </p>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Escribir `frontend/src/pages/Login.jsx`**

```jsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useAuth } from '../AuthContext.jsx'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const { guardarSesion } = useAuth()
  const navigate = useNavigate()

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      const respuesta = await api.iniciarSesion({ email, password })
      guardarSesion(respuesta.token, respuesta.usuario)
      navigate('/')
    } catch (e) {
      setError(e instanceof ApiError && e.status === 401 ? 'Email o contraseña incorrectos' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Iniciar sesión</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="campo">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Ingresando…' : 'Ingresar'}
          </button>
        </form>
        <p>
          ¿No tenés cuenta? <Link to="/registro">Crear cuenta</Link>
        </p>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Conectar las páginas reales en `App.jsx`**

En `frontend/src/App.jsx`, agregar los imports:

```jsx
import Login from './pages/Login.jsx'
import Registro from './pages/Registro.jsx'
```

Y reemplazar las dos rutas placeholder:

```jsx
<Route path="/login" element={<Login />} />
<Route path="/registro" element={<Registro />} />
```

- [ ] **Step 4: Verificar manualmente contra el backend real**

```bash
cd frontend && npm run dev
```

En el navegador (`http://localhost:5173/`):
1. Ir a `/registro`, completar con un email nuevo (ej. `estudiante-manual-1@test.cl`), password de 8+ caracteres, rol "Estudiante", **sin marcar** el checkbox de Términos, enviar → debe mostrar el mensaje de error de la API (422) y no navegar.
2. Marcar el checkbox y volver a enviar → debe crear la cuenta, guardar la sesión, y navegar a `/` (mostrará el placeholder "Configurar ensayo").
3. Verificar en devtools → Application → Local Storage que existe la clave `sesion` con el token.
4. Recargar la página en `/` → debe seguir mostrando el placeholder (no redirige a `/login`, la sesión persiste).
5. Borrar `localStorage` manualmente, ir a `/login`, ingresar con el mismo email/password del estudiante creado en el paso 2 (no hace falta ninguna cuenta preexistente ni contraseña de admin) → debe loguear y navegar a `/`.
6. Ir a `/login` de nuevo (sesión activa) e intentar con ese mismo email pero contraseña incorrecta → debe mostrar "Email o contraseña incorrectos".

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/Registro.jsx frontend/src/pages/Login.jsx frontend/src/App.jsx
git commit -m "feat(frontend): paginas de Registro y Login"
```

---

### Task 9: Página Configurar Ensayo

**Files:**
- Create: `frontend/src/pages/ConfigurarEnsayo.jsx`
- Modify: `frontend/src/App.jsx` (reemplazar el placeholder de `/`)

**Interfaces:**
- Consumes: `NIVELES`, `CANTIDADES`, `EJES` (Task 6); `api.crearEnsayo`, `ApiError` (Task 3); `useApi` (Task 7).
- Produces: navega a `/ensayos/:id` (consumido por Task 10).

- [ ] **Step 1: Escribir `frontend/src/pages/ConfigurarEnsayo.jsx`**

```jsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { NIVELES, CANTIDADES, EJES } from '../constantes.js'

export default function ConfigurarEnsayo() {
  const [nivel, setNivel] = useState(NIVELES[0])
  const [ejesElegidos, setEjesElegidos] = useState([])
  const [cantidad, setCantidad] = useState(CANTIDADES[0])
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const { llamar } = useApi()
  const navigate = useNavigate()

  function alternarEje(valor) {
    setEjesElegidos((actuales) =>
      actuales.includes(valor) ? actuales.filter((e) => e !== valor) : [...actuales, valor],
    )
  }

  async function alEnviar(evento) {
    evento.preventDefault()
    setError(null)
    if (ejesElegidos.length === 0) {
      setError('Elegí al menos un eje')
      return
    }
    setEnviando(true)
    try {
      const ensayo = await llamar((token) =>
        api.crearEnsayo(token, { nivel, ejes: ejesElegidos, cantidad }),
      )
      navigate(`/ensayos/${ensayo.id}`)
    } catch (e) {
      if (e instanceof ApiError && e.codigo === 'STOCK_INSUFICIENTE') {
        setError(`No hay suficientes preguntas disponibles (máximo ${e.extra?.max_disponible ?? 0}). Elegí menos cantidad o más ejes.`)
      } else if (e instanceof ApiError) {
        setError(e.mensaje || 'No se pudo generar el ensayo')
      } else {
        setError('No se pudo conectar con el servidor')
      }
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Configurar ensayo</h1>
        <form onSubmit={alEnviar}>
          <div className="campo">
            <label htmlFor="nivel">Nivel</label>
            <select id="nivel" value={nivel} onChange={(e) => setNivel(e.target.value)}>
              {NIVELES.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label>Ejes</label>
            {EJES.map((eje) => (
              <label key={eje.valor} style={{ display: 'block', marginBottom: 6 }}>
                <input
                  type="checkbox"
                  checked={ejesElegidos.includes(eje.valor)}
                  onChange={() => alternarEje(eje.valor)}
                />{' '}
                {eje.etiqueta}
              </label>
            ))}
          </div>
          <div className="campo">
            <label htmlFor="cantidad">Cantidad de preguntas</label>
            <select id="cantidad" value={cantidad} onChange={(e) => setCantidad(Number(e.target.value))}>
              {CANTIDADES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Generando…' : 'Comenzar ensayo'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Conectar en `App.jsx`**

Agregar el import:

```jsx
import ConfigurarEnsayo from './pages/ConfigurarEnsayo.jsx'
```

Reemplazar la ruta `/`:

```jsx
<Route
  path="/"
  element={
    <RutaPrivada>
      <ConfigurarEnsayo />
    </RutaPrivada>
  }
/>
```

- [ ] **Step 3: Verificar manualmente contra el backend real**

```bash
cd frontend && npm run dev
```

**Nota:** el usuario admin no tiene rol estudiante, así que la API va a devolver 403 al intentar `POST /ensayos` si se prueba logueado como admin. Registrar un estudiante nuevo desde `/registro` para esta prueba y usar ese usuario (no hace falta el admin para verificar esta tarea).

1. Login como estudiante, ir a `/`, elegir nivel M1, marcar el eje "Números", cantidad 10, enviar → debe navegar a `/ensayos/<id>` (mostrará el placeholder "Rendir ensayo").
2. Volver a `/`, no marcar ningún eje, enviar → debe mostrar "Elegí al menos un eje" sin llamar a la API (verificar en la pestaña Network que no sale ningún `POST /ensayos`).
3. Para forzar `STOCK_INSUFICIENTE`: elegir un eje con pocos ítems publicados y cantidad 30 (si en este momento todos los ejes tienen suficiente stock del smoke test, se puede omitir esta verificación y dejarla anotada como pendiente de probar cuando haya menos stock disponible).

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/ConfigurarEnsayo.jsx frontend/src/App.jsx
git commit -m "feat(frontend): pagina para configurar y generar un ensayo"
```

---

### Task 10: Página Rendir Ensayo (pregunta a pregunta, autoguardado)

**Files:**
- Create: `frontend/src/pages/RendirEnsayo.jsx`
- Modify: `frontend/src/App.jsx` (reemplazar el placeholder de `/ensayos/:id`)

**Interfaces:**
- Consumes: `api.obtenerEnsayo`, `api.guardarRespuestas`, `api.enviarEnsayo`, `ApiError` (Task 3); `useApi` (Task 7); `<Formula>` (Task 6).
- Produces: navega a `/ensayos/:id/resultado` (consumido por Task 11).

- [ ] **Step 1: Escribir `frontend/src/pages/RendirEnsayo.jsx`**

```jsx
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import Formula from '../components/Formula.jsx'

export default function RendirEnsayo() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { llamar } = useApi()

  const [preguntas, setPreguntas] = useState(null)
  const [indice, setIndice] = useState(0)
  const [respuestas, setRespuestas] = useState({})
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.obtenerEnsayo(token, id))
      .then((ensayo) => {
        if (cancelado) return
        setPreguntas(ensayo.preguntas)
        const iniciales = {}
        for (const p of ensayo.preguntas) {
          if (p.respuesta_seleccionada) iniciales[p.ensayo_item_id] = p.respuesta_seleccionada
        }
        setRespuestas(iniciales)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el ensayo')
      })
    return () => {
      cancelado = true
    }
  }, [id, llamar])

  const guardarRespuesta = useCallback(
    async (ensayoItemId, etiqueta) => {
      setRespuestas((actuales) => ({ ...actuales, [ensayoItemId]: etiqueta }))
      try {
        await llamar((token) =>
          api.guardarRespuestas(token, id, {
            respuestas: [{ ensayo_item_id: ensayoItemId, respuesta_seleccionada: etiqueta }],
          }),
        )
      } catch {
        setError('No se pudo guardar la respuesta, revisá tu conexión')
      }
    },
    [id, llamar],
  )

  async function alEnviarEnsayo() {
    if (!window.confirm('¿Enviar el ensayo? No vas a poder cambiar las respuestas después.')) return
    setEnviando(true)
    setError(null)
    try {
      await llamar((token) => api.enviarEnsayo(token, id))
      navigate(`/ensayos/${id}/resultado`)
    } catch (e) {
      setError(e instanceof ApiError && e.status === 409 ? 'Este ensayo ya fue enviado' : 'No se pudo enviar el ensayo')
      setEnviando(false)
    }
  }

  if (error && !preguntas) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!preguntas) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  const pregunta = preguntas[indice]
  const esUltima = indice === preguntas.length - 1

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <p>
          Pregunta {indice + 1} de {preguntas.length}
        </p>
        <Formula texto={pregunta.enunciado} />
        <div style={{ marginTop: 16 }}>
          {pregunta.alternativas.map((alt) => (
            <button
              key={alt.etiqueta}
              type="button"
              className={
                'alternativa' + (respuestas[pregunta.ensayo_item_id] === alt.etiqueta ? ' seleccionada' : '')
              }
              onClick={() => guardarRespuesta(pregunta.ensayo_item_id, alt.etiqueta)}
            >
              {alt.etiqueta}) <Formula texto={alt.texto} />
            </button>
          ))}
        </div>
        {error && <p className="error">{error}</p>}
        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <button
            className="boton-secundario"
            type="button"
            disabled={indice === 0}
            onClick={() => setIndice((i) => i - 1)}
          >
            Anterior
          </button>
          {esUltima ? (
            <button className="boton" type="button" disabled={enviando} onClick={alEnviarEnsayo}>
              {enviando ? 'Enviando…' : 'Enviar ensayo'}
            </button>
          ) : (
            <button className="boton" type="button" onClick={() => setIndice((i) => i + 1)}>
              Siguiente
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Conectar en `App.jsx`**

Agregar el import:

```jsx
import RendirEnsayo from './pages/RendirEnsayo.jsx'
```

Reemplazar la ruta `/ensayos/:id`:

```jsx
<Route
  path="/ensayos/:id"
  element={
    <RutaPrivada>
      <RendirEnsayo />
    </RutaPrivada>
  }
/>
```

- [ ] **Step 3: Verificar manualmente contra el backend real**

```bash
cd frontend && npm run dev
```

Con el estudiante de la Task 9 (o uno nuevo) y un ensayo recién generado:

1. Confirmar que se ve "Pregunta 1 de 10" (o la cantidad elegida) y el enunciado.
2. Elegir una alternativa → abrir la pestaña Network y confirmar que sale un `PATCH /api/v1/ensayos/<id>/respuestas` con status 204.
3. Ir a "Siguiente" varias veces, volver con "Anterior" → la alternativa marcada antes debe seguir apareciendo seleccionada (viene de `respuesta_seleccionada` en `GET /ensayos/:id` la próxima vez que se cargue, o del estado local `respuestas` mientras se navega sin recargar).
4. Responder todas las preguntas, en la última pulsar "Enviar ensayo" → debe aparecer el diálogo de confirmación del navegador; confirmar → debe navegar a `/ensayos/<id>/resultado` (placeholder por ahora).
5. Volver atrás en el navegador y tocar "Enviar ensayo" de nuevo en el mismo ensayo (ya finalizado) → debe mostrar "Este ensayo ya fue enviado" (409).

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/RendirEnsayo.jsx frontend/src/App.jsx
git commit -m "feat(frontend): pagina para rendir el ensayo (pregunta a pregunta, autoguardado)"
```

---

### Task 11: Página Resultado

**Files:**
- Create: `frontend/src/pages/Resultado.jsx`
- Modify: `frontend/src/App.jsx` (reemplazar el placeholder de `/ensayos/:id/resultado`)

**Interfaces:**
- Consumes: `api.obtenerResultado`, `ApiError` (Task 3); `useApi` (Task 7); `<Formula>` (Task 6); `EJES` (Task 6, para traducir el nombre del eje en el desglose).

- [ ] **Step 1: Escribir `frontend/src/pages/Resultado.jsx`**

```jsx
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES } from '../constantes.js'
import Formula from '../components/Formula.jsx'

function etiquetaEje(valor) {
  return EJES.find((e) => e.valor === valor)?.etiqueta ?? valor
}

export default function Resultado() {
  const { id } = useParams()
  const { llamar } = useApi()
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.obtenerResultado(token, id))
      .then((r) => {
        if (!cancelado) setResultado(r)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el resultado')
      })
    return () => {
      cancelado = true
    }
  }, [id, llamar])

  if (error) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!resultado) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>Puntaje: {resultado.puntaje} / 1000</h1>
        <p>
          {resultado.correctas} de {resultado.total} correctas
        </p>

        <h2>Desglose por eje</h2>
        <ul>
          {resultado.desglose_por_eje.map((d) => (
            <li key={d.eje}>
              {etiquetaEje(d.eje)}: {d.correctas}/{d.total}
            </li>
          ))}
        </ul>

        <h2>Revisión</h2>
        {resultado.revision.map((item) => (
          <div
            key={item.orden}
            style={{ marginBottom: 16, paddingBottom: 16, borderBottom: '1px solid var(--color-borde)' }}
          >
            <p>
              {item.orden}. <Formula texto={item.enunciado} />
            </p>
            <p>
              Tu respuesta: {item.respuesta_seleccionada ?? '(sin responder)'} — Correcta:{' '}
              {item.respuesta_correcta} —{' '}
              <strong style={{ color: item.es_correcta ? 'green' : 'var(--color-error)' }}>
                {item.es_correcta ? 'Correcta' : 'Incorrecta'}
              </strong>
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Conectar en `App.jsx`**

Agregar el import:

```jsx
import Resultado from './pages/Resultado.jsx'
```

Reemplazar la ruta `/ensayos/:id/resultado`:

```jsx
<Route
  path="/ensayos/:id/resultado"
  element={
    <RutaPrivada>
      <Resultado />
    </RutaPrivada>
  }
/>
```

- [ ] **Step 3: Verificar manualmente contra el backend real**

```bash
cd frontend && npm run dev
```

Usando un ensayo ya enviado (de la Task 10, o generando y enviando uno nuevo):

1. Ir a `/ensayos/<id>/resultado` → debe mostrar el puntaje, el desglose por eje con las etiquetas legibles ("Números", no `numeros`), y la revisión de cada pregunta con la respuesta correcta marcada.
2. Confirmar que las fórmulas (si el ítem tuviera LaTeX) se ven renderizadas, no como texto `$...$` crudo.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/Resultado.jsx frontend/src/App.jsx
git commit -m "feat(frontend): pagina de resultado con desglose por eje y revision"
```

---

### Task 12: Desplegar el frontend en Proxmox

**Files:**
- Modify: `frontend/Dockerfile`
- Modify: `docker-compose.yml` (servicio `web`)

**Interfaces:**
- Consumes: todo lo anterior (build de producción del frontend completo).

- [ ] **Step 1: Modificar `frontend/Dockerfile` para aceptar `VITE_API_URL` como build arg**

Reemplazar el stage de build:

```dockerfile
FROM node:20-alpine AS build
WORKDIR /src
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /src/dist /usr/share/nginx/html
EXPOSE 80
```

- [ ] **Step 2: Modificar el servicio `web` en `docker-compose.yml`**

En la raíz del repo, dentro de `services.web`, agregar `build.args`:

```yaml
  web:
    build:
      context: ./frontend
      args:
        VITE_API_URL: ${VITE_API_URL:-http://192.168.0.190:8080}
    depends_on:
      - api
    ports:
      - "80:80"
    restart: unless-stopped
```

- [ ] **Step 3: Verificar el build localmente (sin necesidad de Docker corriendo, solo sintaxis)**

```bash
cd "C:/Users/isko0/paes/ensayos-paes" && JWT_SECRET=test docker compose config
```
Expected: el servicio `web` en la salida muestra `args: VITE_API_URL: http://192.168.0.190:8080` (o el valor de `.env` si existe).

- [ ] **Step 4: Commit**

```bash
git add frontend/Dockerfile docker-compose.yml
git commit -m "feat: pasa VITE_API_URL como build arg de la imagen web"
git push origin main
```

- [ ] **Step 5: Redesplegar en el CT 118 de Proxmox**

```bash
# vía SSH al host 192.168.0.155 -> pct exec 118:
cd /opt/app && git pull && docker compose up -d --build web
```

- [ ] **Step 6: Verificar en el navegador contra el despliegue real**

Abrir `http://192.168.0.190/` (no `localhost`) y repetir el recorrido completo: registro → configurar ensayo → rendir → resultado, usando un estudiante nuevo creado ahí mismo. Confirmar que no hay errores de CORS en la consola del navegador (la Task 1 ya agregó `http://192.168.0.190` a `CORS_ALLOWED_ORIGIN`, así que debería funcionar sin cambios adicionales).

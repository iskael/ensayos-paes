# Banco de preguntas (admin) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir la sección "Banco de preguntas" para el rol admin: CRUD de exámenes fuente, CRUD de ítems con alternativas, clave de pesos, publicar/ocultar, subida de imágenes, e importación asistida de PDF — activando el link ya existente en el menú y redirigiendo `/` según rol.

**Architecture:** Páginas nuevas y chicas (una por responsabilidad) que consumen endpoints ya existentes y completos del backend (`/examenes`, `/items`, `/imagenes`), todos protegidos con `RequerirRol(RolAdmin)`. Reutiliza `useApi()`, `useAuth()`, `<Formula>` y el patrón de estados (cargando/error/vacío) ya establecido en el resto del frontend.

**Tech Stack:** Mismo stack de las tandas anteriores (React 18, react-router-dom v7, CSS plano). Sin dependencias nuevas.

## Global Constraints

- Sin dependencias nuevas.
- Sin tests automatizados de UI (misma decisión de las tandas anteriores); verificación manual con `npm run dev` (usa `frontend/.env.development` → `VITE_API_URL=http://192.168.0.190:8080`, el backend ya desplegado) y, cuando aplica, scripts de Node que llaman a `api.js` directamente contra ese mismo backend.
- Nombres de funciones/variables/componentes en español, siguiendo la convención ya usada (`etiquetaEje`, `useAuth`, `useApi`, `actualizarCampo`, etc.).
- No reescribir archivos completos sin necesidad; ediciones parciales (agregar imports/rutas/métodos junto a lo existente).
- El guard de rol (admin) vive en el backend (`RequerirRol(domain.RolAdmin)` en `backend/internal/http/router.go:65-93`) — el frontend NO duplica esa validación; solo controla navegación/redirección.
- RN-03 (`backend/internal/domain/clave.go:4`): la suma de los pesos de una clave debe ser exactamente 1000.
- RN-04 (`backend/internal/domain/item.go:33`, `banco_handler.go:380-406`): un ítem solo se puede publicar si tiene `peso > 0` y exactamente 4 alternativas con etiquetas A-D únicas y exactamente una `es_correcta`.
- Límites de archivo ya impuestos por el backend: `POST /imagenes` acepta solo `.png/.jpg/.jpeg/.webp`, máx. 5MB (`backend/internal/storage/imagenes.go:25`); `POST /examenes/:id/importacion-pdf` máx. 20MB (`banco_handler.go:440`).
- Credenciales de admin: usar la cuenta ya existente en el entorno desplegado. NUNCA escribir el password real en el plan, en código, ni en ningún archivo que se vaya a commitear — para scripts de verificación por Node, leerlas de las variables de entorno `ADMIN_EMAIL`/`ADMIN_PASSWORD` (deben estar ya exportadas en la sesión antes de correr el script); para verificación manual en el navegador, escribirlas directamente en el formulario de login sin guardarlas en ningún archivo.
- `pedir()` en `api.js` usa `import.meta.env.VITE_API_URL`, que no existe fuera de Vite — un script `node -e` que haga `import("./src/api.js")` puede fallar por eso. Si pasa, usar el mismo workaround ya documentado en tandas anteriores: cargar el módulo vía `vite.createServer(...).ssrLoadModule(...)` en un script temporal no committeado, en vez de `node -e` directo.

---

### Task 1: Cliente API — soporte FormData en `pedir()` y métodos del Banco

**Files:**
- Modify: `frontend/src/api.js`

**Interfaces:**
- Consumes: `BASE_URL`, `ApiError` (ya existentes, sin cambios).
- Produces (todos siguen la firma `(token, ...) => Promise<...>`, mismo patrón que los métodos ya existentes):
  - `api.crearExamen(token, body)`, `api.listarExamenes(token, {limit, offset} = {})`, `api.obtenerExamen(token, id)`, `api.actualizarExamen(token, id, body)`, `api.eliminarExamen(token, id)`
  - `api.obtenerClave(token, examenId)`, `api.definirClave(token, examenId, pesos)` (donde `pesos` es `Array<{item_id, peso}>`)
  - `api.importarPdf(token, examenId, formData)` (`formData` es una instancia de `FormData` ya armada por quien llama)
  - `api.crearItem(token, body)`, `api.listarItems(token, filtros = {})` (donde `filtros` puede tener `nivel, eje, dificultad, estado, examenId, limit, offset`), `api.obtenerItem(token, id)`, `api.actualizarItem(token, id, body)`, `api.eliminarItem(token, id)`
  - `api.publicarItem(token, id)`, `api.ocultarItem(token, id)`
  - `api.subirImagen(token, formData)` → `Promise<{ url: string }>`

- [ ] **Step 1: Agregar soporte de `FormData` en `pedir()`**

Reemplazar la función `pedir` completa en `frontend/src/api.js` (líneas 18-40) por:

```js
async function pedir(ruta, { metodo = 'GET', body, token } = {}) {
  const esFormData = typeof FormData !== 'undefined' && body instanceof FormData
  const headers = {}
  if (!esFormData) headers['Content-Type'] = 'application/json'
  if (token) headers.Authorization = `Bearer ${token}`

  let res
  try {
    res = await fetch(`${BASE_URL}${ruta}`, {
      method: metodo,
      headers,
      body: esFormData ? body : body !== undefined ? JSON.stringify(body) : undefined,
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
```

- [ ] **Step 2: Agregar los métodos nuevos al objeto `api`**

Agregar dentro del objeto `export const api = { ... }` ya existente, junto a las demás entradas (no reescribir el archivo):

```js
  crearExamen: (token, body) => pedir('/api/v1/examenes', { metodo: 'POST', body, token }),
  listarExamenes: (token, { limit, offset } = {}) => {
    const params = new URLSearchParams()
    if (limit !== undefined) params.set('limit', limit)
    if (offset !== undefined) params.set('offset', offset)
    const qs = params.toString()
    return pedir(`/api/v1/examenes${qs ? `?${qs}` : ''}`, { token })
  },
  obtenerExamen: (token, id) => pedir(`/api/v1/examenes/${id}`, { token }),
  actualizarExamen: (token, id, body) => pedir(`/api/v1/examenes/${id}`, { metodo: 'PUT', body, token }),
  eliminarExamen: (token, id) => pedir(`/api/v1/examenes/${id}`, { metodo: 'DELETE', token }),
  obtenerClave: (token, examenId) => pedir(`/api/v1/examenes/${examenId}/clave`, { token }),
  definirClave: (token, examenId, pesos) =>
    pedir(`/api/v1/examenes/${examenId}/clave`, { metodo: 'PUT', body: { pesos }, token }),
  importarPdf: (token, examenId, formData) =>
    pedir(`/api/v1/examenes/${examenId}/importacion-pdf`, { metodo: 'POST', body: formData, token }),
  crearItem: (token, body) => pedir('/api/v1/items', { metodo: 'POST', body, token }),
  listarItems: (token, filtros = {}) => {
    const params = new URLSearchParams()
    for (const [clave, valor] of Object.entries(filtros)) {
      if (valor !== undefined && valor !== null && valor !== '') params.set(clave, valor)
    }
    const qs = params.toString()
    return pedir(`/api/v1/items${qs ? `?${qs}` : ''}`, { token })
  },
  obtenerItem: (token, id) => pedir(`/api/v1/items/${id}`, { token }),
  actualizarItem: (token, id, body) => pedir(`/api/v1/items/${id}`, { metodo: 'PUT', body, token }),
  eliminarItem: (token, id) => pedir(`/api/v1/items/${id}`, { metodo: 'DELETE', token }),
  publicarItem: (token, id) => pedir(`/api/v1/items/${id}/publicar`, { metodo: 'POST', token }),
  ocultarItem: (token, id) => pedir(`/api/v1/items/${id}/ocultar`, { metodo: 'POST', token }),
  subirImagen: (token, formData) => pedir('/api/v1/imagenes', { metodo: 'POST', body: formData, token }),
```

- [ ] **Step 3: Verificar contra el backend real con un script de Node**

Antes de correr esto, exportar en la sesión de shell (sin escribirlas en ningún archivo): `export ADMIN_EMAIL=...` y `export ADMIN_PASSWORD=...` con las credenciales de la cuenta admin ya existente en `http://192.168.0.190:8080`.

```bash
cd frontend && node -e '
import("./src/api.js").then(async ({ api }) => {
  const email = process.env.ADMIN_EMAIL
  const password = process.env.ADMIN_PASSWORD
  if (!email || !password) throw new Error("Definir ADMIN_EMAIL y ADMIN_PASSWORD en el entorno antes de correr esto")
  const { token } = await api.iniciarSesion({ email, password })

  const examen = await api.crearExamen(token, {
    nombre: "Verificacion Task1",
    anio_admision: 2026,
    tipo: "PAES_Regular",
    nivel: "M1",
  })
  console.log("examen creado con id:", typeof examen.id === "string")

  const lista = await api.listarExamenes(token)
  console.log("listarExamenes es array:", Array.isArray(lista))

  const item = await api.crearItem(token, {
    enunciado: "Item de verificacion (borrar)",
    eje: "numeros",
    nivel: "M1",
    dificultad: "baja",
    alternativas: [
      { etiqueta: "A", texto: "1", es_correcta: true },
      { etiqueta: "B", texto: "2", es_correcta: false },
      { etiqueta: "C", texto: "3", es_correcta: false },
      { etiqueta: "D", texto: "4", es_correcta: false },
    ],
  })
  console.log("item creado con estado borrador:", item.estado === "borrador")

  const clave = await api.definirClave(token, examen.id, [{ item_id: item.id, peso: 1000 }])
  console.log("clave suma_pesos 1000:", clave.suma_pesos === 1000)

  const publicado = await api.publicarItem(token, item.id)
  console.log("item publicado:", publicado.estado === "publicado")

  const oculto = await api.ocultarItem(token, item.id)
  console.log("item oculto:", oculto.estado === "oculto")

  const pngBase64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
  const archivo = new Blob([Buffer.from(pngBase64, "base64")], { type: "image/png" })
  const formData = new FormData()
  formData.append("archivo", archivo, "prueba.png")
  const subida = await api.subirImagen(token, formData)
  console.log("subirImagen devuelve url:", typeof subida.url === "string")

  await api.eliminarItem(token, item.id)
  await api.eliminarExamen(token, examen.id)
  console.log("limpieza ok")
})
'
```
Expected: `true` siete veces, y `"limpieza ok"` al final. (Ver la nota de `import.meta.env` en Global Constraints si el script falla por eso.)

- [ ] **Step 4: Commit**

```bash
git add frontend/src/api.js
git commit -m "feat(frontend): cliente API del banco de preguntas (examenes, items, clave, imagenes)"
git push origin main
```

---

### Task 2: Constantes — activar el menú y agregar catálogos de selects

**Files:**
- Modify: `frontend/src/constantes.js`

**Interfaces:**
- Consumes: nada nuevo.
- Produces: `DIFICULTADES: Array<{valor, etiqueta}>`, `TIPOS_EXAMEN: Array<{valor, etiqueta}>`, `ESTADOS_ITEM: Array<{valor, etiqueta}>`; `MENU_POR_ROL.admin` con la entrada "Banco de preguntas" activada.

- [ ] **Step 1: Editar `frontend/src/constantes.js`**

Agregar estos tres arreglos nuevos después de `EJES`/`etiquetaEje` (no tocar `NIVELES`, `CANTIDADES`, `EJES`, `etiquetaEje`):

```js
export const DIFICULTADES = [
  { valor: 'baja', etiqueta: 'Baja' },
  { valor: 'media', etiqueta: 'Media' },
  { valor: 'alta', etiqueta: 'Alta' },
]

export const TIPOS_EXAMEN = [
  { valor: 'PAES_Regular', etiqueta: 'PAES Regular' },
  { valor: 'PAES_Invierno', etiqueta: 'PAES Invierno' },
  { valor: 'PDT', etiqueta: 'PDT' },
]

export const ESTADOS_ITEM = [
  { valor: 'borrador', etiqueta: 'Borrador' },
  { valor: 'publicado', etiqueta: 'Publicado' },
  { valor: 'oculto', etiqueta: 'Oculto' },
]
```

Reemplazar únicamente la entrada de `admin` en `MENU_POR_ROL` (no tocar `estudiante`/`profesor`):

```js
export const MENU_POR_ROL = {
  estudiante: [
    { etiqueta: 'Configurar ensayo', ruta: '/', disponible: true },
    { etiqueta: 'Mi progreso', ruta: '/dashboard', disponible: true },
  ],
  profesor: [{ etiqueta: 'Mis grupos', ruta: null, disponible: false }],
  admin: [{ etiqueta: 'Banco de preguntas', ruta: '/banco/items', disponible: true }],
}
```

- [ ] **Step 2: Verificar con un script de Node**

```bash
cd frontend && node -e '
import("./src/constantes.js").then(({ MENU_POR_ROL, DIFICULTADES, TIPOS_EXAMEN, ESTADOS_ITEM }) => {
  const item = MENU_POR_ROL.admin.find((i) => i.etiqueta === "Banco de preguntas")
  console.log("Banco de preguntas disponible:", item.disponible === true)
  console.log("Banco de preguntas ruta correcta:", item.ruta === "/banco/items")
  console.log("estudiante sigue sin cambios:", MENU_POR_ROL.estudiante.length === 2)
  console.log("profesor sigue sin cambios:", MENU_POR_ROL.profesor[0].disponible === false)
  console.log("DIFICULTADES tiene 3:", DIFICULTADES.length === 3)
  console.log("TIPOS_EXAMEN tiene 3:", TIPOS_EXAMEN.length === 3)
  console.log("ESTADOS_ITEM tiene 3:", ESTADOS_ITEM.length === 3)
})
'
```
Expected: `true` siete veces.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/constantes.js
git commit -m "feat(frontend): activa 'Banco de preguntas' y agrega catalogos de dificultad/tipo-examen/estado-item"
git push origin main
```

---

### Task 3: `BancoExamenes.jsx` (lista) + estilos base de tabla

**Files:**
- Create: `frontend/src/pages/BancoExamenes.jsx`
- Modify: `frontend/src/styles.css` (agregar clases al final)
- Modify: `frontend/src/App.jsx` (nueva ruta `/banco/examenes`)

**Interfaces:**
- Consumes: `api.listarExamenes` (Task 1); `useApi()` (ya existente).
- Produces: `<BancoExamenes />` (componente de página, default export), montado en `/banco/examenes`. Clases CSS `.tarjeta-ancha` y `.banco-tabla`, reutilizadas por tareas posteriores.

- [ ] **Step 1: Escribir `frontend/src/pages/BancoExamenes.jsx`**

```jsx
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'

export default function BancoExamenes() {
  const { llamar } = useApi()
  const [examenes, setExamenes] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.listarExamenes(token))
      .then((lista) => {
        if (!cancelado) setExamenes(lista)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudieron cargar los exámenes')
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

  if (!examenes) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Exámenes fuente</h1>
        <Link
          to="/banco/examenes/nuevo"
          className="boton"
          style={{ display: 'inline-block', width: 'auto', padding: '0 16px', textDecoration: 'none' }}
        >
          Nuevo examen
        </Link>

        {examenes.length === 0 ? (
          <p>Todavía no hay exámenes registrados.</p>
        ) : (
          <table className="banco-tabla">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Nivel</th>
                <th>Año</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {examenes.map((ex) => (
                <tr key={ex.id}>
                  <td>{ex.nombre}</td>
                  <td>{ex.tipo}</td>
                  <td>{ex.nivel}</td>
                  <td>{ex.anio_admision}</td>
                  <td>
                    <Link to={`/banco/examenes/${ex.id}`}>Editar</Link>
                    {' · '}
                    <Link to={`/banco/examenes/${ex.id}/clave`}>Clave</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Agregar estilos al final de `frontend/src/styles.css`**

```css
.tarjeta-ancha {
  max-width: 900px;
}

.banco-tabla {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 14px;
}

.banco-tabla th,
.banco-tabla td {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid var(--color-borde);
}

.banco-filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}

.banco-filtros select {
  min-height: 40px;
  padding: 6px 10px;
  border: 1px solid var(--color-borde);
  border-radius: 8px;
  font-size: 14px;
}

.boton-enlace {
  border: none;
  background: none;
  color: var(--color-primario);
  cursor: pointer;
  font-size: inherit;
  padding: 0;
}

.badge-estado-item {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--color-fondo-suave);
  font-size: 12px;
  font-weight: 600;
}

.campo textarea,
.campo input[type='number'],
.campo input[type='date'],
.campo input[type='file'] {
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;
  border: 1px solid var(--color-borde);
  border-radius: 8px;
  font-size: 16px;
  font-family: inherit;
}

.campo textarea {
  min-height: 88px;
  resize: vertical;
}

.alternativa-campos {
  border: 1px solid var(--color-borde);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
}

.alternativa-campos-cabecera {
  margin-bottom: 8px;
  font-weight: 600;
}

.clave-suma-valida {
  color: #2e7d32;
  font-weight: 600;
}

.clave-suma-invalida {
  color: var(--color-error);
  font-weight: 600;
}
```

- [ ] **Step 3: Agregar la ruta `/banco/examenes` en `frontend/src/App.jsx`**

Agregar el import junto a los demás:

```jsx
import BancoExamenes from './pages/BancoExamenes.jsx'
```

Agregar la ruta nueva (junto a las demás rutas privadas):

```jsx
<Route
  path="/banco/examenes"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <BancoExamenes />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 4: Verificar manualmente con `npm run dev`**

```bash
cd frontend && npm run dev
```

Con un navegador real (Claude Preview o claude-in-chrome; recordar `preview_resize` a mobile si el viewport arranca en 0x0):
1. Loguear con la cuenta admin ya existente (escribir las credenciales directamente en el formulario, sin guardarlas en ningún archivo).
2. Navegar directo por URL a `/banco/examenes` (el link del menú todavía no funciona del todo — se completa en tareas posteriores).
3. Confirmar que se ve la lista de exámenes (puede estar vacía si es la primera vez) y el botón "Nuevo examen" (el link a `/banco/examenes/nuevo` puede dar 404 todavía — se resuelve en la Tarea 4).

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/BancoExamenes.jsx frontend/src/styles.css frontend/src/App.jsx
git commit -m "feat(frontend): lista de examenes fuente (banco de preguntas)"
git push origin main
```

---

### Task 4: `ExamenForm.jsx` (crear/editar) + rutas

**Files:**
- Create: `frontend/src/pages/ExamenForm.jsx`
- Modify: `frontend/src/App.jsx` (rutas `/banco/examenes/nuevo` y `/banco/examenes/:id`)

**Interfaces:**
- Consumes: `api.crearExamen`, `api.obtenerExamen`, `api.actualizarExamen`, `api.eliminarExamen` (Task 1); `TIPOS_EXAMEN`, `NIVELES` (Task 2 / ya existente); `useApi()`.
- Produces: `<ExamenForm />` (componente de página, default export), montado en `/banco/examenes/nuevo` (crear) y `/banco/examenes/:id` (editar, mismo componente, distingue por `useParams().id === undefined`).

- [ ] **Step 1: Escribir `frontend/src/pages/ExamenForm.jsx`**

```jsx
import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { NIVELES, TIPOS_EXAMEN } from '../constantes.js'

const VACIO = {
  nombre: '',
  anio_admision: new Date().getFullYear(),
  tipo: TIPOS_EXAMEN[0].valor,
  nivel: NIVELES[0],
  edicion: '',
  url_pdf: '',
  fecha_publicacion: '',
}

export default function ExamenForm() {
  const { id } = useParams()
  const esNuevo = id === undefined
  const navigate = useNavigate()
  const { llamar } = useApi()
  const [form, setForm] = useState(VACIO)
  const [cargando, setCargando] = useState(!esNuevo)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    if (esNuevo) return
    let cancelado = false
    llamar((token) => api.obtenerExamen(token, id))
      .then((ex) => {
        if (cancelado) return
        setForm({
          nombre: ex.nombre,
          anio_admision: ex.anio_admision,
          tipo: ex.tipo,
          nivel: ex.nivel,
          edicion: ex.edicion ?? '',
          url_pdf: ex.url_pdf ?? '',
          fecha_publicacion: ex.fecha_publicacion ?? '',
        })
        setCargando(false)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el examen')
      })
    return () => {
      cancelado = true
    }
  }, [esNuevo, id, llamar])

  function actualizarCampo(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }))
  }

  async function guardar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    const cuerpo = {
      nombre: form.nombre,
      anio_admision: Number(form.anio_admision),
      tipo: form.tipo,
      nivel: form.nivel,
      edicion: form.edicion || null,
      url_pdf: form.url_pdf || null,
      fecha_publicacion: form.fecha_publicacion || null,
    }
    try {
      if (esNuevo) {
        await llamar((token) => api.crearExamen(token, cuerpo))
      } else {
        await llamar((token) => api.actualizarExamen(token, id, cuerpo))
      }
      navigate('/banco/examenes')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo guardar el examen' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  async function eliminar() {
    if (!window.confirm('¿Eliminar este examen?')) return
    try {
      await llamar((token) => api.eliminarExamen(token, id))
      navigate('/banco/examenes')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo eliminar el examen' : 'No se pudo conectar con el servidor')
    }
  }

  if (cargando) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta">
        <h1>{esNuevo ? 'Nuevo examen' : 'Editar examen'}</h1>
        <form onSubmit={guardar}>
          <div className="campo">
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              type="text"
              value={form.nombre}
              onChange={(e) => actualizarCampo('nombre', e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="anio">Año de admisión</label>
            <input
              id="anio"
              type="number"
              value={form.anio_admision}
              onChange={(e) => actualizarCampo('anio_admision', e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="tipo">Tipo</label>
            <select id="tipo" value={form.tipo} onChange={(e) => actualizarCampo('tipo', e.target.value)}>
              {TIPOS_EXAMEN.map((t) => (
                <option key={t.valor} value={t.valor}>
                  {t.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="nivel">Nivel</label>
            <select id="nivel" value={form.nivel} onChange={(e) => actualizarCampo('nivel', e.target.value)}>
              {NIVELES.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="edicion">Edición (opcional)</label>
            <input id="edicion" type="text" value={form.edicion} onChange={(e) => actualizarCampo('edicion', e.target.value)} />
          </div>
          <div className="campo">
            <label htmlFor="url_pdf">URL del PDF (opcional)</label>
            <input id="url_pdf" type="text" value={form.url_pdf} onChange={(e) => actualizarCampo('url_pdf', e.target.value)} />
          </div>
          <div className="campo">
            <label htmlFor="fecha_publicacion">Fecha de publicación (opcional)</label>
            <input
              id="fecha_publicacion"
              type="date"
              value={form.fecha_publicacion}
              onChange={(e) => actualizarCampo('fecha_publicacion', e.target.value)}
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? 'Guardando…' : 'Guardar'}
          </button>
        </form>
        {!esNuevo && (
          <button
            type="button"
            className="boton-secundario"
            style={{ marginTop: 12, borderColor: 'var(--color-error)', color: 'var(--color-error)' }}
            onClick={eliminar}
          >
            Eliminar examen
          </button>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Agregar las rutas en `frontend/src/App.jsx`**

Agregar el import:

```jsx
import ExamenForm from './pages/ExamenForm.jsx'
```

Agregar ambas rutas (una para crear, una para editar, mismo componente):

```jsx
<Route
  path="/banco/examenes/nuevo"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <ExamenForm />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
<Route
  path="/banco/examenes/:id"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <ExamenForm />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 3: Verificar manualmente con `npm run dev`**

```bash
cd frontend && npm run dev
```

1. Loguear como admin, ir a `/banco/examenes`.
2. Tocar "Nuevo examen", completar el formulario (nombre, año, tipo, nivel), guardar.
3. Confirmar que vuelve a `/banco/examenes` y el examen nuevo aparece en la lista.
4. Tocar "Editar" en ese examen, cambiar el nombre, guardar, confirmar que el cambio se refleja en la lista.
5. Volver a entrar a "Editar", tocar "Eliminar examen", confirmar el diálogo, confirmar que desaparece de la lista.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/ExamenForm.jsx frontend/src/App.jsx
git commit -m "feat(frontend): formulario de examen fuente (crear/editar/eliminar)"
git push origin main
```

---

### Task 5: `AlternativaCampos.jsx` + `ItemForm.jsx` (crear/editar ítem) + rutas

**Files:**
- Create: `frontend/src/components/AlternativaCampos.jsx`
- Create: `frontend/src/pages/ItemForm.jsx`
- Modify: `frontend/src/App.jsx` (rutas `/banco/items/nuevo` y `/banco/items/:id`)

**Interfaces:**
- Consumes: `api.crearItem`, `api.obtenerItem`, `api.actualizarItem`, `api.subirImagen`, `api.listarExamenes` (Task 1); `EJES`, `NIVELES`, `DIFICULTADES` (Task 2 / existente); `<Formula texto={...} />` (existente); `useApi()`.
- Produces: `<AlternativaCampos alternativa nombre="alternativa-correcta" onCambiarTexto onCambiarImagen onMarcarCorrecta subiendo />` (subcomponente, usado solo por `ItemForm`); `<ItemForm />` (componente de página, default export), montado en `/banco/items/nuevo` y `/banco/items/:id`.

- [ ] **Step 1: Escribir `frontend/src/components/AlternativaCampos.jsx`**

```jsx
export default function AlternativaCampos({ alternativa, onCambiarTexto, onCambiarImagen, onMarcarCorrecta, subiendo }) {
  return (
    <div className="alternativa-campos">
      <div className="alternativa-campos-cabecera">
        <label>
          <input
            type="radio"
            name="alternativa-correcta"
            checked={alternativa.es_correcta}
            onChange={() => onMarcarCorrecta(alternativa.etiqueta)}
          />{' '}
          {alternativa.etiqueta}) es la correcta
        </label>
      </div>
      <textarea
        value={alternativa.texto}
        onChange={(e) => onCambiarTexto(alternativa.etiqueta, e.target.value)}
        placeholder={`Texto de la alternativa ${alternativa.etiqueta} (soporta LaTeX)`}
        required
      />
      <input
        type="file"
        accept="image/png,image/jpeg,image/webp"
        onChange={(e) => e.target.files[0] && onCambiarImagen(alternativa.etiqueta, e.target.files[0])}
      />
      {subiendo && <p>Subiendo imagen…</p>}
      {alternativa.imagen_url && (
        <img src={alternativa.imagen_url} alt="" style={{ maxWidth: '100%', marginTop: 8 }} />
      )}
    </div>
  )
}
```

- [ ] **Step 2: Escribir `frontend/src/pages/ItemForm.jsx`**

```jsx
import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, ApiError } from '../api.js'
import { useApi } from '../useApi.js'
import { NIVELES, EJES, DIFICULTADES } from '../constantes.js'
import Formula from '../components/Formula.jsx'
import AlternativaCampos from '../components/AlternativaCampos.jsx'

const ALTERNATIVAS_VACIAS = ['A', 'B', 'C', 'D'].map((etiqueta) => ({
  etiqueta,
  texto: '',
  imagen_url: null,
  es_correcta: false,
}))

const VACIO = {
  enunciado: '',
  imagen_url: null,
  eje: EJES[0].valor,
  nivel: NIVELES[0],
  dificultad: DIFICULTADES[0].valor,
  peso: '',
  examen_fuente_id: '',
  explicacion: '',
  alternativas: ALTERNATIVAS_VACIAS,
}

export default function ItemForm() {
  const { id } = useParams()
  const esNuevo = id === undefined
  const navigate = useNavigate()
  const { llamar } = useApi()
  const [form, setForm] = useState(VACIO)
  const [examenes, setExamenes] = useState([])
  const [cargando, setCargando] = useState(!esNuevo)
  const [error, setError] = useState(null)
  const [enviando, setEnviando] = useState(false)
  const [subiendoImagen, setSubiendoImagen] = useState(null)

  useEffect(() => {
    let cancelado = false
    llamar((token) => api.listarExamenes(token))
      .then((lista) => {
        if (!cancelado) setExamenes(lista)
      })
      .catch(() => {})
    return () => {
      cancelado = true
    }
  }, [llamar])

  useEffect(() => {
    if (esNuevo) return
    let cancelado = false
    llamar((token) => api.obtenerItem(token, id))
      .then((it) => {
        if (cancelado) return
        setForm({
          enunciado: it.enunciado,
          imagen_url: it.imagen_url,
          eje: it.eje,
          nivel: it.nivel,
          dificultad: it.dificultad,
          peso: it.peso ?? '',
          examen_fuente_id: it.examen_fuente_id ?? '',
          explicacion: it.explicacion ?? '',
          alternativas: it.alternativas.map((a) => ({
            etiqueta: a.etiqueta,
            texto: a.texto,
            imagen_url: a.imagen_url,
            es_correcta: a.es_correcta,
          })),
        })
        setCargando(false)
      })
      .catch(() => {
        if (!cancelado) setError('No se pudo cargar el ítem')
      })
    return () => {
      cancelado = true
    }
  }, [esNuevo, id, llamar])

  function actualizarCampo(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }))
  }

  function cambiarTextoAlternativa(etiqueta, texto) {
    setForm((f) => ({
      ...f,
      alternativas: f.alternativas.map((a) => (a.etiqueta === etiqueta ? { ...a, texto } : a)),
    }))
  }

  function marcarCorrecta(etiqueta) {
    setForm((f) => ({
      ...f,
      alternativas: f.alternativas.map((a) => ({ ...a, es_correcta: a.etiqueta === etiqueta })),
    }))
  }

  async function subirImagenItem(archivo) {
    setSubiendoImagen('item')
    try {
      const datos = new FormData()
      datos.append('archivo', archivo)
      const { url } = await llamar((token) => api.subirImagen(token, datos))
      actualizarCampo('imagen_url', url)
    } catch {
      setError('No se pudo subir la imagen')
    } finally {
      setSubiendoImagen(null)
    }
  }

  async function subirImagenAlternativa(etiqueta, archivo) {
    setSubiendoImagen(etiqueta)
    try {
      const datos = new FormData()
      datos.append('archivo', archivo)
      const { url } = await llamar((token) => api.subirImagen(token, datos))
      setForm((f) => ({
        ...f,
        alternativas: f.alternativas.map((a) => (a.etiqueta === etiqueta ? { ...a, imagen_url: url } : a)),
      }))
    } catch {
      setError('No se pudo subir la imagen')
    } finally {
      setSubiendoImagen(null)
    }
  }

  async function guardar(evento) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    const cuerpo = {
      examen_fuente_id: form.examen_fuente_id || null,
      enunciado: form.enunciado,
      imagen_url: form.imagen_url,
      eje: form.eje,
      nivel: form.nivel,
      dificultad: form.dificultad,
      peso: form.peso === '' ? null : Number(form.peso),
      explicacion: form.explicacion || null,
      alternativas: form.alternativas,
    }
    try {
      if (esNuevo) {
        await llamar((token) => api.crearItem(token, cuerpo))
      } else {
        await llamar((token) => api.actualizarItem(token, id, cuerpo))
      }
      navigate('/banco/items')
    } catch (err) {
      setError(err instanceof ApiError ? err.mensaje || 'No se pudo guardar el ítem' : 'No se pudo conectar con el servidor')
    } finally {
      setEnviando(false)
    }
  }

  if (cargando) {
    return (
      <div className="pantalla">
        <div className="tarjeta tarjeta-ancha">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>{esNuevo ? 'Nuevo ítem' : 'Editar ítem'}</h1>
        <form onSubmit={guardar}>
          <div className="campo">
            <label htmlFor="enunciado">Enunciado (soporta LaTeX)</label>
            <textarea
              id="enunciado"
              value={form.enunciado}
              onChange={(e) => actualizarCampo('enunciado', e.target.value)}
              required
            />
            {form.enunciado && <Formula texto={form.enunciado} />}
          </div>
          <div className="campo">
            <label htmlFor="imagen-item">Imagen del ítem (opcional)</label>
            <input
              id="imagen-item"
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => e.target.files[0] && subirImagenItem(e.target.files[0])}
            />
            {subiendoImagen === 'item' && <p>Subiendo imagen…</p>}
            {form.imagen_url && <img src={form.imagen_url} alt="" style={{ maxWidth: '100%', marginTop: 8 }} />}
          </div>
          <div className="campo">
            <label htmlFor="eje">Eje</label>
            <select id="eje" value={form.eje} onChange={(e) => actualizarCampo('eje', e.target.value)}>
              {EJES.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="nivel">Nivel</label>
            <select id="nivel" value={form.nivel} onChange={(e) => actualizarCampo('nivel', e.target.value)}>
              {NIVELES.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="dificultad">Dificultad</label>
            <select id="dificultad" value={form.dificultad} onChange={(e) => actualizarCampo('dificultad', e.target.value)}>
              {DIFICULTADES.map((d) => (
                <option key={d.valor} value={d.valor}>
                  {d.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="peso">Peso (requerido para publicar)</label>
            <input id="peso" type="number" min="0" value={form.peso} onChange={(e) => actualizarCampo('peso', e.target.value)} />
          </div>
          <div className="campo">
            <label htmlFor="examen">Examen fuente (opcional)</label>
            <select
              id="examen"
              value={form.examen_fuente_id}
              onChange={(e) => actualizarCampo('examen_fuente_id', e.target.value)}
            >
              <option value="">(ninguno)</option>
              {examenes.map((ex) => (
                <option key={ex.id} value={ex.id}>
                  {ex.nombre}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="explicacion">Explicación (opcional)</label>
            <textarea id="explicacion" value={form.explicacion} onChange={(e) => actualizarCampo('explicacion', e.target.value)} />
          </div>

          <h2>Alternativas</h2>
          {form.alternativas.map((alt) => (
            <AlternativaCampos
              key={alt.etiqueta}
              alternativa={alt}
              onCambiarTexto={cambiarTextoAlternativa}
              onCambiarImagen={subirImagenAlternativa}
              onMarcarCorrecta={marcarCorrecta}
              subiendo={subiendoImagen === alt.etiqueta}
            />
          ))}

          {error && <p className="error">{error}</p>}
          <button className="boton" type="submit" disabled={enviando} style={{ marginTop: 8 }}>
            {enviando ? 'Guardando…' : 'Guardar'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Agregar las rutas en `frontend/src/App.jsx`**

Agregar los imports:

```jsx
import ItemForm from './pages/ItemForm.jsx'
```

Agregar ambas rutas:

```jsx
<Route
  path="/banco/items/nuevo"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <ItemForm />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
<Route
  path="/banco/items/:id"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <ItemForm />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 4: Verificar manualmente con `npm run dev`**

```bash
cd frontend && npm run dev
```

1. Loguear como admin, ir directo por URL a `/banco/items/nuevo`.
2. Completar enunciado (probar con algo de LaTeX, ej. `La ecuación $x^2 + 1 = 0$`) y confirmar que la previsualización con `<Formula>` renderiza la fórmula.
3. Completar eje/nivel/dificultad/peso, subir una imagen de prueba en el campo de imagen del ítem, confirmar que aparece el preview de la imagen subida.
4. Completar las 4 alternativas, marcar una como correcta (radio), guardar.
5. Confirmar que redirige a `/banco/items` (puede dar 404 todavía — se resuelve en la Tarea 6, no es un bloqueante de esta tarea).
6. Volver a `/banco/items/nuevo`, intentar guardar con solo 3 alternativas completas — confirmar que el backend devuelve un error de validación y se muestra en pantalla (no crashea).
7. Editar el ítem creado en el paso 4 (navegar directo por URL a `/banco/items/:id` con el id devuelto) y confirmar que el formulario se precarga con sus datos.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/AlternativaCampos.jsx frontend/src/pages/ItemForm.jsx frontend/src/App.jsx
git commit -m "feat(frontend): formulario de item con alternativas e imagenes (crear/editar)"
git push origin main
```

---

### Task 6: `BancoItems.jsx` (lista, filtros, paginado, publicar/ocultar) + ruta

**Files:**
- Create: `frontend/src/pages/BancoItems.jsx`
- Modify: `frontend/src/App.jsx` (nueva ruta `/banco/items`)

**Interfaces:**
- Consumes: `api.listarItems`, `api.publicarItem`, `api.ocultarItem` (Task 1); `EJES`, `NIVELES`, `DIFICULTADES`, `ESTADOS_ITEM`, `etiquetaEje` (Task 2 / existente); `useApi()`.
- Produces: `<BancoItems />` (componente de página, default export), montado en `/banco/items`.

- [ ] **Step 1: Escribir `frontend/src/pages/BancoItems.jsx`**

```jsx
import { useState, useEffect, useCallback } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES, NIVELES, DIFICULTADES, ESTADOS_ITEM, etiquetaEje } from '../constantes.js'

const TAMANO_PAGINA = 20

export default function BancoItems() {
  const { llamar } = useApi()
  const [searchParams, setSearchParams] = useSearchParams()
  const [items, setItems] = useState(null)
  const [error, setError] = useState(null)
  const [accionError, setAccionError] = useState(null)
  const [pagina, setPagina] = useState(0)

  const nivel = searchParams.get('nivel') ?? ''
  const eje = searchParams.get('eje') ?? ''
  const dificultad = searchParams.get('dificultad') ?? ''
  const estado = searchParams.get('estado') ?? ''
  const examenId = searchParams.get('examenId') ?? ''

  const cargar = useCallback(() => {
    setError(null)
    llamar((token) =>
      api.listarItems(token, {
        nivel: nivel || undefined,
        eje: eje || undefined,
        dificultad: dificultad || undefined,
        estado: estado || undefined,
        examenId: examenId || undefined,
        limit: TAMANO_PAGINA,
        offset: pagina * TAMANO_PAGINA,
      }),
    )
      .then(setItems)
      .catch(() => setError('No se pudieron cargar los ítems'))
  }, [llamar, nivel, eje, dificultad, estado, examenId, pagina])

  useEffect(() => {
    cargar()
  }, [cargar])

  function actualizarFiltro(clave, valor) {
    setPagina(0)
    const nuevos = new URLSearchParams(searchParams)
    if (valor) nuevos.set(clave, valor)
    else nuevos.delete(clave)
    setSearchParams(nuevos)
  }

  async function publicar(id) {
    setAccionError(null)
    try {
      await llamar((token) => api.publicarItem(token, id))
      cargar()
    } catch (err) {
      setAccionError(err.mensaje || 'No se pudo publicar el ítem')
    }
  }

  async function ocultar(id) {
    setAccionError(null)
    try {
      await llamar((token) => api.ocultarItem(token, id))
      cargar()
    } catch (err) {
      setAccionError(err.mensaje || 'No se pudo ocultar el ítem')
    }
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Ítems</h1>
        <Link
          to="/banco/items/nuevo"
          className="boton"
          style={{ display: 'inline-block', width: 'auto', padding: '0 16px', textDecoration: 'none' }}
        >
          Nuevo ítem
        </Link>

        {examenId && (
          <p>
            Filtrando por examen.{' '}
            <button type="button" className="boton-enlace" onClick={() => actualizarFiltro('examenId', '')}>
              Quitar filtro
            </button>
          </p>
        )}

        <div className="banco-filtros">
          <select value={nivel} onChange={(e) => actualizarFiltro('nivel', e.target.value)}>
            <option value="">Nivel: todos</option>
            {NIVELES.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
          <select value={eje} onChange={(e) => actualizarFiltro('eje', e.target.value)}>
            <option value="">Eje: todos</option>
            {EJES.map((e) => (
              <option key={e.valor} value={e.valor}>
                {e.etiqueta}
              </option>
            ))}
          </select>
          <select value={dificultad} onChange={(e) => actualizarFiltro('dificultad', e.target.value)}>
            <option value="">Dificultad: todas</option>
            {DIFICULTADES.map((d) => (
              <option key={d.valor} value={d.valor}>
                {d.etiqueta}
              </option>
            ))}
          </select>
          <select value={estado} onChange={(e) => actualizarFiltro('estado', e.target.value)}>
            <option value="">Estado: todos</option>
            {ESTADOS_ITEM.map((e) => (
              <option key={e.valor} value={e.valor}>
                {e.etiqueta}
              </option>
            ))}
          </select>
        </div>

        {accionError && <p className="error">{accionError}</p>}
        {error && <p className="error">{error}</p>}

        {!items ? (
          <p>Cargando…</p>
        ) : items.length === 0 ? (
          <p>No hay ítems con estos filtros.</p>
        ) : (
          <table className="banco-tabla">
            <thead>
              <tr>
                <th>Enunciado</th>
                <th>Eje</th>
                <th>Estado</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {items.map((it) => (
                <tr key={it.id}>
                  <td>
                    {it.enunciado.slice(0, 60)}
                    {it.enunciado.length > 60 ? '…' : ''}
                  </td>
                  <td>{etiquetaEje(it.eje)}</td>
                  <td>
                    <span className="badge-estado-item">{it.estado}</span>
                  </td>
                  <td>
                    <Link to={`/banco/items/${it.id}`}>Editar</Link>
                    {' · '}
                    {it.estado === 'publicado' ? (
                      <button type="button" className="boton-enlace" onClick={() => ocultar(it.id)}>
                        Ocultar
                      </button>
                    ) : (
                      <button type="button" className="boton-enlace" onClick={() => publicar(it.id)}>
                        Publicar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
          <button
            className="boton-secundario"
            type="button"
            style={{ width: 'auto', padding: '0 16px' }}
            disabled={pagina === 0}
            onClick={() => setPagina((p) => p - 1)}
          >
            Anterior
          </button>
          <button
            className="boton-secundario"
            type="button"
            style={{ width: 'auto', padding: '0 16px' }}
            disabled={!items || items.length < TAMANO_PAGINA}
            onClick={() => setPagina((p) => p + 1)}
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Agregar la ruta `/banco/items` en `frontend/src/App.jsx`**

Agregar el import:

```jsx
import BancoItems from './pages/BancoItems.jsx'
```

Agregar la ruta:

```jsx
<Route
  path="/banco/items"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <BancoItems />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 3: Verificar manualmente con `npm run dev`**

```bash
cd frontend && npm run dev
```

1. Loguear como admin, ir a `/banco/items` (ahora sí resuelve — confirmar también que el link "Nuevo ítem" de la Tarea 5 ya redirige acá correctamente).
2. Confirmar que se ven ítems reales (hoy hay 431 en la base) y que el paginado (Anterior/Siguiente) funciona.
3. Filtrar por eje y por estado, confirmar que la lista se actualiza y que la URL refleja los filtros (`?eje=...&estado=...`).
4. Sobre un ítem en `borrador` sin peso asignado, tocar "Publicar" y confirmar que se muestra el error de validación (422) sin romper la pantalla.
5. Editar ese mismo ítem (Tarea 5), asignarle un peso, guardar, volver a `/banco/items`, tocar "Publicar" de nuevo y confirmar que ahora sí pasa a `publicado`.
6. Tocar "Ocultar" sobre ese ítem publicado y confirmar que pasa a `oculto`.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/BancoItems.jsx frontend/src/App.jsx
git commit -m "feat(frontend): lista de items con filtros, paginado y publicar/ocultar"
git push origin main
```

---

### Task 7: `ExamenClave.jsx` (pesos + importar PDF) + ruta

**Files:**
- Create: `frontend/src/pages/ExamenClave.jsx`
- Modify: `frontend/src/App.jsx` (nueva ruta `/banco/examenes/:id/clave`)

**Interfaces:**
- Consumes: `api.listarItems`, `api.obtenerClave`, `api.definirClave`, `api.importarPdf` (Task 1); `EJES`, `DIFICULTADES` (Task 2); `useApi()`.
- Produces: `<ExamenClave />` (componente de página, default export), montado en `/banco/examenes/:id/clave`. Al importar un PDF, navega a `/banco/items?examenId=:id&estado=borrador` (consumido por `BancoItems`, Task 6, que ya lee filtros iniciales de la query string).

- [ ] **Step 1: Escribir `frontend/src/pages/ExamenClave.jsx`**

```jsx
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api.js'
import { useApi } from '../useApi.js'
import { EJES, DIFICULTADES } from '../constantes.js'

export default function ExamenClave() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { llamar } = useApi()
  const [items, setItems] = useState(null)
  const [pesos, setPesos] = useState({})
  const [error, setError] = useState(null)
  const [guardando, setGuardando] = useState(false)
  const [mensajeGuardado, setMensajeGuardado] = useState(null)

  const [archivoPdf, setArchivoPdf] = useState(null)
  const [ejePdf, setEjePdf] = useState(EJES[0].valor)
  const [dificultadPdf, setDificultadPdf] = useState(DIFICULTADES[0].valor)
  const [importando, setImportando] = useState(false)
  const [errorPdf, setErrorPdf] = useState(null)

  const cargar = useCallback(() => {
    setError(null)
    Promise.all([
      llamar((token) => api.listarItems(token, { examenId: id, limit: 200 })),
      llamar((token) => api.obtenerClave(token, id)),
    ])
      .then(([listaItems, clave]) => {
        setItems(listaItems)
        const iniciales = {}
        for (const it of listaItems) iniciales[it.id] = it.peso ?? 0
        for (const p of clave.pesos) iniciales[p.item_id] = p.peso
        setPesos(iniciales)
      })
      .catch(() => setError('No se pudo cargar la clave'))
  }, [llamar, id])

  useEffect(() => {
    cargar()
  }, [cargar])

  const suma = Object.values(pesos).reduce((acc, p) => acc + Number(p || 0), 0)

  function cambiarPeso(itemId, valor) {
    setPesos((p) => ({ ...p, [itemId]: valor }))
  }

  async function guardarClave() {
    setGuardando(true)
    setError(null)
    setMensajeGuardado(null)
    try {
      const cuerpo = Object.entries(pesos).map(([itemId, peso]) => ({ item_id: itemId, peso: Number(peso) }))
      await llamar((token) => api.definirClave(token, id, cuerpo))
      setMensajeGuardado('Clave guardada')
    } catch (err) {
      setError(err.mensaje || 'No se pudo guardar la clave')
    } finally {
      setGuardando(false)
    }
  }

  async function importarPdf(evento) {
    evento.preventDefault()
    if (!archivoPdf) return
    setImportando(true)
    setErrorPdf(null)
    try {
      const datos = new FormData()
      datos.append('archivo', archivoPdf)
      datos.append('eje', ejePdf)
      datos.append('dificultad', dificultadPdf)
      await llamar((token) => api.importarPdf(token, id, datos))
      navigate(`/banco/items?examenId=${id}&estado=borrador`)
    } catch (err) {
      setErrorPdf(err.mensaje || 'No se pudo importar el PDF')
    } finally {
      setImportando(false)
    }
  }

  if (error && !items) {
    return (
      <div className="pantalla">
        <div className="tarjeta">
          <p className="error">{error}</p>
        </div>
      </div>
    )
  }

  if (!items) {
    return (
      <div className="pantalla">
        <div className="tarjeta">Cargando…</div>
      </div>
    )
  }

  return (
    <div className="pantalla">
      <div className="tarjeta tarjeta-ancha">
        <h1>Clave del examen</h1>

        {items.length === 0 ? (
          <p>Este examen todavía no tiene ítems asociados.</p>
        ) : (
          <>
            <table className="banco-tabla">
              <thead>
                <tr>
                  <th>Enunciado</th>
                  <th>Estado</th>
                  <th>Peso</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it) => (
                  <tr key={it.id}>
                    <td>
                      {it.enunciado.slice(0, 50)}
                      {it.enunciado.length > 50 ? '…' : ''}
                    </td>
                    <td>{it.estado}</td>
                    <td>
                      <input
                        type="number"
                        min="0"
                        style={{ width: 80, minHeight: 36 }}
                        value={pesos[it.id] ?? 0}
                        onChange={(e) => cambiarPeso(it.id, e.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className={suma === 1000 ? 'clave-suma-valida' : 'clave-suma-invalida'}>Suma de pesos: {suma} / 1000</p>
            {error && <p className="error">{error}</p>}
            {mensajeGuardado && <p>{mensajeGuardado}</p>}
            <button
              className="boton"
              type="button"
              disabled={guardando}
              style={{ width: 'auto', padding: '0 16px' }}
              onClick={guardarClave}
            >
              {guardando ? 'Guardando…' : 'Guardar clave'}
            </button>
          </>
        )}

        <h2>Importar preguntas desde PDF</h2>
        <form onSubmit={importarPdf}>
          <div className="campo">
            <label htmlFor="archivo-pdf">Archivo PDF</label>
            <input
              id="archivo-pdf"
              type="file"
              accept="application/pdf"
              onChange={(e) => setArchivoPdf(e.target.files[0] ?? null)}
              required
            />
          </div>
          <div className="campo">
            <label htmlFor="eje-pdf">Eje por defecto</label>
            <select id="eje-pdf" value={ejePdf} onChange={(e) => setEjePdf(e.target.value)}>
              {EJES.map((e) => (
                <option key={e.valor} value={e.valor}>
                  {e.etiqueta}
                </option>
              ))}
            </select>
          </div>
          <div className="campo">
            <label htmlFor="dificultad-pdf">Dificultad por defecto</label>
            <select id="dificultad-pdf" value={dificultadPdf} onChange={(e) => setDificultadPdf(e.target.value)}>
              {DIFICULTADES.map((d) => (
                <option key={d.valor} value={d.valor}>
                  {d.etiqueta}
                </option>
              ))}
            </select>
          </div>
          {errorPdf && <p className="error">{errorPdf}</p>}
          <button className="boton" type="submit" disabled={importando} style={{ width: 'auto', padding: '0 16px' }}>
            {importando ? 'Importando…' : 'Importar'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Agregar la ruta en `frontend/src/App.jsx`**

Agregar el import:

```jsx
import ExamenClave from './pages/ExamenClave.jsx'
```

Agregar la ruta:

```jsx
<Route
  path="/banco/examenes/:id/clave"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <ExamenClave />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 3: Generar un PDF de prueba**

Este PDF es solo para verificación manual — no se commitea al repositorio. Si `fpdf2` no está instalado:

```bash
pip install fpdf2
```

Generarlo con:

```bash
python3 -c '
from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)
texto = """1. Cuanto es 2 mas 2?
A) 3
B) 4
C) 5
D) 6

2. Cual es la capital de Chile?
A) Valparaiso
B) Santiago
C) Concepcion
D) Temuco
"""
for linea in texto.split("\n"):
    pdf.cell(0, 8, linea, ln=1)
pdf.output("/tmp/prueba_importacion.pdf")
print("PDF generado en /tmp/prueba_importacion.pdf")
'
```

(En Windows sin `/tmp`, usar cualquier ruta temporal, ej. la carpeta de scratchpad de la sesión.)

- [ ] **Step 4: Verificar manualmente con `npm run dev`**

```bash
cd frontend && npm run dev
```

1. Loguear como admin, crear un examen nuevo (Tarea 4) y anotar su id (o navegar desde la lista).
2. Ir a "Clave" de ese examen (`/banco/examenes/:id/clave`). Debería decir "Este examen todavía no tiene ítems asociados".
3. En la sección "Importar preguntas desde PDF", subir el PDF de prueba generado en el Step 3, elegir eje/dificultad, tocar "Importar".
4. Confirmar que redirige a `/banco/items?examenId=:id&estado=borrador` y que se ven 2 ítems nuevos en estado `borrador` (uno por cada pregunta del PDF de prueba).
5. Volver a "Clave" de ese examen — ahora deberían aparecer esos 2 ítems en la tabla de pesos.
6. Asignar pesos que no sumen 1000 (ej. 300 y 300), tocar "Guardar clave", confirmar que se muestra el error del backend ("La suma de los pesos debe ser 1000") y que el indicador de suma está en rojo.
7. Corregir los pesos para que sumen 1000 (ej. 500 y 500), confirmar que el indicador pasa a verde y que "Guardar clave" muestra "Clave guardada".

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/ExamenClave.jsx frontend/src/App.jsx
git commit -m "feat(frontend): clave de pesos por examen e importacion asistida de PDF"
git push origin main
```

---

### Task 8: Redirección de `/` según rol

**Files:**
- Modify: `frontend/src/App.jsx`

**Interfaces:**
- Consumes: `useAuth()` (existente, expone `{ usuario }`); `ConfigurarEnsayo` (existente, ya importado en `App.jsx`).
- Produces: componente interno `InicioPorRol` (no exportado, vive solo en `App.jsx`), usado como `element` de la ruta `/`.

- [ ] **Step 1: Agregar el import de `useAuth` y `Navigate` en `frontend/src/App.jsx`**

```jsx
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'
```

(La línea de `Routes, Route` ya existe — reemplazarla por la de arriba, que agrega `Navigate`. La línea de `useAuth` es nueva.)

- [ ] **Step 2: Agregar el componente `InicioPorRol` en `frontend/src/App.jsx`**

Agregar antes de `export default function App()`:

```jsx
function InicioPorRol() {
  const { usuario } = useAuth()
  if (usuario?.rol === 'admin') return <Navigate to="/banco/items" replace />
  return <ConfigurarEnsayo />
}
```

- [ ] **Step 3: Usar `InicioPorRol` en la ruta `/`**

Reemplazar el `element` de la ruta `/` (que hoy renderiza `<ConfigurarEnsayo />` directo) para que use `<InicioPorRol />`:

```jsx
<Route
  path="/"
  element={
    <RutaPrivada>
      <LayoutAutenticado>
        <InicioPorRol />
      </LayoutAutenticado>
    </RutaPrivada>
  }
/>
```

- [ ] **Step 4: Verificar manualmente con `npm run dev`**

```bash
cd frontend && npm run dev
```

1. Loguear como admin → confirmar que cae directo en `/banco/items` (no en la pantalla de "Configurar ensayo").
2. Cerrar sesión, loguear con un estudiante existente (o registrar uno nuevo vía `/registro`) → confirmar que sigue cayendo en "Configurar ensayo" en `/`, sin cambios de comportamiento.
3. Desde el estudiante, abrir el drawer del menú y confirmar que "Configurar ensayo" y "Mi progreso" siguen funcionando igual que antes.
4. Desde el admin, abrir el drawer del menú y confirmar que "Banco de preguntas" navega correctamente a `/banco/items`.

Parar el dev server (Ctrl+C) al terminar.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/App.jsx
git commit -m "feat(frontend): redirige / a /banco/items para el rol admin"
git push origin main
```

---

### Task 9: Desplegar en Proxmox

**Files:** ninguno (solo comandos de despliegue).

**Interfaces:** Consumes: todo lo anterior (build de producción del frontend con el banco de preguntas incluido).

- [ ] **Step 1: Redesplegar el frontend en el CT 118 de Proxmox**

```bash
# vía SSH al host 192.168.0.155 -> pct exec 118:
cd /opt/app && git pull && docker compose up -d --build web
```

- [ ] **Step 2: Verificar en el navegador contra el despliegue real**

Abrir `http://192.168.0.190/` (y `http://100.93.161.84/` vía Tailscale), loguear con la cuenta admin, y repetir un flujo completo contra el despliegue real:
1. Crear un examen.
2. Crear un ítem con sus 4 alternativas, asignarle peso, publicarlo.
3. Ir a la clave del examen, verificar que la suma se calcula bien.
4. Ocultar el ítem publicado y confirmar que el estado cambia.
5. Confirmar que un login de estudiante sigue cayendo en "Configurar ensayo" sin cambios.

# Menú de usuario (datos, navegación por rol, logout)

Fecha: 2026-07-07

## Contexto

El frontend actual (tanda anterior) solo tiene el flujo de estudiante
(`ConfigurarEnsayo`, `RendirEnsayo`, `Resultado`) sin ninguna forma de ver
quién está logueado, navegar a otras secciones, o cerrar sesión. Profesor y
admin no tienen ninguna pantalla propia en el frontend todavía (aunque el
backend ya soporta sus endpoints: grupos, banco de preguntas), y el
estudiante tampoco tiene su dashboard de progreso construido aún.

Esta tanda agrega un menú visual, persistente en las pantallas
autenticadas, que resuelve tres cosas: ver los datos del usuario logueado,
navegar a las funcionalidades de su rol (las que ya existen y las que
todavía no, mostradas como deshabilitadas), y cerrar sesión.

## Alcance

- Barra superior + drawer de navegación, presente en las 3 rutas privadas
  actuales (`/`, `/ensayos/:id`, `/ensayos/:id/resultado`).
- Datos del usuario mostrados: nombre, email, rol (ya vienen en
  `useAuth().usuario`, sin requests nuevos al backend).
- Links de navegación por rol, definidos como datos (`MENU_POR_ROL`), no
  como código repetido:
  - **Estudiante:** "Configurar ensayo" (activo, ruta `/`), "Mi progreso"
    (deshabilitado — el dashboard aún no existe).
  - **Profesor:** "Mis grupos" (deshabilitado — sin pantalla propia
    todavía).
  - **Admin:** "Banco de preguntas" (deshabilitado — sin pantalla propia
    todavía).
- Botón "Cerrar sesión", separado visualmente del resto, al final del
  drawer.

Fuera de alcance: construir las pantallas reales de dashboard/grupos/banco
(quedan para tandas futuras — activarlas después es solo cambiar el dato
`disponible`/`ruta` en `MENU_POR_ROL`, sin tocar el componente del menú).

## Arquitectura

- **`frontend/src/components/LayoutAutenticado.jsx`** (nuevo): envuelve el
  contenido de una ruta privada, agregando la barra superior y el drawer.
  Responsabilidad separada de `RutaPrivada` (que sigue encargándose
  únicamente del guard de autenticación — redirige a `/login` si no hay
  token). En `App.jsx`, las 3 rutas privadas quedan
  `<RutaPrivada><LayoutAutenticado><Pagina /></LayoutAutenticado></RutaPrivada>`.
- **`frontend/src/constantes.js`** (modificado): se agrega
  `MENU_POR_ROL`, un objeto `{ estudiante: [...], profesor: [...], admin: [...] }`
  donde cada entrada es `{ etiqueta, ruta, disponible }`.
- **`frontend/src/styles.css`** (modificado): clases nuevas para la barra
  superior, el overlay, el drawer, y los ítems deshabilitados —
  mobile-first, reutilizando las variables CSS ya definidas
  (`--color-primario`, `--color-borde`, etc.).
- Sin estado global nuevo: el estado de abierto/cerrado del drawer es
  `useState` local a `LayoutAutenticado`. Los datos del usuario y
  `cerrarSesion()` ya vienen de `useAuth()` (Tanda anterior, `AuthContext.jsx`).

## Comportamiento

- Barra superior fija arriba: título de la app a la izquierda, ícono ☰ a
  la derecha.
- Tocar ☰ abre el drawer (panel lateral) con un overlay oscuro de fondo.
  Contenido del drawer, de arriba a abajo:
  1. Nombre y email del usuario, con un badge de rol. El backend expone
     `usuario.rol` como `estudiante`/`profesor`/`admin` (minúscula); el
     badge muestra la etiqueta capitalizada ("Estudiante"/"Profesor"/"Admin")
     vía un mapeo simple, mismo patrón que `EJES`/`etiquetaEje` en
     `Resultado.jsx` de la tanda anterior.
  2. Los links de `MENU_POR_ROL[usuario.rol]`: los `disponible: true`
     navegan (vía `react-router-dom`) y cierran el drawer; los
     `disponible: false` se ven visualmente deshabilitados (color
     apagado, sin cursor pointer) y no disparan ninguna acción al tocarlos.
  3. Separado del resto (ej. un borde superior), el botón "Cerrar sesión":
     llama a `useAuth().cerrarSesion()` y navega a `/login`.
- Cerrar el drawer: tocar el overlay, un botón ✕ en el drawer, o navegar
  por un link disponible (se cierra y navega en el mismo gesto).
- Si el rol del usuario no tiene entrada en `MENU_POR_ROL` (no debería
  pasar dado que el backend solo emite `estudiante`/`profesor`/`admin`),
  el drawer muestra solo los datos del usuario y "Cerrar sesión", sin
  links — no debe romper el render.

## Testing

Sin framework de testing automatizado de UI (misma decisión que la tanda
anterior). Verificación manual con `npm run dev` contra el backend ya
desplegado: abrir/cerrar el drawer, confirmar que muestra los datos
correctos del usuario logueado, que los links deshabilitados no navegan,
que el link activo de estudiante navega y cierra el drawer, y que "Cerrar
sesión" limpia la sesión y redirige a `/login`. Verificar además con un
usuario profesor y uno admin (registrados manualmente) que el badge de rol
y los links deshabilitados correspondientes se muestran bien.

## Despliegue

Mismo mecanismo que la tanda anterior: al terminar, reconstruir la imagen
`web` (`docker compose up -d --build web`) en el CT 118 de Proxmox y
verificar en `http://192.168.0.190/`.

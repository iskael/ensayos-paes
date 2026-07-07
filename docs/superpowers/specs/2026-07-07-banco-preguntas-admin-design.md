# Banco de preguntas (admin)

Fecha: 2026-07-07

## Contexto

El backend del Banco de preguntas ya está completo y funcionando (Fase 2/3 del
plan original): CRUD de exámenes fuente, CRUD de ítems con alternativas,
clave de pesos por examen, publicar/ocultar ítems, subida de imágenes e
importación asistida de PDF. Todas las rutas viven bajo `/api/v1/examenes`,
`/api/v1/items` e `/api/v1/imagenes`, protegidas con `RequerirRol(RolAdmin)`
en `backend/internal/http/router.go`.

El frontend no tiene ninguna pantalla que consuma estos endpoints. El link
"Banco de preguntas" en `MENU_POR_ROL.admin` (agregado en la tanda del menú
de usuario) existe pero está `disponible: false, ruta: null` porque esta
pantalla no existía. Esta tanda construye esa sección completa, incluyendo
la importación de PDF.

## Alcance

- CRUD de exámenes fuente (`ExamenFuente`).
- CRUD de ítems con sus 4 alternativas (`Item`/`Alternativa`).
- Clave de pesos por examen (validación de suma = 1000, RN-03).
- Publicar/ocultar ítems (validación de peso y alternativas, RN-04).
- Subida de imágenes (ítem y alternativas).
- Importación asistida de PDF (crea ítems en `borrador`).
- Activa el link "Banco de preguntas" en `MENU_POR_ROL.admin`.
- Redirección de `/` según rol: `admin` → `/banco/items`; estudiante sigue
  viendo `ConfigurarEnsayo` como hoy (el endpoint de crear ensayo es
  estudiante-only en el backend, por lo que un admin no puede usar esa
  pantalla).

Fuera de alcance: reportes/analítica para admin, edición masiva (bulk
actions) de ítems, drag-and-drop de imágenes (un input de archivo simple
basta), dashboard/reportes para profesor (queda para una tanda futura de
"Grupos").

## Arquitectura

### Rutas nuevas

Todas envueltas en `<RutaPrivada><LayoutAutenticado>...</LayoutAutenticado></RutaPrivada>`,
igual que el resto de rutas privadas. El backend ya rechaza con 403 si el rol
no es admin; el frontend no duplica esa validación (mismo criterio que el
resto del proyecto: el guard de rol vive en el backend, el frontend solo
oculta/muestra navegación).

```
/banco/items                  → BancoItems.jsx      (lista + filtros + paginado)
/banco/items/nuevo            → ItemForm.jsx        (crear)
/banco/items/:id              → ItemForm.jsx        (editar, mismo componente)
/banco/examenes               → BancoExamenes.jsx   (lista)
/banco/examenes/nuevo         → ExamenForm.jsx      (crear)
/banco/examenes/:id           → ExamenForm.jsx      (editar)
/banco/examenes/:id/clave     → ExamenClave.jsx     (pesos + importar PDF)
```

### Archivos nuevos

- `frontend/src/pages/BancoItems.jsx`
- `frontend/src/pages/ItemForm.jsx`
- `frontend/src/pages/BancoExamenes.jsx`
- `frontend/src/pages/ExamenForm.jsx`
- `frontend/src/pages/ExamenClave.jsx`
- `frontend/src/components/AlternativaCampos.jsx` — subcomponente usado solo
  dentro de `ItemForm` para cada una de las 4 filas de alternativa (texto,
  imagen, radio "correcta"). Evita duplicar ese bloque 4 veces dentro del
  formulario.

### Archivos modificados

- **`frontend/src/api.js`**: se agregan los siguientes métodos, mismo patrón
  `pedir()` ya existente (`llamar(token)` → fetch con `Authorization`):
  - `crearExamen(token, datos)` → `POST /examenes`
  - `listarExamenes(token, {limit, offset})` → `GET /examenes`
  - `obtenerExamen(token, id)` → `GET /examenes/:id`
  - `actualizarExamen(token, id, datos)` → `PUT /examenes/:id`
  - `eliminarExamen(token, id)` → `DELETE /examenes/:id`
  - `obtenerClave(token, examenId)` → `GET /examenes/:id/clave`
  - `definirClave(token, examenId, pesos)` → `PUT /examenes/:id/clave`
  - `importarPdf(token, examenId, formData)` → `POST /examenes/:id/importacion-pdf`
    (`FormData`, no JSON — `pedir()` necesita una variante que no fuerce
    `Content-Type: application/json` cuando el body es `FormData`)
  - `crearItem(token, datos)` → `POST /items`
  - `listarItems(token, filtros)` → `GET /items` (query string con nivel,
    eje, dificultad, estado, examenId, limit, offset)
  - `obtenerItem(token, id)` → `GET /items/:id`
  - `actualizarItem(token, id, datos)` → `PUT /items/:id`
  - `eliminarItem(token, id)` → `DELETE /items/:id`
  - `publicarItem(token, id)` → `POST /items/:id/publicar`
  - `ocultarItem(token, id)` → `POST /items/:id/ocultar`
  - `subirImagen(token, formData)` → `POST /imagenes` (`FormData`) → `{ url }`
- **`frontend/src/constantes.js`**:
  - `MENU_POR_ROL.admin` pasa de `[{ etiqueta: 'Banco de preguntas', ruta: null, disponible: false }]`
    a `[{ etiqueta: 'Banco de preguntas', ruta: '/banco/items', disponible: true }]`.
  - Se agrega `ESTADOS_ITEM = ['borrador', 'publicado', 'oculto']` y
    `TIPOS_EXAMEN = ['PAES_Regular', 'PAES_Invierno', 'PDT']` para poblar
    selects de filtro/formulario (mismo patrón que `NIVELES`/`CANTIDADES`).
- **`frontend/src/App.jsx`**: se agregan las 7 rutas nuevas. La ruta `/`
  cambia de `<ConfigurarEnsayo />` directo a un componente `InicioPorRol` que
  decide qué renderizar según `usuario.rol`.
- **`frontend/src/styles.css`**: clases nuevas para tabla/lista de ítems y
  exámenes, barra de filtros, filas de alternativa, indicador de suma de
  pesos (válida/inválida). Append-only, mismo patrón de siempre.

## Datos y contrato (ya definidos en `docs/openapi.yaml`)

```
ExamenInput: { nombre, anio_admision, tipo, nivel, edicion?, url_pdf?, fecha_publicacion? }
ExamenFuente: ExamenInput + { id }

ItemInput: { examen_fuente_id?, enunciado, imagen_url?, eje, nivel, dificultad,
             peso?, explicacion?, alternativas: AlternativaInput[4] }
Item: ItemInput + { id, origen, estado, fecha_creacion }
AlternativaInput: { etiqueta (A-D), texto, imagen_url?, es_correcta }

ClaveItemInput: { item_id, peso }
Clave: { examen_id, suma_pesos, valida, pesos: ClaveItemInput[] }

POST /imagenes (multipart, campo "archivo") → { url }
POST /examenes/:id/importacion-pdf (multipart: archivo, eje, dificultad) → Item[] (estado=borrador)
```

Reglas de dominio ya implementadas en el backend (no se reimplementan en el
frontend, solo se reflejan en la UI):
- `ValidarAlternativas` (`backend/internal/domain/item.go:33`): exactamente 4
  alternativas, etiquetas A-D sin repetir, exactamente una `es_correcta`.
- `publicarItem` (RN-04): exige `peso > 0` y alternativas válidas; si no,
  422 con mensaje.
- `definirClave` (RN-03): la suma de todos los pesos enviados debe ser 1000;
  si no, 422 con mensaje "La suma de los pesos debe ser 1000".
- `importarPdf`: los ítems extraídos quedan siempre en `borrador` sin
  alternativa correcta marcada — requieren revisión humana antes de publicar
  (ya bloqueado por `ValidarAlternativas`).

## Comportamiento

**`BancoExamenes.jsx`** (lista): tabla con nombre/tipo/nivel/año, botón
"Nuevo examen", cada fila con links a Editar y Clave. Sin paginado (los
exámenes fuente son pocos, a diferencia de los ítems).

**`ExamenForm.jsx`** (crear/editar): campos de `ExamenInput`. Al guardar,
vuelve a `/banco/examenes`. Botón "Eliminar" con confirmación
(`window.confirm`, mismo patrón simple ya usado en el resto del proyecto).

**`ExamenClave.jsx`**: carga `GET /examenes/:id/clave` (trae `pesos` actuales)
y la lista de ítems de ese examen (`GET /items?examenId=`). Por cada ítem del
examen, un input numérico de peso; muestra la suma en vivo y la resalta en
rojo si ≠ 1000. Botón "Guardar clave" hace `PUT /clave`; si el backend
devuelve 422 muestra el mensaje de error tal cual. Sección aparte "Importar
PDF": input de archivo + selects de eje/dificultad (default para todos los
ítems extraídos) + botón "Importar" → `POST /importacion-pdf` (máx. 20MB,
mismo límite que el backend); al terminar, navega a
`/banco/items?examenId=:id&estado=borrador` para revisar los ítems recién
creados.

**`BancoItems.jsx`** (lista): filtros (nivel, eje, dificultad, estado) +
paginado Anterior/Siguiente (offset-based, tamaño de página fijo de 20). Los
filtros iniciales se leen de la query string (`useSearchParams`) para
soportar el link que llega desde la importación de PDF. Cada fila: enunciado
truncado, eje, estado (badge), y acciones Editar / Publicar u Ocultar según
estado (`borrador`/`oculto` → botón "Publicar"; `publicado` → botón
"Ocultar"). Publicar hace `POST /publicar`; si el backend devuelve 422 se
muestra el mensaje de error en la fila.

**`ItemForm.jsx`** (crear/editar): enunciado (textarea, soporta LaTeX —
reutiliza `<Formula>` para previsualizar), selects de eje/nivel/dificultad,
imagen del ítem (input de archivo → `POST /imagenes` → guarda la `url`
devuelta en `imagen_url`), campo numérico de peso (opcional), examen fuente
(select opcional poblado desde `listarExamenes`), explicación (textarea
opcional), y 4 filas de `AlternativaCampos` (etiqueta fija A-D, texto con
preview LaTeX, imagen opcional, radio "es correcta" mutuamente excluyente).
Guarda con `POST`/`PUT` según sea crear/editar.

**Redirección de `/` por rol**: `InicioPorRol` (definido inline en
`App.jsx` o como componente chico en `components/`) lee `usuario.rol` de
`useAuth()` — si es `admin`, `<Navigate to="/banco/items" replace />`; si
no, `<ConfigurarEnsayo />`. No se toca el comportamiento de
estudiante/profesor.

## Testing

Sin framework de testing automatizado de UI (misma decisión de siempre).
Verificación manual con `npm run dev` contra el backend real, logueado como
el admin existente:
- Crear examen → crear ítem con las 4 alternativas → publicar (probar
  también el caso 422 sin peso asignado).
- Definir clave con suma≠1000 (ver error) y luego =1000 (ver éxito).
- Importar un PDF de prueba → revisar los ítems borrador resultantes.
- Ocultar un ítem publicado.
- Confirmar que un login de estudiante sigue cayendo en `ConfigurarEnsayo`
  en `/`, sin cambios de comportamiento.

## Despliegue

Mismo mecanismo que las tandas anteriores: reconstruir la imagen `web`
(`docker compose up -d --build web`) en el CT 118 de Proxmox tras el merge,
y verificar en `http://192.168.0.190/` (y `http://100.93.161.84/` vía
Tailscale).

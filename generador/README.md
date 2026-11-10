# Generador de ítems (v2, Modo A)

Genera ítems PAES de matemáticas por **plantillas parametrizadas**: la respuesta correcta y los
distractores se calculan por código, y cada distractor corresponde a un error típico. Reemplaza al
`prototipo-ia/` (4 plantillas) como fuente de ítems `generado`. Diseño: `docs/diseno_generacion_ia_v2.md`.

## Uso

```bash
cd generador
python3 generar.py                 # escribe salida/
python3 -m unittest test_generador # pruebas
```

Sin dependencias fuera de la biblioteca estándar. La prueba de render en KaTeX se salta si no existe
`frontend/node_modules/katex` (requiere `npm ci` en `frontend/`).

## Salida (`salida/`, no se versiona)

- `items.json` — ítems aprobados.
- `carga.sql` — inserta los ítems como `origen = generado`, `estado = borrador`. Es idempotente: no
  vuelve a insertar un enunciado que ya existe.
- `publicar.sql` — pasa a `publicado` los ítems de este lote que sigan en `borrador` (se aplica después de revisarlos).
- `muestra.html` — vista previa con fórmulas renderizadas, agrupada por eje y plantilla.
- `reporte.txt` — conteos por eje, dificultad y plantilla.

## Carga al banco

`POST /items` fija `origen = oficial`, así que los ítems generados se cargan por SQL:

```bash
docker compose exec -T db psql -U ensayos -d ensayos_paes -v ON_ERROR_STOP=1 < generador/salida/carga.sql
```

Quedan en `borrador` (RN-04): la publicación es una decisión humana desde el banco de preguntas.

## Cómo se valida cada ítem

1. **Estructural:** 3 distractores, 4 valores y 4 textos distintos, delimitadores `$` bien formados.
2. **Comprobación independiente:** cada plantilla entrega un predicado `comprobar(valor)` que verifica
   la respuesta contra el problema por otro camino (sustitución, enumeración de casos, evaluación
   numérica). La correcta debe cumplirlo y ningún distractor puede cumplirlo.
3. **Error típico obligatorio:** cada distractor declara el error que representa; la explicación del
   ítem lo informa por alternativa.

Una combinación de parámetros que hace coincidir dos alternativas se descarta y se sortea otra.

## Agregar una plantilla

Una función decorada con `@plantilla(eje, nivel)` que recibe un `random.Random` y devuelve una
`Propuesta` (o lanza `Descartar`). Formato de texto: fórmulas entre `$...$` (KaTeX), coma decimal
(`tex`), fracciones irreducibles (`frac`), montos con `pesos`. No usar `$` como signo de dinero ni
saltos de línea en el enunciado.

## Convenciones

- Cada plantilla aporta como máximo `OBJETIVO_POR_PLANTILLA` ítems, para que ninguna domine un eje.
- La semilla es fija: la misma versión del código produce el mismo lote.

## Repaso del lote del prototipo

`repaso_prototipo.py` corrige los 431 ítems que el prototipo dejó en el banco (redacción, formato,
valores exactos en vez de redondeados, explicación con errores típicos) sin cambiar qué etiqueta es la
correcta, porque hay ensayos rendidos que las referencian. Deja publicados 12 por plantilla y oculta
el resto. Lee `salida/antiguos.json` (exportación de los ítems publicados con sus alternativas) y
escribe `salida/repaso.sql`. Aplicado en producción el 2026-11-09.

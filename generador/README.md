# Generador de ítems (v2, Modo A)

Genera ítems PAES de matemáticas por **plantillas parametrizadas**: la respuesta correcta y los
distractores se calculan por código, y cada distractor corresponde a un error típico. Tiene 159
plantillas: 113 de M1 (28 de números, 25 de álgebra y funciones, 36 de geometría y 24 de
probabilidad y estadística) y 46 de M2; 48 de ellas llevan figura. Reemplaza al
`prototipo-ia/` (4 plantillas) como fuente de ítems `generado`. Diseño: `docs/diseno_generacion_ia_v2.md`.

## Uso

```bash
cd generador
python3 generar.py                 # escribe salida/
python3 -m unittest test_generador # pruebas
```

Sin dependencias de Python fuera de la biblioteca estándar. Para convertir las figuras a PNG se
necesita `rsvg-convert` (paquete `librsvg2-bin`). La prueba de render en KaTeX se salta si no existe
`frontend/node_modules/katex` (requiere `npm ci` en `frontend/`).

## Salida (`salida/`, no se versiona)

- `items.json` — ítems aprobados.
- `carga.sql` — inserta los ítems como `origen = generado`, `estado = borrador`. Es idempotente: no
  vuelve a insertar un enunciado que ya existe.
- `publicar.sql` — pasa a `publicado` los ítems de este lote que sigan en `borrador` (se aplica después de revisarlos).
- `figuras/` — una imagen PNG por figura distinta, con nombre `gen-<hash>.png`.
- `muestra.html` — vista previa con fórmulas renderizadas, agrupada por eje y plantilla.
- `reporte.txt` — conteos por eje, dificultad y plantilla.

## Carga al banco

`POST /items` fija `origen = oficial`, así que los ítems generados se cargan por SQL:

```bash
docker compose exec -T db psql -U ensayos -d ensayos_paes -v ON_ERROR_STOP=1 < generador/salida/carga.sql
```

Las figuras se copian antes al volumen de imágenes de la API; `carga.sql` guarda en `imagen_url` la
ruta relativa `/uploads/gen-<hash>.png` y también se la agrega a los ítems ya cargados que no la tenían:

```bash
docker compose cp generador/salida/figuras/. api:/app/uploads/
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

## Geometría modelada en PAES oficiales

`plantillas_geometria_paes.py` reúne 13 plantillas cuyos **tipos de pregunta** se tomaron de las PAES
M1 Regular e Invierno de admisión 2024 publicadas por el DEMRE: diagonal de un cuadrado, razón entre
áreas de círculos, altura de un cilindro dada su capacidad, área de superficie en términos de `x`,
suma de vectores con incógnita, composición de rotación y traslación, paso erróneo en una secuencia
de transformaciones isométricas, vector de traslación de un recorrido, aplicación de una fórmula
dada, área de un cuadrado con esquinas cubiertas, volumen al escalar las aristas, medida real desde
un plano a escala y distancia entre un punto y su reflejo. Se replica la habilidad evaluada con
contextos y números propios; no se copia ningún ítem. Quedan fuera los tipos que dependen de una
figura (gráficos de vectores, cuerpos compuestos, simetría de figuras), que requieren generar
imágenes y que el frontend las muestre.

Una plantilla con alternativas de orden natural ("En el Paso 1" … "En el Paso 4") usa
`orden_fijo=True` y no se baraja.

## Figuras

`figuras.py` dibuja en SVG (trazo negro, relleno gris, rótulos en serif) triángulos, rectángulos,
círculos, trapecios, plano cartesiano con puntos, rectas y vectores, cuadrículas, cajas, cilindros,
conos, figuras formadas por cuadrados y gráficos de barras. Una plantilla entrega la figura en
`Propuesta.figura`; construirla no debe consumir números aleatorios, para no alterar los ítems que la
plantilla ya generaba. Dos ítems pueden compartir enunciado si su figura es distinta.

`plantillas_figuras.py` reúne 16 plantillas modeladas en tipos de pregunta de las PAES M1 de admisión
2023 a 2026: 9 de geometría con figura, 5 de tipos recientes sin figura y 2 de gráficos de barras.

## Números y álgebra modelados en PAES oficiales

`plantillas_numeros_paes.py` y `plantillas_algebra_paes.py` agregan 12 plantillas por eje, con tipos
tomados de las PAES M1 de admisión 2024 a 2026: compras con precios por unidad de medida, porcentaje
de un porcentaje, descuentos sucesivos como expresión, fracción de lo que faltaba, razones,
conversiones, paso erróneo en operaciones combinadas; reducción con paréntesis, factor que falta,
expresiones de dinero y de perímetro, funciones que modelan un estanque o un costo rebajado,
desigualdades de meta y de suscripción, y simetría de la parábola (con figura).

`plantillas_numeros_figuras.py` agrega 5 plantillas de números con figura (PAES M1 2023–2026): punto en la recta
numérica, parte sombreada de un rectángulo, compra desde una tabla de precios, variación porcentual desde un gráfico de
barras y diferencia de temperaturas desde una tabla.

`figuras_prototipo.py` agrega figura a los 12 ítems publicados de área de triángulo del prototipo: lee
`salida/triangulos.txt` (enunciados exportados del banco) y escribe `salida/figuras_prototipo.sql` y las imágenes en
`salida/figuras_prototipo/`. Aplicado en producción el 2026-11-11.

## Probabilidad y estadística modeladas en PAES oficiales

`plantillas_probabilidad_paes.py` agrega 13 plantillas con tipos tomados de las PAES M1 de admisión
2023 a 2026: total de datos y mediana desde una tabla, probabilidad desde una tabla simple y de doble
entrada, promedio como expresión, crecimiento promedio, pago más frecuente desde un gráfico, monedas,
puntaje de un juego, dado cargado, diagrama de cajón y cajas con bolitas. Las tablas van como figura
(`figuras.tabla`), porque el enunciado es texto plano y no admite tablas.

## Modelo de prueba de admisión 2023

`plantillas_modelo_2023.py` agrega 16 plantillas con tipos del Modelo de Prueba de Matemática de admisión 2023 (el mismo
que comenta la "Resolución modelo de prueba matemática 2022" del DEMRE): vasos llenados hasta una fracción, masa con
números mixtos, descripción verbal de un porcentaje, tiempo de la luz con notación científica; capacidad desde dos
fracciones, masa máxima con una diferencia, lados consecutivos desde el área, parámetro para dos soluciones reales, cobro
con recargo sobre un umbral, cuadrática desde el máximo y un punto; escalera que se desliza, área no barrida por dos
plumillas (con figura); promedio de aportes en razón, afirmación que se deduce de un percentil (verificada contra todos
los conjuntos de 6 datos entre 1 y 4) y, en M2, elegir de varios grupos y colorear en fila sin repetir vecinos.

## Nivel M2

`plantillas_m2.py` cubre los contenidos propios del temario de Competencia Matemática 2 (DEMRE,
admisión 2026), con tipos tomados de las PAES M2 de 2024 a 2026: logaritmos, interés compuesto,
orden de números con raíces, potencias de exponente fraccionario; sistemas sin solución o con
infinitas soluciones, crecimiento y decaimiento exponencial, traslación de parábolas, funciones
seno y coseno; razones trigonométricas, homotecia, ángulo inscrito y central, cuerdas que se cortan;
combinatoria, permutaciones, probabilidad condicional, binomial y total. Quedan fuera las preguntas
de suficiencia de datos, que se agregaron después en `plantillas_suficiencia.py` (ver más abajo).

`plantillas_m2_paes.py` agrega 20 plantillas M2 (5 por eje) con tipos de las PAES M2 de invierno 2025, regular 2025 e
invierno 2026: punto que divide un intervalo en una razón, interés generado, valor inicial tras variaciones sucesivas,
cambio de base con logaritmos aproximados, intensidad sonora; vértice con parámetro, altura máxima de un lanzamiento,
reflexión de una parábola, función potencia al escalar la variable, dos cultivos que se duplican; altura y proyección
sobre la hipotenusa, área entre un círculo y un polígono inscrito, rotación de un punto, tangente y secante, homotecia
de razón negativa; condicional desde "ambos" y "solo uno", lotería, orden al azar con condición en los extremos,
transformación lineal de los datos y ganancia esperada.

## Suficiencia de datos (5 alternativas)

`plantillas_suficiencia.py` genera preguntas M2 de suficiencia de datos con las cinco alternativas oficiales en orden fijo
(A a E). La clave se calcula enumerando un dominio finito de casos y se confirma en un dominio más amplio; la explicación da
un contraejemplo por cada afirmación que no basta. Hay una plantilla por eje: valor de una expresión en $x$ e $y$, medidas
de un rectángulo, probabilidad en una urna y número entero por condiciones. Requiere la migración `0004_alternativa_e`.

## Convenciones

- Cada plantilla aporta como máximo `OBJETIVO_POR_PLANTILLA` ítems, para que ninguna domine un eje.
- La semilla es fija: la misma versión del código produce el mismo lote.

## Repaso del lote del prototipo

`repaso_prototipo.py` corrige los 431 ítems que el prototipo dejó en el banco (redacción, formato,
valores exactos en vez de redondeados, explicación con errores típicos) sin cambiar qué etiqueta es la
correcta, porque hay ensayos rendidos que las referencian. Deja publicados 12 por plantilla y oculta
el resto. Lee `salida/antiguos.json` (exportación de los ítems publicados con sus alternativas) y
escribe `salida/repaso.sql`. Aplicado en producción el 2026-11-09.

# Diseño — Generación de ítems con IA (v2)

> Diseño cerrado para la v2. La **implementación queda en v2**; el prototipo offline (`genera_preguntas.py`) ya permite medir calidad sin tocar el scope del MVP.

---

## 1. Objetivo y principios

- Ampliar el banco con ítems nuevos por eje/nivel/dificultad, manteniendo el estilo PAES.
- **Correctitud > volumen.** Un ítem incorrecto publicado daña más la confianza que la falta de variedad.
- **Revisión humana obligatoria** antes de publicar (ya en HU-32; nunca se autopublica).
- **Solo ítems de texto al inicio.** Las figuras (geometría/estadística con imagen) quedan para después, coherente con la decisión "figuras como imágenes".

## 2. Estrategia de generación (dos modos)

**Modo A — Variaciones por plantilla parametrizada (recomendado para arrancar)**
- Plantillas con parámetros aleatorios; la **respuesta correcta y los distractores se calculan por código**.
- Correctitud garantizada por construcción. El LLM, si se usa, solo **naturaliza la redacción**.
- Distractores diseñados a partir de **errores típicos** (olvidar dividir, error de signo, confundir media con mediana, etc.) → pedagógicamente útiles.

**Modo B — Generación libre con LLM + verificación (fase posterior)**
- El LLM crea el ítem desde cero por eje/nivel/dificultad.
- Más flexible y variado, pero **mayor riesgo** de ambigüedad o respuesta mal marcada.
- Solo se habilita una vez validado el pipeline con el Modo A.

## 3. Pipeline de validación (capas)

1. **Estructural:** exactamente 4 alternativas (A–D), una sola correcta, todas distintas.
2. **Simbólica (sympy):** re-deriva la respuesta de forma independiente y la compara con la marcada; verifica que ningún distractor coincida con la correcta y que los valores sean válidos.
3. **Crítica con LLM (opcional):** revisa ambigüedad del enunciado, unicidad de la respuesta y alineación al temario.
4. **Aprobación humana (gate final):** el admin revisa, edita y aprueba/rechaza. Solo entonces pasa a `publicado`.

## 4. Estados y flujo en la app

- `generado` → se crea como **`borrador`** (mismo flujo que la carga por PDF).
- Pasa por las capas 1–3 automáticas; las que fallan se descartan o se marcan.
- Revisión humana → `publicado` o `rechazado`.
- El ítem conserva `origen = generado` (transparencia hacia el estudiante, HU-33).

## 5. Encaje con lo ya diseñado

- **No cambia nada del MVP.** El modelo ya contempla `origen=generado`, `estado=borrador` y el campo `peso`.
- A los ítems generados se les asigna un `peso` por defecto (el admin puede ajustarlo), ya que no provienen de la clave de un examen oficial.

## 6. Alcance sugerido para v2 (incremental)

- **Fase 1:** Modo A en ejes **Números** y **Álgebra y Funciones** (los más verificables simbólicamente).
- **Fase 2:** plantillas acotadas de **Geometría** y **Probabilidad/Estadística** sin figura.
- **Fase 3 (evaluar):** Modo B con verificación, e ítems con figura.

## 7. Métricas de calidad (medibles con el prototipo)

- **Tasa de aprobación** (aprobados / generados).
- **% verificados simbólicamente** sin intervención.
- **Validez de distractores** (distintos, ninguno igual a la correcta).
- Resultado actual del prototipo: ver `reporte_calidad.txt` (rechaza automáticamente colisiones de valores).

## 8. Decisión: ahora vs v2

- **Implementación → v2.** No está en la ruta crítica; el banco oficial DEMRE basta para lanzar y validar el producto.
- **Ahora →** diseño cerrado (este documento) + **prototipo offline** para medir calidad y afinar el approach sin riesgo para el MVP.

## 9. Riesgos y mitigaciones

- *Respuesta mal marcada / ambigüedad* → Modo A (cálculo por código) + verificación simbólica + revisión humana.
- *Distractores inválidos* → generación basada en errores típicos + chequeo de unicidad.
- *Figuras* → excluidas al inicio (solo texto).
- *Costos/latencia del LLM* → el Modo A funciona sin LLM; el LLM es opcional para redacción.

## 10. Prototipo offline

- Archivo: `genera_preguntas.py` (sympy, sin dependencias de la app).
- Genera ítems por plantilla, los valida (estructural + simbólico) y produce:
  - `preguntas_generadas.json` — ítems aprobados (formato alineado al modelo del MVP).
  - `reporte_calidad.txt` — métricas de calidad.
- Sirve para iterar plantillas y estrategias de distractores antes de construir el módulo real en v2.

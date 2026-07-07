#!/usr/bin/env python3
"""
Prototipo offline de generacion de items PAES (v2) - lote 2.

Mismas 4 plantillas parametrizadas que genera_preguntas.py, con rangos de
parametros mas amplios (para soportar ~100 items unicos por eje sin agotar
las combinaciones posibles) y deduplicacion contra los items ya generados
en el lote 1 (preguntas_generadas.json), para no repetir enunciados.

Uso:
    python3 genera_preguntas_lote2.py
"""
from __future__ import annotations
import json
import random
from dataclasses import dataclass, field, asdict
from fractions import Fraction
from pathlib import Path

SEMILLA = 2026
OBJETIVO_POR_PLANTILLA = 100
LIMITE_INTENTOS_POR_PLANTILLA = 5000
LOTE1_JSON = Path("preguntas_generadas.json")
OUT_JSON = Path("preguntas_generadas_lote2.json")
OUT_REPORTE = Path("reporte_calidad_lote2.txt")

ETIQUETAS = ["A", "B", "C", "D"]


def fmt(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    f = float(v)
    return f"{f:.2f}".rstrip("0").rstrip(".")


@dataclass
class Item:
    eje: str
    nivel: str
    dificultad: str
    enunciado: str
    alternativas: list[dict]
    respuesta_correcta: str
    explicacion: str
    origen: str = "generado"
    estado: str = "borrador"
    meta: dict = field(default_factory=dict)


def armar_item(eje, nivel, dificultad, enunciado, correcto, distractores,
               explicacion, meta) -> Item | None:
    valores = [correcto] + distractores
    if len(set(valores)) != 4:
        return None
    random.shuffle(valores)
    alternativas = []
    correcta_label = None
    for et, val in zip(ETIQUETAS, valores):
        es_c = (val == correcto)
        if es_c:
            correcta_label = et
        alternativas.append({"etiqueta": et, "texto": fmt(val), "es_correcta": es_c})
    meta = {**meta, "valor_correcto": fmt(correcto)}
    return Item(eje, nivel, dificultad, enunciado, alternativas,
                correcta_label, explicacion, meta=meta)


# ---------- Plantillas (rangos ampliados respecto al lote 1) ----------

def plantilla_porcentaje() -> Item | None:
    base = random.choice(list(range(100, 5001, 100)))
    pct = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70])
    dificultad = "baja" if pct <= 25 else "media"
    correcto = Fraction(base * pct, 100)
    distractores = [
        Fraction(base * pct, 10),
        Fraction(base * (100 - pct), 100),
        Fraction(base * (pct + 10), 100),
    ]
    enun = f"En una tienda, un producto de ${base} tiene un {pct}% de descuento. Cuanto dinero corresponde al descuento?"
    expl = f"El {pct}% de {base} es {base} * {pct}/100 = {fmt(correcto)}."
    return armar_item("numeros", "M1", dificultad, enun, correcto, distractores, expl,
                      {"plantilla": "porcentaje", "base": base, "pct": pct})


def plantilla_ecuacion_lineal() -> Item | None:
    a = random.choice(list(range(2, 13)))
    x_real = random.choice(list(range(2, 21)))
    b = random.choice(list(range(1, 21)))
    c = a * x_real + b
    dificultad = "media" if a <= 6 else "alta"
    correcto = Fraction(c - b, a)
    distractores = [
        Fraction(c + b, a),
        Fraction(c - b, 1),
        Fraction(b - c, a),
    ]
    enun = f"Resuelve la ecuacion: {a}x + {b} = {c}. Cual es el valor de x?"
    expl = f"{a}x = {c} - {b} = {c-b}; x = {c-b}/{a} = {fmt(correcto)}."
    return armar_item("algebra_funciones", "M1", dificultad, enun, correcto, distractores, expl,
                      {"plantilla": "ecuacion_lineal", "a": a, "b": b, "c": c})


def plantilla_area_triangulo() -> Item | None:
    base = random.choice(list(range(4, 41, 2)))
    altura = random.choice(list(range(3, 31, 2)))
    dificultad = "baja" if base <= 20 and altura <= 15 else "media"
    correcto = Fraction(base * altura, 2)
    distractores = [
        Fraction(base * altura, 1),
        Fraction(base + altura, 1),
        Fraction(base * altura, 4),
    ]
    enun = f"Un triangulo tiene base {base} cm y altura {altura} cm. Cual es su area en cm2?"
    expl = f"Area = base * altura / 2 = {base} * {altura} / 2 = {fmt(correcto)} cm2."
    return armar_item("geometria", "M1", dificultad, enun, correcto, distractores, expl,
                      {"plantilla": "area_triangulo", "base": base, "altura": altura})


def plantilla_media() -> Item | None:
    n = random.choice([5, 6, 7])
    datos = [random.choice(range(1, 50)) for _ in range(n)]
    s = sum(datos)
    correcto = Fraction(s, n)
    datos_ord = sorted(datos)
    mediana = Fraction(datos_ord[n // 2], 1)
    distractores = [
        mediana,
        Fraction(s, 1),
        Fraction(s, n - 1),
    ]
    dificultad = "media" if n <= 6 else "alta"
    enun = f"Dado el conjunto de datos {datos}, cual es el promedio (media aritmetica)?"
    expl = f"Media = ({' + '.join(map(str, datos))}) / {n} = {s}/{n} = {fmt(correcto)}."
    return armar_item("probabilidad_estadistica", "M1", dificultad, enun, correcto, distractores, expl,
                      {"plantilla": "media", "datos": datos, "n": n})


PLANTILLAS = [
    plantilla_porcentaje,
    plantilla_ecuacion_lineal,
    plantilla_area_triangulo,
    plantilla_media,
]


# ---------- Verificacion (misma logica que el lote 1) ----------

def verifica_independiente(item: Item) -> tuple[bool, str]:
    m = item.meta
    p = m["plantilla"]
    if p == "porcentaje":
        esperado = Fraction(m["base"] * m["pct"], 100)
    elif p == "ecuacion_lineal":
        esperado = Fraction(m["c"] - m["b"], m["a"])
    elif p == "area_triangulo":
        esperado = Fraction(m["base"] * m["altura"], 2)
    elif p == "media":
        esperado = Fraction(sum(m["datos"]), len(m["datos"]))
    else:
        return False, "plantilla desconocida"
    if fmt(esperado) != m["valor_correcto"]:
        return False, "respuesta marcada no coincide con re-derivacion"
    return True, "ok"


def valida(item: Item) -> tuple[bool, list[str]]:
    fallas = []
    if len(item.alternativas) != 4:
        fallas.append("no tiene 4 alternativas")
    correctas = [a for a in item.alternativas if a["es_correcta"]]
    if len(correctas) != 1:
        fallas.append("no hay exactamente una alternativa correcta")
    textos = [a["texto"] for a in item.alternativas]
    if len(set(textos)) != 4:
        fallas.append("alternativas no son distintas")
    ok, msg = verifica_independiente(item)
    if not ok:
        fallas.append(f"verificacion simbolica: {msg}")
    return (len(fallas) == 0), fallas


def cargar_enunciados_previos() -> set[str]:
    if not LOTE1_JSON.exists():
        return set()
    with LOTE1_JSON.open(encoding="utf-8") as f:
        datos = json.load(f)
    return {d["enunciado"] for d in datos}


def main():
    random.seed(SEMILLA)
    enunciados_vistos = cargar_enunciados_previos()
    print(f"Enunciados previos cargados (lote 1): {len(enunciados_vistos)}")

    aprobados: list[Item] = []
    rechazados: list[str] = []
    duplicados = 0

    for plantilla in PLANTILLAS:
        aprobados_plantilla = 0
        intentos = 0
        while aprobados_plantilla < OBJETIVO_POR_PLANTILLA and intentos < LIMITE_INTENTOS_POR_PLANTILLA:
            intentos += 1
            item = plantilla()
            if item is None:
                rechazados.append("colision de valores")
                continue
            if item.enunciado in enunciados_vistos:
                duplicados += 1
                continue
            ok, fallas = valida(item)
            if not ok:
                rechazados.append(", ".join(fallas))
                continue
            enunciados_vistos.add(item.enunciado)
            aprobados.append(item)
            aprobados_plantilla += 1
        print(f"{plantilla.__name__}: {aprobados_plantilla}/{OBJETIVO_POR_PLANTILLA} en {intentos} intentos")

    salida = [{k: v for k, v in asdict(i).items() if k != "meta"} for i in aprobados]
    OUT_JSON.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    por_eje = {}
    for i in aprobados:
        por_eje[i.eje] = por_eje.get(i.eje, 0) + 1

    lineas = [
        "REPORTE DE CALIDAD - Prototipo de generacion PAES (lote 2)",
        "=" * 58,
        f"Semilla: {SEMILLA}",
        f"Objetivo por plantilla: {OBJETIVO_POR_PLANTILLA}",
        f"Total aprobados: {len(aprobados)}",
        f"Rechazados (validacion/colision): {len(rechazados)}",
        f"Duplicados contra lote 1: {duplicados}",
        "",
        "Por eje:",
    ]
    for eje, n in sorted(por_eje.items()):
        lineas.append(f"  - {eje}: {n} aprobados")

    reporte = "\n".join(lineas)
    OUT_REPORTE.write_text(reporte + "\n", encoding="utf-8")
    print("\n" + reporte)
    print(f"\n-> {OUT_JSON}  ({len(aprobados)} items)")
    print(f"-> {OUT_REPORTE}")


if __name__ == "__main__":
    main()

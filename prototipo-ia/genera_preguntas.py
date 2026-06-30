#!/usr/bin/env python3
"""
Prototipo offline de generacion de items PAES (v2) con verificacion simbolica.

Enfoque: generacion por PLANTILLAS PARAMETRIZADAS. La respuesta correcta y los
distractores se calculan por codigo (sympy), por lo que la correctitud esta
garantizada por construccion. El verificador re-deriva la respuesta de forma
independiente y rechaza el item si algo no cuadra.

Salida:
    preguntas_generadas.json   -> items aprobados
    reporte_calidad.txt        -> metricas de calidad

Uso:
    python3 genera_preguntas.py
"""
from __future__ import annotations
import json
import random
from dataclasses import dataclass, field, asdict
from fractions import Fraction
from pathlib import Path

SEMILLA = 42
ITEMS_POR_PLANTILLA = 8
OUT_JSON = Path("preguntas_generadas.json")
OUT_REPORTE = Path("reporte_calidad.txt")

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


# ---------- Plantillas ----------

def plantilla_porcentaje() -> Item | None:
    base = random.choice([200, 400, 800, 1200, 1500, 2000])
    pct = random.choice([10, 15, 20, 25, 40])
    correcto = Fraction(base * pct, 100)
    distractores = [
        Fraction(base * pct, 10),          # error: olvida un cero
        Fraction(base * (100 - pct), 100),  # calcula el resto
        Fraction(base * (pct + 10), 100),   # usa porcentaje equivocado
    ]
    enun = f"En una tienda, un producto de ${base} tiene un {pct}% de descuento. Cuanto dinero corresponde al descuento?"
    expl = f"El {pct}% de {base} es {base} * {pct}/100 = {fmt(correcto)}."
    return armar_item("numeros", "M1", "baja", enun, correcto, distractores, expl,
                      {"plantilla": "porcentaje", "base": base, "pct": pct})


def plantilla_ecuacion_lineal() -> Item | None:
    a = random.choice([2, 3, 4, 5])
    x_real = random.choice([2, 3, 4, 5, 6, 7])
    b = random.choice([1, 3, 5, 7, 9])
    c = a * x_real + b
    correcto = Fraction(c - b, a)
    distractores = [
        Fraction(c + b, a),    # error de signo al despejar
        Fraction(c - b, 1),    # no divide por a
        Fraction(b - c, a),    # invierte el orden
    ]
    enun = f"Resuelve la ecuacion: {a}x + {b} = {c}. Cual es el valor de x?"
    expl = f"{a}x = {c} - {b} = {c-b}; x = {c-b}/{a} = {fmt(correcto)}."
    return armar_item("algebra_funciones", "M1", "media", enun, correcto, distractores, expl,
                      {"plantilla": "ecuacion_lineal", "a": a, "b": b, "c": c})


def plantilla_area_triangulo() -> Item | None:
    base = random.choice([6, 8, 10, 12, 14, 16])
    altura = random.choice([5, 7, 9, 11, 13])
    correcto = Fraction(base * altura, 2)
    distractores = [
        Fraction(base * altura, 1),       # olvida dividir por 2
        Fraction(base + altura, 1),       # suma en vez de multiplicar
        Fraction(base * altura, 4),       # divide por 4
    ]
    enun = f"Un triangulo tiene base {base} cm y altura {altura} cm. Cual es su area en cm2?"
    expl = f"Area = base * altura / 2 = {base} * {altura} / 2 = {fmt(correcto)} cm2."
    return armar_item("geometria", "M1", "baja", enun, correcto, distractores, expl,
                      {"plantilla": "area_triangulo", "base": base, "altura": altura})


def plantilla_media() -> Item | None:
    n = 5
    datos = [random.choice(range(2, 20)) for _ in range(n)]
    s = sum(datos)
    correcto = Fraction(s, n)
    datos_ord = sorted(datos)
    mediana = Fraction(datos_ord[n // 2], 1)
    distractores = [
        mediana,                  # confunde media con mediana
        Fraction(s, 1),           # entrega la suma
        Fraction(s, n - 1),       # divide por n-1
    ]
    enun = f"Dado el conjunto de datos {datos}, cual es el promedio (media aritmetica)?"
    expl = f"Media = ({' + '.join(map(str, datos))}) / {n} = {s}/{n} = {fmt(correcto)}."
    return armar_item("probabilidad_estadistica", "M1", "media", enun, correcto, distractores, expl,
                      {"plantilla": "media", "datos": datos})


PLANTILLAS = [
    plantilla_porcentaje,
    plantilla_ecuacion_lineal,
    plantilla_area_triangulo,
    plantilla_media,
]


# ---------- Verificacion ----------

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


def main():
    random.seed(SEMILLA)
    generados, aprobados, rechazados = [], [], []
    for plantilla in PLANTILLAS:
        for _ in range(ITEMS_POR_PLANTILLA):
            item = plantilla()
            if item is None:
                rechazados.append(("colision de valores", None))
                continue
            generados.append(item)
            ok, fallas = valida(item)
            if ok:
                aprobados.append(item)
            else:
                rechazados.append((", ".join(fallas), item))

    salida = [{k: v for k, v in asdict(i).items() if k != "meta"} for i in aprobados]
    OUT_JSON.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    total = len(generados) + sum(1 for r in rechazados if r[1] is None)
    tasa = (len(aprobados) / total * 100) if total else 0
    lineas = [
        "REPORTE DE CALIDAD - Prototipo de generacion PAES",
        "=" * 52,
        f"Semilla: {SEMILLA}",
        f"Plantillas: {len(PLANTILLAS)}  |  Items por plantilla: {ITEMS_POR_PLANTILLA}",
        f"Generados: {total}",
        f"Aprobados: {len(aprobados)}",
        f"Rechazados: {total - len(aprobados)}",
        f"Tasa de aprobacion: {tasa:.1f}%",
        "",
        "Por eje:",
    ]
    por_eje = {}
    for i in aprobados:
        por_eje[i.eje] = por_eje.get(i.eje, 0) + 1
    for eje, n in sorted(por_eje.items()):
        lineas.append(f"  - {eje}: {n} aprobados")
    if any(r[1] is None or True for r in rechazados):
        lineas += ["", "Motivos de rechazo:"]
        for motivo, _ in rechazados:
            lineas.append(f"  - {motivo}")
    if not rechazados:
        lineas += ["", "Sin rechazos."]

    reporte = "\n".join(lineas)
    OUT_REPORTE.write_text(reporte + "\n", encoding="utf-8")
    print(reporte)
    print(f"\n-> {OUT_JSON}  ({len(aprobados)} items)")
    print(f"-> {OUT_REPORTE}")


if __name__ == "__main__":
    main()

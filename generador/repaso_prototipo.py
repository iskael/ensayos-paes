#!/usr/bin/env python3
"""Repaso de los ítems del prototipo (4 plantillas, julio 2026) que ya están en el banco.

Reescribe enunciado, alternativas y explicación con el formato del generador, sin cambiar qué
alternativa es correcta ni el valor de ninguna etiqueta (hay ensayos rendidos que las referencian).
Deja publicados PUBLICADOS_POR_PLANTILLA ítems por plantilla y oculta el resto.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

from nucleo import _es_decimal_finito, m, pesos, tex

PUBLICADOS_POR_PLANTILLA = 12

SALIDA = Path(__file__).parent / "salida"
IN_JSON = SALIDA / "antiguos.json"
OUT_SQL = SALIDA / "repaso.sql"


def fmt_prototipo(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):.2f}".rstrip("0").rstrip(".")


def porcentaje(enunciado):
    r = re.fullmatch(r"En una tienda, un producto de \$(\d+) tiene un (\d+)% de descuento\. Cuanto dinero corresponde al descuento\?", enunciado)
    if not r:
        return None
    base, pct = map(int, r.groups())
    correcto = Fraction(base * pct, 100)
    return {
        "plantilla": "prototipo_porcentaje",
        "enunciado": f"En una tienda, un producto de {pesos(base)} tiene un {pct} % de descuento. ¿Cuánto dinero corresponde al descuento?",
        "pasos": f"El {pct} % de {pesos(base)} es ${base} \\cdot \\frac{{{pct}}}{{100}} = {tex(correcto)}$ pesos.",
        "valores": [
            (correcto, None),
            (Fraction(base * pct, 10), "divide por 10 en vez de por 100 al calcular el porcentaje"),
            (Fraction(base * (100 - pct), 100), "calcula lo que se paga después del descuento, no el descuento"),
            (Fraction(base * (pct + 10), 100), f"calcula el {pct + 10} % en vez del {pct} %"),
        ],
        "texto": lambda v: pesos(int(v)) if v.denominator == 1 else f"$\\text{{\\textdollar}}\\,{tex(v)}$",
        "bonito": True,
    }


def ecuacion(enunciado):
    r = re.fullmatch(r"Resuelve la ecuacion: (\d+)x \+ (\d+) = (\d+)\. Cual es el valor de x\?", enunciado)
    if not r:
        return None
    a, b, c = map(int, r.groups())
    correcto = Fraction(c - b, a)
    return {
        "plantilla": "prototipo_ecuacion_lineal",
        "enunciado": f"¿Cuál es el valor de $x$ en la ecuación ${a}x + {b} = {c}$?",
        "pasos": f"Se resta {b} a ambos lados: ${a}x = {c - b}$. Al dividir por {a} se obtiene $x = {tex(correcto)}$.",
        "valores": [
            (correcto, None),
            (Fraction(c + b, a), f"suma {b} en vez de restarlo al despejar"),
            (Fraction(c - b, 1), f"resta {b} pero no divide por {a}"),
            (Fraction(b - c, a), "resta en el orden inverso y obtiene el signo contrario"),
        ],
        "texto": m,
        "bonito": True,
    }


def triangulo(enunciado):
    r = re.fullmatch(r"Un triangulo tiene base (\d+) cm y altura (\d+) cm\. Cual es su area en cm2\?", enunciado)
    if not r:
        return None
    base, altura = map(int, r.groups())
    correcto = Fraction(base * altura, 2)
    return {
        "plantilla": "prototipo_area_triangulo",
        "enunciado": f"Un triángulo tiene una base de {base} cm y una altura de {altura} cm. ¿Cuál es su área?",
        "pasos": f"El área es $\\frac{{\\text{{base}} \\cdot \\text{{altura}}}}{{2}} = \\frac{{{base} \\cdot {altura}}}{{2}} = {tex(correcto)}$ cm².",
        "valores": [
            (correcto, None),
            (Fraction(base * altura), "multiplica base por altura y olvida dividir por 2"),
            (Fraction(base + altura), "suma la base y la altura en vez de multiplicarlas"),
            (Fraction(base * altura, 4), "divide por 4 en vez de por 2"),
        ],
        "texto": lambda v: f"${tex(v)}\\ \\text{{cm}}^{{2}}$",
        "bonito": True,
    }


def media(enunciado):
    r = re.fullmatch(r"Dado el conjunto de datos \[([\d, ]+)\], cual es el promedio \(media aritmetica\)\?", enunciado)
    if not r:
        return None
    datos = [int(x) for x in r.group(1).split(",")]
    n, s = len(datos), sum(datos)
    correcto = Fraction(s, n)
    return {
        "plantilla": "prototipo_media",
        "enunciado": f"Los datos de un conjunto son: {', '.join(map(str, datos))}. ¿Cuál es su media aritmética (promedio)?",
        "pasos": f"Se suman los datos y se divide por la cantidad: $\\frac{{{' + '.join(map(str, datos))}}}{{{n}}} = \\frac{{{s}}}{{{n}}}"
                 + (f" = {tex(correcto)}$." if tex(correcto) != f"\\frac{{{s}}}{{{n}}}" else "$."),
        "valores": [
            (correcto, None),
            (Fraction(sorted(datos)[n // 2]), "entrega la mediana (el dato central) en vez de la media"),
            (Fraction(s), "suma los datos pero no divide por la cantidad"),
            (Fraction(s, n - 1), f"divide por {n - 1} en vez de por {n}"),
        ],
        "texto": m,
        "bonito": _es_decimal_finito(correcto.denominator),
    }


PLANTILLAS = [porcentaje, ecuacion, triangulo, media]


def repasar(item: dict) -> dict | None:
    for plantilla in PLANTILLAS:
        datos = plantilla(item["enunciado"])
        if datos:
            break
    else:
        return None
    por_texto_viejo = {}
    for valor, error in datos["valores"]:
        por_texto_viejo.setdefault(fmt_prototipo(valor), []).append((valor, error))
    alternativas, errores = [], []
    for alt in item["alternativas"]:
        candidatos = por_texto_viejo.get(alt["texto"], [])
        if len(candidatos) != 1:
            return None
        valor, error = candidatos[0]
        if (error is None) != alt["es_correcta"]:
            return None
        alternativas.append({"id": alt["id"], "texto": datos["texto"](valor)})
        if error:
            errores.append(f"{alt['etiqueta']}) {error}")
    if len({a["texto"] for a in alternativas}) != 4 or len(errores) != 3:
        return None
    return {
        "id": item["id"],
        "plantilla": datos["plantilla"],
        "dificultad": item["dificultad"],
        "bonito": datos["bonito"],
        "enunciado": datos["enunciado"],
        "explicacion": f"{datos['pasos']} Errores frecuentes: {'; '.join(errores)}.",
        "alternativas": alternativas,
    }


def elegir_publicados(repasados: list[dict]) -> set[str]:
    elegidos = set()
    for plantilla in sorted({r["plantilla"] for r in repasados}):
        candidatos = sorted((r for r in repasados if r["plantilla"] == plantilla and r["bonito"]), key=lambda r: r["id"])
        por_dificultad = {}
        for r in candidatos:
            por_dificultad.setdefault(r["dificultad"], []).append(r)
        colas = [por_dificultad[d] for d in sorted(por_dificultad)]
        tomados = 0
        while tomados < PUBLICADOS_POR_PLANTILLA and any(colas):
            for cola in colas:
                if cola and tomados < PUBLICADOS_POR_PLANTILLA:
                    elegidos.add(cola.pop(0)["id"])
                    tomados += 1
    return elegidos


def _sql(texto: str) -> str:
    return "'" + texto.replace("'", "''") + "'"


def main():
    items = json.loads(IN_JSON.read_text(encoding="utf-8"))
    repasados, sin_repaso = [], []
    for it in items:
        r = repasar(it)
        (repasados if r else sin_repaso).append(r or it)
    publicados = elegir_publicados(repasados)
    lineas = ["BEGIN;"]
    for r in repasados:
        lineas.append(f"UPDATE items SET enunciado = {_sql(r['enunciado'])}, explicacion = {_sql(r['explicacion'])}, "
                      f"estado = '{'publicado' if r['id'] in publicados else 'oculto'}' WHERE id = '{r['id']}';")
        for a in r["alternativas"]:
            lineas.append(f"UPDATE alternativas SET texto = {_sql(a['texto'])} WHERE id = '{a['id']}';")
    for it in sin_repaso:
        lineas.append(f"UPDATE items SET estado = 'oculto' WHERE id = '{it['id']}';")
    lineas.append("COMMIT;")
    OUT_SQL.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Ítems leídos: {len(items)} | repasados: {len(repasados)} | no reconocidos (se ocultan): {len(sin_repaso)}")
    print(f"Quedan publicados: {len(publicados)} | pasan a oculto: {len(items) - len(publicados)}")
    print("Publicados por plantilla y dificultad:",
          dict(Counter((r["plantilla"], r["dificultad"]) for r in repasados if r["id"] in publicados)))
    for plantilla in sorted({r["plantilla"] for r in repasados}):
        ejemplo = next(r for r in repasados if r["plantilla"] == plantilla and r["id"] in publicados)
        print(f"\n[{plantilla}] {ejemplo['enunciado']}\n   " + " | ".join(a["texto"] for a in ejemplo["alternativas"])
              + f"\n   > {ejemplo['explicacion']}")


if __name__ == "__main__":
    main()

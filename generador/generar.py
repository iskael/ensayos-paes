#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import random
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import plantillas_numeros  # noqa: F401
import plantillas_algebra  # noqa: F401
import plantillas_geometria  # noqa: F401
import plantillas_geometria_paes  # noqa: F401
import plantillas_figuras  # noqa: F401
import plantillas_numeros_paes  # noqa: F401
import plantillas_algebra_paes  # noqa: F401
import plantillas_probabilidad_paes  # noqa: F401
import plantillas_m2  # noqa: F401
import plantillas_m2_paes  # noqa: F401
import plantillas_numeros_figuras  # noqa: F401
import plantillas_modelo_2023  # noqa: F401
import plantillas_suficiencia  # noqa: F401
import plantillas_probabilidad  # noqa: F401
import plantillas_ciencias  # noqa: F401
import contenido  # noqa: F401
from nucleo import FIJOS, REGISTRO, Descartar, Plantilla, armar_item, propuesta_fija, validar

SEMILLA = 2026
OBJETIVO_POR_PLANTILLA = 12
INTENTOS_POR_PLANTILLA = 4000

SALIDA = Path(__file__).parent / "salida"
OUT_JSON = SALIDA / "items.json"
OUT_SQL = SALIDA / "carga.sql"
OUT_PUBLICAR = SALIDA / "publicar.sql"
OUT_REPORTE = SALIDA / "reporte.txt"
OUT_MUESTRA = SALIDA / "muestra.html"
DIR_FIGURAS = SALIDA / "figuras"
ANCHO_PNG = 720

NOMBRE_EJE = {
    "numeros": "Números",
    "algebra_funciones": "Álgebra y funciones",
    "geometria": "Geometría",
    "probabilidad_estadistica": "Probabilidad y estadística",
    "localizar": "Lectora · Localizar",
    "interpretar": "Lectora · Interpretar",
    "evaluar": "Lectora · Evaluar",
    "biologia": "Ciencias · Biología",
    "fisica": "Ciencias · Física",
    "quimica": "Ciencias · Química",
    "historia": "Historia · Mundo, América y Chile",
    "formacion_ciudadana": "Historia · Formación ciudadana",
    "sistema_economico": "Historia · Sistema económico",
}


def generar(semilla: int = SEMILLA, objetivo: int = OBJETIVO_POR_PLANTILLA):
    items, fallas, descartes = [], [], Counter()
    for pl in REGISTRO:
        rng = random.Random(f"{semilla}:{pl.nombre}")
        vistos = set()
        for _ in range(INTENTOS_POR_PLANTILLA):
            if len(vistos) >= objetivo:
                break
            try:
                propuesta = pl.funcion(rng)
            except Descartar:
                descartes[pl.nombre] += 1
                continue
            problemas = validar(propuesta)
            if problemas:
                if any("valores repetidos" in p for p in problemas):
                    descartes[pl.nombre] += 1
                else:
                    fallas.append((pl.nombre, propuesta.enunciado, problemas))
                continue
            if (propuesta.enunciado, propuesta.figura) in vistos:
                continue
            vistos.add((propuesta.enunciado, propuesta.figura))
            items.append(armar_item(pl, propuesta, rng))
    for it in FIJOS:
        nombre = f"fijo_{it.nivel.lower()}_{it.eje}"
        propuesta = propuesta_fija(it)
        problemas = validar(propuesta)
        if problemas:
            fallas.append((nombre, it.enunciado, problemas))
            continue
        rng = random.Random(f"{semilla}:{it.enunciado}:{it.estimulo.clave if it.estimulo else ''}")
        items.append(armar_item(Plantilla(nombre, it.eje, it.nivel, None), propuesta, rng, it.estimulo, it.orden))
    return items, fallas, descartes


def _sql(texto: str) -> str:
    return "'" + texto.replace("'", "''") + "'"


def a_sql(items: list[dict]) -> str:
    lineas = ["BEGIN;"]
    estimulos = {}
    for it in items:
        if it["estimulo"]:
            estimulos[it["estimulo"]["clave"]] = it["estimulo"]
    for e in estimulos.values():
        titulo = _sql(e["titulo"]) if e["titulo"] else "NULL"
        fuente = _sql(e["fuente"]) if e["fuente"] else "NULL"
        lineas.append(f"INSERT INTO estimulos (clave, titulo, texto, fuente) VALUES ({_sql(e['clave'])}, {titulo}, {_sql(e['texto'])}, {fuente}) "
                      "ON CONFLICT (clave) DO UPDATE SET titulo = EXCLUDED.titulo, texto = EXCLUDED.texto, fuente = EXCLUDED.fuente;")
    for it in items:
        alternativas = ", ".join(
            f"({_sql(a['etiqueta'])}, {_sql(a['texto'])}, {'TRUE' if a['es_correcta'] else 'FALSE'})"
            for a in it["alternativas"])
        imagen = _sql(it["imagen_url"]) if it["imagen_url"] else "NULL"
        estimulo = f"(SELECT id FROM estimulos WHERE clave = {_sql(it['estimulo']['clave'])})" if it["estimulo"] else "NULL"
        orden = str(it["orden_estimulo"]) if it["orden_estimulo"] is not None else "NULL"
        if it["imagen_url"]:
            lineas.append(f"UPDATE items SET imagen_url = {imagen} WHERE origen = 'generado' "
                          f"AND enunciado = {_sql(it['enunciado'])} AND imagen_url IS NULL;")
        lineas.append(
            "WITH nuevo AS (INSERT INTO items (enunciado, imagen_url, eje, nivel, dificultad, origen, estado, peso, explicacion, "
            "estimulo_id, orden_estimulo) "
            f"SELECT {_sql(it['enunciado'])}, {imagen}, "
            f"{_sql(it['eje'])}, {_sql(it['nivel'])}, {_sql(it['dificultad'])}, "
            f"'generado', 'borrador', {it['peso']}, {_sql(it['explicacion'])}, {estimulo}, {orden} "
            f"WHERE NOT EXISTS (SELECT 1 FROM items WHERE enunciado = {_sql(it['enunciado'])} "
            f"AND imagen_url IS NOT DISTINCT FROM {imagen} AND estimulo_id IS NOT DISTINCT FROM {estimulo}) RETURNING id) "
            "INSERT INTO alternativas (item_id, etiqueta, texto, es_correcta) "
            f"SELECT nuevo.id, v.e::etiqueta_alt, v.t, v.c FROM nuevo, (VALUES {alternativas}) AS v(e, t, c);")
    lineas.append("COMMIT;")
    return "\n".join(lineas) + "\n"


def a_sql_publicar(items: list[dict]) -> str:
    enunciados = ",\n  ".join(sorted({_sql(it["enunciado"]) for it in items}))
    return ("UPDATE items SET estado = 'publicado'\nWHERE origen = 'generado' AND estado = 'borrador' AND enunciado IN (\n  "
            f"{enunciados}\n);\n")


def a_reporte(items, fallas, descartes) -> str:
    por_eje = Counter(i["eje"] for i in items)
    por_plantilla = Counter(i["plantilla"] for i in items)
    por_dificultad = Counter(i["dificultad"] for i in items)
    posicion = Counter(a["etiqueta"] for i in items for a in i["alternativas"] if a["es_correcta"])
    lineas = [
        "REPORTE DEL GENERADOR DE ÍTEMS",
        f"Semilla: {SEMILLA} | Plantillas: {len(REGISTRO)} | Objetivo por plantilla: {OBJETIVO_POR_PLANTILLA}",
        f"Ítems aprobados: {len(items)}",
        f"Fallas de validación (bugs de plantilla): {len(fallas)}",
        "",
        "Por eje:",
        *[f"  {NOMBRE_EJE[e]}: {n}" for e, n in por_eje.items()],
        "",
        "Por dificultad:",
        *[f"  {d}: {n}" for d, n in sorted(por_dificultad.items())],
        "",
        "Posición de la alternativa correcta:",
        "  " + "  ".join(f"{e}={posicion[e]}" for e in "ABCDE"),
        "",
        "Por plantilla (aprobados / combinaciones descartadas):",
        *[f"  {pl.eje:<26} {pl.nombre:<40} {por_plantilla[pl.nombre]:>3} / {descartes[pl.nombre]}" for pl in REGISTRO],
    ]
    if fallas:
        lineas += ["", "FALLAS:"] + [f"  [{n}] {e} -> {'; '.join(p)}" for n, e, p in fallas]
    return "\n".join(lineas) + "\n"


def a_muestra(items: list[dict]) -> str:
    partes = [
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>Ítems generados</title>",
        "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css'>",
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>",
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js' "
        "onload=\"renderMathInElement(document.body,{delimiters:[{left:'$',right:'$',display:false}]})\"></script>",
        "<style>body{font-family:system-ui,sans-serif;margin:0;padding:16px;max-width:760px;margin-inline:auto;"
        "line-height:1.5;color:#1c1c1c;background:#faf8f5}h1{font-size:1.4rem}h2{margin-top:2rem;font-size:1.15rem;"
        "border-bottom:2px solid #d9d2c5;padding-bottom:4px}details{background:#fff;border:1px solid #e3ddd2;"
        "border-radius:10px;margin:10px 0;padding:8px 12px}summary{cursor:pointer;font-weight:600}"
        ".item{border-top:1px solid #eee;padding:10px 0}.item:first-of-type{border-top:0}"
        ".alt{margin:2px 0 2px 8px}.ok{font-weight:700;color:#18794e}.exp{font-size:.9rem;color:#555;margin-top:6px}"
        ".fig{display:block;max-width:min(100%,360px);height:auto;margin:10px auto;border:1px solid #e3ddd2;border-radius:8px}.tag{font-size:.75rem;background:#efe9dd;border-radius:6px;padding:1px 6px;margin-left:6px;font-weight:400}"
        "</style></head><body>",
        f"<h1>Ítems generados ({len(items)})</h1>",
        "<p>La alternativa correcta aparece en verde. Toca cada plantilla para ver sus ítems.</p>",
    ]
    for eje, nombre in NOMBRE_EJE.items():
        del_eje = [i for i in items if i["eje"] == eje]
        partes.append(f"<h2>{nombre} ({len(del_eje)})</h2>")
        for pl in [p for p in REGISTRO if p.eje == eje]:
            grupo = [i for i in del_eje if i["plantilla"] == pl.nombre]
            titulo = pl.nombre.replace("_", " ").capitalize()
            partes.append(f"<details><summary>{html.escape(titulo)} <span class='tag'>{len(grupo)} ítems</span></summary>")
            for it in grupo:
                partes.append(f"<div class='item'><div>{html.escape(it['enunciado'])}"
                              f"<span class='tag'>{it['dificultad']}</span></div>")
                if it["imagen_url"]:
                    partes.append(f"<img class='fig' loading='lazy' src='figuras/{it['imagen_url'].rsplit('/', 1)[1]}' alt=''>")
                for a in it["alternativas"]:
                    clase = "alt ok" if a["es_correcta"] else "alt"
                    partes.append(f"<div class='{clase}'>{a['etiqueta']}) {html.escape(a['texto'])}</div>")
                partes.append(f"<div class='exp'>{html.escape(it['explicacion'])}</div></div>")
            partes.append("</details>")
    partes.append("</body></html>")
    return "\n".join(partes)


def escribir_figuras(items: list[dict]) -> int:
    if not shutil.which("rsvg-convert"):
        raise SystemExit("Falta rsvg-convert (paquete librsvg2-bin) para convertir las figuras a PNG.")
    if DIR_FIGURAS.exists():
        shutil.rmtree(DIR_FIGURAS)
    DIR_FIGURAS.mkdir(parents=True)
    escritas = set()
    for it in items:
        svg = it.pop("figura_svg")
        if not svg:
            continue
        nombre = it["imagen_url"].rsplit("/", 1)[1]
        if nombre in escritas:
            continue
        escritas.add(nombre)
        subprocess.run(["rsvg-convert", "-w", str(ANCHO_PNG), "-o", str(DIR_FIGURAS / nombre)],
                       input=svg.encode(), check=True)
    return len(escritas)


def main():
    items, fallas, descartes = generar()
    SALIDA.mkdir(exist_ok=True)
    figuras_escritas = escribir_figuras(items)
    OUT_JSON.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_SQL.write_text(a_sql(items), encoding="utf-8")
    OUT_PUBLICAR.write_text(a_sql_publicar(items), encoding="utf-8")
    OUT_MUESTRA.write_text(a_muestra(items), encoding="utf-8")
    reporte = a_reporte(items, fallas, descartes)
    OUT_REPORTE.write_text(reporte, encoding="utf-8")
    print(reporte)
    print(f"Figuras PNG: {figuras_escritas} en {DIR_FIGURAS}")
    raise SystemExit(1 if fallas else 0)


if __name__ == "__main__":
    main()

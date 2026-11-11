#!/usr/bin/env python3
"""Agrega figura a los ítems de área de triángulo que dejó el prototipo (repasados por repaso_prototipo.py).

Lee `salida/triangulos.txt` (un enunciado por línea, exportado del banco) y escribe `salida/figuras_prototipo.sql` y las
imágenes en `salida/figuras_prototipo/`. Solo completa `imagen_url` donde está vacía, así que es idempotente.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import figuras
from generar import ANCHO_PNG, _sql

SALIDA = Path(__file__).parent / "salida"
ENTRADA = SALIDA / "triangulos.txt"
OUT_SQL = SALIDA / "figuras_prototipo.sql"
DIR_FIGURAS = SALIDA / "figuras_prototipo"
PATRON = re.compile(r"Un triángulo tiene una base de (\d+) cm y una altura de (\d+) cm\. ¿Cuál es su área\?")


def main():
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    lineas = ["BEGIN;"]
    for enunciado in filter(None, map(str.strip, ENTRADA.read_text(encoding="utf-8").splitlines())):
        r = PATRON.fullmatch(enunciado)
        if not r:
            raise SystemExit(f"Enunciado inesperado: {enunciado}")
        base, altura = map(int, r.groups())
        svg = figuras.triangulo_con_altura(base, altura, f"{base} cm", f"{altura} cm", desplazamiento=0.32)
        nombre = f"gen-{hashlib.sha1(svg.encode()).hexdigest()[:16]}.png"
        subprocess.run(["rsvg-convert", "-w", str(ANCHO_PNG), "-o", str(DIR_FIGURAS / nombre)], input=svg.encode(), check=True)
        lineas.append(f"UPDATE items SET imagen_url = {_sql('/uploads/' + nombre)} WHERE enunciado = {_sql(enunciado)} AND imagen_url IS NULL;")
    lineas.append("COMMIT;")
    OUT_SQL.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"{len(lineas) - 2} ítems -> {OUT_SQL}")


if __name__ == "__main__":
    main()

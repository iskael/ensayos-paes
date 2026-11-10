from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable

ETIQUETAS = ["A", "B", "C", "D"]
PESO_DEFECTO = 100

EJES = ("numeros", "algebra_funciones", "geometria", "probabilidad_estadistica")
NIVELES = ("M1", "M2")
DIFICULTADES = ("baja", "media", "alta")


class Descartar(Exception):
    """La combinación de parámetros sorteada no sirve; se sortea otra."""


def miles(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _es_decimal_finito(den: int) -> bool:
    for p in (2, 5):
        while den % p == 0:
            den //= p
    return den == 1


def tex(v) -> str:
    """Número en LaTeX con formato chileno: coma decimal, fracción irreducible si no es decimal finito."""
    v = Fraction(v)
    if v.denominator == 1:
        n = v.numerator
        return miles(n) if abs(n) >= 10000 else str(n)
    if _es_decimal_finito(v.denominator):
        signo = "-" if v < 0 else ""
        v = abs(v)
        entero = v.numerator // v.denominator
        resto = v - entero
        digitos = ""
        while resto:
            resto *= 10
            digitos += str(resto.numerator // resto.denominator)
            resto -= resto.numerator // resto.denominator
        return f"{signo}{entero}{{,}}{digitos}"
    signo = "-" if v < 0 else ""
    return f"{signo}\\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def m(v) -> str:
    return f"${tex(v)}$"


def frac(v) -> str:
    """Como tex(), pero nunca pasa a decimal: fracción irreducible o entero."""
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    signo = "-" if v < 0 else ""
    return f"{signo}\\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def par(n) -> str:
    return f"({tex(n)})" if Fraction(n) < 0 else tex(n)


def simplificada(num: int, den: int) -> str:
    """Fracción tal como se plantea y, si cambia, su forma irreducible."""
    cruda = f"\\frac{{{num}}}{{{den}}}"
    final = frac(Fraction(num, den))
    return cruda if final == cruda else f"{cruda} = {final}"


def opf(valor, error: str | None = None) -> "Opcion":
    return Opcion(valor, f"${frac(valor)}$", error)


def pesos(n: int) -> str:
    return f"$\\text{{\\textdollar}}\\,{miles(int(n))}$"


def raiz_tex(cuadrado: int) -> str:
    """LaTeX de la raíz cuadrada de un entero positivo, simplificada (k√r)."""
    if cuadrado < 0:
        raise Descartar("raíz de negativo")
    r = math.isqrt(cuadrado)
    if r * r == cuadrado:
        return str(r)
    k, resto = 1, cuadrado
    f = 2
    while f * f <= resto:
        while resto % (f * f) == 0:
            resto //= f * f
            k *= f
        f += 1
    return f"{k if k > 1 else ''}\\sqrt{{{resto}}}"


def termino(coef, variable: str, primero: bool) -> str:
    coef = Fraction(coef)
    if coef == 0:
        return ""
    signo = "-" if coef < 0 else ("" if primero else "+")
    cuerpo = tex(abs(coef))
    if variable and abs(coef) == 1:
        cuerpo = ""
    texto = f"{signo}{cuerpo}{variable}"
    return texto if primero else f" {signo} {cuerpo}{variable}"


def polinomio(coefs: list, variable: str = "x") -> str:
    """coefs de mayor a menor grado. Devuelve LaTeX sin delimitadores."""
    grado = len(coefs) - 1
    partes = []
    for i, c in enumerate(coefs):
        g = grado - i
        var = "" if g == 0 else (variable if g == 1 else f"{variable}^{{{g}}}")
        t = termino(c, var, primero=not partes)
        if t:
            partes.append(t)
    return "".join(partes) if partes else "0"


@dataclass
class Opcion:
    valor: object
    texto: str
    error: str | None = None


def op(valor, error: str | None = None, texto: str | None = None) -> Opcion:
    return Opcion(valor, texto if texto is not None else m(valor), error)


@dataclass
class Propuesta:
    enunciado: str
    correcta: Opcion
    distractores: list[Opcion]
    pasos: str
    comprobar: Callable[[object], bool]
    dificultad: str
    orden_fijo: bool = False


@dataclass
class Plantilla:
    nombre: str
    eje: str
    nivel: str
    funcion: Callable[[random.Random], Propuesta]


REGISTRO: list[Plantilla] = []


def plantilla(eje: str, nivel: str = "M1"):
    def decorar(f):
        REGISTRO.append(Plantilla(f.__name__, eje, nivel, f))
        return f
    return decorar


def _latex_valido(texto: str) -> bool:
    return texto.count("$") % 2 == 0 and "$$" not in texto


def validar(p: Propuesta) -> list[str]:
    fallas = []
    if p.dificultad not in DIFICULTADES:
        fallas.append("dificultad inválida")
    if len(p.distractores) != 3:
        fallas.append("no tiene 3 distractores")
    opciones = [p.correcta] + p.distractores
    if len({o.valor for o in opciones}) != len(opciones):
        fallas.append("valores repetidos entre alternativas")
    if len({o.texto for o in opciones}) != len(opciones):
        fallas.append("textos repetidos entre alternativas")
    if not p.comprobar(p.correcta.valor):
        fallas.append("la respuesta correcta no satisface el problema")
    for d in p.distractores:
        if p.comprobar(d.valor):
            fallas.append(f"un distractor también es correcto: {d.texto}")
        if not d.error:
            fallas.append(f"distractor sin error típico asociado: {d.texto}")
    for t in [p.enunciado, p.pasos] + [o.texto for o in opciones]:
        if not _latex_valido(t):
            fallas.append(f"delimitadores de fórmula mal formados: {t}")
    return fallas


def armar_item(pl: Plantilla, p: Propuesta, rng: random.Random) -> dict:
    opciones = [p.correcta] + p.distractores
    if p.orden_fijo:
        opciones.sort(key=lambda o: o.valor)
    else:
        rng.shuffle(opciones)
    alternativas = []
    errores = []
    for etiqueta, o in zip(ETIQUETAS, opciones):
        alternativas.append({"etiqueta": etiqueta, "texto": o.texto, "es_correcta": o is p.correcta})
        if o is not p.correcta:
            errores.append(f"{etiqueta}) {o.error}")
    titulo = "Las demás alternativas" if p.orden_fijo else "Errores frecuentes"
    explicacion = f"{p.pasos} {titulo}: {'; '.join(errores)}."
    return {
        "plantilla": pl.nombre,
        "eje": pl.eje,
        "nivel": pl.nivel,
        "dificultad": p.dificultad,
        "enunciado": p.enunciado,
        "alternativas": alternativas,
        "explicacion": explicacion,
        "peso": PESO_DEFECTO,
        "origen": "generado",
        "estado": "borrador",
    }

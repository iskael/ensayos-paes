"""Preguntas de suficiencia de datos de la PAES M2: cinco alternativas fijas (A a E) en el orden oficial.

La clave se obtiene enumerando un dominio finito de casos: una afirmación basta si con ella el valor pedido queda
determinado (toma un único valor en todos los casos que la cumplen). La comprobación repite la enumeración sobre un
dominio más amplio, para descartar que la conclusión dependa del tamaño del dominio. La explicación muestra un
contraejemplo por cada afirmación que no basta.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable

from nucleo import Descartar, Opcion, Propuesta, plantilla, tex

NUM, ALG, GEO, PRO = "numeros", "algebra_funciones", "geometria", "probabilidad_estadistica"

OPCIONES = ["(1) por sí sola", "(2) por sí sola", "Ambas juntas, (1) y (2)", "Cada una por sí sola, (1) ó (2)",
            "Se requiere información adicional"]


@dataclass
class Afirmacion:
    texto: str
    cumple: Callable[[tuple], bool]


def _valores(dominio, objetivo, condiciones):
    return {objetivo(c) for c in dominio if all(f.cumple(c) for f in condiciones)}


def _clave(dominio, objetivo, a1, a2) -> int:
    s1 = len(_valores(dominio, objetivo, [a1])) == 1
    s2 = len(_valores(dominio, objetivo, [a2])) == 1
    s12 = len(_valores(dominio, objetivo, [a1, a2])) == 1
    if s1 and s2:
        return 3
    if s1:
        return 0
    if s2:
        return 1
    if s12:
        return 2
    return 4


def _ejemplo(dominio, objetivo, condiciones, mostrar):
    vistos = {}
    for c in dominio:
        if all(f.cumple(c) for f in condiciones):
            vistos.setdefault(objetivo(c), c)
        if len(vistos) == 2:
            break
    (v1, c1), (v2, c2) = list(vistos.items())[:2]
    return f"con {mostrar(c1)} el valor es ${tex(v1)}$ y con {mostrar(c2)} es ${tex(v2)}$"


def armar(enunciado, pide, dominio, dominio_amplio, objetivo, a1, a2, mostrar, dificultad="alta"):
    if _valores(dominio, objetivo, [a1, a2]) == set():
        raise Descartar
    clave = _clave(dominio, objetivo, a1, a2)
    if _clave(dominio_amplio, objetivo, a1, a2) != clave:
        raise Descartar
    partes = []
    errores = {}
    for nombre, cond in (("(1) por sí sola", [a1]), ("(2) por sí sola", [a2]), ("con ambas juntas", [a1, a2])):
        valores = _valores(dominio, objetivo, cond)
        if len(valores) == 1:
            partes.append(f"{nombre.capitalize() if nombre[0] != '(' else nombre} basta: {pide} es ${tex(next(iter(valores)))}$")
        else:
            partes.append(f"{nombre.capitalize() if nombre[0] != '(' else nombre} no basta: {_ejemplo(dominio, objetivo, cond, mostrar)}")
    pasos = ". ".join(partes) + "."
    s1 = len(_valores(dominio, objetivo, [a1])) == 1
    s2 = len(_valores(dominio, objetivo, [a2])) == 1
    errores[0] = "la afirmación (2) también basta por sí sola" if s1 and s2 else "con (1) sola el valor no queda determinado"
    errores[1] = "la afirmación (1) también basta por sí sola" if s1 and s2 else "con (2) sola el valor no queda determinado"
    errores[2] = "alguna de las afirmaciones ya basta por sí sola" if s1 or s2 else "ni siquiera juntas determinan el valor"
    errores[3] = "no es cierto que cada una baste por sí sola"
    errores[4] = "con la información dada sí se puede determinar el valor"
    opciones = [Opcion(i, texto, None if i == clave else errores[i]) for i, texto in enumerate(OPCIONES)]
    correcta = opciones[clave]
    distractores = [o for o in opciones if o is not correcta]
    clave_amplia = _clave(dominio_amplio, objetivo, a1, a2)
    return Propuesta(enunciado, correcta, distractores, pasos, lambda v: v == clave_amplia, dificultad, orden_fijo=True)


def _par(c):
    return f"$x = {tex(c[0])}$ e $y = {tex(c[1])}$"


_PARES = [(x, y) for x in range(-12, 13) for y in range(-12, 13)]
_PARES_AMPLIO = [(Fraction(x, 2), Fraction(y, 2)) for x in range(-36, 37) for y in range(-36, 37)]


@plantilla(ALG, "M2")
def suficiencia_valor_de_una_expresion(rng):
    x0, y0 = rng.choice([(x, y) for x, y in _PARES if x != y and x != -y and x and y and abs(x) <= 9 and abs(y) <= 9])
    objetivos = [
        ("x + y", lambda c: c[0] + c[1]),
        ("x - y", lambda c: c[0] - c[1]),
        ("x^2 - y^2", lambda c: c[0] ** 2 - c[1] ** 2),
        ("\\frac{x^2 - y^2}{x + y}", lambda c: c[0] - c[1]),
        ("xy", lambda c: c[0] * c[1]),
        ("\\frac{x}{y}", lambda c: Fraction(c[0]) / c[1]),
    ]
    afirmaciones = [
        lambda: Afirmacion(f"$x + y = {x0 + y0}$", lambda c: c[0] + c[1] == x0 + y0),
        lambda: Afirmacion(f"$x - y = {x0 - y0}$", lambda c: c[0] - c[1] == x0 - y0),
        lambda: Afirmacion(f"$xy = {x0 * y0}$", lambda c: c[0] * c[1] == x0 * y0),
        lambda: Afirmacion(f"$x^2 - y^2 = {x0 * x0 - y0 * y0}$", lambda c: c[0] ** 2 - c[1] ** 2 == x0 * x0 - y0 * y0),
        lambda: Afirmacion(f"$x = {tex(Fraction(x0, y0))}y$" if Fraction(x0, y0).denominator == 1 else f"${Fraction(x0, y0).denominator}x = {Fraction(x0, y0).numerator}y$",
                           lambda c: c[0] * y0 == x0 * c[1]),
        lambda: Afirmacion(f"$x > y$" if x0 > y0 else "$x < y$", lambda c: (c[0] > c[1]) == (x0 > y0)),
    ]
    k = rng.randrange(len(objetivos))
    texto_obj, objetivo = objetivos[k]
    i, j = rng.sample(range(len(afirmaciones)), 2)
    directas = {0: 0, 1: 1, 2: 3, 4: 2, 5: 4}
    if directas.get(k) in (i, j):
        raise Descartar
    a1, a2 = afirmaciones[i](), afirmaciones[j]()
    validos = lambda c: c[1] != 0 and c[0] + c[1] != 0 and c[0] != c[1]
    dominio = [c for c in _PARES if validos(c)]
    amplio = [c for c in _PARES_AMPLIO if validos(c)]
    enunciado = (f"Considera los números reales $x$ e $y$, con $y \\neq 0$, $x \\neq y$ y $x \\neq -y$. Se puede determinar el valor de "
                 f"${texto_obj}$ si se sabe que: (1) {a1.texto}; (2) {a2.texto}.")
    return armar(enunciado, f"${texto_obj}$", dominio, amplio, objetivo, a1, a2, _par)


def _rect(c):
    return f"un rectángulo de {c[0]} por {c[1]}"


_RECTS = [(a, b) for a in range(1, 41) for b in range(1, a + 1)]
_RECTS_AMPLIO = [(a, b) for a in range(1, 121) for b in range(1, a + 1)]


@plantilla(GEO, "M2")
def suficiencia_medidas_de_un_rectangulo(rng):
    a0, b0 = rng.choice([(a, b) for a, b in _RECTS if a <= 24 and a != b and b >= 2])
    objetivos = [
        ("el área del rectángulo", lambda c: c[0] * c[1]),
        ("el perímetro del rectángulo", lambda c: 2 * (c[0] + c[1])),
        ("el cuadrado de la medida de la diagonal", lambda c: c[0] ** 2 + c[1] ** 2),
        ("la medida del lado mayor", lambda c: c[0]),
    ]
    afirmaciones = [
        lambda: Afirmacion(f"el perímetro mide {2 * (a0 + b0)} cm", lambda c: 2 * (c[0] + c[1]) == 2 * (a0 + b0)),
        lambda: Afirmacion(f"el área mide {a0 * b0} cm²", lambda c: c[0] * c[1] == a0 * b0),
        lambda: Afirmacion(f"el lado mayor mide {a0 - b0} cm más que el menor", lambda c: c[0] - c[1] == a0 - b0),
        lambda: Afirmacion(f"el lado menor mide {b0} cm", lambda c: c[1] == b0),
        lambda: Afirmacion(f"el lado mayor es {tex(Fraction(a0, b0)).replace('{,}', ',')} veces el menor" if Fraction(a0, b0).denominator == 1
                           else f"la razón entre el lado mayor y el menor es {Fraction(a0, b0).numerator} : {Fraction(a0, b0).denominator}",
                           lambda c: c[0] * b0 == a0 * c[1]),
    ]
    texto_obj, objetivo = rng.choice(objetivos)
    i, j = rng.sample(range(len(afirmaciones)), 2)
    a1, a2 = afirmaciones[i](), afirmaciones[j]()
    enunciado = (f"Las medidas de los lados de un rectángulo son números enteros de centímetros. Se puede determinar {texto_obj} si se sabe que: "
                 f"(1) {a1.texto}; (2) {a2.texto}.")
    pide = texto_obj
    return armar(enunciado, pide, _RECTS, _RECTS_AMPLIO, objetivo, a1, a2, _rect)


def _urna(c):
    return f"{c[0]} {'azul' if c[0] == 1 else 'azules'} y {c[1]} {'roja' if c[1] == 1 else 'rojas'}"


@plantilla(PRO, "M2")
def suficiencia_probabilidad_en_una_urna(rng):
    n = rng.randrange(4, 13)
    azules = rng.randrange(1, n)
    rojas = n - azules
    dominio = [(a, n - a) for a in range(0, n + 1)]
    objetivos = [
        ("la probabilidad de que la segunda bolita sea azul dado que la primera fue roja", lambda c: Fraction(c[0], n - 1)),
        ("la probabilidad de que las dos bolitas sean rojas", lambda c: Fraction(c[1] * (c[1] - 1), n * (n - 1))),
        ("la cantidad de bolitas azules", lambda c: Fraction(c[0])),
    ]
    p_azul = Fraction(azules, n)
    p_distinto = Fraction(2 * azules * rojas, n * (n - 1))
    afirmaciones = [
        lambda: Afirmacion(f"al extraer una bolita, la probabilidad de que sea azul es ${tex(p_azul)}$", lambda c: Fraction(c[0], n) == p_azul),
        lambda: Afirmacion(f"al extraer dos bolitas sin reposición, la probabilidad de que sean de distinto color es ${tex(p_distinto)}$",
                           lambda c: Fraction(2 * c[0] * c[1], n * (n - 1)) == p_distinto),
        lambda: Afirmacion("hay más bolitas azules que rojas" if azules > rojas else "hay más bolitas rojas que azules" if rojas > azules
                           else "hay tantas bolitas azules como rojas", lambda c: (c[0] > c[1]) == (azules > rojas) and (c[0] == c[1]) == (azules == rojas)),
        lambda: Afirmacion(f"al extraer {3} bolitas con reposición, la probabilidad de que todas sean rojas es ${tex(Fraction(rojas, n) ** 3)}$",
                           lambda c: Fraction(c[1], n) ** 3 == Fraction(rojas, n) ** 3),
    ]
    texto_obj, objetivo = rng.choice(objetivos)
    i, j = rng.sample(range(len(afirmaciones)), 2)
    a1, a2 = afirmaciones[i](), afirmaciones[j]()
    enunciado = (f"En una urna hay {n} bolitas del mismo tipo, algunas azules y las demás rojas. Al extraer dos bolitas sin reposición, se puede "
                 f"determinar {texto_obj} si se sabe que: (1) {a1.texto}; (2) {a2.texto}.") if texto_obj != "la cantidad de bolitas azules" else (
                 f"En una urna hay {n} bolitas del mismo tipo, algunas azules y las demás rojas. Se puede determinar la cantidad de bolitas azules si "
                 f"se sabe que: (1) {a1.texto}; (2) {a2.texto}.")
    pide = {"la cantidad de bolitas azules": "la cantidad de azules"}.get(texto_obj, "la probabilidad pedida")
    return armar(enunciado, pide, dominio, dominio, objetivo, a1, a2, _urna)


def _entero(c):
    return f"$n = {c[0]}$"


_ENTEROS = [(n,) for n in range(1, 301)]
_ENTEROS_AMPLIO = [(n,) for n in range(1, 3001)]


def _es_primo(n):
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


@plantilla(NUM, "M2")
def suficiencia_numero_entero_por_condiciones(rng):
    n0 = rng.randrange(6, 100)
    divisores_mult = [d for d in (2, 3, 4, 5, 6, 7, 9, 10, 12) if n0 % d == 0]
    cota = rng.choice([c for c in (20, 30, 40, 50, 60, 80, 100, 120) if c > n0] or [n0 + 10])
    multiplo = rng.choice([m for m in (2, 3, 4, 5, 6) if m * n0 <= 300] or [2])
    afirmaciones = [
        lambda: Afirmacion(f"$n$ es divisor de ${multiplo * n0}$ y mayor que ${multiplo * n0 // 2 - 1}$" if multiplo > 1 else f"$n$ es divisor de ${n0}$",
                           lambda c: (multiplo * n0) % c[0] == 0 and c[0] > multiplo * n0 // 2 - 1),
        lambda: Afirmacion(f"$n$ es múltiplo de ${divisores_mult[-1]}$ y menor que ${cota}$" if divisores_mult else f"$n$ es menor que ${cota}$",
                           lambda c: (c[0] % divisores_mult[-1] == 0 if divisores_mult else True) and c[0] < cota),
        lambda: Afirmacion(f"$n^2$ está entre ${(n0 - 1) ** 2}$ y ${(n0 + 1) ** 2}$", lambda c: (n0 - 1) ** 2 < c[0] ** 2 < (n0 + 1) ** 2),
        lambda: Afirmacion("$n$ es primo" if _es_primo(n0) else "$n$ no es primo", lambda c: _es_primo(c[0]) == _es_primo(n0)),
        lambda: Afirmacion(f"$n$ es par" if n0 % 2 == 0 else "$n$ es impar", lambda c: c[0] % 2 == n0 % 2),
        lambda: Afirmacion(f"la suma de las cifras de $n$ es ${sum(map(int, str(n0)))}$ y $n < 100$",
                           lambda c: sum(map(int, str(c[0]))) == sum(map(int, str(n0))) and c[0] < 100),
    ]
    i, j = rng.sample(range(len(afirmaciones)), 2)
    a1, a2 = afirmaciones[i](), afirmaciones[j]()
    if not (a1.cumple((n0,)) and a2.cumple((n0,))):
        raise Descartar
    enunciado = f"Considera un número entero positivo $n$. Se puede determinar el valor de $n$ si se sabe que: (1) {a1.texto}; (2) {a2.texto}."
    return armar(enunciado, "$n$", _ENTEROS, _ENTEROS_AMPLIO, lambda c: c[0], a1, a2, _entero)

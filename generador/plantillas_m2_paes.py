"""Segunda tanda de plantillas M2, con tipos tomados de las PAES M2 de invierno 2025, regular 2025 e invierno 2026.

Se replica la habilidad evaluada con contextos y números propios; no se copia ningún ítem.
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction

from nucleo import Descartar, Propuesta, frac, miles, op, opf, par, pesos, plantilla, polinomio, raiz_tex, tex

NUM, ALG, GEO, PRO = "numeros", "algebra_funciones", "geometria", "probabilidad_estadistica"


def _tres_distintos(correcto, candidatos):
    elegidos, vistos = [], {correcto}
    for valor, error in candidatos:
        if valor not in vistos:
            vistos.add(valor)
            elegidos.append((valor, error))
        if len(elegidos) == 3:
            return elegidos
    raise Descartar


def _dec(v) -> str:
    return tex(Fraction(v))


# ----------------------------------------------------------------- Números

@plantilla(NUM, "M2")
def punto_que_divide_un_intervalo_en_razon(rng):
    den = rng.choice([3, 4, 5, 6, 7, 8])
    a = Fraction(rng.randrange(1, 3 * den), den)
    b = a + Fraction(rng.randrange(1, 2 * den), rng.choice([3, 4, 5, 6, 7]))
    if a.denominator == 1 or b.denominator == 1:
        raise Descartar
    k = rng.choice([2, 3, 4])
    palabra = {2: "el doble", 3: "el triple", 4: "el cuádruple"}[k]
    x = (a + k * b) / (1 + k)
    enunciado = (f"Considera el número racional $x$ ubicado en la recta numérica entre ${frac(a)}$ y ${frac(b)}$, tal que la distancia "
                 f"entre ${frac(a)}$ y $x$ es {palabra} de la distancia entre $x$ y ${frac(b)}$. ¿Cuál es el valor de $x$?")
    pasos = (f"La distancia entre los extremos es ${frac(b)} - {frac(a)} = {frac(b - a)}$ y se divide en ${k} + 1 = {k + 1}$ partes iguales, de las "
             f"cuales {k} quedan entre ${frac(a)}$ y $x$: $x = {frac(a)} + \\frac{{{k}}}{{{k + 1}}} \\cdot {frac(b - a)} = {frac(x)}$.")
    candidatos = [((k * a + b) / (1 + k), f"mide {palabra} de la distancia desde ${frac(b)}$ y no desde ${frac(a)}$"),
                  ((a + b) / 2, "calcula el punto medio del intervalo"),
                  (a + (b - a) / k, f"divide la distancia en {k} partes en vez de {k + 1}"),
                  (b - (b - a) / k, f"divide la distancia en {k} partes en vez de {k + 1} y la mide desde el otro extremo")]
    distractores = [opf(v, e) for v, e in _tres_distintos(x, candidatos)]
    return Propuesta(enunciado, opf(x), distractores, pasos, lambda v: a < v < b and v - a == k * (b - v), "media")


def _tasa_decimal(tasa: Fraction) -> str:
    return _dec(1 + tasa / 100)


@plantilla(NUM, "M2")
def interes_generado_con_interes_compuesto(rng):
    capital = rng.randrange(2, 41) * 25000
    tasa = Fraction(rng.choice([5, 10, 15, 20, 25, 30, 35, 40, 50]), 10)
    n = rng.randrange(2, 7)
    unidad, plural = rng.choice([("mensual", "meses"), ("anual", "años")])
    factor = 1 + tasa / 100
    interes = capital * (factor ** n - 1)
    enunciado = (f"Una institución financiera ofrece un interés compuesto {unidad} de un ${_dec(tasa)}\\,\\%$ al capital depositado. Una persona "
                 f"deposita {pesos(capital)} y no hace retiros ni otros depósitos durante {n} {plural}. ¿Cuál de las siguientes expresiones "
                 f"representa el interés que se produce en ese periodo?")
    c = f"\\text{{\\textdollar}}\\,{miles(capital)}"
    textos = {
        "correcta": f"${c} \\cdot ({_tasa_decimal(tasa)}^{{{n}}} - 1)$",
        "final": f"${c} \\cdot {_tasa_decimal(tasa)}^{{{n}}}$",
        "decimal": f"${c} \\cdot {_dec(tasa / 100)}^{{{n}}}$",
        "simple": f"${c} \\cdot {_dec(tasa / 100)} \\cdot {n}$",
        "mal_factor": f"${c} \\cdot ({_dec(1 + tasa / 10)}^{{{n}}} - 1)$",
    }
    valores = {
        "correcta": interes,
        "final": capital * factor ** n,
        "decimal": capital * (tasa / 100) ** n,
        "simple": capital * tasa / 100 * n,
        "mal_factor": capital * ((1 + tasa / 10) ** n - 1),
    }
    errores = {
        "final": "calcula el capital final, que incluye el depósito, y no solo el interés",
        "decimal": "eleva solo la tasa y olvida sumar el capital en cada periodo",
        "simple": "calcula interés simple en vez de compuesto",
        "mal_factor": f"escribe el ${_dec(tasa)}\\,\\%$ como ${_dec(tasa / 10)}$ en vez de ${_dec(tasa / 100)}$",
    }
    pasos = (f"Con interés compuesto el capital al cabo de {n} {plural} es ${c} \\cdot {_tasa_decimal(tasa)}^{{{n}}}$; el interés es esa cantidad menos "
             f"el depósito inicial: ${c} \\cdot {_tasa_decimal(tasa)}^{{{n}}} - {c} = {textos['correcta'][1:-1]}$.")
    orden = rng.sample(["final", "decimal", "simple", "mal_factor"], 4)
    elegidos = _tres_distintos(valores["correcta"], [(valores[k], k) for k in orden])
    distractores = [op(v, errores[k], textos[k]) for v, k in elegidos]
    esperado = capital * factor ** n - capital
    return Propuesta(enunciado, op(interes, None, textos["correcta"]), distractores, pasos, lambda v: v == esperado, "media")


@plantilla(NUM, "M2")
def valor_inicial_tras_variaciones_sucesivas(rng):
    p = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    dias = rng.randrange(3, 6)
    sube = rng.random() < 0.4
    factor = Fraction(100 + p, 100) if sube else Fraction(100 - p, 100)
    inicial = rng.randrange(2, 60) * 10 ** rng.randrange(3, 5)
    final = inicial * factor ** (dias - 1)
    if final.denominator != 1:
        raise Descartar
    final = int(final)
    cosa, verbo = rng.choice([("visitas a un sitio web", "las visitas"), ("búsquedas de una canción", "las búsquedas"),
                              ("pasajeros de una línea de buses", "los pasajeros")])
    cambio = "aumentó" if sube else "disminuyó"
    enunciado = (f"Se registró la cantidad diaria de {cosa} durante {dias} días seguidos. Cada día la cantidad {cambio} un ${p}\\,\\%$ respecto "
                 f"del día anterior, y el último día hubo ${miles(final)}$. ¿Cuál de las siguientes expresiones representa la cantidad "
                 f"del primer día?")
    f_tex = _dec(factor)
    g_tex = _dec(Fraction(p, 100))
    F = miles(final)
    pasos = (f"Entre el primer y el último día hay {dias - 1} variaciones, cada una multiplica por ${f_tex}$. Si $x$ es la cantidad del primer "
             f"día, $x \\cdot {f_tex}^{{{dias - 1}}} = {F}$, de donde $x = \\frac{{{F}}}{{{f_tex}^{{{dias - 1}}}}}$.")
    opciones = [
        (final / factor ** (dias - 1), f"$\\frac{{{F}}}{{{f_tex}^{{{dias - 1}}}}}$", None),
        (final / factor ** dias, f"$\\frac{{{F}}}{{{f_tex}^{{{dias}}}}}$", f"cuenta {dias} variaciones en {dias} días, cuando son {dias - 1}"),
        (final * factor ** (dias - 1), f"${F} \\cdot {f_tex}^{{{dias - 1}}}$", "aplica las variaciones hacia adelante en vez de deshacerlas"),
        (final / Fraction(p, 100) ** (dias - 1), f"$\\frac{{{F}}}{{{g_tex}^{{{dias - 1}}}}}$", "divide por el porcentaje de variación y no por el factor"),
        (final * Fraction(p, 100) ** (dias - 1), f"${F} \\cdot {g_tex}^{{{dias - 1}}}$", "multiplica por el porcentaje de variación"),
    ]
    correcta = op(opciones[0][0], None, opciones[0][1])
    resto = opciones[1:]
    rng.shuffle(resto)
    vistos, distractores = {correcta.valor}, []
    for v, t, e in resto:
        if v not in vistos and len(distractores) < 3:
            vistos.add(v)
            distractores.append(op(v, e, t))
    if len(distractores) < 3:
        raise Descartar
    return Propuesta(enunciado, correcta, distractores, pasos, lambda v: v * factor ** (dias - 1) == final, "media")


_APROX = {2: Fraction(30, 100), 3: Fraction(48, 100), 5: Fraction(70, 100)}
_APROX_TEX = {2: "0{,}30", 3: "0{,}48", 5: "0{,}70"}


def _expr_log(coefs) -> str:
    partes = []
    for primo, c in zip((2, 3, 5), coefs):
        if c == 0:
            continue
        cuerpo = _APROX_TEX[primo] if abs(c) == 1 else f"{abs(c)} \\cdot {_APROX_TEX[primo]}"
        signo = "-" if c < 0 else ("+" if partes else "")
        partes.append(f"{' ' + signo + ' ' if partes else signo}{cuerpo}")
    return "".join(partes) if partes else "0"


def _log_real(coefs) -> float:
    return sum(c * math.log10(p) for c, p in zip(coefs, (2, 3, 5)))


@plantilla(NUM, "M2")
def logaritmo_en_otra_base_con_aproximaciones(rng):
    base = rng.choice([2, 3, 5])
    exps = [rng.randrange(0, 3) for _ in range(3)]
    exps[(2, 3, 5).index(base)] = 0
    if sum(exps) < 2:
        raise Descartar
    n = 2 ** exps[0] * 3 ** exps[1] * 5 ** exps[2]
    num = tuple(exps)
    den = tuple(1 if p == base else 0 for p in (2, 3, 5))
    enunciado = (f"Si $\\log 2 \\approx 0{{,}}30$, $\\log 3 \\approx 0{{,}}48$ y $\\log 5 \\approx 0{{,}}70$, ¿cuál de las siguientes expresiones "
                 f"corresponde a una aproximación de $\\log_{{{base}}} {n}$?")

    def texto(v):
        a, b = v
        if b is None:
            return f"${_expr_log(a)}$"
        if b == "resta":
            return f"${_expr_log(a)} - {_APROX_TEX[base]}$"
        return f"$\\frac{{{_expr_log(a)}}}{{{_expr_log(b)}}}$"

    factores = " \\cdot ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in zip((2, 3, 5), exps) if e)
    pasos = (f"Por cambio de base, $\\log_{{{base}}} {n} = \\frac{{\\log {n}}}{{\\log {base}}}$. Como ${n} = {factores}$, "
             f"$\\log {n} \\approx {_expr_log(num)}$ y $\\log {base} \\approx {_APROX_TEX[base]}$.")
    candidatos = [((den, num), "invierte el cambio de base: divide el logaritmo de la base por el del número"),
                  ((num, "resta"), "resta los logaritmos en vez de dividirlos"),
                  ((num, None), "calcula $\\log " + str(n) + "$ y olvida dividir por el logaritmo de la base"),
                  ((tuple(e * 1 for e in (1 if e else 0 for e in exps)), den), "olvida los exponentes de la descomposición")]
    correcto = (num, den)
    elegidos = _tres_distintos(correcto, candidatos)
    distractores = [op(v, e, texto(v)) for v, e in elegidos]
    objetivo = math.log(n, base)

    def comprobar(v):
        a, b = v
        if b == "resta":
            valor = _log_real(a) - math.log10(base)
        else:
            valor = _log_real(a) / _log_real(b) if b is not None else _log_real(a)
        return abs(valor - objetivo) < 1e-9

    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos, comprobar, "media")


@plantilla(NUM, "M2")
def nivel_de_intensidad_sonora(rng):
    if rng.random() < 0.5:
        beta = rng.choice([35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85])
        lugar = rng.choice(["una sala de clases", "una biblioteca", "una zona residencial de noche", "una oficina"])
        exponente = Fraction(beta - 120, 10)
        enunciado = (f"El nivel de intensidad sonora $\\beta$, en dB, y la intensidad acústica $I$, en $\\frac{{\\text{{W}}}}{{\\text{{m}}^2}}$, se relacionan "
                     f"mediante $\\beta = 10 \\cdot \\log(I) + 120$. Si el nivel máximo permitido en {lugar} es de {beta} dB, ¿cuál es la intensidad "
                     f"acústica máxima permitida, en $\\frac{{\\text{{W}}}}{{\\text{{m}}^2}}$?")
        pasos = (f"Se reemplaza: ${beta} = 10 \\cdot \\log(I) + 120$, luego $\\log(I) = \\frac{{{beta} - 120}}{{10}} = {_dec(exponente)}$ "
                 f"e $I = 10^{{{_dec(exponente)}}}$.")
        candidatos = [(-exponente, "despeja $\\log(I) = \\frac{120 - \\beta}{10}$ y se equivoca en el signo"),
                      (Fraction(beta + 120, 10), "suma 120 en vez de restarlo"),
                      (Fraction(beta, 10) - 120, "divide solo el nivel por 10 y luego resta 120"),
                      (Fraction(beta - 120), "olvida dividir por 10")]
        textos = lambda v: f"$10^{{{_dec(v)}}}$"
        distractores = [op(v, e, textos(v)) for v, e in _tres_distintos(exponente, candidatos)]
        return Propuesta(enunciado, op(exponente, None, textos(exponente)), distractores, pasos,
                         lambda v: 10 * v + 120 == beta, "media")
    k = rng.randrange(2, 6)
    fuente = rng.choice(["un parlante", "una máquina", "un motor"])
    enunciado = (f"El nivel de intensidad sonora $\\beta$, en dB, y la intensidad acústica $I$ se relacionan mediante $\\beta = 10 \\cdot \\log(I) + 120$. "
                 f"Si la intensidad acústica de {fuente} se multiplica por $10^{{{k}}}$, ¿en cuántos dB aumenta su nivel de intensidad sonora?")
    pasos = (f"$10 \\cdot \\log(10^{{{k}}} I) + 120 = 10 \\cdot ({k} + \\log I) + 120 = \\beta + {10 * k}$: aumenta en {10 * k} dB.")
    candidatos = [(k, "suma el exponente sin multiplicarlo por 10"), (10 ** k, "suma la potencia completa en vez de su logaritmo"),
                  (10 * k + 120, "suma también la constante 120"), (k * 120, "multiplica el exponente por 120")]
    distractores = [op(v, e, f"${miles(v)}$ dB") for v, e in _tres_distintos(10 * k, candidatos)]
    return Propuesta(enunciado, op(10 * k, None, f"${10 * k}$ dB"), distractores, pasos,
                     lambda v: abs((10 * math.log10(10 ** k * 3.7) + 120) - (10 * math.log10(3.7) + 120) - v) < 1e-9, "baja")


# ------------------------------------------------------- Álgebra y funciones

@plantilla(ALG, "M2")
def coordenada_y_del_vertice_con_parametro(rng):
    a = rng.choice([-3, -2, -1, 1, 2, 3])
    h = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    c = rng.randrange(-9, 10)
    k = -2 * a * h
    f = lambda x: a * x * x + k * x + c
    yv = f(h)
    libre = "" if c == 0 else (f" + {c}" if c > 0 else f" - {-c}")
    enunciado = (f"Considera la función $f(x) = {polinomio([a, 0, 0])} + kx{libre}$, "
                 f"con $k$ un número real. Si la coordenada $x$ del vértice de su gráfica es ${h}$, ¿cuál es la coordenada $y$ del vértice?")
    pasos = (f"La coordenada $x$ del vértice es $-\\frac{{k}}{{2 \\cdot {par(a)}}} = {h}$, de donde $k = {k}$. Luego "
             f"$f({h}) = {par(a)} \\cdot {par(h)}^2 + {par(k)} \\cdot {par(h)} {'+ ' + str(c) if c >= 0 else '- ' + str(-c)} = {yv}$.")
    candidatos = [(f(-h), f"evalúa la función en ${-h}$ en vez de en ${h}$"),
                  (c + a * h * h, "obtiene $k$ con el signo cambiado"),
                  (c, "olvida los términos con $x$ y responde el término libre"),
                  (k, "responde el valor de $k$"),
                  (-yv, "cambia el signo del resultado")]
    distractores = [op(v, e) for v, e in _tres_distintos(yv, candidatos)]
    k_ind = Fraction(-a * ((h + 1) ** 2 - (h - 1) ** 2), 2)
    return Propuesta(enunciado, op(yv), distractores, pasos, lambda v: v == a * h * h + k_ind * h + c, "alta")


@plantilla(ALG, "M2")
def altura_maxima_de_un_lanzamiento(rng):
    a = rng.choice([2, 4, 5, 10])
    tv = rng.randrange(2, 11)
    h0 = rng.choice([0, 0, 0, 5, 10, 20])
    b = 2 * a * tv
    h = lambda t: -a * t * t + b * t + h0
    maxima = h(tv)
    objeto = rng.choice(["un cohete de juguete", "una pelota", "un proyectil de una competencia escolar"])
    f_tex = polinomio([-a, b, h0], "t")
    pregunta = rng.choice(["altura", "instante"])
    enunciado = (f"La altura, en metros, de {objeto} $t$ segundos después de ser lanzado se modela con $h(t) = {f_tex}$. ")
    if pregunta == "altura":
        enunciado += "¿Cuál es la altura máxima que alcanza?"
        pasos = (f"El máximo está en el vértice: $t = -\\frac{{{b}}}{{2 \\cdot {par(-a)}}} = {tv}$, y $h({tv}) = {maxima}$ m.")
        candidatos = [(h(2 * tv - 1) if h0 else b * tv, "multiplica el coeficiente de $t$ por el instante del vértice" if not h0 else "evalúa en un instante equivocado"),
                      (Fraction(b * b, 2 * a) + h0, "usa $\\frac{b^2}{2a}$ en vez de $\\frac{b^2}{4a}$"),
                      (tv, "responde el instante del vértice y no la altura"),
                      (h(2 * tv) + b, "confunde el máximo con el tiempo de vuelo"),
                      (maxima + a * tv * tv, "suma el término cuadrático en vez de restarlo")]
        distractores = [op(Fraction(v), e, f"${tex(v)}$ m") for v, e in _tres_distintos(Fraction(maxima), [(Fraction(v), e) for v, e in candidatos])]
        return Propuesta(enunciado, op(Fraction(maxima), None, f"${maxima}$ m"), distractores, pasos,
                         lambda v: v == max(h(Fraction(t, 4)) for t in range(0, 8 * tv + 1)), "media")
    enunciado += "¿En qué instante alcanza su altura máxima?"
    pasos = f"El máximo está en el vértice: $t = -\\frac{{{b}}}{{2 \\cdot {par(-a)}}} = {tv}$ s."
    candidatos = [(2 * tv, "calcula el instante en que vuelve a la altura inicial"),
                  (Fraction(b, a), "olvida el 2 de la fórmula del vértice"),
                  (Fraction(tv, 2), "divide dos veces por 2"),
                  (maxima, "responde la altura máxima y no el instante")]
    distractores = [op(Fraction(v), e, f"${tex(v)}$ s") for v, e in _tres_distintos(Fraction(tv), [(Fraction(v), e) for v, e in candidatos])]
    return Propuesta(enunciado, op(Fraction(tv), None, f"${tv}$ s"), distractores, pasos,
                     lambda v: h(v) == max(h(Fraction(t, 4)) for t in range(0, 8 * tv + 1)), "baja")


@plantilla(ALG, "M2")
def reflexion_de_una_funcion_cuadratica(rng):
    a = rng.choice([-3, -2, -1, 1, 2, 3])
    b = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    c = rng.choice([-7, -5, -3, -2, -1, 1, 2, 3, 5, 7])
    eje = rng.choice(["X", "Y"])
    nombres = iter(rng.sample(["g", "h", "p", "q", "r", "s"], 4))

    def texto(v):
        return f"${next(nombres)}(x) = {polinomio(list(v))}$"

    if eje == "X":
        correcto = (-a, -b, -c)
        candidatos = [((-a, b, c), "cambia el signo solo del término cuadrático"), ((a, -b, c), "refleja respecto del eje Y"),
                      ((-a, b, -c), "cambia el signo de los términos de grado par"), ((-a, -b, c), "olvida cambiar el signo del término libre")]
        pasos = f"Reflejar respecto del eje X cambia el signo de cada imagen: $-f(x) = {polinomio([-a, -b, -c])}$."
        prueba = lambda v: all(v[0] * x * x + v[1] * x + v[2] == -(a * x * x + b * x + c) for x in range(-3, 4))
    else:
        correcto = (a, -b, c)
        candidatos = [((-a, -b, -c), "refleja respecto del eje X"), ((-a, b, c), "cambia el signo solo del término cuadrático"),
                      ((a, b, -c), "cambia el signo del término libre"), ((-a, -b, c), "cambia el signo de los términos con $x$")]
        pasos = f"Reflejar respecto del eje Y reemplaza $x$ por $-x$: $f(-x) = {par(a)}(-x)^2 + {par(b)}(-x) + {par(c)} = {polinomio([a, -b, c])}$."
        prueba = lambda v: all(v[0] * x * x + v[1] * x + v[2] == a * x * x - b * x + c for x in range(-3, 4))
    enunciado = (f"Considera la función $f(x) = {polinomio([a, b, c])}$. ¿Cuál de las siguientes funciones tiene como gráfica la reflexión de "
                 f"la gráfica de $f$ con respecto al eje {eje}?")
    elegidos = _tres_distintos(correcto, candidatos)
    correcta = op(correcto, None, texto(correcto))
    distractores = [op(v, e, texto(v)) for v, e in elegidos]
    return Propuesta(enunciado, correcta, distractores, pasos, prueba, "media")


@plantilla(ALG, "M2")
def funcion_potencia_al_escalar_la_variable(rng):
    contexto = rng.choice([
        (4, "La radiación que emite un cuerpo negro, en $\\frac{\\text{W}}{\\text{m}^2}$, es proporcional a la cuarta potencia de su temperatura "
            "absoluta $T$, es decir, $R = \\sigma \\cdot T^4$, con $\\sigma$ constante.", "un cuerpo negro a {t} K emite {q}",
         "¿cuánto emite un cuerpo negro a {t2} K?", "$\\frac{\\text{W}}{\\text{m}^2}$"),
        (2, "La energía cinética de un cuerpo, en joules, se calcula como $E = \\frac{1}{2} m v^2$, con $m$ su masa y $v$ su rapidez.",
         "un carro a {t} m/s tiene una energía cinética de {q}", "¿cuál es su energía cinética a {t2} m/s?", "J"),
        (3, "La masa de una esfera maciza de cierto metal es proporcional al cubo de su radio.",
         "una esfera de {t} cm de radio tiene una masa de {q}", "¿cuál es la masa de una esfera del mismo metal de {t2} cm de radio?", "g"),
    ])
    n, intro, dato, pregunta, unidad = contexto
    t = rng.randrange(2, 9) * (100 if n == 4 else 1)
    m_ = rng.choice([2, 3]) if n < 4 else 2
    q = Fraction(rng.randrange(1000, 9999), 1000) if n == 4 else Fraction(rng.randrange(12, 400))
    correcto = q * m_ ** n
    u = f" {unidad}" if not unidad.startswith("$") else f" {unidad}"
    enunciado = (f"{intro} Si {dato.format(t=t, q=f'${_dec(q)}${u}')}, {pregunta.format(t2=t * m_)}")
    pasos = (f"Al multiplicar la variable por {m_}, el resultado se multiplica por ${m_}^{{{n}}} = {m_ ** n}$: "
             f"${_dec(q)} \\cdot {m_ ** n} = {_dec(correcto)}$.")
    candidatos = [(q * m_, f"supone que el resultado es directamente proporcional a la variable"),
                  (q * m_ * n, f"multiplica por {m_} y por el exponente {n}"),
                  (q * m_ ** (n - 1), f"eleva {m_} a {n - 1} en vez de a {n}"),
                  (q + m_ ** n, f"suma ${m_ ** n}$ en vez de multiplicar")]
    distractores = [op(v, e, f"${_dec(v)}${u}") for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, f"${_dec(correcto)}${u}"), distractores, pasos,
                     lambda v: v / Fraction(t * m_) ** n == q / Fraction(t) ** n, "media")


@plantilla(ALG, "M2")
def dos_cultivos_que_se_duplican(rng):
    da = rng.choice([10, 15, 20, 30])
    db = rng.choice([d for d in (20, 30, 40, 45, 60) if d > da])
    s = rng.randrange(1, 4)
    n0a = rng.choice([50, 100, 200, 300, 500])
    n0b = n0a * 2 ** s
    t = Fraction(s * da * db, db - da)
    if t.denominator != 1:
        raise Descartar
    enunciado = (f"En un laboratorio hay dos cultivos de bacterias. El cultivo A comienza con {n0a} bacterias y duplica su cantidad cada {da} "
                 f"minutos; el cultivo B comienza con {miles(n0b)} bacterias y duplica su cantidad cada {db} minutos. ¿Cuántos minutos después "
                 f"del inicio los dos cultivos tienen la misma cantidad de bacterias?")
    pasos = (f"Se iguala ${n0a} \\cdot 2^{{\\frac{{t}}{{{da}}}}} = {n0b} \\cdot 2^{{\\frac{{t}}{{{db}}}}}$. Como ${n0b} = {n0a} \\cdot 2^{{{s}}}$, "
             f"los exponentes cumplen $\\frac{{t}}{{{da}}} = {s} + \\frac{{t}}{{{db}}}$, de donde $t = {t}$ minutos.")
    candidatos = [(Fraction(s * (db - da)), "resta los tiempos de duplicación y multiplica por la diferencia de exponentes"),
                  (Fraction(s * da * db, db + da), "suma los tiempos de duplicación en el denominador"),
                  (Fraction(da * db, db - da), f"olvida que el cultivo B parte con $2^{{{s}}}$ veces más bacterias"),
                  (Fraction(s * db), "multiplica la diferencia de exponentes solo por el tiempo del cultivo B"),
                  (Fraction(s * da), "multiplica la diferencia de exponentes solo por el tiempo del cultivo A")]
    distractores = [op(v, e, f"${tex(v)}$") for v, e in _tres_distintos(t, candidatos)]
    return Propuesta(enunciado, op(t), distractores, pasos, lambda v: v / da == s + v / db, "alta")


# ----------------------------------------------------------------- Geometría

_TRIOS = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20), (20, 21, 29)]


@plantilla(GEO, "M2")
def altura_sobre_la_hipotenusa(rng):
    p, q, c = rng.choice(_TRIOS)
    k = rng.choice([1, 1, 2, 3])
    p, q, c = p * k, q * k, c * k
    pide = rng.choice(["altura", "proyeccion"])
    if pide == "altura":
        correcto = Fraction(p * q, c)
        enunciado = (f"En un triángulo rectángulo los catetos miden {p} cm y {q} cm. ¿Cuál es la medida de la altura trazada desde el vértice "
                     f"del ángulo recto hacia la hipotenusa?")
        pasos = (f"La hipotenusa mide $\\sqrt{{{p}^2 + {q}^2}} = {c}$ cm. El área se puede calcular con los catetos o con la hipotenusa y su altura: "
                 f"${p} \\cdot {q} = {c} \\cdot h$, luego $h = {_fraccion(p * q, c)}$ cm.")
        candidatos = [(Fraction(p * p, c), "calcula la proyección de un cateto sobre la hipotenusa"),
                      (Fraction(c, 2), "supone que la altura mide la mitad de la hipotenusa"),
                      (Fraction(p + q, 2), "promedia los catetos"),
                      (Fraction(p * q, 2 * c), "divide el área por la hipotenusa sin multiplicar por 2")]
        prueba = lambda v: v * c == p * q
    else:
        correcto = Fraction(p * p, c)
        enunciado = (f"En un triángulo rectángulo los catetos miden {p} cm y {q} cm. ¿Cuál es la medida de la proyección del cateto de {p} cm "
                     f"sobre la hipotenusa?")
        pasos = (f"La hipotenusa mide $\\sqrt{{{p}^2 + {q}^2}} = {c}$ cm. Por el teorema de Euclides, ${p}^2 = {c} \\cdot m$, luego "
                 f"$m = {_fraccion(p * p, c)}$ cm.")
        candidatos = [(Fraction(q * q, c), "calcula la proyección del otro cateto"),
                      (Fraction(p * q, c), "calcula la altura sobre la hipotenusa"),
                      (Fraction(c, 2), "supone que la proyección es la mitad de la hipotenusa"),
                      (Fraction(p, c), "divide el cateto por la hipotenusa sin elevarlo al cuadrado")]
        prueba = lambda v: v * c == p * p
    distractores = [op(v, e, f"${tex(v)}$ cm") for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, f"${tex(correcto)}$ cm"), distractores, pasos, prueba, "media")


def _pi_raiz(v) -> str:
    a, b, r = v
    return f"${tex(a)}\\pi - {tex(b)}\\sqrt{{{r}}}$" if r > 1 else f"${tex(a)}\\pi - {tex(b)}$"


@plantilla(GEO, "M2")
def area_entre_un_circulo_y_un_poligono_inscrito(rng):
    d = rng.choice([10, 12, 16, 20, 24, 30, 40, 50, 60])
    r = Fraction(d, 2)
    poligono = rng.choice(["hexágono regular", "cuadrado"])
    objeto = rng.choice(["una base circular de madera", "un plato circular", "una tapa circular"])
    if poligono == "hexágono regular":
        correcto = (r * r, 3 * r * r / 2, 3)
        candidatos = [((Fraction(d * d), 6 * Fraction(d * d) / 4, 3), "usa el diámetro como si fuera el radio"),
                      ((r * r, r * r / 4, 3), "calcula el área de un solo triángulo equilátero del hexágono"),
                      ((r * r, 3 * r * r, 3), "calcula el área de cada triángulo como $\\frac{\\sqrt{3}}{2} \\ell^2$"),
                      ((2 * r, 3 * r * r / 2, 3), "calcula el perímetro de la circunferencia en vez del área del círculo")]
        pasos = (f"El radio es {tex(r)} cm y el lado del hexágono regular inscrito es igual al radio. El hexágono se forma con 6 triángulos "
                 f"equiláteros: $6 \\cdot \\frac{{\\sqrt{{3}}}}{{4}} \\cdot {tex(r)}^2 = {tex(correcto[1])}\\sqrt{{3}}$. El área pedida es "
                 f"{_pi_raiz(correcto)} cm².")
        real = math.pi * r * r - 6 * math.sqrt(3) / 4 * r * r
    else:
        correcto = (r * r, 2 * r * r, 1)
        candidatos = [((Fraction(d * d), 2 * Fraction(d * d), 1), "usa el diámetro como si fuera el radio"),
                      ((r * r, Fraction(d * d), 1), "toma el lado del cuadrado igual al diámetro"),
                      ((r * r, r * r, 1), "toma el lado del cuadrado igual al radio"),
                      ((2 * r, 2 * r * r, 1), "calcula el perímetro de la circunferencia en vez del área del círculo")]
        pasos = (f"El radio es {tex(r)} cm y la diagonal del cuadrado inscrito es el diámetro, {d} cm, así que su área es "
                 f"$\\frac{{{d}^2}}{{2}} = {tex(correcto[1])}$. El área pedida es {_pi_raiz(correcto)} cm².")
        real = math.pi * r * r - d * d / 2
    enunciado = (f"Un adorno con forma de {poligono} está inscrito en {objeto} de {d} cm de diámetro. Se cubrirá con pintura la parte "
                 f"de la base que no tapa el adorno. ¿Cuál es el área, en cm², que se pintará?")
    distractores = [op(v, e, _pi_raiz(v)) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, _pi_raiz(correcto)), distractores, pasos,
                     lambda v: abs(float(v[0]) * math.pi - float(v[1]) * math.sqrt(v[2]) - real) < 1e-6, "media")


_ANGULOS = {30: ((1, 3, 2), (1, 1, 2)), 45: ((1, 2, 2), (1, 2, 2)), 60: ((1, 1, 2), (1, 3, 2)), 120: ((-1, 1, 2), (1, 3, 2)),
            135: ((-1, 2, 2), (1, 2, 2)), 150: ((-1, 3, 2), (1, 1, 2))}


def _coord(lado, t) -> str:
    signo, raiz, den = t
    coef = Fraction(lado, den)
    cuerpo = (tex(coef) if raiz == 1 else (f"{tex(coef) if coef != 1 else ''}\\sqrt{{{raiz}}}"))
    return f"{'-' if signo < 0 else ''}{cuerpo}"


def _coord_valor(lado, t) -> float:
    signo, raiz, den = t
    return signo * lado * math.sqrt(raiz) / den


@plantilla(GEO, "M2")
def coordenadas_de_un_punto_tras_una_rotacion(rng):
    angulo = rng.choice(list(_ANGULOS))
    lado = rng.choice([2, 4, 6, 8, 10, 12])
    cx, cy = _ANGULOS[angulo]

    def texto(v):
        return f"$({_coord(lado, v[0])}, {_coord(lado, v[1])})$"

    correcto = (cx, cy)
    negy = (cy[0] * -1, cy[1], cy[2])
    candidatos = [((cy, cx), "intercambia el seno y el coseno"),
                  ((cx, negy), "rota en sentido horario"),
                  ((cy, cx) if cx[0] > 0 else ((1, cx[1], cx[2]), cy), "intercambia el seno y el coseno" if cx[0] > 0 else "olvida el signo del coseno de un ángulo obtuso"),
                  (((-1 * cx[0], cx[1], cx[2]), cy), "se equivoca en el signo de la abscisa"),
                  (((cy[0] * -1, cy[1], cy[2]), cx), "intercambia el seno y el coseno y cambia el signo de la abscisa")]
    enunciado = (f"En el plano cartesiano, el punto $P({lado}, 0)$ se rota en torno al origen en ${angulo}^\\circ$ en sentido antihorario. "
                 f"¿Cuáles son las coordenadas del punto obtenido?")
    pasos = (f"Una rotación en torno al origen en un ángulo $\\theta$ lleva $(r, 0)$ a $(r\\cos\\theta, r\\sin\\theta)$: "
             f"$({lado}\\cos {angulo}^\\circ, {lado}\\sin {angulo}^\\circ) = {texto(correcto)[1:-1]}$.")
    rad = math.radians(angulo)
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos,
                     lambda v: abs(_coord_valor(lado, v[0]) - lado * math.cos(rad)) < 1e-9 and abs(_coord_valor(lado, v[1]) - lado * math.sin(rad)) < 1e-9,
                     "media")


@plantilla(GEO, "M2")
def tangente_y_secante_desde_un_punto_exterior(rng):
    exterior = rng.randrange(2, 13)
    cuerda = rng.randrange(2, 21)
    total = exterior + cuerda
    cuadrado = exterior * total
    enunciado = (f"Desde un punto $P$ exterior a una circunferencia se trazan una tangente $\\overline{{PT}}$, con $T$ en la circunferencia, y una "
                 f"secante que corta a la circunferencia en $A$ y $B$, con $A$ entre $P$ y $B$. Si $PA = {exterior}$ cm y $AB = {cuerda}$ cm, "
                 f"¿cuál es la medida de $\\overline{{PT}}$?")
    pasos = (f"Por la relación entre tangente y secante, $PT^2 = PA \\cdot PB = {exterior} \\cdot {total} = {cuadrado}$, luego "
             f"$PT = {raiz_tex(cuadrado)}$ cm.")
    candidatos = [(exterior * cuerda, "multiplica $PA$ por la cuerda $AB$ en vez de por la secante completa $PB$"),
                  (total * total, "toma la tangente igual a la secante completa"),
                  (cuerda * total, "multiplica la cuerda por la secante completa"),
                  (exterior * exterior + cuerda * cuerda, "aplica el teorema de Pitágoras a $PA$ y $AB$")]
    texto = lambda v: f"${raiz_tex(v)}$ cm"
    elegidos = [(v, e) for v, e in _tres_distintos(cuadrado, candidatos)]
    if len({texto(v) for v, _ in elegidos} | {texto(cuadrado)}) < 4:
        raise Descartar
    distractores = [op(v, e, texto(v)) for v, e in elegidos]
    return Propuesta(enunciado, op(cuadrado, None, texto(cuadrado)), distractores, pasos,
                     lambda v: abs(math.sqrt(v) ** 2 - exterior * (exterior + cuerda)) < 1e-9, "media")


@plantilla(GEO, "M2")
def perimetro_y_area_tras_una_homotecia(rng):
    k = rng.choice([Fraction(-3), Fraction(-2), Fraction(-1, 2), Fraction(3, 2), Fraction(2), Fraction(3), Fraction(-3, 2), Fraction(1, 3)])
    pide = rng.choice(["área", "perímetro"])
    medida = Fraction(rng.randrange(6, 61)) * (4 if pide == "área" else 2)
    unidad = "cm²" if pide == "área" else "cm"
    if pide == "área":
        correcto = k * k * medida
        candidatos = [(abs(k) * medida, "multiplica el área por la razón en vez de por su cuadrado"),
                      (-k * k * medida if k < 0 else 2 * k * medida, "conserva el signo negativo de la razón en el área" if k < 0 else "multiplica el área por el doble de la razón"),
                      (medida / (k * k), "divide por el cuadrado de la razón"),
                      (abs(k) ** 3 * medida, "eleva la razón al cubo")]
    else:
        correcto = abs(k) * medida
        candidatos = [(k * k * medida, "multiplica el perímetro por el cuadrado de la razón"),
                      (k * medida, "conserva el signo negativo de la razón en el perímetro") if k < 0 else (medida + k, "suma la razón en vez de multiplicar"),
                      (medida / abs(k), "divide por la razón"),
                      (medida, "supone que la homotecia conserva las medidas"),
                      (medida + abs(k), "suma la razón en vez de multiplicar")]
    enunciado = (f"A un triángulo de {pide} ${tex(medida)}$ {unidad} se le aplica una homotecia de razón ${tex(k)}$. ¿Cuál es el {pide} del "
                 f"triángulo homotético?")
    pasos = (f"Una homotecia de razón $k$ multiplica las longitudes por $|k| = {tex(abs(k))}$ y las áreas por $k^2 = {tex(k * k)}$; el signo solo "
             f"indica que la figura queda al otro lado del centro. El {pide} es ${tex(correcto)}$ {unidad}.")
    texto = lambda v: f"${tex(v)}$ {unidad}"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if v > 0 or True])]
    lado = [Fraction(3), Fraction(4), Fraction(5)]
    perimetro_base, area_base = sum(lado), Fraction(6)
    factor = (sum(abs(k) * x for x in lado) / perimetro_base) if pide == "perímetro" else (Fraction(1, 2) * abs(k) * 3 * abs(k) * 4) / area_base
    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos, lambda v: v == factor * medida, "media")


# ------------------------------------------------- Probabilidad y estadística

@plantilla(PRO, "M2")
def condicional_desde_ambos_y_solo_uno(rng):
    a = Fraction(rng.randrange(5, 40, 5), 100)
    b = Fraction(rng.randrange(10, 70, 5), 100)
    if a + b >= Fraction(95, 100):
        raise Descartar
    solo_otro = 1 - a - b
    x, y = rng.choice([("vainilla", "chocolate"), ("fútbol", "básquetbol"), ("inglés", "francés"), ("perros", "gatos")])
    tema = {"vainilla": "sabores de helado", "fútbol": "deportes", "inglés": "idiomas", "perros": "mascotas"}[x]
    enunciado = (f"Se encuestó a un grupo de estudiantes sobre dos {tema}, {x} y {y}, y todos eligieron al menos uno. Al escoger un estudiante "
                 f"al azar, la probabilidad de que elija ambos es ${_dec(a)}$ y la probabilidad de que elija solo {y} es ${_dec(b)}$. Si se escoge "
                 f"un estudiante al azar, ¿cuál es la probabilidad de que elija {y} dado que eligió {x}?")
    p_x = 1 - b
    correcto = a / p_x
    pasos = (f"Como todos eligen al menos uno, $P(\\text{{{x}}}) = 1 - P(\\text{{solo {y}}}) = 1 - {_dec(b)} = {_dec(p_x)}$. Luego "
             f"$P(\\text{{{y}}} \\mid \\text{{{x}}}) = \\frac{{{_dec(a)}}}{{{_dec(p_x)}}} = {frac(correcto)}$.")
    candidatos = [(a / (a + b), f"calcula la probabilidad de {x} dado {y}"),
                  (a / solo_otro, f"divide por la probabilidad de elegir solo {x}"),
                  (a, "responde la probabilidad de elegir ambos"),
                  (a / (1 - a), "divide por la probabilidad de no elegir ambos")]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if 0 < v < 1])]
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v * (a + solo_otro) == a, "alta")


@plantilla(PRO, "M2")
def probabilidad_de_ganar_una_loteria(rng):
    n = rng.choice([30, 36, 40, 45, 50, 60, 80, 99])
    k = rng.choice([2, 3])
    factores = " \\cdot ".join(str(n - i) for i in range(k))
    perm = math.perm(n, k)
    comb = math.comb(n, k)
    enunciado = (f"En un sorteo cada cartón tiene {k} números distintos del 1 al {n}. Se gana si los {k} números sorteados, que no se repiten "
                 f"y cuyo orden no importa, coinciden con los del cartón. ¿Cuál es la probabilidad de ganar con un cartón?")
    textos = {
        "correcta": f"$\\frac{{{math.factorial(k)}}}{{{factores}}}$",
        "orden": f"$\\frac{{1}}{{{factores}}}$",
        "k": f"$\\frac{{{k}}}{{{factores}}}$",
        "reposicion": f"$\\frac{{1}}{{{n}^{{{k}}}}}$",
        "suma": f"$\\frac{{{k}}}{{{n}}}$",
    }
    valores = {"correcta": Fraction(1, comb), "orden": Fraction(1, perm), "k": Fraction(k, perm), "reposicion": Fraction(1, n ** k),
               "suma": Fraction(k, n)}
    errores = {"orden": "considera que importa el orden en que salen los números",
               "k": f"multiplica por {k} en vez de por ${k}!$" if k == 3 else "considera que importa el orden en que salen los números y suma un caso",
               "reposicion": "supone que los números se pueden repetir",
               "suma": "suma las probabilidades de acertar cada número"}
    if k == 2:
        del valores["k"]
    pasos = (f"Hay $\\binom{{{n}}}{{{k}}} = \\frac{{{factores}}}{{{k}!}} = {miles(comb)}$ resultados posibles igualmente probables y uno solo es "
             f"favorable: $P = \\frac{{{k}!}}{{{factores}}}$.")
    claves = [c for c in ("orden", "k", "reposicion", "suma") if c in valores]
    rng.shuffle(claves)
    elegidos = _tres_distintos(valores["correcta"], [(valores[c], c) for c in claves])
    distractores = [op(v, errores[c], textos[c]) for v, c in elegidos]
    casos = sum(1 for _ in itertools.combinations(range(n), k)) if n <= 60 else comb
    return Propuesta(enunciado, op(valores["correcta"], None, textos["correcta"]), distractores, pasos, lambda v: v == Fraction(1, casos), "media")


@plantilla(PRO, "M2")
def orden_al_azar_con_condicion_en_los_extremos(rng):
    n = rng.randrange(5, 9)
    condicion = rng.choice(["par", "impar", "mixto"])
    pares = n // 2
    impares = n - pares
    if condicion == "par":
        fav = pares * (pares - 1)
        texto_cond = "comience y termine con un número par"
    elif condicion == "impar":
        fav = impares * (impares - 1)
        texto_cond = "comience y termine con un número impar"
    else:
        fav = pares * impares
        texto_cond = "comience con un número par y termine con un número impar"
    correcto = Fraction(fav, n * (n - 1))
    enunciado = (f"Se tienen {n} fichas numeradas del 1 al {n}, todas iguales salvo el número, y se ordenan en fila al azar. ¿Cuál es la "
                 f"probabilidad de que la fila {texto_cond}?")
    cuenta_ext = {"par": pares, "impar": impares, "mixto": pares}[condicion]
    segunda = {"par": pares - 1, "impar": impares - 1, "mixto": impares}[condicion]
    pasos = (f"Solo importan las fichas de los extremos: la primera puede ser cualquiera de las {n} y la última cualquiera de las {n - 1} restantes. "
             f"Los casos favorables son ${cuenta_ext} \\cdot {segunda} = {fav}$, así que $P = {_fraccion(fav, n * (n - 1))}$.")
    candidatos = [(Fraction(cuenta_ext * (segunda + (0 if condicion == 'mixto' else 1)), n * n), "supone que la misma ficha puede quedar en ambos extremos"),
                  (Fraction(cuenta_ext, n), "considera solo el primer extremo"),
                  (Fraction(cuenta_ext + segunda, n), "suma las probabilidades de cada extremo"),
                  (Fraction(fav, math.factorial(n)), f"divide por las ${n}!$ filas posibles sin contar el orden de las fichas del centro")]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if 0 < v < 1])]
    filas = list(itertools.permutations(range(1, n + 1)))

    def cumple(f):
        if condicion == "par":
            return f[0] % 2 == 0 and f[-1] % 2 == 0
        if condicion == "impar":
            return f[0] % 2 == 1 and f[-1] % 2 == 1
        return f[0] % 2 == 0 and f[-1] % 2 == 1

    real = Fraction(sum(1 for f in filas if cumple(f)), len(filas))
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == real, "alta")


def _fraccion(num, den) -> str:
    cruda = f"\\frac{{{num}}}{{{den}}}"
    final = frac(Fraction(num, den))
    return cruda if final == cruda else f"{cruda} = {final}"


def _varianza(datos):
    media = Fraction(sum(datos), len(datos))
    return sum((x - media) ** 2 for x in datos) / len(datos)


@plantilla(PRO, "M2")
def medidas_tras_transformar_los_datos(rng):
    a = rng.choice([2, 3, 4, 5, Fraction(1, 2)])
    b = rng.choice([-10, -5, 3, 5, 10, 20])
    pide = rng.choice(["varianza", "desviación estándar", "promedio"])
    valor = Fraction(rng.randrange(2, 30))
    contexto = rng.choice(["las notas de un curso", "los sueldos de una empresa, en miles de pesos", "las estaturas de un grupo, en cm"])
    nombre = {"varianza": "la varianza", "desviación estándar": "la desviación estándar", "promedio": "el promedio"}[pide]
    enunciado = (f"En {contexto}, {nombre} de los datos es ${tex(valor)}$. Si cada dato se multiplica por ${tex(a)}$ y luego se le suma ${b}$, "
                 f"¿cuál es {nombre} de los nuevos datos?")
    if pide == "varianza":
        correcto = a * a * valor
        candidatos = [(a * valor, "multiplica la varianza por el factor y no por su cuadrado"), (a * a * valor + b, "suma la constante a la varianza"),
                      (a * valor + b, "aplica a la varianza la misma transformación que a los datos"), (a * a * valor + b * b, "suma el cuadrado de la constante")]
        pasos = f"Sumar una constante no cambia la dispersión y multiplicar por ${tex(a)}$ multiplica la varianza por ${tex(a)}^2$: ${tex(correcto)}$."
        transformar = lambda d: _varianza(d)
    elif pide == "desviación estándar":
        correcto = a * valor
        candidatos = [(a * a * valor, "multiplica la desviación estándar por el cuadrado del factor"), (a * valor + b, "suma la constante a la desviación estándar"),
                      (valor + b, "suma la constante y olvida el factor"), (valor, "supone que la desviación estándar no cambia")]
        pasos = f"Sumar una constante no cambia la dispersión y multiplicar por ${tex(a)}$ multiplica la desviación estándar por ${tex(a)}$: ${tex(correcto)}$."
        transformar = None
    else:
        correcto = a * valor + b
        candidatos = [(a * valor, "olvida sumar la constante"), (a * (valor + b), "suma la constante antes de multiplicar"),
                      (valor + b, "olvida multiplicar"), (a * a * valor + b, "multiplica por el cuadrado del factor")]
        pasos = f"El promedio sigue la misma transformación que los datos: ${tex(a)} \\cdot {tex(valor)} + {par(b)} = {tex(correcto)}$."
        transformar = lambda d: Fraction(sum(d), len(d))
    distractores = [op(v, e) for v, e in _tres_distintos(correcto, candidatos)]

    def comprobar(v):
        if pide == "desviación estándar":
            base = [Fraction(0), Fraction(2) * valor]
            nuevos = [a * x + b for x in base]
            return v * v == _varianza(nuevos)
        if pide == "varianza":
            base = [Fraction(0), Fraction(2)]
            escala = valor / _varianza(base)
            return v == _varianza([a * x + b for x in base]) * escala
        base = [valor - 3, valor, valor + 3]
        return v == transformar([a * x + b for x in base])

    return Propuesta(enunciado, op(correcto), distractores, pasos, comprobar, "media")


@plantilla(PRO, "M2")
def ganancia_esperada_de_un_juego(rng):
    premio_alto = rng.choice([3000, 4000, 5000, 6000])
    premio_bajo = rng.choice([500, 1000, 1500])
    costo = rng.choice([500, 1000, 1500, 2000])
    caras_alto = [6]
    caras_bajo = rng.choice([[4, 5], [5], [3, 4, 5]])
    n_alto, n_bajo = len(caras_alto), len(caras_bajo)
    n_pierde = 6 - n_alto - n_bajo
    esperado = Fraction(n_alto * premio_alto + n_bajo * premio_bajo - n_pierde * costo, 6)
    if esperado.denominator != 1:
        raise Descartar
    bajo_txt = " o ".join(str(c) for c in caras_bajo) if n_bajo < 3 else "3, 4 o 5"
    enunciado = (f"En un juego se lanza un dado común. Si sale 6 se ganan {pesos(premio_alto)}; si sale {bajo_txt} se ganan {pesos(premio_bajo)}, "
                 f"y en cualquier otro caso se pierden {pesos(costo)}. ¿Cuál es la ganancia esperada por lanzamiento?")
    pasos = (f"$E = \\frac{{{n_alto}}}{{6}} \\cdot {premio_alto} + \\frac{{{n_bajo}}}{{6}} \\cdot {premio_bajo} - \\frac{{{n_pierde}}}{{6}} \\cdot {costo} = "
             f"{tex(esperado)}$ pesos.")

    def texto(v):
        v = Fraction(v)
        cuerpo = f"\\text{{\\textdollar}}\\,{tex(abs(v))}"
        return f"${'-' if v < 0 else ''}{cuerpo}$"

    candidatos = [(Fraction(n_alto * premio_alto + n_bajo * premio_bajo + n_pierde * costo, 6), "suma la pérdida en vez de restarla"),
                  (Fraction(premio_alto + premio_bajo - costo, 3), "promedia los tres montos sin considerar sus probabilidades"),
                  (Fraction(n_alto * premio_alto + n_bajo * premio_bajo, 6), "olvida los casos en que se pierde"),
                  (Fraction(premio_alto + premio_bajo - costo), "suma los montos sin ponderarlos")]
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(esperado, [(v, e) for v, e in candidatos if v.denominator == 1])]
    real = sum(Fraction(premio_alto if c in caras_alto else premio_bajo if c in caras_bajo else -costo, 6) for c in range(1, 7))
    return Propuesta(enunciado, op(esperado, None, texto(esperado)), distractores, pasos, lambda v: v == real, "media")

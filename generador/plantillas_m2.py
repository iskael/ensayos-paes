"""Plantillas de nivel M2, con los contenidos propios del temario de Competencia Matemática 2 (DEMRE, admisión 2026).

Tipos tomados de las PAES M2 Regular e Invierno de admisión 2024 a 2026. Quedan fuera las preguntas de
suficiencia de datos, porque usan cinco alternativas fijas y la app trabaja con cuatro.
"""
from __future__ import annotations

import math
from fractions import Fraction

import figuras
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


def _fraccion_cruda(num, den) -> str:
    cruda = f"\\frac{{{num}}}{{{den}}}"
    final = frac(Fraction(num, den))
    return cruda if final == cruda else f"{cruda} = {final}"


# ----------------------------------------------------------------- Números

@plantilla(NUM, "M2")
def suma_de_logaritmos_exactos(rng):
    b1, b2 = rng.sample([2, 3, 4, 5, 10], 2)
    e1 = rng.randrange(2, 6)
    e2 = rng.choice([-3, -2, -1, 2, 3])
    arg1 = b1 ** e1
    arg2 = Fraction(b2) ** e2
    correcto = e1 + e2
    texto2 = tex(arg2) if arg2.denominator == 1 else f"\\frac{{1}}{{{arg2.denominator}}}"
    enunciado = f"¿Cuál es el valor de $\\log_{{{b1}}} {arg1} + \\log_{{{b2}}} {texto2}$?"
    pasos = (f"$\\log_{{{b1}}} {arg1} = {e1}$ porque ${b1}^{{{e1}}} = {arg1}$, y $\\log_{{{b2}}} {texto2} = {e2}$ porque "
             f"${b2}^{{{e2}}} = {texto2}$. La suma es ${e1} + {par(e2)} = {correcto}$.")
    candidatos = [
        (e1 - e2, "se equivoca en el signo del segundo logaritmo"),
        (e1 + abs(e2) if e2 < 0 else e1 * e2, "trata el logaritmo de una fracción como positivo" if e2 < 0 else "multiplica los logaritmos en vez de sumarlos"),
        (Fraction(arg1, b1) + (arg2 / b2), "divide cada argumento por su base en vez de buscar el exponente"),
        (e1 * e2, "multiplica los logaritmos en vez de sumarlos"),
    ]
    distractores = [op(Fraction(v), e) for v, e in _tres_distintos(Fraction(correcto), [(Fraction(v), e) for v, e in candidatos])]
    return Propuesta(enunciado, op(Fraction(correcto)), distractores, pasos,
                     lambda v: abs(float(v) - (math.log(arg1, b1) + math.log(float(arg2), b2))) < 1e-9, "baja")


@plantilla(NUM, "M2")
def logaritmo_en_terminos_de_otros(rng):
    a, b = 2, 3
    i, j = rng.randrange(1, 4), rng.randrange(1, 3)
    if i + j < 3:
        raise Descartar
    n = a ** i * b ** j
    division = rng.random() < 0.4
    if division:
        d = rng.choice([5, 10])
        enunciado_arg = f"\\frac{{{n}}}{{{d}}}"
    enunciado = (f"Si $\\log 2 = p$ y $\\log 3 = q$, ¿cuál de las siguientes expresiones es igual a $\\log {n}$?"
                 if not division else
                 f"Si $\\log 2 = p$, $\\log 3 = q$ y $\\log 5 = r$, ¿cuál de las siguientes expresiones es igual a $\\log {enunciado_arg}$?")
    factores = f"{n} = 2^{{{i}}} \\cdot 3^{{{j}}}"

    def expr(cp, cq, cr=0):
        partes = []
        for c, letra in ((cp, "p"), (cq, "q"), (cr, "r")):
            if c:
                signo = "-" if c < 0 else ("+" if partes else "")
                cuerpo = "" if abs(c) == 1 else str(abs(c))
                partes.append(f"{' ' if partes else ''}{signo}{' ' if partes else ''}{cuerpo}{letra}")
        return "$" + "".join(partes).strip() + "$"

    if not division:
        correcta = op((i, j, 0), None, expr(i, j))
        pasos = f"Se descompone ${factores}$. Por las propiedades del logaritmo, $\\log {n} = {i}\\log 2 + {j}\\log 3 = {expr(i, j)[1:-1]}$."
        candidatos = [((j, i, 0), "intercambia los exponentes de 2 y de 3"), ((i * j, 0, 0), "multiplica los exponentes"),
                      ((1, 1, 0), "olvida los exponentes de la descomposición"), ((i + j, i + j, 0), "suma los exponentes y los asigna a ambos logaritmos")]
        comprobar = lambda v: abs(v[0] * math.log10(2) + v[1] * math.log10(3) + v[2] * math.log10(5) - math.log10(n)) < 1e-9
    else:
        cr = -1 if d == 5 else -1
        cp_extra = -1 if d == 10 else 0
        cp, cq = i + cp_extra, j
        if d == 10:
            pasos = (f"Se descompone ${factores}$ y $10 = 2 \\cdot 5$. Entonces $\\log \\frac{{{n}}}{{10}} = "
                     f"{expr(i, j)[1:-1]} - (p + r) = {expr(cp, cq, -1)[1:-1]}$.")
        else:
            pasos = f"Se descompone ${factores}$. Entonces $\\log \\frac{{{n}}}{{5}} = {expr(i, j, -1)[1:-1]}$."
        correcta = op((cp, cq, -1), None, expr(cp, cq, -1))
        candidatos = [((cp, cq, 1), "suma el logaritmo de 5 en vez de restarlo"),
                      ((i, j, 1), "olvida restar el logaritmo de 2 y además suma el de 5"),
                      ((i, j, -1), "descompone 10 como si fuera solo 5") if d == 10 else ((i, j, -5), "resta 5r en vez de r"),
                      ((j, i, -1), "intercambia los exponentes de 2 y de 3"),
                      ((i * j, 0, -1), "multiplica los exponentes")]
        comprobar = lambda v: abs(v[0] * math.log10(2) + v[1] * math.log10(3) + v[2] * math.log10(5) - math.log10(n / d)) < 1e-9
    elegidos = _tres_distintos(correcta.valor, candidatos)
    distractores = [op(v, e, expr(*v)) for v, e in elegidos]
    return Propuesta(enunciado, correcta, distractores, pasos, comprobar, "media")


@plantilla(NUM, "M2")
def capital_con_interes_compuesto(rng):
    capital = rng.randrange(1, 21) * 100000
    tasa = rng.choice([1, 2, 3, 4, 5, 10])
    periodos = rng.randrange(2, 5)
    final = Fraction(capital) * Fraction(100 + tasa, 100) ** periodos
    unidad = rng.choice(["mensual", "anual"])
    plural = "meses" if unidad == "mensual" else "años"
    enunciado = (f"Se depositan {pesos(capital)} en una cuenta de ahorro con un interés compuesto {unidad} de un {tasa} %. Si no se hacen "
                 f"retiros ni otros depósitos, ¿cuál de las siguientes expresiones representa el dinero en la cuenta al cabo de "
                 f"{periodos} {plural}, en pesos?")
    pasos = (f"Con interés compuesto, cada período el capital se multiplica por $1 + \\frac{{{tasa}}}{{100}} = {tex(Fraction(100 + tasa, 100))}$. "
             f"Al cabo de {periodos} {plural}: ${miles(capital)} \\cdot {tex(Fraction(100 + tasa, 100))}^{{{periodos}}}$.")
    factor = tex(Fraction(100 + tasa, 100))

    def alt(valor, texto, error=None):
        return op(Fraction(valor), error, f"${texto}$")

    distractores = [
        alt(capital * (1 + Fraction(tasa * periodos, 100)), f"{miles(capital)} \\cdot (1 + {tex(Fraction(tasa * periodos, 100))})",
            "aplica interés simple: suma el interés de cada período sobre el capital inicial"),
        alt(capital * Fraction(100 + tasa, 100) * periodos, f"{miles(capital)} \\cdot {factor} \\cdot {periodos}",
            "multiplica por la cantidad de períodos en vez de elevar"),
        alt(capital * Fraction(tasa, 100) ** periodos, f"{miles(capital)} \\cdot {tex(Fraction(tasa, 100))}^{{{periodos}}}",
            "eleva solo la tasa, sin sumar el 1 que conserva el capital"),
    ]
    return Propuesta(enunciado, alt(final, f"{miles(capital)} \\cdot {factor}^{{{periodos}}}"), distractores, pasos,
                     lambda v: v == capital * (1 + Fraction(tasa, 100)) ** periodos, "media")


@plantilla(NUM, "M2")
def orden_de_numeros_con_raices(rng):
    while True:
        cuadrados = rng.sample([2, 3, 5, 6, 7], 3)
        coefs = [rng.randrange(2, 6) for _ in range(3)]
        valores = [c * c * r for c, r in zip(coefs, cuadrados)]
        if len(set(valores)) == 3:
            break
    nombres = ["p", "q", "r"]
    textos = [f"{c}\\sqrt{{{r}}}" for c, r in zip(coefs, cuadrados)]
    enunciado = (f"Si $p = {textos[0]}$, $q = {textos[1]}$ y $r = {textos[2]}$, ¿cuál de las siguientes opciones muestra los "
                 f"números ordenados de menor a mayor?")
    orden = sorted(range(3), key=lambda k: valores[k])
    pasos = ("Se comparan los cuadrados: " + ", ".join(f"${nombres[k]}^{{2}} = {coefs[k]}^{{2}} \\cdot {cuadrados[k]} = {valores[k]}$" for k in range(3))
             + f". Como los tres son positivos, el orden de los cuadrados es el mismo: ${' < '.join(nombres[k] for k in orden)}$.")

    def alt(perm, error=None):
        return op(tuple(perm), error, "$" + " < ".join(nombres[k] for k in perm) + "$")

    por_coef = tuple(sorted(range(3), key=lambda k: (coefs[k], cuadrados[k])))
    por_radicando = tuple(sorted(range(3), key=lambda k: (cuadrados[k], coefs[k])))
    candidatos = [(por_coef, "ordena según el número que está fuera de la raíz"),
                  (por_radicando, "ordena según el número que está dentro de la raíz"),
                  (tuple(reversed(orden)), "ordena de mayor a menor"),
                  (tuple(orden[1:] + orden[:1]), "compara bien dos de los números pero ubica mal el tercero"),
                  (tuple([orden[1], orden[0], orden[2]]), "compara bien dos de los números pero ubica mal el tercero")]
    distractores = [alt(v, e) for v, e in _tres_distintos(tuple(orden), candidatos)]
    return Propuesta(enunciado, alt(orden), distractores, pasos,
                     lambda v: [c * math.sqrt(r) for c, r in (zip(*[[coefs[k] for k in v], [cuadrados[k] for k in v]]))] ==
                     sorted(c * math.sqrt(r) for c, r in zip(coefs, cuadrados)), "media")


@plantilla(NUM, "M2")
def potencia_de_exponente_fraccionario(rng):
    base, n, m_ = rng.choice([(8, 3, 2), (27, 3, 2), (16, 4, 3), (32, 5, 2), (81, 4, 3), (125, 3, 2), (64, 3, 2), (64, 6, 5),
                              (4, 2, 3), (9, 2, 3), (25, 2, 3), (16, 2, 3)])
    raiz = round(base ** (1 / n))
    if raiz ** n != base:
        raise Descartar
    negativo = rng.random() < 0.35
    correcto = Fraction(raiz ** m_) if not negativo else Fraction(1, raiz ** m_)
    exponente = f"{'-' if negativo else ''}\\frac{{{m_}}}{{{n}}}"
    enunciado = f"¿Cuál es el valor de ${base}^{{{exponente}}}$?"
    pasos = (f"${base}^{{\\frac{{{m_}}}{{{n}}}}} = (\\sqrt[{n}]{{{base}}})^{{{m_}}} = {raiz}^{{{m_}}} = {raiz ** m_}$"
             + (f". Por el signo negativo del exponente, el resultado es el recíproco: ${frac(correcto)}$." if negativo else "."))
    candidatos = [
        (Fraction(base * m_, n), "multiplica la base por el exponente"),
        (-correcto if negativo else Fraction(1, raiz ** m_), "trata el exponente negativo como un signo negativo del resultado" if negativo else "toma el recíproco aunque el exponente es positivo"),
        (Fraction(round(base ** (1 / m_)) ** n) if round(base ** (1 / m_)) ** m_ == base else Fraction(raiz * m_), "intercambia el índice de la raíz con la potencia" if round(base ** (1 / m_)) ** m_ == base else f"multiplica la raíz por {m_} en vez de elevarla"),
        (Fraction(raiz * m_) if not negativo else Fraction(1, raiz * m_), f"multiplica la raíz por {m_} en vez de elevarla"),
        (Fraction(raiz), "calcula la raíz y olvida elevarla"),
    ]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: abs(float(v) - base ** ((-1 if negativo else 1) * m_ / n)) < 1e-9, "media")


# ------------------------------------------------------- Álgebra y funciones

@plantilla(ALG, "M2")
def sistema_sin_solucion_o_infinitas(rng):
    a, b = rng.choice([(1, 2), (2, 3), (1, 3), (3, 2), (2, 5), (1, 4), (3, 4)])
    k = rng.choice([2, 3, 4])
    c = rng.randrange(1, 10)
    d_igual = k * c
    caso = rng.choice(["sin", "infinitas"])
    pide = "no tenga solución" if caso == "sin" else "tenga infinitas soluciones"
    if caso == "sin":
        d = d_igual + rng.choice([-3, -2, -1, 1, 2, 3])
        enunciado = (f"¿Para qué valor de $m$ el sistema $\\begin{{cases}} {polinomio([a, 0])} + {b}y = {c} \\\\ {k * a}x + my = {d} \\end{{cases}}$ "
                     f"no tiene solución?")
        pasos = (f"El sistema no tiene solución cuando las rectas son paralelas y distintas: los coeficientes de $x$ e $y$ deben ser "
                 f"proporcionales y los términos libres no. La segunda ecuación tiene ${k * a}x$, es decir, {k} veces ${polinomio([a, 0])}$, así que "
                 f"$m = {k} \\cdot {b} = {k * b}$. Con ese valor, ${d} \\neq {k} \\cdot {c}$, de modo que las rectas no coinciden.")
    else:
        d = d_igual
        enunciado = (f"¿Para qué valor de $m$ el sistema $\\begin{{cases}} {polinomio([a, 0])} + {b}y = {c} \\\\ {k * a}x + my = {d} \\end{{cases}}$ "
                     f"tiene infinitas soluciones?")
        pasos = (f"Hay infinitas soluciones cuando ambas ecuaciones representan la misma recta: la segunda debe ser {k} veces la primera. "
                 f"Como ${k} \\cdot {c} = {d}$ y ${k} \\cdot {polinomio([a, 0])} = {k * a}x$, se necesita $m = {k} \\cdot {b} = {k * b}$.")
    correcto = k * b
    candidatos = [(b, "usa el mismo coeficiente de $y$, sin aplicar la proporción entre las ecuaciones"),
                  (Fraction(b, k), f"divide por {k} en vez de multiplicar"),
                  (-k * b, "cambia el signo del coeficiente"),
                  (k * a, "copia el coeficiente de $x$ de la segunda ecuación")]
    distractores = [op(Fraction(v), e) for v, e in _tres_distintos(Fraction(correcto), [(Fraction(v), e) for v, e in candidatos])]

    def comprobar(v):
        det = a * v - b * k * a
        if det != 0:
            return False
        proporcional = Fraction(d, c) == k
        return proporcional if caso == "infinitas" else not proporcional

    return Propuesta(enunciado, op(Fraction(correcto)), distractores, pasos, comprobar, "alta")


@plantilla(ALG, "M2")
def crecimiento_exponencial_en_una_tabla(rng):
    factor = rng.choice([2, 3, 4])
    nombre = {2: "se duplica", 3: "se triplica", 4: "se cuadruplica"}[factor]
    inicial = Fraction(rng.choice([1, 2, 3, 5]), rng.choice([1, 2, 4, 10]))
    dias = rng.randrange(3, 7)
    correcto = inicial * factor ** dias
    que = rng.choice([("la masa de un cultivo bacteriano", "kg"), ("la cantidad de seguidores de un video, en miles", "miles"),
                      ("la superficie, en metros cuadrados, que cubre un alga", "m²")])
    enunciado = (f"En un laboratorio se observa que {que[0]} {nombre} cada día. Si al comenzar la observación el valor es "
                 f"${tex(inicial)}$, ¿cuál es el valor al cabo de {dias} días?")
    pasos = (f"El valor se modela con $M(t) = {tex(inicial)} \\cdot {factor}^{{t}}$. Para $t = {dias}$: "
             f"${tex(inicial)} \\cdot {factor}^{{{dias}}} = {tex(inicial)} \\cdot {factor ** dias} = {tex(correcto)}$.")
    candidatos = [(inicial * factor * dias, "multiplica por el factor y por los días, como si el crecimiento fuera lineal"),
                  (inicial + factor * dias, "suma el crecimiento en vez de multiplicar"),
                  (inicial * factor ** (dias - 1), "eleva a un día menos"),
                  (inicial * dias ** factor, "intercambia la base con el exponente")]
    distractores = [op(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v / inicial == factor ** dias, "media")


@plantilla(ALG, "M2")
def traslacion_de_una_parabola(rng):
    b = rng.choice([n for n in range(-6, 7) if n != 0])
    c = rng.choice([n for n in range(-8, 9) if n != 0])
    k = rng.randrange(2, 7)
    direccion = rng.choice(["derecha", "izquierda", "arriba", "abajo"])
    original = polinomio([1, b, c])
    if direccion in ("derecha", "izquierda"):
        h = k if direccion == "derecha" else -k
        nueva = (1, b - 2 * h, h * h - b * h + c)
        pasos = (f"Trasladar {k} unidades hacia la {direccion} equivale a reemplazar $x$ por $x {'-' if h > 0 else '+'} {k}$: "
                 f"$g(x) = (x {'-' if h > 0 else '+'} {k})^{{2}} {'+' if b > 0 else '-'} {abs(b)}(x {'-' if h > 0 else '+'} {k}) "
                 f"{'+' if c > 0 else '-'} {abs(c)} = {polinomio(list(nueva))}$.")
        malos = [((1, b + 2 * h, h * h + b * h + c), "traslada hacia el lado contrario: reemplaza $x$ con el signo cambiado"),
                 ((1, b, c - h if direccion == "derecha" else c + k), "traslada verticalmente en vez de horizontalmente"),
                 ((1, b - h, c), "solo modifica el término en $x$")]
        evaluar = lambda x: (x - h) ** 2 + b * (x - h) + c
        dificultad = "alta"
    else:
        v = k if direccion == "arriba" else -k
        nueva = (1, b, c + v)
        pasos = f"Trasladar {k} unidades hacia {direccion} suma ${v}$ a la función: $g(x) = {original} {'+' if v > 0 else '-'} {k} = {polinomio(list(nueva))}$."
        malos = [((1, b, c - v), "suma en el sentido contrario"),
                 ((1, b - 2 * v, v * v - b * v + c), "traslada horizontalmente en vez de verticalmente"),
                 ((1, b + v, c), "suma la traslación al término en $x$")]
        evaluar = lambda x: x * x + b * x + c + v
        dificultad = "media"

    def alt(coefs, error=None):
        return op(tuple(coefs), error, f"$g(x) = {polinomio(list(coefs))}$")

    enunciado = (f"Considera la función $f(x) = {original}$. ¿Cuál de las siguientes funciones tiene como gráfica la parábola de $f$ "
                 f"trasladada {k} unidades hacia {'la ' if direccion in ('derecha', 'izquierda') else ''}{direccion}?")
    distractores = [alt(c_, e) for c_, e in _tres_distintos(nueva, malos)]
    return Propuesta(enunciado, alt(nueva), distractores, pasos,
                     lambda q: all(q[0] * x * x + q[1] * x + q[2] == evaluar(x) for x in (0, 1, 2)), dificultad)


SENOS = {0: (0, 1), 30: (1, 2), 45: (2, 2), 60: (3, 2), 90: (1, 1)}


def _seno_exacto(grados):
    grados %= 360
    signo = 1
    if grados > 180:
        signo, grados = -1, grados - 180
    if grados > 90:
        grados = 180 - grados
    r, d = SENOS[grados]
    return signo, r, d


def _texto_raiz(coef, r, d, signo):
    if coef * signo == 0 or r == 0:
        return "0"
    valor_signo = "-" if coef * signo < 0 else ""
    v = Fraction(abs(coef), d)
    if r == 1:
        return f"{valor_signo}{frac(v)}"
    numerador = f"{'' if v.numerator == 1 else v.numerator}\\sqrt{{{r}}}"
    return f"{valor_signo}\\frac{{{numerador}}}{{{v.denominator}}}" if v.denominator != 1 else f"{valor_signo}{numerador}"


@plantilla(ALG, "M2")
def valor_de_una_funcion_trigonometrica(rng):
    a = rng.choice([2, 3, 4, 5, 6])
    funcion = rng.choice(["sen", "cos"])
    desfase = rng.choice([0, 180])
    angulo = rng.choice([30, 45, 60, 120, 135, 150])
    desfase_txt = "" if desfase == 0 else " + \\pi"
    nombres_pi = {30: "\\frac{\\pi}{6}", 45: "\\frac{\\pi}{4}", 60: "\\frac{\\pi}{3}", 120: "\\frac{2\\pi}{3}",
                  135: "\\frac{3\\pi}{4}", 150: "\\frac{5\\pi}{6}"}
    total = angulo + desfase + (0 if funcion == "sen" else 90)
    signo, r, d = _seno_exacto(total)
    valor = a * signo * (math.sqrt(r) / d if r != 1 else 1 / d)
    texto = _texto_raiz(a, r, d, signo)
    enunciado = f"Considera la función $f(x) = {a}\\,\\text{{{funcion}}}(x{desfase_txt})$. ¿Cuál es el valor de $f\\left({nombres_pi[angulo]}\\right)$?"
    pasos = (f"$f\\left({nombres_pi[angulo]}\\right) = {a}\\,\\text{{{funcion}}}\\left({nombres_pi[angulo]}{desfase_txt}\\right)$. "
             + ("Sumar $\\pi$ cambia el signo del seno y del coseno. " if desfase else "")
             + f"El resultado es ${texto}$.")
    s_sin, r_sin, d_sin = _seno_exacto(angulo + desfase + (90 if funcion == "sen" else 0))
    s_sd, r_sd, d_sd = _seno_exacto(angulo + (0 if funcion == "sen" else 90))
    candidatos = [
        (round(-valor, 9), _texto_raiz(a, r, d, -signo), "se equivoca en el signo" if not desfase else "no considera que sumar $\\pi$ cambia el signo"),
        (round(a * s_sin * (math.sqrt(r_sin) / d_sin if r_sin != 1 else 1 / d_sin), 9), _texto_raiz(a, r_sin, d_sin, s_sin),
         "confunde el seno con el coseno"),
        (round(valor / a, 9), _texto_raiz(1, r, d, signo), f"olvida multiplicar por {a}"),
        (round(a * s_sd * (math.sqrt(r_sd) / d_sd if r_sd != 1 else 1 / d_sd), 9), _texto_raiz(a, r_sd, d_sd, s_sd),
         "ignora el desfase dentro de la función"),
    ]
    vistos, elegidos = {round(valor, 9)}, []
    for v, t, e in candidatos:
        if v not in vistos:
            vistos.add(v)
            elegidos.append(op(v, e, f"${t}$"))
    if len(elegidos) < 3:
        raise Descartar
    radianes = math.radians(angulo) + (math.pi if desfase else 0)
    real = a * (math.sin(radianes) if funcion == "sen" else math.cos(radianes))
    return Propuesta(enunciado, op(round(valor, 9), None, f"${texto}$"), elegidos[:3], pasos,
                     lambda v: abs(v - real) < 1e-7, "alta")


@plantilla(ALG, "M2")
def distancia_con_decaimiento_exponencial(rng):
    k = rng.choice([5, 10, 20, 25])
    veces = rng.choice([2, 4, 8, 16])
    exponente = int(math.log2(veces))
    distancia = k * exponente
    contexto = rng.choice([
        ("En una caverna, la intensidad de la luz a $d$ metros de la entrada es", "la intensidad es", "de la que hay en la entrada", "metros"),
        ("En un lago, la intensidad de la luz a $d$ metros de profundidad es", "la intensidad es", "de la que hay en la superficie", "metros"),
    ])
    fraccion = f"\\frac{{1}}{{{veces}}}"
    enunciado = (f"{contexto[0]} $I(d) = I_0 \\cdot 2^{{-\\frac{{d}}{{{k}}}}}$, donde $I_0$ es la intensidad inicial. ¿A qué distancia "
                 f"{contexto[1]} ${fraccion}$ {contexto[2]}?")
    pasos = (f"Se plantea $I_0 \\cdot 2^{{-\\frac{{d}}{{{k}}}}} = {fraccion} I_0$, es decir, $2^{{-\\frac{{d}}{{{k}}}}} = 2^{{-{exponente}}}$. "
             f"Igualando exponentes, $\\frac{{d}}{{{k}}} = {exponente}$ y $d = {distancia}$ {contexto[3]}.")
    candidatos = [(k * veces, f"multiplica {k} por {veces} en vez de por el exponente"),
                  (Fraction(k, veces), f"divide {k} por {veces}"),
                  (k * (veces - 1), "resta 1 al denominador de la fracción"),
                  (Fraction(exponente, k), "divide el exponente por {k} en vez de multiplicar".replace("{k}", str(k)))]
    distractores = [op(Fraction(v), e, f"${tex(v)}$ {contexto[3]}") for v, e in _tres_distintos(Fraction(distancia), [(Fraction(v), e) for v, e in candidatos])]
    return Propuesta(enunciado, op(Fraction(distancia), None, f"${distancia}$ {contexto[3]}"), distractores, pasos,
                     lambda v: abs(2 ** (-float(v) / k) - 1 / veces) < 1e-12, "media")


# ----------------------------------------------------------------- Geometría

TRIG = {30: ("\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}", "\\frac{\\sqrt{3}}{3}"), 45: ("\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}", "1"),
        60: ("\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}", "\\sqrt{3}")}


def _largo_raiz(valor_cuadrado, unidad):
    return f"${raiz_tex(int(valor_cuadrado))}$ {unidad}" if Fraction(valor_cuadrado).denominator == 1 else f"$\\sqrt{{{tex(valor_cuadrado)}}}$ {unidad}"


@plantilla(GEO, "M2")
def lado_con_razones_trigonometricas(rng):
    angulo = rng.choice([30, 45, 60])
    hip = rng.choice([4, 6, 8, 10, 12, 14, 16, 20])
    seno2 = {30: Fraction(1, 4), 45: Fraction(1, 2), 60: Fraction(3, 4)}[angulo]
    opuesto2 = hip * hip * seno2
    adyacente2 = hip * hip - opuesto2
    contexto, unidad = rng.choice([("Una rampa recta", "m"), ("Una escalera apoyada en un muro", "m"), ("Un cable tenso que sujeta un poste", "m")])
    enunciado = (f"{contexto} mide {hip} {unidad} y forma un ángulo de ${angulo}^{{\\circ}}$ con el suelo horizontal. ¿A qué altura "
                 f"sobre el suelo llega su extremo superior?")
    pasos = (f"La altura es el cateto opuesto al ángulo de ${angulo}^{{\\circ}}$ y la longitud es la hipotenusa: "
             f"$h = {hip} \\cdot \\text{{sen}}\\,{angulo}^{{\\circ}} = {hip} \\cdot {TRIG[angulo][0]}$, que da {_largo_raiz(opuesto2, unidad)}.")
    candidatos = [(adyacente2, "usa el coseno, que corresponde al cateto adyacente (la distancia horizontal)"),
                  (Fraction(hip * hip) / seno2 if seno2 != 1 else 4 * hip * hip, "divide por el seno en vez de multiplicar"),
                  (hip * hip * {30: Fraction(1, 3), 45: Fraction(1), 60: Fraction(3)}[angulo], "usa la tangente del ángulo"),
                  (Fraction(hip * hip, 4), "toma siempre la mitad de la longitud")]
    elegidos = _tres_distintos(opuesto2, candidatos)
    distractores = [op(v, e, _largo_raiz(v, unidad)) for v, e in elegidos]
    figura = figuras.triangulo_con_angulo(math.sqrt(adyacente2), math.sqrt(opuesto2), "", "h", f"{hip} {unidad}", f"{angulo}°")
    return Propuesta(enunciado, op(opuesto2, None, _largo_raiz(opuesto2, unidad)), distractores, pasos,
                     lambda v: abs(math.sqrt(v) - hip * math.sin(math.radians(angulo))) < 1e-9, "media", figura=figura)


@plantilla(GEO, "M2")
def modulo_de_un_vector_tras_una_homotecia(rng):
    k = rng.choice([-3, -2, 2, 3, Fraction(1, 2), Fraction(-1, 2)])
    u = (rng.choice([2, 4, 6, -2, -4]), rng.choice([2, 4, 6, -2, -4]))
    imagen_u = (k * u[0], k * u[1])
    a, b, c = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10)])
    w = (a * rng.choice([1, -1]), b * rng.choice([1, -1]))
    correcto = abs(k) * c
    enunciado = (f"Al aplicar una homotecia con centro en el origen al vector $({u[0]},\\ {u[1]})$ se obtiene el vector "
                 f"$({tex(imagen_u[0])},\\ {tex(imagen_u[1])})$. Si se aplica la misma homotecia al vector $({w[0]},\\ {w[1]})$, ¿cuál es el "
                 f"módulo del vector obtenido?")
    pasos = (f"La razón de la homotecia es $k = {tex(k)}$, porque cada componente se multiplicó por ese número. El módulo de "
             f"$({w[0]},\\ {w[1]})$ es $\\sqrt{{{par(w[0])}^{{2}} + {par(w[1])}^{{2}}}} = {c}$, y una homotecia multiplica las longitudes por $|k|$: "
             f"${tex(abs(k))} \\cdot {c} = {tex(correcto)}$.")
    candidatos = [(Fraction(c), "calcula el módulo del vector original y no aplica la homotecia"),
                  (Fraction(k * c), "multiplica el módulo por la razón con su signo; un módulo nunca es negativo") if k < 0 else (Fraction(abs(k) * abs(k) * c), "multiplica el módulo por el cuadrado de la razón"),
                  (Fraction(abs(k) * (abs(w[0]) + abs(w[1]))), "suma las componentes en vez de calcular el módulo"),
                  (Fraction(abs(k) * abs(k) * c), "multiplica el módulo por el cuadrado de la razón"),
                  (Fraction(c) / abs(k), "divide por la razón en vez de multiplicar")]
    distractores = [op(v, e) for v, e in _tres_distintos(Fraction(correcto), candidatos)]
    return Propuesta(enunciado, op(Fraction(correcto)), distractores, pasos,
                     lambda v: abs(float(v) - math.hypot(float(k * w[0]), float(k * w[1]))) < 1e-9, "media")


@plantilla(GEO, "M2")
def angulo_inscrito_y_angulo_central(rng):
    central = rng.choice(range(40, 161, 10))
    da_central = rng.random() < 0.5
    inicio = rng.randrange(-60, 0, 5)
    a, b = inicio, inicio + central
    c = b + (360 - central) / 2 + rng.choice([-25, 0, 25])
    inscrito = Fraction(central, 2)
    if da_central:
        enunciado = (f"En la circunferencia de centro $O$ de la figura, el ángulo central $AOB$ mide ${central}^{{\\circ}}$. ¿Cuánto mide el "
                     f"ángulo inscrito $ACB$?")
        correcto = inscrito
        pasos = f"Un ángulo inscrito mide la mitad del ángulo central que subtiende el mismo arco: ${central}^{{\\circ}} : 2 = {tex(inscrito)}^{{\\circ}}$."
        candidatos = [(Fraction(central), "cree que el ángulo inscrito mide lo mismo que el central"),
                      (Fraction(2 * central), "multiplica por 2 en vez de dividir"),
                      (Fraction(180 - central), "calcula el suplemento del ángulo central"),
                      (Fraction(360 - central, 2), "usa el arco mayor en vez del arco $AB$ que subtiende el ángulo")]
        figura = figuras.angulo_inscrito_y_central(a, b, c, f"{central}°", "x")
    else:
        enunciado = (f"En la circunferencia de centro $O$ de la figura, el ángulo inscrito $ACB$ mide ${tex(inscrito)}^{{\\circ}}$. ¿Cuánto mide "
                     f"el ángulo central $AOB$?")
        correcto = Fraction(central)
        pasos = f"El ángulo central mide el doble del ángulo inscrito que subtiende el mismo arco: $2 \\cdot {tex(inscrito)}^{{\\circ}} = {central}^{{\\circ}}$."
        candidatos = [(inscrito, "cree que el ángulo central mide lo mismo que el inscrito"),
                      (inscrito / 2, "divide por 2 en vez de multiplicar"),
                      (Fraction(180) - inscrito, "calcula el suplemento del ángulo inscrito"),
                      (Fraction(360 - central), "calcula el ángulo del arco mayor")]
        figura = figuras.angulo_inscrito_y_central(a, b, c, "x", f"{tex(inscrito).replace('{,}', ',')}°")

    def grados(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}^{{\\circ}}$")

    distractores = [grados(v, e) for v, e in _tres_distintos(correcto, candidatos)]

    def comprobar(v):
        pa, pb, pc = (complex(math.cos(math.radians(t)), math.sin(math.radians(t))) for t in (a, b, c))
        medido = abs(math.degrees(math.atan2(((pa - pc) / (pb - pc)).imag, ((pa - pc) / (pb - pc)).real)))
        return abs((float(v) if da_central else float(v) / 2) - medido) < 1e-6

    return Propuesta(enunciado, grados(correcto), distractores, pasos, comprobar, "media", figura=figura)


@plantilla(GEO, "M2")
def cuerdas_que_se_cortan_en_una_circunferencia(rng):
    ae, eb = rng.randrange(2, 13), rng.randrange(2, 13)
    producto = ae * eb
    divisores = [d for d in range(2, 25) if producto % d == 0 and d not in (ae, eb) and producto // d not in (ae, eb)]
    if not divisores:
        raise Descartar
    ce = rng.choice(divisores)
    ed = producto // ce
    enunciado = (f"En la circunferencia de la figura, las cuerdas $AB$ y $CD$ se cortan en el punto $E$. Si $AE = {ae}$ cm, $EB = {eb}$ cm "
                 f"y $CE = {ce}$ cm, ¿cuánto mide $ED$?")
    pasos = (f"Cuando dos cuerdas se cortan, el producto de los segmentos de una es igual al de la otra: $AE \\cdot EB = CE \\cdot ED$. "
             f"Entonces ${ae} \\cdot {eb} = {ce} \\cdot ED$ y $ED = {producto} : {ce} = {tex(Fraction(producto, ce))}$ cm.")
    candidatos = [(Fraction(ae + eb - ce), "plantea que las cuerdas miden lo mismo y resta"),
                  (Fraction(ce * eb, ae), "plantea la proporción con los segmentos cruzados"),
                  (Fraction(ae * ce, eb), "plantea la proporción con los segmentos cruzados"),
                  (Fraction(producto), "calcula el producto y no lo divide")]

    def cm(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ cm")

    distractores = [cm(v, e) for v, e in _tres_distintos(Fraction(ed), candidatos)]
    figura = figuras.cuerdas_que_se_cortan((200, 10, 120, 285), [f"{ae}", f"{eb}", f"{ce}", "?"])
    return Propuesta(enunciado, cm(Fraction(ed)), distractores, pasos, lambda v: ce * v == ae * eb, "media", figura=figura)


@plantilla(GEO, "M2")
def tamano_de_una_imagen_proyectada(rng):
    d1 = Fraction(rng.randrange(8, 25), 10)
    ancho = Fraction(rng.randrange(4, 13), 10)
    alto = ancho * Fraction(3, 4)
    k = rng.choice([Fraction(3, 2), Fraction(2), Fraction(5, 2), Fraction(3)])
    d2 = d1 * k
    pide_area = rng.random() < 0.5
    enunciado = (f"El lente de un proyector está a ${tex(d1)}$ m de un muro y proyecta una imagen rectangular de ${tex(ancho)}$ m de ancho por "
                 f"${tex(alto)}$ m de alto. Si el proyector se aleja hasta quedar a ${tex(d2)}$ m del muro, la imagen es una homotecia de la "
                 f"anterior con centro en el lente. ")
    if pide_area:
        correcto = ancho * alto * k * k
        enunciado += "¿Cuál es el área de la nueva imagen?"
        pasos = (f"La razón de la homotecia es ${tex(d2)} : {tex(d1)} = {tex(k)}$. Las medidas se multiplican por ${tex(k)}$ y el área por "
                 f"${tex(k)}^{{2}} = {tex(k * k)}$: ${tex(ancho * alto)} \\cdot {tex(k * k)} = {tex(correcto)}$ m².")
        candidatos = [(ancho * alto * k, "multiplica el área por la razón y no por su cuadrado"),
                      (ancho * alto, "no aplica la homotecia"),
                      (ancho * alto + (k - 1), "suma la razón en vez de multiplicar"),
                      ((ancho + alto) * k * 2, "calcula el perímetro de la nueva imagen")]
        unidad = "m²"
        comprobar = lambda v: v == (ancho * d2 / d1) * (alto * d2 / d1)
    else:
        correcto = ancho * k
        enunciado += "¿Cuál es el ancho de la nueva imagen?"
        pasos = f"La razón de la homotecia es ${tex(d2)} : {tex(d1)} = {tex(k)}$, así que el ancho es ${tex(ancho)} \\cdot {tex(k)} = {tex(correcto)}$ m."
        candidatos = [(ancho + (d2 - d1), "suma al ancho lo que se alejó el proyector"),
                      (ancho * k * k, "multiplica por el cuadrado de la razón"),
                      (ancho / k, "divide por la razón: la imagen crece al alejar el proyector"),
                      (alto * k, "calcula el alto de la nueva imagen")]
        unidad = "m"
        comprobar = lambda v: v * d1 == ancho * d2
    distractores = [op(v, e, f"${tex(v)}$ {unidad}") for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, f"${tex(correcto)}$ {unidad}"), distractores, pasos, comprobar,
                     "alta" if pide_area else "media")


# ------------------------------------------------- Probabilidad y estadística

@plantilla(PRO, "M2")
def cantidad_de_personas_por_saludos(rng):
    n = rng.randrange(6, 31)
    total = n * (n - 1) // 2
    contexto = rng.choice([("estudiantes de una reunión", "saluda con un apretón de manos a cada uno de los demás", "apretones de manos"),
                           ("equipos de un torneo", "juega exactamente un partido contra cada uno de los demás", "partidos")])
    enunciado = (f"En un grupo de {contexto[0]}, cada uno {contexto[1]} una sola vez. Si en total hubo {total} {contexto[2]}, "
                 f"¿cuántos {contexto[0].split(' ')[0]} hay en el grupo?")
    pasos = (f"Con $n$ integrantes, la cantidad de pares distintos es $\\binom{{n}}{{2}} = \\frac{{n(n - 1)}}{{2}}$. Se plantea "
             f"$\\frac{{n(n - 1)}}{{2}} = {total}$, es decir, $n(n - 1) = {2 * total}$, y como ${n} \\cdot {n - 1} = {2 * total}$, $n = {n}$.")
    candidatos = [(n - 1, "plantea $\\frac{n(n + 1)}{2}$ en vez de $\\frac{n(n - 1)}{2}$"),
                  (round(math.sqrt(total)), "toma la raíz cuadrada del total"),
                  (total // 2, "divide el total por 2 en vez de resolver la ecuación"),
                  (n + 1, "resuelve bien la ecuación pero suma 1 al resultado")]
    distractores = [op(v, e) for v, e in _tres_distintos(n, candidatos)]
    return Propuesta(enunciado, op(n), distractores, pasos, lambda v: math.comb(v, 2) == total, "media")


@plantilla(PRO, "M2")
def probabilidad_condicional_en_una_tabla(rng):
    filas, columnas = rng.choice([
        (("Conforme", "No conforme"), ("Menor de 40", "40 o más")),
        (("Conforme", "No conforme"), ("Hombre", "Mujer")),
        (("Vacunado", "No vacunado"), ("Menor de 40", "40 o más")),
        (("Aprobó", "Reprobó"), ("Curso A", "Curso B")),
    ])
    m = [[rng.randrange(8, 60) for _ in range(2)] for _ in range(2)]
    i, j = rng.randrange(2), rng.randrange(2)
    col_total = m[0][j] + m[1][j]
    fila_total = m[i][0] + m[i][1]
    total = sum(map(sum, m))
    correcto = Fraction(m[i][j], col_total)
    enunciado = (f"En la tabla de la figura se clasifica a un grupo de personas. Si se elige al azar a una persona del grupo "
                 f"\"{columnas[j]}\", ¿cuál es la probabilidad de que esté en la categoría \"{filas[i]}\"?")
    pasos = (f"Como se sabe que la persona pertenece a \"{columnas[j]}\", los casos posibles son ${m[0][j]} + {m[1][j]} = {col_total}$. "
             f"De ellos, {m[i][j]} están en \"{filas[i]}\": $P = {_fraccion_cruda(m[i][j], col_total)}$.")
    candidatos = [(Fraction(m[i][j], total), "divide por el total del grupo: calcula la probabilidad de que cumpla ambas condiciones"),
                  (Fraction(m[i][j], fila_total), f"divide por el total de \"{filas[i]}\": invierte la condición"),
                  (Fraction(fila_total, total), f"calcula la probabilidad de \"{filas[i]}\" sin la condición"),
                  (Fraction(col_total, total), f"calcula la probabilidad de \"{columnas[j]}\"")]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    figura = figuras.tabla(["", columnas[0], columnas[1]], [[filas[0], m[0][0], m[0][1]], [filas[1], m[1][0], m[1][1]]])
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: v * (m[0][j] + m[1][j]) == m[i][j], "media", figura=figura)


@plantilla(PRO, "M2")
def probabilidad_binomial_en_una_prueba(rng):
    n = rng.choice([4, 5, 6, 8, 10])
    k = rng.randrange(1, n)
    tipo = rng.choice(["exactamente", "todas"]) if n <= 6 else "exactamente"
    if tipo == "todas":
        k = n
        correcto = Fraction(1, 2 ** n)
        enunciado = (f"Una persona responde al azar y de manera independiente {n} preguntas de verdadero o falso. ¿Cuál es la probabilidad "
                     f"de que responda correctamente todas?")
        pasos = f"Cada respuesta es correcta con probabilidad $\\frac{{1}}{{2}}$ y son independientes: $\\left(\\frac{{1}}{{2}}\\right)^{{{n}}} = \\frac{{1}}{{{2 ** n}}}$."
        candidatos = [(Fraction(1, 2 * n), f"multiplica $\\frac{{1}}{{2}}$ por {n} en el denominador en vez de elevar"),
                      (Fraction(1, 2), "responde como si fuera una sola pregunta"),
                      (Fraction(1, n), f"divide 1 por la cantidad de preguntas"),
                      (Fraction(n, 2 ** n), f"multiplica por {n}, como si hubiera {n} formas de acertarlas todas")]
    else:
        formas = math.comb(n, k)
        correcto = Fraction(formas, 2 ** n)
        enunciado = (f"Una persona responde al azar y de manera independiente {n} preguntas de verdadero o falso. ¿Cuál es la probabilidad "
                     f"de que responda correctamente exactamente {k}?")
        pasos = (f"Cada secuencia de respuestas tiene probabilidad $\\left(\\frac{{1}}{{2}}\\right)^{{{n}}}$ y hay $\\binom{{{n}}}{{{k}}} = {formas}$ "
                 f"formas de elegir cuáles son las {k} correctas: $P = {_fraccion_cruda(formas, 2 ** n)}$.")
        candidatos = [(Fraction(1, 2 ** n), "considera una sola secuencia y olvida contar en qué preguntas están los aciertos"),
                      (Fraction(k, n), "divide la cantidad de aciertos por la cantidad de preguntas"),
                      (Fraction(math.comb(n, k), 2 ** k), f"eleva a {k} en vez de a {n}"),
                      (Fraction(1, 2), "responde como si fuera una sola pregunta")]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if 0 < v <= 1])]
    real = Fraction(math.comb(n, k), 2 ** n)
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == real, "alta")


@plantilla(PRO, "M2")
def ordenamientos_y_permutaciones(rng):
    n = rng.randrange(5, 10)
    k = rng.randrange(2, 5)
    contexto = rng.choice([
        (f"En una carrera participan {n} atletas. ¿De cuántas maneras distintas pueden quedar ocupados los primeros {k} lugares del podio?", True),
        (f"Un club de {n} socios debe elegir un presidente, un tesorero{' y un secretario' if k == 3 else ''}{', un secretario y un vocal' if k == 4 else ''}. "
         f"Si una persona no puede ocupar dos cargos, ¿de cuántas maneras distintas se pueden asignar?", True),
        (f"De un grupo de {n} estudiantes se deben elegir {k} para formar una comisión, sin cargos. ¿De cuántas maneras distintas se puede formar la comisión?", False),
    ])
    if not contexto[1] and k == 2 and n < 6:
        raise Descartar
    importa = contexto[1]
    if contexto[0].startswith("Un club") and k == 2:
        texto = f"Un club de {n} socios debe elegir un presidente y un tesorero. Si una persona no puede ocupar dos cargos, ¿de cuántas maneras distintas se pueden asignar?"
    else:
        texto = contexto[0]
    variacion = math.perm(n, k)
    combinacion = math.comb(n, k)
    correcto = variacion if importa else combinacion
    factores = " \\cdot ".join(str(n - i) for i in range(k))
    if importa:
        pasos = (f"Importa el orden: para el primer lugar hay {n} opciones, para el segundo {n - 1}, y así: "
                 f"${factores} = {variacion}$.")
        candidatos = [(combinacion, "divide por las formas de ordenar, como si el orden no importara"),
                      (n ** k, "permite que una misma persona ocupe más de un lugar"),
                      (n * k, f"multiplica {n} por {k}"),
                      (math.factorial(n), "ordena a todos los participantes y no solo a los elegidos")]
    else:
        pasos = f"No importa el orden de los elegidos: $\\binom{{{n}}}{{{k}}} = \\frac{{{factores}}}{{{k}!}} = {combinacion}$."
        candidatos = [(variacion, "cuenta como distintas las mismas personas elegidas en otro orden"),
                      (n ** k, "permite elegir dos veces a la misma persona"),
                      (n * k, f"multiplica {n} por {k}"),
                      (math.comb(n, k - 1), f"calcula las formas de elegir {k - 1} personas")]
    distractores = [op(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(texto, op(correcto), distractores, pasos,
                     lambda v: v == (math.perm(n, k) if importa else math.comb(n, k)), "media")


@plantilla(PRO, "M2")
def probabilidad_total_con_un_dado_y_dos_cajas(rng):
    a = [rng.randrange(1, 7) for _ in range(2)]
    b = [rng.randrange(1, 7) for _ in range(2)]
    umbral = rng.choice([2, 3, 4])
    p_a = Fraction(umbral, 6)
    pa_blanca = Fraction(a[0], sum(a))
    pb_blanca = Fraction(b[0], sum(b))
    correcto = p_a * pa_blanca + (1 - p_a) * pb_blanca
    enunciado = (f"Se tienen dos cajas: la caja A contiene {a[0]} fichas blancas y {a[1]} rojas, y la caja B contiene {b[0]} fichas blancas y "
                 f"{b[1]} rojas. Se lanza un dado común: si sale un número menor o igual que {umbral}, se extrae una ficha de la caja A; en "
                 f"otro caso, de la caja B. ¿Cuál es la probabilidad de extraer una ficha blanca?")
    pasos = (f"$P(A) = \\frac{{{umbral}}}{{6}}$ y $P(B) = \\frac{{{6 - umbral}}}{{6}}$. Por probabilidad total: "
             f"$\\frac{{{umbral}}}{{6}} \\cdot \\frac{{{a[0]}}}{{{sum(a)}}} + \\frac{{{6 - umbral}}}{{6}} \\cdot \\frac{{{b[0]}}}{{{sum(b)}}} = {frac(correcto)}$.")
    candidatos = [(Fraction(a[0] + b[0], sum(a) + sum(b)), "junta las fichas de ambas cajas e ignora el dado"),
                  ((pa_blanca + pb_blanca) / 2, "supone que cada caja se elige con probabilidad $\\frac{1}{2}$"),
                  (p_a * pa_blanca, "considera solo el caso de la caja A"),
                  (pa_blanca * pb_blanca, "multiplica las probabilidades de ambas cajas")]
    if correcto in (pa_blanca, pb_blanca):
        raise Descartar
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    casos = Fraction(0)
    for cara in range(1, 7):
        caja = a if cara <= umbral else b
        casos += Fraction(1, 6) * Fraction(caja[0], sum(caja))
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == casos, "alta")

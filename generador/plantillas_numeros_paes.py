"""Plantillas de números modeladas en tipos de pregunta de las PAES M1 de admisión 2025 y 2026 (DEMRE).

Se replica la habilidad evaluada con contextos y números propios; ninguna copia un ítem oficial.
"""
from __future__ import annotations

from fractions import Fraction

from nucleo import Descartar, Propuesta, miles, op, pesos, plantilla, tex

EJE = "numeros"


def _alt_pesos(valor, error=None):
    return op(Fraction(valor), error, pesos(int(valor)))


@plantilla(EJE)
def compra_con_precios_por_unidad_de_medida(rng):
    por_peso, por_medio_kilo, por_unidad = rng.choice([
        ("carne molida", "champiñones", ("cebolla", "cebollas")),
        ("queso", "tomates", ("lechuga", "lechugas")),
        ("jamón", "manzanas", ("pan", "panes")),
    ])
    gramos = rng.randrange(300, 1000, 100)
    precio_100 = rng.randrange(700, 1300, 100)
    kilos = rng.randrange(1, 4)
    precio_medio = rng.randrange(1000, 3600, 500)
    unidades = rng.randrange(2, 6)
    precio_unidad = rng.randrange(200, 700, 100)
    parte_peso = gramos // 100 * precio_100
    correcto = parte_peso + 2 * kilos * precio_medio + unidades * precio_unidad
    enunciado = (f"Para una preparación se necesitan {gramos} g de {por_peso}, {kilos} kg de {por_medio_kilo} y {unidades} {por_unidad[1]}. "
                 f"Los precios son: 100 g de {por_peso} a {pesos(precio_100)}, medio kilogramo de {por_medio_kilo} a {pesos(precio_medio)} "
                 f"y cada {por_unidad[0]} a {pesos(precio_unidad)}. ¿Cuánto dinero se necesita para comprar todos los ingredientes?")
    pasos = (f"{por_peso.capitalize()}: ${gramos // 100} \\cdot {miles(precio_100)} = {miles(parte_peso)}$. {por_medio_kilo.capitalize()}: "
             f"{kilos} kg son {2 * kilos} medios kilogramos, ${2 * kilos} \\cdot {miles(precio_medio)} = {miles(2 * kilos * precio_medio)}$. "
             f"{por_unidad[1].capitalize()}: ${unidades} \\cdot {precio_unidad} = {miles(unidades * precio_unidad)}$. En total, {pesos(correcto)}.")
    distractores = [
        _alt_pesos(parte_peso + kilos * precio_medio + unidades * precio_unidad,
                   "usa el precio de medio kilogramo como si fuera el precio por kilogramo"),
        _alt_pesos(precio_100 + precio_medio + precio_unidad, "suma los precios indicados sin considerar las cantidades"),
        _alt_pesos(parte_peso + 2 * kilos * precio_medio + precio_unidad, f"considera una sola unidad en vez de {unidades}"),
    ]
    return Propuesta(enunciado, _alt_pesos(correcto), distractores, pasos,
                     lambda v: v == Fraction(gramos, 100) * precio_100 + kilos / Fraction(1, 2) * precio_medio + unidades * precio_unidad,
                     "media")


@plantilla(EJE)
def combustible_segun_rendimiento(rng):
    rendimiento = rng.choice([8, 10, 12, 15, 16, 20])
    litros = Fraction(rng.randrange(3, 25), 2)
    total = litros * rendimiento
    if total.denominator != 1 or total < 12:
        raise Descartar
    total = int(total)
    tramo1 = rng.randrange(4, total - 3)
    tramo2 = total - tramo1
    enunciado = (f"Un auto recorre {tramo1} km para ir de la ciudad A a la ciudad B y luego {tramo2} km para ir de la ciudad B a la "
                 f"ciudad C. Si el auto rinde {rendimiento} kilómetros por litro de bencina, ¿cuántos litros de bencina necesita para "
                 f"todo el trayecto?")
    pasos = (f"El trayecto completo es ${tramo1} + {tramo2} = {total}$ km. Como recorre {rendimiento} km con cada litro, necesita "
             f"${total} : {rendimiento} = {tex(litros)}$ litros.")
    distractores = [
        op(Fraction(total * rendimiento), "multiplica la distancia por el rendimiento en vez de dividir"),
        op(Fraction(total - rendimiento), "resta el rendimiento a la distancia"),
        op(Fraction(rendimiento, total), "divide el rendimiento por la distancia, en el orden inverso"),
    ]
    return Propuesta(enunciado, op(litros), distractores, pasos,
                     lambda v: v * rendimiento == tramo1 + tramo2, "baja")


@plantilla(EJE)
def numero_cuya_parte_es_un_decimal(rng):
    k, nombre = rng.choice([(2, "mitad"), (3, "tercera parte"), (4, "cuarta parte"), (5, "quinta parte")])
    parte = Fraction(k * rng.randrange(1, 13), 100)
    correcto = parte * k
    enunciado = f"¿Cuál es el número cuya {nombre} es ${tex(parte)}$?"
    pasos = (f"Si la {nombre} del número es ${tex(parte)}$, el número es {k} veces ese valor: "
             f"${k} \\cdot {tex(parte)} = {tex(correcto)}$.")
    distractores = [
        op(parte / k, f"calcula la {nombre} de ${tex(parte)}$ en vez del número completo"),
        op(correcto * 10, "multiplica bien pero corre la coma un lugar de más hacia la derecha"),
        op(correcto / 10, "multiplica bien pero corre la coma un lugar de más hacia la izquierda"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos, lambda v: v / k == parte, "baja")


@plantilla(EJE)
def porcentaje_de_un_porcentaje(rng):
    a, b = rng.choice([10, 20, 25, 40, 50, 75]), rng.choice([10, 20, 25, 40, 50, 75])
    base = rng.choice([100, 200, 400, 800, 1000, 2000])
    correcto = Fraction(base * a * b, 10000)
    if a + b >= 100 or a == b:
        raise Descartar
    enunciado = f"¿Cuánto es el {a} % del {b} % de ${tex(base)}$?"
    intermedio = Fraction(base * b, 100)
    pasos = (f"El {b} % de {tex(base)} es ${tex(intermedio)}$. El {a} % de ${tex(intermedio)}$ es "
             f"${tex(intermedio)} \\cdot \\frac{{{a}}}{{100}} = {tex(correcto)}$.")
    distractores = [
        op(Fraction(base * (a + b), 100), "suma los dos porcentajes y los aplica una sola vez"),
        op(Fraction(base * a * b, 100), "divide por 100 una sola vez en vez de dos"),
        op(intermedio, f"calcula solo el {b} % y no aplica el {a} %"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v * 10000 == base * a * b, "media")


@plantilla(EJE)
def cantidad_total_conocido_un_porcentaje(rng):
    pct = rng.choice([5, 10, 20, 25, 40, 75])
    total = rng.randrange(40, 801, 20)
    parte = Fraction(total * pct, 100)
    if parte.denominator != 1:
        raise Descartar
    parte = int(parte)
    enunciado = f"Si ${parte}$ corresponde al {pct} % de una cantidad, ¿cuál es dicha cantidad?"
    pasos = (f"Si el {pct} % de la cantidad es {parte}, la cantidad es ${parte} : \\frac{{{pct}}}{{100}} = "
             f"{parte} \\cdot \\frac{{100}}{{{pct}}} = {total}$.")
    distractores = [
        op(Fraction(parte * pct, 100), f"calcula el {pct} % de {parte}"),
        op(Fraction(parte * pct), "multiplica el número por el porcentaje sin dividir por 100"),
        op(Fraction(parte + pct), "suma el número y el porcentaje"),
    ]
    return Propuesta(enunciado, op(Fraction(total)), distractores, pasos,
                     lambda v: v * pct == parte * 100, "media")


@plantilla(EJE)
def porcentaje_de_aumento(rng):
    pct = rng.choice([2, 4, 5, 8, 20, 25])
    base = rng.choice([200, 400, 500, 1000, 1500, 2000, 3000, 5000])
    aumento = Fraction(base * pct, 100)
    if aumento.denominator != 1 or base % aumento:
        raise Descartar
    aumento = int(aumento)
    que, unidad = rng.choice([("la cantidad de socios de un club", "socios"), ("la venta mensual de una tienda", "unidades"),
                              ("la población de un pueblo", "personas"), ("la cantidad de seguidores de una cuenta", "seguidores")])
    enunciado = (f"En 2023, {que} era de {tex(base)} {unidad}. En 2024 aumentó en {aumento} {unidad} respecto al año anterior. "
                 f"¿Cuál fue el porcentaje de aumento?")
    pasos = (f"Se compara el aumento con la cantidad inicial: $\\frac{{{aumento}}}{{{tex(base)}}} \\cdot 100 = {pct}$ %.")

    def alt(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ %")

    distractores = [
        alt(100 + pct, "calcula qué porcentaje es el nuevo total respecto del inicial, no el aumento"),
        alt(base // aumento, "divide la cantidad inicial por el aumento, en el orden inverso"),
        alt(pct * 10, "ubica mal la coma al calcular el porcentaje"),
    ]
    return Propuesta(enunciado, alt(pct), distractores, pasos, lambda v: v * base == aumento * 100, "media")


@plantilla(EJE)
def descuentos_sucesivos_como_expresion(rng):
    precio = rng.randrange(10000, 80001, 5000)
    d1, d2 = rng.sample([10, 20, 25, 30, 40], 2)
    f1, f2 = Fraction(100 - d1, 100), Fraction(100 - d2, 100)
    articulo = rng.choice(["una chaqueta", "una mochila", "un par de zapatillas", "una lámpara"])
    enunciado = (f"Una tienda vendía {articulo} a {pesos(precio)}. Primero rebajó su precio en un {d1} % y, tiempo después, rebajó en un "
                 f"{d2} % el precio ya rebajado. ¿Cuál de las siguientes expresiones representa el precio final, en pesos?")
    pasos = (f"Rebajar un {d1} % equivale a multiplicar por ${tex(f1)}$ y rebajar un {d2} % el nuevo precio equivale a multiplicar "
             f"por ${tex(f2)}$. El precio final es ${miles(precio)} \\cdot {tex(f1)} \\cdot {tex(f2)}$.")

    def alt(valor, texto, error=None):
        return op(Fraction(valor), error, f"${miles(precio)} {texto}$")

    distractores = [
        alt(precio * Fraction(d1, 100) * Fraction(d2, 100), f"\\cdot {tex(Fraction(d1, 100))} \\cdot {tex(Fraction(d2, 100))}",
            "multiplica por los porcentajes de descuento en vez de por lo que queda del precio"),
        alt(precio * Fraction(100 - d1 - d2, 100), f"\\cdot {tex(Fraction(100 - d1 - d2, 100))}",
            "suma los dos descuentos, pero el segundo se aplica sobre el precio ya rebajado"),
        alt(precio * (f1 + f2), f"\\cdot ({tex(f1)} + {tex(f2)})", "suma los factores en vez de multiplicarlos"),
    ]
    return Propuesta(enunciado, alt(precio * f1 * f2, f"\\cdot {tex(f1)} \\cdot {tex(f2)}"), distractores, pasos,
                     lambda v: v == precio * (100 - d1) * (100 - d2) / Fraction(10000), "alta")


@plantilla(EJE)
def fraccion_de_lo_que_faltaba(rng):
    a = rng.choice([2, 3, 4, 5])
    p, q = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)])
    total = rng.choice([24, 30, 36, 40, 48, 60, 72, 90, 120])
    resto1 = Fraction(total * (a - 1), a)
    dia2 = resto1 * Fraction(p, q)
    correcto = resto1 - dia2
    directo = total * (1 - Fraction(1, a) - Fraction(p, q))
    if correcto.denominator != 1 or dia2.denominator != 1 or total % a or directo <= 0:
        raise Descartar
    quien, que, unidad = rng.choice([("Una ciclista", "una ruta", "km"), ("Un lector", "un libro", "páginas"),
                                     ("Una cuadrilla", "un camino", "km")])
    verbo = {"Una ciclista": "recorrió", "Un lector": "leyó", "Una cuadrilla": "pavimentó"}[quien]
    enunciado = (f"{quien} {verbo} {que} de {total} {unidad} en tres días. El primer día {verbo} $\\frac{{1}}{{{a}}}$ del total, el segundo día "
                 f"{verbo} $\\frac{{{p}}}{{{q}}}$ de lo que le faltaba y el tercer día {verbo} el resto. ¿Cuánto {verbo} el tercer día?")
    pasos = (f"El primer día avanza ${total} : {a} = {total // a}$ {unidad} y faltan {tex(resto1)}. El segundo día avanza "
             f"$\\frac{{{p}}}{{{q}}} \\cdot {tex(resto1)} = {tex(dia2)}$ {unidad}. Para el tercer día quedan "
             f"${tex(resto1)} - {tex(dia2)} = {tex(correcto)}$ {unidad}.")

    def alt(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ {unidad}")

    distractores = [
        alt(directo, "aplica la segunda fracción sobre el total y no sobre lo que faltaba"),
        alt(dia2, "entrega lo avanzado el segundo día"),
        alt(total // a, "entrega lo avanzado el primer día"),
    ]
    return Propuesta(enunciado, alt(correcto), distractores, pasos,
                     lambda v: v == total * (1 - Fraction(1, a)) * (1 - Fraction(p, q)), "alta")


@plantilla(EJE)
def cantidades_en_una_razon(rng):
    a, b = rng.choice([(2, 3), (3, 5), (2, 5), (3, 4), (4, 7), (1, 4), (5, 8)])
    k = a * rng.randrange(2, 9)
    primero, segundo, mezcla = rng.choice([
        ("colorante rojo", "colorante amarillo", "gotas"),
        ("pintura blanca", "pintura azul", "litros"),
        ("jugo concentrado", "agua", "vasos"),
        ("cemento", "arena", "paladas"),
    ])
    usado = k * b
    correcto = k * a
    enunciado = (f"Para obtener cierta mezcla se combinan {primero} y {segundo} en la razón ${a} : {b}$, respectivamente. "
                 f"Si se usan {usado} {mezcla} de {segundo}, ¿cuántos {mezcla} de {primero} se necesitan?"
                 if mezcla != "gotas" and mezcla != "paladas" else
                 f"Para obtener cierta mezcla se combinan {primero} y {segundo} en la razón ${a} : {b}$, respectivamente. "
                 f"Si se usan {usado} {mezcla} de {segundo}, ¿cuántas {mezcla} de {primero} se necesitan?")
    pasos = (f"Por cada {b} {mezcla} de {segundo} van {a} de {primero}. Como ${usado} : {b} = {k}$, se necesitan "
             f"${k} \\cdot {a} = {correcto}$ {mezcla} de {primero}.")
    distractores = [
        op(usado * b // a, "plantea la proporción con la razón invertida"),
        op(usado - (b - a), "resta la diferencia entre los términos de la razón"),
        op(k * (a + b), "entrega la cantidad total de mezcla"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos, lambda v: v * b == usado * a, "media")


@plantilla(EJE)
def conversion_con_una_equivalencia(rng):
    a, b, origen, destino = rng.choice([
        (5, Fraction(8), "millas", "kilómetros"),
        (2, Fraction(5), "pulgadas", "centímetros"),
        (4, Fraction(3), "tazas", "vasos"),
        (3, Fraction(3, 4), "tazas", "litros"),
    ])
    n = rng.randrange(3, 16)
    medida = n * b
    correcto = n * a
    enunciado = (f"Se sabe que {a} {origen} equivalen aproximadamente a ${tex(b)}$ {destino}. Según esa equivalencia, "
                 f"¿a cuántas {origen} equivalen ${tex(medida)}$ {destino}?")
    pasos = (f"${tex(medida)} : {tex(b)} = {n}$, es decir, la medida contiene {n} veces la equivalencia. "
             f"Entonces corresponde a ${n} \\cdot {a} = {correcto}$ {origen}.")
    distractores = [
        op(medida * b / a, "multiplica por la razón en vez de dividir"),
        op(Fraction(n), f"divide por ${tex(b)}$ pero no multiplica por {a}"),
        op(medida * a, f"multiplica la medida por {a} sin dividir por ${tex(b)}$"),
    ]
    return Propuesta(enunciado, op(Fraction(correcto)), distractores, pasos, lambda v: v * b == medida * a, "media")


@plantilla(EJE)
def ahorro_como_expresion(rng):
    p, q = rng.choice([(3, 5), (2, 5), (3, 4), (2, 3), (5, 8), (4, 7), (1, 4)])
    meses = rng.choice([6, 8, 10, 12, 18])
    correcto = meses * Fraction(q - p, q)

    def alt(coef, error=None):
        coef = Fraction(coef)
        texto = f"${coef.numerator}M$" if coef.denominator == 1 else f"$\\frac{{{coef.numerator}M}}{{{coef.denominator}}}$"
        return op(coef, error, texto.replace("$1M$", "$M$"))

    enunciado = (f"El sueldo líquido mensual de una persona es de $M$ pesos. Todos los meses gasta $\\frac{{{p}}}{{{q}}}$ del sueldo y "
                 f"ahorra el resto. Si el sueldo se mantiene durante {meses} meses, ¿cuál de las siguientes expresiones representa "
                 f"el ahorro total en ese período, en pesos?")
    pasos = (f"Cada mes ahorra $1 - \\frac{{{p}}}{{{q}}} = \\frac{{{q - p}}}{{{q}}}$ del sueldo. En {meses} meses ahorra "
             f"${meses} \\cdot \\frac{{{q - p}}}{{{q}}} \\cdot M$, es decir, {alt(correcto).texto}.")
    distractores = [
        alt(meses * Fraction(p, q), "calcula lo que gasta en vez de lo que ahorra"),
        alt(Fraction(q - p, q), "calcula el ahorro de un solo mes"),
        alt(Fraction(meses, q), "considera una sola de las partes en que se divide el sueldo"),
    ]
    return Propuesta(enunciado, alt(correcto), distractores, pasos,
                     lambda v: v * q == meses * (q - p), "alta")


@plantilla(EJE)
def paso_erroneo_en_operaciones_combinadas(rng):
    e = rng.randrange(1, 6)
    g = rng.randrange(2, 7)
    d = e + g
    c = rng.randrange(2, 6)
    f = rng.choice([2, 3, 4, 5])
    q = rng.randrange(2, 10)
    b = f * q - c * g
    if b < 2 or (c, g) == (2, 2) or (b, c * g) == (2, 2):
        raise Descartar
    paso_malo = rng.randrange(1, 5)
    s1 = d + e if paso_malo == 1 else d - e
    s2 = c + s1 if paso_malo == 2 else c * s1
    s3 = b * s2 if paso_malo == 3 else b + s2
    s4 = Fraction(s3 * f) if paso_malo == 4 else Fraction(s3, f)
    expresion = f"[{b} + {c} \\cdot ({d} - {e})] : {f}"
    lineas = [
        f"Paso 1: resuelve el paréntesis y obtiene $[{b} + {c} \\cdot {s1}] : {f}$.",
        f"Paso 2: resuelve la multiplicación y obtiene $[{b} + {s2}] : {f}$.",
        f"Paso 3: resuelve la suma y obtiene ${s3} : {f}$.",
        f"Paso 4: resuelve la división y obtiene ${tex(s4)}$.",
    ]
    enunciado = (f"Para calcular ${expresion}$, una persona realiza el siguiente procedimiento y comete un error. "
                 f"{' '.join(lineas)} ¿En cuál de los pasos se cometió el error?")
    correccion = {
        1: f"${d} - {e} = {d - e}$, no ${s1}$",
        2: f"${c} \\cdot {s1} = {c * s1}$, no ${s2}$",
        3: f"${b} + {s2} = {b + s2}$, no ${s3}$",
        4: f"${s3} : {f} = {tex(Fraction(s3, f))}$, no ${tex(s4)}$",
    }
    pasos = (f"En el Paso {paso_malo} el cálculo correcto es {correccion[paso_malo]}. Los demás pasos están bien resueltos a partir "
             f"del resultado del paso anterior.")
    bien = {1: f"${d} - {e} = {s1}$", 2: f"${c} \\cdot {s1} = {s2}$", 3: f"${b} + {s2} = {s3}$", 4: f"${s3} : {f} = {tex(s4)}$"}
    opciones = {i: op(i, None if i == paso_malo else f"el Paso {i} es correcto: {bien[i]}", f"En el Paso {i}") for i in range(1, 5)}

    def comprobar(v):
        esperados = [(s1, d - e), (s2, c * s1), (s3, b + s2), (s4, Fraction(s3, f))]
        return {i for i, (dicho, real) in enumerate(esperados, 1) if dicho != real} == {v}

    return Propuesta(enunciado, opciones[paso_malo], [opciones[i] for i in range(1, 5) if i != paso_malo], pasos,
                     comprobar, "media", orden_fijo=True)

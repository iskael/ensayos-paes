"""Plantillas de álgebra y funciones modeladas en tipos de pregunta de las PAES M1 de admisión 2024 a 2026 (DEMRE).

Se replica la habilidad evaluada con contextos y números propios; ninguna copia un ítem oficial.
"""
from __future__ import annotations

from fractions import Fraction

import figuras
from nucleo import Descartar, Propuesta, miles, op, par, pesos, plantilla, polinomio, tex

EJE = "algebra_funciones"


def _alt_poli(coefs, error=None, variable="x"):
    return op(tuple(coefs), error, f"${polinomio(list(coefs), variable)}$")


def _alt_pesos(valor, error=None):
    return op(Fraction(valor), error, pesos(int(valor)))


@plantilla(EJE)
def reduccion_con_signo_menos_ante_parentesis(rng):
    a = rng.randrange(1, 9)
    b = rng.choice([n for n in range(2, 10) if n != a])
    c = rng.choice([n for n in range(-9, 10) if n != 0])
    variable = rng.choice(["x", "b", "m", "t"])
    expresion = f"{polinomio([a, 0], variable)} - ({polinomio([b, c], variable)})"
    correcto = (a - b, -c)
    enunciado = f"¿Cuál de las siguientes expresiones es igual a ${expresion}$?"
    pasos = (f"El signo menos delante del paréntesis cambia el signo de cada término: "
             f"${polinomio([a, 0], variable)} - {polinomio([b, 0], variable)} {'+' if c < 0 else '-'} {abs(c)} = "
             f"{polinomio(list(correcto), variable)}$.")
    distractores = [
        _alt_poli((a - b, c), "cambia el signo solo del primer término del paréntesis", variable),
        _alt_poli((a + b, c), "elimina el paréntesis sin cambiar ningún signo", variable),
        _alt_poli((a + b, -c), "cambia el signo solo del segundo término del paréntesis", variable),
    ]
    return Propuesta(enunciado, _alt_poli(correcto, variable=variable), distractores, pasos,
                     lambda v: all(v[0] * x + v[1] == a * x - (b * x + c) for x in (0, 1, 3)), "baja")


@plantilla(EJE)
def factor_que_falta_en_un_producto(rng):
    a = rng.choice([n for n in range(-9, 10) if n != 0])
    b = rng.choice([n for n in range(-9, 10) if n != 0 and n != a and n != -a])
    producto = polinomio([1, a + b, a * b])
    enunciado = (f"Si $({polinomio([1, a])}) \\cdot P = {producto}$, con $x \\neq {-a}$, ¿cuál de las siguientes expresiones es igual a $P$?")
    pasos = (f"Se factoriza el trinomio buscando dos números que sumen ${a + b}$ y cuyo producto sea ${a * b}$: son ${a}$ y ${b}$. "
             f"Así, ${producto} = ({polinomio([1, a])})({polinomio([1, b])})$ y $P = {polinomio([1, b])}$.")
    distractores = [
        _alt_poli((1, -b), "se equivoca en el signo del término libre"),
        _alt_poli((1, a + b), "usa el coeficiente del término en $x$ como término libre"),
        _alt_poli((1, a * b - a), "resta el término libre del factor conocido en vez de dividir"),
    ]
    return Propuesta(enunciado, _alt_poli((1, b)), distractores, pasos,
                     lambda v: all((x + a) * (v[0] * x + v[1]) == x * x + (a + b) * x + a * b for x in (0, 1, 2)), "media")


@plantilla(EJE)
def dinero_que_sobra_como_expresion(rng):
    n, k = rng.randrange(2, 13), rng.randrange(2, 13)
    if n == k:
        raise Descartar
    cosa1, cosa2 = rng.choice([("yogures", "jugos"), ("cuadernos", "lápices"), ("entradas", "bebidas"), ("empanadas", "postres")])
    enunciado = (f"Una persona compra {n} {cosa1} a $M$ pesos cada uno y {k} {cosa2} a $L$ pesos cada uno, y paga con $P$ pesos, que es "
                 f"suficiente para la compra. ¿Cuál de las siguientes expresiones representa el dinero que le sobra, en pesos?"
                 if cosa1 not in ("entradas", "empanadas") else
                 f"Una persona compra {n} {cosa1} a $M$ pesos cada una y {k} {cosa2} a $L$ pesos cada uno, y paga con $P$ pesos, que es "
                 f"suficiente para la compra. ¿Cuál de las siguientes expresiones representa el dinero que le sobra, en pesos?")
    pasos = (f"El gasto total es ${n}M + {k}L$. Lo que sobra es el dinero con que paga menos todo el gasto: "
             f"$P - ({n}M + {k}L) = P - {n}M - {k}L$.")

    def alt(coefs, texto, error=None):
        return op(coefs, error, f"${texto}$")

    distractores = [
        alt((1, -n, k), f"P - {n}M + {k}L", "resta solo la primera compra y suma la segunda: falta el paréntesis"),
        alt((-1, n, k), f"{n}M + {k}L - P", "resta en el orden inverso: al gasto le quita el dinero disponible"),
        alt((1, -(n + k), -(n + k)), f"P - {n + k}(M + L)", "suma las cantidades y los precios por separado antes de multiplicar"),
    ]
    return Propuesta(enunciado, alt((1, -n, -k), f"P - {n}M - {k}L"), distractores, pasos,
                     lambda v: all(v[0] * p + v[1] * m_ + v[2] * l_ == p - n * m_ - k * l_ for p, m_, l_ in [(100, 3, 5), (70, 2, 1)]),
                     "media")


@plantilla(EJE)
def cinta_que_sobra_en_un_borde(rng):
    a, c = rng.randrange(2, 6), rng.randrange(1, 5)
    b = rng.randrange(1, 10)
    d = rng.randrange(1, 10)
    e = 2 * (a + c) + rng.randrange(2, 12)
    f = rng.randrange(10, 41)
    correcto = (e - 2 * (a + c), f - 2 * (b - d))
    lugar = rng.choice(["Una pista de baile", "Un escenario", "Una huerta", "Una cancha"])
    enunciado = (f"{lugar} de forma rectangular mide $({polinomio([a, b])})$ metros de largo y $({polinomio([c, -d])})$ metros de ancho. "
                 f"Para demarcar su borde se dispone de $({polinomio([e, f])})$ metros de cinta. ¿Cuál de las siguientes expresiones "
                 f"representa los metros de cinta que sobran después de demarcar todo el borde?")
    pasos = (f"El perímetro es $2({polinomio([a, b])}) + 2({polinomio([c, -d])}) = {polinomio([2 * (a + c), 2 * (b - d)])}$. "
             f"Lo que sobra es $({polinomio([e, f])}) - ({polinomio([2 * (a + c), 2 * (b - d)])}) = {polinomio(list(correcto))}$.")
    distractores = [
        _alt_poli((e - (a + c), f - (b - d)), "resta la suma del largo y el ancho, que es solo la mitad del perímetro"),
        _alt_poli((e + 2 * (a + c), f + 2 * (b - d)), "suma el perímetro en vez de restarlo"),
        _alt_poli((e - 2 * (a + c), f + 2 * (b - d)), "al restar el perímetro no cambia el signo de su término libre"),
    ]
    return Propuesta(enunciado, _alt_poli(correcto), distractores, pasos,
                     lambda v: all(v[0] * x + v[1] == e * x + f - 2 * (a * x + b) - 2 * (c * x - d) for x in (10, 11, 20)), "alta")


@plantilla(EJE)
def dos_personas_con_el_mismo_dinero(rng):
    precio = rng.randrange(450, 2501, 10)
    n1 = rng.randrange(5, 11)
    n2 = n1 - rng.randrange(1, 4)
    sobra1 = rng.randrange(100, 1500, 10)
    sobra2 = sobra1 + (n1 - n2) * precio
    dinero = n1 * precio + sobra1
    cosa = rng.choice(["lápices pasta", "cuadernos", "chocolates", "pasajes"])
    p1, p2 = rng.sample(["Daniela", "Marcos", "Antonia", "Felipe", "Camila", "Ignacio"], 2)
    enunciado = (f"{p1} compra {n1} {cosa} del mismo tipo y le sobran {pesos(sobra1)}. {p2} compra {n2} {cosa} iguales a los de {p1} "
                 f"y le sobran {pesos(sobra2)}. Si ambos tenían la misma cantidad de dinero antes de comprar, ¿cuánto dinero tenía cada uno?")
    pasos = (f"Si $x$ es el precio de cada unidad, ${n1}x + {miles(sobra1)} = {n2}x + {miles(sobra2)}$, de donde "
             f"${n1 - n2}x = {miles(sobra2 - sobra1)}$ y $x = {miles(precio)}$. Cada uno tenía "
             f"${n1} \\cdot {miles(precio)} + {miles(sobra1)} = {miles(dinero)}$ pesos.")
    distractores = [
        _alt_pesos(precio, "entrega el precio de una unidad y no el dinero que tenía cada persona"),
        _alt_pesos(n1 * precio, f"calcula lo que gastó {p1} y olvida sumar lo que le sobró"),
        _alt_pesos(n1 * precio + sobra2, "suma al gasto de una persona lo que le sobró a la otra"),
    ]

    def comprobar(v):
        x1, x2 = Fraction(v - sobra1, n1), Fraction(v - sobra2, n2)
        return x1 == x2 and x1 > 0

    return Propuesta(enunciado, _alt_pesos(dinero), distractores, pasos, comprobar, "alta")


@plantilla(EJE)
def funcion_que_modela_un_estanque(rng):
    capacidad = rng.randrange(200, 1501, 20)
    ritmo = rng.randrange(2, 16)
    vacia = rng.random() < 0.6
    if vacia:
        enunciado = (f"Un estanque contiene {capacidad} litros de agua y, al abrir la llave de desagüe, se vacía a razón de {ritmo} litros "
                     f"por minuto. ¿Cuál de las siguientes funciones modela la cantidad de agua, en litros, que queda en el estanque "
                     f"después de $t$ minutos con la llave abierta?")
        pasos = (f"Cada minuto salen {ritmo} litros, así que en $t$ minutos salen ${ritmo}t$ litros. Lo que queda es la cantidad inicial "
                 f"menos lo que salió: $f(t) = {capacidad} - {ritmo}t$.")
        correcta = op((-ritmo, capacidad), None, f"$f(t) = {capacidad} - {ritmo}t$")
        distractores = [
            op((ritmo, capacidad), "suma lo que sale en vez de restarlo", f"$f(t) = {capacidad} + {ritmo}t$"),
            op((capacidad, -ritmo), "intercambia la cantidad inicial con el ritmo de vaciado", f"$f(t) = {capacidad}t - {ritmo}$"),
            op((capacidad - ritmo, 0), "resta el ritmo a la cantidad inicial antes de multiplicar por el tiempo",
               f"$f(t) = ({capacidad} - {ritmo})t$"),
        ]
        valor = lambda t: capacidad - ritmo * t
    else:
        enunciado = (f"Un estanque contiene {capacidad} litros de agua y se le agrega agua a razón de {ritmo} litros por minuto. "
                     f"¿Cuál de las siguientes funciones modela la cantidad de agua, en litros, que hay en el estanque después de "
                     f"$t$ minutos?")
        pasos = (f"Cada minuto entran {ritmo} litros, así que en $t$ minutos entran ${ritmo}t$ litros, que se suman a la cantidad "
                 f"inicial: $f(t) = {capacidad} + {ritmo}t$.")
        correcta = op((ritmo, capacidad), None, f"$f(t) = {capacidad} + {ritmo}t$")
        distractores = [
            op((capacidad, ritmo), "intercambia la cantidad inicial con el ritmo de llenado", f"$f(t) = {capacidad}t + {ritmo}$"),
            op((capacidad + ritmo, 0), "suma el ritmo a la cantidad inicial antes de multiplicar por el tiempo",
               f"$f(t) = ({capacidad} + {ritmo})t$"),
            op((ritmo, 0), "olvida la cantidad de agua que ya había", f"$f(t) = {ritmo}t$"),
        ]
        valor = lambda t: capacidad + ritmo * t
    return Propuesta(enunciado, correcta, distractores, pasos,
                     lambda v: all(v[0] * t + v[1] == valor(t) for t in (0, 1, 7)), "media")


@plantilla(EJE)
def despejar_una_variable_en_una_formula(rng):
    a, b, c = rng.randrange(5, 21), rng.randrange(10, 61, 5), rng.randrange(2, 9)
    n = b + c * rng.randrange(2, 13)
    t = a + (n - b) // c
    contexto = rng.choice([
        ("En cierto modelo, la temperatura ambiental $T$, en °C, se relaciona con la cantidad $n$ de chirridos por minuto de un grillo",
         "¿Cuántos chirridos por minuto emite el grillo cuando la temperatura es de", "°C"),
        ("El tiempo $T$, en minutos, que tarda un horno industrial en estar listo se relaciona con la cantidad $n$ de bandejas cargadas",
         "¿Cuántas bandejas se cargaron si el horno tardó", "minutos"),
    ])
    enunciado = (f"{contexto[0]} mediante la ecuación $T = {a} + \\frac{{n - {b}}}{{{c}}}$. {contexto[1]} {t} {contexto[2]}?")
    pasos = (f"Se reemplaza $T = {t}$: ${t} = {a} + \\frac{{n - {b}}}{{{c}}}$. Restando {a}: $\\frac{{n - {b}}}{{{c}}} = {t - a}$. "
             f"Multiplicando por {c}: $n - {b} = {c * (t - a)}$, de donde $n = {n}$.")
    distractores = [
        op(Fraction(c * (t - a)), f"despeja bien pero olvida sumar {b} al final"),
        op(Fraction(c * t - a + b), f"multiplica por {c} solo el valor de $T$ y no toda la diferencia"),
        op(Fraction(t - a, c) + b, f"divide por {c} en vez de multiplicar"),
    ]
    return Propuesta(enunciado, op(Fraction(n)), distractores, pasos,
                     lambda v: a + Fraction(v - b, c) == t, "media")


@plantilla(EJE)
def minimo_para_superar_una_meta(rng):
    precio = rng.randrange(1500, 6001, 500)
    total_unidades = rng.randrange(60, 201, 10)
    meta = precio * total_unidades
    vendidas = rng.randrange(15, total_unidades - 20)
    correcto = total_unidades - vendidas + 1
    cosa = rng.choice(["plantas", "cuadernos artesanales", "frascos de mermelada", "poleras"])
    enunciado = (f"Una persona vende {cosa} por internet a {pesos(precio)} cada unidad. Este mes necesita que sus ventas superen los "
                 f"{pesos(meta)}. Si ya vendió {vendidas} unidades, ¿cuál es la cantidad mínima de unidades que le falta vender para "
                 f"superar esa meta?")
    pasos = (f"Si $n$ es lo que falta vender, se necesita ${miles(precio)} \\cdot ({vendidas} + n) > {miles(meta)}$, es decir, "
             f"${vendidas} + n > {total_unidades}$ y $n > {total_unidades - vendidas}$. El menor entero que lo cumple es {correcto}.")
    distractores = [
        op(total_unidades - vendidas, "con esa cantidad alcanza justo la meta, pero debe superarla"),
        op(total_unidades + 1, "no descuenta las unidades que ya vendió"),
        op(total_unidades, "calcula las unidades que igualan la meta sin descontar las ya vendidas"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: precio * (vendidas + v) > meta and precio * (vendidas + v - 1) <= meta, "alta")


@plantilla(EJE)
def cuando_conviene_una_suscripcion(rng):
    normal = rng.randrange(1800, 4001, 100)
    rebaja = rng.choice([200, 300, 400, 500])
    con_plan = normal - rebaja
    empate = rng.randrange(4, 16)
    suscripcion = rebaja * empate
    producto = rng.choice(["bidones de agua de 20 L", "cilindros de gas pequeños", "cajas de fruta", "sacos de alimento para mascotas"])
    enunciado = (f"Una empresa vende {producto} a {pesos(normal)} cada uno. También ofrece un plan con una suscripción mensual de "
                 f"{pesos(suscripcion)}, con el cual cada unidad comprada en el mes cuesta {pesos(con_plan)}. ¿Cuál es la cantidad mínima "
                 f"de unidades que se deben comprar en un mes para que el plan resulte más barato que comprar sin él?")
    pasos = (f"Con $n$ unidades, el plan cuesta ${miles(suscripcion)} + {miles(con_plan)}n$ y sin plan se pagan ${miles(normal)}n$. "
             f"Se necesita ${miles(suscripcion)} + {miles(con_plan)}n < {miles(normal)}n$, es decir, ${miles(suscripcion)} < {rebaja}n$ "
             f"y $n > {empate}$. El menor entero que lo cumple es {empate + 1}.")
    distractores = [
        op(empate, "con esa cantidad ambas opciones cuestan lo mismo; el plan todavía no es más barato"),
        op(empate - 1, "con esa cantidad todavía conviene comprar sin el plan"),
        op(suscripcion // (normal + con_plan) + 1, "suma los dos precios en vez de restarlos al comparar"),
    ]
    return Propuesta(enunciado, op(empate + 1), distractores, pasos,
                     lambda v: suscripcion + con_plan * v < normal * v and suscripcion + con_plan * (v - 1) >= normal * (v - 1), "alta")


@plantilla(EJE)
def funcion_de_costo_con_rebaja(rng):
    pct = rng.choice([10, 20, 25, 40, 50])
    a = rng.randrange(100, 801, 100)
    b = rng.randrange(200, 2001, 200)
    factor = Fraction(100 - pct, 100)
    na, nb = a * factor, b * factor
    if na.denominator != 1 or nb.denominator != 1:
        raise Descartar
    que, unidad = rng.choice([("procesar $x$ litros de leche", "leche"), ("imprimir $x$ afiches", "afiches"),
                              ("envasar $x$ kilogramos de fruta", "fruta")])
    enunciado = (f"En una empresa, el costo, en pesos, de {que} se modela mediante la función $f(x) = {polinomio([a, b])}$. "
                 f"La empresa encontró una forma de reducir ese costo en un {pct} %. ¿Cuál de las siguientes funciones modela el nuevo costo?")
    pasos = (f"Reducir el costo en un {pct} % equivale a multiplicar toda la función por ${tex(factor)}$: "
             f"${tex(factor)} \\cdot ({polinomio([a, b])}) = {polinomio([na, nb])}$.")

    def alt(coefs, error=None):
        return op(tuple(Fraction(c) for c in coefs), error, f"$g(x) = {polinomio(list(coefs))}$")

    distractores = [
        alt((na, b), "rebaja solo el término que depende de $x$ y deja igual el costo fijo"),
        alt((a, nb), "rebaja solo el costo fijo"),
        alt((a - na, b - nb), "calcula el monto de la rebaja y no el nuevo costo"),
    ]
    return Propuesta(enunciado, alt((na, nb)), distractores, pasos,
                     lambda v: all(v[0] * x + v[1] == (a * x + b) * (100 - pct) / Fraction(100) for x in (0, 10)), "media")


@plantilla(EJE)
def suma_de_valores_de_una_funcion(rng):
    a = rng.randrange(2, 21)
    b = rng.randrange(5, 31, 5)
    c = rng.randrange(1, 6)
    hasta = rng.choice([3, 4])

    def f(n, signo=-1):
        return a + b * n + signo * c * n * n

    correcto = sum(f(n) for n in range(1, hasta + 1))
    enunciado = (f"Considera la función $f$ definida por $f(n) = {a} + {b}n - {c if c > 1 else ''}n^{{2}}$, con $n$ un número real. "
                 f"¿Cuál es el valor de ${' + '.join(f'f({n})' for n in range(1, hasta + 1))}$?")
    valores = ", ".join(f"$f({n}) = {f(n)}$" for n in range(1, hasta + 1))
    pasos = f"Se evalúa cada término: {valores}. La suma es ${correcto}$."
    distractores = [
        op(f(sum(range(1, hasta + 1))), f"suma los valores de $n$ y evalúa una sola vez, calculando $f({sum(range(1, hasta + 1))})$"),
        op(sum(f(n, 1) for n in range(1, hasta + 1)), "suma el término cuadrático en vez de restarlo"),
        op(f(hasta), f"entrega solo $f({hasta})$"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v == sum(a + b * n - c * n ** 2 for n in range(1, hasta + 1)), "media")


@plantilla(EJE)
def simetria_de_una_parabola(rng):
    h = rng.choice([-3, -2, -1, 1, 2, 3])
    t = rng.choice([2, 3, 4])
    lado = rng.choice([-1, 1])
    x1 = h + lado * t
    abre = rng.choice([1, -1])
    vertice_y = -2 * abre
    k = 4 * abre
    correcto = 2 * h - x1
    if correcto in (-x1, x1 - 2 * h, h) or x1 == 0 or correcto == 0:
        raise Descartar
    coef = Fraction(k - vertice_y, t * t)

    def f(x):
        return vertice_y + coef * (x - h) ** 2

    paso = Fraction(1, 8)
    curva = [(float(h - t - 1 + i * paso), float(f(h - t - 1 + i * paso))) for i in range(int((2 * t + 2) / paso) + 1)]
    enunciado = (f"En la figura se representa la gráfica de una función cuadrática $f$ junto con su eje de simetría, la recta $x = {h}$. "
                 f"El punto $P({x1},\\ {k})$ pertenece a la gráfica. ¿Para qué otro valor de $x$ se cumple que $f(x) = {k}$?")
    pasos = (f"Los puntos de la parábola con igual altura están a la misma distancia del eje de simetría. $P$ está a "
             f"$|{x1} - {par(h)}| = {t}$ unidades del eje, así que el otro punto está {t} unidades al otro lado: $x = {correcto}$.")
    distractores = [
        op(-x1, "refleja el punto con respecto al eje $Y$ en vez de hacerlo con respecto al eje de simetría"),
        op(h, "entrega la posición del eje de simetría"),
        op(x1 - 2 * h, "aplica la distancia al eje hacia el mismo lado o con el signo cambiado"),
    ]
    rango = (min(h - t, 0) - 1.6, max(h + t, 0) + 1.6, min(vertice_y, k, 0) - 1.6, max(vertice_y, k, 0) + 1.8)
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v != x1 and f(Fraction(v)) == k, "media",
                     figura=figuras.plano_cartesiano(puntos={"P": (x1, k)}, curva=curva, eje_vertical=h, rango=rango))

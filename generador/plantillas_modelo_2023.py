"""Plantillas con tipos tomados del Modelo de Prueba de Matemática de admisión 2023 (DEMRE, publicado en 2022 junto con su resolución).

Ese modelo es de transición y usa preguntas de 4 y 5 alternativas; aquí todas se adaptan a 4. Se replica la habilidad
evaluada con contextos y números propios; no se copia ningún ítem.
"""
from __future__ import annotations

import itertools
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


def _mixto(v: Fraction) -> str:
    entero = v.numerator // v.denominator
    resto = v - entero
    if resto == 0:
        return str(entero)
    return f"{entero if entero else ''}\\frac{{{resto.numerator}}}{{{resto.denominator}}}"


# ----------------------------------------------------------------- Números

@plantilla(NUM)
def vasos_llenados_hasta_una_fraccion(rng):
    p, q = rng.choice([(3, 4), (2, 3), (4, 5), (3, 5), (5, 6), (1, 2)])
    n = rng.randrange(4, 40) * p
    total = Fraction(n * q, p)
    if total.denominator != 1:
        raise Descartar
    mas = total - n
    recipiente = rng.choice([("un barril", "vasos"), ("un bidón", "botellas"), ("una olla de sopa", "platos")])
    enunciado = (f"Todo el líquido de {recipiente[0]} se reparte en {n} {recipiente[1]} iguales, llenándolos por completo. Si el contenido de otro "
                 f"recipiente idéntico se reparte en {recipiente[1]} iguales a los anteriores, pero llenándolos solo hasta los "
                 f"$\\frac{{{p}}}{{{q}}}$ de su capacidad, ¿cuántos {recipiente[1]} más se necesitan?")
    pasos = (f"Cada uno recibe $\\frac{{{p}}}{{{q}}}$ de lo que recibía antes, así que se necesitan ${n} \\div \\frac{{{p}}}{{{q}}} = "
             f"{n} \\cdot \\frac{{{q}}}{{{p}}} = {tex(total)}$; son ${tex(total)} - {n} = {tex(mas)}$ más.")
    candidatos = [(total, f"responde el total de {recipiente[1]} y no cuántos más"),
                  (Fraction(n * p, q), f"multiplica por $\\frac{{{p}}}{{{q}}}$ en vez de dividir"),
                  (n - Fraction(n * p, q), f"multiplica por $\\frac{{{p}}}{{{q}}}$ y resta"),
                  (Fraction(n, q), f"divide por {q}"),
                  (Fraction(n, p), f"divide por {p}")]
    distractores = [op(v, e) for v, e in _tres_distintos(mas, [(v, e) for v, e in candidatos if v.denominator == 1 and v > 0])]
    return Propuesta(enunciado, op(mas), distractores, pasos, lambda v: (n + v) * p == n * q, "media")


@plantilla(NUM)
def masa_total_con_numeros_mixtos(rng):
    caja = rng.choice([125, 250, 375, 500, 625, 750, 875])
    f1 = rng.choice([Fraction(1, 4), Fraction(3, 4), Fraction(1, 2), Fraction(3, 8), Fraction(5, 8)])
    f2 = rng.choice([Fraction(5, 4), Fraction(3, 2), Fraction(7, 4), Fraction(9, 8)])
    a, b = rng.randrange(2, 8), rng.randrange(2, 6)
    caja_kg = Fraction(caja, 1000)
    total = caja_kg + a * f1 + b * f2
    enunciado = (f"Una caja vacía tiene una masa de {caja} g. Se le agregan {a} paquetes de ${_mixto(f1)}$ kg cada uno y {b} paquetes de "
                 f"${_mixto(f2)}$ kg cada uno. ¿Cuál es la masa total de la caja con los paquetes?")
    pasos = (f"{caja} g son ${frac(caja_kg)}$ kg. La masa es ${frac(caja_kg)} + {a} \\cdot {frac(f1)} + {b} \\cdot {frac(f2)} = {_mixto(total)}$ kg.")
    candidatos = [(a * f1 + b * f2, "olvida la masa de la caja"),
                  (Fraction(caja, 100) + a * f1 + b * f2, "convierte los gramos a kilogramos dividiendo por 100"),
                  (caja_kg + f1 + f2, "suma un solo paquete de cada tipo"),
                  (caja_kg + a * f1 + b * (f2 - 1) + 1, "suma la parte entera de los paquetes mixtos una sola vez"),
                  (caja_kg + (a + b) * f1, "considera que todos los paquetes son del primer tipo")]
    texto = lambda v: f"${_mixto(v)}$ kg"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(total, candidatos)]
    return Propuesta(enunciado, op(total, None, texto(total)), distractores, pasos,
                     lambda v: v * 1000 == caja + 1000 * (a * f1 + b * f2), "media")


@plantilla(NUM)
def descripcion_verbal_de_un_porcentaje(rng):
    p = rng.choice([2, 4, 5, 8, 15, 20, 25, 40])
    cosa = rng.choice(["del precio de un artículo", "del sueldo de una persona", "de la masa de un saco de harina"])
    sustantivo = {"del precio de un artículo": "El precio", "del sueldo de una persona": "El sueldo",
                  "de la masa de un saco de harina": "La masa"}[cosa]
    enunciado = f"¿Cuál de las siguientes cantidades corresponde al ${p}\\,\\%$ {cosa}?"
    opciones = [
        (Fraction(p, 100), f"{sustantivo} dividido por 100 y luego multiplicado por {p}.", None),
        (Fraction(1, p), f"{sustantivo} dividido por {p}.", f"confunde el {p} % con la parte $\\frac{{1}}{{{p}}}$"),
        (Fraction(100, p), f"{sustantivo} dividido por {p} y luego multiplicado por 100.", "invierte la operación del porcentaje"),
        (Fraction(p, 10), f"{sustantivo} multiplicado por {p} décimos.", f"escribe el {p} % como $\\frac{{{p}}}{{10}}$"),
        (Fraction(p), f"{sustantivo} multiplicado por {p}.", "olvida dividir por 100"),
    ]
    correcta = op(opciones[0][0], None, opciones[0][1])
    pasos = f"El ${p}\\,\\%$ de una cantidad es $\\frac{{{p}}}{{100}}$ de ella: se divide por 100 y se multiplica por {p}."
    vistos, distractores = {correcta.valor}, []
    resto = opciones[1:]
    rng.shuffle(resto)
    for v, t, e in resto:
        if v not in vistos and len(distractores) < 3:
            vistos.add(v)
            distractores.append(op(v, e, t))
    return Propuesta(enunciado, correcta, distractores, pasos, lambda v: v * 100 == p, "baja")


@plantilla(NUM)
def diferencia_de_tiempo_que_tarda_la_luz(rng):
    d1 = rng.randrange(20, 60) * 15000
    k = rng.randrange(1, 9)
    d2 = d1 + k * 15000
    c = 300_000_000
    correcto = Fraction((d2 - d1) * 1000, c)
    cuerpo = rng.choice([("un planeta", "dos de sus satélites"), ("una nave", "dos estaciones espaciales")])
    enunciado = (f"Las distancias desde {cuerpo[0]} a {cuerpo[1]} son ${miles(d1)}$ km y ${miles(d2)}$ km. Si la luz viaja a "
                 f"$300.000.000$ m/s, ¿cuál es la diferencia entre los tiempos que tarda la luz en recorrer ambas distancias?")
    pasos = (f"La diferencia de distancias es ${miles(d2 - d1)}$ km $= {miles((d2 - d1) * 1000)}$ m, y el tiempo es distancia dividida por "
             f"rapidez: $\\frac{{{miles((d2 - d1) * 1000)}}}{{300.000.000}} = {tex(correcto)}$ s.")
    candidatos = [(Fraction(d2 - d1, c), "no convierte los kilómetros a metros"),
                  (Fraction((d2 - d1) * 1_000_000, c), "convierte los kilómetros multiplicando por $1.000.000$"),
                  (Fraction((d1 + d2) * 1000, c), "suma las distancias en vez de restarlas"),
                  (Fraction(d2 * 1000, c), "calcula solo el tiempo de la distancia mayor")]
    texto = lambda v: f"${tex(v)}$ s"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, candidatos)]
    if any(len(t.texto) > 30 for t in distractores):
        raise Descartar
    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos,
                     lambda v: v * c == (d2 - d1) * 1000, "media")


# ------------------------------------------------------- Álgebra y funciones

@plantilla(ALG)
def capacidad_desde_dos_fracciones(rng):
    f1, f2 = rng.choice([(Fraction(1, 2), Fraction(5, 6)), (Fraction(1, 3), Fraction(3, 4)), (Fraction(1, 4), Fraction(2, 3)),
                         (Fraction(2, 5), Fraction(7, 10)), (Fraction(1, 2), Fraction(3, 4)), (Fraction(1, 3), Fraction(5, 6))])
    cap = rng.randrange(2, 13) * (f2 - f1).denominator * f1.denominator
    litros = (f2 - f1) * cap
    if litros.denominator != 1:
        raise Descartar
    recipiente = rng.choice(["Un bidón", "Un estanque", "Una botella grande"])
    enunciado = (f"{recipiente} tiene ocupada con agua ${frac(f1)}$ de su capacidad. Al agregar {tex(litros)} L, se llega a ${frac(f2)}$ de su "
                 f"capacidad. ¿Cuál es su capacidad máxima?")
    pasos = (f"Los {tex(litros)} L corresponden a ${frac(f2)} - {frac(f1)} = {frac(f2 - f1)}$ de la capacidad $C$: "
             f"${frac(f2 - f1)} \\cdot C = {tex(litros)}$, de donde $C = {tex(cap)}$ L.")
    candidatos = [(litros / f2, f"plantea que {tex(litros)} L son ${frac(f2)}$ de la capacidad"),
                  (litros * (f2 - f1), "multiplica por la fracción en vez de dividir"),
                  (litros / (f2 + f1), "suma las fracciones en vez de restarlas"),
                  (litros / f1, f"plantea que {tex(litros)} L son ${frac(f1)}$ de la capacidad")]
    texto = lambda v: f"${tex(v)}$ L"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(cap, candidatos)]
    return Propuesta(enunciado, op(cap, None, texto(cap)), distractores, pasos, lambda v: f1 * v + litros == f2 * v, "media")


@plantilla(ALG)
def masa_maxima_con_una_diferencia_dada(rng):
    maximo = rng.choice([90, 100, 110, 120, 150, 160, 180, 200])
    dif = rng.randrange(1, maximo // 20) * 2 * 5
    if dif >= maximo:
        raise Descartar
    menor = Fraction(maximo - dif, 2)
    lugar, definido = rng.choice([("una cama elástica", "la cama elástica"), ("un columpio doble", "el columpio"), ("un bote inflable", "el bote")])
    enunciado = (f"Dos hermanos quieren usar juntos {lugar} que resiste como máximo {maximo} kg. La diferencia entre sus masas es de {dif} kg. "
                 f"¿Cuál es la masa máxima que puede tener el hermano de menor masa para que {definido} los resista a ambos?")
    pasos = (f"Si $x$ es la masa del menor, el mayor tiene $x + {dif}$ y se pide $x + x + {dif} \\le {maximo}$, es decir, $2x \\le {maximo - dif}$ "
             f"y $x \\le {tex(menor)}$ kg.")
    candidatos = [(Fraction(maximo - dif), "olvida que hay dos personas y no divide por 2"),
                  (Fraction(maximo + dif, 2), "calcula la masa máxima del hermano mayor"),
                  (Fraction(maximo, 2) - dif, "divide el máximo en partes iguales y le resta toda la diferencia"),
                  (Fraction(dif), "responde la diferencia de masas")]
    texto = lambda v: f"${tex(v)}$ kg"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(menor, [(v, e) for v, e in candidatos if v > 0])]
    return Propuesta(enunciado, op(menor, None, texto(menor)), distractores, pasos,
                     lambda v: 2 * v + dif == maximo, "media")


@plantilla(ALG)
def lados_consecutivos_desde_el_area(rng):
    paso, tipo = rng.choice([(2, "pares consecutivos"), (1, "enteros consecutivos"), (2, "impares consecutivos")])
    n = rng.randrange(3, 16)
    if tipo == "pares consecutivos":
        n = 2 * rng.randrange(2, 9)
    elif tipo == "impares consecutivos":
        n = 2 * rng.randrange(1, 8) + 1
    area = n * (n + paso)
    enunciado = (f"Las medidas de los lados de un rectángulo, en metros, son números {tipo}. Si su área es de {area} m², ¿cuánto mide el lado "
                 f"menor?")
    pasos = (f"Si el lado menor mide $x$, el mayor mide $x + {paso}$ y $x(x + {paso}) = {area}$. La solución positiva de "
             f"$x^2 + {'' if paso == 1 else paso}x - {area} = 0$ es $x = {n}$, porque ${n} \\cdot {n + paso} = {area}$.")
    candidatos = [(n + paso, "responde el lado mayor"),
                  (Fraction(area, 2), "divide el área por 2"),
                  (n - paso, "resta en vez de sumar al plantear el lado mayor"),
                  (Fraction(area, 4), "divide el área por 4, como si fuera un cuadrado de perímetro conocido")]
    texto = lambda v: f"${tex(v)}$ m"
    distractores = [op(Fraction(v), e, texto(v)) for v, e in _tres_distintos(Fraction(n), [(Fraction(v), e) for v, e in candidatos if v > 0])]
    return Propuesta(enunciado, op(Fraction(n), None, texto(n)), distractores, pasos,
                     lambda v: v > 0 and v * (v + paso) == area, "media")


def _intervalos(tipo, k):
    return {
        "union": f"$]-\\infty, {-k}[ \\cup ]{k}, \\infty[$",
        "inter": f"$]{-k}, {k}[$",
        "mayor": f"$]{k}, \\infty[$",
        "todos": "$]-\\infty, \\infty[$",
        "cerrado": f"$]-\\infty, {-k}] \\cup [{k}, \\infty[$",
    }[tipo]


@plantilla(ALG)
def parametro_para_dos_soluciones_reales(rng):
    a = rng.choice([1, 2, 3, 4])
    signo_c = rng.choice([1, 1, -1])
    raiz = rng.randrange(1, 6)
    if (raiz * raiz) % a:
        raise Descartar
    c = signo_c * Fraction(raiz * raiz, a)
    k = 2 * raiz
    enunciado = (f"¿Cuál de los siguientes conjuntos contiene a todos los números reales $p$ para los cuales la ecuación "
                 f"${a if a > 1 else ''}x^2 + px {'+' if c > 0 else '-'} {frac(abs(c))} = 0$ tiene dos soluciones reales distintas?")
    if c > 0:
        correcto = ("union", k)
        pasos = (f"Hay dos soluciones reales distintas si el discriminante es positivo: $p^2 - 4 \\cdot {a} \\cdot {frac(c)} > 0$, es decir, "
                 f"$p^2 > {k * k}$, que se cumple si $p < {-k}$ o $p > {k}$.")
        candidatos = [(("inter", k), "invierte la desigualdad del discriminante"), (("mayor", k), "considera solo los valores positivos de $p$"),
                      (("cerrado", k), "incluye los valores en que el discriminante es cero"), (("todos", 0), "supone que siempre hay dos soluciones")]
    else:
        correcto = ("todos", 0)
        pasos = (f"El discriminante es $p^2 - 4 \\cdot {a} \\cdot ({frac(c)}) = p^2 + {k * k}$, que es positivo para todo $p$: siempre hay dos "
                 f"soluciones reales distintas.")
        candidatos = [(("union", k), "olvida que el término libre es negativo"), (("inter", k), "olvida el signo e invierte la desigualdad"),
                      (("mayor", k), "considera solo valores positivos de $p$ mayores que la raíz")]

    def comprobar(v):
        tipo, kk = v
        for p in [x / 4 for x in range(-60, 61)]:
            disc = p * p - 4 * a * float(c)
            dentro = {"union": p < -kk or p > kk, "inter": -kk < p < kk, "mayor": p > kk, "todos": True, "cerrado": p <= -kk or p >= kk}[tipo]
            if dentro != (disc > 1e-12):
                return False
        return True

    distractores = [op(v, e, _intervalos(*v)) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, _intervalos(*correcto)), distractores, pasos, comprobar, "alta")


@plantilla(ALG)
def cobro_con_recargo_sobre_un_umbral(rng):
    fijo = rng.randrange(8, 30) * 100
    q = rng.randrange(5, 15) * 10
    umbral = rng.choice([100, 150, 200, 250, 300])
    r = rng.randrange(2, 9) * 10
    servicio = rng.choice([("Una compañía eléctrica", "kWh"), ("Una empresa de agua potable", "m³")])
    enunciado = (f"{servicio[0]} cobra mensualmente un cargo fijo de {pesos(fijo)} y {pesos(q)} por cada {servicio[1]} consumido. Si en un mes se "
                 f"superan los {umbral} {servicio[1]}, se aplica un recargo de {pesos(r)} por cada {servicio[1]} de exceso. ¿Cuál de las siguientes "
                 f"funciones permite calcular el total a pagar por $x$ {servicio[1]}, si $x > {umbral}$?")
    nombres = iter(rng.sample(["f", "g", "h", "p", "s"], 4))
    formas = {
        "correcta": ((fijo - r * umbral, q + r), f"{miles(fijo)} + {q}x + {r}(x - {umbral})"),
        "umbral_fijo": ((fijo + q * umbral, r), f"{miles(fijo)} + {umbral} \\cdot {q} + {r}x"),
        "sin_umbral": ((fijo, q + r), f"{miles(fijo)} + {q + r}x"),
        "recargo_fijo": ((fijo + r * umbral, q), f"{miles(fijo)} + {q}x + {r} \\cdot {umbral}"),
        "exceso_mal": ((fijo + r * umbral, q + r), f"{miles(fijo)} + {q}x + {r}(x + {umbral})"),
    }
    errores = {"umbral_fijo": "cobra a precio normal solo los primeros consumos y el exceso solo con el recargo",
               "sin_umbral": "aplica el recargo a todo el consumo y no solo al exceso",
               "recargo_fijo": "aplica el recargo a la cantidad del umbral en vez de al exceso",
               "exceso_mal": "calcula el exceso sumando el umbral en vez de restarlo"}
    pasos = (f"Todo el consumo se cobra a {pesos(q)} y solo el exceso, $x - {umbral}$, lleva además el recargo: "
             f"${miles(fijo)} + {q}x + {r}(x - {umbral})$.")

    def texto(clave):
        return f"${next(nombres)}(x) = {formas[clave][1]}$"

    claves = ["umbral_fijo", "sin_umbral", "recargo_fijo", "exceso_mal"]
    rng.shuffle(claves)
    elegidos = _tres_distintos(formas["correcta"][0], [(formas[c][0], c) for c in claves])
    correcta = op(formas["correcta"][0], None, texto("correcta"))
    distractores = [op(v, errores[c], texto(c)) for v, c in elegidos]
    total = lambda x: fijo + q * x + r * max(0, x - umbral)
    return Propuesta(enunciado, correcta, distractores, pasos,
                     lambda v: all(v[0] + v[1] * x == total(x) for x in (umbral + 1, umbral + 37, umbral + 200)), "media")


@plantilla(ALG)
def funcion_cuadratica_desde_el_maximo_y_un_punto(rng):
    t_max = rng.randrange(2, 9)
    m = rng.randrange(1, 6)
    altura_1 = m * (2 * t_max - 1)
    c2, c1 = -m, 2 * t_max * m
    enunciado = (f"Un proyectil se lanza desde el nivel del suelo y sigue una trayectoria parabólica que alcanza su altura máxima a los {t_max} "
                 f"segundos. Si al primer segundo alcanzó una altura de {altura_1} m, ¿cuál de las siguientes funciones modela la altura, en m, "
                 f"a los $t$ segundos?")
    pasos = (f"Parte del suelo, así que $h(t) = at^2 + bt$. El máximo en $t = {t_max}$ exige $-\\frac{{b}}{{2a}} = {t_max}$, o sea $b = {-2 * t_max}a$. "
             f"Con $h(1) = a + b = {altura_1}$ se obtiene $a({1 - 2 * t_max}) = {altura_1}$, $a = {c2}$ y $b = {c1}$.")
    nombres = iter(rng.sample(["f", "g", "h", "p", "s"], 4))

    def texto(v):
        return f"${next(nombres)}(t) = {polinomio([v[0], v[1], 0], 't')}$"

    candidatos = [((Fraction(altura_1), Fraction(0)), "usa la altura del primer segundo como coeficiente de $t^2$"),
                  ((Fraction(-1), Fraction(altura_1 + 1)), "supone que el coeficiente de $t^2$ es $-1$ y ajusta solo el punto"),
                  ((Fraction(-m), Fraction(t_max * m)), "usa $b = -t_{max} \\cdot a$, olvidando el 2 de la fórmula del vértice"),
                  ((Fraction(m), Fraction(-2 * t_max * m)), "invierte los signos: la parábola se abre hacia arriba")]
    correcto = (Fraction(c2), Fraction(c1))
    correcta = op(correcto, None, texto(correcto))
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, correcta, distractores, pasos,
                     lambda v: v[0] < 0 and -v[1] / (2 * v[0]) == t_max and v[0] + v[1] == altura_1, "alta")


# ----------------------------------------------------------------- Geometría

@plantilla(GEO)
def escalera_que_se_desliza(rng):
    pie, alto, largo = rng.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (9, 12, 15), (12, 9, 15), (7, 24, 25)])
    baja = rng.randrange(1, alto // 2 + 1)
    nuevo_alto = alto - baja
    cuadrado = largo * largo - nuevo_alto * nuevo_alto
    if math.isqrt(cuadrado) ** 2 == cuadrado:
        raise Descartar
    objeto = rng.choice(["un madero", "una escalera", "una tabla"])
    enunciado = (f"Se apoya {objeto} de {largo} m de largo en una pared vertical, con su pie a {pie} m de la pared. Si el extremo superior se "
                 f"desliza {baja} m hacia abajo por la pared, ¿cuántos metros se aleja el pie de su posición inicial?")
    pasos = (f"Al inicio la altura es $\\sqrt{{{largo}^2 - {pie}^2}} = {alto}$ m. Después es {nuevo_alto} m y el pie queda a "
             f"$\\sqrt{{{largo}^2 - {nuevo_alto}^2}} = \\sqrt{{{cuadrado}}}$ m; se alejó $(\\sqrt{{{cuadrado}}} - {pie})$ m.")

    def texto(v):
        cuad, resta = v
        r = raiz_tex(cuad)
        return f"$({r} - {resta})$ m" if resta else f"${r}$ m"

    otro = largo * largo - (alto + baja) ** 2
    candidatos = [((cuadrado, 0), "responde la nueva distancia del pie y no cuánto se alejó"),
                  ((baja * baja, 0), "supone que el pie se aleja lo mismo que bajó el extremo"),
                  ((largo * largo - baja * baja, pie), "aplica el teorema de Pitágoras con el desplazamiento en vez de la nueva altura"),
                  ((nuevo_alto * nuevo_alto + pie * pie, pie), "suma los cuadrados en vez de restarlos")]
    if otro > 0:
        candidatos.append(((otro, pie), "sube el extremo en vez de bajarlo"))
    correcto = (cuadrado, pie)
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if v[0] > 0])]
    if len({d.texto for d in distractores} | {texto(correcto)}) < 4:
        raise Descartar
    real = math.sqrt(largo ** 2 - (alto - baja) ** 2) - pie
    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos,
                     lambda v: abs(math.sqrt(v[0]) - v[1] - real) < 1e-9, "alta")


def _resta_pi(v) -> str:
    entero, pi = v
    return f"$({tex(entero)} - {tex(pi)}\\pi)$ cm²"


@plantilla(GEO)
def area_no_barrida_por_dos_plumillas(rng):
    r = rng.randrange(4, 13)
    largo = rng.randrange(2 * r, 2 * r + 12)
    ancho = rng.randrange(r, r + 8)
    if r % 2:
        raise Descartar
    correcto = (Fraction(largo * ancho), Fraction(r * r, 2))
    enunciado = (f"El parabrisas rectangular de un auto de juguete mide {largo} cm de largo y {ancho} cm de ancho. Tiene dos plumillas de "
                 f"{r} cm, con centro de giro en las esquinas inferiores, y cada una barre un cuarto de círculo, como se representa en la "
                 f"figura. ¿Cuál es el área del parabrisas que no limpian las plumillas?")
    pasos = (f"Cada plumilla barre $\\frac{{1}}{{4}}\\pi \\cdot {r}^2 = {tex(Fraction(r * r, 4))}\\pi$ cm²; las dos, ${tex(Fraction(r * r, 2))}\\pi$ cm². "
             f"El área sin limpiar es {_resta_pi(correcto)}.")
    candidatos = [((Fraction(largo * ancho), Fraction(r * r)), "considera que cada plumilla barre medio círculo"),
                  ((Fraction(largo * ancho), Fraction(r * r, 4)), "considera una sola plumilla"),
                  ((Fraction(largo * ancho), Fraction(r)), "usa el perímetro del cuarto de círculo en vez del área"),
                  ((Fraction(2 * (largo + ancho)), Fraction(r * r, 2)), "usa el perímetro del rectángulo en vez del área")]
    distractores = [op(v, e, _resta_pi(v)) for v, e in _tres_distintos(correcto, candidatos)]
    figura = figuras.rectangulo_con_cuartos_de_circulo(largo, ancho, r, f"{largo} cm", f"{ancho} cm", f"{r} cm")
    real = largo * ancho - 2 * math.pi * r * r / 4
    return Propuesta(enunciado, op(correcto, None, _resta_pi(correcto)), distractores, pasos,
                     lambda v: abs(float(v[0]) - float(v[1]) * math.pi - real) < 1e-9, "media", figura=figura)


# ------------------------------------------------- Probabilidad y estadística

@plantilla(PRO)
def promedio_de_aportes_en_razon(rng):
    k = rng.choice([2, 3])
    base = rng.randrange(2, 30) * 5000
    aportes = [base, base * k, base * k * k]
    total = sum(aportes)
    nombres = rng.sample(["Claudia", "María", "Yasna", "Rocío", "Fernanda", "Javiera"], 3)
    veces = {2: "el doble", 3: "el triple"}[k]
    enunciado = (f"Tres amigas reunieron en total {pesos(total)}. {nombres[1]} aportó {veces} que {nombres[0]}, y {nombres[2]} aportó {veces} que "
                 f"{nombres[1]}. ¿Cuál es el promedio del dinero aportado por {nombres[1]} y {nombres[2]}?")
    correcto = Fraction(aportes[1] + aportes[2], 2)
    pasos = (f"Si {nombres[0]} aportó $x$, entonces $x + {k}x + {k * k}x = {miles(total)}$, de donde $x = {miles(base)}$. {nombres[1]} aportó "
             f"{pesos(aportes[1])} y {nombres[2]} {pesos(aportes[2])}; el promedio es {pesos(int(correcto))}.")
    candidatos = [(Fraction(total, 3), "calcula el promedio de las tres amigas"),
                  (Fraction(total, 2), "divide el total por 2"),
                  (Fraction(aportes[1] + aportes[2]), "suma los aportes y no los divide"),
                  (Fraction(aportes[1]), f"responde el aporte de {nombres[1]}"),
                  (Fraction(aportes[0] + aportes[2], 2), f"promedia los aportes de {nombres[0]} y {nombres[2]}")]
    distractores = [op(v, e, pesos(int(v))) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if v.denominator == 1])]
    return Propuesta(enunciado, op(correcto, None, pesos(int(correcto))), distractores, pasos,
                     lambda v: 2 * v == total - Fraction(total, 1 + k + k * k), "media")


def _percentil(datos, q):
    rango = max(1, math.ceil(q / 100 * len(datos)))
    return datos[rango - 1]


_CONJUNTOS = [tuple(c) for c in itertools.combinations_with_replacement(range(1, 5), 6)]


@plantilla(PRO)
def afirmacion_que_se_deduce_de_un_percentil(rng):
    q = rng.choice([15, 20, 30, 35, 40, 45, 60, 65])
    mayor = rng.choice([r for r in (25, 50, 70, 75, 80, 90) if r > q])
    menor = rng.choice([r for r in (10, 20, 25, 30) if r < q] or [10])
    if menor >= q:
        raise Descartar
    afirmaciones = {
        "correcta": (f"$P$ es menor o igual que el percentil {mayor} de los datos.", lambda d, P: P <= _percentil(d, mayor)),
        "estricta_menor": (f"$P$ es mayor que el percentil {menor} de los datos.", lambda d, P: P > _percentil(d, menor)),
        "media": ("La media aritmética de los datos es mayor que $P$.", lambda d, P: sum(d) / len(d) > P),
        "cuartil": ("$P$ es menor que el tercer cuartil de los datos.", lambda d, P: P < _percentil(d, 75)),
        "mediana": ("La mediana de los datos es mayor que $P$.", lambda d, P: _percentil(d, 50) > P),
    }
    errores = {"estricta_menor": f"olvida que el percentil {menor} y el percentil {q} pueden ser iguales",
               "media": "supone que la media se ubica siempre por sobre los percentiles bajos",
               "cuartil": "olvida que el percentil y el tercer cuartil pueden coincidir",
               "mediana": "olvida que el percentil y la mediana pueden coincidir"}
    if q > 50:
        del afirmaciones["mediana"]
    enunciado = f"Considera un grupo de datos numéricos. Si $P$ es el percentil {q} de estos datos, ¿cuál de las siguientes afirmaciones se puede deducir?"
    pasos = (f"Los percentiles no decrecen: como ${q} < {mayor}$, el percentil {q} es menor o igual que el percentil {mayor}. Las demás comparaciones "
             f"estrictas pueden fallar cuando varios datos se repiten, por ejemplo si todos los datos son iguales.")
    claves = [c for c in afirmaciones if c != "correcta"]
    rng.shuffle(claves)
    elegidos = claves[:3]
    correcta = op("correcta", None, afirmaciones["correcta"][0])
    distractores = [op(c, errores[c], afirmaciones[c][0]) for c in elegidos]
    return Propuesta(enunciado, correcta, distractores, pasos,
                     lambda v: all(afirmaciones[v][1](d, _percentil(d, q)) for d in _CONJUNTOS), "alta")


@plantilla(PRO, "M2")
def elegir_de_varios_grupos(rng):
    grupos = rng.sample([5, 6, 7, 8, 9, 10, 12], 3)
    k = rng.choice([2, 3]) if min(grupos) >= 5 else 2
    temas = rng.sample(["matemática", "literatura", "biología", "historia", "química", "física"], 3)
    persona = rng.choice(["Jacinta", "Tomás", "Ignacia", "Benjamín"])
    enunciado = (f"{persona} tiene {grupos[0]} libros de {temas[0]}, {grupos[1]} de {temas[1]} y {grupos[2]} de {temas[2]}, todos distintos. "
                 f"¿De cuántas maneras puede escoger {k} libros de cada tema?")
    combos = [math.comb(g, k) for g in grupos]
    correcto = combos[0] * combos[1] * combos[2]
    b = lambda g: f"\\binom{{{g}}}{{{k}}}"
    textos = {
        "correcta": f"${b(grupos[0])} \\cdot {b(grupos[1])} \\cdot {b(grupos[2])}$",
        "suma": f"${b(grupos[0])} + {b(grupos[1])} + {b(grupos[2])}$",
        "junto": f"$\\binom{{{sum(grupos)}}}{{{3 * k}}}$",
        "orden": f"$\\frac{{{grupos[0]}!}}{{{grupos[0] - k}!}} \\cdot \\frac{{{grupos[1]}!}}{{{grupos[1] - k}!}} \\cdot \\frac{{{grupos[2]}!}}{{{grupos[2] - k}!}}$",
        "potencia": f"$({grupos[0]} \\cdot {grupos[1]} \\cdot {grupos[2]})^{{{k}}}$",
    }
    valores = {"correcta": correcto, "suma": sum(combos), "junto": math.comb(sum(grupos), 3 * k),
               "orden": math.perm(grupos[0], k) * math.perm(grupos[1], k) * math.perm(grupos[2], k),
               "potencia": (grupos[0] * grupos[1] * grupos[2]) ** k}
    errores = {"suma": "suma las formas de cada tema, como si eligiera de un solo tema",
               "junto": "junta todos los libros y elige sin respetar los temas",
               "orden": "considera que importa el orden en que escoge los libros",
               "potencia": "permite escoger el mismo libro más de una vez"}
    pasos = (f"Para cada tema se eligen {k} libros sin importar el orden, y las elecciones se combinan por el principio multiplicativo: "
             f"${b(grupos[0])} \\cdot {b(grupos[1])} \\cdot {b(grupos[2])} = {combos[0]} \\cdot {combos[1]} \\cdot {combos[2]} = {miles(correcto)}$.")
    claves = ["suma", "junto", "orden", "potencia"]
    rng.shuffle(claves)
    elegidos = _tres_distintos(correcto, [(valores[c], c) for c in claves])
    distractores = [op(v, errores[c], textos[c]) for v, c in elegidos]
    real = 1
    for g in grupos:
        real *= sum(1 for _ in itertools.combinations(range(g), k))
    return Propuesta(enunciado, op(correcto, None, textos["correcta"]), distractores, pasos, lambda v: v == real, "media")


@plantilla(PRO, "M2")
def colorear_en_fila_sin_repetir_vecinos(rng):
    n = rng.randrange(4, 10)
    c = rng.randrange(3, 13)
    correcto = c * (c - 1) ** (n - 1)
    enunciado = (f"Un adorno está formado por {n} cuadrados en fila. Se dispone de {c} colores distintos y cada cuadrado se pinta de un solo color, "
                 f"de modo que dos cuadrados vecinos no tengan el mismo color. ¿Cuántos adornos distintos se pueden formar?")
    pasos = (f"El primer cuadrado admite {c} colores y cada uno de los {n - 1} siguientes, cualquiera menos el de su vecino anterior: "
             f"${c} \\cdot {c - 1}^{{{n - 1}}}$.")
    textos = {"correcta": f"${c} \\cdot {c - 1}^{{{n - 1}}}$", "libre": f"${c}^{{{n}}}$", "resta": f"$({c - 1})^{{{n}}}$",
              "perm": f"$\\frac{{{c}!}}{{{c - n}!}}$" if c >= n else f"${c} \\cdot {c - 1} \\cdot {c - 2}$", "producto": f"${n} \\cdot {c}$",
              "menos_uno": f"${c} \\cdot {c - 1}^{{{n}}}$"}
    valores = {"correcta": correcto, "libre": c ** n, "resta": (c - 1) ** n,
               "perm": math.perm(c, n) if c >= n else c * (c - 1) * (c - 2), "producto": n * c, "menos_uno": c * (c - 1) ** n}
    errores = {"libre": "permite que dos vecinos tengan el mismo color", "resta": "descuenta un color también en el primer cuadrado",
               "perm": "exige que todos los cuadrados tengan colores distintos", "producto": "multiplica la cantidad de cuadrados por la de colores",
               "menos_uno": f"aplica la restricción a los {n} cuadrados y no solo a los {n - 1} que tienen un vecino anterior"}
    claves = ["libre", "resta", "perm", "producto", "menos_uno"]
    rng.shuffle(claves)
    elegidos = _tres_distintos(correcto, [(valores[k], k) for k in claves])
    distractores = [op(v, errores[k], textos[k]) for v, k in elegidos]
    cuenta = [1] * c
    for _ in range(n - 1):
        total = sum(cuenta)
        cuenta = [total - x for x in cuenta]
    real = sum(cuenta)
    return Propuesta(enunciado, op(correcto, None, textos["correcta"]), distractores, pasos, lambda v: v == real, "media")

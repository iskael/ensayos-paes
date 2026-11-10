from __future__ import annotations

import itertools
import statistics
from fractions import Fraction

from nucleo import Descartar, Propuesta, frac, op, opf, plantilla, simplificada, tex

EJE = "probabilidad_estadistica"


@plantilla(EJE)
def probabilidad_en_una_urna(rng):
    rojas, azules, verdes = (rng.randrange(2, 10) for _ in range(3))
    total = rojas + azules + verdes
    bolsa = ["roja"] * rojas + ["azul"] * azules + ["verde"] * verdes
    base = (f"En una bolsa hay {rojas} fichas rojas, {azules} azules y {verdes} verdes, todas de igual forma y tamaño. "
            f"Si se extrae una ficha al azar, ")
    if rng.random() < 0.5:
        if azules >= rojas + verdes:
            raise Descartar
        favorable = lambda f: f == "azul"
        correcto = Fraction(azules, total)
        enunciado = base + "¿cuál es la probabilidad de que sea azul?"
        pasos = (f"Hay {azules} casos favorables de un total de {total} fichas: "
                 f"$P = {simplificada(azules, total)}$.")
        distractores = [
            opf(Fraction(azules, rojas + verdes), "compara las azules con las demás fichas en vez de con el total"),
            opf(Fraction(1, 3), "supone que los tres colores son igual de probables"),
            opf(Fraction(rojas + verdes, total), "calcula la probabilidad de que no sea azul"),
        ]
        dificultad = "baja"
    else:
        favorable = lambda f: f != "roja"
        correcto = Fraction(azules + verdes, total)
        enunciado = base + "¿cuál es la probabilidad de que no sea roja?"
        pasos = (f"Las fichas que no son rojas son ${azules} + {verdes} = {azules + verdes}$ de un total de {total}: "
                 f"$P = {simplificada(azules + verdes, total)}$.")
        distractores = [
            opf(Fraction(rojas, total), "calcula la probabilidad de que sea roja"),
            opf(Fraction(2, 3), "supone que los tres colores son igual de probables"),
            opf(Fraction(azules, total), "considera solo uno de los dos colores favorables"),
        ]
        dificultad = "media"
    real = Fraction(sum(1 for f in bolsa if favorable(f)), len(bolsa))
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == real, dificultad)


@plantilla(EJE)
def dos_extracciones_sin_reposicion(rng):
    rojas = rng.randrange(3, 9)
    otras = rng.randrange(2, 9)
    total = rojas + otras
    color = rng.choice(["rojas", "blancas", "negras"])
    correcto = Fraction(rojas * (rojas - 1), total * (total - 1))
    enunciado = (f"Una caja contiene {total} bolitas de igual tamaño, de las cuales {rojas} son {color}. "
                 f"Si se extraen dos bolitas al azar, una tras otra y sin reposición, ¿cuál es la probabilidad de que ambas sean {color}?")
    pasos = (f"La primera es {color[:-1]} con probabilidad $\\frac{{{rojas}}}{{{total}}}$. Sin reponerla quedan "
             f"{rojas - 1} {color} entre {total - 1} bolitas, así que la segunda lo es con probabilidad "
             f"$\\frac{{{rojas - 1}}}{{{total - 1}}}$. El producto es ${frac(correcto)}$.")
    suma = Fraction(rojas, total) + Fraction(rojas - 1, total - 1)
    if suma >= 1:
        raise Descartar
    distractores = [
        opf(Fraction(rojas, total) ** 2, "calcula como si la primera bolita se devolviera a la caja"),
        opf(suma, "suma las probabilidades de cada extracción en vez de multiplicarlas"),
        opf(Fraction(rojas * (rojas - 1), total * total), "descuenta la bolita extraída de las favorables pero no del total"),
    ]
    bolitas = [True] * rojas + [False] * otras
    pares = list(itertools.permutations(range(total), 2))
    real = Fraction(sum(1 for i, j in pares if bolitas[i] and bolitas[j]), len(pares))
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == real, "alta")


@plantilla(EJE)
def suma_de_dos_dados(rng):
    s = rng.randrange(4, 11)
    casos = [(i, j) for i in range(1, 7) for j in range(1, 7) if i + j == s]
    n = len(casos)
    correcto = Fraction(n, 36)
    enunciado = (f"Se lanzan dos dados comunes de seis caras. ¿Cuál es la probabilidad de que la suma de los "
                 f"puntos obtenidos sea {s}?")
    lista = ", ".join(f"({i}, {j})" for i, j in casos)
    pasos = (f"Hay 36 resultados posibles igual de probables. Los que suman {s} son {n}: {lista}. "
             f"Entonces $P = {simplificada(n, 36)}$.")
    distractores = [
        opf(Fraction(1, 11), "considera las 11 sumas posibles (del 2 al 12) como igual de probables"),
        opf(Fraction((n + 1) // 2, 36), "no distingue el orden de los dados, por ejemplo cuenta (1, 3) y (3, 1) como un solo caso"),
        opf(Fraction(s, 36), "usa el valor de la suma como número de casos favorables"),
    ]
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: v * 36 == sum(1 for i, j in itertools.product(range(1, 7), repeat=2) if i + j == s), "media")


@plantilla(EJE)
def mediana_de_datos(rng):
    contexto = rng.choice([
        ("Las edades, en años, de los integrantes de un taller son", 12, 60),
        ("Los goles anotados por un equipo en sus últimos partidos fueron", 0, 9),
        ("Los minutos que tardaron ocho estudiantes en resolver un problema fueron", 5, 40),
        ("Las temperaturas máximas, en °C, registradas durante ocho días fueron", 8, 34),
    ])
    n = rng.choice([6, 8])
    datos = [rng.randrange(contexto[1], contexto[2] + 1) for _ in range(n)]
    ordenados = sorted(datos)
    if datos == ordenados or Fraction(sum(datos), n).denominator > 2:
        raise Descartar
    c1, c2 = ordenados[n // 2 - 1], ordenados[n // 2]
    correcto = Fraction(c1 + c2, 2)
    intro = contexto[0].replace("ocho", "seis") if n == 6 else contexto[0]
    enunciado = f"{intro}: {', '.join(map(str, datos))}. ¿Cuál es la mediana de estos datos?"
    pasos = (f"Ordenados de menor a mayor: {', '.join(map(str, ordenados))}. Como hay {n} datos, la mediana es el "
             f"promedio de los dos centrales: $\\frac{{{c1} + {c2}}}{{2}} = {tex(correcto)}$.")
    distractores = [
        op(Fraction(datos[n // 2 - 1] + datos[n // 2], 2), "promedia los dos datos centrales sin ordenar antes la lista"),
        op(Fraction(sum(datos), n), "calcula la media aritmética en vez de la mediana"),
        op(Fraction(ordenados[-1] - ordenados[0]), "calcula el rango (máximo menos mínimo)"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v == Fraction(statistics.median(datos)).limit_denominator(2), "media")


@plantilla(EJE)
def puntaje_necesario_para_un_promedio(rng):
    n = rng.choice([3, 4])
    previos = [rng.randrange(40, 96, 5) * 10 for _ in range(n)]
    suma = sum(previos)
    if suma % n:
        raise Descartar
    objetivo = rng.randrange(50, 86, 5) * 10
    correcto = (n + 1) * objetivo - suma
    if not 150 <= correcto <= 1000 or n * objetivo - suma <= 0:
        raise Descartar
    enunciado = (f"En sus primeros {n} ensayos, Valentina obtuvo {', '.join(map(str, previos[:-1]))} y {previos[-1]} puntos. "
                 f"¿Qué puntaje necesita en el siguiente ensayo para que el promedio de los {n + 1} ensayos sea {objetivo} puntos?")
    pasos = (f"Para promediar {objetivo} en {n + 1} ensayos se necesita un total de ${n + 1} \\cdot {objetivo} = "
             f"{(n + 1) * objetivo}$ puntos. Ya lleva {suma}, así que necesita ${(n + 1) * objetivo} - {suma} = {correcto}$.")
    distractores = [
        op(objetivo, "cree que basta con obtener el mismo valor del promedio buscado"),
        op(n * objetivo - suma, f"calcula el total necesario con {n} ensayos en vez de {n + 1}"),
        op(2 * objetivo - suma // n, "compensa una sola vez la diferencia entre el promedio actual y el buscado"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: Fraction(suma + v, n + 1) == objetivo, "alta")


@plantilla(EJE)
def principio_multiplicativo(rng):
    a, b, c = rng.randrange(2, 7), rng.randrange(2, 7), rng.randrange(2, 6)
    enunciado = rng.choice([
        f"Un restaurante ofrece un menú formado por una entrada, un plato de fondo y un postre. Si hay {a} entradas, "
        f"{b} platos de fondo y {c} postres, ¿cuántos menús distintos se pueden armar?",
        f"Martina tiene {a} poleras, {b} pantalones y {c} pares de zapatillas. Si elige una prenda de cada tipo, "
        f"¿de cuántas maneras distintas puede vestirse?",
        f"Una heladería ofrece {a} sabores de helado, {b} tipos de salsa y {c} tipos de cono. Si un helado lleva un sabor, "
        f"una salsa y un cono, ¿cuántos helados distintos se pueden pedir?",
    ])
    correcto = a * b * c
    pasos = (f"Por el principio multiplicativo, cada elección se combina con todas las demás: "
             f"${a} \\cdot {b} \\cdot {c} = {correcto}$.")
    distractores = [
        op(a + b + c, "suma las cantidades en vez de multiplicarlas"),
        op(a * b + c, "multiplica solo las dos primeras cantidades y suma la tercera"),
        op((a + b) * c, "suma las dos primeras cantidades antes de multiplicar"),
    ]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v == len(list(itertools.product(range(a), range(b), range(c)))), "baja")


@plantilla(EJE)
def media_desde_tabla_de_frecuencias(rng):
    que, quienes = rng.choice([("hermanos", "estudiantes de un curso"), ("mascotas", "familias de un edificio"),
                               ("libros leídos en el semestre", "estudiantes de un taller")])
    frecuencias = [rng.randrange(1, 10) for _ in range(4)]
    total = sum(frecuencias)
    ponderada = sum(x * f for x, f in enumerate(frecuencias))
    correcto = Fraction(ponderada, total)
    if total not in (10, 20, 25):
        raise Descartar
    f0, f1, f2, f3 = frecuencias
    enunciado = (f"Se preguntó a {total} {quienes} por su número de {que}: {f0} respondieron 0, {f1} respondieron 1, "
                 f"{f2} respondieron 2 y {f3} respondieron 3. ¿Cuál es el promedio de {que} por persona encuestada?"
                 if "familias" not in quienes else
                 f"Se preguntó a {total} {quienes} por su número de {que}: {f0} respondieron 0, {f1} respondieron 1, "
                 f"{f2} respondieron 2 y {f3} respondieron 3. ¿Cuál es el promedio de {que} por familia encuestada?")
    pasos = (f"Se pondera cada valor por su frecuencia: $0 \\cdot {f0} + 1 \\cdot {f1} + 2 \\cdot {f2} + 3 \\cdot {f3} = "
             f"{ponderada}$. Al dividir por el total de respuestas, ${ponderada} : {total} = {tex(correcto)}$.")
    distractores = [
        op(Fraction(3, 2), "promedia los valores 0, 1, 2 y 3 sin considerar cuántas veces aparece cada uno"),
        op(Fraction(total, 4), "promedia las frecuencias en vez de los datos"),
        op(Fraction(ponderada, 4), "divide por la cantidad de valores distintos y no por el total de respuestas"),
    ]
    datos = [x for x, f in enumerate(frecuencias) for _ in range(f)]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v * len(datos) == sum(datos), "media")

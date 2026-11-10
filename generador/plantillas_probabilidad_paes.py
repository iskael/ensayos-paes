"""Plantillas de probabilidad y estadística modeladas en tipos de pregunta de las PAES M1 de admisión 2023 a 2026 (DEMRE).

Se replica la habilidad evaluada con contextos y números propios; ninguna copia un ítem oficial.
Las tablas, los diagramas de cajón y las cajas con bolitas se entregan como figura.
"""
from __future__ import annotations

import itertools
import statistics
from fractions import Fraction

import figuras
from nucleo import Descartar, Propuesta, frac, miles, op, opf, pesos, plantilla, tex

EJE = "probabilidad_estadistica"


def _tres_distintos(correcto, candidatos):
    elegidos, vistos = [], {correcto}
    for valor, error in candidatos:
        if valor not in vistos:
            vistos.add(valor)
            elegidos.append((valor, error))
        if len(elegidos) == 3:
            return elegidos
    raise Descartar


@plantilla(EJE)
def total_de_datos_en_una_tabla(rng):
    que, columna, quienes = rng.choice([
        ("los puntajes de una prueba en un curso", "Puntaje", "estudiantes rindieron la prueba"),
        ("la cantidad de hermanos de los integrantes de un taller", "Hermanos", "personas integran el taller"),
        ("los goles por partido de un campeonato", "Goles", "partidos se jugaron"),
    ])
    n = rng.randrange(5, 8)
    valores = list(range(1, n + 1)) if columna == "Puntaje" else list(range(0, n))
    frecuencias = [rng.randrange(2, 10) for _ in valores]
    total = sum(frecuencias)
    enunciado = f"En la tabla de la figura se resume la distribución de {que}. ¿Cuántos {quienes}?" if columna != "Hermanos" else \
        f"En la tabla de la figura se resume la distribución de {que}. ¿Cuántas {quienes}?"
    pasos = f"El total de datos es la suma de las frecuencias: ${' + '.join(map(str, frecuencias))} = {total}$."
    candidatos = [
        (n, "cuenta las filas de la tabla en vez de sumar las frecuencias"),
        (sum(valores), f"suma los valores de la columna {columna} en vez de las frecuencias"),
        (sum(x * f for x, f in zip(valores, frecuencias)), "multiplica cada valor por su frecuencia y suma, como si calculara un total de puntos"),
        (max(frecuencias), "entrega la frecuencia más alta"),
    ]
    distractores = [op(v, e) for v, e in _tres_distintos(total, candidatos)]
    datos = [x for x, f in zip(valores, frecuencias) for _ in range(f)]
    return Propuesta(enunciado, op(total), distractores, pasos, lambda v: v == len(datos), "baja",
                     figura=figuras.tabla([columna, "Frecuencia"], [[x, f] for x, f in zip(valores, frecuencias)]))


@plantilla(EJE)
def probabilidad_desde_una_tabla_de_preferencias(rng):
    tema, categorias = rng.choice([
        ("su fruta preferida", ["Uva", "Pera", "Manzana", "Naranja", "Frutilla"]),
        ("su sabor de helado favorito", ["Vainilla", "Chocolate", "Frutilla", "Manjar", "Menta"]),
        ("su asignatura favorita", ["Lenguaje", "Matemática", "Historia", "Ciencias", "Artes"]),
    ])
    total = rng.choice([40, 50, 60, 80])
    cortes = sorted(rng.sample(range(4, total - 3), 4))
    cantidades = [cortes[0], cortes[1] - cortes[0], cortes[2] - cortes[1], cortes[3] - cortes[2], total - cortes[3]]
    if min(cantidades) < 3 or len(set(cantidades)) < 5:
        raise Descartar
    i, j = rng.sample(range(5), 2)
    a, b = cantidades[i], cantidades[j]
    correcto = Fraction(a + b, total)
    enunciado = (f"En la tabla de la figura se presentan los resultados de una encuesta realizada a {total} personas sobre {tema}; cada "
                 f"persona eligió una sola opción. Si se elige al azar a una de estas personas, ¿cuál es la probabilidad de que haya "
                 f"elegido {categorias[i]} o {categorias[j]}?")
    pasos = (f"Los casos favorables son ${a} + {b} = {a + b}$ de un total de {total}: "
             f"$P = {figuras_fraccion(a + b, total)}$.")
    candidatos = [
        (Fraction(a + b, total - a - b), "compara con las personas que eligieron otras opciones en vez de con el total"),
        (Fraction(2, 5), "cuenta opciones (2 de 5) en vez de personas"),
        (Fraction(a, total) * Fraction(b, total), "multiplica las dos probabilidades en vez de sumarlas"),
        (Fraction(a, total), f"considera solo a quienes eligieron {categorias[i]}"),
    ]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: v * sum(cantidades) == cantidades[i] + cantidades[j], "media",
                     figura=figuras.tabla(["Opción", "Personas"], [[c, n] for c, n in zip(categorias, cantidades)]))


def figuras_fraccion(num, den) -> str:
    cruda = f"\\frac{{{num}}}{{{den}}}"
    final = frac(Fraction(num, den))
    return cruda if final == cruda else f"{cruda} = {final}"


@plantilla(EJE)
def probabilidad_en_tabla_de_doble_entrada(rng):
    areas = rng.choice([["Científica", "Humanista", "Matemática", "Artística"], ["Fútbol", "Básquetbol", "Natación", "Atletismo"],
                        ["Guitarra", "Piano", "Batería", "Violín"]])
    hombres = [rng.randrange(3, 13) for _ in areas]
    mujeres = [rng.randrange(3, 13) for _ in areas]
    total, total_m = sum(hombres) + sum(mujeres), sum(mujeres)
    i = rng.randrange(4)
    fila = hombres[i] + mujeres[i]
    conjunta = rng.random() < 0.5
    base = (f"En la tabla de la figura se presentan los resultados de una encuesta sobre la preferencia de un grupo de estudiantes; "
            f"cada estudiante eligió una sola opción. ")
    if conjunta:
        correcto = Fraction(mujeres[i], total)
        enunciado = base + f"Si se selecciona al azar a una persona del grupo, ¿cuál es la probabilidad de que sea mujer y prefiera {areas[i]}?"
        pasos = (f"El grupo completo tiene {total} estudiantes y {mujeres[i]} de ellos son mujeres que prefieren {areas[i]}: "
                 f"$P = {figuras_fraccion(mujeres[i], total)}$.")
        candidatos = [
            (Fraction(mujeres[i], total_m), "divide por el total de mujeres, pero la persona se elige entre todo el grupo"),
            (Fraction(mujeres[i], fila), f"divide por el total de quienes prefieren {areas[i]}"),
            (Fraction(total_m, total), "calcula solo la probabilidad de que sea mujer"),
            (Fraction(fila, total), f"calcula solo la probabilidad de que prefiera {areas[i]}"),
        ]
        dificultad = "media"
    else:
        correcto = Fraction(mujeres[i], total_m)
        enunciado = base + f"Si se selecciona al azar a una de las mujeres del grupo, ¿cuál es la probabilidad de que prefiera {areas[i]}?"
        pasos = (f"Como se elige entre las mujeres, el total de casos posibles es {total_m}. De ellas, {mujeres[i]} prefieren {areas[i]}: "
                 f"$P = {figuras_fraccion(mujeres[i], total_m)}$.")
        candidatos = [
            (Fraction(mujeres[i], total), "divide por el total del grupo, pero la persona se elige solo entre las mujeres"),
            (Fraction(mujeres[i], fila), f"divide por el total de quienes prefieren {areas[i]}"),
            (Fraction(fila, total), f"calcula la probabilidad de que cualquier estudiante prefiera {areas[i]}"),
            (Fraction(total_m, total), "calcula la probabilidad de elegir una mujer en todo el grupo"),
        ]
        dificultad = "alta"
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    personas = [(a, "H") for a, n in zip(areas, hombres) for _ in range(n)] + [(a, "M") for a, n in zip(areas, mujeres) for _ in range(n)]
    universo = personas if conjunta else [p for p in personas if p[1] == "M"]
    real = Fraction(sum(1 for p in universo if p == (areas[i], "M")), len(universo))
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == real, dificultad,
                     figura=figuras.tabla(["Preferencia", "Hombre", "Mujer"], [[a, h, m_] for a, h, m_ in zip(areas, hombres, mujeres)]))


def _expresion_promedio(rng, valores, letras, enunciado, textos, figura=None):
    def cociente(num, den):
        return f"$\\frac{{{num}}}{{{den}}}$"

    suma_letras = " + ".join(letras)
    ponderada = " + ".join(f"{t} \\cdot {l}" for t, l in zip(textos, letras))
    suma_valores = " + ".join(textos)
    correcta = op("ponderada/total", None, cociente(ponderada, suma_letras))
    distractores = [
        op("ponderada/3", "divide por la cantidad de valores distintos y no por el total de datos", cociente(ponderada, len(valores))),
        op("valores/total", "suma los valores sin multiplicarlos por sus frecuencias", cociente(suma_valores, suma_letras)),
        op("total/3", "promedia las frecuencias en vez de los datos", cociente(suma_letras, len(valores))),
    ]
    pasos = (f"El promedio es la suma de todos los datos dividida por la cantidad de datos. Cada valor se repite tantas veces como indica su "
             f"frecuencia, así que la suma es ${ponderada}$ y la cantidad de datos es ${suma_letras}$.")

    def comprobar(clave):
        for frecuencias in [(2, 3, 5), (1, 4, 7), (6, 1, 2)]:
            datos = [v for v, f in zip(valores, frecuencias) for _ in range(f)]
            calculado = {
                "ponderada/total": Fraction(sum(v * f for v, f in zip(valores, frecuencias)), sum(frecuencias)),
                "ponderada/3": Fraction(sum(v * f for v, f in zip(valores, frecuencias)), len(valores)),
                "valores/total": Fraction(sum(valores), sum(frecuencias)),
                "total/3": Fraction(sum(frecuencias), len(valores)),
            }[clave]
            if calculado != Fraction(sum(datos), len(datos)):
                return False
        return True

    return Propuesta(enunciado, correcta, distractores, pasos, comprobar, "media", figura=figura)


@plantilla(EJE)
def promedio_de_una_tabla_como_expresion(rng):
    inicio = rng.choice([0, 1, 2, 5, 10])
    salto = rng.choice([1, 2, 5])
    valores = [inicio + k * salto for k in range(3)]
    letras = rng.choice([["P", "Q", "R"], ["a", "b", "c"], ["m", "n", "p"]])
    enunciado = ("Considera la tabla de la figura, en la que las frecuencias se representan con letras. ¿Cuál de las siguientes "
                 "expresiones permite determinar el promedio de los valores?")
    return _expresion_promedio(rng, valores, letras, enunciado, [str(v) for v in valores],
                               figura=figuras.tabla(["Valor", "Frecuencia"], [[v, l] for v, l in zip(valores, letras)]))


@plantilla(EJE)
def sueldo_promedio_como_expresion(rng):
    sueldos = sorted(rng.sample(range(500, 1601, 100), 3))
    letras = ["n", "m", "w"]
    valores = [s * 1000 for s in sueldos]
    enunciado = (f"En una empresa hay tres tipos de sueldo según el puesto de trabajo: $n$ personas ganan {pesos(valores[0])}, $m$ personas "
                 f"ganan {pesos(valores[1])} y $w$ personas ganan {pesos(valores[2])}. ¿Cuál de las siguientes expresiones representa el "
                 f"sueldo promedio de las personas de la empresa, en pesos?")
    return _expresion_promedio(rng, valores, letras, enunciado, [miles(v) for v in valores])


@plantilla(EJE)
def crecimiento_promedio_por_semana(rng):
    semanas = rng.choice([4, 5])
    inicial = rng.randrange(2, 9)
    alturas = [inicial]
    for _ in range(semanas):
        alturas.append(alturas[-1] + rng.randrange(1, 6))
    final = alturas[-1]
    correcto = Fraction(final - inicial, semanas)
    planta = rng.choice(["un brote de poroto", "una planta de tomate", "un girasol"])
    medidas = ", ".join(f"{h} cm" for h in alturas[1:-1]) + f" y {final} cm"
    enunciado = (f"Se plantó {planta} de {inicial} cm de altura y se midió su altura al final de cada una de las siguientes {semanas} "
                 f"semanas, obteniendo {medidas}. ¿Cuántos centímetros creció, en promedio, por semana?")
    pasos = (f"En {semanas} semanas creció ${final} - {inicial} = {final - inicial}$ cm. El crecimiento promedio por semana es "
             f"${final - inicial} : {semanas} = {tex(correcto)}$ cm.")

    def cm(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ cm")

    candidatos = [
        (Fraction(final, semanas), "divide la altura final sin descontar la altura inicial"),
        (Fraction(sum(alturas[1:]), semanas), "promedia las alturas medidas en vez del crecimiento"),
        (Fraction(final - inicial), "entrega el crecimiento total y no el promedio por semana"),
        (Fraction(final - inicial, semanas + 1), f"divide por {semanas + 1}, contando también la medición inicial"),
    ]
    distractores = [cm(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    crecimientos = [b - a for a, b in zip(alturas, alturas[1:])]
    return Propuesta(enunciado, cm(correcto), distractores, pasos,
                     lambda v: v == Fraction(sum(crecimientos), len(crecimientos)), "media")


@plantilla(EJE)
def pago_mas_frecuente_desde_un_grafico(rng):
    horas = [1, 2, 3, 4, 5]
    frecuencias = [rng.randrange(5, 46) for _ in horas]
    if len(set(frecuencias)) < 5:
        raise Descartar
    pago = rng.randrange(8, 21) * 1000
    moda = horas[frecuencias.index(max(frecuencias))]
    menos = horas[frecuencias.index(min(frecuencias))]
    correcto = moda * pago
    enunciado = (f"En el gráfico de la figura se representa la distribución de la cantidad de horas extras realizadas por los trabajadores "
                 f"de una empresa durante un mes. Por cada hora extra se pagan {pesos(pago)}. ¿Cuál fue el pago por horas extras más "
                 f"frecuente entre los trabajadores?")
    pasos = (f"La barra más alta corresponde a {'1 hora extra' if moda == 1 else f'{moda} horas extras'}: es la cantidad más frecuente. "
             f"El pago más frecuente es ${moda} \\cdot {miles(pago)} = {miles(correcto)}$ pesos.")
    candidatos = [
        (max(frecuencias) * pago, "multiplica el pago por la frecuencia más alta en vez de por la cantidad de horas"),
        (max(horas) * pago, "usa la mayor cantidad de horas extras, no la más frecuente"),
        (menos * pago, "usa la cantidad de horas menos frecuente"),
        (pago, "entrega el pago de una sola hora"),
    ]
    distractores = [op(v, e, pesos(v)) for v, e in _tres_distintos(correcto, candidatos)]
    datos = [h for h, f in zip(horas, frecuencias) for _ in range(f)]
    return Propuesta(enunciado, op(correcto, texto=pesos(correcto)), distractores, pasos,
                     lambda v: v == statistics.mode(datos) * pago, "media",
                     figura=figuras.grafico_de_barras([str(h) for h in horas], frecuencias, "Horas extras", "Trabajadores"))


@plantilla(EJE)
def probabilidad_al_lanzar_monedas(rng):
    k = rng.choice([3, 4])
    resultados = list(itertools.product("CS", repeat=k))
    evento, condicion, explicacion = rng.choice([
        ("obtener al menos un sello", lambda r: "S" in r,
         f"El único resultado sin sellos es que salgan {k} caras, con probabilidad $\\frac{{1}}{{{2 ** k}}}$"),
        ("obtener exactamente una cara", lambda r: r.count("C") == 1,
         f"La única cara puede salir en cualquiera de las {k} monedas, lo que da {k} resultados favorables"),
        ("obtener más caras que sellos", lambda r: r.count("C") > r.count("S"),
         "Se cuentan los resultados en que las caras superan a los sellos"),
    ])
    favorables = sum(1 for r in resultados if condicion(r))
    correcto = Fraction(favorables, len(resultados))
    nombre = {3: "tres", 4: "cuatro"}[k]
    enunciado = f"Si se lanzan {nombre} monedas, ¿cuál es la probabilidad de {evento}?"
    pasos = (f"Hay $2^{{{k}}} = {2 ** k}$ resultados igual de probables. {explicacion}. Así, "
             f"$P = {figuras_fraccion(favorables, len(resultados))}$.")
    candidatos = [
        (1 - correcto, "calcula la probabilidad del suceso contrario"),
        (Fraction(1, 2), "responde como si se lanzara una sola moneda"),
        (Fraction(1, k), f"divide 1 por la cantidad de monedas"),
        (Fraction(favorables, 2 * k), f"usa {2 * k} resultados posibles en vez de {2 ** k}"),
        (Fraction(1, 2 ** k), "considera un solo resultado favorable"),
    ]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, [c for c in candidatos if 0 < c[0] < 1])]
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: v * len(resultados) == sum(1 for r in itertools.product("CS", repeat=k) if condicion(r)),
                     "media" if "al menos" in evento else "alta")


@plantilla(EJE)
def puntaje_en_un_juego_de_monedas(rng):
    a, b = rng.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3)])
    resultados = list(itertools.product("CS", repeat=3))

    def puntaje(r):
        return a * r.count("C") - b * r.count("S")

    favorables = sum(1 for r in resultados if puntaje(r) > 0)
    correcto = Fraction(favorables, 8)
    expresion = f"{'' if a == 1 else a}c - {'' if b == 1 else b}s"
    enunciado = (f"Un juego de azar consiste en lanzar tres monedas a la vez. El puntaje de un jugador está dado por la expresión "
                 f"${expresion}$, donde $c$ y $s$ son la cantidad de caras y de sellos obtenidos, respectivamente. ¿Cuál es la "
                 f"probabilidad de que un jugador obtenga un puntaje positivo en un lanzamiento?")
    detalle = ", ".join(f"con {c} {'cara' if c == 1 else 'caras'} el puntaje es ${a * c - b * (3 - c)}$" for c in range(4))
    casos = {0: 1, 1: 3, 2: 3, 3: 1}
    pasos = (f"Según la cantidad de caras: {detalle}. De los 8 resultados posibles hay 1 con 0 caras, 3 con 1 cara, 3 con 2 caras y 1 con "
             f"3 caras; los de puntaje positivo suman {favorables}. Así, $P = {figuras_fraccion(favorables, 8)}$.")
    positivos = [c for c in range(4) if a * c - b * (3 - c) > 0]
    candidatos = [
        (Fraction(len(positivos), 4), "cuenta las cantidades posibles de caras como si fueran igual de probables"),
        (1 - correcto, "calcula la probabilidad de que el puntaje no sea positivo"),
        (Fraction(sum(casos[c] for c in range(4) if c > 3 - c), 8), "considera positivo el puntaje solo cuando hay más caras que sellos, sin usar la expresión"),
        (Fraction(1, 2), "supone que el puntaje es positivo la mitad de las veces"),
        (Fraction(1, 8), "considera un solo resultado favorable"),
        (Fraction(3, 8), "considera solo una de las cantidades de caras favorables"),
    ]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, [c for c in candidatos if 0 < c[0] < 1])]
    if not 0 < correcto < 1:
        raise Descartar
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: v * 8 == sum(1 for r in itertools.product("CS", repeat=3) if puntaje(r) > 0), "alta")


@plantilla(EJE)
def probabilidad_con_un_dado_cargado(rng):
    decimas = [1] * 6
    for _ in range(4):
        decimas[rng.randrange(6)] += 1
    probabilidades = [Fraction(d, 10) for d in decimas]
    evento, caras = rng.choice([("un número par", [2, 4, 6]), ("un número impar", [1, 3, 5]),
                                ("un número mayor que 4", [5, 6]), ("un número menor que 3", [1, 2]),
                                ("un múltiplo de 3", [3, 6])])
    correcto = sum(probabilidades[c - 1] for c in caras)
    enunciado = (f"En la tabla de la figura se presenta la probabilidad de obtener cada cara de un dado cargado al lanzarlo. "
                 f"¿Cuál es la probabilidad de obtener {evento}?")
    pasos = (f"Se suman las probabilidades de las caras favorables ({', '.join(map(str, caras))}): "
             f"${' + '.join(tex(probabilidades[c - 1]) for c in caras)} = {tex(correcto)}$.")
    candidatos = [
        (Fraction(len(caras), 6), "responde como si el dado fuera común, con caras igual de probables"),
        (1 - correcto, "calcula la probabilidad del suceso contrario"),
        (probabilidades[caras[0] - 1], f"considera solo la cara {caras[0]}"),
        (Fraction(len(caras), 10), "cuenta las caras favorables y divide por 10"),
    ]
    elegidos = _tres_distintos(correcto, candidatos)

    def texto(v):
        return f"${tex(v)}$" if Fraction(v).denominator in (1, 2, 5, 10) else f"${frac(v)}$"

    distractores = [op(Fraction(v), e, texto(v)) for v, e in elegidos]
    return Propuesta(enunciado, op(Fraction(correcto), texto=texto(correcto)), distractores, pasos,
                     lambda v: v * 10 == sum(decimas[c - 1] for c in caras), "media",
                     figura=figuras.tabla(["Cara", "Probabilidad"], [[c, str(p.numerator / p.denominator).replace(".", ",")]
                                                                      for c, p in zip(range(1, 7), probabilidades)]))


@plantilla(EJE)
def mediana_desde_una_tabla_de_frecuencias(rng):
    columna, que = rng.choice([("Nota", "las notas de un curso en una evaluación"), ("Hermanos", "la cantidad de hermanos de un grupo de estudiantes"),
                               ("Libros", "la cantidad de libros leídos por los integrantes de un taller")])
    valores = [2, 3, 4, 5, 6, 7] if columna == "Nota" else [0, 1, 2, 3, 4]
    frecuencias = [rng.randrange(1, 10) for _ in valores]
    total = sum(frecuencias)
    if total % 2 == 0:
        raise Descartar
    datos = [x for x, f in zip(valores, frecuencias) for _ in range(f)]
    posicion = (total + 1) // 2
    mediana = datos[posicion - 1]
    moda_candidatas = [x for x, f in zip(valores, frecuencias) if f == max(frecuencias)]
    enunciado = f"En la tabla de la figura se presenta la distribución de {que}. ¿Cuál es la mediana de los datos?"
    acumuladas = list(itertools.accumulate(frecuencias))
    pasos = (f"Hay {total} datos, así que la mediana es el dato que ocupa la posición {posicion} al ordenarlos. Las frecuencias acumuladas "
             f"son {', '.join(map(str, acumuladas))}: la posición {posicion} cae en el valor {mediana}.")
    candidatos = [
        (valores[len(valores) // 2 - (1 if len(valores) % 2 == 0 else 0)], "toma el valor central de la columna sin considerar las frecuencias"),
        (moda_candidatas[0], "entrega la moda, que es el valor con mayor frecuencia"),
        (posicion, "entrega la posición del dato central y no su valor"),
        (valores[-1], "entrega el mayor valor de la tabla"),
        (valores[0], "entrega el menor valor de la tabla"),
    ]
    distractores = [op(v, e) for v, e in _tres_distintos(mediana, candidatos)]
    return Propuesta(enunciado, op(mediana), distractores, pasos, lambda v: v == statistics.median(datos), "alta",
                     figura=figuras.tabla([columna, "Frecuencia"], [[x, f] for x, f in zip(valores, frecuencias)]))


@plantilla(EJE)
def lectura_de_un_diagrama_de_cajon(rng):
    minimo = rng.randrange(5, 31, 5)
    q1 = minimo + rng.randrange(5, 16)
    mediana = q1 + rng.randrange(3, 13)
    q3 = mediana + rng.randrange(5, 21)
    maximo = q3 + rng.randrange(8, 31)
    que, titulo, personas, pregunta = rng.choice([
        ("los tiempos que un grupo de personas logró mantenerse en una postura de ejercicio", "Tiempo en segundos", "personas",
         "cuántas personas lograron mantenerse al menos {} segundos"),
        ("los puntajes obtenidos por un grupo de estudiantes en un ensayo", "Puntaje", "estudiantes",
         "cuántos estudiantes obtuvieron al menos {} puntos"),
        ("las edades de los socios de un club", "Edad en años", "socios", "cuántos socios tienen al menos {} años"),
    ])
    figura = figuras.diagrama_de_cajon(minimo, q1, mediana, q3, maximo, titulo)
    if rng.random() < 0.5:
        n = rng.choice([80, 100, 120, 200])
        enunciado = (f"En el diagrama de cajón de la figura se presenta la distribución de {que}. Si el grupo tiene {n} {personas}, "
                     f"¿aproximadamente {pregunta.format(q3)}?")
        correcto = n // 4
        pasos = (f"El valor {q3} corresponde al tercer cuartil: el 75 % de los datos está por debajo y el 25 % es igual o mayor. "
                 f"El 25 % de {n} es {correcto}.")
        candidatos = [
            (3 * n // 4, "calcula el 75 %, que corresponde a los datos menores que el tercer cuartil"),
            (n // 2, "usa el 50 %, que corresponde a la mediana"),
            (q3, "entrega el valor del cuartil en vez de la cantidad de personas"),
            (maximo - q3, "resta valores del diagrama en vez de usar porcentajes"),
        ]
        distractores = [op(v, e) for v, e in _tres_distintos(correcto, candidatos)]
        return Propuesta(enunciado, op(correcto), distractores, pasos, lambda v: v * 4 == n, "alta", figura=figura)
    enunciado = f"En el diagrama de cajón de la figura se presenta la distribución de {que}. ¿Cuál es el rango intercuartil de los datos?"
    correcto = q3 - q1
    pasos = (f"El rango intercuartil es la diferencia entre el tercer cuartil y el primero, es decir, el largo de la caja: "
             f"${q3} - {q1} = {correcto}$.")
    candidatos = [
        (maximo - minimo, "calcula el rango (máximo menos mínimo)"),
        (mediana, "entrega la mediana"),
        (q3 - mediana, "resta la mediana al tercer cuartil"),
        (mediana - q1, "resta el primer cuartil a la mediana"),
    ]
    distractores = [op(v, e) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto), distractores, pasos, lambda v: v + q1 == q3, "media", figura=figura)


@plantilla(EJE)
def caja_con_probabilidad_en_un_rango(rng):
    alto = rng.random() < 0.5
    t1, t2, t3, t4 = rng.randrange(4, 9), 2 * rng.randrange(2, 5), rng.randrange(5, 11), rng.randrange(5, 11)
    if alto:
        g3 = rng.randrange(1, (t3 + 1) // 2)
        g4 = rng.randrange(t4 // 2 + 1, t4)
        if 2 * g3 >= t3 or 2 * g4 <= t4:
            raise Descartar
        cajas = [((t1, 0), "todas las bolitas son grises: la probabilidad es 1, que no es menor que 1"),
                 ((t2 // 2, t2 // 2), "la mitad de las bolitas son grises: la probabilidad es exactamente 0,5"),
                 ((g3, t3 - g3), "menos de la mitad de las bolitas son grises: la probabilidad es menor que 0,5"),
                 ((g4, t4 - g4), None)]
        condicion = "mayor que 0,5 y menor que 1"
        cumple = lambda p: Fraction(1, 2) < p < 1
    else:
        g3 = rng.randrange(t3 // 2 + 1, t3 + 1)
        g4 = rng.randrange(1, (t4 + 1) // 2)
        if 2 * g3 <= t3 or 2 * g4 >= t4:
            raise Descartar
        cajas = [((0, t1), "no hay bolitas grises: la probabilidad es 0, que no es mayor que 0"),
                 ((t2 // 2, t2 // 2), "la mitad de las bolitas son grises: la probabilidad es exactamente 0,5"),
                 ((g3, t3 - g3), "más de la mitad de las bolitas son grises: la probabilidad es mayor que 0,5"),
                 ((g4, t4 - g4), None)]
        condicion = "mayor que 0 y menor que 0,5"
        cumple = lambda p: 0 < p < Fraction(1, 2)
    rng.shuffle(cajas)
    correcta = next(i for i, (_, error) in enumerate(cajas, 1) if error is None)
    grises, blancas = cajas[correcta - 1][0]
    enunciado = (f"En la figura se muestran cuatro cajas con bolitas grises y blancas, todas del mismo tamaño. ¿En cuál de las cajas, al "
                 f"extraer al azar una bolita, la probabilidad de que sea gris es {condicion}?")
    pasos = (f"En la Caja {correcta} hay {grises} bolitas grises de un total de {grises + blancas}: la probabilidad es "
             f"$\\frac{{{grises}}}{{{grises + blancas}}}$, que es {condicion}.")
    opciones = {i: op(i, None if i == correcta else f"en la Caja {i} {cajas[i - 1][1]}", f"En la Caja {i}") for i in range(1, 5)}
    return Propuesta(enunciado, opciones[correcta], [opciones[i] for i in range(1, 5) if i != correcta], pasos,
                     lambda v: [i for i, ((g, b), _) in enumerate(cajas, 1) if cumple(Fraction(g, g + b))] == [v],
                     "media", orden_fijo=True, figura=figuras.cajas_con_bolitas([c for c, _ in cajas]))

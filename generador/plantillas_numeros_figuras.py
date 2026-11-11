"""Plantillas de números de M1 con figura (recta numérica, rectángulo sombreado, tablas y gráficos de barras).

Tipos tomados de las PAES M1 de admisión 2023 a 2026, con contextos y números propios.
"""
from __future__ import annotations

from fractions import Fraction

import figuras
from nucleo import Descartar, Propuesta, frac, miles, op, opf, pesos, plantilla, tex

NUM = "numeros"


def _tres_distintos(correcto, candidatos):
    elegidos, vistos = [], {correcto}
    for valor, error in candidatos:
        if valor not in vistos:
            vistos.add(valor)
            elegidos.append((valor, error))
        if len(elegidos) == 3:
            return elegidos
    raise Descartar


@plantilla(NUM)
def numero_que_representa_un_punto_en_la_recta(rng):
    d = rng.choice([3, 4, 5, 6, 8])
    inicio = rng.choice([0, 0, -1, -2, -3])
    fin = inicio + 3
    a = rng.randrange(1, 3 * d)
    if a % d == 0:
        raise Descartar
    x = inicio + Fraction(a, d)
    enunciado = (f"En la recta numérica de la figura, cada unidad está dividida en partes iguales. ¿Qué número representa el punto $P$?")
    pasos = (f"Entre dos enteros consecutivos hay {d} espacios iguales, así que cada uno mide $\\frac{{1}}{{{d}}}$. El punto $P$ está "
             f"{a} espacios a la derecha de ${inicio}$: ${inicio} + \\frac{{{a}}}{{{d}}} = {frac(x)}$.")
    candidatos = [(inicio + Fraction(a, d + 1), f"cuenta las {d + 1} marcas de cada unidad en vez de los {d} espacios"),
                  (inicio + Fraction(a + 1, d), "cuenta también la marca del punto de partida"),
                  (inicio + Fraction(a, 10), "lee cada marca como una décima"),
                  (-x if x != 0 else x + 1, "se equivoca en el signo"),
                  (inicio + Fraction(a - 1, d), "deja de contar el último espacio")]
    distractores = [opf(v, e) for v, e in _tres_distintos(x, candidatos)]
    figura = figuras.recta_numerica(inicio, fin, d, [(float(x), "P")])
    return Propuesta(enunciado, opf(x), distractores, pasos, lambda v: (v - inicio) * d == a, "baja", figura=figura)


@plantilla(NUM)
def parte_sombreada_de_un_rectangulo(rng):
    columnas, filas = rng.choice([(4, 2), (5, 2), (5, 4), (4, 5), (6, 2), (6, 3), (4, 3), (5, 3), (8, 2)])
    n = columnas * filas
    k = rng.randrange(1, n)
    celdas = [(c, f) for c in range(columnas) for f in range(filas)]
    sombreadas = set(rng.sample(celdas, k))
    figura = figuras.rectangulo_sombreado(columnas, filas, sombreadas)
    if 100 % n == 0 and rng.random() < 0.6:
        correcto = Fraction(100 * k, n)
        enunciado = "El rectángulo de la figura está dividido en partes iguales. ¿Qué porcentaje del rectángulo está sombreado?"
        pasos = f"Hay {k} de {n} partes sombreadas: $\\frac{{{k}}}{{{n}}} \\cdot 100\\,\\% = {tex(correcto)}\\,\\%$."
        candidatos = [(Fraction(k), "responde la cantidad de partes sombreadas como porcentaje"),
                      (Fraction(100 * (n - k), n), "calcula el porcentaje que no está sombreado"),
                      (Fraction(100 * k, n - k), "divide las partes sombreadas por las no sombreadas"),
                      (Fraction(100 * k, n + 1), "cuenta una parte de más en el total")]
        texto = lambda v: f"${tex(v)}\\,\\%$"
        distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, candidatos)]
        return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos,
                         lambda v: v * n == 100 * len(sombreadas), "baja", figura=figura)
    pide_blanco = rng.random() < 0.4
    objetivo = n - k if pide_blanco else k
    correcto = Fraction(objetivo, n)
    parte = "no está sombreada" if pide_blanco else "está sombreada"
    enunciado = f"El rectángulo de la figura está dividido en partes iguales. ¿Qué fracción del rectángulo {parte}?"
    pasos = f"Hay {objetivo} de {n} partes que cumplen lo pedido: $\\frac{{{objetivo}}}{{{n}}}" + (
        f" = {frac(correcto)}$." if frac(correcto) != f"\\frac{{{objetivo}}}{{{n}}}" else "$.")
    otro = n - objetivo
    candidatos = [(Fraction(otro, n), "calcula la parte contraria a la pedida"),
                  (Fraction(objetivo, otro) if otro else Fraction(objetivo, n + 1), "divide por las partes de la otra clase en vez de por el total"),
                  (Fraction(objetivo, columnas) if objetivo < columnas else Fraction(objetivo, n + filas), "divide solo por la cantidad de columnas"),
                  (Fraction(objetivo, n + 1), "cuenta una parte de más en el total")]
    distractores = [opf(v, e) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if 0 < v])]
    real = Fraction(n - len(sombreadas) if pide_blanco else len(sombreadas), n)
    return Propuesta(enunciado, opf(correcto), distractores, pasos, lambda v: v == real, "baja", figura=figura)


_PRODUCTOS = [("Pan", 1900, 2600), ("Queso", 9000, 14000), ("Jamón", 8000, 13000), ("Manzanas", 1200, 1990), ("Palta", 3500, 6000),
              ("Tomates", 1000, 2200), ("Carne molida", 6500, 9500), ("Nueces", 9000, 16000), ("Arroz", 1100, 1800)]


@plantilla(NUM)
def compra_desde_una_tabla_de_precios(rng):
    productos = rng.sample(_PRODUCTOS, 3)
    precios = [rng.randrange(lo // 100, hi // 100 + 1) * 100 for _, lo, hi in productos]
    cantidades = [rng.choice([250, 500, 750, 1000, 1500, 2000]) for _ in productos]
    compra = list(range(3)) if rng.random() < 0.5 else rng.sample(range(3), 2)
    compra.sort()
    total = sum(Fraction(precios[i] * cantidades[i], 1000) for i in compra)
    if total.denominator != 1:
        raise Descartar

    def cantidad(g):
        return f"{tex(Fraction(g, 1000)).replace('{,}', ',')} kg" if g >= 1000 else f"{g} g"

    lista = [f"{cantidad(cantidades[i])} de {productos[i][0].lower()}" for i in compra]
    texto_lista = ", ".join(lista[:-1]) + f" y {lista[-1]}"
    enunciado = f"En la tabla de la figura se muestran los precios de algunos productos por kilogramo. ¿Cuánto se paga por {texto_lista}?"
    pasos = ("Se multiplica el precio por kilogramo por la cantidad en kilogramos: "
             + " + ".join(f"${miles(precios[i])} \\cdot {tex(Fraction(cantidades[i], 1000))}$" for i in compra)
             + f", que suma {pesos(int(total))}.")
    gramos_mal = next((i for i in compra if cantidades[i] < 1000), None)
    candidatos = [(sum(Fraction(precios[i]) for i in compra), "suma los precios por kilogramo sin considerar las cantidades"),
                  (total - Fraction(precios[compra[-1]] * cantidades[compra[-1]], 1000), "olvida uno de los productos"),
                  (total + Fraction(precios[gramos_mal] * cantidades[gramos_mal], 1000) if gramos_mal is not None else total * 2,
                   "duplica el precio de un producto vendido en gramos" if gramos_mal is not None else "duplica el total"),
                  (sum(Fraction(precios[i] * cantidades[i], 100) for i in compra), "convierte los gramos a kilogramos dividiendo por 100")]
    distractores = [op(v, e, pesos(int(v))) for v, e in _tres_distintos(total, [(v, e) for v, e in candidatos if v.denominator == 1])]
    figura = figuras.tabla(["Producto", "Precio por kg"], [[p[0], f"$ {miles(pr)}"] for p, pr in zip(productos, precios)])
    return Propuesta(enunciado, op(total, None, pesos(int(total))), distractores, pasos,
                     lambda v: v * 1000 == sum(precios[i] * cantidades[i] for i in compra), "media", figura=figura)


@plantilla(NUM)
def variacion_porcentual_desde_un_grafico(rng):
    meses = ["Mar", "Abr", "May", "Jun"]
    nombres = ["marzo", "abril", "mayo", "junio"]
    v1 = rng.choice([200, 240, 250, 300, 400, 500, 600, 800])
    pct = rng.choice([-40, -25, -20, -15, -10, 10, 15, 20, 25, 30, 40, 50])
    v2 = Fraction(v1 * (100 + pct), 100)
    if v2.denominator != 1:
        raise Descartar
    v2 = int(v2)
    otros = [rng.randrange(v1 // 20, v1 * 3 // 20 + 1) * 10 for _ in range(2)]
    i, j = 1, 3
    valores = [otros[0], v1, otros[1], v2]
    ordenados = sorted(valores)
    if any(b - a < max(valores) * 0.08 for a, b in zip(ordenados, ordenados[1:])):
        raise Descartar
    cosa = rng.choice([("el consumo eléctrico de una casa", "Consumo (kWh)"), ("la venta de entradas de un cine", "Entradas"),
                       ("el consumo de agua de un colegio", "Consumo (m³)")])
    enunciado = (f"El gráfico de la figura muestra {cosa[0]} en cuatro meses. ¿En qué porcentaje varió entre {nombres[i]} y "
                 f"{nombres[j]}?")
    pasos = (f"La variación es ${v2} - {v1} = {v2 - v1}$ respecto del valor inicial {v1}: $\\frac{{{v2 - v1}}}{{{v1}}} \\cdot 100\\,\\% = {pct}\\,\\%$, "
             f"es decir, {'aumentó' if pct > 0 else 'disminuyó'} un ${abs(pct)}\\,\\%$.")

    def texto(v):
        v = Fraction(v)
        return f"{'Aumentó' if v > 0 else 'Disminuyó'} un ${tex(abs(v))}\\,\\%$"

    candidatos = [(Fraction(100 * (v2 - v1), v2), "divide la variación por el valor final en vez del inicial"),
                  (Fraction(v2 - v1), "responde la diferencia como si fuera un porcentaje"),
                  (-Fraction(pct), "invierte el sentido de la variación"),
                  (Fraction(100 * v2, v1) - 100 + (10 if pct > 0 else -10), "se equivoca al restar el 100 %")]
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(Fraction(pct), [(v, e) for v, e in candidatos if v != 0])]
    figura = figuras.grafico_de_barras(meses[:4], valores, "Mes", cosa[1], alto=7.0)
    return Propuesta(enunciado, op(Fraction(pct), None, texto(pct)), distractores, pasos,
                     lambda v: v1 * (100 + v) == 100 * v2, "media", figura=figura)


_CIUDADES = ["Punta Arenas", "Coyhaique", "Puerto Natales", "Balmaceda", "Calama", "Putre", "Visviri", "Farellones"]


@plantilla(NUM)
def diferencia_de_temperaturas_desde_una_tabla(rng):
    ciudades = rng.sample(_CIUDADES, 4)
    temps = rng.sample(list(range(-12, 0)), 2) + rng.sample(list(range(1, 15)), 2)
    rng.shuffle(temps)
    alta, baja = max(temps), min(temps)
    correcto = alta - baja
    enunciado = ("En la tabla de la figura se muestran las temperaturas mínimas registradas un mismo día en cuatro localidades. ¿Cuál es la "
                 "diferencia entre la mayor y la menor de esas temperaturas?")
    pasos = f"La mayor es ${alta}$ °C y la menor ${baja}$ °C: ${alta} - ({baja}) = {alta} + {-baja} = {correcto}$ °C."
    segunda = sorted(temps)[1]
    orden = sorted(temps)
    candidatos = [(abs(alta + baja), "suma las temperaturas en vez de restarlas"),
                  (alta - orden[1], "usa la temperatura negativa más cercana a cero en vez de la menor"),
                  (orden[2] - baja, "usa la segunda temperatura más alta en vez de la mayor"),
                  (alta, "olvida la temperatura negativa")]
    texto = lambda v: f"${v}$ °C"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, [(v, e) for v, e in candidatos if v > 0])]
    figura = figuras.tabla(["Localidad", "Temperatura mínima"], [[c, f"{t} °C"] for c, t in zip(ciudades, temps)])
    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos,
                     lambda v: v == max(temps) - min(temps), "baja", figura=figura)

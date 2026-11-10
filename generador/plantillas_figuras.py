"""Plantillas modeladas en tipos de pregunta de las PAES M1 de admisión 2023 a 2026 (DEMRE).

Reúne los tipos que dependen de una figura (trapecio, cuadrícula, traslación de una figura, vector
dibujado, borde alrededor de un rectángulo, círculo inscrito, figura formada por cuadrados, cuerpos
compuestos, gráfico de barras) y los tipos sin figura que se repiten en las pruebas más recientes
(rectángulo de área conocida, deshacer transformaciones, volumen de agua, área de varios círculos,
perímetro de una malla). Se replica la habilidad evaluada con contextos y números propios.
"""
from __future__ import annotations

import math
from fractions import Fraction

import figuras
from nucleo import Descartar, Propuesta, m, op, plantilla, polinomio, tex

GEOMETRIA = "geometria"
ESTADISTICA = "probabilidad_estadistica"


def _punto(p) -> str:
    return f"$({p[0]},\\ {p[1]})$"


def _alt_punto(p, error=None):
    return op(tuple(p), error, _punto(p))


def _unidad(valor, unidad, error=None):
    return op(Fraction(valor), error, f"${tex(valor)}$ {unidad}")


def _con_pi(coef, unidad, error=None):
    coef = Fraction(coef)
    cuerpo = "" if coef == 1 else tex(coef)
    return op(coef, error, f"${cuerpo}\\pi$ {unidad}")


@plantilla(GEOMETRIA)
def altura_de_un_trapecio_rectangulo(rng):
    menor = rng.randrange(3, 13)
    mayor = menor + rng.randrange(2, 11)
    altura = rng.randrange(4, 21)
    area = Fraction((menor + mayor) * altura, 2)
    if area.denominator != 1:
        raise Descartar
    enunciado = (f"En la figura se representa un trapecio rectángulo cuyas bases miden {menor} cm y {mayor} cm. "
                 f"Si su área es {tex(area)} $\\text{{cm}}^{{2}}$, ¿cuál es la medida de su altura?")
    pasos = (f"El área del trapecio es $\\frac{{(\\text{{base mayor}} + \\text{{base menor}}) \\cdot h}}{{2}}$. Entonces "
             f"$\\frac{{({mayor} + {menor}) \\cdot h}}{{2}} = {tex(area)}$, es decir, ${menor + mayor}h = {tex(2 * area)}$ y $h = {altura}$ cm.")
    distractores = [
        _unidad(area / (menor + mayor), "cm", "divide el área por la suma de las bases y olvida el factor 2"),
        _unidad(area / mayor, "cm", "divide el área solo por la base mayor, como si fuera un rectángulo"),
        _unidad(2 * area / (mayor - menor), "cm", "resta las bases en vez de sumarlas"),
    ]
    return Propuesta(enunciado, _unidad(altura, "cm"), distractores, pasos,
                     lambda v: (menor + mayor) * v == 2 * area, "media",
                     figura=figuras.trapecio_rectangulo(menor, mayor, f"{menor} cm", f"{mayor} cm"))


@plantilla(GEOMETRIA)
def vector_entre_casillas_de_una_cuadricula(rng):
    lado = 7
    inicio = (rng.randrange(lado), rng.randrange(lado))
    destino = (rng.randrange(lado), rng.randrange(lado))
    unidades = rng.choice([2, 3, 5])
    casillas = (destino[0] - inicio[0], destino[1] - inicio[1])
    if casillas[0] == 0 or casillas[1] == 0 or abs(casillas[0]) == abs(casillas[1]):
        raise Descartar
    vector = (casillas[0] * unidades, casillas[1] * unidades)
    enunciado = (f"En la cuadrícula de la figura, cada casilla es un cuadrado de {unidades} unidades de lado. Una persona se ubica "
                 f"en el centro de la casilla marcada con P y un tesoro está en el centro de la casilla marcada con T. "
                 f"¿Cuál de los siguientes vectores lleva a la persona hasta el tesoro?")
    horizontal = "derecha" if casillas[0] > 0 else "izquierda"
    vertical = "arriba" if casillas[1] > 0 else "abajo"
    pasos = (f"Desde P hasta T hay {abs(casillas[0])} casillas hacia la {horizontal} y {abs(casillas[1])} hacia {vertical}. "
             f"Como cada casilla mide {unidades} unidades, el vector es {_punto(vector)}.")
    distractores = [
        _alt_punto(casillas, f"cuenta casillas y no las multiplica por las {unidades} unidades de cada una"),
        _alt_punto((-vector[0], -vector[1]), "entrega el vector que va del tesoro a la persona"),
        _alt_punto((vector[0], -vector[1]), "se equivoca en el signo de la componente vertical"),
    ]
    centro = lambda c: ((c[0] + 0.5) * unidades, (c[1] + 0.5) * unidades)
    return Propuesta(enunciado, _alt_punto(vector), distractores, pasos,
                     lambda v: (centro(inicio)[0] + v[0], centro(inicio)[1] + v[1]) == centro(destino), "media",
                     figura=figuras.cuadricula_con_objetos(lado, lado, inicio, destino, unidades))


@plantilla(GEOMETRIA)
def vector_de_traslacion_de_una_figura(rng):
    ancho, alto = rng.randrange(3, 7), rng.randrange(2, 6)
    x0, y0 = rng.randrange(1, 15), rng.randrange(1, 11)
    dx = rng.choice([n for n in range(-12, 13) if abs(n) >= 3])
    dy = rng.choice([n for n in range(-9, 10) if abs(n) >= 2])
    x1, y1 = x0 + dx, y0 + dy
    if min(x1, y1) < 1 or max(x0, x1) + ancho > 22 or max(y0, y1) + alto > 15:
        raise Descartar
    if abs(dx) < ancho + 1 and abs(dy) < alto + 1:
        raise Descartar

    def vertices(x, y):
        return [(x, y), (x + ancho, y), (x + ancho, y + alto), (x, y + alto)]

    enunciado = ("En el plano cartesiano de la figura se muestra una figura en su posición original y la misma figura después de "
                 "una traslación. ¿Cuáles son las coordenadas del vector de traslación?")
    pasos = (f"Se compara un vértice con su imagen. El vértice inferior izquierdo pasa de {_punto((x0, y0))} a {_punto((x1, y1))}: "
             f"la primera coordenada cambia en ${x1} - {x0} = {dx}$ y la segunda en ${y1} - {y0} = {dy}$. El vector es {_punto((dx, dy))}.")
    distractores = [
        _alt_punto((-dx, dy), "se equivoca en el signo de la componente horizontal"),
        _alt_punto((dx, -dy), "se equivoca en el signo de la componente vertical"),
        _alt_punto((-dx, -dy), "resta en el orden inverso: entrega el vector que devuelve la figura a su posición original"),
    ]
    return Propuesta(enunciado, _alt_punto((dx, dy)), distractores, pasos,
                     lambda v: [(x + v[0], y + v[1]) for x, y in vertices(x0, y0)] == vertices(x1, y1), "media",
                     figura=figuras.plano_cartesiano(
                         poligonos=[(vertices(x0, y0), "original"), (vertices(x1, y1), "trasladada")],
                         proyecciones=False, rango=(-1.5, 23.5, -1.5, 16.5)))


@plantilla(GEOMETRIA)
def componentes_de_un_vector_dibujado(rng):
    inicio = (rng.randrange(-6, 7), rng.randrange(-5, 6))
    dx = rng.choice([n for n in range(-7, 8) if n != 0])
    dy = rng.choice([n for n in range(-6, 7) if n != 0])
    fin = (inicio[0] + dx, inicio[1] + dy)
    if 0 in inicio or 0 in fin or abs(fin[0]) > 7 or abs(fin[1]) > 6 or fin == (dx, dy) or (dx, dy) == (inicio[0] + fin[0], inicio[1] + fin[1]):
        raise Descartar
    enunciado = ("En el plano cartesiano de la figura se representa el vector $\\vec{u}$. ¿Cuáles son las componentes de $\\vec{u}$?")
    pasos = (f"El vector parte en {_punto(inicio)} y termina en {_punto(fin)}. Sus componentes son la diferencia entre el punto final "
             f"y el inicial: $({fin[0]} - {tex(inicio[0]) if inicio[0] >= 0 else f'({inicio[0]})'},\\ "
             f"{fin[1]} - {tex(inicio[1]) if inicio[1] >= 0 else f'({inicio[1]})'}) = ({dx},\\ {dy})$.")
    distractores = [
        _alt_punto((-dx, -dy), "resta el punto final al inicial, en el orden inverso"),
        _alt_punto(fin, "entrega las coordenadas del punto final del vector"),
        _alt_punto((inicio[0] + fin[0], inicio[1] + fin[1]), "suma las coordenadas de los extremos en vez de restarlas"),
    ]
    return Propuesta(enunciado, _alt_punto((dx, dy)), distractores, pasos,
                     lambda v: (inicio[0] + v[0], inicio[1] + v[1]) == fin, "media",
                     figura=figuras.plano_cartesiano(vectores=[(inicio, fin, "u")]))


@plantilla(GEOMETRIA)
def perimetro_de_rectangulo_con_borde(rng):
    alto = rng.randrange(2, 9)
    ancho = alto + rng.randrange(2, 10)
    objeto = rng.choice(["una fotografía", "un espejo", "un cuadro", "una piscina"])
    unidad, borde = ("m", "un camino") if objeto == "una piscina" else ("cm", "un marco")
    enunciado = (f"En la figura, el rectángulo gris representa {objeto} cuyos lados miden {alto} {unidad} y {ancho} {unidad}. A su alrededor "
                 f"se construye {borde} de $x$ {unidad} de ancho, de modo que el contorno exterior también es un rectángulo. ¿Cuál de las "
                 f"siguientes expresiones representa el perímetro del rectángulo exterior, en {unidad}?")
    correcto = (8, 2 * (ancho + alto))

    def alt(par, error=None):
        return op(par, error, f"${polinomio(list(par))}$")

    pasos = (f"Cada lado crece $x$ por ambos extremos: los lados del rectángulo exterior miden ${ancho} + 2x$ y ${alto} + 2x$. "
             f"El perímetro es $2({ancho} + 2x) + 2({alto} + 2x) = {polinomio(list(correcto))}$.")
    distractores = [
        alt((4, 2 * (ancho + alto)), "agrega $x$ una sola vez a cada lado, pero el borde está en ambos extremos"),
        alt((4, ancho + alto), "suma un largo y un ancho, es decir, calcula solo la mitad del perímetro"),
        alt((8, ancho + alto), "considera los ocho tramos de $x$ pero suma un solo largo y un solo ancho"),
    ]
    return Propuesta(enunciado, alt(correcto), distractores, pasos,
                     lambda v: all(v[0] * x + v[1] == 2 * (ancho + 2 * x) + 2 * (alto + 2 * x) for x in (1, 2, 5)), "alta",
                     figura=figuras.rectangulo_con_borde(f"{ancho} {unidad}", f"{alto} {unidad}"))


@plantilla(GEOMETRIA)
def circulo_mas_grande_dentro_de_un_cuadrado(rng):
    lado = rng.randrange(10, 61, 2)
    objeto, contenido = rng.choice([("una caja de base cuadrada", "pizza redonda"), ("una bandeja cuadrada", "torta redonda"),
                                    ("un marco cuadrado", "espejo circular")])
    enunciado = (f"La figura representa {objeto} de {tex(lado * lado)} $\\text{{cm}}^{{2}}$ de área, vista desde arriba. "
                 f"¿Cuál es el perímetro de la {contenido} más grande que cabe en ella?" if contenido != "espejo circular" else
                 f"La figura representa {objeto} de {tex(lado * lado)} $\\text{{cm}}^{{2}}$ de área interior. "
                 f"¿Cuál es el perímetro del {contenido} más grande que cabe en él?")
    pasos = (f"El lado del cuadrado mide $\\sqrt{{{lado * lado}}} = {lado}$ cm y coincide con el diámetro del círculo más grande que cabe. "
             f"Su perímetro es $\\pi \\cdot d = {lado}\\pi$ cm.")
    distractores = [
        _con_pi(Fraction(lado, 2), "cm", "multiplica $\\pi$ por el radio en vez de por el diámetro"),
        _con_pi(2 * lado, "cm", "usa el lado del cuadrado como radio"),
        _con_pi(Fraction(lado * lado, 4), "cm", "calcula el área del círculo en vez de su perímetro"),
    ]
    return Propuesta(enunciado, _con_pi(lado, "cm"), distractores, pasos,
                     lambda v: v * v == lado * lado, "media", figura=figuras.circulo_inscrito_en_cuadrado())


def _crecer_figura(rng, cantidad):
    celdas = {(0, 0)}
    while len(celdas) < cantidad:
        c, f = rng.choice(sorted(celdas))
        dc, df = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        celdas.add((c + dc, f + df))
    minimo_c, minimo_f = min(c for c, _ in celdas), min(f for _, f in celdas)
    return {(c - minimo_c, f - minimo_f) for c, f in celdas}


@plantilla(GEOMETRIA)
def perimetro_de_figura_formada_por_cuadrados(rng):
    cantidad = rng.randrange(5, 11)
    celdas = _crecer_figura(rng, cantidad)
    if max(c for c, _ in celdas) > 4 or max(f for _, f in celdas) > 4:
        raise Descartar
    lado = rng.choice([2, 3, 4, 5, 6])
    bordes = sum((c + dc, f + df) not in celdas for c, f in celdas for dc, df in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    area = cantidad * lado * lado
    enunciado = (f"La figura está formada por {cantidad} cuadrados congruentes entre sí y su área total es {area} $\\text{{cm}}^{{2}}$. "
                 f"¿Cuál es el perímetro de la figura?")
    pasos = (f"Cada cuadrado tiene área ${area} : {cantidad} = {lado * lado}$ cm², así que su lado mide {lado} cm. El contorno de la figura "
             f"está formado por {bordes} lados de cuadrado: ${bordes} \\cdot {lado} = {bordes * lado}$ cm.")
    distractores = [
        _unidad(4 * cantidad * lado, "cm", "suma el perímetro de todos los cuadrados, incluyendo los lados interiores"),
        _unidad(bordes * lado * lado, "cm", "usa el área de cada cuadrado como si fuera la medida de su lado"),
        _unidad(bordes, "cm", "cuenta los lados del contorno pero no los multiplica por la medida del lado"),
    ]
    uniones = sum((c + 1, f) in celdas for c, f in celdas) + sum((c, f + 1) in celdas for c, f in celdas)
    return Propuesta(enunciado, _unidad(bordes * lado, "cm"), distractores, pasos,
                     lambda v: v == (4 * cantidad - 2 * uniones) * math.isqrt(area // cantidad), "alta",
                     figura=figuras.poliomino(celdas))


@plantilla(GEOMETRIA)
def volumen_de_dos_cilindros_unidos(rng):
    menor = rng.randrange(2, 7)
    mayor = menor + rng.randrange(2, 7)
    alto = rng.choice([5, 8, 10, 12, 15, 20])
    correcto = alto * (mayor * mayor + menor * menor)
    enunciado = (f"Una pieza metálica se fabrica uniendo dos cilindros rectos sólidos de la misma altura, {alto} cm, como se representa "
                 f"en la figura. El radio del cilindro inferior mide {mayor} cm y el del superior mide {menor} cm. "
                 f"¿Cuál es el volumen de la pieza?")
    pasos = (f"El volumen de cada cilindro es $\\pi r^{{2}} h$. Inferior: $\\pi \\cdot {mayor}^{{2}} \\cdot {alto} = {tex(mayor * mayor * alto)}\\pi$. "
             f"Superior: $\\pi \\cdot {menor}^{{2}} \\cdot {alto} = {tex(menor * menor * alto)}\\pi$. En total, ${tex(correcto)}\\pi$ cm³.")

    def cm3(coef, error=None):
        return op(coef, error, f"${tex(coef)}\\pi\\ \\text{{cm}}^{{3}}$")

    distractores = [
        cm3(alto * (mayor + menor) ** 2, "suma los radios antes de elevar al cuadrado"),
        cm3(alto * mayor * mayor, "calcula solo el volumen del cilindro inferior"),
        cm3(alto * (mayor + menor), "no eleva los radios al cuadrado"),
    ]
    return Propuesta(enunciado, cm3(correcto), distractores, pasos,
                     lambda v: v == sum(r * r * alto for r in (mayor, menor)), "media",
                     figura=figuras.cilindros_apilados(f"{mayor} cm", f"{menor} cm", f"{alto} cm"))


@plantilla(GEOMETRIA)
def superficie_por_pintar_de_un_mueble(rng):
    frente = rng.randrange(40, 121, 10)
    fondo = rng.randrange(30, 81, 10)
    alto = rng.randrange(50, 201, 10)
    if frente == fondo:
        raise Descartar
    lateral = 2 * alto * (frente + fondo)
    correcto = lateral + frente * fondo
    enunciado = (f"Un mueble tiene forma de prisma recto de base rectangular, con las medidas que se indican en la figura: {frente} cm de "
                 f"frente, {fondo} cm de fondo y {alto} cm de alto. Se pintará todo su exterior, excepto la base inferior. "
                 f"¿Cuál es la medida de la superficie por pintar?")
    pasos = (f"Las cuatro caras laterales suman $2 \\cdot {alto} \\cdot ({frente} + {fondo}) = {tex(lateral)}$ cm². La cara superior mide "
             f"${frente} \\cdot {fondo} = {tex(frente * fondo)}$ cm². En total, ${tex(correcto)}$ cm².")

    def cm2(v, error=None):
        return op(v, error, f"${tex(v)}\\ \\text{{cm}}^{{2}}$")

    distractores = [
        cm2(lateral + 2 * frente * fondo, "incluye también la base inferior"),
        cm2(lateral, "considera solo las caras laterales y olvida la cara superior"),
        cm2(alto * (frente + fondo) + frente * fondo, "cuenta solo dos de las cuatro caras laterales"),
    ]
    return Propuesta(enunciado, cm2(correcto), distractores, pasos,
                     lambda v: v == 2 * frente * alto + 2 * fondo * alto + frente * fondo, "media",
                     figura=figuras.caja(f"{frente} cm", f"{fondo} cm", f"{alto} cm", alto=alto / frente))


@plantilla(GEOMETRIA)
def rectangulo_de_area_conocida(rng):
    ancho = rng.randrange(4, 19)
    diferencia = rng.randrange(2, 10)
    largo = ancho + diferencia
    area = ancho * largo
    terreno = rng.choice(["Un terreno", "Una cancha", "Un huerto", "Un estacionamiento"])
    base = (f"{terreno} de forma rectangular tiene un área de {area} $\\text{{m}}^{{2}}$ y su largo mide {diferencia} m más que su ancho. ")
    planteo = (f"Si el ancho es $x$, el largo es $x + {diferencia}$ y $x(x + {diferencia}) = {area}$, es decir, "
               f"${polinomio([1, diferencia, -area])} = 0$, cuya solución positiva es $x = {ancho}$. El largo mide {largo} m.")
    if rng.random() < 0.5:
        enunciado = base + "¿Cuál es su perímetro?"
        correcto = 2 * (ancho + largo)
        pasos = planteo + f" El perímetro es $2 \\cdot ({ancho} + {largo}) = {correcto}$ m."
        distractores = [
            _unidad(ancho + largo, "m", "suma el ancho y el largo una sola vez"),
            _unidad(largo, "m", "entrega la medida del largo"),
            _unidad(4 * largo, "m", "calcula el perímetro como si fuera un cuadrado cuyo lado es el largo"),
        ]
        comprobar = lambda v: any(x * (x + diferencia) == area and v == 2 * (2 * x + diferencia) for x in range(1, 60))
    else:
        enunciado = base + "¿Cuánto mide su largo?"
        correcto = largo
        pasos = planteo
        distractores = [
            _unidad(ancho, "m", "entrega la medida del ancho"),
            _unidad(ancho + largo, "m", "entrega la suma del ancho y el largo"),
            _unidad(largo + diferencia, "m", f"suma {diferencia} dos veces"),
        ]
        comprobar = lambda v: v * (v - diferencia) == area and v > diferencia
    return Propuesta(enunciado, _unidad(correcto, "m"), distractores, pasos, comprobar, "alta",
                     figura=figuras.rectangulo(largo, ancho, f"x + {diferencia}", "x"))


@plantilla(GEOMETRIA)
def punto_original_tras_reflexion_y_traslacion(rng):
    p = (rng.choice([n for n in range(-8, 9) if n != 0]), rng.choice([n for n in range(-8, 9) if n != 0]))
    v = (rng.choice([n for n in range(-6, 7) if n != 0]), rng.choice([n for n in range(-6, 7) if n != 0]))
    q = (-p[0], -p[1])
    r = (q[0] + v[0], q[1] + v[1])
    if 0 in r:
        raise Descartar
    enunciado = (f"A un punto $P$ del plano cartesiano se le aplica una reflexión con respecto al origen y se obtiene el punto $Q$. "
                 f"Luego, $Q$ se traslada según el vector {_punto(v)} y se obtiene el punto $R$. Si $R$ tiene coordenadas {_punto(r)}, "
                 f"¿cuáles son las coordenadas de $P$?")
    pasos = (f"Se deshacen los pasos en orden inverso. Primero se resta el vector: $Q = ({r[0]} - {tex(v[0]) if v[0] >= 0 else f'({v[0]})'},\\ "
             f"{r[1]} - {tex(v[1]) if v[1] >= 0 else f'({v[1]})'}) = ({q[0]},\\ {q[1]})$. La reflexión con respecto al origen cambia "
             f"el signo de ambas coordenadas, así que $P = ({p[0]},\\ {p[1]})$.")
    distractores = [
        _alt_punto(q, "resta el vector pero no deshace la reflexión"),
        _alt_punto((-(r[0] + v[0]), -(r[1] + v[1])), "suma el vector en vez de restarlo al deshacer la traslación"),
        _alt_punto((-r[0], -r[1]), "deshace la reflexión pero no la traslación"),
    ]
    return Propuesta(enunciado, _alt_punto(p), distractores, pasos,
                     lambda x: (-x[0] + v[0], -x[1] + v[1]) == r, "alta")


@plantilla(GEOMETRIA)
def volumen_de_agua_en_una_piscina(rng):
    ancho, largo = rng.randrange(4, 11), rng.randrange(12, 26)
    profundidad = Fraction(rng.choice([15, 17, 18, 20, 22, 24]), 10)
    bajo_borde = rng.choice([10, 20, 30, 40])
    nivel = profundidad - Fraction(bajo_borde, 100)
    correcto = ancho * largo * nivel
    enunciado = (f"Una piscina con forma de paralelepípedo recto mide {ancho} m de ancho, {largo} m de largo y ${tex(profundidad)}$ m de "
                 f"profundidad. El agua llega hasta una marca ubicada {bajo_borde} cm bajo el borde superior. ¿Cuál es el volumen de agua "
                 f"que contiene la piscina?")
    pasos = (f"La altura del agua es ${tex(profundidad)} - {tex(Fraction(bajo_borde, 100))} = {tex(nivel)}$ m, porque {bajo_borde} cm "
             f"equivalen a ${tex(Fraction(bajo_borde, 100))}$ m. El volumen es ${ancho} \\cdot {largo} \\cdot {tex(nivel)} = {tex(correcto)}$ m³.")

    def m3(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}\\ \\text{{m}}^{{3}}$")

    distractores = [
        m3(ancho * largo * profundidad, "calcula el volumen total de la piscina, sin descontar la parte vacía"),
        m3(ancho * largo * (profundidad + Fraction(bajo_borde, 100)), "suma la distancia hasta el borde en vez de restarla"),
        m3(ancho * largo * Fraction(bajo_borde, 100), "calcula el volumen de la parte vacía"),
    ]
    return Propuesta(enunciado, m3(correcto), distractores, pasos,
                     lambda v: v + ancho * largo * Fraction(bajo_borde, 100) == ancho * largo * profundidad, "media")


@plantilla(GEOMETRIA)
def area_total_de_varios_circulos(rng):
    radios = sorted(rng.sample(range(1, 8), 3), reverse=True)
    correcto = sum(r * r for r in radios)
    perimetros = ", ".join(f"${2 * r}\\pi$ m" for r in radios[:-1]) + f" y ${2 * radios[-1]}\\pi$ m"
    enunciado = (f"En el patio de un colegio hay dibujados tres círculos de perímetros {perimetros}, que se pintarán para una actividad. "
                 f"¿Cuál es el área total que se debe pintar?")
    pasos = (f"El perímetro es $2\\pi r$, así que los radios miden {radios[0]} m, {radios[1]} m y {radios[2]} m. La suma de las áreas es "
             f"$\\pi({radios[0]}^{{2}} + {radios[1]}^{{2}} + {radios[2]}^{{2}}) = {correcto}\\pi$ m².")

    def m2(coef, error=None):
        return op(coef, error, f"${coef}\\pi\\ \\text{{m}}^{{2}}$")

    distractores = [
        m2(4 * correcto, "usa el diámetro como radio al dividir el perímetro solo por $\\pi$"),
        m2(sum(radios) ** 2, "suma los radios y eleva al cuadrado, como si fuera un solo círculo"),
        m2(sum(radios), "no eleva los radios al cuadrado"),
    ]
    return Propuesta(enunciado, m2(correcto), distractores, pasos,
                     lambda v: v == sum((Fraction(2 * r, 2)) ** 2 for r in radios), "alta")


@plantilla(GEOMETRIA)
def perimetro_de_una_malla_de_cuadrados(rng):
    lado = rng.choice([2, 3, 4, 5])
    alto = rng.randrange(20, 151, 10)
    largo = alto + rng.randrange(20, 151, 10)
    correcto = 2 * (alto + largo) * lado
    objeto = rng.choice(["Una malla", "Una reja", "Una red"])
    enunciado = (f"{objeto} rectangular está formada por cuadrados de {lado} cm de lado. Tiene {alto} cuadrados de alto y {largo} cuadrados "
                 f"de largo. ¿Cuál es su perímetro?")
    pasos = (f"El alto mide ${alto} \\cdot {lado} = {alto * lado}$ cm y el largo ${largo} \\cdot {lado} = {largo * lado}$ cm. "
             f"El perímetro es $2 \\cdot ({alto * lado} + {largo * lado}) = {tex(correcto)}$ cm.")
    distractores = [
        _unidad((alto + largo) * lado, "cm", "suma el alto y el largo una sola vez"),
        _unidad(2 * (alto + largo), "cm", "cuenta cuadrados del contorno y no multiplica por la medida del lado"),
        _unidad(alto * largo * lado * lado, "cm", "calcula el área de la malla en vez de su perímetro"),
    ]
    return Propuesta(enunciado, _unidad(correcto, "cm"), distractores, pasos,
                     lambda v: v == 2 * alto * lado + 2 * largo * lado, "media")


@plantilla(ESTADISTICA)
def media_desde_un_grafico_de_barras(rng):
    que, quienes, eje = rng.choice([
        ("horas extraordinarias trabajadas", "personas de una oficina", "Horas extraordinarias"),
        ("libros leídos en el semestre", "estudiantes de un taller", "Libros leídos"),
        ("goles anotados por partido", "partidos de un campeonato", "Goles en el partido"),
    ])
    valores = [1, 2, 3, 4]
    frecuencias = [rng.randrange(1, 10) for _ in valores]
    total = sum(frecuencias)
    if total not in (10, 20, 25) or len(set(frecuencias)) < 3:
        raise Descartar
    ponderada = sum(x * f for x, f in zip(valores, frecuencias))
    correcto = Fraction(ponderada, total)
    enunciado = (f"En el gráfico de la figura se muestra la distribución de {que} de {total} {quienes}. "
                 f"¿Cuál es el promedio de {que.split(' ')[0]} por {'partido' if 'partidos' in quienes else 'persona'}?")
    productos = " + ".join(f"{x} \\cdot {f}" for x, f in zip(valores, frecuencias))
    pasos = (f"Se multiplica cada valor por su frecuencia: ${productos} = {ponderada}$. "
             f"Al dividir por el total, ${ponderada} : {total} = {tex(correcto)}$.")
    distractores = [
        op(Fraction(sum(valores), len(valores)), "promedia los valores del eje horizontal sin considerar las frecuencias"),
        op(Fraction(total, len(valores)), "promedia las alturas de las barras"),
        op(Fraction(ponderada, len(valores)), "divide por la cantidad de barras y no por el total de datos"),
    ]
    datos = [x for x, f in zip(valores, frecuencias) for _ in range(f)]
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v * len(datos) == sum(datos), "media",
                     figura=figuras.grafico_de_barras([str(x) for x in valores], frecuencias, eje))


@plantilla(ESTADISTICA)
def porcentaje_desde_un_grafico_de_barras(rng):
    tema, categorias = rng.choice([
        ("su deporte preferido", ["Fútbol", "Básquetbol", "Vóleibol", "Tenis"]),
        ("la carrera que quieren estudiar", ["Ingeniería", "Medicina", "Derecho", "Diseño"]),
        ("su medio de transporte habitual", ["Bus", "Metro", "Bicicleta", "Auto"]),
    ])
    total = rng.choice([20, 25, 40, 50])
    multiplo = {20: 1, 25: 1, 40: 2, 50: 1}[total]
    frecuencias = [multiplo * rng.randrange(2, total // (2 * multiplo)) for _ in range(3)]
    frecuencias.append(total - sum(frecuencias))
    if len(set(frecuencias)) < 4 or min(frecuencias) < 2:
        raise Descartar
    rng.shuffle(frecuencias)
    i = rng.randrange(4)
    elegida, f = categorias[i], frecuencias[i]
    correcto = Fraction(100 * f, total)
    if correcto.denominator != 1:
        raise Descartar
    enunciado = (f"En el gráfico de la figura se presentan las respuestas de un grupo de personas a una encuesta sobre {tema}; cada persona "
                 f"eligió una sola opción. ¿Qué porcentaje de las personas encuestadas eligió {elegida}?")
    pasos = (f"El total de personas es ${' + '.join(map(str, frecuencias))} = {total}$. Eligieron {elegida} {f} personas: "
             f"$\\frac{{{f}}}{{{total}}} \\cdot 100 = {tex(correcto)}$ %.")

    def pct(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ %")

    distractores = [
        pct(f, "confunde la frecuencia con el porcentaje"),
        pct(100 - correcto, "calcula el porcentaje de personas que no eligió esa opción"),
        pct(25, "supone que las cuatro opciones tienen el mismo porcentaje"),
    ]
    return Propuesta(enunciado, pct(correcto), distractores, pasos,
                     lambda v: v * sum(frecuencias) == 100 * frecuencias[i], "media",
                     figura=figuras.grafico_de_barras(categorias, frecuencias, "Opción elegida", "Personas"))

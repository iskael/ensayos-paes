"""Plantillas de geometría modeladas en los tipos de pregunta de las PAES M1 oficiales.

Fuente de los tipos (no de los textos): PAES Regular e Invierno de Competencia Matemática 1,
admisión 2024, publicadas por el DEMRE. Cada plantilla reproduce la habilidad evaluada con
contextos y números propios; ninguna copia un ítem oficial. Solo incluye tipos que se pueden
resolver sin figura.
"""
from __future__ import annotations

import math
from fractions import Fraction

import figuras
from nucleo import Descartar, Propuesta, frac, op, plantilla, raiz_tex, tex

EJE = "geometria"

TERNAS = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15), (12, 16, 20)]


def _punto(p) -> str:
    return f"$({p[0]},\\ {p[1]})$"


def _alt_punto(p, error=None):
    return op(tuple(p), error, _punto(p))


def _complejo(p) -> complex:
    return complex(p[0], p[1])


def _de_complejo(z: complex):
    return (round(z.real), round(z.imag))


@plantilla(EJE)
def diagonal_de_un_cuadrado(rng):
    lado = rng.choice([n for n in range(3, 31) if math.isqrt(n) ** 2 != n])
    contexto, unidad = rng.choice([
        (f"Una caja de regalo tiene forma de cubo de arista {lado} cm. En su cara superior se pega una cinta recta "
         f"que va de un vértice al vértice opuesto de esa cara. ¿Cuál es el largo de la cinta?", "cm"),
        (f"Un patio cuadrado tiene lados de {lado} m. Se instala un cable recto que une dos esquinas opuestas del patio. "
         f"¿Cuál es el largo del cable?", "m"),
        (f"Una baldosa cuadrada tiene lados de {lado} cm y se corta en línea recta por una de sus diagonales. "
         f"¿Cuál es el largo del corte?", "cm"),
    ])

    def largo(cuadrado, error=None, texto=None):
        return op(cuadrado, error, f"${texto or raiz_tex(cuadrado)}$ {unidad}")

    pasos = (f"La diagonal de un cuadrado de lado ${lado}$ forma un triángulo rectángulo con dos lados: "
             f"$\\sqrt{{{lado}^{{2}} + {lado}^{{2}}}} = {lado}\\sqrt{{2}}$ {unidad}.")
    distractores = [
        largo(4 * lado * lado, "suma los dos lados en vez de aplicar el teorema de Pitágoras"),
        largo(4 * lado, "calcula el doble de la raíz del lado", f"2\\sqrt{{{lado}}}"),
        largo(lado ** 4, "calcula el área del cuadrado en vez de su diagonal"),
    ]
    return Propuesta(contexto, largo(2 * lado * lado, texto=f"{lado}\\sqrt{{2}}"), distractores, pasos,
                     lambda v: abs(math.sqrt(v) - math.hypot(lado, lado)) < 1e-9, "media",
                     figura=figuras.cuadrado_con_diagonal(f"{lado} {unidad}"))


@plantilla(EJE)
def radio_desde_razon_de_areas(rng):
    k = rng.choice([2, 3, 4])
    r = rng.choice([n for n in range(2, 13) if n != k and n != k * k])
    achica = rng.random() < 0.5
    parte = {2: "un cuarto", 3: "un noveno", 4: "un dieciseisavo"}[k]
    veces = {2: "cuatro veces", 3: "nueve veces", 4: "dieciséis veces"}[k]

    def cm(v, error=None):
        return op(Fraction(v), error, f"${frac(v)}$ cm")

    if achica:
        correcto = Fraction(r, k)
        enunciado = (f"Un círculo $P$ tiene radio {r} cm. Si el área de un círculo $Q$ es {parte} del área de $P$, "
                     f"¿cuál es el radio de $Q$?")
        pasos = (f"El área depende del cuadrado del radio. Si el área se reduce a {parte}, el radio se divide por "
                 f"$\\sqrt{{{k * k}}} = {k}$: ${r} : {k} = {frac(correcto)}$ cm.")
        distractores = [
            cm(Fraction(r, k * k), "aplica la razón entre las áreas directamente al radio"),
            cm(r * k, "multiplica el radio en vez de dividirlo"),
            cm(r * k * k, "multiplica el radio por la razón entre las áreas"),
        ]
        razon = Fraction(1, k * k)
    else:
        correcto = Fraction(r * k)
        enunciado = (f"Un círculo $P$ tiene radio {r} cm. Si el área de un círculo $Q$ es {veces} el área de $P$, "
                     f"¿cuál es el radio de $Q$?")
        pasos = (f"El área depende del cuadrado del radio. Si el área se multiplica por {k * k}, el radio se multiplica por "
                 f"$\\sqrt{{{k * k}}} = {k}$: ${r} \\cdot {k} = {r * k}$ cm.")
        distractores = [
            cm(r * k * k, "aplica la razón entre las áreas directamente al radio"),
            cm(Fraction(r, k), "divide el radio en vez de multiplicarlo"),
            cm(Fraction(r, k * k), "divide el radio por la razón entre las áreas"),
        ]
        razon = Fraction(k * k)
    return Propuesta(enunciado, cm(correcto), distractores, pasos,
                     lambda v: v > 0 and v * v == r * r * razon, "alta")


@plantilla(EJE)
def altura_de_cilindro_dada_la_capacidad(rng):
    r = rng.choice([2, 3, 4, 5, 6, 10])
    h = rng.choice([Fraction(5), Fraction(15, 2), Fraction(8), Fraction(10), Fraction(12), Fraction(25, 2), Fraction(15), Fraction(20), Fraction(25)])
    volumen = 3 * r * r * h
    if volumen.denominator != 1:
        raise Descartar
    objeto = rng.choice(["un vaso graduado", "un tarro", "un florero", "un envase"])
    enunciado = (f"Se quiere fabricar {objeto} con forma de cilindro recto, de {tex(volumen)} $\\text{{cm}}^{{3}}$ de capacidad y "
                 f"{r} cm de radio basal. Considerando $\\pi$ aproximado a 3, ¿cuál debe ser su altura?")
    pasos = (f"El volumen del cilindro es $\\pi r^{{2}} h$. Con $\\pi \\approx 3$: $3 \\cdot {r}^{{2}} \\cdot h = {tex(volumen)}$, "
             f"es decir, ${3 * r * r}h = {tex(volumen)}$, de donde $h = {tex(h)}$ cm.")

    def cm(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ cm")

    distractores = [
        cm(volumen / (3 * r), "no eleva el radio al cuadrado"),
        cm(volumen / (6 * r), "usa $2\\pi r$ (el perímetro de la base) en vez del área de la base"),
        cm(volumen / (r * r), "no considera $\\pi$ al despejar la altura"),
    ]
    return Propuesta(enunciado, cm(h), distractores, pasos, lambda v: 3 * r * r * v == volumen, "media",
                     figura=figuras.cilindro(f"{r} cm", "h", float(h) / r))


@plantilla(EJE)
def area_de_superficie_en_terminos_de_x(rng):
    a = rng.choice([2, 3, 4, 5])
    b = rng.choice([n for n in range(3, 11) if n != a])
    edificio = rng.random() < 0.5
    if edificio:
        enunciado = (f"Un edificio tiene forma de paralelepípedo recto de base cuadrada. Los lados de la base miden ${a}x$ metros "
                     f"y la altura mide ${b}x$ metros. ¿Cuál es el área que se debe pintar si se consideran solo las cuatro "
                     f"paredes laterales y el techo, en metros cuadrados?")
        cara = "el techo"
    else:
        enunciado = (f"Una caja sin tapa tiene forma de paralelepípedo recto de base cuadrada. Los lados de la base miden ${a}x$ cm "
                     f"y la altura mide ${b}x$ cm. ¿Cuál es el área total de cartón de la caja, considerando sus cuatro caras "
                     f"laterales y el fondo, en centímetros cuadrados?")
        cara = "el fondo"
    correcto = 4 * a * b + a * a

    def alt(coef, error=None):
        return op(coef, error, f"${coef}x^{{2}}$")

    pasos = (f"Cada cara lateral mide ${a}x \\cdot {b}x = {a * b}x^{{2}}$ y son cuatro: ${4 * a * b}x^{{2}}$. "
             f"{cara.capitalize()} mide ${a}x \\cdot {a}x = {a * a}x^{{2}}$. En total, ${correcto}x^{{2}}$.")
    distractores = [
        alt(4 * a * b + 2 * a * a, "cuenta las dos bases, aunque solo se pide una"),
        alt(4 * a * b, f"considera solo las caras laterales y olvida {cara}"),
        alt(a * a * b, "multiplica las tres medidas, como si calculara el volumen"),
    ]
    return Propuesta(enunciado, alt(correcto), distractores, pasos,
                     lambda v: v == sum([a * b] * 4) + a * a, "alta",
                     figura=figuras.caja(f"{a}x", f"{a}x", f"{b}x", alto=b / a, sin_tapa=not edificio))


@plantilla(EJE)
def suma_de_vectores_con_incognita(rng):
    conocidos = [(rng.randrange(-6, 7), rng.randrange(-6, 7)) for _ in range(3)]
    xs, ys = [v[0] for v in conocidos], [v[1] for v in conocidos]
    if not any(x < 0 for x in xs) or not any(y < 0 for y in ys) or 0 in xs + ys:
        raise Descartar
    a, b = rng.randrange(-5, 8), rng.randrange(-5, 8)
    total = (sum(xs) + a, sum(ys) + b)
    mal_a = total[0] - sum(abs(x) for x in xs)
    mal_b = total[1] - sum(abs(y) for y in ys)

    def vec(nombre, v):
        return f"$\\vec{{{nombre}}} = ({v[0]},\\ {v[1]})$"

    def alt(par, error=None):
        return op(par, error, f"${par[0]}$ y ${par[1]}$")

    enunciado = (f"Considera los vectores {vec('p', conocidos[0])}, {vec('q', conocidos[1])}, {vec('r', conocidos[2])} y "
                 f"$\\vec{{s}} = (a,\\ b)$. Si $\\vec{{p}} + \\vec{{q}} + \\vec{{r}} + \\vec{{s}} = ({total[0]},\\ {total[1]})$, "
                 f"¿cuáles son los valores de $a$ y $b$, respectivamente?")
    pasos = (f"Se suma componente a componente. Primera: ${' + '.join(tex(x) if x >= 0 else f'({x})' for x in xs)} + a = {total[0]}$, "
             f"de donde $a = {a}$. Segunda: ${' + '.join(tex(y) if y >= 0 else f'({y})' for y in ys)} + b = {total[1]}$, "
             f"de donde $b = {b}$.")
    distractores = [
        alt((a, mal_b), "en la segunda componente suma los valores sin respetar los signos negativos"),
        alt((mal_a, b), "en la primera componente suma los valores sin respetar los signos negativos"),
        alt((total[0] + sum(xs), total[1] + sum(ys)), "suma los vectores conocidos al resultado en vez de restarlos"),
    ]
    return Propuesta(enunciado, alt((a, b)), distractores, pasos,
                     lambda v: sum(_complejo(c) for c in conocidos) + _complejo(v) == _complejo(total), "media")


ROTAR = {"horario": lambda p: (p[1], -p[0]), "antihorario": lambda p: (-p[1], p[0])}
GIRO_COMPLEJO = {"horario": -1j, "antihorario": 1j}


@plantilla(EJE)
def imagen_por_rotacion_y_traslacion(rng):
    p = (rng.choice([n for n in range(-8, 9) if n != 0]), rng.choice([n for n in range(-8, 9) if n != 0]))
    sentido = rng.choice(["horario", "antihorario"])
    contrario = "antihorario" if sentido == "horario" else "horario"
    v = (rng.choice([n for n in range(-6, 7) if n != 0]), rng.choice([n for n in range(-6, 7) if n != 0]))
    rotado = ROTAR[sentido](p)
    correcto = (rotado[0] + v[0], rotado[1] + v[1])
    otro = ROTAR[contrario](p)
    trasladado = (p[0] + v[0], p[1] + v[1])
    enunciado = (f"Al punto {_punto(p)} se le aplica una rotación en $90^{{\\circ}}$ en sentido {sentido} con centro en el origen "
                 f"del plano cartesiano y, luego, al punto obtenido se le aplica una traslación según el vector {_punto(v)}. "
                 f"¿Cuáles son las coordenadas del punto final?")
    regla = "$(x,\\ y) \\rightarrow (y,\\ -x)$" if sentido == "horario" else "$(x,\\ y) \\rightarrow (-y,\\ x)$"
    pasos = (f"La rotación en $90^{{\\circ}}$ en sentido {sentido} con centro en el origen lleva {regla}, así que {_punto(p)} "
             f"pasa a {_punto(rotado)}. Al sumar el vector {_punto(v)} se obtiene {_punto(correcto)}.")
    distractores = [
        _alt_punto((otro[0] + v[0], otro[1] + v[1]), f"rota en sentido {contrario}"),
        _alt_punto(ROTAR[sentido](trasladado), "aplica primero la traslación y después la rotación"),
        _alt_punto(rotado, "aplica la rotación pero olvida la traslación"),
    ]
    real = _de_complejo(_complejo(p) * GIRO_COMPLEJO[sentido] + _complejo(v))
    return Propuesta(enunciado, _alt_punto(correcto), distractores, pasos, lambda x: tuple(x) == real, "media")


def _transformaciones(rng):
    vector = (rng.choice([n for n in range(-6, 7) if n != 0]), rng.choice([n for n in range(-6, 7) if n != 0]))
    return {
        "traslacion": (f"se traslada según el vector {_punto(vector)}",
                       lambda p: (p[0] + vector[0], p[1] + vector[1]),
                       lambda p: (p[0] - vector[0], p[1] - vector[1]),
                       lambda z: z + _complejo(vector),
                       "en una traslación se suman las componentes del vector a las coordenadas del punto"),
        "rotacion_horaria": ("se rota en $90^{\\circ}$ en sentido horario con centro en el origen",
                             ROTAR["horario"], ROTAR["antihorario"], lambda z: z * -1j,
                             "esa rotación lleva $(x,\\ y)$ a $(y,\\ -x)$"),
        "rotacion_antihoraria": ("se rota en $90^{\\circ}$ en sentido antihorario con centro en el origen",
                                 ROTAR["antihorario"], ROTAR["horario"], lambda z: z * 1j,
                                 "esa rotación lleva $(x,\\ y)$ a $(-y,\\ x)$"),
        "reflexion_y": ("se refleja con respecto al eje $Y$",
                        lambda p: (-p[0], p[1]), lambda p: (p[0], -p[1]), lambda z: complex(-z.real, z.imag),
                        "la reflexión respecto al eje $Y$ cambia el signo de la primera coordenada"),
        "reflexion_x": ("se refleja con respecto al eje $X$",
                        lambda p: (p[0], -p[1]), lambda p: (-p[0], p[1]), lambda z: complex(z.real, -z.imag),
                        "la reflexión respecto al eje $X$ cambia el signo de la segunda coordenada"),
    }


@plantilla(EJE)
def paso_erroneo_en_transformaciones_isometricas(rng):
    catalogo = _transformaciones(rng)
    nombres = rng.sample(list(catalogo), 4)
    inicio = (rng.choice([n for n in range(-7, 8) if n != 0]), rng.choice([n for n in range(-7, 8) if n != 0]))
    paso_malo = rng.randrange(1, 5)
    declarados, lineas, detalle = [inicio], [], {}
    for i, nombre in enumerate(nombres, 1):
        descripcion, aplicar, equivocar, _, regla = catalogo[nombre]
        previo = declarados[-1]
        real = aplicar(previo)
        dicho = equivocar(previo) if i == paso_malo else real
        if i == paso_malo and dicho == real:
            raise Descartar
        declarados.append(dicho)
        lineas.append(f"Paso {i}: el punto {_punto(previo)} {descripcion}, obteniendo el punto {_punto(dicho)}.")
        detalle[i] = (previo, real, dicho, regla)
    enunciado = (f"Una persona aplica cuatro transformaciones isométricas consecutivas al punto {_punto(inicio)} y comete un error "
                 f"en uno de los pasos. {' '.join(lineas)} ¿En cuál de los pasos se cometió el error?")
    previo, real, dicho, regla = detalle[paso_malo]
    pasos = (f"En el Paso {paso_malo}, {regla}: a partir de {_punto(previo)} se debía obtener {_punto(real)} y no {_punto(dicho)}. "
             f"Los demás pasos están bien aplicados sobre el punto del paso anterior.")
    opciones = {i: op(i, None if i == paso_malo else
                      f"el Paso {i} es correcto: de {_punto(detalle[i][0])} se obtiene {_punto(detalle[i][1])}",
                      f"En el Paso {i}") for i in range(1, 5)}

    def comprobar(v):
        malos = set()
        for i, nombre in enumerate(nombres, 1):
            if _de_complejo(catalogo[nombre][3](_complejo(declarados[i - 1]))) != declarados[i]:
                malos.add(i)
        return malos == {v}

    return Propuesta(enunciado, opciones[paso_malo], [opciones[i] for i in range(1, 5) if i != paso_malo], pasos,
                     comprobar, "alta", orden_fijo=True)


@plantilla(EJE)
def vector_de_traslacion_en_un_recorrido(rng):
    sentidos = {"este": (1, 0), "oeste": (-1, 0), "norte": (0, 1), "sur": (0, -1)}
    nombres = rng.sample(["Juan", "Diego", "Pedro", "Sofía", "Elena", "Tomás", "Paula"], 3)
    tramos = []
    for _ in range(2):
        horizontal, vertical = rng.choice(["este", "oeste"]), rng.choice(["norte", "sur"])
        tramos.append((rng.randrange(1, 7), horizontal, rng.randrange(1, 7), vertical))
    x = sum(n * sentidos[h][0] for n, h, _, _ in tramos)
    y = sum(n * sentidos[v][1] for _, _, n, v in tramos)
    if x == 0 or y == 0:
        raise Descartar

    def cuadras(n):
        return "una cuadra" if n == 1 else f"{n} cuadras"

    t1, t2 = tramos
    enunciado = (f"Para ir de su casa a la casa de {nombres[1]}, {nombres[0]} camina {cuadras(t1[0])} hacia el {t1[1]} y "
                 f"{cuadras(t1[2])} hacia el {t1[3]}. Desde ahí, para llegar a la casa de {nombres[2]}, camina {cuadras(t2[0])} hacia el "
                 f"{t2[1]} y {cuadras(t2[2])} hacia el {t2[3]}. Todas las cuadras miden lo mismo. Si el recorrido se grafica en un plano "
                 f"cartesiano con la casa de {nombres[0]} en el origen, el este en el sentido positivo del eje $X$ y el norte en el "
                 f"sentido positivo del eje $Y$, ¿cuál es el vector de traslación que lleva de la casa de {nombres[0]} a la de {nombres[2]}?")
    pasos = (f"Hacia el este se suma y hacia el oeste se resta en la primera componente, que resulta ${x}$. Hacia el norte se suma y "
             f"hacia el sur se resta en la segunda componente, que resulta ${y}$. El vector es {_punto((x, y))}.")
    distractores = [
        _alt_punto((-x, y), "invierte el signo de la componente horizontal (este–oeste)"),
        _alt_punto((x, -y), "invierte el signo de la componente vertical (norte–sur)"),
        _alt_punto((-x, -y), "invierte el signo de ambas componentes"),
    ]
    posicion = 0j
    for n, h, k, v in tramos:
        posicion += n * complex(*sentidos[h]) + k * complex(*sentidos[v])
    return Propuesta(enunciado, _alt_punto((x, y)), distractores, pasos,
                     lambda p: _complejo(p) == posicion, "media", figura=figuras.rosa_de_los_vientos())


def _con_pi_cm(coef, error=None):
    coef = Fraction(coef)
    return op(coef, error, f"${'' if coef == 1 else tex(coef)}\\pi$ cm")


@plantilla(EJE)
def perimetro_de_circulo_con_formula_dada(rng):
    a, b, c = rng.choice(TERNAS)
    if rng.random() < 0.5:
        a, b = b, a
    d = a + b - c
    enunciado = (f"El diámetro $d$ del círculo inscrito en un triángulo rectángulo se puede calcular con la fórmula $d = a + b - c$, "
                 f"donde $a$ y $b$ son las medidas de los catetos y $c$ es la medida de la hipotenusa. Si los catetos de un triángulo "
                 f"rectángulo miden {a} cm y {b} cm, ¿cuál es el perímetro del círculo inscrito en él?")
    pasos = (f"La hipotenusa mide $\\sqrt{{{a}^{{2}} + {b}^{{2}}}} = {c}$ cm. Entonces $d = {a} + {b} - {c} = {d}$ cm y el perímetro "
             f"del círculo es $\\pi \\cdot d = {d}\\pi$ cm.")
    distractores = [
        _con_pi_cm(2 * d, "usa el diámetro como si fuera el radio en $2\\pi r$"),
        _con_pi_cm(Fraction(d, 2), "multiplica $\\pi$ por el radio en vez de por el diámetro"),
        _con_pi_cm(a + b, "no resta la hipotenusa al aplicar la fórmula"),
    ]
    inradio = Fraction(a * b, a + b + c)
    return Propuesta(enunciado, _con_pi_cm(d), distractores, pasos,
                     lambda v: a * a + b * b == c * c and v == 2 * inradio, "alta")


@plantilla(EJE)
def area_de_cuadrado_con_esquinas_cubiertas(rng):
    p = rng.randrange(20, 81, 10)
    m_, n_ = rng.randrange(2, p // 2), rng.randrange(2, p // 2)
    if m_ == n_ or (m_ * n_) % 2:
        raise Descartar
    objeto, cubierta = rng.choice([("Un espejo cuadrado", "de madera"), ("Un vitral cuadrado", "de metal"),
                                   ("Una ventana cuadrada", "de madera")])
    visible = p * p - 2 * m_ * n_
    enunciado = (f"{objeto} tiene lados de {p} cm. En cada una de sus cuatro esquinas se sobrepone una pieza {cubierta} con forma de "
                 f"triángulo rectángulo de catetos {m_} cm y {n_} cm, con el ángulo recto en la esquina. ¿Cuál es el área del vidrio "
                 f"que queda a la vista?")
    pasos = (f"El área total es ${p}^{{2}} = {tex(p * p)}$ cm². Cada triángulo mide $\\frac{{{m_} \\cdot {n_}}}{{2}} = {m_ * n_ // 2}$ cm² "
             f"y son cuatro: ${2 * m_ * n_}$ cm². A la vista quedan ${tex(p * p)} - {2 * m_ * n_} = {tex(visible)}$ cm².")

    def cm2(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}\\ \\text{{cm}}^{{2}}$")

    distractores = [
        cm2(p * p - 4 * m_ * n_, "no divide por 2 al calcular el área de cada triángulo"),
        cm2(p * p - m_ * n_ // 2, "resta el área de un solo triángulo"),
        cm2(p * p + 2 * m_ * n_, "suma el área de los triángulos en vez de restarla"),
    ]
    return Propuesta(enunciado, cm2(visible), distractores, pasos,
                     lambda v: v == p * p - 4 * Fraction(m_ * n_, 2), "media",
                     figura=figuras.cuadrado_con_esquinas(p, m_, n_, f"{p} cm", f"{m_} cm", f"{n_} cm"))


@plantilla(EJE)
def volumen_al_escalar_las_aristas(rng):
    lado = rng.randrange(2, 9)
    alto = rng.choice([n for n in range(3, 13) if n != lado])
    k = rng.choice([2, 3])
    veces = {2: "al doble", 3: "al triple"}[k]
    original = lado * lado * alto
    nuevo = original * k ** 3
    enunciado = (f"Un paralelepípedo recto tiene base cuadrada de lado {lado} cm y altura {alto} cm. Si las medidas de todas sus "
                 f"aristas aumentan {veces}, ¿cuál es el volumen del nuevo paralelepípedo?")
    pasos = (f"Las nuevas medidas son {lado * k} cm, {lado * k} cm y {alto * k} cm, así que el volumen es "
             f"${lado * k} \\cdot {lado * k} \\cdot {alto * k} = {tex(nuevo)}$ cm³. Equivale a multiplicar el volumen original "
             f"({original} cm³) por ${k}^{{3}} = {k ** 3}$.")

    def cm3(v, error=None):
        return op(v, error, f"${tex(v)}\\ \\text{{cm}}^{{3}}$")

    distractores = [
        cm3(original * k, f"multiplica el volumen original por {k}, como si creciera una sola dimensión"),
        cm3(original * k * k, f"multiplica el volumen original por ${k}^{{2}}$, como si crecieran solo dos dimensiones"),
        cm3(original, "calcula el volumen original, sin aplicar el aumento"),
    ]
    return Propuesta(enunciado, cm3(nuevo), distractores, pasos,
                     lambda v: v == (k * lado) * (k * lado) * (k * alto), "media")


@plantilla(EJE)
def medida_real_desde_un_plano_a_escala(rng):
    escala = rng.choice([5, 8, 20, 25, 40, 50])
    en_plano = rng.randrange(12, 151)
    objeto, parte = rng.choice([("una guitarra", "el mástil"), ("un mueble", "la cubierta"),
                                ("un kayak", "el casco"), ("una bicicleta", "el marco")])
    real = Fraction(en_plano * escala, 10)
    enunciado = (f"En un taller se construirá {objeto} a partir de un plano dibujado a escala $1 : {escala}$. En el plano, "
                 f"{parte} mide {en_plano} mm de largo. ¿Cuál es el largo real de esa pieza, en centímetros?")
    pasos = (f"La medida real es {escala} veces la del plano: ${en_plano} \\cdot {escala} = {tex(en_plano * escala)}$ mm. "
             f"Como 10 mm equivalen a 1 cm, corresponde a ${tex(real)}$ cm.")

    def cm(v, error=None):
        return op(Fraction(v), error, f"${tex(v)}$ cm")

    distractores = [
        cm(en_plano * escala, "multiplica por la escala pero no convierte los milímetros a centímetros"),
        cm(Fraction(en_plano * escala, 100), "convierte como si 1 cm equivaliera a 100 mm"),
        cm(Fraction(en_plano, escala), "divide por la escala en vez de multiplicar"),
    ]
    return Propuesta(enunciado, cm(real), distractores, pasos, lambda v: v * 10 == en_plano * escala, "media")


@plantilla(EJE)
def distancia_entre_un_punto_y_su_reflejo(rng):
    a, b, c = rng.choice(TERNAS[:4])
    if rng.random() < 0.5:
        a, b = b, a
    p = (a * rng.choice([-1, 1]), b * rng.choice([-1, 1]))
    eje = rng.choice(["X", "Y"])
    reflejo = (p[0], -p[1]) if eje == "X" else (-p[0], p[1])
    propia, otra = (abs(p[1]), abs(p[0])) if eje == "X" else (abs(p[0]), abs(p[1]))
    enunciado = (f"El punto $A$ de coordenadas {_punto(p)} se refleja con respecto al eje ${eje}$ y se obtiene el punto $B$. "
                 f"¿Cuál es la distancia entre $A$ y $B$?")
    pasos = (f"El reflejo es $B({reflejo[0]},\\ {reflejo[1]})$. $A$ y $B$ están a la misma distancia del eje ${eje}$, "
             f"{propia} unidades cada uno, en lados opuestos: la distancia entre ellos es $2 \\cdot {propia} = {2 * propia}$ unidades.")
    distractores = [
        op(propia, "entrega la distancia del punto al eje, no la distancia entre los dos puntos"),
        op(2 * otra, "usa la coordenada que no cambia con la reflexión"),
        op(2 * c, "refleja el punto con respecto al origen en vez de hacerlo con respecto al eje"),
    ]
    return Propuesta(enunciado, op(2 * propia), distractores, pasos,
                     lambda v: v == abs(_complejo(p) - _complejo(reflejo)), "media",
                     figura=figuras.plano_cartesiano(puntos={"A": p, "B": reflejo}))

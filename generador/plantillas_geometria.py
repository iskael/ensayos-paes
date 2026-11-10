from __future__ import annotations

from fractions import Fraction

import figuras
from nucleo import Descartar, Propuesta, miles, op, par, plantilla, raiz_tex, tex

EJE = "geometria"

TERNAS = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def _largo(cuadrado: int, unidad: str) -> str:
    return f"${raiz_tex(cuadrado)}$ {unidad}"


@plantilla(EJE)
def teorema_de_pitagoras(rng):
    a, b, c = rng.choice(TERNAS)
    k = rng.choice([1, 2, 3]) if c < 30 else 1
    a, b, c = a * k, b * k, c * k
    if rng.random() < 0.5:
        a, b = b, a
    if rng.random() < 0.5:
        unidad = "m"
        enunciado = rng.choice([
            f"Una escalera está apoyada en una pared vertical. Su base queda a {a} m de la pared y su extremo superior "
            f"alcanza una altura de {b} m. ¿Cuánto mide la escalera?",
            f"Un terreno rectangular mide {a} m de ancho y {b} m de largo. ¿Cuánto mide su diagonal?",
        ])
        pasos = (f"Se forma un triángulo rectángulo de catetos {a} y {b}. Por el teorema de Pitágoras, "
                 f"la hipotenusa es $\\sqrt{{{a}^{{2}} + {b}^{{2}}}} = \\sqrt{{{a * a + b * b}}} = {c}$ m.")
        figura = (figuras.triangulo_rectangulo(a, b, f"{a} m", f"{b} m", "?", muro=True) if "escalera" in enunciado
                  else figuras.rectangulo(a, b, f"{a} m", f"{b} m", diagonal="?"))
        correcto = c * c
        distractores = [
            op((a + b) ** 2, "suma las longitudes de los catetos", _largo((a + b) ** 2, unidad)),
            op(abs(a * a - b * b), "resta los cuadrados de los catetos en vez de sumarlos", _largo(abs(a * a - b * b), unidad)),
            op((a * a + b * b) ** 2, "suma los cuadrados pero no extrae la raíz cuadrada", _largo((a * a + b * b) ** 2, unidad)),
        ]
        comprobar = lambda v: v == a * a + b * b
        dificultad = "baja"
    else:
        unidad = "cm"
        enunciado = (f"En un triángulo rectángulo, la hipotenusa mide {c} cm y uno de los catetos mide {a} cm. "
                     f"¿Cuánto mide el otro cateto?")
        pasos = (f"Por el teorema de Pitágoras, el cateto buscado es "
                 f"$\\sqrt{{{c}^{{2}} - {a}^{{2}}}} = \\sqrt{{{c * c - a * a}}} = {b}$ cm.")
        figura = figuras.triangulo_rectangulo(a, b, f"{a} cm", "?", f"{c} cm")
        correcto = b * b
        distractores = [
            op(c * c + a * a, "suma los cuadrados como si buscara la hipotenusa", _largo(c * c + a * a, unidad)),
            op((c - a) ** 2, "resta directamente las longitudes", _largo((c - a) ** 2, unidad)),
            op((c * c - a * a) ** 2, "resta los cuadrados pero no extrae la raíz cuadrada", _largo((c * c - a * a) ** 2, unidad)),
        ]
        comprobar = lambda v: v + a * a == c * c
        dificultad = "media"
    return Propuesta(enunciado, op(correcto, texto=_largo(correcto, unidad)), distractores, pasos, comprobar, dificultad, figura=figura)


def _con_pi(coef, unidad: str) -> str:
    coef = Fraction(coef)
    cuerpo = "" if coef == 1 else tex(coef)
    return f"${cuerpo}\\pi\\ \\text{{{unidad}}}$" if "^" not in unidad else f"${cuerpo}\\pi\\ \\text{{{unidad.split('^')[0]}}}^{{{unidad.split('^')[1]}}}$"


@plantilla(EJE)
def area_del_circulo(rng):
    d = rng.randrange(6, 41, 2)
    r = d // 2
    objeto, unidad = rng.choice([("Una mesa circular", "cm"), ("Una plaza circular", "m"),
                                 ("Una tapa circular", "cm"), ("Un jardín circular", "m")])
    u2 = f"{unidad}^2"
    da_diametro = rng.random() < 0.6
    dato = f"un diámetro de {d} {unidad}" if da_diametro else f"un radio de {r} {unidad}"
    enunciado = f"{objeto} tiene {dato}. ¿Cuál es su área?"
    pasos = ((f"El radio es la mitad del diámetro: {r} {unidad}. " if da_diametro else "") +
             f"El área es $\\pi r^{{2}} = \\pi \\cdot {r}^{{2}} = {r * r}\\pi$ {unidad}².")
    distractores = [
        op(d * d, "usa el diámetro en lugar del radio en la fórmula del área", _con_pi(d * d, u2)),
        op(d, "calcula el perímetro ($2\\pi r$) en vez del área", _con_pi(d, u2)),
        op(r, "no eleva el radio al cuadrado", _con_pi(r, u2)),
    ]
    return Propuesta(enunciado, op(r * r, texto=_con_pi(r * r, u2)), distractores, pasos,
                     lambda v: v * 4 == d * d, "media" if da_diametro else "baja",
                     figura=figuras.circulo_con_medida(f"{d} {unidad}", "diametro") if da_diametro
                     else figuras.circulo_con_medida(f"{r} {unidad}", "radio"))


@plantilla(EJE)
def volumen_de_cilindro_o_cono(rng):
    r = rng.randrange(3, 11)
    h = rng.choice([k for k in range(3, 19, 3) if k != r])
    u3 = "cm^3"
    if rng.random() < 0.5:
        enunciado = (f"Un tarro con forma de cilindro recto tiene un radio basal de {r} cm y una altura de {h} cm. "
                     f"¿Cuál es su volumen?")
        correcto = Fraction(r * r * h)
        pasos = f"El volumen del cilindro es $\\pi r^{{2}} h = \\pi \\cdot {r}^{{2}} \\cdot {h} = {tex(correcto)}\\pi$ cm³."
        distractores = [
            op(Fraction(2 * r * h), "calcula el área lateral ($2\\pi r h$) en vez del volumen", _con_pi(2 * r * h, u3)),
            op(Fraction(r * h * h), "eleva al cuadrado la altura en vez del radio", _con_pi(r * h * h, u3)),
            op(Fraction(r * r * h, 3), "usa la fórmula del cono (divide por 3)", _con_pi(Fraction(r * r * h, 3), u3)),
        ]
        factor = 1
        dificultad = "media"
        figura = figuras.cilindro(f"{r} cm", f"{h} cm", h / r)
    else:
        enunciado = (f"Un cono recto tiene un radio basal de {r} cm y una altura de {h} cm. ¿Cuál es su volumen?")
        correcto = Fraction(r * r * h, 3)
        pasos = (f"El volumen del cono es $\\frac{{1}}{{3}}\\pi r^{{2}} h = \\frac{{1}}{{3}} \\cdot \\pi \\cdot {r}^{{2}} "
                 f"\\cdot {h} = {tex(correcto)}\\pi$ cm³.")
        distractores = [
            op(Fraction(r * r * h), "usa la fórmula del cilindro (olvida dividir por 3)", _con_pi(r * r * h, u3)),
            op(Fraction(r * h * h, 3), "eleva al cuadrado la altura en vez del radio", _con_pi(Fraction(r * h * h, 3), u3)),
            op(Fraction(r * h, 3), "no eleva el radio al cuadrado", _con_pi(Fraction(r * h, 3), u3)),
        ]
        factor = 3
        dificultad = "alta"
        figura = figuras.cono(f"{r} cm", f"{h} cm", h / r)
    return Propuesta(enunciado, op(correcto, texto=_con_pi(correcto, u3)), distractores, pasos,
                     lambda v: v * factor == r * r * h, dificultad, figura=figura)


@plantilla(EJE)
def escala_de_un_mapa(rng):
    escala = rng.choice([50000, 200000, 250000, 400000, 500000, 2000000])
    d = rng.randrange(2, 17)
    real = Fraction(d * escala, 100000)
    enunciado = (f"En un mapa dibujado a escala $1 : {miles(escala)}$, dos ciudades están separadas por {d} cm. "
                 f"¿Cuál es la distancia real entre ellas, en kilómetros?")
    pasos = (f"Cada centímetro del mapa representa {miles(escala)} cm reales. La distancia real es "
             f"${d} \\cdot {miles(escala)} = {miles(d * escala)}$ cm. Como 1 km equivale a 100.000 cm, "
             f"corresponde a ${tex(real)}$ km.")

    def km(v):
        return f"${tex(v)}$ km"

    distractores = [
        op(real * 10, "convierte usando 1 km = 10.000 cm", km(real * 10)),
        op(Fraction(d * 100000, escala), "divide por la escala en vez de multiplicar", km(Fraction(d * 100000, escala))),
        op(real * 1000, "convierte los centímetros a metros y los entrega como kilómetros", km(real * 1000)),
    ]
    return Propuesta(enunciado, op(real, texto=km(real)), distractores, pasos,
                     lambda v: v * 100000 == d * escala, "media")


@plantilla(EJE)
def semejanza_con_sombras(rng):
    alto, sombra = rng.sample(range(2, 9), 2)
    k = rng.randrange(3, 10)
    sombra2 = sombra * k
    correcto = alto * k
    objeto, el_objeto = rng.choice([("un edificio", "el edificio"), ("un árbol", "el árbol"),
                                   ("una torre", "la torre"), ("una antena", "la antena")])
    if (sombra * sombra2) % alto:
        raise Descartar
    enunciado = (f"A cierta hora, un poste vertical de {alto} m de altura proyecta una sombra de {sombra} m. "
                 f"A la misma hora, {objeto} proyecta una sombra de {sombra2} m. ¿Qué altura tiene {el_objeto}?")
    pasos = (f"Los triángulos formados son semejantes, así que las alturas y las sombras son proporcionales: "
             f"$\\frac{{h}}{{{sombra2}}} = \\frac{{{alto}}}{{{sombra}}}$, de donde $h = {correcto}$ m.")

    def mt(v):
        return f"${tex(v)}$ m"

    distractores = [
        op(sombra * sombra2 // alto, "plantea la proporción con la razón invertida", mt(sombra * sombra2 // alto)),
        op(alto + sombra2 - sombra, "suma la diferencia entre las sombras en vez de usar la proporción", mt(alto + sombra2 - sombra)),
        op(alto * sombra2, "multiplica la altura del poste por la sombra y no divide", mt(alto * sombra2)),
    ]
    return Propuesta(enunciado, op(correcto, texto=mt(correcto)), distractores, pasos,
                     lambda v: v * sombra == alto * sombra2, "media",
                     figura=figuras.sombras(f"{alto} m", f"{sombra} m", f"{sombra2} m", el_objeto.split(" ", 1)[1]))


@plantilla(EJE)
def punto_medio_de_un_segmento(rng):
    x1, y1 = rng.randrange(-9, 10), rng.randrange(-9, 10)
    x2 = x1 + 2 * rng.choice([k for k in range(-6, 7) if k != 0])
    y2 = y1 + 2 * rng.choice([k for k in range(-6, 7) if k != 0])
    if (x1 + y1) % 2 or (x2 + y2) % 2:
        raise Descartar
    medio = ((x1 + x2) // 2, (y1 + y2) // 2)

    def alt(punto, error=None):
        return op(punto, error, f"$({punto[0]},\\ {punto[1]})$")

    enunciado = (f"En el plano cartesiano, ¿cuáles son las coordenadas del punto medio del segmento de extremos "
                 f"$A({x1},\\ {y1})$ y $B({x2},\\ {y2})$?")
    pasos = (f"Se promedian las coordenadas: $x = \\frac{{{x1} + {par(x2)}}}{{2}} = {medio[0]}$ e "
             f"$y = \\frac{{{y1} + {par(y2)}}}{{2}} = {medio[1]}$. El punto medio es $({medio[0]},\\ {medio[1]})$.")
    distractores = [
        alt(((x2 - x1) // 2, (y2 - y1) // 2), "resta las coordenadas en vez de sumarlas"),
        alt((x1 + x2, y1 + y2), "suma las coordenadas pero no divide por 2"),
        alt(((x1 + y1) // 2, (x2 + y2) // 2), "promedia las coordenadas de cada punto en vez de promediar las $x$ y las $y$ por separado"),
    ]
    return Propuesta(enunciado, alt(medio), distractores, pasos,
                     lambda v: (2 * v[0] - x1, 2 * v[1] - y1) == (x2, y2), "baja",
                     figura=figuras.plano_cartesiano(puntos={"A": (x1, y1), "B": (x2, y2)}, segmentos=[((x1, y1), (x2, y2))]))


@plantilla(EJE)
def area_de_rectangulo_desde_perimetro(rng):
    k = rng.choice([2, 3, 4])
    ancho = rng.randrange(2, 13)
    largo = k * ancho
    perimetro = 2 * (ancho + largo)
    veces = {2: "el doble", 3: "el triple", 4: "cuatro veces"}[k]
    enunciado = (f"El largo de un rectángulo mide {veces} de su ancho y su perímetro es {perimetro} cm. "
                 f"¿Cuál es el área del rectángulo?")
    pasos = (f"Si el ancho es $a$, el largo es ${k}a$ y el perímetro es $2(a + {k}a) = {2 * (k + 1)}a = {perimetro}$, "
             f"de donde $a = {ancho}$ cm y el largo es {largo} cm. El área es ${ancho} \\cdot {largo} = {ancho * largo}$ cm².")

    def cm2(v):
        return f"${tex(v)}\\ \\text{{cm}}^{{2}}$"

    distractores = [
        op(4 * ancho * largo, "plantea el perímetro como ancho más largo, sin considerar los cuatro lados", cm2(4 * ancho * largo)),
        op(largo, "entrega la medida del largo en vez del área", cm2(largo)),
        op(ancho * ancho, "eleva el ancho al cuadrado, como si el rectángulo fuera un cuadrado", cm2(ancho * ancho)),
    ]

    def comprobar(v):
        a = Fraction(perimetro, 2 * (k + 1))
        return v == a * (k * a)

    return Propuesta(enunciado, op(ancho * largo, texto=cm2(ancho * largo)), distractores, pasos, comprobar, "alta",
                     figura=figuras.rectangulo(largo, ancho, "largo", "ancho"))

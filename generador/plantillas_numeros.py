from __future__ import annotations

import math
from fractions import Fraction

from nucleo import Descartar, Propuesta, frac, m, miles, op, opf, pesos, plantilla, raiz_tex, tex

EJE = "numeros"

ARTICULOS = ["una mochila", "una calculadora científica", "un par de zapatillas", "una chaqueta", "un libro", "una bicicleta"]


@plantilla(EJE)
def precio_con_variacion_porcentual(rng):
    articulo = rng.choice(ARTICULOS)
    precio = rng.randrange(8000, 90001, 2000)
    pct = rng.choice([5, 10, 15, 20, 25, 30, 40])
    descuento = rng.random() < 0.6
    variacion = precio * pct // 100
    if descuento:
        correcto = precio - variacion
        enunciado = (f"El precio normal de {articulo} es {pesos(precio)}. Durante una liquidación se vende con "
                     f"un {pct} % de descuento. ¿Cuál es su precio final?")
        pasos = (f"El descuento es el {pct} % de {pesos(precio)}, es decir, {pesos(variacion)}. "
                 f"El precio final es {pesos(precio)} menos {pesos(variacion)}, que da {pesos(correcto)}.")
        distractores = [
            op(variacion, "entrega solo el monto del descuento, sin restarlo del precio", pesos(variacion)),
            op(precio + variacion, "suma el porcentaje en vez de restarlo", pesos(precio + variacion)),
            op(precio - pct * 100, f"trata el {pct} % como un monto fijo de {pesos(pct * 100)}", pesos(precio - pct * 100)),
        ]
    else:
        correcto = precio + variacion
        enunciado = (f"El precio de {articulo} era {pesos(precio)} y aumentó en un {pct} %. "
                     f"¿Cuál es su nuevo precio?")
        pasos = (f"El aumento es el {pct} % de {pesos(precio)}, es decir, {pesos(variacion)}. "
                 f"El nuevo precio es {pesos(precio)} más {pesos(variacion)}, que da {pesos(correcto)}.")
        distractores = [
            op(variacion, "entrega solo el monto del aumento, sin sumarlo al precio", pesos(variacion)),
            op(precio - variacion, "resta el porcentaje en vez de sumarlo", pesos(precio - variacion)),
            op(precio + pct * 100, f"trata el {pct} % como un monto fijo de {pesos(pct * 100)}", pesos(precio + pct * 100)),
        ]
    factor = 100 - pct if descuento else 100 + pct
    return Propuesta(enunciado, op(correcto, texto=pesos(correcto)), distractores, pasos,
                     lambda v: v * 100 == precio * factor, "baja")


@plantilla(EJE)
def precio_original_antes_del_descuento(rng):
    articulo = rng.choice(ARTICULOS)
    original = rng.randrange(10000, 120001, 2000)
    pct = rng.choice([10, 20, 25, 40])
    final = original * (100 - pct) // 100
    enunciado = (f"Después de aplicarle un {pct} % de descuento, {articulo} cuesta {pesos(final)}. "
                 f"¿Cuál era su precio antes del descuento?")
    pasos = (f"El precio pagado corresponde al {100 - pct} % del precio original. "
             f"Entonces el original es {pesos(final)} dividido por {m(Fraction(100 - pct, 100))}, que da {pesos(original)}.")
    distractores = [
        op(Fraction(final * (100 + pct), 100), f"aumenta el precio rebajado en un {pct} %, pero el porcentaje se calcula sobre el precio original",
           pesos(final * (100 + pct) // 100)),
        op(Fraction(final * (100 - pct), 100), f"vuelve a descontar el {pct} % en vez de deshacer el descuento",
           pesos(final * (100 - pct) // 100)),
        op(Fraction(final * 100, pct), f"divide por {pct} % en vez de por {100 - pct} %", pesos(final * 100 // pct)),
    ]
    if (final * (100 + pct)) % 100 or (final * (100 - pct)) % 100 or (final * 100) % pct:
        raise Descartar
    return Propuesta(enunciado, op(Fraction(original), texto=pesos(original)), distractores, pasos,
                     lambda v: v * (100 - pct) == final * 100, "alta")


@plantilla(EJE)
def fraccion_del_total(rng):
    b, d = rng.sample([2, 3, 4, 5, 6, 8, 10], 2)
    a = rng.randrange(1, b)
    c = rng.randrange(1, d)
    if math.gcd(a, b) != 1 or math.gcd(c, d) != 1:
        raise Descartar
    f1, f2 = Fraction(a, b), Fraction(c, d)
    suma = f1 + f2
    if suma >= 1:
        raise Descartar
    quien, tarea = rng.choice([("Camila", "pintó"), ("Benjamín", "leyó"), ("Antonia", "recorrió"), ("Matías", "completó")])
    cosa = {"pintó": "una muralla", "leyó": "un libro", "recorrió": "una ruta", "completó": "un álbum"}[tarea]
    pide_resto = rng.random() < 0.5
    base = (f"{quien} {tarea} ${frac(f1)}$ de {cosa} en la mañana y ${frac(f2)}$ en la tarde. ")
    comun = b * d // math.gcd(b, d)
    pasos_suma = (f"Con denominador común {comun}: ${frac(f1)} + {frac(f2)} = "
                  f"\\frac{{{a * comun // b}}}{{{comun}}} + \\frac{{{c * comun // d}}}{{{comun}}} = {frac(suma)}$.")
    mala = Fraction(a + c, b + d)
    if pide_resto:
        correcto = 1 - suma
        enunciado = base + "¿Qué fracción le falta para terminar?"
        pasos = pasos_suma + f" Lo que falta es $1 - {frac(suma)} = {frac(correcto)}$."
        distractores = [
            opf(suma, "entrega lo que ya avanzó, no lo que falta"),
            opf(1 - mala, "suma numeradores entre sí y denominadores entre sí antes de restar de 1"),
            opf(mala, "suma numeradores entre sí y denominadores entre sí"),
        ]
        dificultad = "media"
    else:
        correcto = suma
        enunciado = base + "¿Qué fracción lleva en total?"
        pasos = pasos_suma
        distractores = [
            opf(mala, "suma numeradores entre sí y denominadores entre sí"),
            opf(Fraction(a + c, b * d), "multiplica los denominadores pero suma los numeradores sin amplificar"),
            opf(f1 * f2, "multiplica las fracciones en vez de sumarlas"),
        ]
        dificultad = "baja"
    objetivo = 1 if pide_resto else 0
    return Propuesta(enunciado, opf(correcto), distractores, pasos,
                     lambda v: (abs(objetivo - v) if pide_resto else v) * b * d == a * d + c * b, dificultad)


@plantilla(EJE)
def propiedades_de_potencias(rng):
    base = rng.choice([2, 3, 5, 7, 10])
    e1, e2, e3 = rng.randrange(2, 9), rng.randrange(2, 9), rng.randrange(2, 12)
    correcto = e1 + e2 - e3

    def pot(e):
        return f"${base}^{{{e}}}$"

    enunciado = (f"¿Cuál de las siguientes expresiones es igual a "
                 f"$\\dfrac{{{base}^{{{e1}}} \\cdot {base}^{{{e2}}}}}{{{base}^{{{e3}}}}}$?")
    pasos = (f"Al multiplicar potencias de igual base se suman los exponentes y al dividir se restan: "
             f"${e1} + {e2} - {e3} = {correcto}$, por lo que el resultado es {pot(correcto)}.")
    distractores = [
        op(e1 * e2 - e3, "multiplica los exponentes del numerador en vez de sumarlos", pot(e1 * e2 - e3)),
        op(e1 + e2 + e3, "suma el exponente del denominador en vez de restarlo", pot(e1 + e2 + e3)),
        op(e3 - e1 - e2, "resta en el orden inverso (denominador menos numerador)", pot(e3 - e1 - e2)),
    ]
    real = Fraction(base) ** e1 * Fraction(base) ** e2 / Fraction(base) ** e3
    return Propuesta(enunciado, op(correcto, texto=pot(correcto)), distractores, pasos,
                     lambda v: Fraction(base) ** v == real, "media" if correcto < 0 else "baja")


@plantilla(EJE)
def proporcion_directa(rng):
    objeto, plural = rng.choice([("cuaderno", "cuadernos"), ("entrada al cine", "entradas al cine"),
                                 ("kilogramo de manzanas", "kilogramos de manzanas"), ("pasaje", "pasajes")])
    unitario = rng.randrange(600, 4001, 50)
    n1 = rng.randrange(2, 9)
    n2 = rng.randrange(n1 + 2, n1 + 10)
    total1 = unitario * n1
    correcto = unitario * n2
    enunciado = (f"Por {n1} {plural} se pagan {pesos(total1)}. Si el precio por unidad no cambia, "
                 f"¿cuánto se paga por {n2} {plural}?")
    pasos = (f"Cada {objeto} cuesta {pesos(total1)} dividido por {n1}, es decir, {pesos(unitario)}. "
             f"Por {n2} se pagan ${n2} \\cdot {miles(unitario)} = {miles(correcto)}$ pesos.")
    distractores = [
        op(unitario, "entrega el precio de una sola unidad", pesos(unitario)),
        op(total1 + unitario, "agrega solo una unidad más al total inicial", pesos(total1 + unitario)),
        op(total1 * n2, "multiplica el total inicial por la nueva cantidad sin calcular el precio unitario", pesos(total1 * n2)),
    ]
    return Propuesta(enunciado, op(correcto, texto=pesos(correcto)), distractores, pasos,
                     lambda v: v * n1 == total1 * n2, "baja")


@plantilla(EJE)
def proporcion_inversa(rng):
    agentes, tarea, unidad = rng.choice([
        ("obreros", "construir un muro", "días"),
        ("llaves iguales", "llenar un estanque", "horas"),
        ("máquinas iguales", "fabricar un pedido", "horas"),
        ("pintores", "pintar un edificio", "días"),
    ])
    n1, n2 = rng.sample(range(2, 13), 2)
    t1 = rng.randrange(3, 25)
    if (n1 * t1) % n2 or (t1 * n2) % n1:
        raise Descartar
    correcto = n1 * t1 // n2
    enunciado = (f"Trabajando al mismo ritmo, {n1} {agentes} tardan {t1} {unidad} en {tarea}. "
                 f"¿Cuántas {unidad} tardarían {n2} {agentes}?" if unidad == "horas" else
                 f"Trabajando al mismo ritmo, {n1} {agentes} tardan {t1} {unidad} en {tarea}. "
                 f"¿Cuántos {unidad} tardarían {n2} {agentes}?")
    pasos = (f"Es una proporción inversa: el producto se mantiene constante. "
             f"${n1} \\cdot {t1} = {n1 * t1}$, y ${n1 * t1} : {n2} = {correcto}$ {unidad}.")
    distractores = [
        op(t1 * n2 // n1, "la trata como proporción directa"),
        op(t1 - (n2 - n1), "resta la diferencia de cantidades en vez de usar la proporción"),
        op(n1 * t1, "calcula el producto constante pero no lo divide"),
    ]
    if t1 - (n2 - n1) <= 0:
        raise Descartar
    return Propuesta(enunciado, op(correcto), distractores, pasos,
                     lambda v: v * n2 == n1 * t1, "media")


@plantilla(EJE)
def suma_de_raices(rng):
    r = rng.choice([2, 3, 5, 7])
    a, b = rng.sample(range(2, 8), 2)
    n1, n2 = a * a * r, b * b * r
    correcto = (a + b) ** 2 * r

    def alt(cuadrado, error=None):
        return op(cuadrado, error, f"${raiz_tex(cuadrado)}$")

    enunciado = f"¿Cuál de las siguientes expresiones es igual a $\\sqrt{{{n1}}} + \\sqrt{{{n2}}}$?"
    pasos = (f"Se descompone cada raíz: $\\sqrt{{{n1}}} = {a}\\sqrt{{{r}}}$ y $\\sqrt{{{n2}}} = {b}\\sqrt{{{r}}}$. "
             f"Al sumar términos semejantes resulta ${a + b}\\sqrt{{{r}}}$.")
    distractores = [
        op(n1 + n2, "suma las cantidades subradicales, pero la raíz de una suma no es la suma de las raíces", f"$\\sqrt{{{n1 + n2}}}$"),
        op((a + b) ** 2 * 2 * r, "suma también los radicandos al sumar los términos", f"${a + b}\\sqrt{{{2 * r}}}$"),
        alt((a * b) ** 2 * r, "multiplica los coeficientes en vez de sumarlos"),
    ]
    real = math.sqrt(n1) + math.sqrt(n2)
    return Propuesta(enunciado, alt(correcto), distractores, pasos,
                     lambda v: abs(math.sqrt(v) - real) < 1e-9, "media")

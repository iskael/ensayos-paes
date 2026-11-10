from __future__ import annotations

from fractions import Fraction

from nucleo import Descartar, Propuesta, miles, op, opf, par, pesos, plantilla, polinomio, simplificada, tex

EJE = "algebra_funciones"


@plantilla(EJE)
def ecuacion_lineal_con_parentesis(rng):
    a = rng.randrange(2, 8)
    c = rng.choice([k for k in range(1, 10) if k != a])
    b = rng.choice([k for k in range(-6, 7) if k != 0])
    x0 = rng.choice([k for k in range(-6, 10) if k != 0])
    d = a * (x0 + b) - c * x0
    izquierda = f"{a}({polinomio([1, b])})"
    derecha = polinomio([c, d])
    enunciado = f"¿Cuál es la solución de la ecuación ${izquierda} = {derecha}$?"
    pasos = (f"Se distribuye: ${polinomio([a, a * b])} = {derecha}$. Se agrupan las $x$ a un lado: "
             f"${polinomio([a - c, 0])} = {tex(d - a * b)}$, de donde $x = {tex(x0)}$.")
    distractores = [
        op(Fraction(d - b, a - c), f"no multiplica el segundo término del paréntesis por {a}"),
        op(Fraction(d + a * b, a - c), "comete un error de signo al pasar el término constante al otro lado"),
        op(Fraction(d - a * b, a + c), "suma los términos con $x$ en vez de restarlos al agruparlos"),
    ]
    return Propuesta(enunciado, op(Fraction(x0)), distractores, pasos,
                     lambda v: a * (v + b) == c * v + d, "media")


@plantilla(EJE)
def sistema_de_ecuaciones_en_contexto(rng):
    contexto = rng.choice(["entradas", "monedas", "preguntas"])
    if contexto == "entradas":
        p, q = rng.choice([(5000, 3000), (6000, 2500), (4500, 2000), (8000, 5000), (7000, 4000)])
    elif contexto == "monedas":
        p, q = rng.choice([(500, 100), (100, 50), (500, 50)])
    else:
        p, q = rng.choice([(5, 2), (4, 3), (3, 1), (5, 3)])
    x = rng.randrange(4, 40)
    y = rng.randrange(4, 40)
    if x == y or x == 2 * y or y == 2 * x:
        raise Descartar
    n, total = x + y, p * x + q * y
    if total % (p + q):
        raise Descartar
    if contexto == "entradas":
        enunciado = (f"Para una función de teatro se vendieron {n} entradas en total. La entrada de adulto cuesta "
                     f"{pesos(p)} y la de niño {pesos(q)}. Si se recaudaron {pesos(total)}, ¿cuántas entradas de adulto se vendieron?")
        nombres = ("entradas de adulto", "entradas de niño")
    elif contexto == "monedas":
        enunciado = (f"En una alcancía hay {n} monedas, todas de {pesos(p)} o de {pesos(q)}. Si en total suman "
                     f"{pesos(total)}, ¿cuántas monedas de {pesos(p)} hay?")
        nombres = (f"monedas de {pesos(p)}", f"monedas de {pesos(q)}")
    else:
        enunciado = (f"Una prueba tiene {n} preguntas: algunas valen {p} puntos y las demás valen {q} puntos. "
                     f"Si el puntaje total de la prueba es {total} puntos, ¿cuántas preguntas valen {p} puntos?")
        nombres = (f"preguntas de {p} puntos", f"preguntas de {q} puntos")
    pasos = (f"Sea $x$ la cantidad de {nombres[0]} e $y$ la de {nombres[1]}: $x + y = {n}$ y "
             f"${miles(p)}x + {miles(q)}y = {miles(total)}$. Reemplazando $y = {n} - x$ se obtiene "
             f"${miles(p - q)}x = {miles(total - q * n)}$, por lo que $x = {x}$.")
    distractores = [
        op(y, f"entrega la otra incógnita (la cantidad de {nombres[1]})"),
        op(abs(x - y), "entrega la diferencia entre ambas cantidades"),
        op(total // (p + q), "divide el total por la suma de los dos valores, como si hubiera la misma cantidad de cada tipo"),
    ]
    return Propuesta(enunciado, op(x), distractores, pasos,
                     lambda v: p * v + q * (n - v) == total, "alta")


@plantilla(EJE)
def modelo_lineal_cargo_fijo(rng):
    servicio, unidad, fijo_txt = rng.choice([
        ("Un taxi", "kilómetro recorrido", "un cargo fijo"),
        ("Un servicio de arriendo de bicicletas", "hora de uso", "una inscripción"),
        ("Una gásfiter", "hora de trabajo", "una visita"),
        ("Una imprenta", "afiche impreso", "un costo de diseño"),
    ])
    variable = rng.randrange(300, 2501, 100)
    fijo = variable * rng.randrange(2, 9)
    n = rng.randrange(4, 21)
    total = fijo + variable * n
    plural = {"kilómetro recorrido": "kilómetros", "hora de uso": "horas", "hora de trabajo": "horas", "afiche impreso": "afiches"}[unidad]
    base = f"{servicio} cobra {fijo_txt} de {pesos(fijo)} más {pesos(variable)} por cada {unidad}. "
    if rng.random() < 0.5:
        enunciado = base + f"¿Cuánto se paga en total por {n} {plural}?"
        pasos = (f"El costo es $C(x) = {miles(fijo)} + {miles(variable)}x$. Para $x = {n}$: "
                 f"${miles(fijo)} + {miles(variable)} \\cdot {n} = {miles(total)}$ pesos.")
        correcta = op(total, texto=pesos(total))
        distractores = [
            op((fijo + variable) * n, "suma el cargo fijo y el valor por unidad antes de multiplicar", pesos((fijo + variable) * n)),
            op(variable * n, "olvida sumar el cargo fijo", pesos(variable * n)),
            op(fijo * n + variable, "intercambia el cargo fijo con el valor por unidad", pesos(fijo * n + variable)),
        ]
        return Propuesta(enunciado, correcta, distractores, pasos,
                         lambda v: v - fijo == variable * n, "baja")
    enunciado = base + f"Si una persona pagó {pesos(total)} en total, ¿cuántos {plural} corresponden a ese pago?" \
        if plural != "horas" else base + f"Si una persona pagó {pesos(total)} en total, ¿cuántas horas corresponden a ese pago?"
    pasos = (f"Se plantea ${miles(fijo)} + {miles(variable)}x = {miles(total)}$. Restando el cargo fijo: ${miles(variable)}x = {miles(total - fijo)}$, "
             f"de donde $x = {n}$.")
    distractores = [
        op(Fraction(total, variable), "divide el total por el valor unitario sin descontar el cargo fijo"),
        op(Fraction(total + fijo, variable), "suma el cargo fijo en vez de restarlo"),
        op(Fraction(total - fijo, fijo), "resta el cargo fijo pero divide por el cargo fijo en vez de por el valor unitario"),
    ]
    return Propuesta(enunciado, op(Fraction(n)), distractores, pasos,
                     lambda v: fijo + variable * v == total, "media")


@plantilla(EJE)
def pendiente_entre_dos_puntos(rng):
    x1, y1 = rng.randrange(-6, 7), rng.randrange(-6, 7)
    dx = rng.choice([k for k in range(-6, 7) if k != 0])
    dy = rng.choice([k for k in range(-8, 9) if k != 0])
    x2, y2 = x1 + dx, y1 + dy
    if abs(dx) == abs(dy) or x1 + x2 == 0:
        raise Descartar
    pendiente = Fraction(dy, dx)
    enunciado = (f"¿Cuál es la pendiente de la recta que pasa por los puntos $A({x1},\\ {y1})$ y $B({x2},\\ {y2})$?")
    pasos = (f"La pendiente es el cociente entre la variación de $y$ y la de $x$: "
             f"$m = \\frac{{{y2} - {par(y1)}}}{{{x2} - {par(x1)}}} = {simplificada(dy, dx)}$.")
    distractores = [
        opf(Fraction(dx, dy), "invierte el cociente: divide la variación de $x$ por la de $y$"),
        opf(-pendiente, "resta las coordenadas en distinto orden en el numerador y en el denominador"),
        opf(Fraction(y1 + y2, x1 + x2), "suma las coordenadas en vez de restarlas"),
    ]
    return Propuesta(enunciado, opf(pendiente), distractores, pasos,
                     lambda v: v * (x2 - x1) == y2 - y1, "media")


def _conjunto(valores) -> str:
    return "$\\{" + ",\\ ".join(tex(v) for v in sorted(valores)) + "\\}$"


@plantilla(EJE)
def soluciones_de_ecuacion_cuadratica(rng):
    r1, r2 = rng.sample([k for k in range(-9, 10) if k != 0], 2)
    if r1 == -r2:
        raise Descartar
    s, p = r1 + r2, r1 * r2
    ecuacion = polinomio([1, -s, p])
    enunciado = f"¿Cuál es el conjunto solución de la ecuación ${ecuacion} = 0$?"
    pasos = (f"Se buscan dos números cuyo producto sea ${p}$ y cuya suma sea ${s}$: son ${r1}$ y ${r2}$. "
             f"Así, ${ecuacion} = (x {'-' if r1 > 0 else '+'} {abs(r1)})(x {'-' if r2 > 0 else '+'} {abs(r2)})$ "
             f"y las soluciones son {_conjunto({r1, r2})}.")

    def alt(valores, error=None):
        if len(valores) != 2:
            raise Descartar
        return op(frozenset(valores), error, _conjunto(valores))

    distractores = [
        alt({-r1, -r2}, "factoriza bien pero toma los números del paréntesis con su mismo signo"),
        alt({-s, p}, "toma los coeficientes de la ecuación como si fueran las soluciones"),
        alt({-r1, r2} if abs(r1) < abs(r2) else {r1, -r2}, "comete un error de signo en una de las soluciones"),
    ]
    return Propuesta(enunciado, alt({r1, r2}), distractores, pasos,
                     lambda v: len(v) == 2 and all(x * x - s * x + p == 0 for x in v), "media")


@plantilla(EJE)
def producto_de_binomios(rng):
    if rng.random() < 0.5:
        a, b = (rng.choice([k for k in range(-8, 9) if k != 0]) for _ in range(2))
        if a == -b:
            raise Descartar
        expresion = f"({polinomio([1, a])})({polinomio([1, b])})"
        correcto = (1, a + b, a * b)
        pasos = (f"Se multiplica cada término: $x \\cdot x = x^{{2}}$, los términos cruzados suman "
                 f"${polinomio([a + b, 0])}$ y el producto de los términos libres es ${a * b}$. "
                 f"Resulta ${polinomio(list(correcto))}$.")
        malos = [
            ((1, 0, a * b), "multiplica solo primero con primero y último con último, sin los términos cruzados"),
            ((1, a * b, a + b), "intercambia la suma y el producto de los términos libres"),
            ((1, a + b, -a * b), "comete un error de signo en el producto de los términos libres"),
        ]
        dificultad = "baja"
        evaluar = lambda x: (x + a) * (x + b)
    else:
        a = rng.randrange(2, 6)
        b = rng.choice([k for k in range(-7, 8) if k != 0])
        expresion = f"({polinomio([a, b])})^{{2}}"
        correcto = (a * a, 2 * a * b, b * b)
        pasos = (f"Cuadrado de binomio: el cuadrado del primer término es ${a * a}x^{{2}}$, el doble producto es "
                 f"${polinomio([2 * a * b, 0])}$ y el cuadrado del segundo es ${b * b}$. Resulta ${polinomio(list(correcto))}$.")
        malos = [
            ((a * a, 0, b * b), "eleva cada término al cuadrado y olvida el doble producto"),
            ((a * a, a * b, b * b), "calcula el producto de los términos pero no lo duplica"),
            ((a, 2 * a * b, b * b), f"no eleva al cuadrado el coeficiente {a} del primer término"),
        ]
        dificultad = "media"
        evaluar = lambda x: (a * x + b) ** 2
    enunciado = f"¿Cuál de las siguientes expresiones es equivalente a ${expresion}$?"

    def alt(coefs, error=None):
        return op(coefs, error, f"${polinomio(list(coefs))}$")

    return Propuesta(enunciado, alt(correcto), [alt(c, e) for c, e in malos], pasos,
                     lambda v: all(v[0] * x * x + v[1] * x + v[2] == evaluar(x) for x in (0, 1, 2, 3)), dificultad)


@plantilla(EJE)
def inecuacion_lineal(rng):
    a = rng.choice([-7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
    k = rng.choice([x for x in range(-8, 9) if x != 0])
    b = rng.choice([x for x in range(-9, 10) if x != 0])
    c = a * k + b
    simbolo = rng.choice(["<", ">", "<=", ">="])
    latex = {"<": "<", ">": ">", "<=": "\\le", ">=": "\\ge"}
    opuesto = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}
    resultado = opuesto[simbolo] if a < 0 else simbolo

    def alt(sentido, cota, error=None):
        return op((sentido, Fraction(cota)), error, f"$x {latex[sentido]} {tex(cota)}$")

    enunciado = f"¿Cuál es el conjunto solución de la inecuación ${polinomio([a, b])} {latex[simbolo]} {c}$?"
    if a < 0:
        pasos = (f"Se resta ${b}$ a ambos lados: ${polinomio([a, 0])} {latex[simbolo]} {c - b}$. Al dividir por ${a}$, "
                 f"que es negativo, se invierte el sentido de la desigualdad: $x {latex[resultado]} {k}$.")
        distractores = [
            alt(simbolo, k, "no invierte la desigualdad al dividir por un número negativo"),
            alt(resultado, -k, "invierte la desigualdad pero se equivoca en el signo del cociente"),
            alt(simbolo, -k, "no invierte la desigualdad y además se equivoca en el signo del cociente"),
        ]
        dificultad = "alta"
    else:
        pasos = (f"Se resta ${b}$ a ambos lados: ${polinomio([a, 0])} {latex[simbolo]} {c - b}$. Al dividir por ${a}$, "
                 f"que es positivo, la desigualdad mantiene su sentido: $x {latex[resultado]} {k}$.")
        distractores = [
            alt(opuesto[simbolo], k, "invierte la desigualdad aunque divide por un número positivo"),
            alt(simbolo, Fraction(c + b, a), "comete un error de signo al pasar el término constante al otro lado"),
            alt(simbolo, c - b, f"no divide por {a} después de despejar"),
        ]
        dificultad = "media"

    def cumple(x, sentido, cota):
        return {"<": x < cota, ">": x > cota, "<=": x <= cota, ">=": x >= cota}[sentido]

    def comprobar(v):
        sentido, cota = v
        return all(cumple(x, sentido, cota) == cumple(a * x + b, simbolo, c)
                   for x in (cota - 1, cota, cota + 1, Fraction(k) - 1, Fraction(k), Fraction(k) + 1))

    return Propuesta(enunciado, alt(resultado, k), distractores, pasos, comprobar, dificultad)

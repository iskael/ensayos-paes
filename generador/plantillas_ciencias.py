"""Plantillas de Física y Química de la PAES de Ciencias (temario regular 2026): las preguntas con cálculo.

Electricidad (ley de Ohm, resistencias, potencia y consumo), ondas (rapidez, frecuencia y longitud de onda), mecánica (ley
de Hooke, segunda ley de Newton con roce); estructura atómica (partículas de un ion), cantidad de sustancia, soluciones
(molaridad, dilución, porcentajes) y estequiometría. Las preguntas conceptuales están escritas a mano en `contenido/`.
"""
from __future__ import annotations

from fractions import Fraction

from functools import wraps

from nucleo import Descartar, Propuesta, miles, op, tex
from nucleo import plantilla as _plantilla

CIE, FIS, QUI = "CIENCIAS", "fisica", "quimica"


def _texto_plano(texto: str) -> str:
    partes = texto.split("$")
    return "$".join(p.replace("{,}", ",") if i % 2 == 0 else p for i, p in enumerate(partes))


def plantilla(eje, nivel):
    """Como nucleo.plantilla, pero corrige la coma decimal escrita fuera de las fórmulas."""
    def decorar(f):
        @wraps(f)
        def envuelta(rng):
            p = f(rng)
            p.enunciado = _texto_plano(p.enunciado)
            p.pasos = _texto_plano(p.pasos)
            for o in [p.correcta] + p.distractores:
                o.texto = _texto_plano(o.texto)
            return p
        return _plantilla(eje, nivel)(envuelta)
    return decorar


def _tres_distintos(correcto, candidatos):
    elegidos, vistos = [], {correcto}
    for valor, error in candidatos:
        if valor not in vistos and valor > 0:
            vistos.add(valor)
            elegidos.append((valor, error))
        if len(elegidos) == 3:
            return elegidos
    raise Descartar


def _con_unidad(unidad):
    return lambda v: f"${tex(v)}$ {unidad}"


def _armar(enunciado, correcto, candidatos, pasos, comprobar, dificultad, unidad):
    texto = _con_unidad(unidad)
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(correcto, candidatos)]
    return Propuesta(enunciado, op(correcto, None, texto(correcto)), distractores, pasos, comprobar, dificultad)


# ----------------------------------------------------------------- Física

@plantilla(FIS, CIE)
def ley_de_ohm(rng):
    r = Fraction(rng.choice([2, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 50]))
    i = Fraction(rng.choice([1, 2, 3, 4, 5, 6])) / rng.choice([1, 2, 4, 5])
    v = r * i
    if v.denominator != 1:
        raise Descartar
    pide = rng.choice(["corriente", "resistencia", "voltaje"])
    aparato = rng.choice(["un calefactor", "una ampolleta", "un resistor de un circuito", "un hervidor"])
    if pide == "corriente":
        enunciado = (f"Un circuito simple tiene {aparato} de resistencia {tex(r)} Ω conectado a una fuente de {tex(v)} V. ¿Cuál es la "
                     f"intensidad de la corriente que circula por él?")
        pasos = f"Por la ley de Ohm, $I = \\frac{{V}}{{R}} = \\frac{{{tex(v)}}}{{{tex(r)}}} = {tex(i)}$ A."
        cands = [(v * r, "multiplica el voltaje por la resistencia"), (r / v, "divide la resistencia por el voltaje"),
                 (v - r if v > r else v + r, "resta o suma las magnitudes en vez de dividirlas"), (i * 2, "duplica el resultado")]
        return _armar(enunciado, i, cands, pasos, lambda x: x * r == v, "baja", "A")
    if pide == "resistencia":
        enunciado = (f"Al conectar {aparato} a una diferencia de potencial de {tex(v)} V, circula una corriente de {tex(i)} A. ¿Cuál es su "
                     f"resistencia eléctrica?")
        pasos = f"Por la ley de Ohm, $R = \\frac{{V}}{{I}} = \\frac{{{tex(v)}}}{{{tex(i)}}} = {tex(r)}$ Ω."
        cands = [(v * i, "multiplica el voltaje por la corriente"), (i / v, "divide la corriente por el voltaje"),
                 (v + i, "suma el voltaje y la corriente"), (r / 2, "divide por 2 el resultado")]
        return _armar(enunciado, r, cands, pasos, lambda x: x * i == v, "baja", "Ω")
    enunciado = (f"Por {aparato} de resistencia {tex(r)} Ω circula una corriente de {tex(i)} A. ¿Cuál es la diferencia de potencial "
                 f"entre sus extremos?")
    pasos = f"Por la ley de Ohm, $V = I \\cdot R = {tex(i)} \\cdot {tex(r)} = {tex(v)}$ V."
    cands = [(r / i, "divide la resistencia por la corriente"), (i / r, "divide la corriente por la resistencia"),
             (r + i, "suma la resistencia y la corriente"), (v * 2, "duplica el resultado")]
    return _armar(enunciado, v, cands, pasos, lambda x: x == i * r, "baja", "V")


@plantilla(FIS, CIE)
def resistencias_en_serie_o_paralelo(rng):
    conexion = rng.choice(["serie", "paralelo"])
    if conexion == "serie":
        rs = [Fraction(rng.choice([2, 3, 4, 5, 6, 8, 10, 12])) for _ in range(rng.choice([2, 3]))]
        eq = sum(rs)
        inverso = 1 / sum(1 / x for x in rs)
        cands = [(inverso, "aplica la fórmula de la conexión en paralelo"), (eq / len(rs), "promedia las resistencias"),
                 (max(rs), "toma la resistencia mayor"), (eq * 2, "duplica la suma")]
        pasos = f"En serie las resistencias se suman: $R_{{eq}} = {' + '.join(tex(x) for x in rs)} = {tex(eq)}$ Ω."
    else:
        pares = [(3, 6), (4, 4), (6, 12), (2, 2), (10, 15), (12, 4), (20, 5), (6, 6), (8, 24), (30, 60)]
        a, b = rng.choice(pares)
        rs = [Fraction(a), Fraction(b)]
        eq = 1 / (1 / rs[0] + 1 / rs[1])
        cands = [(rs[0] + rs[1], "suma las resistencias, como si estuvieran en serie"), (1 / rs[0] + 1 / rs[1], "olvida invertir la suma de los inversos"),
                 ((rs[0] + rs[1]) / 2, "promedia las resistencias"), (min(rs), "toma la resistencia menor")]
        pasos = (f"En paralelo, $\\frac{{1}}{{R_{{eq}}}} = \\frac{{1}}{{{tex(rs[0])}}} + \\frac{{1}}{{{tex(rs[1])}}}$, de donde "
                 f"$R_{{eq}} = \\frac{{{tex(rs[0])} \\cdot {tex(rs[1])}}}{{{tex(rs[0])} + {tex(rs[1])}}} = {tex(eq)}$ Ω.")
    lista = ", ".join(f"{tex(x)} Ω" for x in rs[:-1]) + f" y {tex(rs[-1])} Ω"
    enunciado = f"Se conectan en {conexion} resistores de {lista}. ¿Cuál es la resistencia equivalente del conjunto?"
    real = sum(rs) if conexion == "serie" else 1 / sum(1 / x for x in rs)
    return _armar(enunciado, eq, cands, pasos, lambda x: x == real, "media", "Ω")


@plantilla(FIS, CIE)
def consumo_y_costo_electrico(rng):
    potencia = rng.choice([60, 100, 500, 800, 1000, 1200, 1500, 2000, 2200])
    horas = rng.choice([2, 3, 4, 5, 6, 8, 10])
    dias = rng.choice([10, 15, 20, 30])
    precio = rng.choice([150, 180, 200, 220, 250])
    energia = Fraction(potencia * horas * dias, 1000)
    costo = energia * precio
    if costo.denominator != 1:
        raise Descartar
    aparato = rng.choice(["una estufa eléctrica", "un hervidor", "un computador", "un televisor", "un secador de pelo"])
    enunciado = (f"{aparato.capitalize()} de {miles(potencia)} W se usa {horas} horas diarias durante {dias} días. Si el kWh cuesta "
                 f"{precio} pesos, ¿cuánto cuesta la energía que consume en ese periodo?")
    pasos = (f"Energía: ${miles(potencia)} \\text{{ W}} \\cdot {horas} \\text{{ h}} \\cdot {dias} = {miles(potencia * horas * dias)}$ Wh "
             f"$= {tex(energia)}$ kWh. Costo: ${tex(energia)} \\cdot {precio} = {tex(costo)}$ pesos.")
    cands = [(costo * 1000, "no convierte los watts a kilowatts"), (Fraction(potencia * horas * precio, 1000), "calcula el costo de un solo día"),
             (costo / horas, "olvida multiplicar por las horas diarias"), (costo * 2, "duplica el resultado")]
    texto = lambda v: f"${miles(int(v))}$ pesos"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(costo, [(v, e) for v, e in cands if v.denominator == 1])]
    return Propuesta(enunciado, op(costo, None, texto(costo)), distractores, pasos,
                     lambda x: x * 1000 == potencia * horas * dias * precio, "media")


@plantilla(FIS, CIE)
def rapidez_frecuencia_y_longitud_de_onda(rng):
    pide = rng.choice(["rapidez", "frecuencia", "longitud"])
    f = Fraction(rng.choice([2, 4, 5, 10, 20, 25, 40, 50, 100, 200, 250, 500]))
    lam = Fraction(rng.choice([1, 2, 3, 4, 5, 6, 8])) / rng.choice([1, 2, 4, 10])
    v = f * lam
    medio = rng.choice(["una cuerda", "la superficie de un estanque", "un resorte largo", "el aire"])
    if pide == "rapidez":
        enunciado = f"Una onda que se propaga por {medio} tiene una frecuencia de {tex(f)} Hz y una longitud de onda de ${tex(lam)}$ m. ¿Cuál es su rapidez de propagación?"
        pasos = f"$v = \\lambda \\cdot f = {tex(lam)} \\cdot {tex(f)} = {tex(v)}$ m/s."
        cands = [(f / lam, "divide la frecuencia por la longitud de onda"), (lam / f, "divide la longitud de onda por la frecuencia"),
                 (f + lam, "suma la frecuencia y la longitud de onda"), (v / 2, "divide el producto por 2")]
        return _armar(enunciado, v, cands, pasos, lambda x: x == f * lam, "baja", "m/s")
    if pide == "frecuencia":
        enunciado = f"Una onda que se propaga por {medio} con una rapidez de ${tex(v)}$ m/s tiene una longitud de onda de ${tex(lam)}$ m. ¿Cuál es su frecuencia?"
        pasos = f"$f = \\frac{{v}}{{\\lambda}} = \\frac{{{tex(v)}}}{{{tex(lam)}}} = {tex(f)}$ Hz."
        cands = [(v * lam, "multiplica la rapidez por la longitud de onda"), (lam / v, "divide la longitud de onda por la rapidez"),
                 (v + lam, "suma la rapidez y la longitud de onda"), (f * 2, "duplica el resultado")]
        return _armar(enunciado, f, cands, pasos, lambda x: x * lam == v, "media", "Hz")
    enunciado = f"Una onda que se propaga por {medio} con una rapidez de ${tex(v)}$ m/s tiene una frecuencia de {tex(f)} Hz. ¿Cuál es su longitud de onda?"
    pasos = f"$\\lambda = \\frac{{v}}{{f}} = \\frac{{{tex(v)}}}{{{tex(f)}}} = {tex(lam)}$ m."
    cands = [(v * f, "multiplica la rapidez por la frecuencia"), (f / v, "divide la frecuencia por la rapidez"),
             (v + f, "suma la rapidez y la frecuencia"), (lam * 10, "corre la coma un lugar")]
    return _armar(enunciado, lam, cands, pasos, lambda x: x * f == v, "media", "m")


@plantilla(FIS, CIE)
def ley_de_hooke(rng):
    k = Fraction(rng.choice([20, 40, 50, 80, 100, 120, 150, 200, 250, 400, 500]))
    x_cm = Fraction(rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]))
    x = x_cm / 100
    fuerza = k * x
    pide = rng.choice(["fuerza", "estiramiento"])
    if pide == "fuerza":
        enunciado = f"Un resorte ideal de constante elástica {tex(k)} N/m se estira {tex(x_cm)} cm desde su largo natural. ¿Qué fuerza ejerce el resorte?"
        pasos = f"Por la ley de Hooke, $F = k \\cdot x = {tex(k)} \\cdot {tex(x)} = {tex(fuerza)}$ N (el estiramiento en metros)."
        cands = [(k * x_cm, "usa el estiramiento en centímetros sin convertirlo a metros"), (k / x_cm, "divide la constante por el estiramiento"),
                 (fuerza * 10, "convierte los centímetros a metros dividiendo por 10"), (k + x_cm, "suma la constante y el estiramiento")]
        return _armar(enunciado, fuerza, cands, pasos, lambda f_: f_ == k * x, "media", "N")
    enunciado = f"Un resorte ideal de constante elástica {tex(k)} N/m se estira al colgarle un objeto que ejerce una fuerza de ${tex(fuerza)}$ N. ¿Cuántos centímetros se estira?"
    pasos = f"Por la ley de Hooke, $x = \\frac{{F}}{{k}} = \\frac{{{tex(fuerza)}}}{{{tex(k)}}} = {tex(x)}$ m $= {tex(x_cm)}$ cm."
    cands = [(x, "deja el resultado en metros"), (fuerza * k, "multiplica la fuerza por la constante"),
             (x_cm * 10, "convierte a centímetros multiplicando por 1.000"), (k / fuerza, "divide la constante por la fuerza")]
    return _armar(enunciado, x_cm, cands, pasos, lambda c: c / 100 * k == fuerza, "media", "cm")


@plantilla(FIS, CIE)
def segunda_ley_de_newton_con_roce(rng):
    m = Fraction(rng.choice([2, 4, 5, 8, 10, 20, 25, 40, 50]))
    mu = Fraction(rng.choice([1, 2, 3, 4, 5]), 10)
    g = Fraction(10)
    roce = mu * m * g
    f = roce + m * rng.choice([1, 2, 3, 4, 5])
    a = (f - roce) / m
    enunciado = (f"Sobre una caja de {tex(m)} kg apoyada en una superficie horizontal se aplica una fuerza horizontal de {tex(f)} N. Si el "
                 f"coeficiente de roce cinético es ${tex(mu)}$ y $g = 10$ m/s², ¿cuál es la aceleración de la caja?")
    pasos = (f"La fuerza de roce es $\\mu \\cdot m \\cdot g = {tex(mu)} \\cdot {tex(m)} \\cdot 10 = {tex(roce)}$ N. La fuerza neta es "
             f"${tex(f)} - {tex(roce)} = {tex(f - roce)}$ N y $a = \\frac{{{tex(f - roce)}}}{{{tex(m)}}} = {tex(a)}$ m/s².")
    cands = [(f / m, "ignora la fuerza de roce"), ((f + roce) / m, "suma el roce en vez de restarlo"),
             ((f - mu * m) / m, "calcula el roce sin multiplicar por g"), (f - roce, "olvida dividir por la masa")]
    return _armar(enunciado, a, cands, pasos, lambda x: x * m == f - mu * m * g, "alta", "m/s²")


# ----------------------------------------------------------------- Química

_ELEMENTOS = [("sodio", "Na", 11, 23), ("magnesio", "Mg", 12, 24), ("aluminio", "Al", 13, 27), ("azufre", "S", 16, 32),
              ("cloro", "Cl", 17, 35), ("potasio", "K", 19, 39), ("calcio", "Ca", 20, 40), ("oxígeno", "O", 8, 16),
              ("flúor", "F", 9, 19), ("nitrógeno", "N", 7, 14)]
_CARGAS = {"Na": 1, "Mg": 2, "Al": 3, "S": -2, "Cl": -1, "K": 1, "Ca": 2, "O": -2, "F": -1, "N": -3}


@plantilla(QUI, CIE)
def particulas_de_un_ion(rng):
    nombre, simbolo, z, a = rng.choice(_ELEMENTOS)
    carga = _CARGAS[simbolo]
    electrones = z - carga
    neutrones = a - z
    pide = rng.choice(["electrones", "neutrones"])
    signo = ("+" if carga > 0 else "-") if abs(carga) == 1 else f"{abs(carga)}{'+' if carga > 0 else '-'}"
    ion = f"${{}}^{{{a}}}_{{{z}}}\\text{{{simbolo}}}^{{{signo}}}$"
    enunciado = f"¿Cuántos {pide} tiene el ion {ion}?"
    if pide == "electrones":
        correcto = Fraction(electrones)
        pasos = (f"El número atómico es {z}, así que el átomo neutro tiene {z} electrones. Con carga {signo} "
                 f"{'perdió' if carga > 0 else 'ganó'} {abs(carga)}: ${z} {'-' if carga > 0 else '+'} {abs(carga)} = {electrones}$.")
        cands = [(Fraction(z + carga), "suma la carga positiva o resta la negativa, al revés"), (Fraction(z), "olvida la carga del ion"),
                 (Fraction(a - electrones), "resta los electrones a la masa"), (Fraction(neutrones), "calcula los neutrones")]
    else:
        correcto = Fraction(neutrones)
        pasos = f"Los neutrones son el número másico menos el número atómico: ${a} - {z} = {neutrones}$; la carga no los cambia."
        cands = [(Fraction(a), "responde el número másico"), (Fraction(z), "responde el número atómico"),
                 (Fraction(neutrones - carga), "le aplica la carga del ion a los neutrones"), (Fraction(a + z), "suma el número másico y el atómico")]
    distractores = [op(v, e) for v, e in _tres_distintos(correcto, cands)]
    real = electrones if pide == "electrones" else neutrones
    return Propuesta(enunciado, op(correcto), distractores, pasos, lambda v: v == real, "baja")


_COMPUESTOS = [("agua", "H_2O", 18), ("dióxido de carbono", "CO_2", 44), ("cloruro de sodio", "NaCl", 58), ("glucosa", "C_6H_{12}O_6", 180),
               ("amoníaco", "NH_3", 17), ("hidróxido de sodio", "NaOH", 40), ("metano", "CH_4", 16), ("ácido sulfúrico", "H_2SO_4", 98)]


@plantilla(QUI, CIE)
def moles_desde_la_masa(rng):
    nombre, formula, masa_molar = rng.choice(_COMPUESTOS)
    moles = Fraction(rng.choice([1, 2, 3, 4, 5, 10])) / rng.choice([1, 2, 4, 10])
    masa = moles * masa_molar
    pide = rng.choice(["moles", "masa"])
    if pide == "moles":
        enunciado = f"La masa molar del {nombre} (${formula}$) es {masa_molar} g/mol. ¿Cuántos moles hay en ${tex(masa)}$ g de esta sustancia?"
        pasos = f"$n = \\frac{{m}}{{M}} = \\frac{{{tex(masa)}}}{{{masa_molar}}} = {tex(moles)}$ mol."
        cands = [(masa * masa_molar, "multiplica la masa por la masa molar"), (Fraction(masa_molar) / masa, "divide la masa molar por la masa"),
                 (moles * 10, "corre la coma un lugar"), (masa / 2, "divide la masa por 2")]
        return _armar(enunciado, moles, cands, pasos, lambda n: n * masa_molar == masa, "baja", "mol")
    enunciado = f"La masa molar del {nombre} (${formula}$) es {masa_molar} g/mol. ¿Qué masa tienen ${tex(moles)}$ mol de esta sustancia?"
    pasos = f"$m = n \\cdot M = {tex(moles)} \\cdot {masa_molar} = {tex(masa)}$ g."
    cands = [(Fraction(masa_molar) / moles, "divide la masa molar por los moles"), (moles / masa_molar, "divide los moles por la masa molar"),
             (Fraction(masa_molar) + moles, "suma la masa molar y los moles"), (masa * 2, "duplica el resultado")]
    return _armar(enunciado, masa, cands, pasos, lambda x: x == moles * masa_molar, "baja", "g")


@plantilla(QUI, CIE)
def concentracion_molar(rng):
    nombre, formula, masa_molar = rng.choice(_COMPUESTOS[2:])
    moles = Fraction(rng.choice([1, 2, 3, 4, 5])) / rng.choice([1, 2, 4, 10])
    volumen_ml = rng.choice([100, 200, 250, 500, 1000, 2000])
    v = Fraction(volumen_ml, 1000)
    molaridad = moles / v
    masa = moles * masa_molar
    enunciado = (f"Se disuelven ${tex(masa)}$ g de {nombre} (${formula}$, masa molar {masa_molar} g/mol) en agua hasta completar "
                 f"{volumen_ml} mL de solución. ¿Cuál es la concentración molar de la solución?")
    pasos = (f"Moles de soluto: $\\frac{{{tex(masa)}}}{{{masa_molar}}} = {tex(moles)}$ mol. Volumen: {volumen_ml} mL $= {tex(v)}$ L. "
             f"$M = \\frac{{{tex(moles)}}}{{{tex(v)}}} = {tex(molaridad)}$ mol/L.")
    cands = [(moles / volumen_ml, "usa el volumen en mililitros"), (masa / v, "usa la masa en vez de los moles"),
             (moles * v, "multiplica por el volumen en vez de dividir"), (moles, "olvida dividir por el volumen")]
    candidatos = [(c, e) for c, e in cands if c != molaridad]
    return _armar(enunciado, molaridad, candidatos, pasos, lambda x: x * v * masa_molar == masa, "media", "mol/L")


@plantilla(QUI, CIE)
def dilucion_de_una_solucion(rng):
    c1 = Fraction(rng.choice([1, 2, 3, 4, 5, 6]))
    v1 = Fraction(rng.choice([50, 100, 150, 200, 250]))
    factor = rng.choice([2, 4, 5, 10])
    v2 = v1 * factor
    c2 = c1 / factor
    pide = rng.choice(["concentracion", "agua"])
    if pide == "concentracion":
        enunciado = f"A {tex(v1)} mL de una solución {tex(c1)} mol/L se le agrega agua hasta completar {miles(int(v2))} mL. ¿Cuál es la nueva concentración?"
        pasos = f"Los moles de soluto no cambian: $C_1 V_1 = C_2 V_2$, luego $C_2 = \\frac{{{tex(c1)} \\cdot {tex(v1)}}}{{{tex(v2)}}} = {tex(c2)}$ mol/L."
        cands = [(c1 * factor, "multiplica la concentración en vez de dividirla"), (c1 * v1 / (v2 + v1), "suma los volúmenes, como si se agregara el volumen final"),
                 (c1 - c2, "resta las concentraciones"), (c1, "supone que la concentración no cambia")]
        return _armar(enunciado, c2, cands, pasos, lambda x: x * v2 == c1 * v1, "media", "mol/L")
    agua = v2 - v1
    enunciado = (f"Se quiere preparar una solución {tex(c2)} mol/L a partir de {tex(v1)} mL de una solución {tex(c1)} mol/L. ¿Cuántos mL de agua "
                 f"hay que agregar?")
    pasos = (f"$V_2 = \\frac{{C_1 V_1}}{{C_2}} = \\frac{{{tex(c1)} \\cdot {tex(v1)}}}{{{tex(c2)}}} = {tex(v2)}$ mL. Se agregan "
             f"${tex(v2)} - {tex(v1)} = {tex(agua)}$ mL de agua.")
    cands = [(v2, "responde el volumen final y no el agua agregada"), (v1 / factor, "divide el volumen en vez de multiplicarlo"),
             (v1 * (factor + 1), "suma un volumen inicial de más"), (v1, "agrega el mismo volumen inicial")]
    return _armar(enunciado, agua, [(c, e) for c, e in cands if c != agua], pasos, lambda x: c1 * v1 == c2 * (v1 + x), "alta", "mL")


@plantilla(QUI, CIE)
def porcentaje_masa_masa(rng):
    soluto = Fraction(rng.choice([2, 4, 5, 8, 10, 12, 15, 20, 25, 30]))
    solvente = Fraction(rng.choice([20, 40, 45, 50, 75, 80, 90, 100, 150, 200]))
    total = soluto + solvente
    porcentaje = soluto * 100 / total
    if porcentaje.denominator not in (1, 2, 4, 5, 10):
        raise Descartar
    sal = rng.choice(["sal", "azúcar", "sulfato de cobre", "bicarbonato de sodio"])
    enunciado = f"Se disuelven {tex(soluto)} g de {sal} en {tex(solvente)} g de agua. ¿Cuál es el porcentaje masa/masa (% m/m) de la solución?"
    pasos = (f"La masa de la solución es ${tex(soluto)} + {tex(solvente)} = {tex(total)}$ g. "
             f"$\\% \\, m/m = \\frac{{{tex(soluto)}}}{{{tex(total)}}} \\cdot 100 = {tex(porcentaje)}\\,\\%$.")
    cands = [(soluto * 100 / solvente, "divide por la masa del solvente en vez de la de la solución"), (soluto / total, "olvida multiplicar por 100"),
             (solvente * 100 / total, "calcula el porcentaje de agua"), (soluto * 100 / (total + soluto), "suma dos veces el soluto")]
    texto = lambda v: f"${tex(v)}\\,\\%$"
    distractores = [op(v, e, texto(v)) for v, e in _tres_distintos(porcentaje, cands)]
    return Propuesta(enunciado, op(porcentaje, None, texto(porcentaje)), distractores, pasos,
                     lambda x: x * (soluto + solvente) == soluto * 100, "baja")


_REACCIONES = [
    ("2H_2 + O_2 \\rightarrow 2H_2O", "hidrógeno", 2, 2, "agua", 2, 18),
    ("CH_4 + 2O_2 \\rightarrow CO_2 + 2H_2O", "metano", 1, 16, "dióxido de carbono", 1, 44),
    ("C + O_2 \\rightarrow CO_2", "carbono", 1, 12, "dióxido de carbono", 1, 44),
    ("2Mg + O_2 \\rightarrow 2MgO", "magnesio", 2, 24, "óxido de magnesio", 2, 40),
    ("N_2 + 3H_2 \\rightarrow 2NH_3", "nitrógeno", 1, 28, "amoníaco", 2, 17),
    ("CaCO_3 \\rightarrow CaO + CO_2", "carbonato de calcio", 1, 100, "óxido de calcio", 1, 56),
]


@plantilla(QUI, CIE)
def masa_de_producto_por_estequiometria(rng):
    ecuacion, reactivo, coef_r, m_r, producto, coef_p, m_p = rng.choice(_REACCIONES)
    moles_r = Fraction(rng.choice([1, 2, 3, 4, 5, 10]))
    masa_r = moles_r * m_r
    moles_p = moles_r * coef_p / coef_r
    masa_p = moles_p * m_p
    enunciado = (f"Considera la reacción balanceada ${ecuacion}$. Si reaccionan completamente {tex(masa_r)} g de {reactivo} "
                 f"(masa molar {m_r} g/mol) con suficiente del otro reactivo, ¿qué masa de {producto} (masa molar {m_p} g/mol) se forma?")
    pasos = (f"Moles de {reactivo}: $\\frac{{{tex(masa_r)}}}{{{m_r}}} = {tex(moles_r)}$ mol. La razón es {coef_r} : {coef_p}, así que se forman "
             f"${tex(moles_p)}$ mol de {producto}, es decir, ${tex(moles_p)} \\cdot {m_p} = {tex(masa_p)}$ g.")
    cands = [(moles_r * m_p, "ignora los coeficientes de la ecuación"), (masa_r, "supone que la masa del producto es igual a la del reactivo"),
             (moles_p, "responde los moles y no la masa"), (moles_r * m_p * coef_p * coef_r if coef_p * coef_r > 1 else masa_p * 2, "multiplica por los dos coeficientes")]
    return _armar(enunciado, masa_p, [(c, e) for c, e in cands if c != masa_p], pasos,
                  lambda x: x * coef_r == masa_r / m_r * coef_p * m_p, "alta", "g")

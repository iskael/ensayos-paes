"""Figuras en SVG para los ítems: trazo negro, relleno gris y rótulos en serif, al estilo de las pruebas oficiales."""
from __future__ import annotations

import html
import math

NEGRO = "#111111"
GRIS = "#d4d4d4"
GRIS_CLARO = "#ececec"
FUENTE = "DejaVu Serif, Georgia, serif"


class Lienzo:
    def __init__(self, xmin, xmax, ymin, ymax, ancho=360, margen=36):
        self.xmin, self.ymax, self.margen = xmin, ymax, margen
        self.k = (ancho - 2 * margen) / (xmax - xmin)
        self.ancho = ancho
        self.alto = round((ymax - ymin) * self.k + 2 * margen)
        self.elementos: list[str] = []

    def p(self, punto):
        x, y = punto
        return (round(self.margen + (x - self.xmin) * self.k, 2), round(self.margen + (self.ymax - y) * self.k, 2))

    def _trazo(self, grosor, punteada, color=NEGRO):
        guion = ' stroke-dasharray="5 4"' if punteada else ""
        return f'stroke="{color}" stroke-width="{grosor}"{guion} stroke-linecap="round" stroke-linejoin="round"'

    def linea(self, a, b, punteada=False, grosor=1.8, color=NEGRO):
        (x1, y1), (x2, y2) = self.p(a), self.p(b)
        self.elementos.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {self._trazo(grosor, punteada, color)}/>')

    def poligono(self, puntos, relleno="none", grosor=1.8, punteada=False):
        pts = " ".join(f"{x},{y}" for x, y in map(self.p, puntos))
        self.elementos.append(f'<polygon points="{pts}" fill="{relleno}" {self._trazo(grosor, punteada)}/>')

    def elipse(self, centro, rx, ry, relleno="none", grosor=1.8, punteada=False):
        cx, cy = self.p(centro)
        self.elementos.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{round(rx * self.k, 2)}" ry="{round(ry * self.k, 2)}" '
                              f'fill="{relleno}" {self._trazo(grosor, punteada)}/>')

    def circulo(self, centro, radio, relleno="none", grosor=1.8):
        self.elipse(centro, radio, radio, relleno, grosor)

    def media_elipse(self, centro, rx, ry, inferior=True, punteada=False, grosor=1.8):
        (x1, y1), (x2, _) = self.p((centro[0] - rx, centro[1])), self.p((centro[0] + rx, centro[1]))
        barrido = 0 if inferior else 1
        self.elementos.append(f'<path d="M {x1} {y1} A {round(rx * self.k, 2)} {round(ry * self.k, 2)} 0 0 {barrido} {x2} {y1}" '
                              f'fill="none" {self._trazo(grosor, punteada)}/>')

    def flecha(self, a, b, grosor=2.2):
        (x1, y1), (x2, y2) = self.p(a), self.p(b)
        angulo = math.atan2(y2 - y1, x2 - x1)
        largo, ancho = 11, 4.5
        bx, by = x2 - largo * math.cos(angulo), y2 - largo * math.sin(angulo)
        izq = (bx + ancho * math.sin(angulo), by - ancho * math.cos(angulo))
        der = (bx - ancho * math.sin(angulo), by + ancho * math.cos(angulo))
        self.elementos.append(f'<line x1="{x1}" y1="{y1}" x2="{round(bx, 2)}" y2="{round(by, 2)}" {self._trazo(grosor, False)}/>')
        self.elementos.append(f'<polygon points="{x2},{y2} {round(izq[0], 2)},{round(izq[1], 2)} {round(der[0], 2)},{round(der[1], 2)}" fill="{NEGRO}"/>')

    def punto(self, a, radio=3.4):
        x, y = self.p(a)
        self.elementos.append(f'<circle cx="{x}" cy="{y}" r="{radio}" fill="{NEGRO}"/>')

    def texto(self, a, contenido, dx=0, dy=0, ancla="middle", cursiva=False, tam=15, negrita=False):
        x, y = self.p(a)
        estilo = (' font-style="italic"' if cursiva else "") + (' font-weight="bold"' if negrita else "")
        self.elementos.append(f'<text x="{round(x + dx, 2)}" y="{round(y + dy, 2)}" text-anchor="{ancla}" font-family="{FUENTE}" '
                              f'font-size="{tam}"{estilo} fill="{NEGRO}">{html.escape(str(contenido))}</text>')

    def angulo_recto(self, vertice, hacia1, hacia2, lado=11):
        vx, vy = self.p(vertice)

        def unitario(destino):
            dx, dy = self.p(destino)[0] - vx, self.p(destino)[1] - vy
            n = math.hypot(dx, dy)
            return dx / n * lado, dy / n * lado

        (ax, ay), (bx, by) = unitario(hacia1), unitario(hacia2)
        self.elementos.append(f'<polyline points="{round(vx + ax, 2)},{round(vy + ay, 2)} {round(vx + ax + bx, 2)},{round(vy + ay + by, 2)} '
                              f'{round(vx + bx, 2)},{round(vy + by, 2)}" fill="none" {self._trazo(1.2, False)}/>')

    def svg(self) -> str:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.ancho} {self.alto}" width="{self.ancho}" height="{self.alto}">'
                f'<rect width="{self.ancho}" height="{self.alto}" fill="#ffffff"/>' + "".join(self.elementos) + "</svg>")


def _proporcion(a, b, minimo=0.45):
    """Escala dos medidas para dibujarlas sin que una quede aplastada; la figura es ilustrativa, no a escala."""
    mayor = max(a, b)
    return max(a / mayor, minimo), max(b / mayor, minimo)


def triangulo_rectangulo(base, altura, rotulo_base, rotulo_altura, rotulo_hipotenusa, muro=False):
    b, h = _proporcion(base, altura)
    b, h = b * 10, h * 10
    l = Lienzo(-2.6, b + 1.2, -1.6, h + 0.8)
    if muro:
        l.poligono([(-0.9, 0), (0, 0), (0, h + 0.5), (-0.9, h + 0.5)], relleno=GRIS, grosor=1.2)
        l.linea((-1.6, 0), (b + 0.9, 0), grosor=1.2)
    l.poligono([(0, 0), (b, 0), (0, h)])
    l.angulo_recto((0, 0), (b, 0), (0, h))
    l.texto((b / 2, 0), rotulo_base, dy=20)
    l.texto((0, h / 2), rotulo_altura, dx=-8 if not muro else -40, dy=5, ancla="end" if not muro else "middle")
    l.texto((b / 2, h / 2), rotulo_hipotenusa, dx=10, dy=-6, ancla="start")
    return l.svg()


def rectangulo(ancho, alto, rotulo_ancho, rotulo_alto, diagonal=None):
    a, h = _proporcion(ancho, alto)
    a, h = a * 10, h * 10
    l = Lienzo(-2.8, a + 0.8, -1.6, h + 0.6)
    l.poligono([(0, 0), (a, 0), (a, h), (0, h)], relleno=GRIS_CLARO)
    if diagonal is not None:
        l.linea((0, 0), (a, h), punteada=True)
        l.texto((a / 2, h / 2), diagonal, dx=-10, dy=-8, ancla="end", cursiva=True)
    l.texto((a / 2, 0), rotulo_ancho, dy=20)
    l.texto((0, h / 2), rotulo_alto, dx=-8, dy=5, ancla="end")
    return l.svg()


def circulo_con_medida(rotulo, tipo="radio"):
    l = Lienzo(-6, 6, -6, 6, ancho=280)
    l.circulo((0, 0), 5, relleno=GRIS_CLARO)
    l.punto((0, 0), 2.6)
    if tipo == "radio":
        l.linea((0, 0), (5, 0))
        l.texto((2.5, 0), rotulo, dy=-8)
    else:
        l.linea((-5, 0), (5, 0))
        l.texto((0, 0), rotulo, dy=-10)
    return l.svg()


def cuadrado_con_diagonal(rotulo_lado):
    l = Lienzo(-1.2, 11.5, -2, 10.8, ancho=300)
    l.poligono([(0, 0), (10, 0), (10, 10), (0, 10)], relleno=GRIS_CLARO)
    l.linea((0, 0), (10, 10), grosor=2.4)
    l.texto((5, 0), rotulo_lado, dy=20)
    l.texto((10, 5), rotulo_lado, dx=8, dy=5, ancla="start")
    l.texto((5, 5), "?", dx=-12, dy=-6, tam=17, negrita=True)
    return l.svg()


def cuadrado_con_esquinas(lado, m, n, rotulo_lado, rotulo_m, rotulo_n):
    escala = 10 / lado
    a, b = max(m * escala, 1.6), max(n * escala, 1.6)
    l = Lienzo(-1.2, 11.2, -2, 11.4, ancho=320)
    l.poligono([(0, 0), (10, 0), (10, 10), (0, 10)])
    for esquina, sx, sy, horizontal, vertical in [((0, 0), 1, 1, a, b), ((10, 0), -1, 1, b, a), ((10, 10), -1, -1, a, b), ((0, 10), 1, -1, b, a)]:
        l.poligono([esquina, (esquina[0] + sx * horizontal, esquina[1]), (esquina[0], esquina[1] + sy * vertical)], relleno=GRIS)
    l.texto((5, 0), rotulo_lado, dy=20)
    l.texto((b / 2, 10), rotulo_n, dy=-7, tam=13)
    l.texto((0, 10 - a / 2), rotulo_m, dx=-6, dy=4, ancla="end", tam=13)
    return l.svg()


def trapecio_rectangulo(base_menor, base_mayor, rotulo_menor, rotulo_mayor, rotulo_altura=None):
    menor = max(10 * base_menor / base_mayor, 3)
    l = Lienzo(-2.6, 10.8, -1.8, 7.4)
    l.poligono([(0, 0), (10, 0), (menor, 6), (0, 6)], relleno=GRIS_CLARO)
    l.angulo_recto((0, 0), (10, 0), (0, 6))
    l.texto((5, 0), rotulo_mayor, dy=20)
    l.texto((menor / 2, 6), rotulo_menor, dy=-8)
    if rotulo_altura:
        l.texto((0, 3), rotulo_altura, dx=-8, dy=5, ancla="end")
    return l.svg()


def plano_cartesiano(puntos=None, segmentos=(), vectores=(), recta=None, poligonos=(), cuadricula=True, proyecciones=True, rango=None,
                     curva=None, eje_vertical=None):
    """puntos: {rótulo: (x, y)}; vectores: [(inicio, fin, rótulo)]; poligonos: [(vértices, rótulo)]."""
    puntos = puntos or {}
    todos = list(puntos.values()) + [p for v in vectores for p in v[:2]] + [p for pol, _ in poligonos for p in pol] + [(0, 0)]
    if rango:
        xmin, xmax, ymin, ymax = rango
    else:
        xmin, xmax = min(x for x, _ in todos) - 1.5, max(x for x, _ in todos) + 1.5
        ymin, ymax = min(y for _, y in todos) - 1.5, max(y for _, y in todos) + 1.5
    l = Lienzo(xmin, xmax, ymin, ymax, ancho=360, margen=26)
    if cuadricula:
        for x in range(math.ceil(xmin), math.floor(xmax) + 1):
            l.linea((x, ymin), (x, ymax), grosor=0.6, color="#cfcfcf")
        for y in range(math.ceil(ymin), math.floor(ymax) + 1):
            l.linea((xmin, y), (xmax, y), grosor=0.6, color="#cfcfcf")
    l.flecha((xmin, 0), (xmax, 0), grosor=1.4)
    l.flecha((0, ymin), (0, ymax), grosor=1.4)
    l.texto((xmax, 0), "X", dx=-4, dy=18, tam=14)
    l.texto((0, ymax), "Y", dx=-14, dy=10, tam=14)
    marcas_x, marcas_y = set(), set()
    for vertices, rotulo in poligonos:
        l.poligono(vertices, relleno=GRIS)
        for x, y in vertices:
            marcas_x.add(x), marcas_y.add(y)
        cx = sum(x for x, _ in vertices) / len(vertices)
        cy = sum(y for _, y in vertices) / len(vertices)
        l.texto((cx, max(y for _, y in vertices)), rotulo, dy=-7, tam=12)
    if recta:
        (x1, y1), (x2, y2) = recta
        t0 = min((xmin - x1) / (x2 - x1), (xmax - x1) / (x2 - x1)) if x2 != x1 else 0
        t1 = max((xmin - x1) / (x2 - x1), (xmax - x1) / (x2 - x1)) if x2 != x1 else 1

        def recortar(t):
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

        candidatos = [t0, t1]
        if y2 != y1:
            candidatos += [(ymin - y1) / (y2 - y1), (ymax - y1) / (y2 - y1)]
        dentro = sorted(t for t in candidatos if xmin - 1e-9 <= recortar(t)[0] <= xmax + 1e-9 and ymin - 1e-9 <= recortar(t)[1] <= ymax + 1e-9)
        l.linea(recortar(dentro[0]), recortar(dentro[-1]), grosor=1.6)
    if eje_vertical is not None:
        l.linea((eje_vertical, ymin), (eje_vertical, ymax), punteada=True, grosor=1.3)
        marcas_x.add(eje_vertical)
    if curva:
        visibles = [p for p in curva if ymin <= p[1] <= ymax]
        for a, b in zip(visibles, visibles[1:]):
            l.linea(a, b, grosor=2)
    for a, b in segmentos:
        l.linea(a, b, grosor=2)
    for inicio, fin, rotulo in vectores:
        l.flecha(inicio, fin)
        mx, my = (inicio[0] + fin[0]) / 2, (inicio[1] + fin[1]) / 2
        if rotulo:
            l.texto((mx, my), rotulo, dx=-10, dy=-8, cursiva=True, negrita=True)
        for extremo in (inicio, fin):
            marcas_x.add(extremo[0]), marcas_y.add(extremo[1])
            if proyecciones:
                l.linea(extremo, (extremo[0], 0), punteada=True, grosor=1)
                l.linea(extremo, (0, extremo[1]), punteada=True, grosor=1)
    for rotulo, (x, y) in puntos.items():
        l.punto((x, y))
        l.texto((x, y), rotulo, dx=9, dy=-8, ancla="start", cursiva=True)
        marcas_x.add(x), marcas_y.add(y)
        if proyecciones:
            l.linea((x, y), (x, 0), punteada=True, grosor=1)
            l.linea((x, y), (0, y), punteada=True, grosor=1)
    for x in sorted(marcas_x - {0}):
        l.linea((x, -0.12), (x, 0.12), grosor=1.2)
        l.texto((x, 0), _num(x), dy=17, tam=12)
    for y in sorted(marcas_y - {0}):
        l.linea((-0.12, y), (0.12, y), grosor=1.2)
        l.texto((0, y), _num(y), dx=-7, dy=4, ancla="end", tam=12)
    return l.svg()


def _num(v) -> str:
    return str(v).replace("-", "−").replace(".", ",")


def cuadricula_con_objetos(columnas, filas, inicio, destino, unidades_por_casilla):
    """inicio y destino son casillas (columna, fila) contadas desde abajo a la izquierda, partiendo en 0."""
    l = Lienzo(-3.4, columnas + 1, -1.2, filas + 1, ancho=360, margen=22)
    for c in range(columnas + 1):
        l.linea((c, 0), (c, filas), grosor=1.1)
    for f in range(filas + 1):
        l.linea((0, f), (columnas, f), grosor=1.1)
    l.flecha((0, 0), (columnas + 0.8, 0), grosor=1.4)
    l.flecha((0, 0), (0, filas + 0.8), grosor=1.4)
    l.texto((columnas + 0.8, 0), "X", dy=17, tam=13)
    l.texto((0, filas + 0.8), "Y", dx=-12, dy=6, tam=13)
    l.punto((inicio[0] + 0.5, inicio[1] + 0.5), radio=6)
    l.texto((inicio[0] + 0.5, inicio[1] + 0.5), "P", dy=-10, tam=12, negrita=True)
    cx, cy = destino[0] + 0.5, destino[1] + 0.5
    estrella = []
    for i in range(10):
        radio = 0.36 if i % 2 == 0 else 0.15
        angulo = math.pi / 2 + i * math.pi / 5
        estrella.append((cx + radio * math.cos(angulo), cy + radio * math.sin(angulo)))
    l.poligono(estrella, relleno=NEGRO, grosor=1)
    l.texto((cx, cy), "T", dy=-14, tam=12, negrita=True)
    l.linea((-0.35, filas - 1), (-0.35, filas), grosor=1.2)
    l.linea((-0.5, filas - 1), (-0.2, filas - 1), grosor=1.2)
    l.linea((-0.5, filas), (-0.2, filas), grosor=1.2)
    l.texto((-0.6, filas - 0.5), f"{unidades_por_casilla} unidades" if unidades_por_casilla != 1 else "1 unidad", dy=4, ancla="end", tam=11)
    return l.svg()


def rosa_de_los_vientos():
    l = Lienzo(-6, 6, -4.4, 4.4, ancho=300, margen=20)
    l.flecha((-3.4, 0), (3.4, 0), grosor=1.6)
    l.flecha((3.4, 0), (-3.4, 0), grosor=1.6)
    l.flecha((0, -3), (0, 3), grosor=1.6)
    l.flecha((0, 3), (0, -3), grosor=1.6)
    l.texto((0, 3), "Norte (eje Y)", dy=-8, tam=13)
    l.texto((0, -3), "Sur", dy=18, tam=13)
    l.texto((3.4, 0), "Este (eje X)", dx=4, dy=-10, ancla="middle", tam=13)
    l.texto((-3.4, 0), "Oeste", dx=-4, dy=-10, ancla="middle", tam=13)
    return l.svg()


def caja(rotulo_frente, rotulo_fondo, rotulo_alto, alto=1.0, sin_tapa=False):
    a, h, f = 6.0, 6.0 * max(min(alto, 1.7), 0.55), 2.6
    l = Lienzo(-3.4, a + f + 2.6, -1.8, h + f * 0.7 + 0.8)
    dx, dy = f, f * 0.7
    l.poligono([(0, 0), (a, 0), (a, h), (0, h)], relleno=GRIS_CLARO)
    l.poligono([(a, 0), (a + dx, dy), (a + dx, h + dy), (a, h)], relleno=GRIS)
    l.poligono([(0, h), (a, h), (a + dx, h + dy), (dx, h + dy)], relleno="#ffffff" if sin_tapa else "#f6f6f6")
    if sin_tapa:
        l.linea((dx, h + dy), (dx, h + dy - 1.2), punteada=True, grosor=1)
    l.texto((a / 2, 0), rotulo_frente, dy=20)
    l.texto((a + dx / 2, dy / 2), rotulo_fondo, dx=12, dy=12, ancla="start")
    l.texto((0, h / 2), rotulo_alto, dx=-8, dy=5, ancla="end")
    return l.svg()


def cilindro(rotulo_radio, rotulo_alto, proporcion_alto=1.2):
    r, ry = 3.4, 0.9
    h = 3.4 * max(min(proporcion_alto, 2.2), 0.6) * 1.4
    l = Lienzo(-6.6, 6.6, -1.8, h + 1.6, ancho=300)
    l.poligono([(-r, 0), (r, 0), (r, h), (-r, h)], relleno=GRIS_CLARO, grosor=0.01)
    l.linea((-r, 0), (-r, h))
    l.linea((r, 0), (r, h))
    l.media_elipse((0, 0), r, ry, inferior=True)
    l.media_elipse((0, 0), r, ry, inferior=False, punteada=True, grosor=1.1)
    l.elipse((0, h), r, ry, relleno="#f6f6f6")
    l.punto((0, h), 2.4)
    l.linea((0, h), (r, h), grosor=1.4)
    l.texto((r / 2, h), rotulo_radio, dy=-6, tam=13)
    l.texto((r, h / 2), rotulo_alto, dx=10, dy=5, ancla="start")
    return l.svg()


def cono(rotulo_radio, rotulo_alto, proporcion_alto=1.2):
    r, ry = 3.4, 0.9
    h = 3.4 * max(min(proporcion_alto, 2.2), 1.1) * 1.4
    l = Lienzo(-6.6, 6.6, -2.2, h + 0.8, ancho=300)
    l.poligono([(-r, 0), (r, 0), (0, h)], relleno=GRIS_CLARO, grosor=0.01)
    l.linea((-r, 0), (0, h))
    l.linea((r, 0), (0, h))
    l.media_elipse((0, 0), r, ry, inferior=True)
    l.media_elipse((0, 0), r, ry, inferior=False, punteada=True, grosor=1.1)
    l.linea((0, 0), (0, h), punteada=True, grosor=1.2)
    l.linea((0, 0), (r, 0), punteada=True, grosor=1.2)
    l.angulo_recto((0, 0), (r, 0), (0, h), lado=8)
    l.texto((r / 2, -0.9), rotulo_radio, dy=20, tam=13)
    l.texto((0, h * 0.4), rotulo_alto, dx=7, dy=5, ancla="start", tam=13)
    return l.svg()


def cilindros_apilados(rotulo_radio_inferior, rotulo_radio_superior, rotulo_alto):
    R, r, ry, h = 4.2, 2.2, 0.9, 3.2
    l = Lienzo(-7.4, 7.4, -1.8, 2 * h + 1.6, ancho=320)
    l.poligono([(-R, 0), (R, 0), (R, h), (-R, h)], relleno=GRIS_CLARO, grosor=0.01)
    l.linea((-R, 0), (-R, h))
    l.linea((R, 0), (R, h))
    l.media_elipse((0, 0), R, ry, inferior=True)
    l.elipse((0, h), R, ry, relleno="#f6f6f6")
    l.poligono([(-r, h), (r, h), (r, 2 * h), (-r, 2 * h)], relleno=GRIS, grosor=0.01)
    l.linea((-r, h), (-r, 2 * h))
    l.linea((r, h), (r, 2 * h))
    l.media_elipse((0, h), r, ry * 0.6, inferior=True)
    l.elipse((0, 2 * h), r, ry * 0.6, relleno="#f6f6f6")
    l.linea((0, 2 * h), (r, 2 * h), grosor=1.3)
    l.texto((r / 2, 2 * h), rotulo_radio_superior, dy=-7, tam=12)
    l.linea((0, 0), (R, 0), punteada=True, grosor=1.2)
    l.texto((R / 2, 0), rotulo_radio_inferior, dy=-6, tam=12)
    l.texto((R, h / 2), rotulo_alto, dx=9, dy=5, ancla="start", tam=13)
    l.texto((r, 1.5 * h), rotulo_alto, dx=9, dy=5, ancla="start", tam=13)
    return l.svg()


def sombras(rotulo_poste, rotulo_sombra_poste, rotulo_sombra_objeto, nombre_objeto):
    l = Lienzo(-1, 21, -2.2, 10.6, ancho=380, margen=22)
    l.linea((-0.6, 0), (20.6, 0), grosor=1.2)
    l.poligono([(0, 0), (0, 3), (4, 0)], relleno=GRIS_CLARO)
    l.linea((0, 0), (0, 3), grosor=3)
    l.angulo_recto((0, 0), (4, 0), (0, 3), lado=8)
    l.texto((0, 1.5), rotulo_poste, dx=-6, dy=4, ancla="end", tam=12)
    l.texto((2, 0), rotulo_sombra_poste, dy=17, tam=12)
    l.poligono([(8, 0), (8, 9), (20, 0)], relleno=GRIS_CLARO)
    l.linea((8, 0), (8, 9), grosor=3)
    l.angulo_recto((8, 0), (20, 0), (8, 9), lado=8)
    l.texto((8, 4.5), "?", dx=-9, dy=5, ancla="end", tam=16, negrita=True)
    l.texto((14, 0), rotulo_sombra_objeto, dy=17, tam=12)
    l.texto((8, 9), nombre_objeto, dy=-7, tam=12)
    l.texto((0, 3), "poste", dy=-7, tam=12)
    return l.svg()


def rectangulo_con_borde(rotulo_ancho, rotulo_alto, rotulo_borde="x"):
    l = Lienzo(-0.6, 14.6, -0.6, 9.6, ancho=360, margen=18)
    l.poligono([(0, 0), (14, 0), (14, 9), (0, 9)])
    l.poligono([(2, 2), (12, 2), (12, 7), (2, 7)], relleno=GRIS)
    l.texto((7, 4.5), rotulo_ancho, dy=-4, tam=13)
    l.texto((7, 4.5), "×", dy=12, tam=12)
    l.texto((7, 4.5), rotulo_alto, dy=28, tam=13)
    for a, b in [((0, 4.5), (2, 4.5)), ((12, 4.5), (14, 4.5)), ((7, 0), (7, 2)), ((7, 7), (7, 9))]:
        l.linea(a, b, punteada=True, grosor=1.1)
    l.texto((1, 4.5), rotulo_borde, dy=-6, cursiva=True, tam=14)
    l.texto((13, 4.5), rotulo_borde, dy=-6, cursiva=True, tam=14)
    l.texto((7, 1), rotulo_borde, dx=9, dy=5, cursiva=True, tam=14)
    l.texto((7, 8), rotulo_borde, dx=9, dy=5, cursiva=True, tam=14)
    return l.svg()


def circulo_inscrito_en_cuadrado():
    l = Lienzo(-0.8, 10.8, -0.8, 10.8, ancho=260, margen=16)
    l.poligono([(0, 0), (10, 0), (10, 10), (0, 10)], relleno=GRIS_CLARO)
    l.circulo((5, 5), 5, relleno="#ffffff")
    return l.svg()


def poliomino(celdas):
    """celdas: conjunto de (columna, fila)."""
    columnas = max(c for c, _ in celdas) + 1
    filas = max(f for _, f in celdas) + 1
    lado = max(columnas, filas)
    l = Lienzo(-0.5, lado + 0.5, -0.5 - (lado - filas) / 2, filas + 0.5 + (lado - filas) / 2, ancho=280, margen=16)
    desplazamiento = (lado - columnas) / 2
    for c, f in sorted(celdas):
        x = c + desplazamiento
        l.poligono([(x, f), (x + 1, f), (x + 1, f + 1), (x, f + 1)], relleno=GRIS, grosor=1.5)
    return l.svg()


def grafico_de_barras(categorias, valores, titulo_x, titulo_y="Frecuencia"):
    n, maximo = len(categorias), max(valores)
    paso = 2.0
    alto = max(6.0, maximo * 0.5)
    l = Lienzo(-1.6, n * paso + 0.8, -1.9, alto + 1.4, ancho=360, margen=20)
    l.flecha((0, 0), (0, alto + 0.9), grosor=1.4)
    l.linea((0, 0), (n * paso + 0.4, 0), grosor=1.4)
    for i, (categoria, valor) in enumerate(zip(categorias, valores)):
        x = 0.5 + i * paso
        h = alto * valor / maximo
        l.poligono([(x, 0), (x + 1, 0), (x + 1, h), (x, h)], relleno=GRIS, grosor=1.4)
        l.texto((x + 0.5, 0), categoria, dy=16, tam=11)
    for valor in sorted(set(valores)):
        h = alto * valor / maximo
        l.linea((0, h), (n * paso, h), punteada=True, grosor=0.8)
        l.texto((0, h), valor, dx=-6, dy=4, ancla="end", tam=12)
    l.texto((0, 0), "0", dx=-6, dy=4, ancla="end", tam=12)
    l.texto((0, alto + 0.9), titulo_y, dx=4, dy=-8, ancla="start", tam=12)
    l.texto((n * paso / 2 + 0.2, 0), titulo_x, dy=36, tam=12)
    return l.svg()

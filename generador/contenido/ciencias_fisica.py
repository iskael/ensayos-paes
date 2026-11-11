"""Física conceptual: ondas y luz, mecánica, Tierra, electricidad. Las de cálculo están en plantillas_ciencias.py."""
from nucleo import fijo


def F(dificultad, enunciado, correcta, distractores, pasos):
    fijo("CIENCIAS", "fisica", dificultad, enunciado, correcta, distractores, pasos)


F("baja", "¿Cuál de las siguientes ondas electromagnéticas tiene la mayor frecuencia?",
  "Los rayos gamma",
  [("Las ondas de radio", "son las de menor frecuencia del espectro"),
   ("Las microondas", "tienen menor frecuencia que la luz visible"),
   ("La luz visible", "tiene menor frecuencia que los rayos X y gamma")],
  "En el espectro electromagnético la frecuencia crece de las ondas de radio a los rayos gamma, y la longitud de onda disminuye.")

F("media", "Todas las ondas electromagnéticas en el vacío tienen igual:",
  "rapidez de propagación",
  [("frecuencia", "la frecuencia distingue a las ondas del espectro"),
   ("longitud de onda", "la longitud de onda también cambia a lo largo del espectro"),
   ("energía por fotón", "la energía depende de la frecuencia")],
  "En el vacío todas viajan a la rapidez de la luz, cerca de 300.000 km/s; difieren en frecuencia y longitud de onda.")

F("media", "Una ambulancia se acerca con la sirena encendida. ¿Qué percibe una persona detenida en la vereda?",
  "Un sonido más agudo que el que percibiría si la ambulancia estuviera detenida",
  [("Un sonido más grave", "eso ocurre cuando la fuente se aleja"),
   ("El mismo tono, solo con más intensidad", "olvida el efecto Doppler"),
   ("Un sonido que viaja más rápido", "la rapidez del sonido depende del medio, no de la fuente")],
  "Por el efecto Doppler, si la fuente se acerca, las ondas llegan más juntas y la frecuencia percibida aumenta.")

F("media", "¿Qué tipo de espejo se usa en los retrovisores laterales de los autos para ampliar el campo de visión?",
  "Un espejo convexo",
  [("Un espejo cóncavo", "el cóncavo aumenta la imagen de objetos cercanos, pero reduce el campo"),
   ("Un espejo plano", "el plano no amplía el campo de visión"),
   ("Una lente convergente", "una lente refracta la luz, no la refleja")],
  "El espejo convexo forma imágenes virtuales, derechas y más pequeñas, y abarca un campo de visión mayor.")

F("media", "Un rayo de luz blanca atraviesa un prisma y se separa en colores. ¿Cómo se llama este fenómeno?",
  "Dispersión",
  [("Reflexión", "en la reflexión la luz rebota en una superficie"),
   ("Difracción", "la difracción ocurre al rodear un obstáculo o pasar por una rendija"),
   ("Interferencia", "la interferencia es la superposición de ondas")],
  "Cada color se refracta con un ángulo distinto porque el índice de refracción depende de la longitud de onda.")

F("baja", "Un libro está en reposo sobre una mesa. Según la tercera ley de Newton, ¿cuál es la reacción al peso del libro?",
  "La fuerza con que el libro atrae a la Tierra",
  [("La fuerza normal que la mesa ejerce sobre el libro", "la normal actúa sobre el mismo cuerpo: no es su par de acción y reacción"),
   ("La fuerza de roce de la mesa", "no hay roce si no hay tendencia al movimiento"),
   ("La fuerza que el libro ejerce sobre la mesa", "es la reacción de la normal, no del peso")],
  "El peso es la atracción de la Tierra sobre el libro; su reacción es la atracción del libro sobre la Tierra.")

F("media", "Un auto se mueve en línea recta con velocidad constante. ¿Qué se puede afirmar de la fuerza neta sobre él?",
  "Es cero",
  [("Apunta en el sentido del movimiento", "una fuerza neta lo aceleraría"),
   ("Es igual al peso del auto", "el peso se compensa con la normal"),
   ("Apunta en sentido contrario al movimiento", "lo frenaría")],
  "Por la primera ley de Newton, un cuerpo con velocidad constante tiene fuerza neta nula: la fuerza del motor compensa el roce.")

F("media", "Según la teoría de la tectónica de placas, ¿qué ocurre en un límite convergente entre una placa oceánica y una continental, como frente a Chile?",
  "La placa oceánica, más densa, se hunde bajo la continental (subducción)",
  [("Las placas se separan y se forma nuevo fondo marino", "eso ocurre en un límite divergente"),
   ("Las placas se deslizan lateralmente sin hundirse", "eso ocurre en un límite transformante"),
   ("La placa continental se hunde bajo la oceánica", "la continental es menos densa")],
  "La subducción de la placa de Nazca bajo la Sudamericana explica los sismos frecuentes y el volcanismo de Chile.")

F("media", "¿Qué evidencia apoyó la teoría de la deriva continental propuesta por Wegener?",
  "La coincidencia de fósiles y rocas en continentes hoy separados por océanos",
  [("La existencia de las estaciones del año", "se deben a la inclinación del eje terrestre"),
   ("Las mareas", "se deben principalmente a la atracción de la Luna"),
   ("La rotación de la Tierra", "no explica el movimiento de los continentes")],
  "El calce de las costas de África y Sudamérica y los mismos fósiles a ambos lados del Atlántico sugerían que estuvieron unidos.")

F("alta", "En una casa, ¿por qué los artefactos se conectan en paralelo y no en serie?",
  "Para que cada uno reciba el mismo voltaje y funcione aunque otro se apague",
  [("Para que todos compartan la misma corriente", "eso ocurre en serie"),
   ("Para que la resistencia total aumente", "en paralelo la resistencia equivalente disminuye"),
   ("Para que gasten menos energía en total", "la conexión no reduce la energía que consume cada uno")],
  "En paralelo todos quedan sometidos al voltaje de la red (220 V) y cada uno tiene su propio camino para la corriente.")

F("media", "¿Cuál es la función del disyuntor (automático) en una instalación eléctrica domiciliaria?",
  "Cortar la corriente cuando circula más de la permitida",
  [("Aumentar el voltaje de la red", "eso lo haría un transformador"),
   ("Medir la energía consumida", "esa es la función del medidor"),
   ("Convertir la corriente alterna en continua", "eso lo hace un rectificador")],
  "El disyuntor protege la instalación ante sobrecargas o cortocircuitos, que podrían calentar los cables.")

F("alta", "Dos ampolletas, una de 60 W y otra de 100 W, se conectan a la red de 220 V. ¿Cuál afirmación es correcta?",
  "Por la de 100 W circula más corriente",
  [("Por la de 60 W circula más corriente", "con igual voltaje, más potencia implica más corriente"),
   ("Ambas tienen igual resistencia", "la de 60 W tiene mayor resistencia"),
   ("La de 60 W consume más energía en el mismo tiempo", "consume menos, porque su potencia es menor")],
  "Como P = V · I y el voltaje es el mismo, la corriente es proporcional a la potencia: 100 W / 220 V es mayor que 60 W / 220 V.")

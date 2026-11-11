"""Química conceptual: materia, modelos atómicos, química orgánica, reacciones y soluciones."""
from nucleo import fijo


def Q(dificultad, enunciado, correcta, distractores, pasos):
    fijo("CIENCIAS", "quimica", dificultad, enunciado, correcta, distractores, pasos)


Q("baja", "¿Cuál de las siguientes es una mezcla homogénea?",
  "El agua con sal disuelta",
  [("El agua con aceite", "se distinguen dos fases: es heterogénea"),
   ("La arena con limaduras de hierro", "se distinguen sus componentes: es heterogénea"),
   ("El agua destilada", "es una sustancia pura, no una mezcla")],
  "En una mezcla homogénea (solución) no se distinguen los componentes; el agua salada es un ejemplo.")

Q("baja", "¿Qué método es el más adecuado para separar arena de agua?",
  "La filtración",
  [("La destilación", "sirve para separar líquidos miscibles o un sólido disuelto"),
   ("La imantación", "solo separa materiales magnéticos"),
   ("La cristalización", "sirve para recuperar un sólido disuelto")],
  "La arena no se disuelve en agua y queda retenida en el filtro, mientras el agua lo atraviesa.")

Q("media", "¿Qué aportó el modelo atómico de Rutherford?",
  "La existencia de un núcleo pequeño, denso y con carga positiva",
  [("Que los electrones están incrustados en una masa positiva", "ese es el modelo de Thomson"),
   ("Que los electrones giran en órbitas de energía definida", "ese es el aporte de Bohr"),
   ("Que el átomo es indivisible", "esa es la idea de Dalton")],
  "En el experimento de la lámina de oro, unas pocas partículas alfa rebotaban: la carga positiva estaba concentrada en un núcleo.")

Q("media", "Dos átomos tienen el mismo número atómico pero distinto número másico. ¿Qué son?",
  "Isótopos",
  [("Isóbaros", "los isóbaros tienen igual número másico"),
   ("Iones", "un ion tiene distinta cantidad de electrones que protones"),
   ("Isómeros", "isómero se refiere a moléculas con igual fórmula y distinta estructura")],
  "Los isótopos son átomos del mismo elemento (igual Z) con distinta cantidad de neutrones.")

Q("baja", "¿Qué partícula del átomo tiene carga negativa?",
  "El electrón",
  [("El protón", "el protón tiene carga positiva"),
   ("El neutrón", "el neutrón no tiene carga"),
   ("El núcleo", "el núcleo tiene carga positiva")],
  "El electrón tiene carga negativa y una masa mucho menor que la del protón y el neutrón.")

Q("media", "¿Cuántos enlaces covalentes forma habitualmente el átomo de carbono en los compuestos orgánicos?",
  "Cuatro",
  [("Dos", "el carbono tiene cuatro electrones de valencia"),
   ("Tres", "le faltaría un electrón para completar el octeto"),
   ("Uno", "eso es propio del hidrógeno")],
  "El carbono es tetravalente: comparte sus cuatro electrones de valencia y forma cuatro enlaces.")

Q("media", "¿Qué grupo funcional caracteriza a los alcoholes?",
  "El grupo hidroxilo (–OH)",
  [("El grupo carboxilo (–COOH)", "caracteriza a los ácidos carboxílicos"),
   ("El grupo carbonilo en un extremo (–CHO)", "caracteriza a los aldehídos"),
   ("El grupo amino (–NH₂)", "caracteriza a las aminas")],
  "Un alcohol tiene un grupo –OH unido a un carbono saturado, como el etanol, CH₃CH₂OH.")

Q("media", "¿Cuál es la fórmula general de los alcanos?",
  "CₙH₂ₙ₊₂",
  [("CₙH₂ₙ", "es la fórmula de los alquenos"),
   ("CₙH₂ₙ₋₂", "es la fórmula de los alquinos"),
   ("CₙHₙ", "no corresponde a una familia de hidrocarburos de cadena abierta")],
  "Los alcanos son hidrocarburos saturados de cadena abierta, con solo enlaces simples: metano CH₄, etano C₂H₆.")

Q("media", "¿Qué establece la ley de conservación de la masa de Lavoisier?",
  "En una reacción química, la masa total de los reactantes es igual a la de los productos",
  [("La masa de los productos siempre es mayor", "la masa no se crea"),
   ("Un compuesto tiene siempre la misma proporción en masa de sus elementos", "esa es la ley de las proporciones definidas de Proust"),
   ("Los gases reaccionan en volúmenes enteros", "esa es la ley de Gay-Lussac")],
  "En un sistema cerrado, la materia no se crea ni se destruye: solo se reordenan los átomos.")

Q("alta", "¿Qué factor aumenta, en general, la solubilidad de un sólido en agua?",
  "El aumento de la temperatura",
  [("La disminución de la temperatura", "en la mayoría de los sólidos la solubilidad baja con el frío"),
   ("El aumento de la presión", "la presión afecta sobre todo la solubilidad de los gases"),
   ("Agitar la solución", "agitar acelera la disolución, pero no cambia cuánto se puede disolver")],
  "Para la mayoría de los sólidos, más temperatura permite disolver más soluto; agitar o moler solo hace más rápido el proceso.")

Q("media", "Una solución se describe como 20 % m/v. ¿Qué significa?",
  "Que hay 20 g de soluto en 100 mL de solución",
  [("Que hay 20 g de soluto en 100 g de solución", "eso es 20 % m/m"),
   ("Que hay 20 mL de soluto en 100 mL de solución", "eso es 20 % v/v"),
   ("Que hay 20 g de soluto en 100 mL de solvente", "el porcentaje se refiere al volumen de la solución")],
  "El % m/v expresa gramos de soluto por cada 100 mL de solución.")

Q("alta", "En la reacción 2H₂ + O₂ → 2H₂O, ¿cuántas moléculas de oxígeno reaccionan con 10 moléculas de hidrógeno?",
  "5",
  [("10", "ignora los coeficientes de la ecuación"),
   ("20", "invierte la razón entre los coeficientes"),
   ("2", "usa el coeficiente del hidrógeno como resultado")],
  "La razón es 2 de H₂ por 1 de O₂: 10 de H₂ reaccionan con 5 de O₂ y forman 10 de H₂O.")

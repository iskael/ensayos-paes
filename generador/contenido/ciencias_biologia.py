"""Biología (módulo común y electivo): organización celular, procesos y funciones, herencia y evolución, organismo y ambiente."""
from nucleo import fijo


def B(dificultad, enunciado, correcta, distractores, pasos):
    fijo("CIENCIAS", "biologia", dificultad, enunciado, correcta, distractores, pasos)


# ---------------- Organización, estructura y actividad celular

B("baja", "¿Qué estructura celular está presente tanto en las células procariontes como en las eucariontes?",
  "Los ribosomas",
  [("El núcleo", "el núcleo delimitado por membrana es exclusivo de las eucariontes"),
   ("Las mitocondrias", "las procariontes no tienen organelos membranosos"),
   ("El retículo endoplasmático", "es un sistema de membranas propio de las eucariontes")],
  "Todas las células sintetizan proteínas, por eso todas tienen ribosomas; las procariontes carecen de núcleo y de organelos rodeados de membrana.")

B("baja", "¿Cuál es la función principal de las mitocondrias?",
  "Producir ATP mediante la respiración celular",
  [("Sintetizar proteínas a partir del ARN mensajero", "esa es la función de los ribosomas"),
   ("Realizar la fotosíntesis", "la fotosíntesis ocurre en los cloroplastos"),
   ("Degradar sustancias mediante enzimas digestivas", "esa es la función de los lisosomas")],
  "En la mitocondria ocurren el ciclo de Krebs y la cadena transportadora de electrones, que generan la mayor parte del ATP de la célula.")

B("media", "Una célula presenta pared celular, cloroplastos y una gran vacuola central. ¿A qué tipo de célula corresponde con mayor probabilidad?",
  "A una célula vegetal",
  [("A una célula animal", "las células animales no tienen pared celular ni cloroplastos"),
   ("A una bacteria", "las bacterias tienen pared, pero no cloroplastos ni vacuola central"),
   ("A un hongo", "los hongos tienen pared de quitina, pero no cloroplastos")],
  "Pared celular de celulosa, cloroplastos y vacuola central son, en conjunto, rasgos característicos de las células vegetales.")

B("media", "¿Qué organelo modifica, empaqueta y distribuye las proteínas que sintetiza el retículo endoplasmático rugoso?",
  "El complejo de Golgi",
  [("El lisosoma", "el lisosoma degrada sustancias; recibe enzimas desde el Golgi"),
   ("El nucléolo", "el nucléolo forma las subunidades de los ribosomas"),
   ("El peroxisoma", "el peroxisoma degrada peróxido de hidrógeno y ácidos grasos")],
  "Las proteínas pasan del retículo rugoso al complejo de Golgi, donde se modifican y se empaquetan en vesículas para su destino.")

B("media", "Se coloca un glóbulo rojo en una solución con una concentración de solutos mayor que la de su citoplasma. ¿Qué se espera que ocurra?",
  "La célula pierde agua y se arruga",
  [("La célula gana agua y se hincha hasta estallar", "eso ocurre en una solución hipotónica"),
   ("La célula no cambia, porque la membrana es impermeable al agua", "el agua atraviesa la membrana por osmosis"),
   ("Los solutos entran a la célula por osmosis", "la osmosis es el paso del agua, no de los solutos")],
  "En un medio hipertónico el agua sale de la célula por osmosis, desde donde hay menos solutos hacia donde hay más, y la célula se arruga (crenación).")

B("alta", "Una sustancia entra a la célula en contra de su gradiente de concentración. ¿Qué tipo de transporte se utiliza?",
  "Transporte activo, con gasto de ATP",
  [("Difusión simple", "la difusión ocurre a favor del gradiente"),
   ("Difusión facilitada por proteínas canal", "también ocurre a favor del gradiente, sin gasto de energía"),
   ("Osmosis", "la osmosis es el movimiento del agua a favor de su gradiente")],
  "Mover una sustancia desde donde hay menos hacia donde hay más concentración requiere energía: es transporte activo, como la bomba sodio-potasio.")

B("media", "¿Cuál de los siguientes componentes forma la estructura básica de la membrana plasmática?",
  "Una bicapa de fosfolípidos con proteínas incluidas",
  [("Una capa de celulosa", "la celulosa forma la pared de las células vegetales, no la membrana"),
   ("Una doble capa de proteínas sin lípidos", "el modelo de mosaico fluido se basa en una bicapa lipídica"),
   ("Una capa de ADN y ARN", "los ácidos nucleicos no forman la membrana")],
  "Según el modelo de mosaico fluido, la membrana es una bicapa de fosfolípidos con proteínas integrales y periféricas.")

B("baja", "¿Qué molécula almacena la información genética en las células?",
  "El ADN",
  [("El ATP", "el ATP transporta energía"),
   ("La glucosa", "la glucosa es una fuente de energía"),
   ("El colesterol", "el colesterol es un lípido de la membrana")],
  "El ADN contiene los genes; su secuencia de nucleótidos codifica la información para sintetizar proteínas.")

# ---------------- Procesos y funciones biológicas: reproducción, ciclo celular, meiosis

B("media", "¿En qué etapa del ciclo celular se duplica el ADN?",
  "En la fase S de la interfase",
  [("En la profase de la mitosis", "en la profase el ADN ya está duplicado y se condensa"),
   ("En la fase G1", "en G1 la célula crece, pero aún no replica su ADN"),
   ("En la citocinesis", "en la citocinesis se divide el citoplasma")],
  "La interfase tiene tres fases: G1 (crecimiento), S (síntesis o replicación del ADN) y G2 (preparación para la división).")

B("media", "Una célula humana con 46 cromosomas realiza mitosis. ¿Cuántos cromosomas tiene cada célula hija?",
  "46",
  [("23", "confunde la mitosis con la meiosis"),
   ("92", "suma los cromosomas duplicados como si fueran independientes"),
   ("46 en una y 0 en la otra", "la mitosis reparte el material genético en partes iguales")],
  "La mitosis produce dos células genéticamente idénticas a la original, con el mismo número de cromosomas (2n = 46).")

B("media", "¿Cuál es una diferencia entre la mitosis y la meiosis?",
  "La meiosis produce células haploides y genéticamente distintas entre sí",
  [("La mitosis ocurre solo en las células sexuales", "la mitosis ocurre en las células somáticas"),
   ("La meiosis tiene una sola división celular", "la meiosis tiene dos divisiones sucesivas"),
   ("La mitosis produce cuatro células hijas", "la mitosis produce dos células hijas")],
  "La meiosis tiene dos divisiones, reduce el número de cromosomas a la mitad y, por el entrecruzamiento y la segregación al azar, genera variabilidad.")

B("alta", "¿En qué etapa de la meiosis ocurre el entrecruzamiento (crossing-over) entre cromosomas homólogos?",
  "En la profase I",
  [("En la metafase II", "en la meiosis II se separan cromátidas, sin homólogos apareados"),
   ("En la anafase I", "en la anafase I los homólogos ya se separan"),
   ("En la interfase", "en la interfase los homólogos no están apareados")],
  "En la profase I los cromosomas homólogos se aparean y forman bivalentes, momento en que intercambian segmentos de cromátidas.")

B("media", "En el ciclo menstrual, ¿qué hormona alcanza un peak que desencadena la ovulación?",
  "La hormona luteinizante (LH)",
  [("La progesterona", "la progesterona aumenta después de la ovulación, producida por el cuerpo lúteo"),
   ("La oxitocina", "la oxitocina participa en el parto y la lactancia"),
   ("La insulina", "la insulina regula la glucosa en la sangre")],
  "Hacia la mitad del ciclo, un aumento brusco de LH provoca la liberación del ovocito desde el folículo maduro.")

B("media", "¿Qué estructura del ovario produce progesterona después de la ovulación?",
  "El cuerpo lúteo",
  [("El endometrio", "el endometrio es la capa interna del útero, que responde a la progesterona"),
   ("La hipófisis", "la hipófisis produce FSH y LH"),
   ("La trompa de Falopio", "en la trompa ocurre normalmente la fecundación")],
  "Tras la ovulación, el folículo se transforma en cuerpo lúteo, que secreta progesterona y mantiene el endometrio preparado.")

B("baja", "¿Dónde ocurre normalmente la fecundación en la especie humana?",
  "En la trompa de Falopio",
  [("En el útero", "el embrión se implanta en el útero, pero la fecundación ocurre antes"),
   ("En el ovario", "el ovario libera el ovocito, que luego es captado por la trompa"),
   ("En la vagina", "los espermatozoides deben recorrer el útero hasta la trompa")],
  "El ovocito liberado es captado por la trompa de Falopio, donde suele encontrarse con los espermatozoides.")

B("media", "¿Cuál de los siguientes métodos de control de la natalidad protege además de las infecciones de transmisión sexual?",
  "El preservativo",
  [("La píldora anticonceptiva", "es un método hormonal: no forma una barrera contra microorganismos"),
   ("El dispositivo intrauterino", "impide el embarazo, pero no evita el contagio"),
   ("El método del calendario", "es un método natural, sin barrera")],
  "Solo los métodos de barrera, como el preservativo, impiden el contacto con fluidos que transmiten infecciones.")

B("media", "¿Qué tipo de microorganismo causa el sida?",
  "Un virus",
  [("Una bacteria", "las bacterias causan otras ITS, como la sífilis o la gonorrea"),
   ("Un hongo", "los hongos causan, por ejemplo, la candidiasis"),
   ("Un protozoo", "los protozoos causan la tricomoniasis")],
  "El sida es causado por el virus de inmunodeficiencia humana (VIH), que destruye linfocitos T del sistema inmune.")

B("alta", "Un gameto humano normal, ¿cuántos cromosomas tiene?",
  "23",
  [("46", "esa es la cantidad de una célula somática diploide"),
   ("22", "olvida el cromosoma sexual"),
   ("92", "duplica la cantidad diploide")],
  "Los gametos son haploides (n): tienen 22 autosomas y un cromosoma sexual, en total 23.")

# ---------------- Procesos y funciones: sistema nervioso, hormonal, homeostasis

B("media", "¿Qué hormona disminuye la concentración de glucosa en la sangre?",
  "La insulina",
  [("El glucagón", "el glucagón la aumenta"),
   ("La adrenalina", "la adrenalina aumenta la glucosa disponible"),
   ("El cortisol", "el cortisol eleva la glucosa en la sangre")],
  "El páncreas libera insulina tras comer: favorece que las células capten glucosa y que el hígado la almacene como glucógeno.")

B("media", "¿Qué tipo de regulación mantiene la temperatura corporal cerca de un valor constante?",
  "La retroalimentación negativa",
  [("La retroalimentación positiva", "la positiva amplifica el cambio, como en el parto"),
   ("La herencia ligada al sexo", "no es un mecanismo de regulación fisiológica"),
   ("La selección natural", "actúa sobre poblaciones a lo largo de generaciones")],
  "En la retroalimentación negativa, una desviación del valor normal activa respuestas que la contrarrestan, como sudar cuando sube la temperatura.")

# ---------------- Herencia y evolución

B("media", "En una planta, el color púrpura (P) es dominante sobre el blanco (p). ¿Qué proporción de la descendencia de un cruce Pp × Pp se espera que sea blanca?",
  "1/4",
  [("1/2", "confunde la proporción con la de un cruce Pp × pp"),
   ("3/4", "responde la proporción de plantas púrpura"),
   ("0", "olvida que dos heterocigotos pueden aportar el alelo recesivo")],
  "El cuadro de Punnett da PP, Pp, Pp y pp: solo pp (1 de 4) muestra el fenotipo recesivo blanco.")

B("media", "Un individuo de genotipo Aa, ¿qué es respecto de ese gen?",
  "Heterocigoto",
  [("Homocigoto dominante", "un homocigoto dominante sería AA"),
   ("Homocigoto recesivo", "un homocigoto recesivo sería aa"),
   ("Haploide", "un haploide tiene un solo alelo de cada gen")],
  "Un heterocigoto porta dos alelos distintos del mismo gen.")

B("alta", "El daltonismo es una característica recesiva ligada al cromosoma X. Una mujer portadora tiene hijos con un hombre de visión normal. ¿Qué probabilidad tiene un hijo varón de ser daltónico?",
  "1/2",
  [("1/4", "calcula la probabilidad sobre todos los hijos y no solo sobre los varones"),
   ("0", "supone que el padre debe ser daltónico"),
   ("1", "supone que todo hijo de madre portadora es daltónico")],
  "Los hijos varones reciben su único X de la madre (XᴰXᵈ): la mitad recibe Xᵈ y es daltónica.")

B("media", "¿Qué aporte hizo Gregor Mendel a la biología?",
  "Describió cómo se heredan los caracteres a partir de experimentos con arvejas",
  [("Propuso la selección natural como mecanismo de evolución", "ese fue el aporte de Darwin y Wallace"),
   ("Describió la estructura de doble hélice del ADN", "eso lo hicieron Watson y Crick con datos de Franklin"),
   ("Propuso la herencia de los caracteres adquiridos", "esa idea es de Lamarck")],
  "Mendel cruzó variedades de arveja y dedujo que los caracteres se transmiten mediante factores (hoy genes) que se segregan.")

B("media", "¿Cuál de las siguientes ideas corresponde a la teoría de Lamarck?",
  "Los caracteres adquiridos por el uso o desuso de un órgano se heredan",
  [("Los individuos con variaciones ventajosas dejan más descendencia", "esa es la idea de selección natural de Darwin y Wallace"),
   ("Las especies no cambian a lo largo del tiempo", "Lamarck sí planteaba que las especies cambian"),
   ("Las mutaciones al azar originan la variabilidad", "es un aporte posterior de la genética")],
  "Lamarck proponía que los órganos se desarrollan con el uso y que esos cambios se transmiten a la descendencia; hoy se sabe que no es así.")

B("alta", "Una población de bacterias se expone a un antibiótico y, tras varias generaciones, la mayoría es resistente. ¿Cuál es la mejor explicación?",
  "Las pocas bacterias que ya eran resistentes sobrevivieron y se reprodujeron",
  [("El antibiótico provocó en cada bacteria la resistencia que necesitaba", "las mutaciones no ocurren por necesidad"),
   ("Las bacterias aprendieron a resistir el antibiótico", "las bacterias no aprenden; cambia la frecuencia de los genes"),
   ("El antibiótico perdió su efecto con el tiempo", "el antibiótico es el mismo; cambió la población")],
  "Es selección natural: la variación preexistente hace que algunas sobrevivan, y su descendencia hereda la resistencia.")

B("media", "¿Cuál de las siguientes es una evidencia de la evolución biológica?",
  "Las estructuras homólogas, como las extremidades de los mamíferos",
  [("La generación espontánea de la vida", "fue refutada por Pasteur"),
   ("La fijeza de las especies", "es una idea contraria a la evolución"),
   ("La herencia de las cicatrices", "los caracteres adquiridos no se heredan")],
  "Las estructuras homólogas comparten un origen común aunque cumplan funciones distintas; junto a los fósiles y la biología molecular son evidencia de evolución.")

B("alta", "¿Qué técnica permite insertar un gen humano en una bacteria para que esta produzca, por ejemplo, insulina?",
  "La tecnología del ADN recombinante",
  [("La clonación por transferencia nuclear", "sirve para obtener individuos genéticamente idénticos"),
   ("La selección artificial", "selecciona individuos, pero no inserta genes de otra especie"),
   ("La fermentación", "es un proceso metabólico, no una técnica de manipulación genética")],
  "Con enzimas de restricción y ligasas se inserta el gen en un plásmido que luego se introduce en la bacteria.")

B("media", "¿Qué es una mutación?",
  "Un cambio en la secuencia del material genético",
  [("La expresión de un alelo dominante", "es parte de la herencia normal, no un cambio en el ADN"),
   ("El intercambio de genes entre especies por cruzamiento", "no es la definición de mutación"),
   ("Un cambio del fenotipo causado solo por el ambiente", "un cambio ambiental no altera el ADN")],
  "Las mutaciones son cambios en el ADN; son la fuente original de la variabilidad genética.")

# ---------------- Organismo y ambiente

B("baja", "¿En qué organelo de las células vegetales ocurre la fotosíntesis?",
  "En el cloroplasto",
  [("En la mitocondria", "en la mitocondria ocurre la respiración celular"),
   ("En la vacuola", "la vacuola almacena agua y sustancias"),
   ("En el núcleo", "el núcleo contiene el material genético")],
  "Los cloroplastos contienen clorofila, que capta la energía lumínica para sintetizar glucosa.")

B("media", "¿Cuáles son los reactantes de la fotosíntesis?",
  "Dióxido de carbono y agua",
  [("Glucosa y oxígeno", "son los productos de la fotosíntesis"),
   ("Oxígeno y agua", "el oxígeno es un producto, no un reactante"),
   ("Glucosa y dióxido de carbono", "la glucosa se produce, no se consume")],
  "La ecuación global es 6CO₂ + 6H₂O + luz → C₆H₁₂O₆ + 6O₂.")

B("media", "En una cadena trófica, ¿qué ocurre con la energía al pasar de un nivel al siguiente?",
  "Solo una fracción pasa al nivel siguiente; el resto se pierde principalmente como calor",
  [("Se transfiere completa al nivel siguiente", "en cada nivel se gasta energía en la respiración"),
   ("Aumenta en cada nivel", "la energía disponible disminuye hacia los consumidores superiores"),
   ("Se recicla y vuelve a los productores", "la materia se recicla; la energía fluye en una sola dirección")],
  "Cerca de un 10 % de la energía de un nivel queda disponible para el siguiente; por eso las cadenas tróficas tienen pocos eslabones.")

B("media", "En la cadena trófica pasto → conejo → zorro → puma, ¿qué nivel trófico ocupa el zorro?",
  "Consumidor secundario",
  [("Consumidor primario", "el consumidor primario es el conejo, que come pasto"),
   ("Productor", "el productor es el pasto"),
   ("Consumidor terciario", "el consumidor terciario es el puma")],
  "El productor (pasto) es comido por el consumidor primario (conejo), y este por el secundario (zorro).")

B("media", "¿Qué organismos cumplen la función de descomponedores en un ecosistema?",
  "Hongos y bacterias",
  [("Plantas y algas", "son productores"),
   ("Herbívoros", "son consumidores primarios"),
   ("Carnívoros", "son consumidores secundarios o terciarios")],
  "Los descomponedores degradan la materia orgánica muerta y devuelven nutrientes inorgánicos al suelo.")

B("alta", "Un estudiante quiere saber si la intensidad de la luz afecta la tasa de fotosíntesis de una planta acuática. ¿Cuál es la variable independiente del experimento?",
  "La intensidad de la luz",
  [("La cantidad de burbujas de oxígeno liberadas", "es la variable dependiente, la que se mide"),
   ("La especie de la planta", "debe mantenerse constante: es una variable controlada"),
   ("La temperatura del agua", "debe controlarse para no afectar el resultado")],
  "La variable independiente es la que el investigador modifica; la dependiente es la que mide como respuesta.")

B("media", "¿Qué proceso libera dióxido de carbono a la atmósfera en el ciclo del carbono?",
  "La respiración celular",
  [("La fotosíntesis", "la fotosíntesis capta CO₂ de la atmósfera"),
   ("La fijación de nitrógeno", "pertenece al ciclo del nitrógeno"),
   ("La transpiración de las plantas", "libera vapor de agua")],
  "Los seres vivos oxidan la materia orgánica en la respiración y liberan CO₂; la combustión también lo libera.")

B("alta", "Un investigador observa que en un lago aumentan las algas después de que se vierten fertilizantes. ¿Qué conclusión se puede inferir con mayor fundamento?",
  "Los nutrientes de los fertilizantes favorecen el crecimiento de las algas",
  [("Los fertilizantes son tóxicos para las algas", "el resultado muestra lo contrario"),
   ("Las algas producen fertilizantes", "confunde la causa con el efecto"),
   ("La temperatura del lago aumentó por los fertilizantes", "no hay datos sobre la temperatura")],
  "El aumento de algas por exceso de nitrógeno y fósforo se llama eutrofización; una conclusión debe basarse en los datos observados.")

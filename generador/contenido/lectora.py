"""Competencia Lectora: textos originales, cada uno con cinco preguntas ordenadas (habilidades localizar, interpretar y evaluar).

Los textos son propios (no se reproduce material del DEMRE). Los párrafos se separan con una línea en blanco: la app los
numera, así que las preguntas pueden referirse a «el párrafo 2».
"""
from nucleo import Estimulo, fijo


def texto(clave, titulo, cuerpo, fuente, preguntas):
    est = Estimulo(f"cl-{clave}", titulo, cuerpo.strip(), fuente)
    for orden, (eje, dificultad, enunciado, correcta, distractores, pasos) in enumerate(preguntas, start=1):
        fijo("CL", eje, dificultad, enunciado, correcta, distractores, pasos, estimulo=est, orden=orden)


LOC, INT, EVA = "localizar", "interpretar", "evaluar"

texto("abejas-urbanas", "Abejas en la ciudad", """
En los últimos diez años, varias municipalidades de Santiago han instalado colmenas en techos de edificios públicos y en plazas cerradas al tránsito. La idea, que al principio despertó desconfianza entre los vecinos, nació de una constatación preocupante: las poblaciones de abejas melíferas y de abejas nativas han disminuido en buena parte del país, y con ellas la polinización de huertos, árboles frutales y plantas silvestres.

Contra lo que podría pensarse, la ciudad no es un mal lugar para estos insectos. Los parques, los jardines particulares y el arbolado de las calles ofrecen una floración más variada y prolongada que la de muchos campos dedicados a un solo cultivo. Además, en las zonas urbanas se usan menos plaguicidas que en la agricultura intensiva, una de las principales causas de la mortandad de colmenas.

Sin embargo, los especialistas advierten que la apicultura urbana no es una solución por sí sola. Una colmena de abejas melíferas puede albergar a decenas de miles de individuos que compiten por el néctar con las cerca de cuatrocientas especies de abejas nativas que habitan en Chile, la mayoría solitarias y menos visibles. Si se instalan demasiadas colmenas en un barrio con pocas flores, las nativas pueden salir perjudicadas.

Por eso, los programas más recientes combinan las colmenas con «corredores de flores»: franjas de plantas nativas sembradas en bandejones, colegios y sitios eriazos. Estas plantas, adaptadas al clima seco, requieren poco riego y florecen en distintas épocas del año, lo que asegura alimento para insectos muy diversos. La meta, dicen sus impulsores, no es tener más miel, sino una ciudad donde quepan muchas formas de vida.
""", "Texto elaborado para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿cuál es una de las principales causas de la mortandad de colmenas?",
     "El uso de plaguicidas en la agricultura intensiva",
     [("La falta de techos disponibles en los edificios públicos", "el texto menciona los techos como lugar de instalación, no como causa de mortandad"),
      ("La competencia con las abejas nativas", "la competencia perjudica a las nativas, no a las colmenas"),
      ("La desconfianza de los vecinos", "es una reacción ante las colmenas, no una causa de su muerte")],
     "El párrafo 2 dice que en la ciudad se usan menos plaguicidas que en la agricultura intensiva, «una de las principales causas de la mortandad de colmenas»."),
    (INT, "media", "¿Qué función cumple el párrafo 3 en el texto?",
     "Introducir una advertencia que matiza los beneficios de la apicultura urbana",
     [("Explicar por qué la ciudad es un buen lugar para las abejas", "eso lo hace el párrafo 2"),
      ("Describir el origen de los programas de colmenas", "el origen se explica en el párrafo 1"),
      ("Proponer la solución que adoptan los programas recientes", "la solución se presenta en el párrafo 4")],
     "El párrafo 3 comienza con «Sin embargo» y plantea un riesgo: demasiadas colmenas pueden perjudicar a las abejas nativas."),
    (INT, "media", "En el contexto del párrafo 1, la expresión «despertó desconfianza» significa que la idea:",
     "generó dudas o recelo",
     [("provocó entusiasmo inmediato", "es lo contrario de la desconfianza"),
      ("fue rechazada por las autoridades", "el texto habla de los vecinos, no de las autoridades"),
      ("pasó inadvertida", "si despertó desconfianza, sí fue notada")],
     "Desconfiar es dudar de algo; la idea «al principio» generó recelo entre los vecinos."),
    (INT, "alta", "¿Cuál es la idea principal del texto?",
     "La apicultura urbana puede ayudar a los polinizadores si se acompaña de flores nativas que también beneficien a las abejas silvestres",
     [("La ciudad es el mejor lugar para producir miel en Chile", "el texto dice que la meta no es tener más miel"),
      ("Las abejas melíferas deben reemplazar a las nativas en las ciudades", "el texto advierte justamente contra perjudicar a las nativas"),
      ("Los plaguicidas son la única causa de la disminución de las abejas", "es una de las causas, no la única")],
     "El texto presenta el problema, el valor de la ciudad, un riesgo y la solución combinada; la idea que integra todo es la del corredor de flores junto a las colmenas."),
    (EVA, "alta", "¿Cuál de las siguientes situaciones sería coherente con lo que proponen los impulsores de los corredores de flores?",
     "Un colegio siembra plantas nativas de floración escalonada en su patio",
     [("Un barrio con pocas flores instala veinte colmenas nuevas", "el texto advierte que eso puede perjudicar a las nativas"),
      ("Una municipalidad riega a diario pasto ornamental en sus bandejones", "las plantas propuestas son nativas y de poco riego"),
      ("Una empresa reemplaza un sitio eriazo por un monocultivo de flores", "el texto valora la variedad de plantas, no un solo cultivo")],
     "Aplicar el texto a una nueva situación: los corredores son franjas de plantas nativas, de poco riego y que florecen en distintas épocas."),
])

texto("carta-biblioteca", "Carta al director: la biblioteca del barrio", """
Señor director:

Hace unas semanas se anunció que la biblioteca pública de nuestro barrio reducirá su horario de atención a tres días por semana, por falta de presupuesto. Quiero expresar mi preocupación, no solo como vecina, sino como madre de dos estudiantes que han encontrado allí lo que no tienen en casa: silencio, conexión a internet y alguien dispuesto a ayudarlos a buscar información.

Se suele decir que en la era digital las bibliotecas están de más, porque «todo está en internet». Quienes afirman esto olvidan que no todos los hogares tienen un computador ni un espacio tranquilo para estudiar. En la sala de lectura de nuestra biblioteca, cada tarde, se sientan escolares que comparten un único celular con sus hermanos, adultos mayores que aprenden a hacer trámites en línea y personas que buscan trabajo.

Reconozco que los recursos municipales son limitados y que hay otras necesidades urgentes. Pero recortar el horario de la biblioteca es una economía mal entendida: el ahorro es pequeño y el daño recae precisamente sobre quienes tienen menos alternativas. Existen otras posibilidades, como convenios con universidades para que estudiantes en práctica apoyen la atención, o el uso compartido del edificio con talleres que paguen un arriendo.

Invito a las autoridades a conversar con los usuarios antes de tomar una decisión definitiva. Una biblioteca abierta no es un lujo: es una de las pocas puertas que siguen abiertas para todos.

Carolina Fuentes, vecina de la comuna
""", "Carta ficticia elaborada para este ensayo.", [
    (LOC, "baja", "¿Qué medida motiva la carta?",
     "La reducción del horario de la biblioteca a tres días por semana",
     [("El cierre definitivo de la biblioteca", "se reduce el horario, no se cierra"),
      ("La falta de internet en la biblioteca", "la biblioteca sí ofrece conexión"),
      ("Un convenio con universidades", "es una alternativa que propone la autora")],
     "El párrafo 2 informa que la biblioteca «reducirá su horario de atención a tres días por semana»."),
    (INT, "media", "¿Con qué propósito la autora menciona a los escolares, los adultos mayores y las personas que buscan trabajo?",
     "Para mostrar que la biblioteca atiende necesidades que internet en casa no resuelve para todos",
     [("Para criticar que esas personas no tengan computador", "no critica a los usuarios"),
      ("Para demostrar que la biblioteca está siempre llena", "no se refiere a la cantidad de público"),
      ("Para pedir que se construya una biblioteca más grande", "no pide un edificio nuevo")],
     "Los ejemplos refutan la idea de que «todo está en internet»: muestran a quienes no tienen otras alternativas."),
    (INT, "media", "En el párrafo 4, la expresión «una economía mal entendida» se refiere a que el recorte:",
     "ahorra poco y causa un perjuicio mayor",
     [("es un error de cálculo del presupuesto", "no se discute el cálculo, sino el costo social"),
      ("demuestra que la municipalidad no tiene dinero", "la autora reconoce la falta de recursos, pero ese no es el sentido de la expresión"),
      ("beneficia a las personas de menos recursos", "es lo contrario de lo que plantea")],
     "La autora explica a continuación: «el ahorro es pequeño y el daño recae precisamente sobre quienes tienen menos alternativas»."),
    (EVA, "media", "¿Qué actitud adopta la autora frente a las autoridades?",
     "Crítica, pero dispuesta al diálogo y a proponer soluciones",
     [("Indiferente, porque cree que nada cambiará", "pide conversar antes de la decisión"),
      ("Agresiva, porque exige su renuncia", "no pide renuncias"),
      ("Conformista, porque acepta la medida sin objeciones", "se opone a la medida")],
     "Reconoce que los recursos son limitados, propone alternativas y las invita a conversar con los usuarios."),
    (EVA, "alta", "¿Cuál de los siguientes recursos usa la autora para reforzar su argumento en el párrafo 3?",
     "Presenta y refuta una opinión contraria muy difundida",
     [("Cita estadísticas oficiales sobre el uso de la biblioteca", "no hay cifras en el texto"),
      ("Recurre a la opinión de un experto en educación", "no cita expertos"),
      ("Narra una anécdota de su infancia", "no hay anécdotas personales de infancia")],
     "Cita la frase «todo está en internet» y la contradice con ejemplos de usuarios reales: es una refutación."),
])

texto("cuento-farolero", "El último farolero", """
Cuando instalaron el alumbrado eléctrico en el pueblo, nadie pensó en don Abelardo. Durante cuarenta años había recorrido cada tarde las mismas once cuadras con su escalera al hombro, encendiendo uno por uno los faroles de parafina. Los niños lo seguían para verlo subir; los perros ya ni le ladraban.

La primera noche de las ampolletas, el pueblo entero salió a la plaza. Hubo aplausos, discursos y una banda que tocó dos cuecas desafinadas. Don Abelardo miró la luz blanca, tan pareja que borraba las sombras de los árboles, y se fue a su casa antes de que terminara la música.

Al día siguiente, a la hora de siempre, tomó la escalera. Su hija le recordó que ya no había nada que encender. Él asintió, pero salió igual. Recorrió las once cuadras, se detuvo bajo cada poste y, sin subir, miró hacia arriba durante un rato, como quien saluda a un conocido.

Lo hizo todas las tardes hasta el invierno. Con el tiempo, algunos vecinos empezaron a esperarlo en la puerta para conversar, y los niños, que ya no tenían nada que ver, lo acompañaban de todos modos. Cuando don Abelardo murió, una tarde de julio, las ampolletas se encendieron a su hora, como siempre. Pero esa noche, por primera vez, varios vecinos sacaron velas a sus ventanas.
""", "Cuento breve elaborado para este ensayo.", [
    (LOC, "baja", "¿Durante cuánto tiempo don Abelardo encendió los faroles del pueblo?",
     "Cuarenta años",
     [("Once años", "once son las cuadras que recorría"),
      ("Hasta el invierno", "hasta el invierno siguió recorriendo las calles, después del alumbrado eléctrico"),
      ("Dos temporadas", "el texto no lo dice")],
     "El párrafo 1 dice: «Durante cuarenta años había recorrido cada tarde las mismas once cuadras»."),
    (INT, "media", "¿Por qué don Abelardo se va a su casa antes de que termine la música en la inauguración?",
     "Porque el alumbrado eléctrico deja sin sentido el oficio al que dedicó su vida",
     [("Porque no le gustan las cuecas", "no hay indicios de eso"),
      ("Porque estaba cansado de recorrer las calles", "al día siguiente vuelve a recorrerlas"),
      ("Porque lo despidieron durante los discursos", "el texto no menciona un despido")],
     "Se infiere de que «nadie pensó en don Abelardo» y de que su trabajo desaparece con la nueva luz."),
    (INT, "alta", "¿Qué sentido tiene que don Abelardo siga recorriendo las cuadras sin encender nada?",
     "Mantener su rutina como una forma de despedirse de su oficio y de los faroles",
     [("Vigilar que las ampolletas funcionen bien", "no revisa nada: solo mira hacia arriba"),
      ("Protestar contra el alumbrado eléctrico", "no hay protesta; su gesto es de saludo"),
      ("Buscar un nuevo trabajo en el pueblo", "no se menciona esa búsqueda")],
     "Mira cada poste «como quien saluda a un conocido»: el gesto es afectivo, una despedida de lo que fue su vida."),
    (INT, "alta", "¿Qué expresa el gesto de los vecinos al final del cuento?",
     "Un homenaje a don Abelardo que reconoce el valor de lo que él representaba",
     [("Su rechazo a la luz eléctrica", "las velas no reemplazan a las ampolletas, que se encienden igual"),
      ("Que hubo un corte de luz en el pueblo", "las ampolletas se encendieron a su hora"),
      ("Su costumbre habitual de encender velas cada noche", "lo hacen «por primera vez»")],
     "Sacar velas «por primera vez» la noche de su muerte recuerda la luz de los faroles que él encendía."),
    (EVA, "media", "¿Qué tipo de narrador tiene el cuento?",
     "Un narrador externo que relata los hechos en tercera persona",
     [("Un narrador protagonista que cuenta su propia historia", "nunca habla don Abelardo en primera persona"),
      ("Un narrador testigo que participa como vecino", "no hay un «yo» que participe"),
      ("La hija de don Abelardo", "la hija aparece como personaje, no narra")],
     "El relato usa la tercera persona («tomó la escalera», «se fue a su casa») y no participa en los hechos."),
])

texto("aviso-vacunacion", "Campaña de invierno: preguntas frecuentes", """
¿Quiénes deben vacunarse contra la influenza? La vacuna es gratuita y está dirigida a las personas con mayor riesgo de complicaciones: adultos de 60 años o más, embarazadas a partir de la semana 13, niños entre 6 meses y 10 años, personas con enfermedades crónicas y trabajadores de la salud. Quienes no pertenecen a estos grupos pueden vacunarse en farmacias privadas.

¿Dónde me vacuno? En cualquier centro de salud familiar (Cesfam) de la red pública, sin necesidad de inscribirse en él. Además, durante abril y mayo habrá puntos móviles en colegios, estaciones de metro y ferias libres. Solo debe presentar su cédula de identidad; los menores de edad deben ir acompañados por un adulto responsable.

¿Por qué vacunarse todos los años? Porque el virus de la influenza cambia de una temporada a otra y la protección de la vacuna disminuye con los meses. Cada año se fabrica una vacuna nueva según las cepas que se espera que circulen. La protección comienza alrededor de dos semanas después de la inyección, por lo que conviene vacunarse antes del peak de contagios, que suele ocurrir entre junio y julio.

¿La vacuna puede darme influenza? No. La vacuna contiene virus inactivados, que no pueden causar la enfermedad. Algunas personas presentan dolor en el brazo o décimas de fiebre durante uno o dos días, síntomas leves que desaparecen solos. Si tiene dudas por una condición particular, consulte en su centro de salud.
""", "Texto informativo elaborado para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿qué documento hay que presentar para vacunarse en la red pública?",
     "La cédula de identidad",
     [("Un certificado de inscripción en el Cesfam", "el texto dice que no es necesario inscribirse"),
      ("Una receta médica", "no se pide receta"),
      ("Un certificado de enfermedad crónica", "no se menciona")],
     "El párrafo 2 indica: «Solo debe presentar su cédula de identidad»."),
    (LOC, "media", "¿Cuál de las siguientes personas pertenece a la población objetivo de la vacuna gratuita?",
     "Una mujer con 20 semanas de embarazo",
     [("Un estudiante sano de 18 años", "no pertenece a los grupos de riesgo mencionados"),
      ("Un niño de 4 meses", "el grupo comienza a los 6 meses"),
      ("Una mujer con 8 semanas de embarazo", "las embarazadas se vacunan desde la semana 13")],
     "Las embarazadas se vacunan «a partir de la semana 13»; 20 semanas cumple la condición."),
    (INT, "media", "¿Por qué se recomienda vacunarse antes de junio?",
     "Porque la protección tarda unas dos semanas en comenzar y los contagios aumentan en junio y julio",
     [("Porque después de junio la vacuna deja de ser gratuita", "el texto no lo menciona"),
      ("Porque la vacuna solo se fabrica en abril", "no se dice cuándo se fabrica"),
      ("Porque en junio los puntos móviles se trasladan a los colegios", "los puntos móviles funcionan en abril y mayo")],
     "Se combinan dos datos del párrafo 3: el tiempo que tarda la protección y la época del peak."),
    (INT, "media", "¿Cuál es el propósito principal del texto?",
     "Informar a la población sobre la vacunación y responder sus dudas más comunes",
     [("Convencer a las farmacias de vender la vacuna", "no se dirige a las farmacias"),
      ("Explicar en detalle cómo se fabrica la vacuna", "solo menciona brevemente que se fabrica cada año"),
      ("Narrar la historia de la influenza en Chile", "no es un relato histórico")],
     "El formato de preguntas y respuestas busca informar y resolver dudas frecuentes."),
    (EVA, "alta", "¿Por qué resulta adecuado organizar este texto en preguntas y respuestas?",
     "Porque permite al lector encontrar rápidamente la información que le interesa",
     [("Porque así el texto parece más literario", "no se busca un efecto literario"),
      ("Porque evita dar datos concretos", "el texto entrega datos concretos"),
      ("Porque obliga a leer el texto de principio a fin", "este formato permite leer solo la parte que interesa")],
     "En un texto informativo de servicio, las preguntas funcionan como títulos que orientan la búsqueda de información."),
])

texto("columna-pantallas", "¿Prohibir los celulares en la sala de clases?", """
Cada cierto tiempo vuelve el debate: ¿deben los colegios prohibir los teléfonos celulares durante las clases? Varios países europeos ya lo han hecho, y sus defensores citan estudios que asocian la presencia del teléfono con menor concentración y peores resultados. Los detractores, en cambio, advierten que la prohibición desconoce que los celulares son también herramientas de aprendizaje.

Creo que el debate está mal planteado. La pregunta no es si el celular es bueno o malo, sino para qué se usa en cada momento. Un teléfono que vibra cada pocos minutos con notificaciones de redes sociales difícilmente convive con la lectura atenta de un texto difícil. Pero ese mismo aparato puede servir para medir la aceleración en una clase de física o para grabar una entrevista en un proyecto de historia.

La experiencia de algunos colegios chilenos sugiere un camino intermedio: los teléfonos se guardan en una caja a la entrada de la sala y se sacan solo cuando el profesor diseña una actividad que los requiere. Esta regla tiene una ventaja que las prohibiciones totales no tienen: obliga a pensar el celular como una herramienta con un propósito, y no como un compañero permanente.

Claro que ninguna norma reemplaza la conversación. Si los estudiantes no entienden por qué la atención es valiosa, encontrarán la manera de esquivar cualquier caja. Enseñar a decidir cuándo desconectarse puede ser, al final, una lección más importante que cualquier contenido que el teléfono distraiga.
""", "Columna de opinión elaborada para este ensayo.", [
    (LOC, "baja", "¿Qué medida aplican algunos colegios chilenos, según el texto?",
     "Guardar los teléfonos en una caja y sacarlos solo para actividades que los requieran",
     [("Prohibir completamente los celulares en el colegio", "esa es la medida de algunos países europeos"),
      ("Permitir el uso libre del celular en clases", "no es lo que describe"),
      ("Entregar un teléfono a cada estudiante", "no se menciona")],
     "El párrafo 3 describe la caja a la entrada de la sala."),
    (INT, "media", "¿Cuál es la tesis que defiende el autor?",
     "El uso del celular en clases debe depender del propósito de cada actividad",
     [("Los celulares deben prohibirse en todos los colegios", "el autor critica la prohibición total"),
      ("Los celulares siempre mejoran el aprendizaje", "reconoce que pueden distraer"),
      ("El debate sobre los celulares no tiene importancia", "dice que está mal planteado, no que no importe")],
     "En el párrafo 2 afirma: «La pregunta no es si el celular es bueno o malo, sino para qué se usa en cada momento»."),
    (INT, "media", "¿Qué función cumplen los ejemplos de la clase de física y del proyecto de historia?",
     "Mostrar usos del celular que favorecen el aprendizaje",
     [("Demostrar que el celular distrae", "esos ejemplos muestran lo contrario"),
      ("Explicar cómo funcionan las notificaciones", "no tratan de las notificaciones"),
      ("Criticar a los profesores de esas asignaturas", "no hay crítica a los profesores")],
     "Los ejemplos ilustran la otra cara del argumento: el mismo aparato puede ser una herramienta."),
    (EVA, "alta", "¿Qué limitación reconoce el autor a su propia propuesta?",
     "Que una norma no funciona si los estudiantes no comprenden el valor de la atención",
     [("Que las cajas son caras para los colegios", "no habla de costos"),
      ("Que los estudios europeos son poco confiables", "no cuestiona esos estudios"),
      ("Que los profesores no saben usar el celular", "no lo menciona")],
     "El párrafo 4 dice que, sin comprensión, los estudiantes «encontrarán la manera de esquivar cualquier caja»."),
    (EVA, "media", "¿Cómo se organiza el texto?",
     "Plantea un debate, toma posición, propone una alternativa y cierra con una reflexión",
     [("Narra una experiencia personal de principio a fin", "no es un relato"),
      ("Enumera instrucciones para usar el celular", "no es un instructivo"),
      ("Compara datos de varios países en una tabla", "no hay tabla ni comparación de cifras")],
     "Párrafo 1: debate; 2: postura; 3: propuesta intermedia; 4: reflexión final."),
])

texto("biografia-mistral", "Una maestra rural", """
Lucila Godoy Alcayaga nació en 1889 en Vicuña, en el valle del Elqui. Hija de un profesor que abandonó el hogar cuando ella tenía tres años, creció junto a su madre y su media hermana Emelina, también maestra, quien le enseñó a leer. Desde adolescente trabajó como ayudante en escuelas rurales del valle, sin haber obtenido un título formal de profesora, lo que le valió durante años la desconfianza de algunas autoridades educacionales.

Sus primeros textos aparecieron en diarios de La Serena y, más tarde, de otras ciudades. En 1914 ganó los Juegos Florales de Santiago con los «Sonetos de la muerte», y el seudónimo con que ya firmaba algunos textos, Gabriela Mistral, comenzó a ser conocido en todo el país. Ese mismo nombre la acompañaría en su labor docente, que la llevó a dirigir liceos en Punta Arenas, Temuco y Santiago.

En 1922 fue invitada a México para colaborar en una reforma educacional que buscaba llevar la escuela al campo. Desde entonces vivió la mayor parte de su vida fuera de Chile, como cónsul y conferencista, sin dejar de escribir sobre los niños, los campesinos, las mujeres y los pueblos indígenas de América.

En 1945 recibió el Premio Nobel de Literatura, el primero otorgado a un escritor latinoamericano. Seis años después, recién, obtuvo en Chile el Premio Nacional de Literatura. Murió en Nueva York en 1957 y fue sepultada, según su deseo, en Montegrande, el pueblo del valle donde había pasado su infancia.
""", "Texto biográfico elaborado para este ensayo.", [
    (LOC, "baja", "¿En qué año recibió Gabriela Mistral el Premio Nobel de Literatura?",
     "En 1945",
     [("En 1914", "en 1914 ganó los Juegos Florales"),
      ("En 1951", "corresponde al Premio Nacional, seis años después del Nobel"),
      ("En 1922", "en 1922 viajó a México")],
     "El párrafo 4 indica que lo recibió en 1945."),
    (INT, "media", "¿Por qué algunas autoridades desconfiaron de ella durante años?",
     "Porque ejercía como profesora sin un título formal",
     [("Porque firmaba con un seudónimo", "el texto no relaciona el seudónimo con la desconfianza"),
      ("Porque vivía fuera de Chile", "la desconfianza es anterior a su vida en el extranjero"),
      ("Porque había ganado un concurso literario", "no se presenta como causa")],
     "El párrafo 1 vincula la desconfianza con que trabajó «sin haber obtenido un título formal de profesora»."),
    (INT, "alta", "¿Qué sugiere la palabra «recién» en el párrafo 4?",
     "Que el reconocimiento en Chile llegó tarde en comparación con el internacional",
     [("Que el Premio Nacional era más importante que el Nobel", "no compara la importancia de los premios"),
      ("Que el Premio Nacional se creó ese año", "el texto no lo dice"),
      ("Que recibió ambos premios al mismo tiempo", "hay seis años de diferencia")],
     "«Recién» subraya la demora: primero la reconoció el mundo y solo después su propio país."),
    (INT, "media", "¿Cuál es el propósito principal del texto?",
     "Dar a conocer los hitos de la vida de Gabriela Mistral",
     [("Analizar el estilo de los «Sonetos de la muerte»", "no analiza su poesía"),
      ("Explicar la reforma educacional mexicana", "la menciona solo como un hecho de su vida"),
      ("Criticar a las autoridades educacionales chilenas", "no es un texto de crítica")],
     "Es una biografía breve: ordena cronológicamente los hechos principales de su vida."),
    (EVA, "alta", "¿Qué relación establece el texto entre el inicio y el final de la vida de Mistral?",
     "Un regreso simbólico al valle de su infancia, donde fue sepultada",
     [("Un contraste entre la pobreza y la riqueza", "no se menciona su situación económica"),
      ("Una ruptura definitiva con su lugar de origen", "pidió ser sepultada en Montegrande"),
      ("Una repetición de los conflictos con su padre", "el padre no vuelve a aparecer")],
     "El texto empieza en el valle del Elqui y termina en Montegrande, «el pueblo del valle donde había pasado su infancia»."),
])

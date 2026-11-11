"""Competencia Lectora, segunda tanda de textos originales."""
from contenido.lectora import EVA, INT, LOC, texto

texto("desierto-florido", "Cuando florece el desierto", """
En la región de Atacama, uno de los lugares más secos del planeta, hay años en que el suelo pardo se cubre de un día para otro de flores violetas, amarillas y blancas. El fenómeno, conocido como desierto florido, no ocurre todos los años: depende de que caigan lluvias excepcionales, generalmente asociadas al fenómeno de El Niño, que calienta las aguas del Pacífico y altera el clima de la costa.

El secreto está bajo tierra. Durante años, a veces décadas, miles de semillas y bulbos permanecen en estado latente, a la espera de la humedad suficiente para germinar. Cuando llueve más de lo habitual, las plantas aprovechan el breve periodo favorable: brotan, florecen y producen nuevas semillas en pocas semanas, antes de que el suelo vuelva a secarse. Entre ellas destacan la pata de guanaco, la añañuca y la garra de león, esta última considerada en peligro.

El espectáculo atrae cada vez a más visitantes, y con ellos aparecen problemas. Algunos turistas arrancan flores o bulbos para llevárselos, y otros conducen vehículos fuera de los caminos, lo que compacta el suelo y destruye las semillas que debían asegurar la próxima floración. Por eso, las autoridades han delimitado senderos, han prohibido la extracción de plantas y han instalado guardaparques en los sectores más visitados.

Los científicos recuerdan que el desierto florido es mucho más que un paisaje atractivo. Es una muestra de cómo la vida se adapta a condiciones extremas y un laboratorio natural para estudiar la resistencia de las plantas a la sequía, una pregunta que el cambio climático vuelve cada vez más urgente.
""", "Texto expositivo elaborado para este ensayo.", [
    (LOC, "baja", "¿De qué depende que ocurra el desierto florido?",
     "De que caigan lluvias excepcionales en la zona",
     [("De la llegada de turistas", "los turistas acuden cuando ya ocurrió"),
      ("De que se siembren semillas cada año", "las semillas ya están en el suelo"),
      ("De que los guardaparques rieguen los senderos", "no se menciona riego")],
     "El párrafo 1 dice que «depende de que caigan lluvias excepcionales»."),
    (INT, "media", "¿Qué significa que las semillas permanezcan «en estado latente»?",
     "Que se mantienen vivas pero inactivas hasta que hay condiciones para germinar",
     [("Que están muertas por la sequía", "si estuvieran muertas no podrían germinar"),
      ("Que crecen lentamente bajo tierra", "no crecen: esperan"),
      ("Que fueron enterradas por los turistas", "no se relaciona con los turistas")],
     "El texto explica que esperan «la humedad suficiente para germinar»: están inactivas, no muertas."),
    (INT, "media", "Según el texto, ¿por qué conducir fuera de los caminos afecta al desierto florido?",
     "Porque compacta el suelo y destruye las semillas de futuras floraciones",
     [("Porque contamina el aire con polvo", "el texto no lo menciona"),
      ("Porque asusta a los animales que polinizan", "no se mencionan polinizadores"),
      ("Porque impide que llueva", "la lluvia no depende de los vehículos")],
     "El párrafo 3 establece una relación de causa y consecuencia entre los vehículos y la pérdida de semillas."),
    (INT, "alta", "¿Cuál es la idea principal del último párrafo?",
     "El desierto florido tiene un valor científico además de su atractivo visual",
     [("El desierto florido es el mejor destino turístico de Chile", "el párrafo se aleja del turismo"),
      ("El cambio climático ha terminado con el desierto florido", "no se afirma eso"),
      ("Los científicos prohíben visitar el desierto florido", "las restricciones las ponen las autoridades")],
     "El párrafo dice que es «mucho más que un paisaje atractivo» y lo presenta como un laboratorio natural."),
    (EVA, "media", "¿Qué propósito cumple la mención de la garra de león «considerada en peligro»?",
     "Reforzar la importancia de proteger las especies del desierto florido",
     [("Explicar cómo se forma una flor", "no describe su formación"),
      ("Recomendar a los turistas que la recolecten", "el texto se opone a la extracción"),
      ("Demostrar que todas las especies están extintas", "no generaliza así")],
     "Mencionar una especie amenazada da peso a las medidas de protección del párrafo 3."),
])

texto("resena-pelicula", "Reseña: «La última temporada»", """
«La última temporada», el nuevo largometraje del director Tomás Arancibia, sigue durante un verano a una familia de pescadores de una caleta del norte que debe decidir si vende su bote a una empresa turística. Lo que podría haber sido un drama previsible sobre la tradición amenazada por el progreso se convierte, gracias a un guion contenido y a actuaciones notables, en una de las películas chilenas más honestas de los últimos años.

El mayor mérito de Arancibia es no tomar partido de manera evidente. La empresa no es una caricatura de villanos y la familia no es un grupo de héroes intachables: el padre se aferra al oficio por orgullo tanto como por convicción, y la hija menor ve en la venta la posibilidad de estudiar en la universidad. La cámara observa estas tensiones sin subrayarlas, con largos planos del mar al amanecer que funcionan como pausas para el espectador.

No todo, sin embargo, está igual de logrado. La subtrama de un romance entre el hijo mayor y una turista santiaguina se siente forzada y resta ritmo a la segunda mitad. Además, algunos diálogos explican lo que las imágenes ya habían mostrado con elocuencia, como si el director desconfiara por momentos de su propio público.

Aun con estos reparos, «La última temporada» es una película que vale la pena ver en pantalla grande. Su final abierto, que no revelaremos aquí, ha dividido a la crítica; a mi juicio, es la decisión más valiente de una obra que prefiere las preguntas a las respuestas fáciles.
""", "Reseña ficticia elaborada para este ensayo.", [
    (LOC, "baja", "¿Qué decisión debe tomar la familia protagonista de la película?",
     "Si vende su bote a una empresa turística",
     [("Si se muda a Santiago", "no es la decisión central"),
      ("Si la hija estudia o trabaja en la caleta", "es una consecuencia posible, no la decisión planteada"),
      ("Si participa en una competencia de pesca", "no se menciona")],
     "El párrafo 1 dice que la familia «debe decidir si vende su bote a una empresa turística»."),
    (INT, "media", "Según el autor, ¿qué evita la película?",
     "Presentar a los personajes como buenos y malos de manera simplista",
     [("Mostrar paisajes del mar", "la película tiene largos planos del mar"),
      ("Incluir una historia de amor", "sí incluye un romance"),
      ("Usar actores conocidos", "no se refiere al elenco")],
     "El párrafo 2 señala que la empresa no es una caricatura y la familia no es un grupo de héroes intachables."),
    (INT, "media", "¿Qué función cumple el párrafo 3 en la reseña?",
     "Señalar las debilidades de la película",
     [("Resumir el argumento completo", "el argumento se presenta en el párrafo 1"),
      ("Revelar el final de la película", "el final no se revela"),
      ("Describir la trayectoria del director", "no se describe su trayectoria")],
     "Comienza con «No todo, sin embargo, está igual de logrado» y enumera dos defectos."),
    (EVA, "alta", "¿Cuál es la valoración global que hace el autor de la película?",
     "Positiva, aunque con reparos puntuales",
     [("Completamente negativa", "recomienda verla en pantalla grande"),
      ("Neutra, porque no emite opiniones", "emite juicios claros"),
      ("Positiva y sin ninguna crítica", "critica la subtrama romántica y algunos diálogos")],
     "La califica como «una de las películas chilenas más honestas», pero reconoce defectos en el párrafo 3."),
    (EVA, "alta", "Cuando el autor dice que algunos diálogos explican lo que las imágenes ya mostraron, ¿qué critica?",
     "La redundancia, que subestima la capacidad del público de comprender",
     [("La mala calidad de la fotografía", "elogia las imágenes"),
      ("La falta de diálogos en la película", "critica lo contrario"),
      ("Que los actores hablen demasiado rápido", "no se refiere a la dicción")],
     "Agrega que es «como si el director desconfiara por momentos de su propio público»."),
])

texto("sueno-adolescentes", "¿Por qué los adolescentes se acuestan tarde?", """
Muchos padres creen que sus hijos adolescentes se acuestan tarde por simple desorden o por el uso de pantallas. Las pantallas influyen, pero la biología también tiene algo que decir. Durante la adolescencia, el reloj interno del cuerpo, que regula los ciclos de sueño y vigilia, se desplaza: la melatonina, la hormona que induce el sueño, comienza a liberarse más tarde que en la infancia, a veces hasta dos horas después.

Este retraso hace que a un adolescente le cueste dormirse antes de las once o las doce de la noche, aunque se acueste temprano. El problema es que los horarios escolares no siguen ese cambio. Si la jornada comienza a las ocho de la mañana, muchos estudiantes duermen seis o siete horas, cuando los especialistas recomiendan entre ocho y diez a esa edad.

La falta de sueño acumulada tiene consecuencias conocidas: dificultades para concentrarse, cambios de ánimo, menor rendimiento académico y mayor riesgo de accidentes. Algunos distritos escolares de Estados Unidos retrasaron el inicio de las clases en media hora o una hora, y las investigaciones posteriores registraron más horas de sueño, menos atrasos y una leve mejora en las calificaciones.

Mientras tanto, hay medidas que dependen de cada familia: evitar las pantallas en la hora previa a dormir, mantener horarios regulares también los fines de semana y exponerse a la luz natural por la mañana, que ayuda a ajustar el reloj interno. No se trata de pelear contra la biología, sino de entenderla.
""", "Texto de divulgación elaborado para este ensayo.", [
    (LOC, "baja", "¿Cuántas horas de sueño recomiendan los especialistas para los adolescentes, según el texto?",
     "Entre ocho y diez",
     [("Seis o siete", "es lo que muchos duermen, no lo recomendado"),
      ("Dos más que en la infancia", "dos horas es el retraso posible de la melatonina"),
      ("Once o doce", "esas son las horas en que les cuesta dormirse")],
     "El párrafo 2 dice que se recomiendan «entre ocho y diez a esa edad»."),
    (INT, "media", "¿Qué relación establece el texto entre la melatonina y el horario de sueño adolescente?",
     "Su liberación más tardía explica que a los adolescentes les cueste dormirse temprano",
     [("Su exceso provoca que los adolescentes duerman demasiado", "el texto habla de un retraso, no de un exceso"),
      ("Las pantallas eliminan por completo la melatonina", "no se afirma eso"),
      ("La melatonina aumenta con la luz de la mañana", "la luz matinal ajusta el reloj, no aumenta la hormona")],
     "Es una relación de causa y consecuencia entre los párrafos 1 y 2."),
    (INT, "media", "¿Qué función cumple el ejemplo de los distritos escolares de Estados Unidos?",
     "Aportar evidencia de que retrasar el inicio de clases puede tener efectos positivos",
     [("Mostrar que en Estados Unidos los jóvenes duermen menos", "no compara países"),
      ("Explicar cómo funciona el reloj interno", "eso se explica en el párrafo 1"),
      ("Criticar a los padres de los adolescentes", "no hay crítica a los padres")],
     "Las investigaciones registraron más horas de sueño, menos atrasos y mejores notas."),
    (INT, "alta", "¿Qué sentido tiene la frase final «No se trata de pelear contra la biología, sino de entenderla»?",
     "Propone adaptar los hábitos y horarios al funcionamiento natural del cuerpo",
     [("Sostiene que la biología no influye en el sueño", "todo el texto afirma lo contrario"),
      ("Recomienda a los adolescentes estudiar biología", "es una expresión figurada"),
      ("Afirma que no hay nada que hacer frente al problema", "el párrafo propone medidas concretas")],
     "Sintetiza el texto: en vez de culpar a los jóvenes, ajustar horarios y hábitos a su reloj interno."),
    (EVA, "alta", "¿Qué opinión común busca corregir el texto desde su inicio?",
     "Que los adolescentes se acuestan tarde solo por desorden o por usar pantallas",
     [("Que la luz natural daña el sueño", "el texto recomienda la luz natural"),
      ("Que las clases deberían empezar más temprano", "no es una opinión que el texto mencione"),
      ("Que los adolescentes necesitan menos sueño que los niños", "no aparece esa idea")],
     "El primer párrafo presenta la creencia de los padres y la matiza con la explicación biológica."),
])

texto("cuento-lista", "La lista", """
Antes de mudarse, mi abuela hizo una lista de lo que se llevaría al departamento nuevo. Era una hoja de cuaderno escrita con letra apretada, con columnas que ella misma había trazado con regla: «Llevar», «Regalar», «Botar». La pegó con cinta en la puerta del refrigerador y nos prohibió tocarla.

Durante dos semanas, la lista cambió todos los días. El sillón verde pasó de «Regalar» a «Llevar» y volvió a «Regalar». La máquina de coser, que nadie había visto funcionar en años, se quedó siempre en «Llevar», con dos líneas debajo. Las cartas de mi abuelo no aparecían en ninguna columna. Cuando le pregunté por ellas, me dijo que esas no eran cosas.

El día de la mudanza, los hombres del camión cargaron todo lo que estaba en la primera columna. Al final quedó la casa vacía, con marcas más claras en las paredes donde habían estado los cuadros. Mi abuela recorrió las piezas despacio, tocando los marcos de las puertas, y yo pensé que iba a llorar. No lloró. Se acercó al refrigerador, despegó la lista, la dobló en cuatro y se la guardó en el bolsillo del delantal.

Años después, ordenando sus cosas, encontré la hoja entre las páginas de un libro de recetas. Al reverso, con la misma letra apretada, había escrito una sola palabra, sin columna: «Quedarse».
""", "Cuento breve elaborado para este ensayo.", [
    (LOC, "baja", "¿Qué columnas tenía la lista de la abuela?",
     "«Llevar», «Regalar» y «Botar»",
     [("«Llevar», «Vender» y «Guardar»", "no son las columnas mencionadas"),
      ("«Cosas» y «Recuerdos»", "esa distinción la hace la abuela al hablar de las cartas, no en la hoja"),
      ("«Quedarse» y «Partir»", "«Quedarse» aparece al reverso, sin columna")],
     "El párrafo 1 las nombra textualmente."),
    (INT, "media", "¿Qué revela que la lista cambiara todos los días?",
     "Las dudas de la abuela al desprenderse de objetos cargados de recuerdos",
     [("Que la abuela tenía mala memoria", "no hay indicios de olvido"),
      ("Que los nietos modificaban la lista a escondidas", "la abuela prohibió tocarla"),
      ("Que el departamento nuevo era muy grande", "no se menciona su tamaño")],
     "El sillón va y viene entre columnas: decidir qué dejar le cuesta, porque los objetos tienen valor afectivo."),
    (INT, "alta", "¿Qué quiere decir la abuela cuando afirma que las cartas «no eran cosas»?",
     "Que su valor afectivo las ponía fuera de cualquier decisión práctica",
     [("Que las cartas ya se habían perdido", "no se dice que se hayan perdido"),
      ("Que pensaba botarlas sin anotarlas", "no hay indicios de que quisiera deshacerse de ellas"),
      ("Que las cartas no tenían importancia", "es lo contrario: eran demasiado importantes para clasificarlas")],
     "Las cartas del abuelo no entran en ninguna columna porque no se miden como objetos."),
    (INT, "alta", "¿Qué sentido tiene la palabra «Quedarse» escrita al reverso de la lista?",
     "Expresa el deseo íntimo de la abuela de no abandonar su casa",
     [("Es una instrucción para los hombres del camión", "la escribe en privado y la guarda"),
      ("Indica que la mudanza se canceló", "la mudanza sí ocurrió"),
      ("Es el nombre de una receta de cocina", "aparece en la hoja guardada en el libro, pero no es una receta")],
     "Escrita sin columna y oculta, revela lo que la abuela no dijo en voz alta: no quería irse."),
    (EVA, "media", "¿Desde qué perspectiva se narra el cuento?",
     "Desde la de un nieto o nieta que recuerda los hechos en primera persona",
     [("Desde la de la abuela, que cuenta su propia mudanza", "la abuela es narrada, no narradora"),
      ("Desde la de un narrador que no participa en la historia", "el narrador dice «mi abuela» y «yo pensé»"),
      ("Desde la de uno de los hombres del camión", "no corresponde a ese personaje")],
     "Expresiones como «mi abuela», «le pregunté» y «encontré la hoja» muestran un narrador protagonista o testigo en primera persona."),
])

texto("agua-hogar", "¿Cuánta agua usamos en casa?", """
Una persona en una ciudad chilena usa, en promedio, entre 150 y 200 litros de agua potable al día. La mayor parte no se bebe: se va por la ducha, el inodoro y la lavadora. La siguiente información, preparada por una empresa sanitaria, muestra el consumo aproximado de algunas actividades cotidianas.

Ducha de 10 minutos: entre 100 y 120 litros. Descarga de un inodoro antiguo: entre 12 y 15 litros; uno de doble descarga usa entre 3 y 6. Lavado de loza a mano con la llave abierta: hasta 100 litros; con el lavaplatos tapado, unos 20. Lavadora con carga completa: entre 60 y 90 litros. Riego de jardín con manguera durante media hora: alrededor de 500 litros.

Con pequeños cambios es posible reducir el consumo en casi un tercio. Acortar la ducha a cinco minutos ahorra más de 50 litros por persona cada día. Instalar aireadores en las llaves, que mezclan el agua con aire, disminuye el caudal sin que se note la diferencia. Regar al atardecer, cuando el sol no evapora el agua, permite usar menos para obtener el mismo resultado.

Estas medidas importan especialmente en la zona central, que acumula más de una década de sequía. Cada litro que no se usa en una casa es agua que permanece en embalses y napas subterráneas para los meses más secos.
""", "Texto informativo elaborado para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿cuánta agua usa aproximadamente una ducha de 10 minutos?",
     "Entre 100 y 120 litros",
     [("Entre 150 y 200 litros", "es el consumo diario promedio de una persona"),
      ("Entre 60 y 90 litros", "corresponde a la lavadora"),
      ("Más de 50 litros", "es lo que se ahorra al acortar la ducha")],
     "El párrafo 2 indica el consumo de la ducha."),
    (INT, "media", "¿Qué actividad de las mencionadas consume más agua?",
     "Regar el jardín con manguera durante media hora",
     [("Ducharse 10 minutos", "consume hasta 120 litros"),
      ("Lavar la loza con la llave abierta", "consume hasta 100 litros"),
      ("Usar la lavadora con carga completa", "consume hasta 90 litros")],
     "El riego con manguera usa alrededor de 500 litros, la cifra más alta de la lista."),
    (INT, "media", "¿Por qué conviene regar al atardecer?",
     "Porque se evapora menos agua y se necesita menos para el mismo resultado",
     [("Porque el agua es más barata en la tarde", "no se habla del precio"),
      ("Porque las plantas solo absorben agua de noche", "no se afirma eso"),
      ("Porque los aireadores funcionan mejor en la tarde", "los aireadores se instalan en las llaves")],
     "El párrafo 3 explica que al atardecer «el sol no evapora el agua»."),
    (EVA, "media", "¿Qué propósito tiene el último párrafo?",
     "Mostrar la importancia de ahorrar agua en el contexto de la sequía",
     [("Explicar cómo funcionan los embalses", "solo los menciona"),
      ("Comparar el consumo de distintas ciudades", "no hay comparación entre ciudades"),
      ("Recomendar que no se use la lavadora", "no hace esa recomendación")],
     "Relaciona el ahorro doméstico con la sequía de la zona central y con el agua disponible en embalses y napas."),
    (EVA, "alta", "¿Qué ventaja tiene presentar el consumo de cada actividad con cifras concretas?",
     "Permite al lector comparar actividades y decidir dónde le conviene ahorrar",
     [("Hace el texto más difícil de comprender", "las cifras lo hacen más concreto"),
      ("Demuestra que el agua potable es gratuita", "no se habla del costo"),
      ("Reemplaza la necesidad de dar recomendaciones", "el texto igual da recomendaciones")],
     "Las cifras del párrafo 2 sustentan las recomendaciones del párrafo 3 y facilitan la comparación."),
])

texto("rapa-nui-turismo", "¿Cuántos visitantes puede recibir una isla?", """
Rapa Nui recibe cada año a decenas de miles de turistas atraídos por los moai, sus paisajes volcánicos y su cultura. Para una isla de poco más de 160 kilómetros cuadrados, a más de 3.500 kilómetros del continente, esa cifra plantea una pregunta difícil: ¿cuántas personas pueden llegar sin dañar aquello que vienen a ver?

Los defensores de limitar el turismo señalan que la isla tiene recursos escasos. El agua dulce proviene casi totalmente de acuíferos subterráneos que se recargan con la lluvia, la basura debe enviarse al continente o acumularse en un vertedero con capacidad limitada, y la mayor parte de los alimentos llega por barco o avión. A eso se suma el desgaste de los sitios arqueológicos, algunos de los cuales han sido dañados por visitantes que se suben a las estructuras o se llevan piedras como recuerdo.

Quienes se oponen a las restricciones recuerdan que el turismo es la principal fuente de ingresos de muchas familias isleñas. Reducir el número de visitantes, advierten, podría afectar a los pequeños emprendimientos de alojamiento, comida y guías, y favorecer solo a los operadores más grandes, capaces de resistir una temporada más corta.

Entre ambas posiciones han surgido propuestas intermedias: limitar el tiempo de permanencia en la isla, exigir que cada visita a sitios arqueológicos sea guiada por un isleño, cobrar un aporte que financie el manejo de residuos y priorizar a los operadores locales. Lo que parece claro es que la decisión no debería tomarse sin la participación de la comunidad rapanui, que ha cuidado su territorio durante siglos y conoce mejor que nadie sus límites.
""", "Texto argumentativo elaborado para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿de dónde proviene casi toda el agua dulce de Rapa Nui?",
     "De acuíferos subterráneos que se recargan con la lluvia",
     [("De plantas desalinizadoras", "no se mencionan"),
      ("De barcos que la traen del continente", "los barcos traen alimentos"),
      ("De ríos que nacen en los volcanes", "no se mencionan ríos")],
     "El párrafo 2 indica que proviene «casi totalmente de acuíferos subterráneos»."),
    (INT, "media", "¿Qué tienen en común los argumentos del párrafo 2?",
     "Muestran que los recursos y el patrimonio de la isla tienen un límite",
     [("Muestran que el turismo genera empleos", "eso se plantea en el párrafo 3"),
      ("Explican el origen de los moai", "no se refieren al origen de los moai"),
      ("Proponen soluciones intermedias", "las soluciones están en el párrafo 4")],
     "Agua, basura, alimentos y sitios arqueológicos aparecen como recursos que pueden agotarse o dañarse."),
    (INT, "media", "¿Qué riesgo plantean quienes se oponen a restringir el turismo?",
     "Que la medida perjudique a los pequeños emprendedores isleños",
     [("Que aumente la basura en la isla", "es un argumento a favor de limitar"),
      ("Que los turistas dañen los sitios arqueológicos", "también es un argumento a favor de limitar"),
      ("Que la isla quede sin agua", "es un argumento del párrafo 2")],
     "El párrafo 3 advierte que se podría favorecer solo a los operadores más grandes."),
    (EVA, "alta", "¿Cuál es la postura del autor en el último párrafo?",
     "Considera indispensable que la comunidad rapanui participe en la decisión",
     [("Apoya prohibir completamente el turismo", "propone medidas intermedias, no una prohibición"),
      ("Cree que no hay que cambiar nada", "presenta propuestas de cambio"),
      ("Se abstiene de dar cualquier opinión", "dice lo que «parece claro» y lo que «no debería» hacerse")],
     "La frase final expresa su posición: la decisión no debe tomarse sin la comunidad rapanui."),
    (EVA, "alta", "¿Cómo se estructura principalmente este texto?",
     "Plantea un problema, expone dos posturas opuestas y luego propuestas intermedias",
     [("Narra la historia de la isla en orden cronológico", "no es un relato histórico"),
      ("Describe paso a paso cómo visitar la isla", "no es un instructivo"),
      ("Presenta solo los beneficios del turismo", "presenta también sus costos")],
     "Párrafo 1: pregunta; 2: argumentos para limitar; 3: argumentos en contra; 4: propuestas y postura."),
])

texto("cronica-caleta", "Madrugada en la caleta", """
A las cinco de la mañana, cuando el resto de la ciudad todavía duerme, la caleta ya huele a petróleo, a sal y a café recalentado. Los botes vuelven de a uno, con las luces de navegación encendidas, y el muelle se llena de un ruido ordenado: cajones que se arrastran, gaviotas que discuten y voces que gritan precios que nadie parece anotar.

Don Ramiro, que lleva treinta y dos años en el mar, baja de su bote con las manos rojas de frío. Esta noche sacaron reineta y algo de jibia, «poco, pero algo», dice. Cuenta que antes salían tres veces por semana y volvían con los cajones llenos; ahora salen casi todos los días y vuelven con la mitad. Culpa a la pesca industrial, al agua más tibia y, a ratos, a la mala suerte. Su hijo, que lo ayuda a descargar, estudia mecánica en un instituto y no piensa seguir el oficio.

En el mesón de la feria, las señoras que limpian el pescado trabajan a una velocidad que parece imposible. Una de ellas, la señora Nora, separa los filetes de una reineta en menos de un minuto, sin mirar el cuchillo. Mientras tanto, conversa con una clienta sobre el precio del gas y sobre el nieto que acaba de entrar al colegio.

A las ocho, cuando llegan los primeros turistas con sus cámaras, la caleta ya parece otra. Los botes descansan amarrados, el muelle está casi limpio y las gaviotas se pelean por los restos. Nadie que llegue a esa hora imagina el trabajo de las tres horas anteriores, que se repite, con más o menos suerte, cada madrugada.
""", "Crónica elaborada para este ensayo.", [
    (LOC, "baja", "¿Qué pescaron don Ramiro y su hijo esa noche?",
     "Reineta y algo de jibia",
     [("Merluza y congrio", "no se mencionan"),
      ("Solo jibia", "también sacaron reineta"),
      ("Nada, porque había mal tiempo", "sacaron «poco, pero algo»")],
     "El párrafo 2 lo indica textualmente."),
    (INT, "media", "¿Qué cambio en la pesca describe don Ramiro?",
     "Ahora salen con más frecuencia y obtienen menos peces",
     [("Ahora salen menos y pescan más", "es lo contrario"),
      ("Ahora pescan solo para los turistas", "no lo dice"),
      ("Ahora usan barcos industriales", "culpa a la pesca industrial; él no la practica")],
     "Antes salían tres veces por semana con los cajones llenos; ahora casi todos los días y vuelven con la mitad."),
    (INT, "media", "¿Qué sugiere el dato de que el hijo de don Ramiro estudia mecánica?",
     "Que el oficio de pescador podría no continuar en la familia",
     [("Que el bote necesita reparaciones", "no se relaciona con el bote"),
      ("Que la pesca será más moderna", "no se infiere eso"),
      ("Que don Ramiro quiere dejar de pescar", "es el hijo quien no seguirá el oficio")],
     "El texto dice que el hijo «no piensa seguir el oficio»."),
    (INT, "alta", "¿Qué contraste establece el último párrafo?",
     "Entre el trabajo intenso de la madrugada y la imagen tranquila que ven los turistas",
     [("Entre la pesca artesanal y la pesca industrial", "no es el foco del último párrafo"),
      ("Entre el frío de la noche y el calor del día", "no se habla del clima"),
      ("Entre los pescadores jóvenes y los viejos", "no se los compara")],
     "Los turistas llegan cuando «la caleta ya parece otra» y no imaginan el trabajo anterior."),
    (EVA, "media", "¿Qué recurso predomina en el párrafo 1?",
     "La descripción sensorial de olores y sonidos",
     [("La cita de estadísticas", "no hay cifras"),
      ("El diálogo entre personajes", "no hay diálogos"),
      ("La argumentación con razones", "no se defiende una tesis")],
     "Se describen olores (petróleo, sal, café) y sonidos (cajones, gaviotas, voces): crea la atmósfera de la crónica."),
])

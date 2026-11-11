"""Competencia Lectora, tercera tanda de textos originales."""
from contenido.lectora import EVA, INT, LOC, texto

texto("microplasticos", "Partículas que no se ven", """
Los microplásticos son fragmentos de plástico de menos de cinco milímetros. Algunos se fabrican así, como las microesferas que se usaban en cremas exfoliantes; la mayoría, sin embargo, se forma cuando objetos más grandes, como botellas, bolsas o redes de pesca, se rompen lentamente por acción del sol, el oleaje y el roce.

En las últimas dos décadas se han encontrado microplásticos en casi todos los lugares donde se han buscado: en la arena de las playas, en el hielo del Ártico, en el agua potable, en la sal de mesa y en el interior de peces y mariscos. Un estudio realizado en playas del litoral chileno encontró fragmentos en todas las muestras analizadas, aunque en concentraciones muy variables según la cercanía a ciudades y desembocaduras de ríos.

Lo que todavía no está claro es cuánto daño causan. En experimentos de laboratorio, algunos organismos marinos expuestos a altas concentraciones comen menos, crecen más lento o se reproducen con dificultad. Pero las concentraciones de esos experimentos suelen ser mayores que las que se encuentran en el ambiente, y los efectos sobre la salud humana se conocen aún menos. Los científicos coinciden en que faltan estudios de largo plazo.

Esa incertidumbre, advierten algunos investigadores, no debería servir de excusa para esperar. El plástico que hoy llega al mar seguirá fragmentándose durante siglos, de modo que reducir su uso y mejorar su reciclaje es una medida de precaución razonable, incluso antes de tener todas las respuestas.
""", "Texto de divulgación elaborado para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿qué tamaño tienen los microplásticos?",
     "Menos de cinco milímetros",
     [("Menos de cinco centímetros", "el texto habla de milímetros"),
      ("Más de cinco milímetros", "es lo contrario"),
      ("El tamaño de una botella", "las botellas son objetos que se fragmentan")],
     "La primera oración del párrafo 1 lo define."),
    (INT, "media", "¿Cómo se forma la mayoría de los microplásticos?",
     "Por la fragmentación lenta de objetos de plástico más grandes",
     [("Por la fabricación de cremas exfoliantes", "es solo una parte, no la mayoría"),
      ("Por la acción de los peces sobre el plástico", "el texto menciona sol, oleaje y roce"),
      ("Por reacciones químicas en el agua potable", "no se menciona")],
     "El párrafo 1 dice que «la mayoría» se forma cuando objetos grandes «se rompen lentamente»."),
    (INT, "media", "¿Qué conclusión se desprende del estudio en playas chilenas?",
     "La concentración de microplásticos es mayor cerca de ciudades y desembocaduras",
     [("No hay microplásticos en las playas de Chile", "se encontraron en todas las muestras"),
      ("Todas las playas tienen la misma concentración", "las concentraciones eran «muy variables»"),
      ("Los microplásticos provienen solo del Ártico", "no se afirma eso")],
     "Se infiere de que las concentraciones variaban «según la cercanía a ciudades y desembocaduras de ríos»."),
    (EVA, "alta", "¿Por qué el autor relativiza los resultados de los experimentos de laboratorio?",
     "Porque usan concentraciones mayores que las que hay en el ambiente",
     [("Porque fueron hechos con peces chilenos", "no se menciona el origen de los organismos"),
      ("Porque los científicos falsificaron los datos", "no hay ninguna acusación"),
      ("Porque demostraron que los microplásticos son inofensivos", "mostraron efectos, pero en condiciones extremas")],
     "El párrafo 3 explica la limitación: las concentraciones experimentales «suelen ser mayores»."),
    (EVA, "alta", "¿Qué postura defiende el último párrafo?",
     "Que conviene actuar con precaución aunque falten pruebas definitivas",
     [("Que hay que esperar a tener todas las respuestas antes de actuar", "es justamente lo que rechaza"),
      ("Que el plástico desaparece rápidamente del mar", "dice que se fragmenta durante siglos"),
      ("Que el reciclaje no sirve para nada", "propone mejorarlo")],
     "La incertidumbre «no debería servir de excusa para esperar»: es un argumento basado en el principio de precaución."),
])

texto("tren-sur", "El tren nocturno", """
Mi padre decía que el tren al sur no era un medio de transporte, sino una manera de cambiar de idioma. Salíamos de la Estación Central al anochecer, con un canasto de huevos duros, pan amasado y un termo de té, y despertábamos en otro país: lluvia en los vidrios, potreros verdes y mujeres en los andenes ofreciendo queso y longanizas en canastos cubiertos con paños blancos.

Yo tenía nueve años la última vez que hicimos ese viaje. Recuerdo el traqueteo que me impedía dormir y la luz amarilla del pasillo, que se colaba por la cortina del camarote. Mi padre, que nunca hablaba mucho, se sentaba junto a la ventana y nombraba los pueblos a medida que pasábamos, aunque afuera no se viera nada: «Rancagua», «Curicó», «Talca», como quien reza un rosario aprendido de memoria.

Años después supe que ese tren había dejado de correr. Las estaciones de varios pueblos se convirtieron en bodegas, en sedes vecinales o simplemente en ruinas con los vidrios rotos. Cuando volví al sur, ya adulta, lo hice en un bus con aire acondicionado y pantallas en los asientos. Llegué más rápido y más descansada. Nadie nombró los pueblos.

A veces, en el insomnio, intento repetir la lista de mi padre. Me equivoco en el orden, me salto alguno. Entonces entiendo que lo que se perdió no fue solo un tren, sino una forma de recorrer el país, despacio, sabiendo el nombre de cada lugar por el que se pasa.
""", "Relato elaborado para este ensayo.", [
    (LOC, "baja", "¿Qué edad tenía la narradora la última vez que viajó en el tren con su padre?",
     "Nueve años",
     [("Era adulta", "de adulta viajó en bus"),
      ("Doce años", "no se menciona esa edad"),
      ("No se indica en el texto", "el párrafo 2 la indica")],
     "El párrafo 2 comienza: «Yo tenía nueve años la última vez que hicimos ese viaje»."),
    (INT, "alta", "¿Qué quiere decir el padre con que el tren era «una manera de cambiar de idioma»?",
     "Que el viaje llevaba a un paisaje y unas costumbres muy distintas de las de la ciudad",
     [("Que en el sur se hablaba otra lengua", "es una expresión figurada"),
      ("Que en el tren se aprendían idiomas extranjeros", "no hay clases en el tren"),
      ("Que el tren era muy ruidoso", "el ruido no se relaciona con la frase")],
     "Lo explica la imagen siguiente: despertaban «en otro país», con lluvia, potreros y comidas propias del sur."),
    (INT, "media", "¿Qué comparación usa la narradora para describir cómo su padre nombraba los pueblos?",
     "La compara con rezar un rosario aprendido de memoria",
     [("La compara con leer un mapa", "no hay tal comparación"),
      ("La compara con cantar una canción", "no se menciona"),
      ("La compara con el traqueteo del tren", "el traqueteo se describe aparte")],
     "La frase «como quien reza un rosario aprendido de memoria» sugiere un ritual íntimo y repetido."),
    (INT, "alta", "¿Qué contraste plantea el párrafo 3?",
     "Entre la comodidad del viaje moderno y la pérdida de una experiencia significativa",
     [("Entre la lluvia del sur y el calor del norte", "no se habla del norte"),
      ("Entre la juventud del padre y la vejez de la narradora", "no es el foco"),
      ("Entre el precio del tren y el del bus", "no se mencionan precios")],
     "El bus es más rápido y cómodo, pero «Nadie nombró los pueblos»."),
    (EVA, "media", "¿Qué tono predomina en el texto?",
     "Nostálgico",
     [("Humorístico", "no hay humor"),
      ("Indignado", "no hay protesta ni enojo"),
      ("Técnico", "no es un texto especializado")],
     "La narradora recuerda con añoranza una experiencia de su infancia que ya no existe."),
])

texto("trabajo-remoto", "Trabajar desde casa: ¿para quién?", """
La pandemia convirtió el trabajo a distancia en una experiencia masiva. Oficinas enteras se trasladaron a comedores y dormitorios, y muchas empresas descubrieron que buena parte de las tareas podía hacerse sin que los trabajadores se movieran de sus casas. Años después, el debate sigue abierto: ¿se trata de un avance que llegó para quedarse o de una solución de emergencia?

Quienes lo defienden destacan el ahorro de tiempo. En ciudades como Santiago, un trabajador puede pasar más de una hora y media diaria en traslados; trabajar desde casa le devuelve ese tiempo para descansar, estudiar o estar con su familia. Además, señalan, disminuye la congestión y la contaminación.

Los críticos responden que esos beneficios no se distribuyen por igual. Solo una parte de los empleos puede hacerse a distancia: la mayoría de los trabajadores del comercio, la construcción, la salud o el transporte no tienen esa opción. Y entre quienes sí la tienen, no todos cuentan con un espacio adecuado ni con una buena conexión a internet. Para muchas mujeres, además, trabajar en casa significó sumar las tareas domésticas y de cuidado a la jornada laboral, sin una separación clara entre ambas.

Por eso, más que preguntar si el teletrabajo es bueno o malo, convendría preguntar en qué condiciones lo es. Una ley puede garantizar el derecho a desconectarse, exigir que el empleador provea los equipos y fijar límites a la jornada. Sin esas reglas, el trabajo a distancia corre el riesgo de ampliar las desigualdades que prometía reducir.
""", "Texto argumentativo elaborado para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿cuánto tiempo diario puede pasar un trabajador de Santiago en traslados?",
     "Más de una hora y media",
     [("Media hora", "la cifra es mayor"),
      ("Tres horas exactas", "no se menciona esa cifra"),
      ("Más de cinco horas", "no se menciona esa cifra")],
     "El párrafo 2 indica «más de una hora y media diaria en traslados»."),
    (INT, "media", "¿Qué tienen en común los argumentos del párrafo 3?",
     "Muestran que los beneficios del teletrabajo no alcanzan a todos por igual",
     [("Muestran que el teletrabajo reduce la contaminación", "ese es un argumento a favor, del párrafo 2"),
      ("Explican cómo instalar internet en la casa", "no es un instructivo"),
      ("Defienden que el teletrabajo debe prohibirse", "no se propone prohibirlo")],
     "Empleos que no pueden hacerse a distancia, falta de espacio o conexión y doble jornada femenina apuntan a la desigualdad."),
    (INT, "media", "En el párrafo 3, ¿a qué se refiere la idea de «sumar las tareas domésticas y de cuidado a la jornada laboral»?",
     "A que muchas mujeres trabajaron y cuidaron del hogar al mismo tiempo, sin separación clara",
     [("A que las mujeres trabajaron menos horas", "el texto sugiere lo contrario"),
      ("A que las tareas domésticas pasaron a ser pagadas", "no se dice que se pagaran"),
      ("A que los hombres asumieron todo el trabajo doméstico", "no se afirma")],
     "La frase describe una sobrecarga: la casa se volvió a la vez lugar de trabajo y de cuidado."),
    (EVA, "alta", "¿Cuál es la tesis del autor?",
     "El teletrabajo puede ser positivo solo si se regulan sus condiciones",
     [("El teletrabajo es siempre mejor que el trabajo presencial", "el autor matiza sus beneficios"),
      ("El teletrabajo es una solución que debe abandonarse", "no propone abandonarlo"),
      ("El teletrabajo no tiene relación con la desigualdad", "plantea que puede ampliarla")],
     "El párrafo 4 propone preguntar «en qué condiciones» es bueno y sugiere reglas concretas."),
    (EVA, "media", "¿Qué función cumple la pregunta con que termina el párrafo 1?",
     "Plantear el problema que el texto discutirá",
     [("Responder la pregunta del título", "la respuesta llega al final"),
      ("Resumir la conclusión del autor", "la conclusión está en el último párrafo"),
      ("Presentar una anécdota personal", "no es una anécdota")],
     "La pregunta abre el debate que se desarrolla con argumentos a favor, en contra y una propuesta."),
])

texto("instructivo-sismo", "Qué hacer durante un sismo", """
Chile es uno de los países con más actividad sísmica del mundo. Saber cómo actuar antes, durante y después de un terremoto puede reducir el riesgo de lesiones. Las siguientes recomendaciones se basan en las indicaciones de los organismos de emergencia.

Antes. Identifique en su casa, colegio o trabajo los lugares más seguros, lejos de ventanas, repisas y objetos que puedan caer. Fije a la pared los muebles altos y mantenga a mano una mochila de emergencia con agua, linterna, radio a pilas, botiquín y copias de documentos. Acuerde con su familia un punto de encuentro.

Durante. Si está dentro de un edificio, no corra hacia la salida: la mayoría de las lesiones ocurre por la caída de objetos o al intentar moverse. Agáchese, cúbrase la cabeza y el cuello y afírmese de un mueble firme hasta que termine el movimiento. Si está en la calle, aléjese de cables, postes y fachadas. Si está en la costa y el sismo le impide mantenerse en pie, evacúe de inmediato hacia una zona alta, sin esperar una alerta oficial.

Después. Revise si hay personas heridas y aléjese de construcciones dañadas. No use ascensores. Corte el gas si siente olor y no encienda fósforos ni velas. Use el teléfono solo para emergencias, para no saturar las líneas, e infórmese por radio sobre las instrucciones de las autoridades.
""", "Texto instructivo elaborado para este ensayo.", [
    (LOC, "baja", "¿Qué elemento se recomienda incluir en la mochila de emergencia?",
     "Una radio a pilas",
     [("Fósforos y velas", "después del sismo se recomienda no encenderlos"),
      ("Un televisor portátil", "no se menciona"),
      ("Los muebles altos", "deben fijarse a la pared")],
     "El párrafo 2 enumera agua, linterna, radio a pilas, botiquín y copias de documentos."),
    (LOC, "media", "Según el texto, ¿cuándo se debe evacuar hacia una zona alta en la costa?",
     "Si el sismo impide mantenerse en pie, aunque no haya una alerta oficial",
     [("Solo cuando las autoridades lo ordenen", "el texto dice no esperar una alerta oficial"),
      ("Después de revisar si hay heridos", "la evacuación debe ser inmediata"),
      ("Solo si se corta la luz", "no se condiciona a la luz")],
     "El párrafo 3 lo indica para la costa."),
    (INT, "media", "¿Por qué se recomienda no correr hacia la salida durante el sismo?",
     "Porque la mayoría de las lesiones ocurre por la caída de objetos o al moverse",
     [("Porque las puertas se traban siempre", "no se afirma eso"),
      ("Porque es mejor salir después de una hora", "no se indica un tiempo"),
      ("Porque los ascensores son más seguros", "se recomienda no usar ascensores")],
     "La razón aparece en el mismo párrafo, después de la recomendación."),
    (INT, "media", "¿Qué criterio organiza las recomendaciones del texto?",
     "El momento: antes, durante y después del sismo",
     [("La región del país", "no se divide por regiones"),
      ("La edad de las personas", "no se divide por edades"),
      ("La intensidad del sismo", "no se clasifica por intensidad")],
     "Cada párrafo de recomendaciones comienza con «Antes», «Durante» o «Después»."),
    (EVA, "alta", "¿Por qué es adecuado que el texto use verbos en modo imperativo, como «agáchese» o «aléjese»?",
     "Porque su propósito es dar instrucciones claras que se puedan seguir",
     [("Porque busca narrar una experiencia personal", "no es un relato"),
      ("Porque quiere expresar una opinión discutible", "no es un texto de opinión"),
      ("Porque así evita entregar información concreta", "entrega información concreta")],
     "El imperativo es propio de los textos instructivos, que orientan una acción.")
])
